import logging
import os
import re
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel

from app.ai.web_search import web_search
from app.ai.loader import load_pdf
from app.ai.vectorstore import create_vector_store
from app.ai.rag import get_rag_chain
from app.ai.language import detect_language
from app.ai.memory import memory
from app.core.dependencies import get_current_user

from app.db.database import SessionLocal
from app.models.chat_history import ChatHistory

logger = logging.getLogger(__name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DOCUMENTS_DIR = os.path.join(BASE_DIR, "documents")

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
    dependencies=[Depends(get_current_user)]
)


class QuestionRequest(BaseModel):
    question: str


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def clean_text(text: str) -> str:

    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


async def validate_pdf_upload(file: UploadFile) -> None:

    filename = file.filename or ""
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are accepted."
        )

    content_type = (file.content_type or "").lower()
    if content_type and content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are accepted."
        )

    try:
        header = await file.read(8)
        await file.seek(0)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to read uploaded file."
        )

    if not header.startswith(b"%PDF"):
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is not a valid PDF."
        )


def build_sources(docs):
    sources = []
    seen = set()

    for doc in docs:
        metadata = doc.metadata or {}

        filename = (
            metadata.get("filename")
            or metadata.get("source")
            or "Uploaded document"
        )

        page = metadata.get("page")

        if isinstance(page, int):
            page_number = page + 1
        else:
            page_number = None

        key = (filename, page_number)

        if key in seen:
            continue

        seen.add(key)

        source = {
            "file": os.path.basename(str(filename)),
        }

        if page_number is not None:
            source["page"] = page_number

        sources.append(source)

    return sources


def build_context(docs):
    context_parts = []
    seen_chunks = set()

    for index, doc in enumerate(docs, start=1):
        text = clean_text(doc.page_content)

        if not text:
            continue

        normalized = text.lower()

        if normalized in seen_chunks:
            continue

        seen_chunks.add(normalized)

        metadata = doc.metadata or {}

        filename = (
            metadata.get("filename")
            or metadata.get("source")
            or "Uploaded document"
        )

        page = metadata.get("page")

        if isinstance(page, int):
            page_label = page + 1
        else:
            page_label = "Unknown"

        context_parts.append(
            f"[SOURCE {index} | FILE: {os.path.basename(str(filename))} | PAGE: {page_label}]\\n"
            f"{text}"
        )

    return "\\n\\n".join(context_parts)


def document_fallback_answer(
    question: str,
    context: str,
    history: str
) -> str:

    q = question.lower().strip()

    # -----------------------------------------------------
    # GENERAL KNOWLEDGE QUESTIONS
    # -----------------------------------------------------

    general_patterns = [

        # Basic / conversational knowledge
        "what is ",
        "what are ",
        "who is ",
        "who are ",
        "where is ",
        "where are ",
        "when is ",
        "when was ",
        "when did ",
        "why ",
        "how ",
        "how does ",
        "how do ",
        "how can ",
        "how to ",
        "explain ",
        "define ",
        "definition of ",
        "meaning of ",
        "example of ",
        "examples of ",
        "difference between ",
        "compare ",
        "comparison between ",
        "advantages of ",
        "disadvantages of ",
        "uses of ",
        "types of ",
        "features of ",
        "benefits of ",

        # Mathematics
        "math",
        "mathematics",
        "algebra",
        "geometry",
        "trigonometry",
        "calculus",
        "probability",
        "statistics",
        "permutation",
        "combination",
        "matrix",
        "matrices",
        "determinant",
        "derivative",
        "integral",
        "limit",
        "logarithm",
        "equation",
        "quadratic",
        "linear equation",
        "prime number",
        "percentage",
        "ratio",
        "proportion",
        "average",
        "mean",
        "median",
        "mode",
        "variance",
        "standard deviation",
        "factorial",
        "fibonacci",
        "area",
        "volume",
        "perimeter",

        # Computer Science
        "computer science",
        "programming",
        "coding",
        "algorithm",
        "data structure",
        "array",
        "string",
        "linked list",
        "doubly linked list",
        "stack",
        "queue",
        "deque",
        "hashmap",
        "hash map",
        "hash table",
        "heap",
        "tree",
        "binary tree",
        "binary search tree",
        "graph",
        "recursion",
        "dynamic programming",
        "greedy algorithm",
        "sorting",
        "searching",
        "binary search",
        "linear search",
        "time complexity",
        "space complexity",
        "big o",
        "oops",
        "object oriented",
        "object oriented programming",
        "class",
        "object",
        "inheritance",
        "polymorphism",
        "encapsulation",
        "abstraction",

        # Programming languages
        "python",
        "java",
        "c++",
        "c language",
        "javascript",
        "typescript",
        "html",
        "css",
        "react",
        "next.js",
        "node.js",
        "sql",

        # Databases
        "database",
        "dbms",
        "mysql",
        "postgresql",
        "mongodb",
        "nosql",
        "normalization",
        "primary key",
        "foreign key",
        "join",
        "indexing",
        "transaction",
        "acid",

        # AI / ML / Data Science
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "data science",
        "data analytics",
        "data analysis",
        "neural network",
        "cnn",
        "rnn",
        "transformer",
        "llm",
        "large language model",
        "generative ai",
        "natural language processing",
        "nlp",
        "computer vision",
        "reinforcement learning",
        "supervised learning",
        "unsupervised learning",
        "classification",
        "regression",
        "clustering",
        "overfitting",
        "underfitting",
        "training",
        "testing",
        "dataset",
        "feature engineering",

        # Web / Software
        "web development",
        "frontend",
        "backend",
        "full stack",
        "api",
        "rest api",
        "http",
        "https",
        "json",
        "xml",
        "git",
        "github",
        "software engineering",
        "software development",
        "debugging",
        "framework",
        "library",

        # Cybersecurity / Networking
        "cybersecurity",
        "cyber security",
        "networking",
        "network",
        "ip address",
        "dns",
        "tcp",
        "udp",
        "firewall",
        "malware",
        "virus",
        "phishing",
        "encryption",
        "decryption",
        "authentication",
        "authorization",
        "vpn",
        "cloud computing",

        # Science
        "physics",
        "chemistry",
        "biology",
        "science",
        "atom",
        "molecule",
        "energy",
        "force",
        "gravity",
        "electricity",
        "magnetism",
        "cell",
        "dna",
        "evolution",
        "photosynthesis",

        # General knowledge
        "history",
        "geography",
        "politics",
        "government",
        "economics",
        "economy",
        "business",
        "finance",
        "technology",
        "space",
        "planet",
        "earth",
        "universe",
        "country",
        "capital",
        "language",
        "culture",
        "education",
        "career",
        "interview",
        "current affairs",
        "general knowledge",
        "gk",
    ]

# -----------------------------------------------------
# DOCUMENT-SPECIFIC QUESTIONS HAVE PRIORITY
# -----------------------------------------------------

    document_keywords = [
        "my ",
        "me ",
        "i ",
        "i'm ",
        "i am ",
        "myself",
        "resume",
        "cv",
        "cgpa",
        "gpa",
        "college",
        "university",
        "degree",
        "education",
        "qualification",
        "skills",
        "skill",
        "project",
        "projects",
        "experience",
        "internship",
        "internships",
        "leetcode",
        "dsa",
        "certification",
        "certifications",
        "achievement",
        "achievements",
        "phone",
        "email",
        "address",
        "contact",
    ]

    is_document_question = any(
        keyword in q
        for keyword in document_keywords
    )

    # General knowledge questions go to the LLM.
    # Personal/document questions use the uploaded document.
    if not is_document_question:
        if any(
            pattern in q
            for pattern in general_patterns
        ):
            return None

    context_clean = clean_text(context)
    # -----------------------------------------------------
    # CGPA
    # -----------------------------------------------------

    if (
        "cgpa" in q
        or "grade point" in q
    ):

        match = re.search(
            r"(\d+(?:\.\d+)?)\s*(?:/|out of)\s*10",
            context_clean,
            re.IGNORECASE
        )

        if match:

            return (
                f"Your CGPA is **{match.group(1)} / 10**."
            )

    # -----------------------------------------------------
    # DSA
    # -----------------------------------------------------

    if (
        "dsa" in q
        or "data structure" in q
        or "leetcode" in q
        or "problems have i solved" in q
    ):

        match = re.search(
            r"(\d+)\+?\s*(?:DSA\s*)?(?:problems|questions)",
            context_clean,
            re.IGNORECASE
        )

        if match:

            return (
                f"You have solved **{match.group(1)}+ DSA problems** "
                "on LeetCode."
            )

    # -----------------------------------------------------
    # PROJECTS
    # -----------------------------------------------------
    # Project names are intentionally NOT hard-coded.
    # Project questions are answered by the RAG/LLM
    # using the currently uploaded document.
    # -----------------------------------------------------

    # -----------------------------------------------------
    # -----------------------------------------------------
    # FOLLOW-UP: NUMBERING
    # -----------------------------------------------------

    # Do not hard-code project names here.
    # Let the LLM use conversation history and document context.
    if (
        "numbering" in q
        or "numbered" in q
        or "number me" in q
        or "number mein" in q
        or "numbering mein" in q
    ):
        return None
    # -----------------------------------------------------
    # EDUCATION / EXPERIENCE
    # -----------------------------------------------------

    # These questions are intentionally handled by the LLM
    # using the retrieved resume/document context.
    # No personal information is hard-coded here.

# FAVORITE FOOD / UNKNOWN PERSONAL INFO
    # -----------------------------------------------------

    if (
        "favorite food" in q
        or "favourite food" in q
    ):

        if not re.search(
            r"favorite food|favourite food",
            context_clean,
            re.IGNORECASE
        ):

            return (
                "I don't know based on the uploaded document."
            )

    # -----------------------------------------------------
    # GENERIC FALLBACK
    # -----------------------------------------------------

    return None


# =========================================================
# PDF UPLOAD
# =========================================================

@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    logger.info("AI PDF upload request received")

    await validate_pdf_upload(file)

    os.makedirs(
        DOCUMENTS_DIR,
        exist_ok=True
    )

    safe_filename = f"{uuid.uuid4().hex}.pdf"
    file_path = os.path.join(
        DOCUMENTS_DIR,
        safe_filename
    )

    try:
        contents = await file.read()

        if not contents:
            raise HTTPException(
                status_code=400,
                detail="Uploaded PDF is empty."
            )

        with open(
            file_path,
            "wb"
        ) as f:
            f.write(contents)

        chunks = load_pdf(
            file_path
        )

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="Uploaded PDF contains no readable content."
            )

        create_vector_store(
            chunks
        )

        logger.info("PDF uploaded and indexed successfully: %s", safe_filename)

        return {
            "success": True,
            "message": "PDF uploaded and indexed successfully.",
            "filename": safe_filename,
            "chunks": len(chunks)
        }

    except HTTPException:
        raise

    except Exception:
        logger.exception("PDF upload failed")
        raise HTTPException(
            status_code=500,
            detail="PDF upload failed due to a server error."
        )



# =========================================================
# WEB SEARCH DECISION
# =========================================================

def should_use_web_search(question: str) -> bool:
    q = question.lower().strip()

    web_patterns = [
        "latest",
        "today",
        "current",
        "currently",
        "recent",
        "recently",
        "news",
        "price",
        "weather",
        "stock",
        "who is the ceo",
        "who is current",
        "new version",
        "latest version",
        "2026",
        "search the web",
        "search online",
        "internet",
        "online",
    ]

    return any(pattern in q for pattern in web_patterns)

# =========================================================
# ASK AI
# =========================================================

@router.post("/ask")
def ask_question(
    data: QuestionRequest
):
    logger.info("AI ask request received")

    question = data.question.strip()
    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    user_language = detect_language(question)
    logger.debug("Detected language: %s", user_language)

    try:
        retriever, llm = get_rag_chain()
    except FileNotFoundError:
        logger.warning("Vector store not found for AI ask request")
        raise HTTPException(
            status_code=503,
            detail="Knowledge base not available. Please upload a PDF first."
        )
    except Exception:
        logger.exception("Failed to initialize AI pipeline")
        raise HTTPException(
            status_code=503,
            detail="AI service is currently unavailable."
        )

    try:
        docs = retriever.invoke(question)
    except Exception:
        logger.exception("Document retrieval failed")
        raise HTTPException(
            status_code=503,
            detail="AI retrieval failed. Please try again later."
        )

    if not docs:
        logger.info("No documents were retrieved for the question")
        docs = []

    context = build_context(docs)

    document_keywords = [
        "my ",
        "me ",
        "resume",
        "cv",
        "cgpa",
        "gpa",
        "college",
        "university",
        "degree",
        "education",
        "qualification",
        "skills",
        "skill",
        "project",
        "projects",
        "experience",
        "internship",
        "internships",
        "leetcode",
        "dsa",
        "certification",
        "certifications",
        "achievement",
        "achievements",
        "phone",
        "email",
        "address",
        "contact",
    ]

    is_document_question = any(
        keyword in question.lower()
        for keyword in document_keywords
    )

    sources = build_sources(docs) if is_document_question else []

    history = memory.format_history(max_messages=10)
    conversation_context = memory.get_conversation_context(max_messages=6)

    fallback_answer = document_fallback_answer(
        question,
        context,
        history
    )

    if fallback_answer:
        answer = fallback_answer
        logger.debug("Using document fallback answer")
    else:
        web_results = []
        try:
            web_results = web_search(question, max_results=5)
            logger.debug("Web search returned %d results", len(web_results))
        except Exception:
            logger.exception("Web search failed")
            web_results = []

        web_context = ""
        if web_results:
            web_parts = []
            for index, result in enumerate(web_results, start=1):
                title = result.get("title", "").strip()
                url = result.get("url", "").strip()
                snippet = result.get("snippet", "").strip()
                web_parts.append(
                    f"{index}. {title}\n"
                    f"URL: {url}\n"
                    f"Snippet: {snippet}"
                )
            web_context = "\n\n".join(web_parts)

        prompt = f"""
You are NEXUS ONE AI Assistant.

You can answer two types of questions.

TYPE 1 - DOCUMENT / PERSONAL QUESTIONS:
Questions about the user's resume, CGPA, education, college,
degree, projects, skills, experience, internship, achievements,
contact details, or other personal information.

For these questions:
- Use the uploaded document as the source of truth.
- Never invent personal information.
- If the information exists in the document, answer directly.
- If the information truly does not exist, say:
  "I don't know based on the uploaded document."

TYPE 2 - GENERAL KNOWLEDGE QUESTIONS:
Questions such as "What is an array?", "Explain binary search",
"What is Python?", "What is AI?", mathematics, science,
programming concepts, and other normal knowledge questions.

For these questions:
- Answer using your general knowledge.
- Do NOT require the answer to exist in the uploaded document.
- Give a clear and concise explanation.
- Never say "I don't know based on the uploaded document"
  for a normal general-knowledge question.

            CONVERSATION RULES:

            1. Use conversation history for follow-up questions.
            2. Resolve "it", "this", "that", "they", "them", "these", and "those"
               using the most recent relevant conversation topic.
            3. If the previous topic was the user document, continue using that topic.
            4. If the user asks "Is it good?", evaluate the most recent relevant conversation topic.
            5. If the user asks a multi-part question, answer EVERY part of the question.
            6. Never answer only the first part of a multi-part question.
            7. Do not switch to an unrelated older conversation topic.

            LANGUAGE RULES:

            The value USER LANGUAGE is authoritative.

            - If USER LANGUAGE is Hindi, the FINAL ANSWER MUST be written in Hindi
              using Devanagari script.
            - If USER LANGUAGE is English, the FINAL ANSWER MUST be written in English.
            - If USER LANGUAGE is Tamil, the FINAL ANSWER MUST be written in Tamil script.
            - If USER LANGUAGE is Telugu, the FINAL ANSWER MUST be written in Telugu script.
            - If USER LANGUAGE is Kannada, the FINAL ANSWER MUST be written in Kannada script.
            - If USER LANGUAGE is Malayalam, the FINAL ANSWER MUST be written in Malayalam script.
            - If USER LANGUAGE is Bengali, the FINAL ANSWER MUST be written in Bengali script.
            - If USER LANGUAGE is Marathi, the FINAL ANSWER MUST be written in Devanagari script.
            - If USER LANGUAGE is Gujarati, the FINAL ANSWER MUST be written in Gujarati script.
            - If USER LANGUAGE is Punjabi, the FINAL ANSWER MUST be written in Gurmukhi script.
            - If USER LANGUAGE is Japanese, the FINAL ANSWER MUST be written in Japanese.
            - If USER LANGUAGE is French, the FINAL ANSWER MUST be written in French.
            - If USER LANGUAGE is Spanish, the FINAL ANSWER MUST be written in Spanish.
            - If USER LANGUAGE is Sanskrit, the FINAL ANSWER MUST be written in Devanagari script.

            CRITICAL LANGUAGE CHECK:
            Before producing the FINAL ANSWER, check the USER LANGUAGE.
            NEVER answer a Hindi question in English.
            NEVER answer a Tamil question in English.
            NEVER answer a Telugu question in English.
            NEVER answer a Kannada question in English.
            NEVER answer a Malayalam question in English.
            NEVER answer a Bengali question in English.
            NEVER answer a Marathi question in English.
            NEVER answer a Gujarati question in English.
            NEVER answer a Punjabi question in English.
            NEVER translate a non-English question into English for the final answer.
            Keep proper nouns, project names, technology names, numbers, and technical
            terms unchanged when appropriate, but explain the surrounding answer in
            the required language.

            GENERAL KNOWLEDGE RULES:

            - Normal general-knowledge questions may be answered from general knowledge.
            - Do NOT require normal general-knowledge answers to exist in the uploaded document.
            - Never say "I dont know based on the uploaded document" for a normal knowledge question.

            FOLLOW-UP RESOLUTION RULES:

            - Prefer the immediately preceding relevant question and answer.
            - If the immediately preceding message is itself a follow-up, trace it back
              to the original topic.
            - Do not invent information that is not supported by the conversation or document.
            - When a follow-up refers to a document topic, use BOTH conversation history
              and document context.

            USER LANGUAGE:

            {user_language}

            DOCUMENT CONTEXT:

            {context}

            USER QUESTION:

            {question}

            ANSWER:
            """

        try:
            response = llm.invoke(prompt)
        except Exception:
            logger.exception("LLM invocation failed")
            raise HTTPException(
                status_code=503,
                detail="AI model invocation failed. Please try again later."
            )

        answer = getattr(response, "content", None)
        if not isinstance(answer, str):
            logger.warning("LLM returned a non-string response")
            raise HTTPException(
                status_code=503,
                detail="AI service returned an invalid response."
            )

        replacements = {
            "???": "?",
            "??": "?",
            "? ": " ",
        }
        for bad, good in replacements.items():
            answer = answer.replace(bad, good)

        answer = answer.replace("NEXUS ONE ? AI", "NEXUS ONE ? AI")
        answer = answer.replace("NEXUS ONE ??? AI", "NEXUS ONE ? AI")
        answer = answer.replace("NEXUS ONE - AI", "NEXUS ONE ? AI")

        if answer == "GEMINI_QUOTA_EXCEEDED":
            is_document_question = any(
                keyword in question.lower()
                for keyword in [
                    "my ",
                    "myself",
                    "resume",
                    "cv",
                    "cgpa",
                    "gpa",
                    "college",
                    "university",
                    "degree",
                    "education",
                    "qualification",
                    "skills",
                    "skill",
                    "project",
                    "projects",
                    "experience",
                    "internship",
                    "internships",
                    "leetcode",
                    "dsa",
                    "certification",
                    "certifications",
                    "achievement",
                    "achievements",
                    "phone",
                    "email",
                    "address",
                    "contact",
                ]
            )
            if is_document_question:
                fallback_answer = document_fallback_answer(
                    question,
                    context,
                    history
                )
                if fallback_answer:
                    answer = fallback_answer
                else:
                    answer = (
                        "I don't know based on the uploaded document."
                    )
            else:
                answer = (
                    "General knowledge is temporarily unavailable "
                    "because the AI model quota has been exhausted. "
                    "Please try again later."
                )
        elif answer == "GEMINI_AUTH_ERROR":
            answer = (
                "AI service authentication failed. "
                "Please check the AI provider configuration."
            )
        elif answer == "GEMINI_SERVICE_ERROR":
            answer = (
                "AI service is temporarily unavailable. "
                "Please try again later."
            )

        if not answer or not answer.strip():
            logger.warning("AI answer was empty after LLM invocation")
            raise HTTPException(
                status_code=503,
                detail="AI service returned an empty response. Please try again later."
            )

    memory.add_message("user", question)
    memory.add_message("assistant", answer)

    db = SessionLocal()
    try:
        db.add(
            ChatHistory(
                user_id=None,
                role="user",
                content=question
            )
        )
        db.add(
            ChatHistory(
                user_id=None,
                role="assistant",
                content=answer
            )
        )
        db.commit()
    except Exception:
        db.rollback()
        logger.exception("Failed to save chat history")
    finally:
        db.close()

    return {
        "success": True,
        "question": question,
        "language": user_language,
        "answer": answer,
        "sources": sources
    }


# =========================================================
# CHAT HISTORY
# =========================================================

@router.get("/history")
def get_chat_history():

    db = SessionLocal()

    try:

        rows = (
            db.query(ChatHistory)
            .order_by(
                ChatHistory.id.asc()
            )
            .all()
        )

        return {
            "success": True,
            "history": [
                {
                    "id": row.id,
                    "role": row.role,
                    "content": row.content,
                    "created_at": (
                        row.created_at.isoformat()
                        if row.created_at
                        else None
                    )
                }
                for row in rows
            ]
        }

    except Exception:

        logger.exception("Failed to load chat history")

        raise HTTPException(
            status_code=500,
            detail="Unable to load chat history at this time."
        )

    finally:

        db.close()


# =========================================================
# CLEAR IN-MEMORY CHAT
# =========================================================

@router.delete("/memory")
def clear_memory():

    memory.clear()

    return {        "success": True,
        "message": "Chat memory cleared."
    }

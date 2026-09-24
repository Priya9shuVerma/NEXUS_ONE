# NEXUS ONE 🚀

> **AI-Powered Enterprise Intelligence & Cyber Defense Platform**

NEXUS ONE is a full-stack AI platform designed to combine **Artificial Intelligence, Retrieval-Augmented Generation (RAG), cybersecurity, authentication, data management, and cloud-ready application architecture** into a single enterprise-oriented system.

The platform allows users to securely interact with documents using AI, manage their profiles, and provides administrators with user-management and audit capabilities.

---

## ✨ Key Features

### 🤖 AI & RAG

- AI-powered question answering
- Retrieval-Augmented Generation (RAG)
- PDF/document ingestion
- Semantic document search
- FAISS vector database
- Hugging Face sentence-transformer embeddings
- LangChain integration
- Groq-powered LLM responses
- Context-aware answers based on uploaded documents

### 🔐 Authentication & Security

- JWT-based authentication
- Access-token based authorization
- Refresh-token support
- Secure password handling
- Role-Based Access Control (RBAC)
- User and Admin roles
- User enable/disable management
- Password change functionality
- Audit-log support
- Protected API endpoints

### 👤 User Management

- User registration
- User login
- User profile management
- Get current authenticated user
- Update user information
- Admin user management
- Enable/disable users
- Promote user to Admin
- Change Admin back to User
- Delete users

### 🛡️ Cybersecurity Architecture

NEXUS ONE is designed with security-focused architecture including:

- Authentication and authorization
- RBAC-based access control
- Security-oriented API structure
- Audit logging
- Secure token management
- Cloud-security-ready architecture

### ☁️ Cloud & Infrastructure Ready

The platform is designed to support containerized and cloud-ready deployment using:

- Docker
- PostgreSQL
- Redis
- FastAPI
- Next.js
- REST APIs

---

# 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │      NEXUS ONE       │
                    │   Enterprise AI      │
                    │   & Cyber Defense    │
                    └──────────┬───────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
        ┌───────▼────────┐           ┌────────▼────────┐
        │   Next.js      │           │    FastAPI      │
        │   Frontend     │◄─────────►│    Backend      │
        └────────────────┘           └────────┬────────┘
                                              │
                         ┌────────────────────┼────────────────────┐
                         │                    │                    │
                  ┌──────▼──────┐      ┌──────▼──────┐      ┌─────▼─────┐
                  │ PostgreSQL  │      │    Redis    │      │   SQLite  │
                  │  Database   │      │    Cache    │      │  Local DB │
                  └─────────────┘      └─────────────┘      └───────────┘
                                              │
                                      ┌───────▼────────┐
                                      │    AI / RAG     │
                                      └───────┬────────┘
                                              │
                         ┌────────────────────┼───────────────────┐
                         │                    │                   │
                  ┌──────▼──────┐      ┌──────▼──────┐     ┌──────▼──────┐
                  │  LangChain  │      │    FAISS    │     │    Groq     │
                  │    RAG      │      │ Vector DB   │     │     LLM     │
                  └─────────────┘      └─────────────┘     └─────────────┘
```

---

# 🛠️ Tech Stack

## Backend

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- JWT Authentication
- REST APIs

## Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS

## AI / Machine Learning

- LangChain
- LangChain Community
- Hugging Face
- Sentence Transformers
- FAISS
- RAG
- Groq LLM

## Database & Storage

- SQLite for local development
- PostgreSQL for production/containerized deployment
- Redis for caching and supporting application services
- FAISS for vector storage

## Security

- JWT
- RBAC
- Password hashing
- Access control
- Audit logs
- Protected API routes

## Infrastructure

- Docker
- Docker Compose
- REST APIs
- Cloud-ready architecture

---

# 📁 Project Structure

```text
NEXUS_ONE/
│
├── backend/
│   │
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── admin.py
│   │   │   └── ai.py
│   │   │
│   │   ├── ai/
│   │   │   ├── embeddings.py
│   │   │   ├── document_loader.py
│   │   │   ├── ingest.py
│   │   │   ├── llm.py
│   │   │   ├── rag.py
│   │   │   └── vectorstore.py
│   │   │
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── core/
│   │   └── main.py
│   │
│   ├── data/
│   ├── documents/
│   ├── vector_db/
│   ├── nexus_one.db
│   ├── .env
│   └── requirements.txt
│
├── frontend/
│
├── docs/
│
├── docker/
│
├── README.md
└── .gitignore
```

---

# 🔌 API Modules

NEXUS ONE currently exposes REST APIs for:

## Authentication

```text
POST /auth/register
POST /auth/login
POST /auth/refresh-token
POST /auth/logout

GET  /auth/me
PUT  /auth/profile
PUT  /auth/change-password
```

## Users

```text
GET    /users/
GET    /users/all
GET    /users/{user_id}
PUT    /users/{user_id}
DELETE /users/{user_id}
```

## Administration

```text
GET    /admin/
GET    /admin/stats
GET    /admin/dashboard
GET    /admin/users

PUT    /admin/disable-user/{user_id}
PUT    /admin/enable-user/{user_id}

PUT    /admin/make-admin/{user_id}
PUT    /admin/make-user/{user_id}

DELETE /admin/delete-user/{user_id}

GET    /admin/audit-logs
```

## AI / RAG

```text
POST /ai/ask
```

Example request:

```json
{
  "question": "What is this document about?"
}
```

---

# 🧠 RAG Pipeline

The AI module follows a document-based RAG pipeline:

```text
PDF / Document
      │
      ▼
Document Loader
      │
      ▼
Text Extraction
      │
      ▼
Document Chunks
      │
      ▼
Sentence Transformer
      │
      ▼
Embeddings
      │
      ▼
FAISS Vector Store
      │
      ▼
Similarity Search
      │
      ▼
Relevant Context
      │
      ▼
Groq LLM
      │
      ▼
AI Generated Answer
```

This allows NEXUS ONE to answer questions using information retrieved from the indexed documents instead of relying only on the language model's general knowledge.

---

# ⚙️ Local Development

## 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd NEXUS_ONE
```

## 2. Create / activate virtual environment

### Windows

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

## 3. Install backend dependencies

```powershell
cd backend
pip install -r requirements.txt
```

## 4. Configure environment variables

Create:

```text
backend/.env
```

Example:

```env
APP_NAME=NEXUS ONE

DATABASE_URL=sqlite:///./nexus_one.db

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60

GROQ_API_KEY=your_groq_api_key
```

> Never commit `.env` or API keys to GitHub.

---

# ▶️ Run Backend

From the `backend` directory:

```powershell
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

OpenAPI specification:

```text
http://127.0.0.1:8000/openapi.json
```

---

# 📄 Document Ingestion

Place a PDF document inside:

```text
backend/data/
```

Run the ingestion module:

```powershell
python -m app.ai.ingest
```

The generated FAISS vector store is saved inside:

```text
backend/vector_db/
```

---

# 🧪 AI Testing

Open:

```text
http://127.0.0.1:8000/docs
```

Navigate to:

```text
AI → POST /ai/ask
```

Example:

```json
{
  "question": "Summarize the uploaded document."
}
```

The system retrieves relevant document chunks from FAISS and sends the retrieved context to the configured LLM.

---

# 🐳 Docker

NEXUS ONE is designed for containerized deployment.

Example services:

```text
Frontend
   │
   ▼
FastAPI Backend
   │
   ├── PostgreSQL
   │
   ├── Redis
   │
   └── AI / RAG Engine
```

Docker can be used to provide reproducible development and deployment environments.

---

# 🔒 Security Considerations

The project follows security-oriented development practices including:

- JWT-based authentication
- Role-Based Access Control
- Protected API endpoints
- Password hashing
- Token expiration
- User activation/deactivation
- Administrative authorization
- Audit logging
- Environment-based secret management
- Separation of frontend and backend services

API keys and secrets should always be stored in environment variables rather than source code.

---

# 🚀 Future Enhancements

Planned / extensible capabilities include:

- Multi-document RAG
- Conversational AI memory
- AI chat history
- Advanced document management
- Redis-based caching
- PostgreSQL production deployment
- Cloud resource management
- Just-In-Time (JIT) access
- Just-Enough-Administration (JEA)
- Security event monitoring
- Advanced cybersecurity analytics
- Cloud IAM integration
- Multilingual AI interactions
- Enterprise analytics dashboard

---

# 🎯 Project Objective

NEXUS ONE aims to provide a unified platform where **AI intelligence, secure application architecture, document-based knowledge retrieval, user management, and cybersecurity capabilities** can work together.

The project is designed as a practical demonstration of:

- Full-stack development
- Backend engineering
- REST API development
- AI/RAG systems
- Vector databases
- Authentication & authorization
- Database management
- Cybersecurity architecture
- Containerization
- Cloud-ready application design

---

# 👨‍💻 Author

**Priyanshu Kumar Verma**

B.Tech – Computer Science Engineering (Data Science)

NEXUS ONE — AI-Powered Enterprise Intelligence & Cyber Defense Platform

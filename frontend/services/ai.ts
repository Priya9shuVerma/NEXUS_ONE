import api from "./api";

export const askAI = async (question: string) => {
  const response = await api.post("/ai/ask", {
    question,
  });

  return response.data;
};

export const uploadPDF = async (file: File) => {
  if (!file) {
    throw new Error("No PDF file selected.");
  }

  if (!file.name.toLowerCase().endsWith(".pdf")) {
    throw new Error("Only PDF files are allowed.");
  }

  const token = localStorage.getItem("access_token");

  if (!token) {
    throw new Error("Authentication required. Please login again.");
  }

  const formData = new FormData();
  formData.append("file", file, file.name);

  const response = await fetch("http://127.0.0.1:8000/ai/upload", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  });

  let data: any = null;

  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    const detail =
      data?.detail ||
      data?.message ||
      `Upload failed with status ${response.status}`;

    throw new Error(
      Array.isArray(detail)
        ? detail.map((item: any) => item?.msg || String(item)).join(", ")
        : String(detail)
    );
  }

  return data;
};

export const getChatHistory = async () => {
  const response = await api.get("/ai/history");

  return response.data;
};

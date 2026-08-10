import api from "./api";

export const askAI = async (question: string) => {

const response = await api.post("/ai/ask", {
question,
});

return response.data;
};

export const uploadPDF = async (file: File) => {

const formData = new FormData();

formData.append("file", file);

const response = await api.post(
"/ai/upload",
formData,
{
headers: {
"Content-Type": "multipart/form-data",
},
}
);

return response.data;
};

export const getChatHistory = async () => {

const response = await api.get(
"/ai/history"
);

return response.data;
};

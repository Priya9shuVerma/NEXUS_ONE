import api from "./api";


// Login API
export const loginUser = async ({
  email,
  password,
}: {
  email: string;
  password: string;
}) => {

  const response = await api.post("/auth/login", {
    email,
    password,
  });

  localStorage.setItem(
    "access_token",
    response.data.access_token
  );

  return response.data;
};


// Register API
export const registerUser = async ({
  username,
  email,
  password,
}: {
  username: string;
  email: string;
  password: string;
}) => {

  const response = await api.post("/auth/register", {
    username,
    email,
    password,
  });

  return response.data;
};


// Logout
export const logoutUser = () => {

  localStorage.removeItem(
    "access_token"
  );

};
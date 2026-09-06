import api from "./api";

// ------------------------------------------------------------
// Login
// ------------------------------------------------------------

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

  localStorage.setItem("access_token", response.data.access_token);

  if (response.data.refresh_token) {
    localStorage.setItem("refresh_token", response.data.refresh_token);
  }

  return response.data;
};

// ------------------------------------------------------------
// Register
// ------------------------------------------------------------

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

// ------------------------------------------------------------
// Current Profile
// GET /auth/me
// ------------------------------------------------------------

export const getProfile = async () => {
  const response = await api.get("/auth/me");
  return response.data;
};

// ------------------------------------------------------------
// Update Profile
// PUT /auth/profile
// ------------------------------------------------------------

export const updateProfile = async ({
  full_name,
  phone,
  bio,
  profile_image,
}: {
  full_name?: string;
  phone?: string;
  bio?: string;
  profile_image?: string;
}) => {
  const response = await api.put("/auth/profile", {
    full_name,
    phone,
    bio,
    profile_image,
  });

  return response.data;
};

// ------------------------------------------------------------
// Change Password
// PUT /auth/change-password
// ------------------------------------------------------------

export const changePassword = async ({
  old_password,
  new_password,
}: {
  old_password: string;
  new_password: string;
}) => {
  const response = await api.put("/auth/change-password", {
    old_password,
    new_password,
  });

  return response.data;
};

// ------------------------------------------------------------
// Forgot Password
// POST /auth/forgot-password
// ------------------------------------------------------------

export const forgotPassword = async ({
  email,
}: {
  email: string;
}) => {
  const response = await api.post("/auth/forgot-password", {
    email,
  });

  return response.data;
};

// ------------------------------------------------------------
// Reset Password
// POST /auth/reset-password
// ------------------------------------------------------------

export const resetPassword = async ({
  token,
  new_password,
}: {
  token: string;
  new_password: string;
}) => {
  const response = await api.post("/auth/reset-password", {
    token,
    new_password,
  });

  return response.data;
};

// ------------------------------------------------------------
// Logout
// POST /auth/logout
// ------------------------------------------------------------

export const logoutUser = async () => {
  const refreshToken = localStorage.getItem("refresh_token");

  try {
    if (refreshToken) {
      await api.post("/auth/logout", {
        refresh_token: refreshToken,
      });
    }
  } finally {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  }
};

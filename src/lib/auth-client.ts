import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.REACT_APP_BACKEND_URL || "http://localhost:8000",
});

export const { signUp, signIn, signOut, useSession } = authClient;

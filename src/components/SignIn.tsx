import React, { useState } from "react";
import styles from "./SignIn.module.css";

const backendUrl = "http://127.0.0.1:8000";

interface SignInFormData {
  email: string;
  password: string;
}

export default function SignIn({ onSignInSuccess }: { onSignInSuccess?: () => void }) {
  const [formData, setFormData] = useState<SignInFormData>({
    email: "",
    password: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess(false);

    setLoading(true);

    try {
      const response = await fetch(`${backendUrl}/auth/signin`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (data.success) {
        setSuccess(true);
        // Store token in localStorage
        if (data.token) {
          localStorage.setItem("auth_token", data.token);
          localStorage.setItem("user_id", data.user.id);
        }
        // Reset form
        setFormData({
          email: "",
          password: "",
        });
        // Trigger callback
        if (onSignInSuccess) {
          setTimeout(onSignInSuccess, 1500);
        }
      } else {
        setError(data.message || "Sign in failed");
      }
    } catch (err) {
      setError(`Error: ${err instanceof Error ? err.message : "Unknown error"}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.formWrapper}>
        <h2>Welcome Back</h2>
        <p className={styles.subtitle}>Sign in to your account</p>

        {error && <div className={styles.error}>{error}</div>}
        {success && <div className={styles.success}>✓ Signed in successfully! Redirecting...</div>}

        <form onSubmit={handleSubmit} className={styles.form}>
          {/* Email */}
          <div className={styles.formGroup}>
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              required
              value={formData.email}
              onChange={handleInputChange}
              placeholder="your.email@example.com"
              disabled={loading}
            />
          </div>

          {/* Password */}
          <div className={styles.formGroup}>
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              required
              value={formData.password}
              onChange={handleInputChange}
              placeholder="Your password"
              disabled={loading}
            />
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            className={styles.submitButton}
            disabled={loading}
          >
            {loading ? "Signing In..." : "Sign In"}
          </button>

          <p className={styles.signupLink}>
            Don't have an account? <a href="/signup">Create one here</a>
          </p>
        </form>
      </div>
    </div>
  );
}

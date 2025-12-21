import React, { useState } from "react";
import styles from "./SignUp.module.css";

const backendUrl = "http://127.0.0.1:8000";

interface SignUpFormData {
  email: string;
  password: string;
  confirmPassword: string;
  softwareBackground: string;
  hardwareExperience: string;
  programmingLanguages: string[];
  learningGoal: string;
}

export default function SignUp({ onSignUpSuccess }: { onSignUpSuccess?: () => void }) {
  const [formData, setFormData] = useState<SignUpFormData>({
    email: "",
    password: "",
    confirmPassword: "",
    softwareBackground: "beginner",
    hardwareExperience: "low",
    programmingLanguages: [],
    learningGoal: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleLanguageToggle = (lang: string) => {
    setFormData((prev) => ({
      ...prev,
      programmingLanguages: prev.programmingLanguages.includes(lang)
        ? prev.programmingLanguages.filter((l) => l !== lang)
        : [...prev.programmingLanguages, lang],
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess(false);

    // Validation
    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (formData.password.length < 8) {
      setError("Password must be at least 8 characters");
      return;
    }

    if (!formData.learningGoal.trim()) {
      setError("Please enter your learning goal");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(`${backendUrl}/auth/signup`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password,
          software_background: formData.softwareBackground,
          hardware_experience: formData.hardwareExperience,
          programming_languages: formData.programmingLanguages,
          learning_goal: formData.learningGoal,
        }),
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
          confirmPassword: "",
          softwareBackground: "beginner",
          hardwareExperience: "low",
          programmingLanguages: [],
          learningGoal: "",
        });
        // Trigger callback
        if (onSignUpSuccess) {
          setTimeout(onSignUpSuccess, 1500);
        }
      } else {
        setError(data.message || "Sign up failed");
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
        <h2>Create Your Account</h2>
        <p className={styles.subtitle}>Join our robotics community</p>

        {error && <div className={styles.error}>{error}</div>}
        {success && <div className={styles.success}>✓ Account created successfully! Redirecting...</div>}

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
              placeholder="At least 8 characters"
              disabled={loading}
            />
          </div>

          {/* Confirm Password */}
          <div className={styles.formGroup}>
            <label htmlFor="confirmPassword">Confirm Password</label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              required
              value={formData.confirmPassword}
              onChange={handleInputChange}
              placeholder="Repeat your password"
              disabled={loading}
            />
          </div>

          <hr className={styles.divider} />
          <p className={styles.sectionTitle}>Learning Profile</p>

          {/* Software Background */}
          <div className={styles.formGroup}>
            <label htmlFor="softwareBackground">Software Experience</label>
            <select
              id="softwareBackground"
              name="softwareBackground"
              value={formData.softwareBackground}
              onChange={handleInputChange}
              disabled={loading}
            >
              <option value="beginner">Beginner - Just starting with programming</option>
              <option value="intermediate">Intermediate - Some programming experience</option>
              <option value="advanced">Advanced - Professional development background</option>
            </select>
          </div>

          {/* Hardware Experience */}
          <div className={styles.formGroup}>
            <label htmlFor="hardwareExperience">Hardware Experience</label>
            <select
              id="hardwareExperience"
              name="hardwareExperience"
              value={formData.hardwareExperience}
              onChange={handleInputChange}
              disabled={loading}
            >
              <option value="low">Low - No hardware experience</option>
              <option value="medium">Medium - Some robotics/electronics experience</option>
              <option value="high">High - Extensive hands-on hardware experience</option>
            </select>
          </div>

          {/* Programming Languages */}
          <div className={styles.formGroup}>
            <label>Programming Languages</label>
            <div className={styles.languageGrid}>
              {["Python", "C++", "ROS", "JavaScript", "Java"].map((lang) => (
                <label key={lang} className={styles.checkbox}>
                  <input
                    type="checkbox"
                    checked={formData.programmingLanguages.includes(lang)}
                    onChange={() => handleLanguageToggle(lang)}
                    disabled={loading}
                  />
                  {lang}
                </label>
              ))}
            </div>
          </div>

          {/* Learning Goal */}
          <div className={styles.formGroup}>
            <label htmlFor="learningGoal">What's Your Learning Goal?</label>
            <textarea
              id="learningGoal"
              name="learningGoal"
              value={formData.learningGoal}
              onChange={handleInputChange}
              placeholder="e.g., I want to build humanoid robots, understand ROS fundamentals, etc."
              rows={4}
              disabled={loading}
            />
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            className={styles.submitButton}
            disabled={loading}
          >
            {loading ? "Creating Account..." : "Create Account"}
          </button>

          <p className={styles.loginLink}>
            Already have an account? <a href="/signin">Sign in here</a>
          </p>
        </form>
      </div>
    </div>
  );
}

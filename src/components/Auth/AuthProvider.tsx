import React, { createContext, useContext, useState, useEffect } from 'react';

interface User {
  external_id?: string;
  id?: number;
  email?: string;
  software_background?: string;
  hardware_experience?: string;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  signin: (email: string) => Promise<void>;
  signup: (profile: any) => Promise<void>;
  signout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Restore session from localStorage on component mount
    const externalId = typeof window !== 'undefined' ? localStorage.getItem('external_id') : null;
    if (externalId) {
      setUser({ external_id: externalId });
    }
    setIsLoading(false);
  }, []);

  const signup = async (profile: any) => {
    try {
      const backendUrl = typeof window !== 'undefined' 
        ? window.location.origin.includes('localhost') 
          ? 'http://localhost:8000'
          : window.location.origin
        : 'http://localhost:8000';
      
      const res = await fetch(`${backendUrl}/api/auth/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(profile),
      });
      const data = await res.json();
      if (res.ok && data.user) {
        const extId = String(data.user.external_id || data.user.id);
        localStorage.setItem('external_id', extId);
        setUser({ external_id: extId, ...data.user });
      } else {
        throw new Error(data.detail || 'Signup failed');
      }
    } catch (e) {
      console.error('Signup failed:', e);
      throw e;
    }
  };

  const signin = async (email: string) => {
    try {
      const backendUrl = typeof window !== 'undefined' 
        ? window.location.origin.includes('localhost') 
          ? 'http://localhost:8000'
          : window.location.origin
        : 'http://localhost:8000';
      
      const res = await fetch(`${backendUrl}/api/auth/signin`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });
      const data = await res.json();
      if (res.ok && data.user) {
        const extId = String(data.user.external_id || data.user.id);
        localStorage.setItem('external_id', extId);
        setUser({ external_id: extId, ...data.user });
      } else {
        throw new Error(data.detail || 'Signin failed');
      }
    } catch (e) {
      console.error('Signin failed:', e);
      throw e;
    }
  };

  const signout = async () => {
    localStorage.removeItem('external_id');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, signin, signup, signout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider');
  return ctx;
}

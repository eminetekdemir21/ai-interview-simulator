import React, { createContext, useContext, useEffect, useState, useCallback } from "react";
import { api, getToken, setToken } from "../api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const bootstrap = useCallback(async () => {
    setLoading(true);
    try {
      const token = await getToken();
      if (!token) {
        setUser(null);
        return;
      }
      const me = await api.me();
      setUser(me);
    } catch {
      await setToken(null);
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    bootstrap();
  }, [bootstrap]);

  const login = async (email, password) => {
    const res = await api.login(email, password);
    await setToken(res.token);
    setUser(res);
  };

  const register = async (name, email, password) => {
    const res = await api.register(name, email, password);
    await setToken(res.token);
    setUser(res);
  };

  const logout = async () => {
    try {
      await api.logout();
    } catch {
      // Token zaten gecersizse sorun degil, yine de yerelden temizle
    }
    await setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, refresh: bootstrap }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth, AuthProvider icinde kullanilmali");
  return ctx;
}

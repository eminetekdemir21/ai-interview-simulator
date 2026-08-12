import AsyncStorage from "@react-native-async-storage/async-storage";
import { API_BASE_URL } from "./config";

const TOKEN_KEY = "ip_token";

export async function getToken() {
  return AsyncStorage.getItem(TOKEN_KEY);
}

export async function setToken(token) {
  if (token) {
    await AsyncStorage.setItem(TOKEN_KEY, token);
  } else {
    await AsyncStorage.removeItem(TOKEN_KEY);
  }
}

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
  }
}

/**
 * Backend'e istek atar. Web'de cerez kullanilirken, mobilde
 * Authorization: Bearer <token> header'i kullanilir (backend'de
 * auth.get_current_user bunu kabul edecek sekilde guncellendi).
 */
async function request(path, { method = "GET", body, isForm = false, auth = true } = {}) {
  const headers = {};
  if (!isForm) headers["Content-Type"] = "application/json";

  if (auth) {
    const token = await getToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }

  let res;
  try {
    res = await fetch(`${API_BASE_URL}${path}`, {
      method,
      headers,
      body: isForm ? body : body ? JSON.stringify(body) : undefined,
    });
  } catch (e) {
    throw new ApiError("Sunucuya baglanilamadi. Internet baglantini ve config.js'deki adresi kontrol et.", 0);
  }

  let data = null;
  const text = await res.text();
  if (text) {
    try {
      data = JSON.parse(text);
    } catch {
      data = null;
    }
  }

  if (!res.ok) {
    const message = (data && data.detail) || `Istek basarisiz (${res.status})`;
    throw new ApiError(message, res.status);
  }
  return data;
}

export const api = {
  register: (name, email, password) =>
    request("/api/register", { method: "POST", body: { name, email, password }, auth: false }),
  login: (email, password) =>
    request("/api/login", { method: "POST", body: { email, password }, auth: false }),
  logout: () => request("/api/logout", { method: "POST" }),
  me: () => request("/api/me"),

  historyStats: () => request("/api/history/stats"),
  history: () => request("/api/history"),

  companies: () => request("/api/companies", { auth: false }),

  createSession: () => request("/api/session", { method: "POST" }),

  uploadCv: async (sessionId, file) => {
    const form = new FormData();
    form.append("session_id", sessionId);
    form.append("file", { uri: file.uri, name: file.name, type: file.mimeType || "application/pdf" });
    return request("/api/upload-cv", { method: "POST", body: form, isForm: true });
  },

  uploadJob: async (sessionId, { file, jobText }) => {
    const form = new FormData();
    form.append("session_id", sessionId);
    if (file) {
      form.append("file", { uri: file.uri, name: file.name, type: file.mimeType || "application/pdf" });
    } else if (jobText) {
      form.append("job_text", jobText);
    }
    return request("/api/upload-job", { method: "POST", body: form, isForm: true });
  },

  startInterview: async (sessionId, { companyId, role, difficulty, interviewType, totalQuestions }) => {
    const form = new FormData();
    form.append("session_id", sessionId);
    if (companyId) form.append("company_id", companyId);
    if (role) form.append("role", role);
    if (difficulty) form.append("difficulty", difficulty);
    if (interviewType) form.append("interview_type", interviewType);
    if (totalQuestions) form.append("total_questions", String(totalQuestions));
    return request("/api/start", { method: "POST", body: form, isForm: true });
  },

  submitAnswer: (sessionId, answer) =>
    request("/api/answer", { method: "POST", body: { session_id: sessionId, answer } }),

  result: (sessionId) => request(`/api/result/${sessionId}`),

  // Profil
  profile: () => request("/api/profile"),
  updateProfile: (name, targetRole) =>
    request("/api/profile", { method: "POST", body: { name, target_role: targetRole } }),

  // AI Kariyer Kocu
  coach: (message, history) => request("/api/coach", { method: "POST", body: { message, history } }),

  // CV Analizi (auth gerektirmiyor)
  cvAnalysis: async (file) => {
    const form = new FormData();
    form.append("file", { uri: file.uri, name: file.name, type: file.mimeType || "application/pdf" });
    return request("/api/cv-analysis", { method: "POST", body: form, isForm: true, auth: false });
  },

  // Is Uyumu (auth gerektirmiyor)
  jobMatch: async (file, jobText) => {
    const form = new FormData();
    form.append("file", { uri: file.uri, name: file.name, type: file.mimeType || "application/pdf" });
    form.append("job_text", jobText);
    return request("/api/job-match", { method: "POST", body: form, isForm: true, auth: false });
  },

  // Yol Haritasi
  roadmap: () => request("/api/roadmap"),
  regenerateRoadmap: () => request("/api/roadmap/regenerate", { method: "POST" }),
  toggleRoadmapTask: (weekIndex, taskIndex) =>
    request("/api/roadmap/toggle", { method: "POST", body: { week_index: weekIndex, task_index: taskIndex } }),

  // Gunluk Meydan Okuma
  challengeToday: () => request("/api/challenge/today"),
  challengeAnswer: (answer) => request("/api/challenge/answer", { method: "POST", body: { answer } }),
  challengeStats: () => request("/api/challenge/stats"),

  // Portfolyo
  portfolio: () => request("/api/portfolio"),
  connectGithub: (username) => request("/api/portfolio/github", { method: "POST", body: { username } }),
  disconnectGithub: () => request("/api/portfolio/disconnect", { method: "POST" }),
};

export { ApiError };

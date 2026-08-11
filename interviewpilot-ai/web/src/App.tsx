import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import { useEffect } from "react"
import { AppShell } from "@/components/layout/AppShell"
import { useUIStore } from "@/store/uiStore"

import LandingPage from "@/pages/marketing/LandingPage"
import LoginPage from "@/pages/auth/LoginPage"
import DashboardPage from "@/pages/app/DashboardPage"
import ResumeAnalysisPage from "@/pages/app/ResumeAnalysisPage"
import JobMatchPage from "@/pages/app/JobMatchPage"
import CompaniesPage from "@/pages/app/CompaniesPage"
import InterviewPracticePage from "@/pages/app/InterviewPracticePage"
import LiveCodingPage from "@/pages/app/LiveCodingPage"
import HistoryPage from "@/pages/app/HistoryPage"
import AnalyticsPage from "@/pages/app/AnalyticsPage"
import RoadmapPage from "@/pages/app/RoadmapPage"
import AchievementsPage from "@/pages/app/AchievementsPage"
import CareerCoachPage from "@/pages/app/CareerCoachPage"
import ProfilePage from "@/pages/app/ProfilePage"
import SettingsPage from "@/pages/app/SettingsPage"

export default function App() {
  const theme = useUIStore((s) => s.theme)

  useEffect(() => {
    document.documentElement.classList.toggle("dark", theme === "dark")
  }, [theme])

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />

        <Route path="/app" element={<AppShell />}>
          <Route index element={<Navigate to="dashboard" replace />} />
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="resume-analysis" element={<ResumeAnalysisPage />} />
          <Route path="job-match" element={<JobMatchPage />} />
          <Route path="companies" element={<CompaniesPage />} />
          <Route path="interview-practice" element={<InterviewPracticePage />} />
          <Route path="live-coding" element={<LiveCodingPage />} />
          <Route path="history" element={<HistoryPage />} />
          <Route path="analytics" element={<AnalyticsPage />} />
          <Route path="roadmap" element={<RoadmapPage />} />
          <Route path="achievements" element={<AchievementsPage />} />
          <Route path="career-coach" element={<CareerCoachPage />} />
          <Route path="profile" element={<ProfilePage />} />
          <Route path="settings" element={<SettingsPage />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

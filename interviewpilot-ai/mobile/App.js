import React from "react";
import { StatusBar } from "expo-status-bar";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { View, ActivityIndicator } from "react-native";

import { AuthProvider, useAuth } from "./src/context/AuthContext";
import { colors } from "./src/theme";

import LoginScreen from "./src/screens/LoginScreen";
import RegisterScreen from "./src/screens/RegisterScreen";
import DashboardScreen from "./src/screens/DashboardScreen";
import InterviewSetupScreen from "./src/screens/InterviewSetupScreen";
import InterviewRoomScreen from "./src/screens/InterviewRoomScreen";
import ReportScreen from "./src/screens/ReportScreen";
import HistoryScreen from "./src/screens/HistoryScreen";
import MenuScreen from "./src/screens/MenuScreen";
import AnalyticsScreen from "./src/screens/AnalyticsScreen";
import RoadmapScreen from "./src/screens/RoadmapScreen";
import ChallengeScreen from "./src/screens/ChallengeScreen";
import PortfolioScreen from "./src/screens/PortfolioScreen";
import JobMatchScreen from "./src/screens/JobMatchScreen";
import CvAnalysisScreen from "./src/screens/CvAnalysisScreen";
import CareerCoachScreen from "./src/screens/CareerCoachScreen";
import ProfileScreen from "./src/screens/ProfileScreen";

const Stack = createNativeStackNavigator();

const screenOptions = {
  headerStyle: { backgroundColor: colors.surface },
  headerTintColor: colors.text,
  headerTitleStyle: { fontWeight: "700" },
  headerShadowVisible: false,
  contentStyle: { backgroundColor: colors.bg },
};

function RootNavigator() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <View style={{ flex: 1, alignItems: "center", justifyContent: "center", backgroundColor: colors.bg }}>
        <ActivityIndicator size="large" color={colors.indigo600} />
      </View>
    );
  }

  return (
    <Stack.Navigator screenOptions={screenOptions}>
      {user ? (
        <>
          <Stack.Screen name="Dashboard" component={DashboardScreen} options={{ title: "InterviewPilot AI" }} />
          <Stack.Screen name="InterviewSetup" component={InterviewSetupScreen} options={{ title: "Yeni Mulakat" }} />
          <Stack.Screen name="InterviewRoom" component={InterviewRoomScreen} options={{ title: "Mulakat Odasi", headerBackVisible: false }} />
          <Stack.Screen name="Report" component={ReportScreen} options={{ title: "Sonuc Raporu", headerBackVisible: false }} />
          <Stack.Screen name="History" component={HistoryScreen} options={{ title: "Gecmis Mulakatlar" }} />
          <Stack.Screen name="Menu" component={MenuScreen} options={{ title: "Tum Ozellikler" }} />
          <Stack.Screen name="Analytics" component={AnalyticsScreen} options={{ title: "Analitik" }} />
          <Stack.Screen name="Roadmap" component={RoadmapScreen} options={{ title: "Yol Haritasi" }} />
          <Stack.Screen name="Challenge" component={ChallengeScreen} options={{ title: "Gunluk Meydan Okuma" }} />
          <Stack.Screen name="Portfolio" component={PortfolioScreen} options={{ title: "Portfolyo" }} />
          <Stack.Screen name="JobMatch" component={JobMatchScreen} options={{ title: "Is Uyumu" }} />
          <Stack.Screen name="CvAnalysis" component={CvAnalysisScreen} options={{ title: "CV Analizi" }} />
          <Stack.Screen name="CareerCoach" component={CareerCoachScreen} options={{ title: "AI Kariyer Kocu" }} />
          <Stack.Screen name="Profile" component={ProfileScreen} options={{ title: "Profil" }} />
        </>
      ) : (
        <>
          <Stack.Screen name="Login" component={LoginScreen} options={{ title: "Giris Yap" }} />
          <Stack.Screen name="Register" component={RegisterScreen} options={{ title: "Kayit Ol" }} />
        </>
      )}
    </Stack.Navigator>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <NavigationContainer>
        <StatusBar style="dark" />
        <RootNavigator />
      </NavigationContainer>
    </AuthProvider>
  );
}

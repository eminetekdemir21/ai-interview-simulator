import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, ScrollView, ActivityIndicator, Alert } from "react-native";
import * as FileSystem from "expo-file-system";
import * as Sharing from "expo-sharing";
import { api, ApiError, getToken } from "../api";
import { API_BASE_URL } from "../config";
import { colors, radius } from "../theme";
import Button from "../components/Button";
import Card from "../components/Card";

const SUB_LABELS = {
  technical: "Teknik",
  communication: "Iletisim",
  confidence: "Ozguven",
  system_design: "Sistem Tasarimi",
};

export default function ReportScreen({ route, navigation }) {
  const { sessionId } = route.params;
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [downloading, setDownloading] = useState(false);

  useEffect(() => {
    api
      .result(sessionId)
      .then(setReport)
      .catch((e) => setError(e instanceof ApiError ? e.message : "Rapor yuklenemedi"))
      .finally(() => setLoading(false));
  }, [sessionId]);

  const onDownloadPdf = async () => {
    setDownloading(true);
    try {
      const token = await getToken();
      const fileUri = `${FileSystem.cacheDirectory}mulakat_raporu_${sessionId.slice(0, 8)}.pdf`;
      const result = await FileSystem.downloadAsync(
        `${API_BASE_URL}/api/history/${sessionId}/pdf`,
        fileUri,
        { headers: token ? { Authorization: `Bearer ${token}` } : {} }
      );
      if (result.status !== 200) {
        throw new Error(`PDF indirilemedi (${result.status})`);
      }
      const canShare = await Sharing.isAvailableAsync();
      if (canShare) {
        await Sharing.shareAsync(result.uri, { mimeType: "application/pdf", dialogTitle: "Mulakat Raporu" });
      } else {
        Alert.alert("PDF indirildi", result.uri);
      }
    } catch (e) {
      Alert.alert("Hata", e.message || "PDF indirilemedi");
    } finally {
      setDownloading(false);
    }
  };

  if (loading) {
    return (
      <View style={{ flex: 1, alignItems: "center", justifyContent: "center", backgroundColor: colors.bg }}>
        <ActivityIndicator size="large" color={colors.indigo600} />
      </View>
    );
  }

  if (error || !report) {
    return (
      <View style={{ flex: 1, alignItems: "center", justifyContent: "center", backgroundColor: colors.bg, padding: 20 }}>
        <Text style={{ color: colors.danger, textAlign: "center" }}>{error || "Rapor bulunamadi"}</Text>
        <Button title="Dashboard'a Don" onPress={() => navigation.popToTop()} style={{ marginTop: 20 }} />
      </View>
    );
  }

  return (
    <ScrollView style={{ flex: 1, backgroundColor: colors.bg }} contentContainerStyle={{ padding: 16 }}>
      <Card style={{ alignItems: "center", paddingVertical: 26 }}>
        <Text style={styles.scoreBig}>{report.overall_score}</Text>
        <Text style={styles.scoreOutOf}>/ 100 genel skor</Text>
        {!!report.company_name && <Text style={styles.companyTag}>{report.company_name}</Text>}
      </Card>

      {!!report.summary && (
        <Card style={{ marginTop: 14 }}>
          <Text style={styles.sectionLabel}>Ozet</Text>
          <Text style={styles.bodyText}>{report.summary}</Text>
        </Card>
      )}

      {!!report.sub_scores && (
        <Card style={{ marginTop: 14 }}>
          <Text style={styles.sectionLabel}>Alt Skorlar</Text>
          {Object.entries(report.sub_scores).map(([key, val]) => (
            <View key={key} style={styles.subRow}>
              <Text style={styles.subLabel}>{SUB_LABELS[key] || key}</Text>
              <Text style={styles.subValue}>{val}/100</Text>
            </View>
          ))}
        </Card>
      )}

      {report.strengths?.length > 0 && (
        <Card style={{ marginTop: 14 }}>
          <Text style={[styles.sectionLabel, { color: colors.success }]}>Guclu Yonler</Text>
          {report.strengths.map((s, i) => (
            <Text key={i} style={styles.listItem}>
              • {s}
            </Text>
          ))}
        </Card>
      )}

      {report.weaknesses?.length > 0 && (
        <Card style={{ marginTop: 14 }}>
          <Text style={[styles.sectionLabel, { color: colors.warning }]}>Gelistirilmesi Gereken Yonler</Text>
          {report.weaknesses.map((s, i) => (
            <Text key={i} st
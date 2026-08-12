import React, { useState } from "react";
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from "react-native";
import * as DocumentPicker from "expo-document-picker";
import { api, ApiError } from "../api";
import { colors, radius } from "../theme";
import Button from "../components/Button";
import Card from "../components/Card";

export default function CvAnalysisScreen() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const pickCv = async () => {
    const res = await DocumentPicker.getDocumentAsync({ type: ["application/pdf", "text/plain"] });
    if (!res.canceled && res.assets?.[0]) {
      setFile(res.assets[0]);
      setResult(null);
    }
  };

  const onAnalyze = async () => {
    setError("");
    if (!file) return setError("Once CV'ni yukle (PDF)");
    setLoading(true);
    try {
      const res = await api.cvAnalysis(file);
      setResult(res);
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Analiz basarisiz");
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={{ flex: 1, backgroundColor: colors.bg }} contentContainerStyle={{ padding: 16 }}>
      <Card>
        <Text style={styles.label}>CV (PDF)</Text>
        <TouchableOpacity onPress={pickCv} style={styles.pickRow}>
          <Text style={{ color: file ? colors.text : colors.textFaint, flex: 1 }} numberOfLines={1}>
            {file ? file.name : "PDF sec"}
          </Text>
          <Text style={{ color: colors.indigo600, fontWeight: "700" }}>Sec</Text>
        </TouchableOpacity>
        {!!error && <Text style={styles.errorText}>{error}</Text>}
        <Button title="CV'yi Analiz Et" onPress={onAnalyze} loading={loading} style={{ marginTop: 14 }} />
      </Card>

      {!!result && (
        <>
          <Card style={{ marginTop: 14, alignItems: "center", paddingVertical: 22 }}>
            <Text style={styles.scoreBig}>{result.score}</Text>
            <Text style={styles.scoreOutOf}>/ 100 · {result.level}</Text>
          </Card>

          {result.strengths?.length > 0 && (
            <Card style={{ marginTop: 14 }}>
              <Text style={[styles.sectionLabel, { color: colors.success }]}>Guclu Yonler</Text>
              {result.strengths.map((s, i) => (
                <Text key={i} style={styles.listItem}>
                  • {s}
                </Text>
              ))}
            </Card>
          )}

          {result.improvements?.length > 0 && (
            <Card style={{ marginTop: 14 }}>
              <Text style={[styles.sectionLabel, { color: colors.warning }]}>Iyilestirme Onerileri</Text>
              {result.improvements.map((s, i) => (
                <Text key={i} style={styles.listItem}>
                  • {s}
                </Text>
              ))}
            </Card>
          )}

          {result.missing_sections?.length > 0 && (
            <Card style={{ marginTop: 14, marginBottom: 40 }}>
              <Text style={styles.sectionLabel}>Eksik Bolumler</Text>
              {result.missing_sections.map((s, i) => (
                <Text key={i} style={styles.listItem}>
                  • {s}
                </Text>
              ))}
            </Card>
          )}
        </>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  label: { fontSize: 12.5, fontWeight: "700", color: colors.textMuted, marginBottom: 6 },
  pickRow: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: colors.surfaceAlt,
    borderWidth: 1.5,
    borderColor: colors.borderStrong,
    borderRadius: radius.md,
    paddingHorizontal: 14,
    paddingVertical: 12,
  },
  errorText: { color: colors.danger, fontSize: 13, marginTop: 10 },
  scoreBig: { fontSize: 40, fontWeight: "800", color: colors.indigo600 },
  scoreOutOf: { fontSize: 12, color: colors.textMuted, marginTop: 2 },
  sectionLabel: { fontSize: 13, fontWeight: "800", color: colors.text, marginBottom: 8 },
  listItem: { fontSize: 13.5, color: colors.text, lineHeight: 19, marginBottom: 3 },
});

import React, { useState } from "react";
import { View, Text, TextInput, StyleSheet, ScrollView, TouchableOpacity } from "react-native";
import * as DocumentPicker from "expo-document-picker";
import { api, ApiError } from "../api";
import { colors, radius } from "../theme";
import Button from "../components/Button";
import Card from "../components/Card";

export default function JobMatchScreen() {
  const [cvFile, setCvFile] = useState(null);
  const [jobText, setJobText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const pickCv = async () => {
    const res = await DocumentPicker.getDocumentAsync({ type: ["application/pdf", "text/plain"] });
    if (!res.canceled && res.assets?.[0]) setCvFile(res.assets[0]);
  };

  const onAnalyze = async () => {
    setError("");
    if (!cvFile) return setError("Once CV'ni yukle (PDF)");
    if (!jobText.trim()) return setError("Is ilani metnini yapistir");
    setLoading(true);
    setResult(null);
    try {
      const res = await api.jobMatch(cvFile, jobText.trim());
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
          <Text style={{ color: cvFile ? colors.text : colors.textFaint, flex: 1 }} numberOfLines={1}>
            {cvFile ? cvFile.name : "PDF sec"}
          </Text>
          <Text style={{ color: colors.indigo600, fontWeight: "700" }}>Sec</Text>
        </TouchableOpacity>

        <Text style={[styles.label, { marginTop: 16 }]}>Is Ilani Metni</Text>
        <TextInput
          style={styles.textarea}
          placeholder="Is ilani metnini buraya yapistir..."
          placeholderTextColor={colors.textFaint}
          multiline
          value={jobText}
          onChangeText={setJobText}
        />

        {!!error && <Text style={styles.errorText}>{error}</Text>}
        <Button title="Uyumu Analiz Et" onPress={onAnalyze} loading={loading} style={{ marginTop: 14 }} />
      </Card>

      {!!result && (
        <>
          <Card style={{ marginTop: 14, alignItems: "center", paddingVertical: 22 }}>
            <Text style={styles.scoreBig}>{result.match_score}</Text>
            <Text style={styles.scoreOutOf}>/ 100 uyum skoru</Text>
          </Card>

          <Card style={{ marginTop: 14 }}>
            <Text style={styles.sectionLabel}>Ozet</Text>
            <Text style={styles.bodyText}>{result.summary}</Text>
          </Card>

          {result.matched_keywords?.length > 0 && (
            <Card style={{ marginTop: 14 }}>
              <Text style={[styles.sectionLabel, { color: colors.success }]}>Eslesen Anahtar Kelimeler</Text>
              <View style={styles.chipWrap}>
                {result.matched_keywords.map((k, i) => (
                  <View key={i} style={[styles.chip, styles.chipSuccess]}>
                    <Text style={styles.chipTextSuccess}>{k}</Text>
                  </View>
                ))}
              </View>
            </Card>
          )}

          {result.missing_keywords?.length > 0 && (
            <Card style={{ marginTop: 14, marginBottom: 40 }}>
              <Text style={[styles.sectionLabel, { color: colors.warning }]}>Eksik Anahtar Kelimeler</Text>
              <View style={styles.chipWrap}>
                {result.missing_keywords.map((k, i) => (
                  <View key={i} style={[styles.chip, styles.chipWarning]}>
                    <Text style={styles.chipTextWarning}>{k}</Text>
                  </View>
                ))}
              </View>
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
  textarea: {
    backgroundColor: colors.surfaceAlt,
    borderWidth: 1.5,
    borderColor: colors.borderStrong,
    borderRadius: radius.md,
    paddingHorizontal: 14,
    paddingVertical: 12,
    fontSize: 14,
    color: colors.text,
    minHeight: 100,
    textAlignVertical: "top",
  },
  errorText: { color: colors.danger, fontSize: 13, marginTop: 10 },
  scoreBig: { fontSize: 40, fontWeight: "800", color: colors.indigo600 },
  scoreOutOf: { fontSize: 12, color: colors.textMuted, marginTop: 2 },
  sectionLabel: { fontSize: 13, fontWeight: "800", color: colors.text, marginBottom: 8 },
  bodyText: { fontSize: 13.5, color: colors.text, lineHeight: 19 },
  chipWrap: { flexDirection: "row", flexWrap: "wrap", gap: 8 },
  chip: { paddingHorizontal: 12, paddingVertical: 6, borderRadius: 999 },
  chipSuccess: { backgroundColor: colors.successSoft },
  chipWarning: { backgroundColor: colors.warningSoft },
  chipTextSuccess: { fontSize: 12, fontWeight: "700", color: colors.success },
  chipTextWarning: { fontSize: 12, fontWeight: "700", color: colors.warning },
});

import React, { useCallback, useState } from "react";
import { View, Text, TextInput, StyleSheet, ScrollView, ActivityIndicator } from "react-native";
import { useFocusEffect } from "@react-navigation/native";
import { api, ApiError } from "../api";
import { colors, radius } from "../theme";
import Button from "../components/Button";
import Card from "../components/Card";

export default function ChallengeScreen() {
  const [today, setToday] = useState(null);
  const [stats, setStats] = useState(null);
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const load = useCallback(() => {
    setLoading(true);
    setError("");
    Promise.all([api.challengeToday(), api.challengeStats()])
      .then(([t, s]) => {
        setToday(t);
        setStats(s);
      })
      .catch((e) => setError(e instanceof ApiError ? e.message : "Yuklenemedi"))
      .finally(() => setLoading(false));
  }, []);

  useFocusEffect(
    useCallback(() => {
      load();
    }, [load])
  );

  const onSubmit = async () => {
    if (!answer.trim()) return setError("Once bir cevap yaz");
    setError("");
    setSubmitting(true);
    try {
      const record = await api.challengeAnswer(answer.trim());
      setToday(record);
      const s = await api.challengeStats();
      setStats(s);
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Cevap gonderilemedi");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <View style={{ flex: 1, alignItems: "center", justifyContent: "center", backgroundColor: colors.bg }}>
        <ActivityIndicator size="large" color={colors.indigo600} />
      </View>
    );
  }

  return (
    <ScrollView style={{ flex: 1, backgroundColor: colors.bg }} contentContainerStyle={{ padding: 16 }}>
      {!!stats && (
        <View style={styles.statRow}>
          <StatBox label="Seri" value={`${stats.streak} gun`} />
          <StatBox label="Bu Hafta" value={`${stats.week_completed}/${stats.week_total}`} />
          <StatBox label="Rozete Kalan" value={`${stats.days_to_badge} gun`} />
        </View>
      )}

      <Card style={{ marginTop: 14 }}>
        <Text style={styles.questionLabel}>BUGUNUN SORUSU</Text>
        <Text style={styles.questionText}>{today?.question}</Text>
      </Card>

      {today?.completed ? (
        <Card style={{ marginTop: 14 }}>
          <View style={styles.scoreRow}>
            <Text style={styles.scoreLabel}>Puan</Text>
            <Text style={styles.scoreValue}>{today.score}/100</Text>
          </View>
          <Text style={styles.feedbackLabel}>Geri Bildirim</Text>
          <Text style={styles.feedbackText}>{today.feedback}</Text>
          <Text style={styles.doneNote}>Bugunku sorunu tamamladin, yarin yeni bir soru seni bekliyor.</Text>
        </Card>
      ) : (
        <>
          <Text style={styles.label}>Cevabin</Text>
          <TextInput
            style={styles.textarea}
            placeholder="Kisaca cevapla..."
            placeholderTextColor={colors.textFaint}
            multiline
            value={answer}
            onChangeText={setAnswer}
          />
          {!!error && <Text style={styles.errorText}>{error}</Text>}
          <Button title="Cevabi Gonder" onPress={onSubmit} loading={submitting} style={{ marginTop: 14, marginBottom: 40 }} />
        </>
      )}
    </ScrollView>
  );
}

function StatBox({ label, value }) {
  return (
    <Card style={styles.statBox}>
      <Text style={styles.statValue}>{value}</Text>
      <Text style={styles.statLabel}>{label}</Text>
    </Card>
  );
}

const styles = StyleSheet.create({
  statRow: { flexDirection: "row", gap: 10 },
  statBox: { flex: 1, alignItems: "center", paddingVertical: 14 },
  statValue: { fontSize: 15, fontWeight: "800", color: colors.indigo600 },
  statLabel: { fontSize: 11, color: colors.textMuted, marginTop: 4 },
  questionLabel: { fontSize: 11, fontWeight: "800", color: colors.indigo600, letterSpacing: 0.5 },
  questionText: { fontSize: 15.5, color: colors.text, marginTop: 8, lineHeight: 22 },
  label: { fontSize: 12.5, fontWeight: "700", color: colors.textMuted, marginTop: 18, marginBottom: 6 },
  textarea: {
    backgroundColor: colors.surface,
    borderWidth: 1.5,
    borderColor: colors.borderStrong,
    borderRadius: radius.md,
    paddingHorizontal: 14,
    paddingVertical: 12,
    fontSize: 14.5,
    color: colors.text,
    minHeight: 110,
    textAlignVertical: "top",
  },
  errorText: { color: colors.danger, fontSize: 13, marginTop: 10 },
  scoreRow: { flexDirection: "row", justifyContent: "space-between", alignItems: "center" },
  scoreLabel: { fontSize: 13, color: colors.textMuted, fontWeight: "700" },
  scoreValue: { fontSize: 20, fontWeight: "800", color: colors.indigo600 },
  feedbackLabel: { fontSize: 11.5, fontWeight: "800", color: colors.textMuted, marginTop: 12, marginBottom: 4 },
  feedbackText: { fontSize: 14, color: colors.text, lineHeight: 20 },
  doneNote: { fontSize: 12, color: colors.textFaint, marginTop: 14 },
});

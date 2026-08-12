import React, { useState } from "react";
import { View, Text, TextInput, StyleSheet, ScrollView } from "react-native";
import { api, ApiError } from "../api";
import { colors, radius } from "../theme";
import Button from "../components/Button";
import Card from "../components/Card";

export default function InterviewRoomScreen({ route, navigation }) {
  const { sessionId, firstQuestion, meta } = route.params;

  const [question, setQuestion] = useState(firstQuestion.question);
  const [questionNumber, setQuestionNumber] = useState(firstQuestion.question_number);
  const [totalQuestions, setTotalQuestions] = useState(firstQuestion.total_questions);
  const [answer, setAnswer] = useState("");
  const [feedback, setFeedback] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [finished, setFinished] = useState(false);

  const onSubmit = async () => {
    if (!answer.trim()) return setError("Once bir cevap yaz");
    setError("");
    setSubmitting(true);
    try {
      const res = await api.submitAnswer(sessionId, answer.trim());
      setFeedback(res);
      setFinished(res.finished);
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Cevap gonderilemedi");
    } finally {
      setSubmitting(false);
    }
  };

  const onNext = () => {
    if (finished) {
      navigation.replace("Report", { sessionId, meta });
      return;
    }
    setQuestion(feedback.next_question);
    setQuestionNumber(feedback.question_number + 1);
    setTotalQuestions(feedback.total_questions);
    setAnswer("");
    setFeedback(null);
  };

  return (
    <ScrollView style={{ flex: 1, backgroundColor: colors.bg }} contentContainerStyle={{ padding: 16 }}>
      <View style={styles.progressRow}>
        <Text style={styles.progressText}>
          Soru {questionNumber} / {totalQuestions}
        </Text>
        {!!meta?.company && <Text style={styles.progressText}>{meta.company}</Text>}
      </View>

      <Card style={{ marginTop: 10 }}>
        <Text style={styles.questionLabel}>SORU</Text>
        <Text style={styles.questionText}>{question}</Text>
      </Card>

      {!feedback ? (
        <>
          <Text style={styles.label}>Cevabin</Text>
          <TextInput
            style={styles.textarea}
            placeholder="Cevabini buraya yaz..."
            placeholderTextColor={colors.textFaint}
            multiline
            value={answer}
            onChangeText={setAnswer}
            editable={!submitting}
          />
          {!!error && <Text style={styles.errorText}>{error}</Text>}
          <Button title="Cevabi Gonder" onPress={onSubmit} loading={submitting} style={{ marginTop: 14 }} />
        </>
      ) : (
        <Card style={{ marginTop: 16 }}>
          <View style={styles.scoreRow}>
            <Text style={styles.scoreLabel}>Puan</Text>
            <Text style={styles.scoreValue}>{feedback.score}/100</Text>
          </View>
          <Text style={styles.feedbackLabel}>Geri Bildirim</Text>
          <Text style={styles.feedbackText}>{feedback.feedback}</Text>
          {!!feedback.missing_points && (
            <>
              <Text style={styles.feedbackLabel}>Eksik Noktalar</Text>
              <Text style={styles.feedbackText}>{feedback.missing_points}</Text>
            </>
          )}
          <Button
            title={finished ? "Sonuc Raporunu Gor" : "Sonraki Soru"}
            onPress={onNext}
            style={{ marginTop: 16 }}
          />
        </Card>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  progressRow: { flexDirection: "row", justifyContent: "space-between", alignItems: "center" },
  progressText: { fontSize: 12.5, fontWeight: "700", color: colors.textMuted },
  questionLabel: { fontSize: 11, fontWeight: "800", color: colors.indigo600, letterSpacing: 0.5 },
  questionText: { fontSize: 16, color: colors.text, marginTop: 8, lineHeight: 23 },
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
    minHeight: 140,
    textAlignVertical: "top",
  },
  errorText: { color: colors.danger, fontSize: 13, marginTop: 10 },
  scoreRow: { flexDirection: "row", justifyContent: "space-between", alignItems: "center" },
  scoreLabel: { fontSize: 13, color: colors.textMuted, fontWeight: "700" },
  scoreValue: { fontSize: 22, fontWeight: "800", color: colors.indigo600 },
  feedbackLabel: { fontSize: 11.5, fontWeight: "800", color: colors.textMuted, marginTop: 14, marginBottom: 4 },
  feedbackText: { fontSize: 14, color: colors.text, lineHeight: 20 },
});

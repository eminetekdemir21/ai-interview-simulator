import React, { useCallback, useState } from "react";
import { View, Text, StyleSheet, ScrollView, ActivityIndicator, TouchableOpacity } from "react-native";
import { useFocusEffect } from "@react-navigation/native";
import { api, ApiError } from "../api";
import { colors, radius } from "../theme";
import Button from "../components/Button";
import Card from "../components/Card";

export default function RoadmapScreen() {
  const [roadmap, setRoadmap] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [regenerating, setRegenerating] = useState(false);

  const load = useCallback(() => {
    setLoading(true);
    setError("");
    api
      .roadmap()
      .then(setRoadmap)
      .catch((e) => setError(e instanceof ApiError ? e.message : "Yol haritasi yuklenemedi"))
      .finally(() => setLoading(false));
  }, []);

  useFocusEffect(
    useCallback(() => {
      load();
    }, [load])
  );

  const onToggle = async (weekIndex, taskIndex) => {
    // Iyimser (optimistic) guncelleme: aninda goster, hata olursa geri al
    setRoadmap((prev) => {
      if (!prev) return prev;
      const next = JSON.parse(JSON.stringify(prev));
      next.weeks[weekIndex].tasks[taskIndex].done = !next.weeks[weekIndex].tasks[taskIndex].done;
      return next;
    });
    try {
      await api.toggleRoadmapTask(weekIndex, taskIndex);
    } catch {
      load();
    }
  };

  const onRegenerate = async () => {
    setRegenerating(true);
    setError("");
    try {
      const r = await api.regenerateRoadmap();
      setRoadmap(r);
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Yeniden olusturulamadi");
    } finally {
      setRegenerating(false);
    }
  };

  if (loading) {
    return (
      <View style={{ flex: 1, alignItems: "center", justifyContent: "center", backgroundColor: colors.bg }}>
        <ActivityIndicator size="large" color={colors.indigo600} />
      </View>
    );
  }

  if (error && !roadmap) {
    return (
      <View style={{ flex: 1, alignItems: "center", justifyContent: "center", backgroundColor: colors.bg, padding: 20 }}>
        <Text style={{ color: colors.textMuted, textAlign: "center" }}>{error}</Text>
      </View>
    );
  }

  return (
    <ScrollView style={{ flex: 1, backgroundColor: colors.bg }} contentContainerStyle={{ padding: 16 }}>
      <Card>
        <Text style={styles.focusLabel}>ODAK ALANI</Text>
        <Text style={styles.focusTitle}>{roadmap.focus_area}</Text>
        <Text style={styles.summary}>{roadmap.summary}</Text>
      </Card>

      {roadmap.weeks.map((week, wi) => (
        <Card key={wi} style={{ marginTop: 14 }}>
          <Text style={styles.weekTitle}>{week.title}</Text>
          {week.tasks.map((task, ti) => (
            <TouchableOpacity key={ti} onPress={() => onToggle(wi, ti)} style={styles.taskRow}>
              <View style={[styles.checkbox, task.done && styles.checkboxDone]}>
                {task.done && <Text style={styles.checkmark}>✓</Text>}
              </View>
              <Text style={[styles.taskText, task.done && styles.taskTextDone]}>{task.text}</Text>
            </TouchableOpacity>
          ))}
        </Card>
      ))}

      <Button
        title="Yol Haritasini Yeniden Olustur"
        variant="secondary"
        onPress={onRegenerate}
        loading={regenerating}
        style={{ marginTop: 18, marginBottom: 40 }}
      />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  focusLabel: { fontSize: 11, fontWeight: "800", color: colors.indigo600, letterSpacing: 0.5 },
  focusTitle: { fontSize: 18, fontWeight: "800", color: colors.text, marginTop: 6 },
  summary: { fontSize: 13.5, color: colors.textMuted, marginTop: 8, lineHeight: 19 },
  weekTitle: { fontSize: 14, fontWeight: "800", color: colors.text, marginBottom: 10 },
  taskRow: { flexDirection: "row", alignItems: "center", paddingVertical: 7 },
  checkbox: {
    width: 20,
    height: 20,
    borderRadius: 6,
    borderWidth: 1.5,
    borderColor: colors.borderStrong,
    marginRight: 10,
    alignItems: "center",
    justifyContent: "center",
  },
  checkboxDone: { backgroundColor: colors.indigo600, borderColor: colors.indigo600 },
  checkmark: { color: "#fff", fontSize: 12, fontWeight: "800" },
  taskText: { fontSize: 13.5, color: colors.text, flex: 1 },
  taskTextDone: { color: colors.textFaint, textDecorationLine: "line-through" },
});

import React, { useCallback, useState } from "react";
import { View, Text, StyleSheet, FlatList, ActivityIndicator, TouchableOpacity } from "react-native";
import { useFocusEffect } from "@react-navigation/native";
import { api, ApiError } from "../api";
import { colors, radius } from "../theme";
import Card from "../components/Card";

export default function HistoryScreen({ navigation }) {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useFocusEffect(
    useCallback(() => {
      let active = true;
      setLoading(true);
      api
        .history()
        .then((data) => active && setRecords(data))
        .catch((e) => active && setError(e instanceof ApiError ? e.message : "Gecmis yuklenemedi"))
        .finally(() => active && setLoading(false));
      return () => {
        active = false;
      };
    }, [])
  );

  if (loading) {
    return (
      <View style={{ flex: 1, alignItems: "center", justifyContent: "center", backgroundColor: colors.bg }}>
        <ActivityIndicator size="large" color={colors.indigo600} />
      </View>
    );
  }

  if (error) {
    return (
      <View style={{ flex: 1, alignItems: "center", justifyContent: "center", backgroundColor: colors.bg, padding: 20 }}>
        <Text style={{ color: colors.danger }}>{error}</Text>
      </View>
    );
  }

  if (records.length === 0) {
    return (
      <View style={{ flex: 1, alignItems: "center", justifyContent: "center", backgroundColor: colors.bg, padding: 20 }}>
        <Text style={{ color: colors.textMuted, textAlign: "center" }}>Henuz tamamlanmis bir mulakat yok.</Text>
      </View>
    );
  }

  return (
    <FlatList
      style={{ flex: 1, backgroundColor: colors.bg }}
      contentContainerStyle={{ padding: 16 }}
      data={records}
      keyExtractor={(item) => item.id}
      ItemSeparatorComponent={() => <View style={{ height: 10 }} />}
      renderItem={({ item }) => (
        <TouchableOpacity onPress={() => navigation.navigate("Report", { sessionId: item.id })}>
          <Card style={styles.row}>
            <View style={{ flex: 1 }}>
              <Text style={styles.title}>{item.company_name || item.role || "Genel Mulakat"}</Text>
              <Text style={styles.sub}>
                {(item.created_at || "").slice(0, 10)} · {item.question_count ?? 0} soru
              </Text>
            </View>
            <Text style={styles.score}>{item.overall_score}</Text>
          </Card>
        </TouchableOpacity>
      )}
    />
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: "row", alignItems: "center", justifyContent: "space-between" },
  title: { fontSize: 14.5, fontWeight: "700", color: colors.text },
  sub: { fontSize: 12, color: colors.textMuted, marginTop: 3 },
  score: { fontSize: 20, fontWeight: "800", color: colors.indigo600, marginLeft: 12 },
});

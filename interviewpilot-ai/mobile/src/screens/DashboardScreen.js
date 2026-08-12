import React, { useCallback, useState } from "react";
import { View, Text, StyleSheet, ScrollView, RefreshControl, ActivityIndicator } from "react-native";
import { useFocusEffect } from "@react-navigation/native";
import { useAuth } from "../context/AuthContext";
import { api, ApiError } from "../api";
import { colors, radius } from "../theme";
import Button from "../components/Button";
import Card from "../components/Card";

export default function DashboardScreen({ navigation }) {
  const { user, logout } = useAuth();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [refreshing, setRefreshing] = useState(false);

  const load = useCallback(async () => {
    try {
      setError("");
      const data = await api.historyStats();
      setStats(data);
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Istatistikler yuklenemedi");
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useFocusEffect(
    useCallback(() => {
      load();
    }, [load])
  );

  const onRefresh = () => {
    setRefreshing(true);
    load();
  };

  const firstName = (user?.name || user?.email || "").split(" ")[0];

  return (
    <ScrollView
      style={{ flex: 1, backgroundColor: colors.bg }}
      contentContainerStyle={{ padding: 18 }}
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={colors.indigo600} />}
    >
      <Text style={styles.greet}>Merhaba, {firstName || "hosgeldin"} 👋</Text>
      <Text style={styles.sub}>Bugun pratik yapmaya hazir misin?</Text>

      {loading ? (
        <ActivityIndicator style={{ marginTop: 40 }} color={colors.indigo600} />
      ) : error ? (
        <Card style={{ marginTop: 20 }}>
          <Text style={{ color: colors.danger }}>{error}</Text>
        </Card>
      ) : !stats || stats.total_interviews === 0 ? (
        <Card style={{ marginTop: 24, alignItems: "center", paddingVertical: 28 }}>
          <Text style={{ fontSize: 16, fontWeight: "700", color: colors.text }}>Henuz bir mulakat yapmadin</Text>
          <Text style={{ fontSize: 13, color: colors.textMuted, textAlign: "center", marginTop: 8 }}>
            Ilk mulakatini tamamladiginda buradaki tum istatistikler gercek verilerinle dolacak.
          </Text>
        </Card>
      ) : (
        <View style={styles.kpiGrid}>
          <KpiCard label="Mulakat Serisi" value={`${stats.streak_days ?? 0}`} sub="ardisik gun" />
          <KpiCard label="Ortalama Skor" value={`${stats.avg_score ?? 0}`} />
          <KpiCard label="Toplam Mulakat" value={`${stats.total_interviews ?? 0}`} />
          <KpiCard label="En Yuksek Skor" value={`${stats.best_score ?? 0}`} />
        </View>
      )}

      <View style={{ marginTop: 26, gap: 12 }}>
        <Button title="+ Yeni Mulakat Baslat" onPress={() => navigation.navigate("InterviewSetup")} />
        <Button title="Gecmis Mulakatlarim" variant="secondary" onPress={() => navigation.navigate("History")} />
        <Button title="Tum Ozellikler (Analitik, Yol Haritasi, ...)" variant="secondary" onPress={() => navigation.navigate("Menu")} />
        <Button title="Cikis Yap" variant="secondary" onPress={logout} />
      </View>
    </ScrollView>
  );
}

function KpiCard({ label, value, sub }) {
  return (
    <Card style={styles.kpiCard}>
      <Text style={styles.kpiLabel}>{label}</Text>
      <Text style={styles.kpiValue}>{value}</Text>
      {!!sub && <Text style={styles.kpiSub}>{sub}</Text>}
    </Card>
  );
}

const styles = StyleSheet.create({
  greet: { fontSize: 20, fontWeight: "800", color: colors.text },
  sub: { fontSize: 13, color: colors.textMuted, marginTop: 4, marginBottom: 6 },
  kpiGrid: { flexDirection: "row", flexWrap: "wrap", gap: 12, marginTop: 18 },
  kpiCard: { width: "47%", paddingVertical: 16 },
  kpiLabel: { fontSize: 12, color: colors.textMuted, fontWeight: "600" },
  kpiValue: { fontSize: 24, fontWeight: "800", color: colors.text, marginTop: 6 },
  kpiSub: { fontSize: 11, color: colors.textFaint, marginTop: 2 },
});

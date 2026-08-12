import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, ScrollView, ActivityIndicator } from "react-native";
import { api, ApiError } from "../api";
import { colors, radius } from "../theme";
import Card from "../components/Card";

const SUB_LABELS = {
  technical: "Teknik",
  communication: "Iletisim",
  confidence: "Ozguven",
  system_design: "Sistem Tasarimi",
};

function Bar({ label, value, max = 100 }) {
  const pct = Math.max(2, Math.min(100, (value / max) * 100));
  return (
    <View style={{ marginBottom: 12 }}>
      <View style={styles.barRow}>
        <Text style={styles.barLabel}>{label}</Text>
        <Text style={styles.barValue}>{value}</Text>
      </View>
      <View style={styles.barTrack}>
        <View style={[styles.barFill, { width: `${pct}%` }]} />
      </View>
    </View>
  );
}

export default function AnalyticsScreen() {
  const [stats, setStats] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([api.historyStats(), api.history()])
      .then(([s, h]) => {
        setStats(s);
        setHistory(h);
      })
      .catch((e) => setError(e instanceof ApiError ? e.message : "Veriler yuklenemedi"))
      .finally(() => setLoading(false));
  }, []);

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

  if (!stats || !stats.total_interviews) {
    return (
      <View style={{ flex: 1, alignItems: "center", justifyContent: "center", backgroundColor: colors.bg, padding: 20 }}>
        <Text style={{ color: colors.textMuted, textAlign: "center" }}>
          Henuz mulakat verisi yok. Ilk mulakatini tamamladiginda burada gercek analizlerini gorursun.
        </Text>
      </View>
    );
  }

  // Sirket bazinda ortalama skor (client-side hesaplanir)
  const byCompany = {};
  history.forEach((r) => {
    const name = r.company_name || "Genel";
    if (!byCompany[name]) byCompany[name] = { total: 0, count: 0 };
    byCompany[name].total += r.overall_score || 0;
    byCompany[name].count += 1;
  });
  const companyAverages = Object.entries(byCompany)
    .map(([name, v]) => ({ name, avg: Math.round(v.total / v.count), count: v.count }))
    .sort((a, b) => b.avg - a.avg);

  return (
    <ScrollView style={{ flex: 1, backgroundColor: colors.bg }} contentContainerStyle={{ padding: 16 }}>
      <Card>
        <Text style={styles.sectionLabel}>Alt Beceri Ortalamalari</Text>
        {Object.entries(stats.avg_sub_scores || {}).map(([key, val]) => (
          <Bar key={key} label={SUB_LABELS[key] || key} value={val} />
        ))}
      </Card>

      <Card style={{ marginTop: 14 }}>
        <Text style={styles.sectionLabel}>Skor Gecmisi (son mulakatlar)</Text>
        {(stats.recent || []).map((r, i) => (
          <View key={i} style={styles.recentRow}>
            <Text style={styles.recentDate}>{(r.created_at || "").slice(0, 10)}</Text>
            <Text style={styles.recentCompany} numberOfLines={1}>
              {r.company_name || r.role || "Genel"}
            </Text>
            <Text style={styles.recentScore}>{r.overall_score}</Text>
          </View>
        ))}
      </Card>

      {companyAverages.length > 0 && (
        <Card style={{ marginTop: 14 }}>
          <Text style={styles.sectionLabel}>Sirket Bazinda Ortalama</Text>
          {companyAverages.map((c) => (
            <View key={c.name} style={styles.recentRow}>
              <Text style={styles.recentCompany} numberOfLines={1}>
                {c.name}
              </Text>
              <Text style={styles.recentDate}>{c.count} mulakat</Text>
              <Text style={styles.recentScore}>{c.avg}</Text>
            </View>
          ))}
        </Card>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  sectionLabel: { fontSize: 13, fontWeight: "800", color: colors.text, marginBottom: 12 },
  barRow: { flexDirection: "row", justifyContent: "space-between", marginBottom: 4 },
  barLabel: { fontSize: 12.5, color: colors.textMuted, fontWeight: "600" },
  barValue: { fontSize: 12.5, color: colors.text, fontWeight: "700" },
  barTrack: { height: 8, borderRadius: 999, backgroundColor: colors.surfaceAlt, overflow: "hidden" },
  barFill: { height: "100%", backgroundColor: colors.indigo600, borderRadius: 999 },
  recentRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  recentDate: { fontSize: 11.5, color: colors.textFaint, width: 78 },
  recentCompany: { fontSize: 12.5, color: colors.text, flex: 1, fontWeight: "600" },
  recentScore: { fontSize: 14, fontWeight: "800", color: colors.indigo600, marginLeft: 8 },
});

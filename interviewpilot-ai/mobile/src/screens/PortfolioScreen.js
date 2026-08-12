import React, { useCallback, useState } from "react";
import { View, Text, TextInput, StyleSheet, ScrollView, ActivityIndicator } from "react-native";
import { useFocusEffect } from "@react-navigation/native";
import { api, ApiError } from "../api";
import { colors, radius } from "../theme";
import Button from "../components/Button";
import Card from "../components/Card";

export default function PortfolioScreen() {
  const [data, setData] = useState(null);
  const [username, setUsername] = useState("");
  const [loading, setLoading] = useState(true);
  const [connecting, setConnecting] = useState(false);
  const [error, setError] = useState("");
  const [notConnected, setNotConnected] = useState(false);

  const load = useCallback(() => {
    setLoading(true);
    setError("");
    setNotConnected(false);
    api
      .portfolio()
      .then(setData)
      .catch((e) => {
        if (e instanceof ApiError && e.status === 400) {
          setNotConnected(true);
        } else {
          setError(e instanceof ApiError ? e.message : "Portfolyo yuklenemedi");
        }
      })
      .finally(() => setLoading(false));
  }, []);

  useFocusEffect(
    useCallback(() => {
      load();
    }, [load])
  );

  const onConnect = async () => {
    if (!username.trim()) return setError("GitHub kullanici adini gir");
    setError("");
    setConnecting(true);
    try {
      const res = await api.connectGithub(username.trim());
      setData(res);
      setNotConnected(false);
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Baglanamadi");
    } finally {
      setConnecting(false);
    }
  };

  const onDisconnect = async () => {
    try {
      await api.disconnectGithub();
      setData(null);
      setNotConnected(true);
      setUsername("");
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Baglanti kesilemedi");
    }
  };

  if (loading) {
    return (
      <View style={{ flex: 1, alignItems: "center", justifyContent: "center", backgroundColor: colors.bg }}>
        <ActivityIndicator size="large" color={colors.indigo600} />
      </View>
    );
  }

  if (notConnected || !data) {
    return (
      <ScrollView style={{ flex: 1, backgroundColor: colors.bg }} contentContainerStyle={{ padding: 16 }}>
        <Card>
          <Text style={styles.sectionLabel}>GitHub Hesabini Bagla</Text>
          <Text style={styles.helpText}>
            Genel GitHub kullanici adini gir, gercek repo verilerinden AI destekli bir portfolyo
            degerlendirmesi olusturalim.
          </Text>
          <TextInput
            style={styles.input}
            placeholder="orn. octocat"
            placeholderTextColor={colors.textFaint}
            autoCapitalize="none"
            value={username}
            onChangeText={setUsername}
          />
          {!!error && <Text style={styles.errorText}>{error}</Text>}
          <Button title="Baglan" onPress={onConnect} loading={connecting} style={{ marginTop: 14 }} />
        </Card>
      </ScrollView>
    );
  }

  const { profile, repos, analysis } = data;

  return (
    <ScrollView style={{ flex: 1, backgroundColor: colors.bg }} contentContainerStyle={{ padding: 16 }}>
      <Card style={{ alignItems: "center", paddingVertical: 22 }}>
        <Text style={styles.profileName}>{profile.name || profile.login}</Text>
        <Text style={styles.profileLogin}>@{profile.login}</Text>
        {!!profile.bio && <Text style={styles.profileBio}>{profile.bio}</Text>}
        <View style={styles.profileStatsRow}>
          <Text style={styles.profileStat}>{profile.public_repos ?? 0} repo</Text>
          <Text style={styles.profileStat}>{profile.followers ?? 0} takipci</Text>
        </View>
      </Card>

      {!!analysis && (
        <Card style={{ marginTop: 14 }}>
          <View style={styles.scoreRow}>
            <Text style={styles.sectionLabel}>AI Degerlendirmesi</Text>
            <Text style={styles.scoreValue}>{analysis.score}/100</Text>
          </View>
          <Text style={styles.bodyText}>{analysis.summary}</Text>
          {analysis.strengths?.length > 0 && (
            <>
              <Text style={styles.subLabel}>Guclu Yonler</Text>
              {analysis.strengths.map((s, i) => (
                <Text key={i} style={styles.listItem}>
                  • {s}
                </Text>
              ))}
            </>
          )}
          {analysis.improvements?.length > 0 && (
            <>
              <Text style={styles.subLabel}>Gelistirilebilir</Text>
              {analysis.improvements.map((s, i) => (
                <Text key={i} style={styles.listItem}>
                  • {s}
                </Text>
              ))}
            </>
          )}
        </Card>
      )}

      {repos?.length > 0 && (
        <Card style={{ marginTop: 14 }}>
          <Text style={styles.sectionLabel}>Repolar</Text>
          {repos.map((r) => (
            <View key={r.name} style={styles.repoRow}>
              <Text style={styles.repoName}>{r.name}</Text>
              <Text style={styles.repoDesc} numberOfLines={2}>
                {r.description || "(aciklama yok)"}
              </Text>
            </View>
          ))}
        </Card>
      )}

      <Button title="Baglantiyi Kes" variant="secondary" onPress={onDisconnect} style={{ marginTop: 16, marginBottom: 40 }} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  sectionLabel: { fontSize: 13, fontWeight: "800", color: colors.text, marginBottom: 8 },
  helpText: { fontSize: 12.5, color: colors.textMuted, marginBottom: 14, lineHeight: 18 },
  input: {
    backgroundColor: colors.surfaceAlt,
    borderWidth: 1.5,
    borderColor: colors.borderStrong,
    borderRadius: radius.md,
    paddingHorizontal: 14,
    paddingVertical: 12,
    fontSize: 15,
    color: colors.text,
  },
  errorText: { color: colors.danger, fontSize: 13, marginTop: 10 },
  profileName: { fontSize: 17, fontWeight: "800", color: colors.text },
  profileLogin: { fontSize: 13, color: colors.textMuted, marginTop: 2 },
  profileBio: { fontSize: 12.5, color: colors.textMuted, marginTop: 8, textAlign: "center" },
  profileStatsRow: { flexDirection: "row", gap: 16, marginTop: 12 },
  profileStat: { fontSize: 12.5, fontWeight: "700", color: colors.indigo600 },
  scoreRow: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", marginBottom: 8 },
  scoreValue: { fontSize: 16, fontWeight: "800", color: colors.indigo600 },
  bodyText: { fontSize: 13.5, color: colors.text, lineHeight: 19 },
  subLabel: { fontSize: 11.5, fontWeight: "800", color: colors.textMuted, marginTop: 12, marginBottom: 4 },
  listItem: { fontSize: 13, color: colors.text, lineHeight: 19 },
  repoRow: { paddingVertical: 8, borderBottomWidth: 1, borderBottomColor: colors.border },
  repoName: { fontSize: 13.5, fontWeight: "700", color: colors.text },
  repoDesc: { fontSize: 12, color: colors.textMuted, marginTop: 2 },
});

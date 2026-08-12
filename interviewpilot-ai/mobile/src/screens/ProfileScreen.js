import React, { useEffect, useState } from "react";
import { View, Text, TextInput, StyleSheet, ScrollView, ActivityIndicator } from "react-native";
import { useAuth } from "../context/AuthContext";
import { api, ApiError } from "../api";
import { colors, radius } from "../theme";
import Button from "../components/Button";
import Card from "../components/Card";

export default function ProfileScreen() {
  const { logout, refresh } = useAuth();
  const [profile, setProfile] = useState(null);
  const [name, setName] = useState("");
  const [targetRole, setTargetRole] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    api
      .profile()
      .then((p) => {
        setProfile(p);
        setName(p.name || "");
        setTargetRole(p.target_role || "");
      })
      .catch((e) => setError(e instanceof ApiError ? e.message : "Profil yuklenemedi"))
      .finally(() => setLoading(false));
  }, []);

  const onSave = async () => {
    setError("");
    setSaved(false);
    setSaving(true);
    try {
      await api.updateProfile(name.trim(), targetRole.trim());
      setSaved(true);
      refresh();
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Kaydedilemedi");
    } finally {
      setSaving(false);
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
      <Card>
        <Text style={styles.label}>E-posta</Text>
        <Text style={styles.readonlyValue}>{profile?.email}</Text>

        <Text style={[styles.label, { marginTop: 16 }]}>Ad Soyad</Text>
        <TextInput style={styles.input} value={name} onChangeText={setName} placeholder="Ad Soyad" placeholderTextColor={colors.textFaint} />

        <Text style={[styles.label, { marginTop: 16 }]}>Hedef Rol</Text>
        <TextInput
          style={styles.input}
          value={targetRole}
          onChangeText={setTargetRole}
          placeholder="orn. Backend Gelistirici"
          placeholderTextColor={colors.textFaint}
        />

        {!!error && <Text style={styles.errorText}>{error}</Text>}
        {saved && <Text style={styles.savedText}>Kaydedildi</Text>}
        <Button title="Kaydet" onPress={onSave} loading={saving} style={{ marginTop: 16 }} />
      </Card>

      <Button title="Cikis Yap" variant="secondary" onPress={logout} style={{ marginTop: 16, marginBottom: 40 }} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  label: { fontSize: 12.5, fontWeight: "700", color: colors.textMuted, marginBottom: 6 },
  readonlyValue: { fontSize: 14.5, color: colors.textFaint },
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
  errorText: { color: colors.danger, fontSize: 13, marginTop: 12 },
  savedText: { color: colors.success, fontSize: 13, marginTop: 12 },
});

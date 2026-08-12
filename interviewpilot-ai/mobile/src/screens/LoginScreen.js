import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  TouchableOpacity,
} from "react-native";
import { useAuth } from "../context/AuthContext";
import { colors, radius } from "../theme";
import Button from "../components/Button";
import { ApiError } from "../api";

export default function LoginScreen({ navigation }) {
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const onSubmit = async () => {
    setError("");
    if (!email.trim()) return setError("E-posta gir");
    if (!password) return setError("Sifre gir");
    setLoading(true);
    try {
      await login(email.trim(), password);
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Giris basarisiz");
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      style={{ flex: 1, backgroundColor: colors.bg }}
      behavior={Platform.OS === "ios" ? "padding" : undefined}
    >
      <ScrollView contentContainerStyle={styles.container} keyboardShouldPersistTaps="handled">
        <View style={styles.brandRow}>
          <View style={styles.brandMark}>
            <Text style={styles.brandMarkText}>IP</Text>
          </View>
          <Text style={styles.brandName}>
            InterviewPilot <Text style={{ color: colors.indigo600 }}>AI</Text>
          </Text>
        </View>
        <Text style={styles.title}>Tekrar hos geldin</Text>
        <Text style={styles.subtitle}>Mulakat pratigine kaldigin yerden devam et</Text>

        <View style={styles.card}>
          <Text style={styles.label}>E-posta</Text>
          <TextInput
            style={styles.input}
            placeholder="ornek@eposta.com"
            placeholderTextColor={colors.textFaint}
            autoCapitalize="none"
            keyboardType="email-address"
            value={email}
            onChangeText={setEmail}
          />
          <Text style={styles.label}>Sifre</Text>
          <TextInput
            style={styles.input}
            placeholder="••••••••"
            placeholderTextColor={colors.textFaint}
            secureTextEntry
            value={password}
            onChangeText={setPassword}
          />
          {!!error && (
            <View style={styles.errorBox}>
              <Text style={styles.errorText}>{error}</Text>
            </View>
          )}
          <Button title="Giris Yap" onPress={onSubmit} loading={loading} style={{ marginTop: 6 }} />
        </View>

        <TouchableOpacity onPress={() => navigation.navigate("Register")} style={{ marginTop: 20 }}>
          <Text style={styles.footerText}>
            Hesabin yok mu? <Text style={{ color: colors.indigo600, fontWeight: "700" }}>Kayit ol</Text>
          </Text>
        </TouchableOpacity>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flexGrow: 1, padding: 24, justifyContent: "center" },
  brandRow: { flexDirection: "row", alignItems: "center", justifyContent: "center", marginBottom: 18, gap: 10 },
  brandMark: {
    width: 36,
    height: 36,
    borderRadius: 10,
    backgroundColor: colors.indigo600,
    alignItems: "center",
    justifyContent: "center",
    marginRight: 8,
  },
  brandMarkText: { color: "#fff", fontWeight: "800" },
  brandName: { fontSize: 18, fontWeight: "800", color: colors.text },
  title: { fontSize: 22, fontWeight: "800", color: colors.text, textAlign: "center" },
  subtitle: { fontSize: 13.5, color: colors.textMuted, textAlign: "center", marginTop: 6, marginBottom: 26 },
  card: {
    backgroundColor: colors.surface,
    borderRadius: radius.lg,
    borderWidth: 1,
    borderColor: colors.border,
    padding: 20,
  },
  label: { fontSize: 12.5, fontWeight: "700", color: colors.textMuted, marginBottom: 6, marginTop: 12 },
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
  errorBox: { backgroundColor: colors.dangerSoft, borderRadius: radius.md, padding: 10, marginTop: 14 },
  errorText: { color: colors.danger, fontSize: 13 },
  footerText: { textAlign: "center", fontSize: 13, color: colors.textFaint },
});

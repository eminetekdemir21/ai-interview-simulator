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

export default function RegisterScreen({ navigation }) {
  const { register } = useAuth();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const onSubmit = async () => {
    setError("");
    if (!name.trim()) return setError("Adini gir");
    if (!email.includes("@")) return setError("Gecerli bir e-posta gir");
    if (password.length < 6) return setError("Sifre en az 6 karakter olmali");
    if (password !== password2) return setError("Sifreler eslesmiyor");
    setLoading(true);
    try {
      await register(name.trim(), email.trim(), password);
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Kayit basarisiz");
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
        <Text style={styles.title}>Hesap olustur</Text>
        <Text style={styles.subtitle}>Mulakat pratigine baslamak icin kayit ol</Text>

        <View style={styles.card}>
          <Text style={styles.label}>Ad Soyad</Text>
          <TextInput style={styles.input} placeholder="Ad Soyad" placeholderTextColor={colors.textFaint} value={name} onChangeText={setName} />

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
            placeholder="En az 6 karakter"
            placeholderTextColor={colors.textFaint}
            secureTextEntry
            value={password}
            onChangeText={setPassword}
          />

          <Text style={styles.label}>Sifre (Tekrar)</Text>
          <TextInput
            style={styles.input}
            placeholder="••••••••"
            placeholderTextColor={colors.textFaint}
            secureTextEntry
            value={password2}
            onChangeText={setPassword2}
          />

          {!!error && (
            <View style={styles.errorBox}>
              <Text style={styles.errorText}>{error}</Text>
            </View>
          )}
          <Button title="Kayit Ol" onPress={onSubmit} loading={loading} style={{ marginTop: 6 }} />
        </View>

        <TouchableOpacity onPress={() => navigation.navigate("Login")} style={{ marginTop: 20 }}>
          <Text style={styles.footerText}>
            Zaten hesabin var mi? <Text style={{ color: colors.indigo600, fontWeight: "700" }}>Giris yap</Text>
          </Text>
        </TouchableOpacity>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flexGrow: 1, padding: 24, justifyContent: "center" },
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

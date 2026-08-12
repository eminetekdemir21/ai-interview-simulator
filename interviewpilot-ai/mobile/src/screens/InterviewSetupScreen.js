import React, { useEffect, useState } from "react";
import { View, Text, TextInput, StyleSheet, ScrollView, TouchableOpacity, ActivityIndicator } from "react-native";
import * as DocumentPicker from "expo-document-picker";
import { api, ApiError } from "../api";
import { colors, radius } from "../theme";
import Button from "../components/Button";
import Card from "../components/Card";

const DIFFICULTIES = [
  { val: "junior", label: "Junior", sub: "0-2 yil" },
  { val: "mid", label: "Mid-level", sub: "2-5 yil" },
  { val: "senior", label: "Senior", sub: "5+ yil" },
  { val: "staff", label: "Staff/Principal", sub: "8+ yil" },
];

const TYPES = [
  { val: "technical", label: "Teknik", sub: "Kod & kavramlar" },
  { val: "behavioral", label: "Davranissal", sub: "STAR yontemi" },
  { val: "system-design", label: "System Design", sub: "Mimari" },
  { val: "mixed", label: "Karisik", sub: "Hepsinden biraz" },
];

export default function InterviewSetupScreen({ navigation }) {
  const [companies, setCompanies] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState(null);
  const [role, setRole] = useState("");
  const [difficulty, setDifficulty] = useState(DIFFICULTIES[0]);
  const [type, setType] = useState(TYPES[0]);

  const [cvFile, setCvFile] = useState(null);
  const [jobFile, setJobFile] = useState(null);
  const [jobText, setJobText] = useState("");

  const [loadingCompanies, setLoadingCompanies] = useState(true);
  const [starting, setStarting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .companies()
      .then(setCompanies)
      .catch(() => setCompanies([]))
      .finally(() => setLoadingCompanies(false));
  }, []);

  const pickCv = async () => {
    const res = await DocumentPicker.getDocumentAsync({ type: ["application/pdf", "text/plain"] });
    if (!res.canceled && res.assets?.[0]) setCvFile(res.assets[0]);
  };

  const pickJob = async () => {
    const res = await DocumentPicker.getDocumentAsync({ type: ["application/pdf", "text/plain"] });
    if (!res.canceled && res.assets?.[0]) {
      setJobFile(res.assets[0]);
      setJobText("");
    }
  };

  const onStart = async () => {
    setError("");
    if (!cvFile) return setError("Once CV'ni yukle (PDF)");
    if (!jobFile && !jobText.trim()) return setError("Is ilani metni gir ya da dosya yukle");

    setStarting(true);
    try {
      const session = await api.createSession();
      const sessionId = session.session_id;

      await api.uploadCv(sessionId, cvFile);
      await api.uploadJob(sessionId, { file: jobFile, jobText: jobText.trim() || undefined });

      const question = await api.startInterview(sessionId, {
        companyId: selectedCompany?.id,
        role: role.trim(),
        difficulty: difficulty.label,
        interviewType: type.label,
        totalQuestions: 4,
      });

      navigation.replace("InterviewRoom", {
        sessionId,
        firstQuestion: question,
        meta: {
          company: selectedCompany ? selectedCompany.name : null,
          role: role.trim(),
          difficulty: difficulty.label,
          type: type.label,
        },
      });
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Mulakat baslatilamadi");
    } finally {
      setStarting(false);
    }
  };

  return (
    <ScrollView style={{ flex: 1, backgroundColor: colors.bg }} contentContainerStyle={{ padding: 16 }}>
      <SectionTitle title="1. CV'ni Yukle" />
      <Card>
        <PickRow label={cvFile ? cvFile.name : "PDF sec"} onPress={pickCv} filled={!!cvFile} />
      </Card>

      <SectionTitle title="2. Is Ilani" />
      <Card>
        <PickRow label={jobFile ? jobFile.name : "PDF sec"} onPress={pickJob} filled={!!jobFile} />
        <Text style={styles.orText}>ya da metin olarak yapistir</Text>
        <TextInput
          style={styles.textarea}
          placeholder="Is ilani metnini buraya yapistir..."
          placeholderTextColor={colors.textFaint}
          multiline
          value={jobText}
          onChangeText={(t) => {
            setJobText(t);
            if (t) setJobFile(null);
          }}
        />
      </Card>

      <SectionTitle title="3. Sirket (opsiyonel)" />
      {loadingCompanies ? (
        <ActivityIndicator color={colors.indigo600} />
      ) : (
        <View style={styles.chipWrap}>
          <Chip label="Genel" selected={!selectedCompany} onPress={() => setSelectedCompany(null)} />
          {companies.map((c) => (
            <Chip key={c.id} label={c.name} selected={selectedCompany?.id === c.id} onPress={() => setSelectedCompany(c)} />
          ))}
        </View>
      )}

      <SectionTitle title="4. Hedef Rol (opsiyonel)" />
      <Card>
        <TextInput
          style={styles.input}
          placeholder="orn. Backend Gelistirici"
          placeholderTextColor={colors.textFaint}
          value={role}
          onChangeText={setRole}
        />
      </Card>

      <SectionTitle title="5. Seviye" />
      <View style={styles.optGrid}>
        {DIFFICULTIES.map((d) => (
          <OptCard key={d.val} item={d} selected={difficulty.val === d.val} onPress={() => setDifficulty(d)} />
        ))}
      </View>

      <SectionTitle title="6. Mulakat Turu" />
      <View style={styles.optGrid}>
        {TYPES.map((t) => (
          <OptCard key={t.val} item={t} selected={type.val === t.val} onPress={() => setType(t)} />
        ))}
      </View>

      {!!error && (
        <Card style={{ backgroundColor: colors.dangerSoft, borderColor: colors.dangerSoft, marginTop: 16 }}>
          <Text style={{ color: colors.danger }}>{error}</Text>
        </Card>
      )}

      <Button title="Mulakati Baslat" onPress={onStart} loading={starting} style={{ marginTop: 22, marginBottom: 40 }} />
    </ScrollView>
  );
}

function SectionTitle({ title }) {
  return <Text style={styles.sectionTitle}>{title}</Text>;
}

function PickRow({ label, onPress, filled }) {
  return (
    <TouchableOpacity onPress={onPress} style={styles.pickRow}>
      <Text style={{ color: filled ? colors.text : colors.textFaint, flex: 1 }} numberOfLines={1}>
        {label}
      </Text>
      <Text style={{ color: colors.indigo600, fontWeight: "700" }}>Sec</Text>
    </TouchableOpacity>
  );
}

function Chip({ label, selected, onPress }) {
  return (
    <TouchableOpacity onPress={onPress} style={[styles.chip, selected && styles.chipSelected]}>
      <Text style={[styles.chipText, selected && styles.chipTextSelected]}>{label}</Text>
    </TouchableOpacity>
  );
}

function OptCard({ item, selected, onPress }) {
  return (
    <TouchableOpacity onPress={onPress} style={[styles.optCard, selected && styles.optCardSelected]}>
      <Text style={[styles.optTitle, selected && { color: colors.indigo600 }]}>{item.label}</Text>
      <Text style={styles.optSub}>{item.sub}</Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  sectionTitle: { fontSize: 13.5, fontWeight: "800", color: colors.text, marginTop: 18, marginBottom: 8 },
  pickRow: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: colors.surfaceAlt,
    borderWidth: 1.5,
    borderColor: colors.borderStrong,
    borderRadius: radius.md,
    paddingHorizontal: 14,
    paddingVertical: 12,
  },
  orText: { fontSize: 11.5, color: colors.textFaint, marginTop: 12, marginBottom: 6 },
  textarea: {
    backgroundColor: colors.surfaceAlt,
    borderWidth: 1.5,
    borderColor: colors.borderStrong,
    borderRadius: radius.md,
    paddingHorizontal: 14,
    paddingVertical: 12,
    fontSize: 14,
    color: colors.text,
    minHeight: 100,
    textAlignVertical: "top",
  },
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
  chipWrap: { flexDirection: "row", flexWrap: "wrap", gap: 8 },
  chip: {
    paddingHorizontal: 14,
    paddingVertical: 9,
    borderRadius: 999,
    backgroundColor: colors.surface,
    borderWidth: 1.5,
    borderColor: colors.borderStrong,
  },
  chipSelected: { backgroundColor: colors.indigo600, borderColor: colors.indigo600 },
  chipText: { fontSize: 12.5, fontWeight: "600", color: colors.text },
  chipTextSelected: { color: "#fff" },
  optGrid: { flexDirection: "row", flexWrap: "wrap", gap: 10 },
  optCard: {
    width: "47%",
    backgroundColor: colors.surface,
    borderWidth: 1.5,
    borderColor: colors.borderStrong,
    borderRadius: radius.md,
    padding: 14,
  },
  optCardSelected: { borderColor: colors.indigo, backgroundColor: colors.surfaceAlt },
  optTitle: { fontSize: 13.5, fontWeight: "700", color: colors.text },
  optSub: { fontSize: 11.5, color: colors.textFaint, marginTop: 2 },
});

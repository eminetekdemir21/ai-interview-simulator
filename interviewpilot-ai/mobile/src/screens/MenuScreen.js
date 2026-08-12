import React from "react";
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from "react-native";
import { colors, radius } from "../theme";

const SECTIONS = [
  {
    title: "Kariyer",
    items: [
      { label: "CV Analizi", sub: "ATS uyumlulugu ve icerik kalitesi", screen: "CvAnalysis" },
      { label: "Is Uyumu", sub: "CV'ni bir is ilaniyla karsilastir", screen: "JobMatch" },
      { label: "AI Kariyer Kocu", sub: "Gercek verilerine gore sohbet", screen: "CareerCoach" },
      { label: "Portfolyo", sub: "GitHub tabanli degerlendirme", screen: "Portfolio" },
    ],
  },
  {
    title: "Gelisim",
    items: [
      { label: "Analitik", sub: "Skor trendi ve alt beceriler", screen: "Analytics" },
      { label: "Yol Haritasi", sub: "Kisisellestirilmis ogrenme plani", screen: "Roadmap" },
      { label: "Gunluk Meydan Okuma", sub: "Her gun yeni bir mini soru", screen: "Challenge" },
    ],
  },
  {
    title: "Hesap",
    items: [{ label: "Profil", sub: "Ad, hedef rol, hesap bilgileri", screen: "Profile" }],
  },
];

export default function MenuScreen({ navigation }) {
  return (
    <ScrollView style={{ flex: 1, backgroundColor: colors.bg }} contentContainerStyle={{ padding: 16 }}>
      {SECTIONS.map((section) => (
        <View key={section.title} style={{ marginBottom: 22 }}>
          <Text style={styles.sectionTitle}>{section.title}</Text>
          {section.items.map((item) => (
            <TouchableOpacity key={item.screen} style={styles.row} onPress={() => navigation.navigate(item.screen)}>
              <View style={{ flex: 1 }}>
                <Text style={styles.rowLabel}>{item.label}</Text>
                <Text style={styles.rowSub}>{item.sub}</Text>
              </View>
              <Text style={styles.chevron}>›</Text>
            </TouchableOpacity>
          ))}
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  sectionTitle: { fontSize: 12, fontWeight: "800", color: colors.textFaint, marginBottom: 8, letterSpacing: 0.5 },
  row: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: colors.surface,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: radius.md,
    paddingHorizontal: 14,
    paddingVertical: 14,
    marginBottom: 8,
  },
  rowLabel: { fontSize: 14.5, fontWeight: "700", color: colors.text },
  rowSub: { fontSize: 12, color: colors.textMuted, marginTop: 2 },
  chevron: { fontSize: 20, color: colors.textFaint, marginLeft: 8 },
});

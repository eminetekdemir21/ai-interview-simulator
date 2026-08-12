import React, { useRef, useState } from "react";
import {
  View,
  Text,
  TextInput,
  StyleSheet,
  FlatList,
  KeyboardAvoidingView,
  Platform,
  TouchableOpacity,
  ActivityIndicator,
} from "react-native";
import { api, ApiError } from "../api";
import { colors, radius } from "../theme";

export default function CareerCoachScreen() {
  const [messages, setMessages] = useState([
    { role: "assistant", text: "Merhaba! Mulakat performansina gore sana yardimci olmak icin buradayim. Ne konusmak istersin?" },
  ]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");
  const listRef = useRef(null);

  const onSend = async () => {
    const text = input.trim();
    if (!text || sending) return;
    setError("");
    setInput("");
    const nextMessages = [...messages, { role: "user", text }];
    setMessages(nextMessages);
    setSending(true);
    try {
      const history = nextMessages.map((m) => ({ role: m.role === "user" ? "user" : "assistant", text: m.text }));
      const res = await api.coach(text, history);
      setMessages((prev) => [...prev, { role: "assistant", text: res.reply }]);
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Yanit alinamadi");
    } finally {
      setSending(false);
      setTimeout(() => listRef.current?.scrollToEnd({ animated: true }), 100);
    }
  };

  return (
    <KeyboardAvoidingView style={{ flex: 1, backgroundColor: colors.bg }} behavior={Platform.OS === "ios" ? "padding" : undefined}>
      <FlatList
        ref={listRef}
        data={messages}
        keyExtractor={(_, i) => String(i)}
        contentContainerStyle={{ padding: 16, gap: 10 }}
        onContentSizeChange={() => listRef.current?.scrollToEnd({ animated: false })}
        renderItem={({ item }) => (
          <View style={[styles.bubble, item.role === "user" ? styles.bubbleUser : styles.bubbleBot]}>
            <Text style={item.role === "user" ? styles.bubbleTextUser : styles.bubbleTextBot}>{item.text}</Text>
          </View>
        )}
      />
      {sending && (
        <View style={{ paddingHorizontal: 16, paddingBottom: 6 }}>
          <ActivityIndicator color={colors.indigo600} />
        </View>
      )}
      {!!error && (
        <Text style={{ color: colors.danger, fontSize: 12.5, paddingHorizontal: 16, paddingBottom: 6 }}>{error}</Text>
      )}
      <View style={styles.inputRow}>
        <TextInput
          style={styles.input}
          placeholder="Mesajini yaz..."
          placeholderTextColor={colors.textFaint}
          value={input}
          onChangeText={setInput}
          multiline
          editable={!sending}
        />
        <TouchableOpacity onPress={onSend} disabled={sending || !input.trim()} style={styles.sendBtn}>
          <Text style={styles.sendBtnText}>Gonder</Text>
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  bubble: { maxWidth: "84%", borderRadius: radius.lg, paddingHorizontal: 14, paddingVertical: 10 },
  bubbleUser: { alignSelf: "flex-end", backgroundColor: colors.indigo600 },
  bubbleBot: { alignSelf: "flex-start", backgroundColor: colors.surface, borderWidth: 1, borderColor: colors.border },
  bubbleTextUser: { color: "#fff", fontSize: 14, lineHeight: 20 },
  bubbleTextBot: { color: colors.text, fontSize: 14, lineHeight: 20 },
  inputRow: {
    flexDirection: "row",
    alignItems: "flex-end",
    padding: 12,
    borderTopWidth: 1,
    borderTopColor: colors.border,
    backgroundColor: colors.surface,
    gap: 8,
  },
  input: {
    flex: 1,
    backgroundColor: colors.surfaceAlt,
    borderWidth: 1.5,
    borderColor: colors.borderStrong,
    borderRadius: radius.md,
    paddingHorizontal: 14,
    paddingVertical: 10,
    fontSize: 14,
    color: colors.text,
    maxHeight: 110,
  },
  sendBtn: {
    backgroundColor: colors.indigo600,
    borderRadius: radius.md,
    paddingHorizontal: 16,
    paddingVertical: 12,
  },
  sendBtnText: { color: "#fff", fontWeight: "700", fontSize: 13 },
});

// =====================================================================
// Logika antarmuka chat: kirim pesan ke /api/chat dengan fetch()
// lalu tampilkan balasan tanpa memuat ulang halaman.
// =====================================================================
const messagesEl = document.getElementById("messages");
const form = document.getElementById("chat-form");
const input = document.getElementById("chat-input");
const sendButton = form.querySelector('button[type="submit"]');

/** Tambahkan satu gelembung pesan ke layar. */
function addMessage(sender, text) {
  const row = document.createElement("div");
  row.className = `msg msg-${sender}`;

  if (sender === "bot") {
    const avatar = document.createElement("span");
    avatar.className = "msg-avatar";
    avatar.textContent = THEME.avatar;
    row.appendChild(avatar);
  }

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;            // textContent, BUKAN innerHTML -> aman dari XSS

  row.appendChild(bubble);
  messagesEl.appendChild(row);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return bubble;
}

/** Kirim pesan ke server. */
async function sendMessage(text) {
  document.querySelectorAll(".chip").forEach((chip) => { chip.disabled = true; });
  addMessage("user", text);
  const typing = addMessage("bot", "Sedang menyiapkan balasan…").parentElement;
  typing.setAttribute("role", "status");
  input.disabled = true;
  sendButton.disabled = true;

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, theme: THEME.id }),
    });
    const data = await res.json();
    typing.remove();

    if (!res.ok) {
      addMessage("bot", `⚠️ ${data.error}`);
      return;
    }
    addMessage("bot", data.reply);
  } catch (err) {
    typing.remove();
    addMessage("bot", "⚠️ Gagal terhubung ke server.");
    console.error(err);
  } finally {
    input.disabled = false;
    sendButton.disabled = false;
    document.querySelectorAll(".chip").forEach((chip) => { chip.disabled = false; });
    input.focus();
  }
}

/** Muat riwayat percakapan saat halaman dibuka. */
async function loadHistory() {
  try {
    const res = await fetch(`/api/history/${THEME.id}`);
    const rows = res.ok ? await res.json() : [];
    if (rows.length === 0) {
      addMessage("bot", THEME.greeting);
      return;
    }
    rows.forEach((r) => addMessage(r.sender, r.text));
  } catch (err) {
    addMessage("bot", THEME.greeting);
  }
}

// ---- Event listener ------------------------------------------------
form.addEventListener("submit", (e) => {
  e.preventDefault();                     // cegah form memuat ulang halaman
  const text = input.value.trim();
  if (!text) return;                      // pesan kosong diabaikan
  input.value = "";
  sendMessage(text);
});

document.querySelectorAll(".chip").forEach((chip) => {
  chip.addEventListener("click", () => sendMessage(chip.textContent));
});

loadHistory();

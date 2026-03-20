# 🦙 AI-chat-app-using-Groq-LLaMA-4-Scout


A sleek, fast AI chat interface built with **Streamlit**, powered by **Groq's inference engine** and **Meta's LLaMA 4 Scout** model. Ask anything and get blazing-fast responses with a clean dark UI.

---

## ✨ Features

- ⚡ **Ultra-fast inference** via Groq's hardware-optimized API
- 🧠 **Multi-model support** — LLaMA 4 Scout, LLaMA 4 Maverick, LLaMA 3, Mixtral
- 🎨 **Custom dark UI** — styled with CSS for a polished chat experience
- 🔧 **Configurable settings** — temperature, max tokens, and model selection via sidebar
- 💬 **Context-aware conversations** — full message history sent to the model each turn
- 🗑️ **Clear chat** — reset the conversation anytime

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Frontend | Streamlit + Custom CSS |
| LLM Backend | Groq API |
| Model | meta-llama/llama-4-scout-17b-16e-instruct |
| Language | Python 3.8+ |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/llama4-scout-chat.git
cd llama4-scout-chat
```

### 2. Install dependencies

```bash
pip install streamlit groq
```

### 3. Get your Groq API key

Sign up at [console.groq.com](https://console.groq.com) and generate a free API key.

### 4. Run the app

```bash
streamlit run groq_chat_app.py
```

Then open `http://localhost:8501` in your browser.

---

## 🔑 API Key Setup

You can provide your Groq API key in two ways:

**Option A — Via the sidebar (recommended):**
Enter it directly in the app's sidebar under `Groq API Key`.

**Option B — Via environment variable:**
```bash
export GROQ_API_KEY="gsk_your_key_here"
streamlit run groq_chat_app.py
```

---

## ⚙️ Configuration Options

| Setting | Range | Default | Description |
|---|---|---|---|
| Model | 5 options | LLaMA 4 Scout | The LLM model to use |
| Temperature | 0.0 – 2.0 | 1.0 | Controls response creativity |
| Max Tokens | 256 – 4096 | 1024 | Maximum response length |

---

## 📁 Project Structure

```
llama4-scout-chat/
│
├── groq_chat_app.py   # Main Streamlit app
└── README.md          # Project documentation
```

---

## 🤖 Supported Models

| Model | Best For |
|---|---|
| `meta-llama/llama-4-scout-17b-16e-instruct` | Fast, general-purpose Q&A |
| `meta-llama/llama-4-maverick-17b-128e-instruct` | Long context tasks |
| `llama3-70b-8192` | High-quality detailed responses |
| `llama3-8b-8192` | Lightweight, quick replies |
| `mixtral-8x7b-32768` | Multilingual & long documents |

---

## 📌 Notes

- The app displays only the **latest question and answer** on screen, keeping the UI clean — while still sending the full conversation history to the model for context.
- API keys are never stored permanently; they exist only in the current session.

---


> Built with 🧡 using Groq + LLaMA 4 + Streamlit

import streamlit as st
import requests
import json

# --- Fungsi ambil respons AI ---
def get_ai_response(messages_payload):
    api_key = "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"  # ganti dengan API key OpenRouter
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        data=json.dumps({
            "model": "openai/gpt-4o-mini",  # default GPT Mini
            "messages": messages_payload,
            "max_tokens": 1000,
            "temperature": 0.7,
        }),
    )

    if response.status_code != 200:
        return None

    data = response.json()
    choice = data["choices"][0]

    if "message" in choice and "content" in choice["message"]:
        return choice["message"]["content"]

    if "text" in choice:
        return choice["text"]

    return None


# --- State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = {}   # {judul: [messages]}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

if "new_chat_flag" not in st.session_state:
    st.session_state.new_chat_flag = False


# --- Sidebar ---
with st.sidebar:
    st.markdown("<h1 style='font-size: 28px;'>🤖 AI Chatbot</h1>", unsafe_allow_html=True)

    if st.button("➕ New Chat"):
        st.session_state.messages = []
        st.session_state.current_chat = None
        st.rerun()

    st.divider()
    st.subheader("📜 Conversations")

    if st.session_state.history:
        for title in list(st.session_state.history.keys()):
            col1, col2 = st.columns([6, 1])  # lebih besar space untuk judul
            with col1:
                if st.button(title, key=f"open_{title}"):
                    st.session_state.messages = st.session_state.history[title].copy()
                    st.session_state.current_chat = title
            with col2:
                if st.button("🗑", key=f"delete_{title}"):
                    del st.session_state.history[title]
                    if st.session_state.current_chat == title:
                        st.session_state.messages = []
                        st.session_state.current_chat = None
                    st.rerun()

        if st.button("🧹 Clear All"):
            st.session_state.history = {}
            st.session_state.messages = []
            st.session_state.current_chat = None
            st.rerun()


# --- Tampilan Tengah ---
if not st.session_state.messages:  # welcome hanya kalau belum ada chat sama sekali
    st.markdown(
        """
        <div style="display: flex; flex-direction: column; 
                    align-items: center; justify-content: center; 
                    height: 70vh; color: gray;">
            <div style="font-size: 50px;">💬</div>
            <h2>Welcome to AI Chatbot</h2>
            <p>Start a new conversation to begin chatting</p>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    # CSS bubble chat
    st.markdown("""
    <style>
    .chat-bubble {
        max-width: 70%;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 8px;
        line-height: 1.4;
    }
    .user-bubble {
        background-color: #DCF8C6;
        margin-left: auto;
        text-align: right;
    }
    .assistant-bubble {
        background-color: #F1F0F0;
        margin-right: auto;
        text-align: left;
    }
    </style>
    """, unsafe_allow_html=True)

    # tampilkan semua messages yang sudah ada
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]

        if role == "user":
            st.markdown(f"<div class='chat-bubble user-bubble'>{content}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-bubble assistant-bubble'>{content}</div>", unsafe_allow_html=True)


# --- Input user ---
if prompt := st.chat_input("Tulis pesan..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    # kalau chat pertama → bikin judul
    if st.session_state.current_chat is None:
        title = " ".join(prompt.split()[:5]) + ("..." if len(prompt.split()) > 5 else "")
        st.session_state.current_chat = title
        st.session_state.history[title] = st.session_state.messages.copy()
        st.session_state.new_chat_flag = True

    # tampilkan bubble user langsung
    st.markdown(f"<div class='chat-bubble user-bubble'>{prompt}</div>", unsafe_allow_html=True)

    # respon AI (langsung jalan juga di chat pertama)
    with st.spinner("Berpikir..."):
        messages_for_api = st.session_state.messages.copy()
        ai_response = get_ai_response(messages_for_api)

        if ai_response:
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            st.session_state.history[st.session_state.current_chat] = st.session_state.messages.copy()
            st.markdown(f"<div class='chat-bubble assistant-bubble'>{ai_response}</div>", unsafe_allow_html=True)
        else:
            st.error("Error: Gagal mendapatkan respons dari AI")

    # kalau chat pertama → refresh setelah respon muncul biar sidebar/history update
    if st.session_state.new_chat_flag:
        st.session_state.new_chat_flag = False
        st.rerun()

# 🤖 AI Chatbot

Aplikasi chatbot sederhana berbasis **Streamlit** yang terhubung ke **OpenRouter API (GPT-4o-mini)**.  
Mendukung multi-chat, menyimpan riwayat percakapan, dan tampilan balon obrolan seperti aplikasi chat.

---

## ✨ Fitur
- 💬 Chat interaktif dengan AI.  
- 📜 Menyimpan dan membuka kembali riwayat percakapan.  
- ➕ Membuat percakapan baru.  
- 🗑 Menghapus percakapan tertentu atau semua riwayat sekaligus.  
- 🎨 Tampilan **chat bubble** (user vs AI) mirip aplikasi pesan.  

---

## 🚀 Cara Menjalankan
1. Pastikan Python sudah terinstall (versi 3.9 ke atas).  

2. Install library yang dibutuhkan:
   ```bash
   pip install streamlit requests

3. Buka file app.py, lalu ganti API key dengan milikmu:
    ```bash
    api_key = "sk-or-v1-xxxxxxxxxxxxxxxxxxxxx"  # ganti dengan API key OpenRouter punyamu

4. Jalankan aplikasi:
    ```bash
    streamlit run chatbot.py

import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from openai import OpenAI

# ================= CONFIG =================
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(
    page_title="CatBot Dashboard",
    page_icon="🐱",
    layout="wide"
)

# ================= SIDEBAR =================
with st.sidebar:
    st.title("🐱 CatBot")
    st.markdown("**Dashboard Generative AI**")
    st.markdown("Analisis tren pencarian kucing")
    menu = st.radio(
        "Navigasi",
        ["Beranda", "Chatbot"]
    )
    st.markdown("---")
    st.caption("Digunakan untuk keperluan akademik")

# ================= GOOGLE TRENDS (STATIC CSV) =================
@st.cache_data
def load_trend_data():
    return pd.read_csv("trend_kucing.csv")

trend_df = load_trend_data()

# ================= BERANDA =================
if menu == "Beranda":
    st.title("📊 Dashboard Tren Pencarian Kucing")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📈 Seberapa Sering Orang Mencari Tren Kucing")

        fig, ax = plt.subplots()
        ax.plot(
            trend_df["date"],
            trend_df["kucing"],
            linewidth=2
        )
        ax.set_xlabel("Waktu")
        ax.set_ylabel("Indeks Minat Pencarian")
        ax.set_title("Tren Pencarian Kata 'Kucing' di Google (Indonesia)")
        ax.grid(True)

        st.pyplot(fig)

    with col2:
        st.subheader("🧠 Insight Awal")
        st.write(
            """
            - Minat pencarian tentang **kucing** cenderung stabil sepanjang tahun  
            - Terjadi peningkatan pada periode tertentu  
            - Data dapat dimanfaatkan untuk edukasi dan analisis tren  
            """
        )

# ================= CHATBOT =================
if menu == "Chatbot":
    st.title("💬 Chatbot Analisis Tren Kucing")

    st.markdown(
        """
        Chatbot ini mampu:
        - Menjawab pertanyaan tentang kucing  
        - Menganalisis data tren pencarian  
        - Memberikan insight berdasarkan grafik  
        """
    )

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "Kamu adalah CatBot, chatbot edukatif yang "
                    "menganalisis tren pencarian kucing dan "
                    "menjawab dengan bahasa Indonesia yang mudah dipahami."
                )
            }
        ]

    for msg in st.session_state.messages[1:]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Tanya tentang kucing atau tren pencariannya...")

    if user_input:
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        # Ringkasan data tren untuk AI
        trend_summary = trend_df.tail(5).to_string(index=False)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages + [
                {
                    "role": "system",
                    "content": (
                        "Berikut ringkasan data tren pencarian kucing:\n"
                        + trend_summary
                    )
                }
            ]
        )

        bot_reply = response.choices[0].message.content

        st.session_state.messages.append(
            {"role": "assistant", "content": bot_reply}
        )

        with st.chat_message("assistant"):
            st.markdown(bot_reply)

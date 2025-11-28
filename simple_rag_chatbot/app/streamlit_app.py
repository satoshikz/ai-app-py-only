"""Simple RAG chat app using Streamlit"""

import streamlit as st
from llm import SimpleRAGChatbot

st.title("Simple RAG Chatbot")
st.caption("AI技術に関する質問に答えます")

# Initialize session state
if "chatbot" not in st.session_state:
    with st.spinner("ベクトルデータベースを初期化中..."):
        st.session_state.chatbot = SimpleRAGChatbot()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("質問を入力してください"):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("回答を生成中..."):
            response = st.session_state.chatbot.chat(prompt)
        st.markdown(response)

        # Show sources in expander
        with st.expander("📚 参照した情報源"):
            sources = st.session_state.chatbot.get_sources(prompt)
            for i, doc in enumerate(sources, 1):
                st.markdown(f"**ソース {i}:**")
                st.text(doc.page_content[:300] + "...")
                st.divider()

    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar
with st.sidebar:
    st.header("設定")

    if st.button("会話をリセット", use_container_width=True):
        st.session_state.chatbot.reset()
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.subheader("使い方")
    st.markdown(
        """
        このチャットボットは、AI技術に関する知識ベースを使用して質問に答えます。

        **質問例:**
        - RAGとは何ですか？
        - ベクトルデータベースの利点は？
        - プロンプトエンジニアリングの手法を教えて
        - LLMの主要なモデルは？
        """
    )

    st.divider()

    st.caption("Powered by LangChain & ChromaDB")

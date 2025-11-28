# ai-app-py-only

PythonでAIアプリを作るテンプレート

## 使用技術

- **uv** - パッケージマネージャー
- **LangChain** - LLMアプリケーションフレームワーク
- **LangSmith** - LLMアプリケーション監視
- **OpenAI API** - LLM
- **Streamlit** - WebUIフレームワーク
- **ChromaDB** - ベクトルデータベース
- **DeepEval** - LLM評価フレームワーク
- **Codex CLI** - コーディングエージェント

## セットアップ

```bash
# uvのインストール
curl -LsSf https://astral.sh/uv/install.sh | sh

# 仮想環境の作成
uv venv

# 依存関係のインストール
uv sync

# 環境変数の設定
cp .env.example .env
# .envにAPIキーを設定
```

## アプリ(テンプレート)

### Simple Chatbot
基本的なチャットボット

```bash
uv run streamlit run simple_chatbot/app/streamlit_app.py
```

### Simple RAG Chatbot
ベクトル検索を使ったRAGチャットボット

```bash
uv run streamlit run simple_rag_chatbot/app/streamlit_app.py
```

## 評価

```bash
# Simple Chatbot
uv run python simple_chatbot/evals/metrics.py

# RAG Chatbot
uv run python simple_rag_chatbot/evals/metrics.py
```

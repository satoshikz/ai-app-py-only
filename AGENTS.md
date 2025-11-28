# Repository Guidelines

このリポジトリは LangChain・OpenAI・Streamlit・ChromaDB を使った 2 種類のチャットボットのテンプレートです。以下の手引きに従い、追加開発や運用を統一してください。すべての議論と成果物は日本語でまとめ、実装に入る前に必ず設計内容をレビューし合意を得てください。

## 作業方針
- 対話や設計資料は必ず日本語で記述します。
- Issue や PR コメントは英語で記述します。
- 新機能や改善に着手する際は、要件・アーキテクチャ・テスト方針を設計ドキュメントとして示し、関係者の合意を得てから実装へ進みます。

## プロジェクト構成とモジュール配置
- `simple_chatbot/` は基本チャット UI (`app/streamlit_app.py`) と LangChain 構成 (`app/llm.py`)、評価スクリプト (`evals/`) を持ちます。
- `simple_rag_chatbot/` は同じレイアウトで、`data/` にベクトル化対象を置き、RAG 専用のリトリーバーを `app/` で定義します。
- 新しいアプリはこの 2 ディレクトリを参照して並列構成（`app/`, `data/`, `evals/`）を複製し、共通設定は `pyproject.toml`・`uv.lock` を経由して共有してください。

## 技術スタック
- LangChain（core/community/text splitters/openai）でチェーン構築、LangSmith で観測、ChromaDB でベクトル検索、DeepEval で品質評価を行います。
- Web UI は Streamlit、LLM/API は OpenAI（`gpt-4.1-mini` など低コストモデル）を前提とし、環境変数でキーを与えます。
- 依存管理は `uv`（`pyproject.toml` + `uv.lock`）で固定されているため、追加パッケージも `uv add` を使用してください。

## ビルド・テスト・開発コマンド
- `uv venv && uv sync`：Python 3.13 仮想環境の作成と依存解決。
- `uv run streamlit run simple_chatbot/app/streamlit_app.py`（RAG 版はパスを差し替え）でローカルサーバー起動。
- `uv run python simple_chatbot/evals/metrics.py` および `uv run python simple_rag_chatbot/evals/metrics.py` は必須の DeepEval スイート。新アプリでも評価スクリプトを実装し、同等のコマンドを整備してください。

## コーディングスタイルと命名規則
- Python は 4 スペースインデント、関数・変数は snake_case、定数は UPPER_SNAKE_CASE、公開関数には型ヒントと Google スタイルの docstring を付けます。
- Streamlit 側は UI ロジックを `streamlit_app.py` に限定し、チェーンやユーティリティは `llm.py` や新規モジュールへ切り出します。
- 依存機能を更新する際は `uv pip list | rg langchain` などでインストール済みバージョンを確認し、公式ドキュメントの最新仕様を参照してから実装してください。

## テスト指針
- すべてのアプリで DeepEval を用いた評価シナリオを実装し、`{feature}_metrics.py` の命名でケースを積み増します。
- `simple_rag_chatbot/data/` へ追加するデータは小さな決定論的サンプルを含め、検索再現性を担保します。
- PR では実行した評価コマンドと結果の概略を記述し、重大なチェーン変更時はカバレッジの変化も言及してください。

## コミットとプルリクエスト
- Git 履歴に合わせた短い命令形（例：`Add RAG prompts`, `Fix eval flow`）で一機能一コミットを徹底します。
- PR 説明には目的、関連 Issue、実行コマンド、必要なら UI のスクリーンショット、環境変数の追加箇所を含めます。
- 新規アプリや評価フローを提案する際は、simple_* との整合ポイントと DeepEval 実装状況を明示してください。

## セキュリティと設定
- `.env.example` を `.env` にコピーし、API キーはローカルのみに保持して `os.environ.get` で参照します。
- 企業や個人データは `simple_rag_chatbot/data/private/` などに隔離し、マスキングや削除手順を PR で共有してください。

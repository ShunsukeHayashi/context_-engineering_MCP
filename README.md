# 🤖 MCP AI ガイドサーバー

OpenAI、Google、Anthropicが公開する厳選されたAI関連ガイドの集約リポジトリおよび検索インターフェースです。

このサーバーは、これらのガイドのメタデータ（タイトル、発行者、説明、トピック、直接ダウンロードリンク）へのプログラマティックアクセスを提供し、AIエージェント構築、プロンプトエンジニアリング、企業規模のAI展開などの分野をカバーしています。

## ✨ 主な機能

### 🔍 基本機能
- **全ガイド一覧**: 利用可能なすべてのAIガイドの包括的なリストを取得
- **ガイド検索**: タイトルや説明のキーワードやトピックに基づいてガイドをフィルタリング
- **ガイド詳細取得**: 特定のAIガイドの完全なメタデータにアクセス
- **ダウンロードURL取得**: 特定のガイドの直接ダウンロードリンクを取得
- **ヘルスチェック**: サーバーの状態を確認するエンドポイント

### 🧠 Gemini AI 強化機能
- **セマンティック検索**: Gemini AIによる意味理解ベースの検索
- **ガイド分析**: ガイドの詳細分析と学習目標の生成
- **URL コンテンツ分析**: 外部URLからのガイド内容の分析
- **ガイド比較**: 複数のガイドの比較分析

### 🤖 MCP Server 統合
- **Claude Desktop 連携**: MCPプロトコルによるClaude Desktopとの統合
- **8つのツール**: ガイド管理とAI分析のための包括的なツールセット

### 📊 ワークフロー管理システム
- **自動ワークフロー生成**: 自然言語入力からのワークフロー自動作成
- **インテリジェントタスク分解**: AIによる最適なタスク分割
- **エージェント管理**: 能力と負荷を考慮した自動アサイン
- **リアルタイム可視化**: 美しいダッシュボードでの進捗追跡

## 🛠️ 前提条件

- Python 3.10+
- pip (Pythonパッケージインストーラー)
- Docker (オプション、コンテナ化デプロイメント用)
- Google Gemini API キー

## 🚀 セットアップと実行

### 1. リポジトリのクローン
```bash
git clone https://github.com/ShunsukeHayashi/context_-engineering_MCP.git
cd "context engineering_mcp_server"
```

### 2. 仮想環境の作成（推奨）
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 3. 依存関係のインストール
```bash
pip install -r requirements.txt
```

### 4. 環境設定
```bash
cp .env.example .env
# .envファイルを編集してGEMINI_API_KEYを設定
```

### 5. サーバーの起動

#### AI Guides API サーバー
```bash
uvicorn main:app --host 0.0.0.0 --port 8888 --reload
```

#### ワークフロー管理システム
```bash
cd workflow_system
export GEMINI_API_KEY="your_api_key_here"
./start_workflow_system.sh
```

## 🌐 アクセス方法

### AI Guides API
- **API サーバー**: http://localhost:8888
- **API ドキュメント**: http://localhost:8888/docs
- **ReDoc**: http://localhost:8888/redoc

### ワークフロー管理システム
- **ダッシュボード**: http://localhost:9000
- **API**: http://localhost:9000/api/*
- **WebSocket**: ws://localhost:9000/ws

### MCP Server (Claude Desktop)
Claude Desktop の設定ファイルに自動追加されます：
- 8つのツールが利用可能
- AI ガイドの検索・分析・比較機能

## 🔧 Docker での実行

### 1. Docker イメージのビルド
```bash
docker build -t mcp-ai-guides-server .
```

### 2. Docker コンテナの実行
```bash
docker run -d --name ai-guides-app -p 8888:8888 mcp-ai-guides-server
```

## 📡 API エンドポイント

### 基本エンドポイント

#### `GET /health`
サーバーの状態確認
```json
{
  "status": "ok",
  "service": "MCP AI Guides Server",
  "version": "1.0.0"
}
```

#### `GET /guides`
全AIガイドの一覧取得

#### `GET /guides/search?query={keyword}`
キーワードによるガイド検索

#### `GET /guides/{title}`
特定ガイドの詳細取得

#### `GET /guides/{title}/download-url`
ダウンロードURLの取得

### Gemini AI 強化エンドポイント

#### `POST /guides/search/gemini`
セマンティック検索
```json
{
  "query": "AIエージェントの構築方法",
  "use_grounding": true
}
```

#### `GET /guides/{title}/analyze`
ガイドの詳細分析

#### `POST /guides/analyze-url`
URLからのコンテンツ分析

#### `POST /guides/compare`
複数ガイドの比較
```json
{
  "guide_titles": [
    "OpenAI: GPT Best Practices",
    "Google: Introduction to Generative AI"
  ]
}
```

### ワークフロー管理 API

#### `POST /api/workflows`
新しいワークフロー作成
```json
{
  "user_input": "ECサイトの商品管理システムを開発してください",
  "context": {"budget": 100000, "deadline": "2024-03-01"}
}
```

#### `GET /api/workflows`
ワークフロー一覧取得

#### `GET /api/workflows/{workflow_id}`
特定ワークフローの詳細

#### `POST /api/workflows/{workflow_id}/start`
ワークフロー実行開始

## 🧰 MCP Tools (Claude Desktop)

1. **list_ai_guides** - 全ガイドの一覧
2. **search_ai_guides** - キーワード検索
3. **get_guide_details** - ガイド詳細取得
4. **get_guide_download_url** - ダウンロードURL取得
5. **search_guides_with_gemini** - Gemini セマンティック検索
6. **analyze_guide** - ガイド分析
7. **analyze_guide_url** - URL分析
8. **compare_guides** - ガイド比較

## 🎯 使用例

### 基本的な検索
```bash
curl "http://localhost:8888/guides/search?query=agent"
```

### Gemini による高度な検索
```bash
curl -X POST "http://localhost:8888/guides/search/gemini" \
  -H "Content-Type: application/json" \
  -d '{"query": "機械学習プロジェクトの始め方", "use_grounding": true}'
```

### ワークフロー作成
```bash
curl -X POST "http://localhost:9000/api/workflows" \
  -H "Content-Type: application/json" \
  -d '{"user_input": "チャットボットを開発したい"}'
```

### Claude Desktop での使用
```
「AIエージェントに関するガイドを検索して」
「OpenAI GPT Best Practices を分析して」
「プロンプトエンジニアリングのガイドを比較して」
```

## 📊 システム構成

### コアコンポーネント
- **main.py**: FastAPI メインアプリケーション
- **gemini_service.py**: Gemini AI 統合サービス
- **mcp-server/**: Claude Desktop MCP サーバー
- **workflow_system/**: AI ワークフロー管理システム

### ワークフローシステム
- **workflow_models.py**: データモデル
- **workflow_generator.py**: AI ワークフロー生成
- **agent_manager.py**: エージェント管理
- **workflow_api.py**: API サーバー
- **dashboard.html**: リアルタイム可視化

## 🔧 カスタマイズ

### 新しいガイドの追加
`main.py` の `AI_GUIDES_DATA` に追加：
```python
{
    "title": "新しいガイドタイトル",
    "publisher": "発行者名",
    "description": "ガイドの説明",
    "topics": ["トピック1", "トピック2"],
    "download_url": "https://example.com/guide.pdf"
}
```

### エージェントタイプの追加
`workflow_models.py` で新しいエージェントタイプを定義

### ダッシュボードのカスタマイズ
`dashboard.html` のCSS/JavaScriptを修正

## 🐛 エラーハンドリング

- **404 Not Found**: ガイドが見つからない場合
- **500 Internal Server Error**: サーバー内部エラー
- **認証エラー**: Gemini API キーが無効な場合

## 🚀 パフォーマンス最適化

- Gemini API のレート制限に注意
- 大量のガイドの場合はデータベース使用を検討
- WebSocket接続数の制限
- キャッシュの実装

## 🤝 開発への貢献

このプロジェクトはオープンソースです。Issue報告やPull Requestをお待ちしています。

### 開発の開始
```bash
# 開発環境のセットアップ
pip install -r requirements.txt
pip install pytest pytest-asyncio httpx  # テスト用

# テストの実行
pytest

# 開発サーバーの起動
uvicorn main:app --reload
```

## 📄 ライセンス

MIT License - 詳細は LICENSE ファイルを参照してください。

## 🆘 サポート

問題が発生した場合：
1. [Issues](https://github.com/ShunsukeHayashi/context_-engineering_MCP/issues) でバグ報告
2. [Discussions](https://github.com/ShunsukeHayashi/context_-engineering_MCP/discussions) で質問
3. 📧 開発者への直接連絡

---

**🤖 このプロジェクトは Claude Code によって生成されました**

完全なAI駆動のワークフロー管理システムで、自然言語入力からタスク分解、エージェントアサイン、リアルタイム進捗追跡まで、すべてをカバーします。
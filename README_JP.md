# 🧠 Context Engineering MCP プラットフォーム

単なるAIガイドの取得にとどまらず、完全なコンテキスト管理、最適化、プロンプトエンジニアリング機能を提供する包括的なAI駆動のContext Engineeringプラットフォームです。

## ✨ 主な機能

### 📚 AIガイド管理
- **完全なガイドリスト**: OpenAI、Google、AnthropicのAIガイドの包括的なメタデータにアクセス
- **検索機能**: キーワード、トピック、説明によるガイドのフィルタリング
- **セマンティック検索**: Gemini AIによる意味理解ベースの高度な検索
- **ガイド分析**: 学習目標生成を含む詳細分析
- **ガイド比較**: 複数ガイドの並列比較

### 🔧 Context Engineering システム
- **コンテキストウィンドウ管理**: トークン追跡機能付きコンテキストウィンドウの作成・管理
- **コンテキスト分析**: セマンティック一貫性チェックを含むAI駆動の品質評価
- **最適化エンジン**: トークン削減、明確性、関連性の自動最適化
- **マルチモーダル対応**: テキスト、画像、音声、動画、ドキュメントの処理
- **RAG統合**: 検索拡張生成のコンテキスト管理

### 📋 プロンプトテンプレート管理
- **テンプレート作成**: 再利用可能なプロンプトテンプレートの作成・管理
- **AI生成**: 目的と例に基づくテンプレートの自動生成
- **バージョン管理**: テンプレート使用状況と品質スコアの追跡
- **テンプレートレンダリング**: 動的な変数置換

### 🤖 MCP サーバー統合
- **Claude Desktop サポート**: 完全なMCPプロトコル統合
- **15の包括的なツール**: コンテキストエンジニアリング用の完全なツールセット
- **リアルタイム更新**: ライブ更新のためのWebSocketサポート

### 📊 ワークフロー管理
- **自動ワークフロー生成**: 自然言語入力からのワークフロー作成
- **インテリジェントタスク分解**: AI駆動のタスク分割
- **エージェント管理**: 能力に基づく自動割り当て
- **リアルタイム可視化**: 進捗追跡のための美しいダッシュボード

## 🛠️ 前提条件

- Python 3.10+
- Node.js 16+ (MCPサーバー用)
- Google Gemini API キー
- Docker (オプション、コンテナ化デプロイメント用)

## 🚀 セットアップとインストール

### 1. リポジトリのクローン
```bash
git clone https://github.com/ShunsukeHayashi/context_-engineering_MCP.git
cd "context engineering_mcp_server"
```

### 2. 環境設定
```bash
cp .env.example .env
# .envファイルを編集してGEMINI_API_KEYを追加
```

### 3. 依存関係のインストール

#### AI Guides API サーバー用
```bash
pip install -r requirements.txt
```

#### Context Engineering システム用
```bash
cd context_engineering
python -m venv context_env
source context_env/bin/activate  # Windows: context_env\Scripts\activate
pip install -r requirements.txt
```

#### MCP サーバー用
```bash
cd mcp-server
npm install
```

## 🌐 プラットフォームの実行

### 1. AI Guides API サーバー
```bash
uvicorn main:app --host 0.0.0.0 --port 8888 --reload
```

### 2. Context Engineering API サーバー
```bash
cd context_engineering
./start_context_engineering.sh
```

### 3. MCP サーバー (Claude Desktop用)
```bash
cd mcp-server
node context_mcp_server.js
```

## 🌍 アクセスポイント

### AI Guides API
- **APIサーバー**: http://localhost:8888
- **APIドキュメント**: http://localhost:8888/docs
- **ReDoc**: http://localhost:8888/redoc

### Context Engineering プラットフォーム
- **ダッシュボード**: http://localhost:9001
- **APIドキュメント**: http://localhost:9001/docs
- **WebSocket**: ws://localhost:9001/ws

### MCP サーバー設定
Claude Desktop の設定に追加:
```json
{
  "mcpServers": {
    "context-engineering": {
      "command": "node",
      "args": ["/path/to/mcp-server/context_mcp_server.js"]
    }
  }
}
```

## 📡 API エンドポイント

### AI Guides エンドポイント

#### 基本エンドポイント
- `GET /guides` - 全AIガイドの一覧
- `GET /guides/search?query={keyword}` - ガイド検索
- `GET /guides/{title}` - ガイド詳細取得
- `GET /guides/{title}/download-url` - ダウンロードURL取得

#### Gemini強化エンドポイント
- `POST /guides/search/gemini` - セマンティック検索
- `GET /guides/{title}/analyze` - ガイド分析
- `POST /guides/analyze-url` - 外部URL分析
- `POST /guides/compare` - 複数ガイド比較

### Context Engineering エンドポイント

#### セッション管理
- `POST /api/sessions` - 新規セッション作成
- `GET /api/sessions` - セッション一覧
- `GET /api/sessions/{session_id}` - セッション詳細

#### コンテキストウィンドウ
- `POST /api/sessions/{session_id}/windows` - コンテキストウィンドウ作成
- `POST /api/contexts/{window_id}/elements` - コンテキスト要素追加
- `GET /api/contexts/{window_id}` - コンテキストウィンドウ取得
- `POST /api/contexts/{window_id}/analyze` - コンテキスト分析

#### 最適化
- `POST /api/contexts/{window_id}/optimize` - コンテキスト最適化
- `POST /api/contexts/{window_id}/auto-optimize` - 自動最適化
- `GET /api/optimization/{task_id}` - 最適化ステータス

#### テンプレート管理
- `POST /api/templates` - テンプレート作成
- `POST /api/templates/generate` - AIでテンプレート生成
- `GET /api/templates` - テンプレート一覧
- `POST /api/templates/{template_id}/render` - テンプレートレンダリング

## 🧰 MCP ツール (15種類)

### AI Guides ツール (4種)
1. **list_ai_guides** - 全AIガイドの一覧
2. **search_ai_guides** - キーワードでガイド検索
3. **search_guides_with_gemini** - Geminiによるセマンティック検索
4. **analyze_guide** - 特定ガイドの分析

### Context Engineering ツール (7種)
5. **create_context_session** - 新規コンテキストセッション作成
6. **create_context_window** - コンテキストウィンドウ作成
7. **add_context_element** - コンテキストに要素追加
8. **analyze_context** - コンテキスト品質分析
9. **optimize_context** - コンテキストウィンドウ最適化
10. **auto_optimize_context** - 自動最適化
11. **get_context_stats** - システム統計取得

### テンプレート管理ツール (4種)
12. **create_prompt_template** - 新規テンプレート作成
13. **generate_prompt_template** - AIテンプレート生成
14. **list_prompt_templates** - 利用可能テンプレート一覧
15. **render_template** - 変数でテンプレートレンダリング

## 🎯 使用例

### 基本的なAIガイド検索
```bash
curl "http://localhost:8888/guides/search?query=エージェント"
```

### Geminiによるセマンティック検索
```bash
curl -X POST "http://localhost:8888/guides/search/gemini" \
  -H "Content-Type: application/json" \
  -d '{"query": "AIエージェントの構築方法", "use_grounding": true}'
```

### コンテキストセッション作成
```bash
curl -X POST "http://localhost:9001/api/sessions" \
  -H "Content-Type: application/json" \
  -d '{"name": "私のAIプロジェクト", "description": "チャットボット開発用コンテキスト"}'
```

### コンテキスト要素追加
```bash
curl -X POST "http://localhost:9001/api/contexts/{window_id}/elements" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "あなたは親切なAIアシスタントです...",
    "type": "system",
    "priority": 10
  }'
```

### コンテキスト最適化
```bash
curl -X POST "http://localhost:9001/api/contexts/{window_id}/optimize" \
  -H "Content-Type: application/json" \
  -d '{
    "goals": ["reduce_tokens", "improve_clarity"],
    "constraints": {"min_tokens": 100}
  }'
```

## 📊 システムアーキテクチャ

### コアコンポーネント
- **main.py**: AIガイド用FastAPIメインアプリケーション
- **gemini_service.py**: Gemini AI統合サービス
- **context_engineering/**: 完全なコンテキストエンジニアリングシステム
  - **context_models.py**: コンテキスト管理用データモデル
  - **context_analyzer.py**: AI駆動コンテキスト分析
  - **context_optimizer.py**: コンテキスト最適化エンジン
  - **template_manager.py**: プロンプトテンプレート管理
  - **context_api.py**: コンテキストエンジニアリング用FastAPIサーバー
- **mcp-server/**: MCPサーバー実装
  - **index.js**: 基本AIガイドMCPサーバー
  - **context_mcp_server.js**: 完全なコンテキストエンジニアリングMCPサーバー

### 事前定義テンプレート (5種類)
1. **基本的な質問応答** - シンプルな質問回答形式
2. **専門家ロールプレイ** - 専門的な応答
3. **段階的思考プロセス** - 思考の連鎖推論
4. **Few-Shot学習** - 例ベースの学習
5. **コード生成** - プログラミングタスクテンプレート

## 🔧 Dockerデプロイメント

### Dockerイメージのビルド
```bash
docker build -t context-engineering-platform .
```

### Docker Composeで実行
```bash
docker-compose up -d
```

## 🚀 パフォーマンス最適化

- Gemini APIレート制限の考慮
- トークン使用量の最適化
- WebSocket接続管理
- 頻繁にアクセスされるデータのキャッシング

## 🤝 貢献

このプロジェクトはオープンソースです。Issue報告やPull Requestを歓迎します。

### 開発環境のセットアップ
```bash
# 開発用依存関係のインストール
pip install -r requirements.txt
pip install pytest pytest-asyncio httpx

# テストの実行
pytest

# 開発サーバーの起動
uvicorn main:app --reload  # AI Guides
cd context_engineering && python context_api.py  # Context Engineering
```

## 📄 ライセンス

MIT License - 詳細はLICENSEファイルを参照してください。

## 🆘 サポート

問題が発生した場合：
1. [Issues](https://github.com/ShunsukeHayashi/context_-engineering_MCP/issues)でバグ報告
2. [Discussions](https://github.com/ShunsukeHayashi/context_-engineering_MCP/discussions)で質問
3. 📧 開発者への直接連絡

---

**🤖 このプロジェクトはClaude Codeによって強化されました**

AIガイド管理から高度なコンテキスト最適化、プロンプトエンジニアリング、リアルタイムワークフロー可視化まで、すべてを処理する完全なContext Engineeringプラットフォームです。
# 🤖 AI ワークフロー管理システム

インプットからワークフロー生成、タスク分解、エージェントアサインを行い、リアルタイムで状態を可視化するシステムです。

## 🌟 主な機能

### 1. AI によるワークフロー自動生成
- **Gemini AI** を使用してユーザーの要求からワークフローを自動生成
- 適切なタスク分解と依存関係の設定
- 必要なエージェントの自動配置

### 2. インテリジェントなタスク分解
- 大きなタスクを実行可能な小さなサブタスクに自動分解
- 依存関係を考慮した最適な分解
- 各タスクの推定時間と優先度の自動設定

### 3. エージェント管理とアサイン
- エージェントの能力とタスク要件のマッチング
- 負荷分散を考慮した最適なアサイン
- リアルタイムでのタスク再アサイン

### 4. リアルタイム状態可視化
- **美しいダッシュボード** でワークフローの進捗を可視化
- タスク依存関係のネットワーク図
- エージェントの負荷状況をリアルタイム表示
- WebSocket による即座の状態更新

## 🚀 セットアップ

### 1. 依存関係のインストール
```bash
cd workflow_system
pip install -r requirements.txt
```

### 2. 環境変数の設定
```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
```

### 3. システム起動
```bash
./start_workflow_system.sh
```

## 📊 アクセス方法

### ダッシュボード
- **URL**: http://localhost:9000
- リアルタイムでワークフローの状態を可視化
- 新しいワークフローの作成
- タスクとエージェントの管理

### API エンドポイント

#### ワークフロー管理
```bash
# 新しいワークフロー作成
POST /api/workflows
{
  "user_input": "ECサイトの商品管理システムを開発してください",
  "context": {"budget": 100000, "deadline": "2024-03-01"}
}

# ワークフロー一覧取得
GET /api/workflows

# 特定のワークフロー取得
GET /api/workflows/{workflow_id}

# ワークフロー実行開始
POST /api/workflows/{workflow_id}/start
```

#### タスク管理
```bash
# タスク状態更新
POST /api/tasks/{task_id}/update
{
  "status": "completed",
  "result": {"output": "タスクの結果"},
  "errors": []
}

# タスク分解
POST /api/tasks/{task_id}/decompose
```

#### 統計情報
```bash
# ダッシュボード統計
GET /api/dashboard/stats
```

## 🏗️ システム構成

### コアコンポーネント

1. **workflow_models.py** - データモデル定義
   - Workflow, Task, Agent クラス
   - 状態管理とプロパティ

2. **workflow_generator.py** - AI による生成エンジン
   - Gemini API を使用したワークフロー生成
   - タスク自動分解機能

3. **agent_manager.py** - エージェント管理
   - 最適なエージェント選択
   - タスクアサインとパフォーマンス追跡

4. **workflow_api.py** - API サーバー
   - RESTful API の提供
   - WebSocket による リアルタイム通信
   - バックグラウンド処理

5. **dashboard.html** - 可視化ダッシュボード
   - Chart.js による美しいグラフ
   - D3.js によるネットワーク可視化
   - リアルタイム状態更新

## 🎯 使用例

### 1. 基本的なワークフロー作成
```bash
curl -X POST "http://localhost:9000/api/workflows" \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "オンラインショップのユーザー認証システムを実装してください"
  }'
```

### 2. ダッシュボードでのワークフロー管理
1. ブラウザで http://localhost:9000 を開く
2. 「新しいワークフロー作成」に要求を入力
3. 「ワークフロー生成」ボタンをクリック
4. 生成されたワークフローをリアルタイムで監視

### 3. WebSocket でのリアルタイム更新
```javascript
const ws = new WebSocket('ws://localhost:9000/ws');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('リアルタイム更新:', data);
    
    switch(data.type) {
        case 'workflow_created':
            console.log('新しいワークフローが作成されました');
            break;
        case 'task_updated':
            console.log('タスクが更新されました');
            break;
        case 'progress_update':
            console.log('進捗が更新されました');
            break;
    }
};
```

## 🔧 カスタマイズ

### エージェントタイプの追加
```python
class AgentType(Enum):
    RESEARCHER = "researcher"
    ANALYST = "analyst"
    DEVELOPER = "developer"
    REVIEWER = "reviewer"
    COORDINATOR = "coordinator"
    SPECIALIST = "specialist"
    # 新しいタイプを追加
    YOUR_CUSTOM_TYPE = "your_custom_type"
```

### 可視化のカスタマイズ
- `dashboard.html` の CSS や JavaScript をカスタマイズ
- Chart.js の設定を変更してグラフをカスタマイズ
- D3.js のネットワーク可視化を拡張

## 🐛 トラブルシューティング

### よくある問題

1. **GEMINI_API_KEY エラー**
   ```bash
   export GEMINI_API_KEY="valid_api_key"
   ```

2. **ポート競合**
   - workflow_api.py の `port=9000` を変更

3. **依存関係エラー**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

## 📈 パフォーマンス最適化

- エージェント数の調整
- タスク分解の粒度調整
- WebSocket 接続数の制限
- データベース導入（現在はメモリ上）

## 🤝 貢献

このシステムはオープンソースです。改善提案やバグ報告をお待ちしています。

## 📄 ライセンス

MIT License - 詳細は LICENSE ファイルをご覧ください。
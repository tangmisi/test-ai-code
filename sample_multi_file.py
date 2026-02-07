import os
import subprocess
import time

# 必要ライブラリのインポート
from langchain_ollama import ChatOllama
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# --- 1. モデルの設定 ---
# Mac miniのスペックに合わせ、qwen2.5-coder:7b または 14b を推奨
MODEL_NAME = "llama3.1:8b" 
llm = ChatOllama(model=MODEL_NAME, temperature=0)

# --- 2. ツールの定義 ---

@tool
def read_file(path: str):
    """指定されたパスのファイルを読み込みます。"""
    if not os.path.exists(path):
        return f"エラー: {path} が見つかりません。"
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"読み込み失敗: {str(e)}"

@tool
def write_file(path: str, content: str):
    """指定されたパスにファイルを書き込みます。ディレクトリがない場合は自動作成します。"""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"{path} を正常に書き込み・更新しました。"
    except Exception as e:
        return f"書き込み失敗: {str(e)}"

@tool
def list_project_files(directory: str = "lib"):
    """プロジェクトのファイル構造を一覧表示し、現状を把握します。"""
    file_list = []
    for root, _, filenames in os.walk(directory):
        for f in filenames:
            file_list.append(os.path.join(root, f))
    return "\n".join(file_list) if file_list else "ファイルが見つかりません。"

@tool
def run_flutter_analyze():
    """flutter analyzeを実行し、現在のコードにエラーがないか確認します。"""
    result = subprocess.run("flutter analyze", capture_output=True, text=True, shell=True)
    if result.returncode == 0:
        return "静的解析エラーはありません。完璧です。"
    else:
        return f"エラーが検出されました。修正が必要です:\n{result.stdout}\n{result.stderr}"

# --- 3. エージェントの構築 ---

# tools = [read_file, write_file, list_project_files, run_flutter_analyze]
tools = [read_file, write_file, list_project_files]

# 最新の LangChain 仕様に準拠したプロンプト
prompt = ChatPromptTemplate.from_messages([
    ("system", """あなたは非常に優秀なFlutterエンジニアです。
ユーザーの要望に対し、以下のステップで行動してください。
1. `list_project_files` でプロジェクトの全体像を把握する。
2. 必要なファイルを `read_file` で読み込む。
3. 修正案を考え、`write_file` で複数のファイルを作成・更新する。

回答は簡潔に行い、可能な限りツールを活用して実装を完了させてください。"""),
    ("user", "{input}"),
    # エラーの原因だった scratchpad を正しく配置
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# エージェントと実行エンジンの作成
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True, 
    handle_parsing_errors=True
)

# --- 4. 実行フローの定義 ---

def main():
    print("🚀 Flutter AI Agent 起動中...")
    instruction = input("AIへの指示（例：計算履歴画面を追加して）: ")
    
    # 開発用ブランチの作成
    branch_name = f"ai-dev-{int(time.time())}"
    subprocess.run(f"git checkout -b {branch_name}", shell=True)

    print(f"🔧 タスク開始: {instruction}")
    
    try:
        # AIに実行を依頼
        result = agent_executor.invoke({"input": instruction})
        print("\n✅ AIの作業が完了しました。")
        print(result["output"])
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        return

    # 人間による動作確認
    print("\n--- プレビュービルドを開始します (macOS) ---")
    # proc = subprocess.Popen(["flutter", "run", "-d", "macos"]) 
    
    is_ok = input("\nアプリの動作は期待通りですか？ (y: コミットしてPR作成 / n: 破棄): ").lower()
    # proc.terminate()

    if is_ok == 'y':
        print("📦 Git操作とPR作成を実行します...")
        subprocess.run("git add .", shell=True)
        subprocess.run(f"git commit -m 'feat: {instruction[:50]}'", shell=True)
        subprocess.run(f"git push origin {branch_name}", shell=True)
        
        # GitHub CLI でPR作成
        subprocess.run(f"gh pr create --title 'AI Implementation: {instruction[:50]}' --body '{instruction}'", shell=True)
        print("🎉 プルリクエストを作成しました！")
    else:
        print("🚫 変更を確定せずに終了します。")

if __name__ == "__main__":
    main()

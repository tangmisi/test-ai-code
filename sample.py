import os
import subprocess
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

# --- 設定 ---
# MODEL_NAME = "qwen2.5-coder:7b" # Mac miniのスペックに応じ 14b 等に変更可
MODEL_NAME = "llama3.1:8b" # Mac miniのスペックに応じ 14b 等に変更可
TARGET_FILE = "lib/main.dart"     # 修正したいファイルパス
ISSUE_DESCRIPTION = input()

llm = ChatOllama(model=MODEL_NAME, temperature=0)

def run_command(command):
    """シェルコマンドを実行し、結果を返す"""
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    return result.stdout

def main():
    # 1. 現在のファイル内容を読み込む
    if not os.path.exists(TARGET_FILE):
        print(f"ファイルが見つかりません: {TARGET_FILE}")
        return

    with open(TARGET_FILE, "r") as f:
        current_code = f.read()

    print(f"--- 修正開始: {TARGET_FILE} ---")

    # 2. AIに修正を依頼するプロンプト
    prompt = ChatPromptTemplate.from_messages([
        ("system", "あなたはFlutterの専門家です。提供されたコードを指定された指示に従って修正し、修正後のコード全体のみを出力してください。解説は不要です。Markdownのコードブロックも不要です。"),
        ("user", "指示: {instruction}\n\n現在のコード:\n{code}")
    ])

    chain = prompt | llm
    new_code = chain.invoke({
        "instruction": ISSUE_DESCRIPTION,
        "code": current_code
    }).content.strip()

    # 3. ファイルを上書き保存
    with open(TARGET_FILE, "w") as f:
        f.write(new_code)
    print("ファイルを更新しました。")

    # 4. Git操作
    print("Gitコミットを実行中...")
    run_command(f"git add {TARGET_FILE}")
    commit_msg = f"AI fix: {ISSUE_DESCRIPTION[:30]}..."
    run_command(f"git commit -m '{commit_msg}'")
    run_command(f"git push")
    
    print(f"完了! コミットメッセージ: {commit_msg}")

if __name__ == "__main__":
    main()

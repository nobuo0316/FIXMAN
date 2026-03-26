import streamlit as st
import re

def fix_fstring_raw_text(code):
    # f-string (f'...' または f"...") の中身を探す正規表現
    # 1. f'...' のパターン
    # 2. f"..." のパターン
    # それぞれの内部にある「本物の改行」を "\\n" に置換する
    
    def replace_newline(match):
        full_match = match.group(0)
        # 文字列の中身だけ取り出して改行を置換
        return full_match.replace('\n', '\\n')

    # 非強欲マッチングで f'...' と f"..." を抽出
    # ※トリプルクォートは対象外にする（それ自体は文法的にOKなため）
    pattern_single = r"f'[^']*'"
    pattern_double = r'f"[^"]*"'
    
    # 改行を含む可能性があるので re.DOTALL を使用
    fixed_code = re.sub(r"f'[^']+'", replace_newline, code, flags=re.DOTALL)
    fixed_code = re.sub(r'f"[^"]+"', replace_newline, fixed_code, flags=re.DOTALL)
    
    return fixed_code

# --- Streamlit UI ---
st.set_page_config(page_title="f-string Emergency Fixer", layout="wide")
st.title("🛠 f-string 構文エラー修正ツール")
st.warning("`unterminated f-string` エラーが出るコードを強制的に1行に直します。")

uploaded_file = st.file_uploader("Pythonファイルをアップロード", type=["py"])

if uploaded_file:
    content = uploaded_file.read().decode("utf-8")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("修正前 (Error Line: 1340付近)")
        st.code(content, language="python")

    # 正規表現による強制置換
    fixed_code = fix_fstring_raw_text(content)
    
    with col2:
        st.subheader("修正後")
        st.code(fixed_code, language="python")
        st.download_button(
            label="修正済みファイルを保存",
            data=fixed_code,
            file_name=f"fixed_{uploaded_file.name}",
            mime="text/x-python"
        )

import streamlit as st
import ast

def fix_fstring_newlines(code):
    try:
        # コードを抽象構文木(AST)に変換
        tree = ast.parse(code)
        
        for node in ast.walk(tree):
            # f-string (JoinedStr) を探す
            if isinstance(node, ast.JoinedStr):
                for value in node.values:
                    # f-string内の固定テキスト部分 (Constant)
                    if isinstance(value, ast.Constant) and isinstance(value.value, str):
                        # 実際の改行文字をエスケープ文字 "\\n" に置換
                        # これにより、物理的な改行がコード上の一行に収まる
                        value.value = value.value.replace('\n', '\\n')
        
        # Python 3.9以降の標準機能でソースコードに戻す
        return ast.unparse(tree)
    except SyntaxError as e:
        return f"構文エラー: {e.msg} (line {e.lineno})"
    except Exception as e:
        return f"予期せぬエラーが発生しました: {e}"

# --- Streamlit UI ---
st.set_page_config(page_title="f-string Newline Fixer", layout="wide")

st.title("🐍 f-string 改行修正ツール")
st.info("f-string内にある物理的な改行を、自動で `\\n` 文字に書き換えます。")

uploaded_file = st.file_uploader("Pythonファイルをアップロード (.py)", type=["py"])

if uploaded_file:
    # ファイル読み込み
    content = uploaded_file.read().decode("utf-8")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("修正前")
        st.code(content, language="python")

    # 変換処理
    fixed_code = fix_fstring_newlines(content)
    
    with col2:
        st.subheader("修正後")
        if fixed_code.startswith("構文エラー") or fixed_code.startswith("予期せぬエラー"):
            st.error(fixed_code)
        else:
            st.code(fixed_code, language="python")
            st.download_button(
                label="修正済みファイルをダウンロード",
                data=fixed_code,
                file_name=f"fixed_{uploaded_file.name}",
                mime="text/x-python"
            )

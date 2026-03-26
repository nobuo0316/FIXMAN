import streamlit as st
import ast
import astor  # または ast.unparse (Python 3.9+)

def fix_fstring_newlines(code):
    tree = ast.parse(code)

    for node in ast.walk(tree):
        # f-string (JoinedStr) を探す
        if isinstance(node, ast.JoinedStr):
            for value in node.values:
                # f-string内の固定テキスト部分 (Constant)
                if isinstance(value, ast.Constant) and isinstance(value.value, str):
                    # 実際の改行を \n 文字列に置換
                    value.value = value.value.replace('\n', '\\n')
    
    return astor.to_source(tree)

# --- Streamlit UI ---
st.set_page_config(page_title="f-string Fixer", page_icon="🐍")
st.title("🐍 f-string 改行修正ツール")
st.write("アップロードされた .py ファイル内の f-string にある物理改行を `\\n` に変換します。")

uploaded_file = st.file_uploader("Pythonファイルをアップロード", type=["py"])

if uploaded_file is not None:
    raw_code = uploaded_file.read().decode("utf-8")
    
    st.subheader("修正前")
    st.code(raw_code, language="python")

    try:
        fixed_code = fix_fstring_newlines(raw_code)
        
        st.subheader("修正後")
        st.code(fixed_code, language="python")

        st.download_button(
            label="修正済みファイルをダウンロード",
            data=fixed_code,
            file_name=f"fixed_{uploaded_file.name}",
            mime="text/x-python"
        )
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

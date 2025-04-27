import streamlit as st

# Import các hàm từ ứng dụng con
from DeleteImg import run_DeleteBackground_app
from Language import run_Language_Check_app

# Cấu hình trang chính
st.set_page_config(page_title="Multi-App", layout="wide")

# Sidebar chứa menu ứng dụng
st.sidebar.title("Home page")
app_choice = st.sidebar.selectbox(
    "Chọn ứng dụng:",
    ["Delete Background Image", "Language Check"]
)

# Điều hướng đến ứng dụng được chọn
if app_choice == "Delete Background Image":
    run_DeleteBackground_app()
elif app_choice == "Language Check":
    run_Language_Check_app()

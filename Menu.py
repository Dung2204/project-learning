import streamlit as st

from Deleteimg import run_DeleteBackground_app

# Cấu hình trang chính - phải được gọi ngay đầu file
st.set_page_config(page_title="Multi-App", layout="wide")

# Sidebar chứa menu ứng dụng
st.sidebar.title("Home page")
app_choice = st.sidebar.selectbox(
    "Chọn ứng dụng:",
    ["Delete Background Image"]
)


# Điều hướng đến ứng dụng được chọn     
if app_choice == "Delete Background Image":
    run_DeleteBackground_app()

import streamlit as st

# Import các hàm từ ứng dụng con
from DeleteImg import run_DeleteBackground_app


# Cấu hình trang chính - phải được gọi ngay đầu file
st.set_page_config(page_title="Multi-App", layout="wide")

# Sidebar chứa menu ứng dụng
st.sidebar.title("Home page")
app_choice = st.sidebar.selectbox(
    "Chọn ứng dụng:",
    ["DeleteBackgroundImg"]
)

# Nội dung chính của trang
st.title("Chương Trình Ứng Dụng")

# Điều hướng đến ứng dụng được chọn
if app_choice == "Delete Background Image":
    run_DeleteBackground_app()

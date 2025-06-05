import streamlit as st
import streamlit.components.v1 as components
import random
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
st.set_page_config(page_title="🎲 Lucky Number", layout="centered")
st.title("🎲 Lucky Number Generator")

# Google Apps Script Web App URL
def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1ixe0S7_f0XKi7b6y8A6FhcI9GWwzqIZnxM_hUxDImd4").sheet1
    return sheet
sheet = connect_to_sheet()

if "user_ip" not in st.session_state:
    st.session_state.user_ip = ""

# مكون مخصص يستخدم JavaScript للحصول على عنوان الـ IP
components.html(
    """
    <script>
        fetch("https://api.ipify.org?format=json")
            .then(response => response.json())
            .then(data => {
                const ip = data.ip;
                const queryParams = new URLSearchParams(window.location.search);
                queryParams.set("ip", ip);
                const newUrl = window.location.pathname + "?" + queryParams.toString();
                window.history.replaceState({}, "", newUrl);
                window.parent.postMessage({isStreamlitMessage: true}, "*");
            })
            .catch(() => {});
    </script>
    """,
    height=0
)

# قراءة IP من عنوان الصفحة
ip = st.query_params.get("ip", "")
if ip and not st.session_state.user_ip:
    st.session_state.user_ip = ip

# واجهة توليد الرقم
if st.button("🔮 اعرف رقمك المحظوظ"):
    number = random.randint(1, 100)
    st.success(f"🎉 رقمك المحظوظ هو: {number}")

    # إرسال IP إلى Google Script
    if st.session_state.user_ip and google_webhook_url:
        try:
            sheet.append_row([ip])
        except Exception as e:
            st.error("جرب مرة اخري ")

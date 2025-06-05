import streamlit as st
import streamlit.components.v1 as components
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="🎲 Lucky Number", layout="centered")
st.title("🎲 Lucky Number Generator")

@st.cache_resource
def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google"], scope)
    client = gspread.authorize(creds)
    sheet_id = "1ixe0S7_f0XKi7b6y8A6FhcI9GWwzqIZnxM_hUxDImd4"
    sheet = client.open_by_key(sheet_id).sheet1
    return sheet

sheet = connect_to_sheet()

# --- الخطوة 1: إخفاء الإدخال وتخزين الـ IP في session_state ---
hide_input_style = """
    <style>
    div[data-testid="stTextInput"] {
        display: none;
    }
    </style>
"""
st.markdown(hide_input_style, unsafe_allow_html=True)

# إعداد قيمة في session_state
if "user_ip" not in st.session_state:
    st.session_state.user_ip = ""

# إدخال مخفي نربطه بـ session_state
st.text_input("IP", key="user_ip")

# JavaScript يقوم بتحديث session_state عبر text_input
components.html(
    """
    <script>
        async function getIP() {
            try {
                const res = await fetch('https://api.ipify.org?format=json');
                const data = await res.json();
                const input = window.parent.document.querySelector('input[data-testid="stTextInput"]');
                if (input && data.ip) {
                    input.value = data.ip;
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                }
            } catch (e) {
                console.log("IP fetch failed.");
            }
        }
        getIP();
    </script>
    """,
    height=0,
)

# --- الخطوة 2: ننتظر حتى يتم ملء الـ IP ثم نظهر الزر ---
if st.session_state.user_ip:
    if st.button("🔮 اعرف رقمك المحظوظ"):
        number = random.randint(1, 100)
        ip = st.session_state.user_ip
        st.success(f"🎉 رقمك المحظوظ هو: {number}")
        st.success(f"تم الحصول على IP: {ip}")
        try:
            sheet.append_row([ip, number])
            st.info("✅ تم تسجيل بياناتك بنجاح!")
        except Exception as e:
            st.error("❌ حدث خطأ أثناء إرسال البيانات.")
else:
    st.warning("⏳ جاري الحصول على عنوان IP... يرجى الانتظار لحظة.")

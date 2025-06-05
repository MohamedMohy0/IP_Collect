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

# 1. عنصر لإدخال الـ IP عبر JavaScript
ip_input = st.empty()

components.html(
    """
    <script>
        async function getIP() {
            try {
                const res = await fetch('https://api.ipify.org?format=json');
                const data = await res.json();
                const streamlitInput = window.parent.document.querySelector('input[data-testid="stTextInput"]');
                if (streamlitInput) {
                    streamlitInput.value = data.ip;
                    streamlitInput.dispatchEvent(new Event('input', { bubbles: true }));
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

user_ip = ip_input.text_input("IP Address", value="", label_visibility="collapsed")

# 2. توليد الرقم المحظوظ وتخزينه في Google Sheet
if st.button("🔮 اعرف رقمك المحظوظ"):
    if user_ip:
        number = random.randint(1, 100)
        st.success(f"🎉 رقمك المحظوظ هو: {number}")
        st.success(f"تم الحصول على IP: {user_ip}")
        try:
            sheet.append_row([user_ip, number])
            st.info("✅ تم تسجيل بياناتك بنجاح!")
        except Exception as e:
            st.error("❌ حدث خطأ أثناء إرسال البيانات.")
    else:
        st.warning("⛔ لم يتم الحصول على عنوان IP بعد. حاول مرة أخرى بعد ثوانٍ.")

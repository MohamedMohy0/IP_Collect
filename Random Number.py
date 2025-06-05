import streamlit as st
import streamlit.components.v1 as components
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

# Initialize Streamlit
st.set_page_config(page_title="🎲 Lucky Number", layout="centered")
st.title("🎲 Lucky Number Generator")

# ---- JavaScript to Fetch Real User IP ----
def get_real_ip():
    js_code = """
    <script>
        async function fetchIP() {
            try {
                const response = await fetch('https://api.ipify.org?format=json');
                const data = await response.json();
                window.parent.postMessage({ type: 'IP_RESULT', ip: data.ip }, '*');
            } catch (error) {
                window.parent.postMessage({ type: 'IP_ERROR', error: error.message }, '*');
            }
        }
        fetchIP();
    </script>
    """
    components.html(js_code, height=0)

    # Wait for JS to send IP (hacky but works)
    time.sleep(2)  # Allow time for JS to execute
    if 'user_ip' not in st.session_state:
        st.session_state.user_ip = "Unknown (Check Browser Permissions)"

# ---- Google Sheets Connection ----
@st.cache_resource
def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google"], scope)
    client = gspread.authorize(creds)
    sheet_id = "1ixe0S7_f0XKi7b6y8A6FhcI9GWwzqIZnxM_hUxDImd4"  # Replace with your Sheet ID
    return client.open_by_key(sheet_id).sheet1

# ---- Main App ----
get_real_ip()  # Fetch IP via JavaScript

# Display IP (if received)
if 'user_ip' in st.session_state:
    st.success(f"✅ تم التقاط عنوان IP: {st.session_state.user_ip}")

# Generate Lucky Number
if st.button("🔮 اعرف رقمك المحظوظ"):
    if 'number_generated' not in st.session_state:
        number = random.randint(1, 100)
        st.success(f"🎉 رقمك المحظوظ هو: {number}")

        try:
            sheet = connect_to_sheet()
            sheet.append_row([st.session_state.user_ip, number])
            st.info("✅ تم تسجيل بياناتك بنجاح!")
            st.session_state.number_generated = True
        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء إرسال البيانات: {e}")
    else:
        st.warning("⚠️ لقد حصلت بالفعل على رقمك المحظوظ!")

# ---- Listen for JavaScript IP Result ----
html_listener = """
<script>
    window.addEventListener('message', (event) => {
        if (event.data.type === 'IP_RESULT') {
            window.parent.document.querySelector('iframe').contentWindow.postMessage({
                'type': 'streamlit:setComponentValue',
                'value': event.data.ip
            }, '*');
        }
    });
</script>
"""
components.html(html_listener, height=0)

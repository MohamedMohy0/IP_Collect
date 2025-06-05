import streamlit as st
import streamlit.components.v1 as components
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests

# Initialize Streamlit
st.set_page_config(page_title="🎲 Lucky Number", layout="centered")
st.title("🎲 Lucky Number Generator")

# ---- Fetch IP Function ----
def get_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        response.raise_for_status()
        return response.json()['ip']
    except Exception as e:
        st.error(f"⚠️ Failed to fetch IP: {e}")
        return "Unknown"

# Get IP and display
ip = get_ip()
st.success(f"✅ تم التقاط عنوان IP: {ip}")

# ---- Google Sheets Connection ----
@st.cache_resource
def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google"], scope)
    client = gspread.authorize(creds)
    sheet_id = "1ixe0S7_f0XKi7b6y8A6FhcI9GWwzqIZnxM_hUxDImd4"  # Replace with your Sheet ID
    return client.open_by_key(sheet_id).sheet1

sheet = connect_to_sheet()

# ---- Lucky Number Generator ----
if st.button("🔮 اعرف رقمك المحظوظ"):
    if 'number_generated' not in st.session_state:  # Prevent multiple submissions
        number = random.randint(1, 100)
        st.success(f"🎉 رقمك المحظوظ هو: {number}")
        
        try:
            sheet.append_row([ip, number])
            st.info("✅ تم تسجيل بياناتك بنجاح!")
            st.session_state.number_generated = True  # Mark as submitted
        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء إرسال البيانات: {e}")
    else:
        st.warning("⚠️ لقد حصلت بالفعل على رقمك المحظوظ!")

import streamlit as st
import streamlit.components.v1 as components
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests



# Store the IP in a variable
my_ip = get_ip()
print("My IP:", my_ip)
# إعداد صفحة Streamlit
st.set_page_config(page_title="🎲 Lucky Number", layout="centered")
st.title("🎲 Lucky Number Generator")

# الاتصال بـ Google Sheets
@st.cache_resource
def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google"], scope)
    client = gspread.authorize(creds)
    sheet_id = "1ixe0S7_f0XKi7b6y8A6FhcI9GWwzqIZnxM_hUxDImd4"  # <-- غيّره حسب ملفك
    sheet = client.open_by_key(sheet_id).sheet1
    return sheet

sheet = connect_to_sheet()

try:
    response = requests.get('https://api.ipify.org?format=json')
    response.raise_for_status()  # Raise an error for bad status codes
    ip = response.json()['ip']
    return ip_address
except Exception as e:
    print(f"Failed to get IP: {e}")
    return None


# عرض الـ IP بعد التقاطه
st.success(f"✅ تم التقاط عنوان IP: {ip}")

# زر معرفة الرقم المحظوظ
if st.button("🔮 اعرف رقمك المحظوظ"):
    number = random.randint(1, 100)
    st.success(f"🎉 رقمك المحظوظ هو: {number}")
    try:
        sheet.append_row([ip, number])
        st.info("✅ تم تسجيل بياناتك بنجاح!")
    except Exception as e:
        st.error("❌ حدث خطأ أثناء إرسال البيانات. حاول مرة أخرى.")

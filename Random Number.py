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

# نحصل على IP من رابط الصفحة
query_params = st.query_params
user_ip = query_params.get("ip", [""])[0]

# إذا لم يوجد IP، نستخدم JavaScript لإعادة تحميل الصفحة مع IP
if not user_ip:
    components.html(
        """
        <script>
            async function getIP() {
                try {
                    const res = await fetch('https://api.ipify.org?format=json');
                    const data = await res.json();
                    if (data.ip) {
                        const newUrl = window.location.origin + window.location.pathname + "?ip=" + data.ip;
                        window.location.replace(newUrl);
                    }
                } catch (e) {
                    document.body.innerHTML = "<p>⚠️ فشل في الحصول على IP.</p>";
                }
            }
            getIP();
        </script>
        """,
        height=0,
    )
    st.warning("⏳ جاري الحصول على عنوان IP... يرجى الانتظار لحظة.")
    st.stop()

# زر معرفة الرقم المحظوظ
if st.button("🔮 اعرف رقمك المحظوظ"):
    number = random.randint(1, 100)
    st.success(f"🎉 رقمك المحظوظ هو: {number}")
    st.success(f"تم الحصول على IP: {user_ip}")
    try:
        sheet.append_row([user_ip, number])
        st.info("✅ تم تسجيل بياناتك بنجاح!")
    except Exception as e:
        st.error("❌ حدث خطأ أثناء إرسال البيانات.")

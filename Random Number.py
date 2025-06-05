import streamlit as st
import streamlit.components.v1 as components
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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

# نحصل على IP من الرابط
query_params = st.query_params
user_ip = query_params.get("ip", [""])[0]

# إذا لم يوجد IP، نطلبه من JavaScript
if not user_ip:
    components.html(
        """
        <div id="ipDisplay" style="font-size: 24px; color: white; font-weight: bold;">
            Getting your IP...
        </div>

        <script>
            async function getIP() {
                try {
                    const res = await fetch('https://api.ipify.org?format=json');
                    const data = await res.json();
                    const ip = data.ip;
                    document.getElementById("ipDisplay").innerText = "Your IP address is: " + ip;

                    const currentUrl = new URL(window.location.href);
                    if (!currentUrl.searchParams.get("ip")) {
                        currentUrl.searchParams.set("ip", ip);
                        window.location.replace(currentUrl.toString());
                    }

                } catch (e) {
                    document.getElementById("ipDisplay").innerText = "⚠️ Failed to get IP.";
                }
            }
            getIP();
        </script>
        """,
        height=100,
    )
    st.warning("⏳ جاري الحصول على عنوان IP... يرجى الانتظار لحظة.")
    st.stop()

# عرض الـ IP بعد التقاطه
st.success(f"✅ تم التقاط عنوان IP: {user_ip}")

# زر معرفة الرقم المحظوظ
if st.button("🔮 اعرف رقمك المحظوظ"):
    number = random.randint(1, 100)
    st.success(f"🎉 رقمك المحظوظ هو: {number}")
    try:
        sheet.append_row([user_ip, number])
        st.info("✅ تم تسجيل بياناتك بنجاح!")
    except Exception as e:
        st.error("❌ حدث خطأ أثناء إرسال البيانات. حاول مرة أخرى.")

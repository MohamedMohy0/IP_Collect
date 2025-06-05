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

ip_holder = st.empty()

# 2. نستخدم session_state لتخزين IP
if "user_ip" not in st.session_state:
    st.session_state.user_ip = None

# 3. HTML + JavaScript لجلب الـ IP
components.html(
    """
    <script>
        async function getIP() {
            try {
                const res = await fetch('https://api.ipify.org?format=json');
                const data = await res.json();

                // إرسال IP إلى Streamlit عبر postMessage
                window.parent.postMessage(
                    {
                        isStreamlitMessage: true,
                        type: 'streamlit:setComponentValue',
                        value: data.ip
                    },
                    '*'
                );
            } catch (e) {
                window.parent.postMessage(
                    {
                        isStreamlitMessage: true,
                        type: 'streamlit:setComponentValue',
                        value: "Failed to get IP"
                    },
                    '*'
                );
            }
        }
        getIP();
    </script>
    """,
    height=0
)

# 4. استقبال القيمة المُرسلة من JavaScript
ip = ip_holder.text_input("Your IP (Hidden field)", value="", label_visibility="collapsed")

if ip and not st.session_state.user_ip and "Failed" not in ip:
    st.session_state.user_ip = ip

# 5. عرض النتيجة
if st.session_state.user_ip:
    st.success(f"✅ تم الحصول على IP: {st.session_state.user_ip}")
else:
    st.info("👀 جاري الحصول على عنوان الـ IP ...")
# st.query_params.get ترجع list، نأخذ العنصر الأول إذا موجود


# if st.button("🔮 اعرف رقمك المحظوظ"):
#     number = random.randint(1, 100)
#     st.success(f"🎉 رقمك المحظوظ هو: {number}")
#     st.success(f"تم الحصول على IP: {ip}")
#     if st.session_state.user_ip:
#         try:
#             st.write(f"جاري إرسال البيانات: IP={st.session_state.user_ip}, رقم={number}")
#             sheet.append_row([st.session_state.user_ip, number])
#         except Exception as e:
#             st.error("جرب مرة أخري")

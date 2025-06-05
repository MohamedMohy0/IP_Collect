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

if "user_ip" not in st.session_state:
    st.session_state.user_ip = ""

ip = components.html(
    """
    <div id="ipDisplay" style="font-size: 24px; color: white; font-weight: bold;">
        Getting your IP...
    </div>
    <script>
        async function getIP() {
            try {
                const res = await fetch('https://api.ipify.org?format=json');
                const data = await res.json();
                document.getElementById("ipDisplay").innerText = "Your IP address is: " + data.ip;

                // هذا السطر يرسل IP إلى بايثون
                window.parent.postMessage({ isStreamlitMessage: true, type: 'streamlit:setComponentValue', value: data.ip }, "*");

            } catch (e) {
                document.getElementById("ipDisplay").innerText = "Failed to get IP.";
                window.parent.postMessage({ isStreamlitMessage: true, type: 'streamlit:setComponentValue', value: null }, "*");
            }
        }
        getIP();
    </script>
    """,
    height=100
)

# st.query_params.get ترجع list، نأخذ العنصر الأول إذا موجود
ip_list = st.query_params.get("ip", [])
ip = ip_list[0] if ip_list else ""

if ip and not st.session_state.user_ip:
    st.session_state.user_ip = ip

if st.button("🔮 اعرف رقمك المحظوظ"):
    number = random.randint(1, 100)
    st.success(f"🎉 رقمك المحظوظ هو: {number}")
    st.write(f"جاري إرسال البيانات: IP={ip}, رقم={number}")
    sheet.append_row([ip, number])
    st.write(f"جاري إرسال البيانات: IP={st.session_state.user_ip}, رقم={number}")
    sheet.append_row([st.session_state.user_ip, number])
    if st.session_state.user_ip:
        try:
            st.write(f"جاري إرسال البيانات: IP={st.session_state.user_ip}, رقم={number}")
            sheet.append_row([st.session_state.user_ip, number])
        except Exception as e:
            st.error("جرب مرة أخري")

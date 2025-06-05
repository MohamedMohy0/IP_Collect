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

# st.query_params.get ترجع list، نأخذ العنصر الأول إذا موجود
ip_list = st.query_params.get("ip", [])
ip = ip_list[0] if ip_list else ""

if ip and not st.session_state.user_ip:
    st.session_state.user_ip = ip

if st.button("🔮 اعرف رقمك المحظوظ"):
    number = random.randint(1, 100)
    st.success(f"🎉 رقمك المحظوظ هو: {number}")

    if st.session_state.user_ip:
        try:
            st.write(f"جاري إرسال البيانات: IP={st.session_state.user_ip}, رقم={number}")
            sheet.append_row([st.session_state.user_ip, number])
        except Exception as e:
            st.error("جرب مرة أخري")

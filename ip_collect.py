import streamlit as st
import streamlit.components.v1 as components

# Display the IP using a JS fetch from an external service
components.html(
    """
    <script>
        async function getIP() {
            const res = await fetch('https://api.ipify.org?format=json');
            const data = await res.json();
            const ip = data.ip;
            window.parent.postMessage({type: 'ip', ip: ip}, '*');
        }
        getIP();
    </script>
    """,
    height=0,
)

# Use Streamlit's built-in JavaScript event listener to receive the IP
ip_holder = st.empty()

st.markdown("### Waiting for your IP...")

# Custom Streamlit event receiver via st_javascript (works with custom components)
components.html(
    """
    <script>
        window.addEventListener("message", (event) => {
            if (event.data.type === "ip") {
                const ip = event.data.ip;
                const streamlitMsg = window.parent.document.querySelector('iframe').contentWindow;
                streamlitMsg.postMessage({isStreamlitMessage: true, type: "streamlit:setComponentValue", value: ip}, "*");
            }
        });
    </script>
    """,
    height=0,
)

# Use st.experimental_get_query_params as a workaround to check if IP was received
ip = st.experimental_get_query_params().get("ip", [None])[0]
if ip:
    st.success(f"Your IP address is: {ip}")
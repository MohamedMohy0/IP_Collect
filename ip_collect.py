import streamlit as st
import streamlit.components.v1 as components

st.markdown("### Getting your IP address...")

# Create a hidden component to receive IP
ip = components.html(
    """
    <script>
        const getIP = async () => {
            const res = await fetch('https://api.ipify.org?format=json');
            const data = await res.json();
            const ip = data.ip;

            // Send the IP back as the component value
            const streamlitMsg = window.parent;
            streamlitMsg.postMessage({
                isStreamlitMessage: true,
                type: "streamlit:setComponentValue",
                value: ip
            }, "*");
        };
        getIP();
    </script>
    """,
    height=0,
)

# Show result if received
if ip:
    st.success(f"Your IP address is: {ip}")
else:
    st.info("Still fetching your IP...")

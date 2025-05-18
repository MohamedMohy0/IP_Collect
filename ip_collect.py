import streamlit as st
import streamlit.components.v1 as components

# Check if IP is already stored
if "ip" not in st.session_state:
    st.session_state.ip = None

# If we don't have it yet, inject JS to get it
if not st.session_state.ip:
    st.markdown("### Getting your IP address...")

    # Display JS to get IP and send it back to Streamlit
    components.html(
        """
        <script>
            async function sendIPToStreamlit() {
                const res = await fetch('https://api.ipify.org?format=json');
                const data = await res.json();
                const ip = data.ip;

                // Send IP back to Streamlit
                const streamlitFrame = window.parent;
                streamlitFrame.postMessage({type: 'streamlit:setComponentValue', value: ip}, '*');
            }

            sendIPToStreamlit();
        </script>
        """,
        height=0,
    )

    # Placeholder to trigger rerun when IP is received
    ip_component = components.html(
        """
        <script>
            window.addEventListener("message", (event) => {
                const data = event.data;
                if (data.type === "streamlit:setComponentValue") {
                    const ip = data.value;
                    window.parent.postMessage(
                        { isStreamlitMessage: true, type: "streamlit:setComponentValue", value: ip },
                        "*"
                    );
                }
            });
        </script>
        """,
        height=0,
    )

else:
    st.success(f"Your IP address is: {st.session_state.ip}")

# Read query parameters using the new method
params = st.query_params
ip_input = params.get("ip", [None])[0]
ip_from_js = params.get("ip_from_js", [None])[0]

# Use query param fallback if needed
if ip_input and not st.session_state.ip:
    st.session_state.ip = ip_input
elif ip_from_js and not st.session_state.ip:
    st.session_state.ip = ip_from_js

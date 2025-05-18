import streamlit as st
import streamlit.components.v1 as components

# If IP is already in query params, show it
ip = st.query_params.get("ip", [None])[0]

if ip:
    st.success(f"Your IP address is: {ip}")
else:
    st.markdown("### Getting your IP...")

    # Inject JavaScript to get the IP and redirect the page with it in the URL
    components.html(
        """
        <script>
            async function getIPAndRedirect() {
                const res = await fetch('https://api.ipify.org?format=json');
                const data = await res.json();
                const ip = data.ip;

                // Redirect with IP in query params
                const url = new URL(window.location);
                url.searchParams.set('ip', ip);
                window.location.href = url.toString();
            }
            getIPAndRedirect();
        </script>
        """,
        height=0,
    )

import requests
import streamlit as st

st.title("Minimal Application")

username = st.text_input("Username")

if st.button("Submit"):
    response = requests.get(f"http://localhost:5000/player/hello/{username}")

    if response.status_code == 200:
        st.write(f"Hello {username}")
    else:
        st.write("We don't know each other.")

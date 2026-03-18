import streamlit as st
import os

def load_css():
    base_dir = os.path.dirname(os.path.dirname(__file__))  # go to root
    css_path = os.path.join(base_dir, "assets", "styles.css")

    print("CSS PATH:", css_path)  # 🔍 DEBUG

    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.error(f"CSS NOT FOUND ❌ → {css_path}")
import streamlit as st
from generate_story import generate_story
import os
from PIL import Image

st.title("📚 Mii’s Personalized Storybook")

uploaded_file = st.file_uploader("Upload a front-facing photo", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Photo", use_container_width=True)

    with open("uploads/child.png", "wb") as f:
        f.write(uploaded_file.getbuffer())

    if st.button("📘 Generate Story Preview"):
        try:
            st.info("Generating all story pages...")
            pages = generate_story("uploads/child.png")
            for p in pages:
                st.image(p, use_container_width=True)
            st.success("✅ Done!")
        except Exception as e:
            st.error(f"Face swap failed: {e}")
else:
    st.warning("Please upload a photo to continue.")


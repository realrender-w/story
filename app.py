import streamlit as st
import os
from generate_story import generate_story

# Streamlit UI config
st.set_page_config(page_title="Storybook Generator", layout="centered")

st.title("📖 Personalized Storybook Generator")
st.markdown("Upload a photo and type a name — we'll create a magical 20-page adventure!")

# Input fields
child_name = st.text_input("👶 Enter your child's name:", max_chars=20)
uploaded_image = st.file_uploader("📷 Upload a clear photo of your child", type=["jpg", "jpeg", "png"])

# Directories
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "output"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Button trigger
if st.button("✨ Generate Story"):
    if not child_name:
        st.warning("Please enter the child's name.")
    elif not uploaded_image:
        st.warning("Please upload a child photo.")
    else:
        # Save uploaded photo
        upload_path = os.path.join(UPLOAD_DIR, "child.png")
        with open(upload_path, "wb") as f:
            f.write(uploaded_image.read())

        # Generate storybook
        with st.spinner("Generating your storybook..."):
            generate_story(child_name, upload_path)

        st.success(f"✅ Story generated for {child_name.title()}!")

        # Display cover if exists
        cover_path = f"{OUTPUT_DIR}/cover_{child_name.lower()}.png"
        if os.path.exists(cover_path):
            st.image(cover_path, caption="📘 Cover Page", use_container_width=True)
            with open(cover_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download Cover Page",
                    data=f,
                    file_name=f"{child_name}_cover.png",
                    mime="image/png"
                )

        # Display story pages
        st.markdown("### 📚 Download Your Story Pages")
        for i in range(1, 21):
            output_file = f"{OUTPUT_DIR}/page{i}_{child_name.lower()}.png"
            if os.path.exists(output_file):
                st.image(output_file, caption=f"Page {i}", use_container_width=True)
                with open(output_file, "rb") as f:
                    st.download_button(
                        label=f"⬇️ Download Page {i}",
                        data=f,
                        file_name=f"{child_name}_page{i}.png",
                        mime="image/png"
                    )
            else:
                st.info(f"⚠️ Page {i} was skipped or could not be generated.")

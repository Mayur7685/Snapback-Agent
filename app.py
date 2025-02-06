import streamlit as st
from PIL import Image
import moondream as md
import os

# Initialize Moondream model
api_key = os.getenv("MOONDREAM_API_KEY")
model = md.vl(api_key=api_key)

# Streamlit UI
st.title("SnapBack Complaint Analyzer 🚀")

uploaded_image = st.file_uploader("Upload complaint image", type=["jpg", "jpeg", "png"])
complaint_text = st.text_input("Describe your complaint (e.g. 'Expired milk from Blinkit')")

if uploaded_image and complaint_text:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Analyze Complaint"):
        # Prepare image+text prompt
        prompt = f"Analyze this complaint: {complaint_text}. Check for: \
        1. Product condition 2. Expiry date 3. Packaging damage. \
        Respond in JSON format with severity (high/medium/low) and verification status."

        # Encode the image
        encoded_image = model.encode_image(image)

        # Generate analysis with Moondream
        with st.spinner("Analyzing complaint..."):
            analysis = model.query(encoded_image, prompt)["answer"]
        
        # Display results
        st.subheader("AI Analysis:")
        st.write(analysis)

        # Generate suggested tweet
        st.subheader("Suggested Tweet:")
        tweet = f"@{complaint_text.split()[-1]}Care {complaint_text} - Verified by @SnapBackAI\n#QuickCommerce #ConsumerRights"
        st.code(tweet)

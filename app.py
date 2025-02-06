import streamlit as st
from PIL import Image
import moondream as md
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API key from environment variable
MOONDREAM_API_KEY = os.getenv("MOONDREAM_API_KEY")

if not MOONDREAM_API_KEY:
    st.error("API Key is missing. Please set it in the .env file.")
else:
    # Initialize Moondream model with API key
    model = md.vl(api_key=MOONDREAM_API_KEY)

# Streamlit UI
st.title("SnapBack Complaint Analyzer 🚀")

uploaded_image = st.file_uploader("Upload complaint image", type=["jpg", "jpeg", "png"])
complaint_text = st.text_input("Describe your complaint (e.g. 'Expired milk from Blinkit')")

if uploaded_image and complaint_text:
    image = Image.open(uploaded_image)

    if st.button("Analyze Complaint"):
        prompt = f"""
Analyze this food-related complaint: "{complaint_text}". Based on the uploaded image, perform the following checks:

1. **Product Condition**: Assess the physical state of the food item.
2. **Expiry Date**: Verify if the product is expired or close to expiration.
3. **Packaging Integrity**: Check for signs of tampering, leaks, or damage.
4. **Food Safety Concerns**: Identify potential health hazards.

Respond in JSON format:
{{
  "product_condition": "...",
  "expiry_status": "...",
  "packaging_integrity": "...",
  "food_safety_concerns": "...",
  "severity": "...",
  "verification_status": "..."
}}
"""

        encoded_image = model.encode_image(image)

        with st.spinner("Analyzing complaint..."):
            try:
                analysis = model.query(encoded_image, prompt)["answer"]
                analysis_json = json.loads(analysis)  # Convert response to JSON
                
                # Extract key insights
                product_condition = analysis_json.get("product_condition", "N/A")
                expiry_status = analysis_json.get("expiry_status", "N/A")
                packaging_integrity = analysis_json.get("packaging_integrity", "N/A")
                food_safety_concerns = analysis_json.get("food_safety_concerns", "N/A")
                severity = analysis_json.get("severity", "N/A")
                verification_status = analysis_json.get("verification_status", "N/A")

                # Twitter-style thread with callouts
                st.subheader("📢 Suggested Twitter Thread")

                st.markdown(f"**SnapBack AI**  🚀 (@SnapBackAI)  \n*1h ago*")
                st.info(f"**Complaint:** {complaint_text}")

                st.image(image, caption="Complaint Image", use_container_width=True)

                st.success(f"✅ **Product Condition:** {product_condition}")
                st.warning(f"⏳ **Expiry Status:** {expiry_status}")
                st.error(f"📦 **Packaging Integrity:** {packaging_integrity}")
                st.info(f"⚠️ **Food Safety Concerns:** {food_safety_concerns}")
                st.error(f"🔴 **Severity:** `{severity.upper()}`")
                st.warning(f"🟢 **Verification Status:** `{verification_status}`")

                st.markdown("---")
                st.markdown("🔁 **Retweets:** 245 | ❤️ **Likes:** 1.2K")


            except Exception as e:
                st.error(f"An error occurred: {e}")

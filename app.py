import os
import io
import streamlit as st
from PIL import Image
from PIL.ExifTags import TAGS
from google import genai
from google.genai import types
from dotenv import load_dotenv

# setup
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL_ID = "gemini-2.5-flash"

def get_photo_metadata(uploaded_file) -> dict:
    try:
        with Image.open(uploaded_file) as img:
            exif_data = img.getexif()
            if not exif_data:
                return {"info": "no exif data found"}
            
            readable = {TAGS.get(tag_id, tag_id): value for tag_id, value in exif_data.items()}
            
            # extract deeper exif tags
            exif_ifd = exif_data.get_ifd(0x8769)
            for tag_id, value in exif_ifd.items():
                tag_name = TAGS.get(tag_id, tag_id)
                readable[tag_name] = value
            
            if 'MakerNote' in readable:
                del readable['MakerNote']
                
            return readable
    except Exception as e:
        return {"error": str(e)}

# ui config
st.set_page_config(page_title="Photograph Quality Agent", layout="wide", initial_sidebar_state="expanded")

# high-contrast dark theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400&family=Lekton&display=swap');
    
    html, body, [class*="css"], p, li, span, label, input, button, textarea {
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 300 !important;
        color: #f8fafc !important;
    }

    .stApp {
        background-color: #020617;
    }

    .lekton-output, .stMarkdown p, .stMarkdown li {
        font-family: 'Lekton', monospace !important;
        font-size: 18px !important;
        line-height: 1.6 !important;
        color: #f8fafc !important;
    }

    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b;
    }
    
    [data-testid="sidebar-button"], 
    [data-testid="stSidebarCollapseButton"],
    .st-emotion-cache-6q9ru6,
    .st-emotion-cache-1ky9p6y {
        display: none !important;
    }

    .caption-text {
        color: #94a3b8 !important; 
        font-size: 14px;
        margin-bottom: 25px;
    }

    .stButton>button {
        float: right;
        border-radius: 2px;
        background-color: #334155 !important;
        color: #ffffff !important;
        border: 1px solid #475569;
        padding: 0.6rem 2.5rem;
        transition: 0.1s ease;
    }
    
    .stButton>button:hover {
        background-color: #475569 !important;
        border: 1px solid #94a3b8;
    }

    .metadata-value {
        font-size: 12px;
        color: #cbd5e1;
        margin-bottom: 4px;
        border-bottom: 1px solid #1e293b;
        padding-bottom: 2px;
        word-wrap: break-word;
    }

    .report-container:empty {
        display: none !important;
    }

    .report-container {
        padding: 30px;
        background-color: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 4px;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {display: none !important;}
    
    .stFileUploader section {
        background-color: #1e293b !important;
        border: 1px dashed #475569 !important;
    }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<p style='font-size: 14px; color: #94a3b8;'>INPUT_SOURCE</p>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Select Image", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

if uploaded_file:
    head_col, btn_col = st.columns([3, 1])
    with head_col:
        st.title("Photograph Quality Agent")
        st.markdown("<p class='caption-text'>A technical audit and professional critique</p>", unsafe_allow_html=True)
    with btn_col:
        st.write(" ") 
        st.write(" ")
        run_audit = st.button("Run Audit")

    st.markdown("<hr style='border: 0; border-top: 1px solid #1e293b; margin: 0 0 30px 0;'>", unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 2], gap="large")
    
    metadata = get_photo_metadata(uploaded_file)
    image = Image.open(uploaded_file)
    
    with col_left:
        st.image(image, use_container_width=True)
        st.markdown("<p style='color: #64748b; font-size: 11px; text-transform: uppercase; margin-top:20px;'>Hardware_EXIF_Data</p>", unsafe_allow_html=True)
        for key, value in metadata.items():
            # rendering everything except the deleted MakerNote
            st.markdown(f"<p class='metadata-value'>{key}: {value}</p>", unsafe_allow_html=True)

    with col_right:
        if run_audit:
            st.markdown("<div class='report-container lekton-output'>", unsafe_allow_html=True)
            with st.spinner("Processing image..."):
                img_byte_arr = io.BytesIO()
                image.convert("RGB").save(img_byte_arr, format='JPEG')
                image_bytes = img_byte_arr.getvalue()
                
                prompt = f"""
    You are a dual specialist AI: A Technical Photography Auditor and a Master Photography Mentor. 
    Below is the technical metadata for a photo, along with the image itself.
    
    METADATA:
    {metadata}
    
    HARDWARE HEALTH AUDIT (You are very concise, objective, and technical) (format this title as a H1)
    1. Compare the Aperture (F-stop) and ISO to the visual noise and blur.
    2. Check high-contrast edges for "Chromatic Aberration" (color fringing).
    3. Identify if any "Software Simulation" (like Portrait Mode) was used.
    4. Check if the Exposure Bias (e.g., -2.8) matches the lighting conditions.
    5. Scan the sky and flat color areas for "Sensor Dust" (dark circular spots). Note that dust is most visible at small apertures (f/8 - f/22).
    6. Provide a summary "Technical Health Report" with a grade (A-F). (a concise paragraph with no bullet points/no numbering)

    PHOTOGRAPHY MENTORING (You are thorough and critical, not overly encouraging) (format this title as a H1)
    1. Provide a detailed but concise critique focusing on important photographic elements: composition, lighting, focus, subject, color theory, and storytelling. (Write each element (and any other you feel is key that isn't already listed) as bullet points)
    2. IF APPLICABLE provide suggestions that could improve photo quality specific to the photo at hand
    3. Provide a summary "Mentoring Report" with a grade (A-F). (a concise paragraph with no bullet points/no numbering)

    Regarding the output, do NOT repeat your instructions (e.g., don't use the phrases "very concise", "detailed but concise critique", etc.) in the final response.
    """
                try:
                    response = client.models.generate_content(
                        model=MODEL_ID,
                        contents=[
                            types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                            prompt
                        ]
                    )
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Execution Error: {e}")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color: #475569;'>Ready for analysis.</p>", unsafe_allow_html=True)
else:
    st.title("Photograph Quality Agent")
    st.markdown("<p class='caption-text'>A technical audit and professional critique</p>", unsafe_allow_html=True)
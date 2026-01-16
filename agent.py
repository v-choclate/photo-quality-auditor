import os
import base64
from PIL import Image
from PIL.ExifTags import TAGS, IFD
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL_ID = "gemini-2.5-flash"

def get_photo_metadata(image_path: str) -> dict:
    # extracts technical EXIF metadata from a local image file.

    try:
        with Image.open(image_path) as img:
            exif_data = img.getexif()
            if not exif_data:
                return {"error": "No EXIF metadata found"}
            
            readable = {TAGS.get(tag_id, tag_id): value for tag_id, value in exif_data.items()}
            exif_ifd = exif_data.get_ifd(0x8769)

            for tag_id, value in exif_ifd.items():
                tag_name = TAGS.get(tag_id, tag_id)
                readable[tag_name] = value
            
            if 'MakerNote' in readable:
                del readable['MakerNote']

            return readable
    except Exception as e:
        return {"error": str(e)}

def run_audit(image_path: str):
    print(f"Starting audit for: {image_path}")
    
    # use the tool to get the data
    metadata = get_photo_metadata(image_path)
    
    # read the image as bytes for Gemini's vision
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    # system prompt
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

    # execute the audit
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                prompt
            ]
        )
        print("\n--- AUDIT REPORT ---")
        print(response.text)
    except Exception as e:
        print(f"❌ Audit failed: {e}")

# RUN TEST
if __name__ == "__main__":
    my_photo = "test_photo.jpg" 
    
    if os.path.exists(my_photo):
        run_audit(my_photo)
    else:
        print(f"⚠️  File not found: {my_photo}. Please add a .jpg to your folder.")
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Initialize the Client
# Note: In 2026, the 'v1' stable API is the default for these models
client = genai.Client(api_key=api_key)

# The most reliable model for free-tier users right now
MODEL_ID = "gemini-2.5-flash" 

print(f"🚀 Connecting to {MODEL_ID}...")

try:
    response = client.models.generate_content(
        model=MODEL_ID,
        contents="System check: Are you ready to audit metadata?"
    )
    print(f"\n✅ SUCCESS!")
    print(f"🤖 Agent: {response.text}")

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n💡 Let's see exactly what models your key can access...")
    
    # Improved scanner that avoids the 'Attribute' error
    try:
        models = client.models.list()
        print("Available models for your account:")
        for m in models:
            # We just print the name directly to avoid attribute errors
            print(f" - {m.name}")
    except Exception as list_err:
        print(f"Could not list models: {list_err}")
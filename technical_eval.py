import os
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from dotenv import load_dotenv

load_dotenv()

technician_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash"),
    name="hardware_technician",
    description="Specialist in hardware health. Accesses local images via file paths.",
    instruction="""You are a hardware technician. 
    You will be given a local file path to an image.
    1. Open and analyze the image from that path.
    2. Analyze metadata and pixels for sensor dust, CA, and sharpness.
    3. Report ONLY technical hardware facts."""
)

app = to_a2a(technician_agent, port=8001)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)
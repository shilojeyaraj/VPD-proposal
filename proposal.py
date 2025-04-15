from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with the secret key
OPENAI_SECRET_KEY = os.getenv("OPENAI_SECRET_KEY")  # Ensure this is set in your .env file
if not OPENAI_SECRET_KEY:
    raise ValueError("OPENAI_SECRET_KEY is not set. Please check your .env file.")

client = OpenAI(api_key=OPENAI_SECRET_KEY)

# Conversation history
conversation = [
    {"role": "system", "content": "You are a tech consultant generating proposals tailored to clients' needs."}
]

def add_message(role, content):
    conversation.append({"role": role, "content": content})

# Generate a response using GPT-4
def generate_response():
    response = client.responses.create(
        model="gpt-4",
        input=conversation
    )
    reply = response.output_text
    add_message("assistant", reply)
    return reply

# Add initial user message
user_input = "Client is a logistics firm seeking a cloud-native inventory management solution."
add_message("user", user_input)

# Generate and print the proposal
proposal = generate_response()
print("\n--- Initial Proposal ---\n")
print(proposal)



# Generate feedback message for improvement
feedback = str(["The proposal recieved the following scores: ",[1,0,0.5,0,0.25,1],{
    "Structure Adherence": "The submission perfectly adheres to the required structure. "
                           "Executive Summary/Overview, Client/Proposed Context & Market Opportunity, "
                           "Proposed Value Proposition Design Approach, Key Deliverables, Timeline, Price & Engagement Model.",
    "Clarity and Brand Tone": "The writing is exceptionally clear and perfectly embodies the brand tone.",
    "Market Fit Validation": "The proposal clearly addresses the NEED of the client, and why it is required.",
    "Timeline/Budget": "Team Structure and Pricing over the Timeline of the Project.",
    "Completeness": "All required elements are present and thoroughly addressed.",
    "Consistency/Stability": "The submission is completely consistent in language, style, and messaging."
}, "please revise the proposal based on this following criteria","note that the scores are graded from 0 to 1."
])

# Example of printing the feedback


add_message("user", feedback)

# Generate improved proposal
improved_proposal = generate_response()
print("\n--- Improved Proposal ---\n")
print(improved_proposal)

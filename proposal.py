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

# Define the success criteria and scoring logic
criteria = {
    "Structure Adherence": lambda proposal: 5 if "Executive Summary" in proposal and "Key Deliverables" in proposal else 3,
    "Clarity and Brand Tone": lambda proposal: 5 if len(proposal.split()) > 100 else 3,
    "Completeness": lambda proposal: 5 if all(
        section in proposal for section in [
            "Executive Summary", "Client/Proposed Context", "Market Opportunity",
            "Proposed Value Proposition Design Approach", "Key Deliverables", "Timeline", "Price & Engagement Model"
        ]
    ) else 2,
    "Consistency/Stability": lambda proposal: 5  # Assume consistent language for simplicity
}

def grade_proposal(proposal):
    """Grade the proposal based on the success criteria."""
    scores = {key: func(proposal) for key, func in criteria.items()}
    total_score = sum(scores.values()) / len(criteria)  # Average score
    return total_score, scores

# Add initial user message
user_input = "Client is a logistics firm seeking a cloud-native inventory management solution."
add_message("user", user_input)

# Generate and print the proposal
proposal = generate_response()
print("\n--- Initial Proposal ---\n")
print(proposal)

# Grade the proposal
total_score, scores = grade_proposal(proposal)
print("\n--- Proposal Grading ---\n")
print(f"Total Score: {total_score:.2f}/5.00")
for criterion, score in scores.items():
    print(f"{criterion}: {score}/5")

# Generate feedback message for improvement
feedback = (
    f"The proposal received the following scores:\n"
    + "\n".join([f"{criterion}: {score}/5" for criterion, score in scores.items()])
    + "\nPlease revise the proposal to improve clarity, completeness, and adherence to the criteria."
)
print("\n--- Feedback ---\n")
print(feedback)

# Add feedback to the conversation
add_message("user", feedback)

# Generate improved proposal
improved_proposal = generate_response()
print("\n--- Improved Proposal ---\n")
print(improved_proposal)
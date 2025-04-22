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
user_input = "Client is Manulife Financial Corporation – Climate Adaptation & Resilience Validate the opportunity for Manulife Financial Corporation to develop a new product in the ‘Climate Adaptation & Resilience’ domain. Test interest in new forms of risk financing that help individuals or businesses invest in climate adaptation infrastructure. Explore partnerships with governments or NGOs to make offerings viable."
add_message("user", user_input)

criteria = {
    "Structure Adherence": lambda proposal: 5 if all(
        section in proposal for section in [
            "Executive Summary", "Client/Proposed Context", "Market Opportunity",
            "Proposed Value Proposition Design Approach", "Key Deliverables", "Timeline", "Price & Engagement Model"
        ]
    ) else 3 if any(
        section in proposal for section in [
            "Executive Summary", "Key Deliverables", "Timeline"
        ]
    ) else 1,
    "Clarity and Brand Tone": lambda proposal: 5 if len(proposal.split()) > 150 else 4 if len(proposal.split()) > 100 else 3 if len(proposal.split()) > 50 else 2,
    "Market Fit Validation": lambda proposal: 5 if "need" in proposal.lower() else 3,
    "Timeline/Budget": lambda proposal: 5 if "timeline" in proposal.lower() and "budget" in proposal.lower() else 3 if "timeline" in proposal.lower() or "budget" in proposal.lower() else 1,
    "Completeness": lambda proposal: 5 if len(proposal.split()) > 200 else 4 if len(proposal.split()) > 150 else 3 if len(proposal.split()) > 100 else 2,
    "Consistency/Stability": lambda proposal: 5  # Assume consistent language for simplicity
}

def grade_proposal(proposal):
    """Grade the proposal based on the success criteria."""
    scores = {key: func(proposal) for key, func in criteria.items()}
    total_score = sum(scores.values()) / len(criteria)  # Average score
    return total_score, scores
def generate_feedback(scores):
    """Generate feedback based on the scoring results."""
    feedback = "The proposal received the following scores:\n"
    for criterion, score in scores.items():
        feedback += f"{criterion}: {score}/5\n"
        if score < 5:
            if criterion == "Structure Adherence":
                feedback += "- Ensure all required sections are included, such as 'Timeline' or 'Price & Engagement Model'.\n"
            elif criterion == "Clarity and Brand Tone":
                feedback += "- Improve clarity by expanding sections and ensuring alignment with the brand tone.\n"
            elif criterion == "Market Fit Validation":
                feedback += "- Clearly address the client's needs and how the proposal meets them.\n"
            elif criterion == "Timeline/Budget":
                feedback += "- Include specific details about the timeline and budget.\n"
            elif criterion == "Completeness":
                feedback += "- Add more content to ensure all required elements are thoroughly addressed.\n"
    feedback += "Please revise the proposal based on this feedback."
    return feedback
# Add initial user message
user_input = "Draft a business proposal for Manulife Financial Corporation to explore a new product in climate adaptation and resilience."
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
feedback = generate_feedback(scores)
print("\n--- Feedback ---\n")
print(feedback)

# Add feedback to the conversation
add_message("user", feedback)

# Generate improved proposal
improved_proposal = generate_response()
print("\n--- Improved Proposal ---\n")
print(improved_proposal)

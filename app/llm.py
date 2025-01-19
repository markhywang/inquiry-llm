import openai
from .models import *

# Please enter an OpenAI API key here in order to use this application
openai.api_key = "[ENTER API KEY NAME HERE]"

# Keep track of all messages to make GPT remember conversational history
llm_answer_messages = []
llm_insight_messages = []

# Store all responses to display on the application
responses = []


# Initialize the role of the system
def init() -> None:
    """Establish the roles of both LLMs so adjust them to their specified roles"""
    llm_answer_messages = []
    llm_insight_messages = []
    responses = []
    
    llm_answer_role = "You are an AI that answers questions concisely and accurately while also being thorough in your explanations."
    llm_insight_role = "You are an AI that responds with insightful and thought-provoking follow-up questions or comments to deepen the understanding of a certain topic."
    
    llm_answer_messages.append({"role": "system", "content": llm_answer_role})
    llm_insight_messages.append({"role": "system", "content": llm_insight_role})


# Function for LLM that answers questions
def llm_answer_inference(question: str) -> str:
    """This LLM answers questions either given by the user or by the other LLM"""
    llm_answer_messages.append({"role": "user", "content": question}) # Store question into LLM messages
    
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo", # Can also used GPT-4, but GPT-4 Turbo is more lightweight and cost-efficient
        messages=llm_answer_messages
    )
    
    # Save this response inside the database
    response_data = Response(
        is_answer=True,
        content=response
    )
    response_data.save()
    
    return response['choices'][0]['message']['content'].strip()
    

# Function for LLM that gives insightful comments
def llm_insight_inference(answer: str) -> str:
    """This LLM gives insightful follow-ups to help the user further deepen their understanding of a particular topic"""
    insight_message = f"Here is an answer to consider when generating insightful and thought-provoking follow-up questions: {answer}"
    llm_insight_messages.append({"role": "user", "content": insight_message}) # Store question into LLM messages
    
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo", # Can also used GPT-4, but GPT-4 Turbo is more lightweight and cost-efficient
        messages=llm_insight_messages
    )
    
    # Save this response inside the database
    response_data = Response(
        is_answer=False,
        content=response
    )
    response_data.save()
    
    return response['choices'][0]['message']['content'].strip()


# Function for generation of conversation between the two LLMs
def generate(initial_prompt: str, rounds=7) -> list[str]:
    init()
    
    # Store current prompt and insight
    current_prompt = initial_prompt
    current_answer = None
    
    # Simulate all rounds except for last two (since those are concluding ones)
    for i in range(0, rounds - 2):
        # If 'i' is even, then it's an answer round. Otherwise, it's an insight round
        if i % 2 == 0:
            current_answer = llm_answer_inference(current_prompt)
            responses.append(current_answer)
        else:
            current_prompt = llm_insight_inference(current_answer)
            responses.append(current_prompt)
            
    # The last two rounds consists of one LLM thanking the other for answering the questions then closing off
    thank_you_message = openai.ChatCompletion.create(
        model="gpt-4-turbo", # Can also used GPT-4, but GPT-4 Turbo is more lightweight and cost-efficient
        messages=[
            {"role": "system", "content": "You are an AI that thanks and appreciates the other AI for answering all of your inquiries."},
            {"role": "user", "content": llm_answer_messages[-1]} # Get the last answer message
        ]
    )
    thank_you_message = thank_you_message['choices'][0]['message']['content'].strip()
    responses.append(thank_you_message)
    
    closing_message = openai.ChatCompletion.create(
        model="gpt-4-turbo", # Can also used GPT-4, but GPT-4 Turbo is more lightweight and cost-efficient
        messages=[
            {"role": "system", "content": "You are an AI that responds politely to a thank-you message, acknowledging it and closing the conversation gracefully."},
            {"role": "user", "content": thank_you_message} # Get the last answer message
        ]
    )
    closing_message = closing_message['choices'][0]['message']['content'].strip()
    responses.append(closing_message)
    
    # Return all responses to be displayed on the application
    return responses

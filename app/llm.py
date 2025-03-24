from openai import OpenAI
from .models import Response
from dotenv import dotenv_values

# Load API key from .env file
CONFIG = dotenv_values(".env")
client = OpenAI(api_key=CONFIG['OPENAI_API_KEY'])

# Keep track of all messages
llm_answer_messages = []
llm_insight_messages = []
responses = []


# Initialize the role of the system
def init() -> None:
    """Establish the roles of both LLMs so adjust them to their specified roles"""
    global llm_answer_messages, llm_insight_messages, responses
    
    llm_answer_messages = []
    llm_insight_messages = []
    responses = []
    
    llm_answer_role = "You are an AI that answers questions concisely and accurately while also being thorough in your explanations. Ensure the output doesn't exceed 1000 characters. If applicable, format any mathematical expressions using LaTeX."
    llm_insight_role = "You are an AI that responds with insightful and thought-provoking follow-up questions or comments to deepen the understanding of a certain topic. Ensure the output doesn't exceed 1000 characters. If applicable, format any mathematical expressions using LaTeX."
    
    llm_answer_messages.append({"role": "system", "content": llm_answer_role})
    llm_insight_messages.append({"role": "system", "content": llm_insight_role})


# Function for LLM that answers questions
def llm_answer_inference(question: str) -> str:
    """This LLM answers questions either given by the user or by the other LLM"""
    llm_answer_messages.append({"role": "user", "content": question})
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=llm_answer_messages
    )
    
    answer = response.choices[0].message.content.strip()
    # Save response in database
    response_data = Response(is_answer=True, content=answer)
    response_data.save()
    
    return answer
    

# Function for LLM that gives insightful comments
def llm_insight_inference(answer: str) -> str:
    """This LLM gives insightful follow-ups to help the user further deepen their understanding of a particular topic"""
    insight_message = f"Here is an answer to consider when generating insightful and thought-provoking follow-up questions: {answer}"
    llm_insight_messages.append({"role": "user", "content": insight_message})
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=llm_insight_messages
    )
    
    insight = response.choices[0].message.content.strip()

    # Save response in database
    response_data = Response(is_answer=False, content=insight)
    response_data.save()
    
    return insight


# Function for generation of conversation between the two LLMs
def generate_responses(initial_prompt: str, rounds) -> list[str]:
    init()
    
    current_prompt = initial_prompt
    current_answer = None
    
    for i in range(rounds - 2):
        if i % 2 == 0:
            current_answer = llm_answer_inference(current_prompt)
            responses.append(current_answer)
        else:
            current_prompt = llm_insight_inference(current_answer)
            responses.append(current_prompt)
            
    # The last two rounds: Thank you and closing messages
    thank_you_message = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI that thanks and appreciates the other AI for answering all of your inquiries. Ensure the output doesn't exceed 1000 characters. If applicable, format any mathematical expressions using LaTeX."},
            {"role": "user", "content": llm_answer_messages[-1]["content"]}
        ]
    )
    thank_you_text = thank_you_message.choices[0].message.content.strip()
    responses.append(thank_you_text)
    
    closing_message = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI that responds politely to a thank-you message, acknowledging it and closing the conversation gracefully. Ensure the output doesn't exceed 1000 characters. If applicable, format any mathematical expressions using LaTeX."},
            {"role": "user", "content": thank_you_text}
        ]
    )
    closing_text = closing_message.choices[0].message.content.strip()
    responses.append(closing_text)
    
    return responses

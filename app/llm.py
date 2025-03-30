import json
from openai import OpenAI
from dotenv import dotenv_values

# Load API key from .env file
CONFIG = dotenv_values(".env")
OPENAI_MODEL = "gpt-4o-mini"
OPENAI_TOOLS = [
    {"type": "web_search_preview"}
]

client = OpenAI(api_key=CONFIG['OPENAI_API_KEY'])

llm_answer_messages = []
llm_insight_messages = []
responses = []

def init() -> None:
    """Initialize the conversation roles."""
    global llm_answer_messages, llm_insight_messages, responses
    llm_answer_messages = []
    llm_insight_messages = []
    responses = []
    
    llm_answer_role = (
        "You are an AI that answers questions concisely and accurately while also being thorough in your explanations. "
        "Ensure the output doesn't exceed 1000 characters. If applicable, format any mathematical expressions using LaTeX."
    )
    llm_insight_role = (
        "You are an AI that responds with insightful and thought-provoking follow-up questions or comments to deepen the understanding of a certain topic. "
        "Ensure the output doesn't exceed 1000 characters. If applicable, format any mathematical expressions using LaTeX."
    )
    
    llm_answer_messages.append({"role": "system", "content": llm_answer_role})
    llm_insight_messages.append({"role": "system", "content": llm_insight_role})

def extract_token(chunk):
    """Safely extract token content from a streaming chunk."""
    delta = getattr(chunk, "delta", None)

    if isinstance(delta, dict):
        return delta.get("content", "")
    elif isinstance(delta, str):
        return delta

    return ""

def llm_answer_inference_stream(question: str):
    """Stream the answer output token by token."""
    llm_answer_messages.append({"role": "user", "content": question})
    response = client.responses.create(
        model=OPENAI_MODEL,
        tools=OPENAI_TOOLS,
        input=llm_answer_messages,
        stream=True
    )

    for chunk in response:
        token = extract_token(chunk)
        if token:
            yield token

def llm_insight_inference_stream(answer: str):
    """Stream the insightful follow-up output token by token."""
    insight_message = (
        "Here is an answer to consider when generating insightful and thought-provoking follow-up questions: "
        f"{answer}"
    )
    llm_insight_messages.append({"role": "user", "content": insight_message})
    response = client.responses.create(
        model=OPENAI_MODEL,
        tools=OPENAI_TOOLS,
        input=llm_insight_messages,
        stream=True
    )

    for chunk in response:
        token = extract_token(chunk)
        if token:
            yield token

def generate_responses_stream(initial_prompt: str, rounds: int):
    """
    Generator that yields each token (wrapped as JSON) as soon as it is received.
    Each round is prefixed by a JSON object with "start": true to signal a new round.
    """
    init()
    current_prompt = initial_prompt
    current_answer = ""
    
    # Alternate rounds: even rounds (LLM A) answer, odd rounds (LLM B) insight.
    for i in range(rounds - 2):
        if i % 2 == 0:
            # LLM A answer round
            yield json.dumps({"model": "LLM A", "round": i, "start": True}) + "\n"

            for token in llm_answer_inference_stream(current_prompt):
                current_answer += token
                yield json.dumps({"model": "LLM A", "round": i, "token": token}) + "\n"
        else:
            # LLM B insight round
            yield json.dumps({"model": "LLM B", "round": i, "start": True}) + "\n"
            current_prompt = ""

            for token in llm_insight_inference_stream(current_answer):
                current_prompt += token
                yield json.dumps({"model": "LLM B", "round": i, "token": token}) + "\n"
    
    # Determine the model of the last round in the loop
    last_round_index = rounds - 3  # last round index produced by loop
    last_model = "LLM A" if (last_round_index % 2 == 0) else "LLM B"
    
    # Alternate the thank-you and closing models based on last round:
    if last_model == "LLM A":
        thank_you_model = "LLM B"
        closing_model = "LLM A"
    else:
        thank_you_model = "LLM A"
        closing_model = "LLM B"
    
    # Thank-you message
    thank_you_stream = client.responses.create(
        model=OPENAI_MODEL,
        tools=OPENAI_TOOLS,
        input=[
            {"role": "system", "content": (
                "You are an AI that thanks and appreciates the other AI for answering all of your inquiries. "
                "Ensure the output doesn't exceed 1000 characters. If applicable, format any mathematical expressions using LaTeX."
            )},
            {"role": "user", "content": llm_answer_messages[-1]["content"]}
        ],
        stream=True
    )
    yield json.dumps({"model": thank_you_model, "round": rounds - 2, "start": True}) + "\n"
    thank_you_text = ""
    for chunk in thank_you_stream:
        token = extract_token(chunk)
        if token:
            thank_you_text += token
            yield json.dumps({"model": thank_you_model, "round": rounds - 2, "token": token}) + "\n"
    
    # Closing message
    closing_stream = client.responses.create(
        model=OPENAI_MODEL,
        tools=OPENAI_TOOLS,
        input=[
            {"role": "system", "content": (
                "You are an AI that responds politely to a thank-you message, acknowledging it and closing the conversation gracefully. "
                "Ensure the output doesn't exceed 1000 characters. If applicable, format any mathematical expressions using LaTeX."
            )},
            {"role": "user", "content": thank_you_text}
        ],
        stream=True
    )
    yield json.dumps({"model": closing_model, "round": rounds - 1, "start": True}) + "\n"
    for chunk in closing_stream:
        token = extract_token(chunk)
        if token:
            yield json.dumps({"model": closing_model, "round": rounds - 1, "token": token}) + "\n"

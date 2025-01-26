# Inquiry LLM  

**Inquiry LLM** is an innovative AI-driven platform designed to foster dynamic and insightful learning through insightful exchanges between two language models. The project features two AI chatbots that collaborate to enhance the user’s understanding of complex topics.

The process starts with the user asking a question on a specific subject (e.g., math, physics, philosophy). LLM A responds with a thoughtful and accurate answer, and LLM B follows up with an insightful, probing question or comment that deepens the discussion. Then, LLM A answers LLM B's new inquiry thoroughly, and this process continues. This back-and-forth exchange simulates a true Socratic dialogue, encouraging exploration and critical thinking to understand any concept at a much deeper level.

Inquiry LLM was written using HTML/CSS, Django, and vanilla JavaScript. The application uses pre-trained LLM models using [OpenAI](https://github.com/OPENAI) API.

## Why Inquiry LLM?
Inquiry LLM stands out as a unique educational tool that transforms passive information retrieval into an active learning process. Whether you're exploring new concepts or diving deeper into familiar topics, Inquiry LLM ensures every interaction is insightful, engaging, and rewarding.

## Key Features
- **Collaborative AI:** Two LLMs engage in a constructive dialogue to explore topics from multiple perspectives.
- **Socratic Method:** Encourages deeper understanding through inquiry and follow-up questions.
- **Dialogue Length Preferences:** Allows the user to choose how many different insights they want in a single complete conversation.
- **User Engagement:** Starts with user questions and builds a meaningful exchange.

## Future Updates
I am planning to update Inquiry LLM from time to time, which includes implementing new features which will further help users better learn any concept or idea they have in mind.

Some features I plan to add are as follows:
- The ability to attach images, files, video, audio, etc.
- Different fine-tuned and aligned models for different educational domains (e.g. a pair of LLMs focused on physics and a different pair focused on, for example, history).
- Interactive visualizations throughout the dialogue, which includes the incorporation of diagrams, graphs, charts, etc. when necessary.
- Conversation summarization
- Random topic suggestions for people with a strong thirst for knowledge :)

## Getting Started
1. In terminal, ```git clone``` the contents of ```https://github.com/markhywang/inquiry-llm```.
2. Ensure all the necessary packages from the ```requirements.txt``` file are installed properly.
3. In terminal, ```cd``` into the main directory of the cloned repository.
4. Enter the command ```python manage.py makemigrations website``` to make migrations for the app.
5. Enter the command ```python manage.py migrate``` to apply migrations to your local SQL database.
6. Create a ```.env``` file and insert (1) an [OpenAI API Key](https://openai.com/index/openai-api/) as well as (2) the value for ```SECRET_KEY``` located inside ```inquiry_llm/settings.py```.
7. Enter the command ```python manage.py runserver``` to run the server locally.

![alt text](https://github.com/markhywang/inquiry-llm/blob/master/assets/dev-screenshot.PNG)
An early-stage development screenshot
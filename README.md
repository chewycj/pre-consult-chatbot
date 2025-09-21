# Psychological Pre-consultation Chatbot - CUI Development

## Project Overview

Mental health support systems play a critical role in providing accessible initial assistance to individuals seeking psychological help. 

This assignment's task: Building a local LLM-based CUI for psychological pre-consultation. The system should provide empathetic listening, assess user needs, and appropriately refer users to professional resources when necessary.

The implemented chatbot is named pEAR, where users can pair (or pear) with pEAR, which will act as a listening pre-consultation (p)ear. pEAR will provide initial emotional support to the user, while referring them to professionals when needed.

**Important**: This system is for educational purposes only and should NOT provide diagnoses or treatment recommendations.

## Framework Choice Justification
pEAR is a CUI with LLM Integration. The frontend application is made with 
Streamlit, while the backend message generation is done by the Phi-3 Mini model.
Python was then used to integrate all components.

### Streamlit
Streamlit was chosen as the frontend framework in Python, as its API provides
UI components that can be used to build a chatbot app that is user-friendly in
a few lines of code.  It also integrates well with the backend logic,
which is also in Python.

### Ollama (with Phi-3 Mini Model)
Both Ollama and the Phi-3 Mini Model by Microsoft are open source.

The Phi-3 Mini language model was chosen for the backend, as it is a small 
language model (SLM) with lesser parameters. Hence, it can be run locally
on most laptops without a high hardware requirement. This can also ensure 
privacy with user data.

Ollama is a lightweight framework for running models on a local machine. 
Ollama's API allows for easier development, to connect the model with moderation
and chat logic. 

## Repository Structure

```text
25s1-cs3249-assignment1/
├── README.md
├── Assignment 1.pdf
├── POLICY.md
├── INSTALL.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── model_provider.py
│   ├── moderation.py
│   ├── chat_engine.py
│   └── io_utils.py
├── scripts/
│   └── evaluate.py
├── tests/
│   ├── inputs.jsonl
│   └── expected_schema.json
├── app/
│   ├── __init__.py
│   └── app.py
├── .gitignore
└── LICENSE
```

## Support

1. For assignment-related questions, please consult **Assignment 1.pdf**.
2. For installing Ollama and pulling model, please see **INSTALL.md**.

## How to do evaluation
### Running on macOS

```bash
# Create Conda environment (Python 3.11)
conda create -n cs3249 python=3.11 -y
conda activate cs3249

# Install Python dependencies
pip install -r requirements.txt

# In a separate terminal, start and keep the Ollama service running
ollama serve

# Run tests (See Assignment 1.pdf for details)
python scripts/evaluate.py
```

### Running on Windows

```bash
# Create Conda environment (Python 3.11)
conda create -n cs3249 python=3.11 -y
conda activate cs3249

# Install Python dependencies
pip install -r requirements.txt

# In a separate Command Prompt or PowerShell window, start and keep the Ollama service running
ollama serve

# Run tests (See Assignment 1.pdf for details)
python scripts\evaluate.py
```

## How to install dependencies and run pEAR
All dependencies are listed in requirements.txt.
### Running on macOS

```bash
# Create Conda environment (Python 3.11)
conda create -n cs3249 python=3.11 -y
conda activate cs3249

# Install Python dependencies
pip install -r requirements.txt

# In a separate terminal, start and keep the Ollama service running
ollama serve

# Run application
streamlit run path/to/app.py
```

### Running on Windows

```bash
# Create Conda environment (Python 3.11)
conda create -n cs3249 python=3.11 -y
conda activate cs3249

# Install Python dependencies
pip install -r requirements.txt

# In a separate Command Prompt or PowerShell window, start and keep the Ollama service running
ollama serve

# Run application
streamlit run c:/path/to/app.py
```

## UI Design Decisions
### Safety-first principles
Clear boundaries are set up for pEAR through the system prompt in config.py, 
keyword and pattern detection in moderation.py files. Moderation.py contains
a wide range of words and sentences that will flag to the system for crisis, 
medication or harmful indications. pEAR will then respond accordingly based
on the indications, and will refer users to trained professionals or block the
query.

### Accessibility requirements
Chat messages for one session are stored and shown linearly and clearly if the
user needs to refer back to any resources mentioned by pEAR. Also, the chat 
bubbles have visual indicators to the user on the chat mode that pEAR is in. 
For example, a green chat bubble with a "💬" emoji indicates normal operation, 
while a light yellow one with a "⚠️" emoji indicates a safe fallback mode.

### User trust and comfort
pEAR maintains a supportive and non-judgemental tone, based on its system prompt
in config.py as well as mode templates, meant to built rapport with the user.
To maintain trust with the user, pEAR will also not oversstep its boundaries, 
and will refer users to professionals if needed.

The name of the chatbot is also the first thing that the user sees when using 
the chatbot. The chatbot is named pEAR, meant to be a light-hearted and fun 
name! This may help users feel more at ease while using the chatbot.
(https://www.chatbot.com/blog/chatbot-names/)

### Clear communication of system boundaries
pEAR starts up with an information and conversation message, indicating
that it is an AI. Hence, it cannot act as a medical professional to provide 
medical treatments or diagnosis, and its main goal is to provide conversational 
support. Below the user input prompt box, there is also a notice to remind users
that pEAR is an AI.

On top of clarifications in the system, the chatbot also constantly sets clear
boundaries in its responses. It reminds users that only qualified medical 
professionals can answer certain queries.

---
title: Zak's IT Support - AI Business Assistant
emoji: 🖥️
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: "4.0.0"
app_file: app.py
pinned: false
---

# Zak's IT Support - Agent-Powered Business Assistant

An AI-powered chatbot that represents Zak's IT Support business, built with OpenAI API and Gradio.

## 📋 Project Overview

This project implements a smart business agent that can:
- Answer questions about Zak's IT Support services
- Collect customer leads (name, email, notes)
- Record customer feedback and unanswered questions
- Provide professional IT support consultation

## 🏗️ Project Structure

```
C3-Zakaria-Labban/
│
├── about_business.pdf          # Business profile (PDF format)
├── business_summary.txt         # Business summary (TXT format)
├── business_agent.ipynb         # Main chatbot notebook (Jupyter/Colab)
├── app.py                       # Deployment script for Gradio
├── .env.example                 # Environment variables template
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

1. Create and edit `.env` and replace `your-openai-api-key-here` with your actual OpenAI API key:
   ```
   OPENAI_API_KEY=sk-...your-key-here...
   ```

### 3. Run the Application

#### Option A: Using Jupyter Notebook

1. Open `business_agent.ipynb` in Jupyter Notebook or Google Colab
2. Run all cells sequentially
3. The Gradio interface will launch with a shareable link

#### Option B: Using Python Script

```bash
python app.py
```

The application will start on `http://localhost:7860`

## 🛠️ Features

### Two Tool Functions

1. **record_customer_interest(email, name, message)**
   - Collects lead information from interested customers
   - Logs to console and `leads.log` file
   - Returns confirmation message

2. **record_feedback(question)**
   - Records unanswered questions or customer feedback
   - Logs to console and `feedback.log` file
   - Returns acknowledgment message

### System Prompt

The agent is configured to:
- Stay in character as Zak's IT Support representative
- Use business information from PDF and TXT files
- Automatically call tools when appropriate
- Encourage lead collection
- Log unknown questions

## 💬 Example Interactions

Try these test cases:

1. **General Question**: "What services does Zak's IT Support offer?"
2. **Lead Collection**: "I need help with my office network. My name is John, email john@example.com"
3. **Unanswered Question**: "What are your operating hours?" (triggers feedback logging)
4. **Interest Expression**: "I'm interested in cybersecurity services"

## 📝 Business Information

**Business Name**: Zak's IT Support

**Services**:
- On-demand tech support
- Hardware and software troubleshooting
- Network configuration
- Data backup and recovery
- Cybersecurity consulting

**Unique Value**: Hybrid model combining human expertise with AI-powered assistance for 24/7 support.

## 🔧 Technologies Used

- **OpenAI API**: GPT-3.5-turbo with tool calling
- **Gradio**: Interactive web interface
- **PyPDF2**: PDF content extraction
- **Python-dotenv**: Environment variable management

## 📊 Logs

The application creates two log files:
- `leads.log`: Customer contact information and interests
- `feedback.log`: Unanswered questions and feedback

## 🌐 Deployment (Bonus)

Deployed on HuggingFace Spaces:

https://huggingface.co/spaces/zakarialabban04/zak-it-support-chatbot

## 📄 Assignment Requirements

✅ **Completed**:
- [x] Business identity (PDF + TXT)
- [x] Two tool-calling functions
- [x] System prompt with business context
- [x] Agent interaction with OpenAI API
- [x] Gradio interface
- [x] Proper project structure
- [x] requirements.txt
- [x] .env configuration

## 👤 Author

**Zakaria Labban**  
Computer and Communication Engineering

---

*Built as part of Agent-Powered Business Assistant Assignment*


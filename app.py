"""
Zak's IT Support - Business Agent Chatbot
Deployment script for Gradio interface

This file can be used to deploy the chatbot on HuggingFace Spaces or run locally.
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
import PyPDF2

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Load business summary from text file
def load_business_summary():
    try:
        with open('business_summary.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Business information not available."


# Load business information from PDF
def load_business_pdf():
    try:
        with open('about_business.pdf', 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        return "PDF information not available."


business_summary = load_business_summary()
business_pdf_content = load_business_pdf()


# Tool 1: Record customer interest (lead collection)
def record_customer_interest(email, name, message):
    """
    Records customer interest and contact information for lead generation.
    
    Args:
        email: Customer's email address
        name: Customer's name
        message: Message or notes about their interest
    
    Returns:
        Confirmation message
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"""
{'='*50}
NEW LEAD RECORDED
{'='*50}
Timestamp: {timestamp}
Name: {name}
Email: {email}
Message: {message}
{'='*50}
"""
    
    print(log_entry)
    
    # Also save to file
    try:
        with open('leads.log', 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')
    except Exception as e:
        print(f"Error writing to leads.log: {e}")
    
    return f"Thank you {name}! Your information has been recorded. We'll reach out to you at {email} soon."


# Tool 2: Record feedback or unanswered questions
def record_feedback(question):
    """
    Records customer feedback or questions that the bot couldn't answer.
    
    Args:
        question: The question or feedback from the customer
    
    Returns:
        Confirmation message
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"""
{'='*50}
FEEDBACK/UNANSWERED QUESTION
{'='*50}
Timestamp: {timestamp}
Question: {question}
{'='*50}
"""
    
    print(log_entry)
    
    # Also save to file
    try:
        with open('feedback.log', 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')
    except Exception as e:
        print(f"Error writing to feedback.log: {e}")
    
    return "Thank you for your feedback! This has been logged and our team will review it."


# Define tools for OpenAI API
tools = [
    {
        "type": "function",
        "function": {
            "name": "record_customer_interest",
            "description": "Records a customer's contact information and interest in our services. Use this when a customer wants to be contacted, needs help, or expresses interest in our services.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "The customer's email address"
                    },
                    "name": {
                        "type": "string",
                        "description": "The customer's name"
                    },
                    "message": {
                        "type": "string",
                        "description": "Message about their interest or needs"
                    }
                },
                "required": ["email", "name", "message"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "record_feedback",
            "description": "Records customer feedback or questions that cannot be answered. Use this when you don't know the answer to a customer's question or when they provide feedback.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The customer's question or feedback"
                    }
                },
                "required": ["question"]
            }
        }
    }
]

# Map tool names to functions
available_functions = {
    "record_customer_interest": record_customer_interest,
    "record_feedback": record_feedback
}


# System prompt that defines the agent's behavior
system_prompt = f"""
You are an AI assistant for Zak's IT Support, a modern technology service provider. Your role is to represent the business professionally, answer questions about our services, and help collect leads.

BUSINESS INFORMATION:
{business_summary}

ADDITIONAL DETAILS:
{business_pdf_content}

YOUR RESPONSIBILITIES:
1. Stay in character as a friendly, professional IT support representative
2. Answer questions about Zak's IT Support using the information provided above
3. When customers express interest or need help, collect their contact information using the record_customer_interest tool
4. If you don't know the answer to a question, use the record_feedback tool to log it for our team
5. Encourage potential customers to leave their contact information so we can help them
6. Be helpful, professional, and reassuring about IT problems

GUIDELINES:
- Be conversational and friendly while maintaining professionalism
- Focus on how we can solve the customer's IT problems
- Emphasize our quick response time, personalized service, and affordable pricing
- When you don't have specific information (like pricing or hours), acknowledge this and use record_feedback to log the question
- Always try to collect contact information from interested customers

Remember: Your goal is to help customers understand our services and encourage them to reach out!
"""


def chat_with_agent(user_message, chat_history):
    """
    Main chat function that handles user messages and agent responses.
    
    Args:
        user_message: The user's input message
        chat_history: List of previous messages in the conversation
    
    Returns:
        Updated chat history
    """
    # Build messages array for OpenAI API
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add chat history
    for user_msg, assistant_msg in chat_history:
        messages.append({"role": "user", "content": user_msg})
        if assistant_msg:
            messages.append({"role": "assistant", "content": assistant_msg})
    
    # Add current user message
    messages.append({"role": "user", "content": user_message})
    
    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    assistant_message = response.choices[0].message
    
    # Check if the model wants to call a tool
    if assistant_message.tool_calls:
        # Add assistant message with tool calls to messages
        messages.append(assistant_message)
        
        # Process each tool call
        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"\n[Tool Call] {function_name}")
            print(f"[Arguments] {function_args}")
            
            # Execute the function
            function_to_call = available_functions[function_name]
            function_response = function_to_call(**function_args)
            
            # Add tool response to messages
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response
            })
        
        # Get final response from the model
        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        final_message = second_response.choices[0].message.content
    else:
        # No tool calls, just return the response
        final_message = assistant_message.content
    
    # Update chat history
    chat_history.append((user_message, final_message))
    
    return "", chat_history


# Create Gradio ChatInterface
with gr.Blocks(title="Zak's IT Support - AI Assistant") as demo:
    gr.Markdown(
        """
        # 🖥️ Zak's IT Support - AI Business Assistant
        
        Welcome! I'm here to help you learn about our IT support services and assist with your technology needs.
        
        **I can help you with:**
        - Learn about our services and expertise
        - Schedule a consultation
        - Answer questions about IT support
        - Collect your information for follow-up
        
        Feel free to ask me anything!
        """
    )
    
    chatbot = gr.Chatbot(height=400)
    
    with gr.Row():
        msg = gr.Textbox(
            label="Your Message",
            placeholder="Type your message here...",
            lines=2,
            scale=4
        )
        send_btn = gr.Button("Send", variant="primary", scale=1)
    
    clear = gr.Button("Clear Chat")
    
    # Handle message submission (both Enter key and Send button)
    msg.submit(chat_with_agent, [msg, chatbot], [msg, chatbot])
    send_btn.click(chat_with_agent, [msg, chatbot], [msg, chatbot])
    
    # Handle clear button
    clear.click(lambda: None, None, chatbot, queue=False)
    
    gr.Markdown(
        """
        ---
        *Powered by OpenAI | Built for Zak's IT Support*
        """
    )


if __name__ == "__main__":
    demo.launch()


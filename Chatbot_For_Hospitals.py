import requests
from bs4 import BeautifulSoup
import time
import gradio as gr
import google.generativeai as genai
import textwrap
import os

os.environ["GOOGLE_API_KEY"] = "AIzaSyA5f8ItgVZeonnoitVM3PyYQQiYkAv_EUQ"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel('gemini-1.5-flash')

HOSPITAL_URLS = {
    "SDMH Hospital Jaipur": "https://sdmh.in/",
    "CK Birla Hospitals, Jaipur": "https://ckshospitals.com/",
    "Jaipur Hospital": "https://jaipurhospital.in/",
    "Rungta Hospital Jaipur": "https://rungtahospital.com/",
    "MG Hospital & Research Centre Jaipur": "https://mgmch.org/",
    "Shalby Hospital Jaipur": "https://shalby.org/hospitals/jaipur-shalby/",
    "Rajasthan Hospital Jaipur": "https://rajasthanhospital.in/",
    "Manipal Hospital Jaipur": "https://www.manipalhospitals.com/jaipur/",
    "Bhagwan Mahaveer Cancer Hospital & Research Centre Jaipur": "https://bmchrc.org/",
    "Eternal Hospital Jaipur": "https://ehcc.org/",
    "Goyal Hospital & Research Centre Jaipur": "https://www.goyalhospital.org/",
    "Yashaman Hospital Jaipur": "https://www.yashamanhospital.com/",
    "ASG Eye Hospital Jaipur": "https://www.asgeyehospital.com/",
    "Manidhari Hospital Jaipur": "https://manidharihospital.com/",
    "Daukiya Hospital Jaipur": "https://www.daukiyahospital.com/"
}

SCRAPED_HOSPITAL_DATA = {}

def scrape_hospital_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        main_content_tags = ['p', 'h1', 'h2', 'h3', 'li', 'span', 'div']
        relevant_text = []
        for tag_name in main_content_tags:
            for tag in soup.find_all(tag_name):
                text = tag.get_text(separator=' ', strip=True)
                if len(text) > 20 and not any(keyword in text.lower() for keyword in ['privacy policy', 'terms of use', 'copyright', 'subscribe', 'menu', 'search']):
                    relevant_text.append(text)

        full_text = " ".join(relevant_text)
        full_text = ' '.join(full_text.split())
        return full_text[:5000]
    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during scraping {url}: {e}")
        return None

def initial_data_load():
    global SCRAPED_HOSPITAL_DATA
    print("Starting initial data scraping...")
    for hospital_name, url in HOSPITAL_URLS.items():
        print(f"Processing {hospital_name} from {url}")
        data = scrape_hospital_data(url)
        if data:
            SCRAPED_HOSPITAL_DATA[hospital_name] = data
            print(f"Successfully scraped data for {hospital_name}.")
        else:
            SCRAPED_HOSPITAL_DATA[hospital_name] = "Information not available from this website."
            print(f"Could not scrape data for {hospital_name}.")
        time.sleep(1)
    print("Initial data scraping complete.")
    if not SCRAPED_HOSPITAL_DATA:
        print("Warning: No hospital data was successfully scraped. Chatbot may not be able to answer questions.")

def generate_response(query, hospital_data, conversation_history):
    if not hospital_data:
        return "I don't have any hospital data loaded to answer your questions. Please check the scraping process."

    context_data = ""
    for hospital, data in hospital_data.items():
        context_data += f"\n--- Hospital: {hospital} ---\n"
        context_data += data + "\n"
    
    chat_prompt = textwrap.dedent(f"""
    You are a helpful and informative chatbot about hospitals in Jaipur.
    Your primary function is to answer user questions based *only* on the provided hospital data.
    You also have a simulated appointment booking feature.

    --- HOSPITAL DATA ---
    {context_data}
    --- END HOSPITAL DATA ---

    User queries can be about hospital information or booking appointments.
    
    If the user asks to book an appointment, guide them through these steps:
    1. First, ask: "Which hospital are you interested in, and what is your full name?"
    2. After receiving the hospital and name, ask: "What is the primary reason for your visit (e.g., General Check-up, Cardiology, Dermatology)?"
    3. After receiving the reason, ask: "Do you have a preferred doctor's name, or any specific doctor you'd like to see?" (Note: You cannot provide a list of doctors; you can only ask the user for a name.)
    4. After receiving the doctor's name (or if none), ask: "What date and time would you prefer for your appointment?"
    5. After collecting all information, provide a confirmation message like: "Thank you, [Patient Name]. Your simulated appointment for [Hospital Name] for [Disease/Specialty] with Dr. [Doctor's Name - or 'no specific doctor'] on [Date] at [Time] has been noted. Please remember, this is a simulated booking for demonstration purposes. To confirm a real appointment, you will need to visit the hospital's official website or contact them directly."
    
    If information is not explicitly found in the provided hospital data for a general query, state that you don't have that specific information. Do not make up answers.
    """)

    full_conversation = []
    full_conversation.append({"role": "user", "parts": [{"text": chat_prompt}]})

    for user_msg, bot_msg in conversation_history:
        full_conversation.append({"role": "user", "parts": [{"text": user_msg}]})
        full_conversation.append({"role": "model", "parts": [{"text": bot_msg}]})
    
    full_conversation.append({"role": "user", "parts": [{"text": query}]})

    try:
        response = model.generate_content(full_conversation)
        return response.text
    except Exception as e:
        print(f"Error generating content with Gemini: {e}")
        return "I apologize, but I'm unable to process your request at the moment due to an issue with the AI model."

def chatbot_interface(message, history):
    response = generate_response(message, SCRAPED_HOSPITAL_DATA, history)
    return response

initial_data_load()

if __name__ == "__main__":
    print("Starting Gradio app...")
    gr.ChatInterface(
        chatbot_interface,
        title="Jaipur Hospitals Info Chatbot",
        description="Ask me anything about hospitals in Jaipur based on scraped data, or try booking a simulated appointment!",
        examples=[
            "I want to book an appointment.",
            "Tell me about Manipal Hospital."
        ]
    ).launch(share=False)
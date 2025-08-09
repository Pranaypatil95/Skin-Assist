import google.generativeai as genai

# Replace with your actual API key
genai.configure(api_key="AIzaSyDUytvZ93WvuNLeymb7vfItp3t87H2uE2A")

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
]

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Get user input
user_input = input("Enter your text: ")

# Check if the input is a skin-related topic
prompt_parts = ["'"+user_input+"' Is this text a skin-related topic? If yes, say 'yes'; if no, say 'no'"]

response = model.generate_content(prompt_parts)

if response.text.lower() == "yes":
    # If yes, generate skin-related information
    prompt_parts = [user_input+"in 5 line"]
    response = model.generate_content(prompt_parts)
    print(response.text)
else:
    print("Invalid")

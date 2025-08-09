import random
import json
import torch
import os
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

cmodel = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


from .model import NeuralNet
from .nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Get the path to the current directory
current_directory = os.path.dirname(__file__)

# Construct the path to the intents.json file
intents_path = os.path.join(current_directory, 'intents.json')

with open(intents_path, 'r') as json_data:
    intents = json.load(json_data)

# Construct the path to the data.pth file
file_path = os.path.join(current_directory, "data.pth")

FILE = file_path
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Dr. Skinn Assist"

def generate_bot_response(user_input):
    print(user_input)
    sentence = tokenize(user_input)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)
    
    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    print("----",prob.item())
    
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                print(f"{bot_name}: {random.choice(intent['responses'])}")
                return f"{bot_name}: {random.choice(intent['responses'])}"
    else:
        prompt_parts = ["'"+user_input+"' Is this text a skin-related topic? If yes, say 'yes'; if no, say 'no'"]

        response = cmodel.generate_content(prompt_parts)

        if response.text.lower() == "yes":
            print(response.text)
            print(user_input)
            # If yes, generate skin-related information
            
            prompt_parts = [user_input+"in 5 lines"]
            response = cmodel.generate_content(prompt_parts)
            print(f"{bot_name}: {response.text}")
            return f"{bot_name}: {response.text}"
        
        else:
            return f"{bot_name}: Sorry sir/mam, I don't understand...\nIf you want you can put your queries in 'Feedback/Queries' section.We will reply as soon as possible."

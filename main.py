from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from chatterbot.filters import get_recent_repeated_responses
from chatterbot.logic import LogicAdapter
import random
def select_chatbot(query, chatbots):
    max_confidence = -1
    best_chatbot = None
    # Iterate through each chatbot and select the one with the highest confidence
    for chatbot in chatbots:
        response=chatbot.get_response(query)
        confidence=response.confidence
        if confidence > max_confidence:
            max_confidence = confidence
            best_chatbot = chatbot
    return best_chatbot
chatbot1 = ChatBot(
    "megabot",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database_uri="sqlite:///megabot.sqlite3",
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry. I am still learning!',
            'maximum_similarity_threshold': 0.50,
        },
    ],
)
chatbot2 = ChatBot(
    "gigabot",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database_uri="sqlite:///gigabot.sqlite3",
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I do not have an answer to that.',
            'maximum_similarity_threshold': 0.80,
        },
    ],
)
lines=[]
with open("dialogs.csv", "r") as file:
    lines = file.readlines()
# Split the dataset into two parts
half = len(lines) // 2
data1 = lines[:half]
data2 = lines[half:]
custom_training_data1 = [
    "hi","hello",
    "How are you?", "I'm doing well,how about you?",
    "What's up?", "Not much, talking to you!",
    "What you doing later","watch a movie",
    "Goodbye", "Catch you later!",
]
#Training bot 1 with input text file and custom.
trainer1=ListTrainer(chatbot1)
trainer1.train(custom_training_data1)
trainer1.train(data1)
custom_training_data2 = [
    "hello?", "hi, wassup",
    "what is your name?", "gigabot",
    "What do you eat?","electricity",
    "see ya", "bye, talk to you later",
]
#Training bot 2 with input text file and custom.
trainer2=ListTrainer(chatbot2)
trainer2.train(custom_training_data2)
trainer2.train(data2)
# Train chatbot1 with English corpus
corpus_trainer1 = ChatterBotCorpusTrainer(chatbot1)
# Train chatbot2 with movie and computer-related corpus
corpus_trainer2 = ChatterBotCorpusTrainer(chatbot2)
corpus_trainer2.train("chatterbot.corpus.english")
chatbots = [chatbot1, chatbot2]
# Interaction with the chatbots
print("Welcome! we are megabot and gigabot. Type 'exit' to end the conversation.")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("Goodbye!")
        break
    else:
        selected_chatbot = select_chatbot(user_input, chatbots)
        print(selected_chatbot.name ,": ",selected_chatbot.get_response(user_input))

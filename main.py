# libraries
from newspaper import Article
import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
warnings.filterwarnings('ignore')

nltk.download('punkt', quiet=True)

# dataset
dataset = Article('https://www.canada.ca/en/public-health/services/diseases/2019-novel-coronavirus-infection/canadas-reponse.html')
dataset.download()
dataset.parse()
dataset.nlp()
dataset_text = dataset.text

# Tokenization
text = dataset_text
sentence_list = nltk.sent_tokenize(text)

# Index Sort
def index_sort(words):
    l = len(words)
    list_index = list(range(0, l))
    temp = words

    for i in range(l):
        for j in range(l):
            if temp[list_index[i]] > temp[list_index[j]]:
                hold = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = hold

    return list_index

    
# Greeting
def greet(user_input):
    user_input = user_input.lower()

    bot_greetings = ['Hi!', 'Hey!', 'Hello!', 'Have any questions?']
    user_greetings = ['hi', 'hey', 'hello', 'whats up', 'sup']

    for word in user_input.split():
        if word in user_greetings:
            return random.choice(bot_greetings)


# Bot answers
def bot_answer(user_input):
    user_input = user_input.lower()
    sentence_list.append(user_input)

    bot_response = ''
    cv = CountVectorizer().fit_transform(sentence_list)
    similarity_scores = cosine_similarity(cv[-1], cv)
    similarity_scores_list = similarity_scores.flatten()
    indexes = index_sort(similarity_scores_list)
    indexes = indexes[1:]
    response_flag = 0
    c = 0

    for i in range(len(indexes)):
        if similarity_scores_list[indexes[i]] > 0.0:
            bot_response = bot_response+' '+sentence_list[indexes[i]]
            response_flag = 1
            c += 1
        if c > 2:
            break

    if response_flag == 0:
        bot_response = bot_response+' '+'I do not understand'

    sentence_list.remove(user_input)

    return bot_response


# Start bot
print('Covi-Bot: Hello I am Covi-Bot, I will answer any questions related to post covid procedures in Canada!')

exit_statements = ['goodbye', 'leave', 'exit', 'see you', 'bye']

while True:
    user_input = input('Type: ')
    if user_input.lower() in exit_statements:
        print('Covi-Bot: Bye! Have a nice day!')
        break
    else:
        if greet(user_input) != None:
            print('Covi-Bot: '+ greet(user_input))
        else:
            print('Covi-Bot: '+bot_answer(user_input))
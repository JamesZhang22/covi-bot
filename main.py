# libraries
from tkinter import *
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
dataset2 = Article('https://www.canada.ca/en/public-health/services/diseases/2019-novel-coronavirus-infection/symptoms.html')
dataset2.download()
dataset2.parse()
dataset2.nlp()
dataset_text2 = dataset.text

# Tokenization
text = dataset_text + dataset_text2
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

    bot_greetings = ['Wassup!', 'Hi there!', 'Hi!', 'Hey!', 'Hello!', 'Have any questions?']
    user_greetings = ['wassup', 'anyone there', 'hi', 'hey', 'hello', 'whats up', 'sup']

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
    response = False
    c = 0

    for i in range(len(indexes)):
        if similarity_scores_list[indexes[i]] > 0.0:
            bot_response = bot_response+' '+sentence_list[indexes[i]]
            response = True
            c += 1
        if c > 0:
            break

    if response == False:
        bot_response = bot_response+' '+'Please clarify, I do not understand'

    sentence_list.remove(user_input)

    return bot_response


class Application:
    def __init__(self):
        self.window = Tk()
        self.setup_main_window()

    def run(self):
        self.window.mainloop()

    def setup_main_window(self):
        self.window.title('Covi-Bot')
        self.window.resizable(width=False, height=False)
        self.window.configure(width=800, height=600, bg='White')

        header = Label(self.window, bg='dark blue', fg='white', text="COVI-BOT", font=('Arial', 15), pady=15)
        header.place(relwidth=1)

        self.text = Text(self.window, width=20, height=2, bg='light blue', fg='black', font=('Arial', 15), padx=5, pady=5)
        self.text.place(relheight=0.8, relwidth=1, rely=0.1)
        self.text.configure(cursor="arrow", state=DISABLED)

        scrollbar = Scrollbar(self.text)
        scrollbar.place(relheight=1, relx=1.1)
        scrollbar.configure(command=self.text.yview)

        bottom_border = Label(self.window, bg='grey', height=80)
        bottom_border.place(relwidth=1, rely=0.82)

        self.message = Entry(bottom_border, bg='light grey', fg='black', font=('Arial', 12))
        self.message.place(relwidth=0.7, relheight=0.06, rely=0.01, relx=0.01)
        self.message.focus()
        self.message.bind('<Return>', self.pressed)

        send_button = Button(bottom_border, text='Send', font=('Arial', 20), width=20, bg='green', activebackground='light green', command=lambda: self.pressed(None))
        send_button.place(relx=0.73, rely=0.01, relheight=0.06, relwidth=0.25)


    def pressed(self, event):
        msg = self.message.get()
        self.insert_msg(msg, "You")


    def insert_msg(self, msg, sender):
        if not msg:
            return

        self.message.delete(0, END)
        message1 = sender +  ': ' + msg + '\n\n'
        self.text.configure(state=NORMAL)
        self.text.insert(END, message1)
        self.text.configure(state=DISABLED)

        message2 = 'Covi-Bot: ' + bot_response(msg) + '\n\n'
        self.text.configure(state=NORMAL)
        self.text.insert(END, message2)
        self.text.configure(state=DISABLED)

        self.text.see(END)


running = True
def bot_response(msg):
    global running
    if msg == 'reconnect':
        running = True
        return 'I am back!'

    exit_statements = ['goodbye', 'leave', 'exit', 'see you', 'bye']

    while running:
        if msg.lower() in exit_statements:
            running = False
            return 'Bye! Have a nice day!'
        elif 'help' in msg.lower():
            return 'Hello I am Covi-Bot, I will answer any questions related to post covid procedures in Canada!'
        elif 'thanks' in msg.lower():
            return 'You are welcome!'
        else:
            if greet(msg) != None:
                return greet(msg)
            else:
                return bot_answer(msg)




if __name__ == "__main__":
    app = Application()
    app.run()
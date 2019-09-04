import telebot
import collections
from QuestionManager import QuestionManager
from Answer import Answer
from QuizQuestion import QuizQuestion
from State import State

class User(object):
	def __init__(self, uid, state):
		self.id = uid
		self.state = state
		self.questionManager = QuestionManager()

class DialogBot(object):

    def __init__(self):
    	self.users = collections.defaultdict(User)

dialogBot = DialogBot()
# state = State.Start

bot = telebot.TeleBot('648232646:AAHfynYQnWd_xD1knO6gZ7bE4V2_hQI_EZE')



@bot.message_handler(commands=['start'])
def start_message(message):
	global dialogBot
	dialogBot.users[message.chat.id] = User(message.chat.id, State.Start)
	keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
	keyboard.add(telebot.types.KeyboardButton(text="Викторина"))
	keyboard.add(telebot.types.KeyboardButton(text="Верю не верю"))
	bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def send_text(message):
	global dialogBot
	state = dialogBot.users[message.chat.id].state
	print(state)
	if state == State.Start:
	    if message.text.lower() == 'викторина':
	        startCountryQuiz(message)
	    elif message.text.lower() == 'верю не верю':
	        startTruthOrLieQuiz(message)
	elif state == State.CountryQuiz:
		if message.text == dialogBot.users[message.chat.id].questionManager.currQuestion.answers[0].text:
			pickAnswer(message, 0)
		elif message.text == dialogBot.users[message.chat.id].questionManager.currQuestion.answers[1].text:
			pickAnswer(message, 1)
		elif message.text == dialogBot.users[message.chat.id].questionManager.currQuestion.answers[2].text:
			pickAnswer(message, 2)
		elif message.text == dialogBot.users[message.chat.id].questionManager.currQuestion.answers[3].text:
			pickAnswer(message, 3)
		elif message.text.lower() == 'далее':
			print(dialogBot.users[message.chat.id].questionManager.cnt, dialogBot.users[message.chat.id].questionManager.maxQuestions)

			if(dialogBot.users[message.chat.id].questionManager.cnt < dialogBot.users[message.chat.id].questionManager.maxQuestions):
				continueCountryQuiz(message)
			else:
				showResults(message)



def startCountryQuiz(message):
	global dialogBot
	dialogBot.users[message.chat.id].state = State.CountryQuiz
	dialogBot.users[message.chat.id].questionManager = QuestionManager()
	questionManager = dialogBot.users[message.chat.id].questionManager
	question = questionManager.getQuestion()
		
	keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
	keyboard.add(telebot.types.KeyboardButton(text=question.answers[0].text))
	keyboard.add(telebot.types.KeyboardButton(text=question.answers[1].text))
	keyboard.add(telebot.types.KeyboardButton(text=question.answers[2].text))
	keyboard.add(telebot.types.KeyboardButton(text=question.answers[3].text))

	bot.send_message(message.chat.id, question.text, reply_markup=keyboard)

def continueCountryQuiz(message):
	global dialogBot
	questionManager = dialogBot.users[message.chat.id].questionManager
	question = questionManager.getQuestion()
		
	keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
	keyboard.add(telebot.types.KeyboardButton(text=question.answers[0].text))
	keyboard.add(telebot.types.KeyboardButton(text=question.answers[1].text))
	keyboard.add(telebot.types.KeyboardButton(text=question.answers[2].text))
	keyboard.add(telebot.types.KeyboardButton(text=question.answers[3].text))

	bot.send_message(message.chat.id, question.text, reply_markup=keyboard)

def pickAnswer(message, num):
	global dialogBot
	questionManager = dialogBot.users[message.chat.id].questionManager
	keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
	keyboard.add(telebot.types.KeyboardButton(text='Далее'))
	if(questionManager.checkAnswer(num)):
		questionManager.rightAnswers += 1
		bot.send_message(message.chat.id, 'Верно', reply_markup=keyboard)
	else:
		bot.send_message(message.chat.id, 'Неверно', reply_markup=keyboard)
		
		text = 'Правильный ответ : ' + questionManager.currQuestion.answers[questionManager.getRightAnswer()].text
		bot.send_message(message.chat.id, text, reply_markup=keyboard)
	
	
	bot.send_message(message.chat.id, questionManager.currQuestion.info, reply_markup=keyboard)




def startTruthOrLieQuiz(message):
	pass

def showResults(message):
	global dialogBot
	dialogBot.users[message.chat.id].state = State.Start
	questionManager = dialogBot.users[message.chat.id].questionManager
	text = 'Ваш результат: ' + str(questionManager.rightAnswers) + '/' + str(questionManager.maxQuestions)

	keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
	keyboard.add(telebot.types.KeyboardButton(text="Викторина"))
	keyboard.add(telebot.types.KeyboardButton(text="Верю не верю"))

	bot.send_message(message.chat.id, text, reply_markup=keyboard)
 

bot.polling()
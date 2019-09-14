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
		self.questionManager = ''

class DialogBot(object):
    def __init__(self):
    	self.users = collections.defaultdict(User)

dialogBot = DialogBot()

bot = telebot.TeleBot('648232646:AAHfynYQnWd_xD1knO6gZ7bE4V2_hQI_EZE')

def isItemExist(_object, test_list):
	for item in test_list: 
		# print(item)
		if(item == _object.id) : 
			print ("Element Exists") 
			return True
	return False

@bot.message_handler(commands=['start'])
def start_message(message):
	global dialogBot
	dialogBot.users[message.chat.id] = User(message.chat.id, State.Start)
	keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
	keyboard.add(telebot.types.KeyboardButton(text="Угадай страну"))
	keyboard.add(telebot.types.KeyboardButton(text="Верю не верю"))
	bot.send_message(message.chat.id, 'Начнем тест?', reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def send_text(message):
	print(message.chat.id)
	global dialogBot
	if not dialogBot.users:
		print('no users')
		return
	if not isItemExist(User(message.chat.id, State.Start), dialogBot.users):
		print("no such user")
		print(*dialogBot.users)
		return
	state = dialogBot.users[message.chat.id].state
	print(state)
	if state == State.Start:
		if message.text.lower() == 'угадай страну':
			startCountryQuiz(message)
		elif message.text.lower() == 'верю не верю':
			startTruthOrLieQuiz(message)

	elif state == State.Results:
		start_message(message)

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
	elif state == State.TruthOrLieQuiz:
		if message.text == 'Правда':
			pickAnswer(message, 0)
		elif message.text == 'Ложь':
			pickAnswer(message, 1)
		elif message.text.lower() == 'далее':
			print(dialogBot.users[message.chat.id].questionManager.cnt, dialogBot.users[message.chat.id].questionManager.maxQuestions)

			if(dialogBot.users[message.chat.id].questionManager.cnt < dialogBot.users[message.chat.id].questionManager.maxQuestions):
				continueCountryQuiz(message)
			else:
				showResults(message)



def startCountryQuiz(message):
	global dialogBot
	dialogBot.users[message.chat.id].state = State.CountryQuiz
	dialogBot.users[message.chat.id].questionManager = QuestionManager('CountryQuiz')
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
	global dialogBot
	dialogBot.users[message.chat.id].state = State.TruthOrLieQuiz
	dialogBot.users[message.chat.id].questionManager = QuestionManager('TruthOrLieParser')
	questionManager = dialogBot.users[message.chat.id].questionManager
	question = questionManager.getQuestion()
		
	keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
	keyboard.add(telebot.types.KeyboardButton(text='Правда'))
	keyboard.add(telebot.types.KeyboardButton(text='Ложь'))
	print(questionManager.currQuestion.info)
	bot.send_message(message.chat.id, question.text, reply_markup=keyboard)

def showResults(message):
	global dialogBot
	dialogBot.users[message.chat.id].state = State.Results
	questionManager = dialogBot.users[message.chat.id].questionManager
	text = 'Ваш результат: ' + str(questionManager.rightAnswers) + '/' + str(questionManager.maxQuestions)
	keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
	keyboard.add(telebot.types.KeyboardButton(text="На главную"))
	bot.send_message(message.chat.id, text, reply_markup=keyboard)
 
if __name__ == "__main__":
	bot.polling()
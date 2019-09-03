import telebot
from QuestionManager import QuestionManager
from Answer import Answer
from QuizQuestion import QuizQuestion
from State import State

# questionManager = QuestionManager()
state = State.Start

bot = telebot.TeleBot('648232646:AAHfynYQnWd_xD1knO6gZ7bE4V2_hQI_EZE')
keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
keyboard.add(telebot.types.KeyboardButton(text="Викторина"))
keyboard.add(telebot.types.KeyboardButton(text="Верю не верю"))

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def send_text(message):
	print(state)
	if state == State.Start:
	    if message.text.lower() == 'викторина':
	        startCountryQuiz(message)
	    elif message.text.lower() == 'верю не верю':
	        startTruthOrLieQuiz(message)
	elif state == State.CountryQuiz:
		if message.text == questionManager.currQuestion.answers[0].text:
			pickAnswer(message, 0)
		elif message.text == questionManager.currQuestion.answers[1].text:
			pickAnswer(message, 1)
		elif message.text == questionManager.currQuestion.answers[2].text:
			pickAnswer(message, 2)
		elif message.text == questionManager.currQuestion.answers[3].text:
			pickAnswer(message, 3)
		elif message.text.lower() == 'далее':
			print(questionManager.cnt, questionManager.maxQuestions)

			if(questionManager.cnt < questionManager.maxQuestions):
				continueCountryQuiz(message)
			else:
				showResults(message)



def startCountryQuiz(message):
	global state
	state = State.CountryQuiz
	global questionManager
	questionManager = QuestionManager()
	question = questionManager.getQuestion()
		
	keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
	keyboard.add(telebot.types.KeyboardButton(text=question.answers[0].text))
	keyboard.add(telebot.types.KeyboardButton(text=question.answers[1].text))
	keyboard.add(telebot.types.KeyboardButton(text=question.answers[2].text))
	keyboard.add(telebot.types.KeyboardButton(text=question.answers[3].text))

	bot.send_message(message.chat.id, question.text, reply_markup=keyboard)

def continueCountryQuiz(message):
	question = questionManager.getQuestion()
		
	keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
	keyboard.add(telebot.types.KeyboardButton(text=question.answers[0].text))
	keyboard.add(telebot.types.KeyboardButton(text=question.answers[1].text))
	keyboard.add(telebot.types.KeyboardButton(text=question.answers[2].text))
	keyboard.add(telebot.types.KeyboardButton(text=question.answers[3].text))

	bot.send_message(message.chat.id, question.text, reply_markup=keyboard)

def pickAnswer(message, num):
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
	global state
	state = State.Start
	text = 'Ваш результат: ' + str(questionManager.rightAnswers) + '/' + str(questionManager.maxQuestions)

	keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
	keyboard.add(telebot.types.KeyboardButton(text="Викторина"))
	keyboard.add(telebot.types.KeyboardButton(text="Верю не верю"))

	bot.send_message(message.chat.id, text, reply_markup=keyboard)
 

bot.polling()
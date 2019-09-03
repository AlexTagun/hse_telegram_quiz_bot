from State import State
from CountryParser import CountryParser
from Answer import Answer
from QuizQuestion import QuizQuestion

class QuestionManager:
	def __init__(self):
		self.cnt = 0
		self.maxQuestions = 10
		self.rightAnswers = 0
		countryParser = CountryParser()
		self.questions = countryParser.questions[:10]
		self.currQuestion = ''

	def getQuestion(self):
		self.cnt += 1
		self.currQuestion = self.questions[self.cnt - 1]
		return self.currQuestion

	def getRightAnswer(self):
		if self.currQuestion.answers[0].correct == 'true':
			return 0
		elif self.currQuestion.answers[1].correct == 'true':
			return 1
		elif self.currQuestion.answers[2].correct == 'true':
			return 2
		elif self.currQuestion.answers[3].correct == 'true':
			return 3
		return 0

	def checkAnswer(self, num):
		print(num, self.getRightAnswer())
		if self.getRightAnswer() == num:
			return True
		return False



import xml.etree.ElementTree as ET
from Answer import Answer
from QuizQuestion import QuizQuestion

class TruthOrLieParser:
	def __init__(self):
		self.questions = []
		root = ET.parse('TruthOrLieQuiz.xml').getroot()
		for type_tag in root.findall('question'):
			qId = type_tag.get('id')
			text = type_tag.get('text')
			info = type_tag.get('info')
			qAnswers = type_tag.findall('answer')

			answers = [0,0,0,0]
			answers[0] = Answer(qAnswers[0].get('id'), qAnswers[0].get('text'), qAnswers[0].get('correct'))
			answers[1] = Answer(qAnswers[1].get('id'), qAnswers[1].get('text'), qAnswers[1].get('correct'))
			answers[2] = Answer('', '', '')
			answers[3] = Answer('', '', '')
			self.questions.append(QuizQuestion(qId, text, info, answers))

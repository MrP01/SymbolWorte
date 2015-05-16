from PySide.QtCore import QObject

from Progress import Calculator
import ListOrders,math
	
def splitWordByCapital(word):
	l=[]
	for i in range(len(word)):
		c=word[i]
		if c == c.upper():
			if i != len(word)-1:
				if word[i+1] == word[i+1].lower():
					c+=word[i+1]
			l.append(c)
	return l

class SymbolWordCalculator(Calculator):
	def __init__(self,periodicSystem):
		Calculator.__init__(self)
		self.periodicSystem=periodicSystem
	
	def calculate(self,word):
		self.word=word.lower()
		self.result=""
		self.resultElements=[]
		
		#Calculating debatable elements
		
		self.progress.setup(len(self.periodicSystem))
		debatable=[]	#List of debatable Elemets (Word contains element.symbol)
		for element in self.periodicSystem:
			for i in range(self.word.count(element.symbol.lower())):	#If symbol twice (or more) in self.word, add it twice!
				debatable.append(element)
			if self.progress.notify():
				break
		
		#Calculating the self.result
		
		def calc(order):
			symWord=""	#Word made of element.symbols in order
			for element in order:
				symWord+=element.symbol
			if self.word in symWord.lower():	#Check whether our self.word matches symWord
				pos=symWord.lower().find(self.word)
				self.result=symWord[pos:pos+len(self.word)]	#If so, we have our self.result!
				return True
			if self.progress.notify():
				return True
		
		self.progress.setup(math.factorial(len(debatable)))
		ListOrders.orders(debatable,calc)	#Loops over all possible orders of debatable
		self.progress.complete()
		
		#Calculating all elements used in self.result
		
		for elementSymbol in splitWordByCapital(self.result):
			for element in debatable:
				if (elementSymbol == element.symbol) and (element not in self.resultElements):
					self.resultElements.append(element)
		
		return self.result != ""

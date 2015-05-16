from PySide.QtCore import QObject,Signal,QThread,QEventLoop
from PySide.QtGui import QWidget,QProgressBar,QPushButton,QHBoxLayout

class Calculator(QObject):
	calculationDone=Signal(object)
	def __init__(self):
		QObject.__init__(self)
		self.progress=Progress()
	
	def main(self,args,kwargs):
		self.calculationDone.emit(self.calculate(*args,**kwargs))
	
	def calculate(self,*args):
		return True

class Worker(QThread):
	_startCalc=Signal(tuple,dict)
	_init=Signal()
	def __init__(self,parent=None):
		QThread.__init__(self,parent)
	
	def start(self):
		QThread.start(self)
		loop=QEventLoop()
		self._init.connect(loop.quit)
		loop.exec_()
	
	def createCalculator(self):	#Reimplement
		return Calculator()
	
	def run(self):
		self.calculator=self.createCalculator()
		self._startCalc.connect(self.calculator.main)
		self._init.emit()
		self.exec_()
	
	def startCalculation(self,*args,**kwargs):
		self._startCalc.emit(args,kwargs)

class Progress(QObject):
	progressSetup=Signal(int)
	progressNotified=Signal(int)
	progressCompleted=Signal()
	def __init__(self):
		QObject.__init__(self)
		self.progress=0
		self.maximum=0
		self._aborted=False
	
	def abort(self):
		self._aborted=True
	
	def setup(self,maximum):
		self._aborted=False
		self.maximum=maximum
		self.progress=0
		self.progressSetup.emit(self.maximum)
	
	def notify(self):
		if self._aborted:
			return True
		self.progress+=1
		self.progressNotified.emit(self.progress)
	
	def complete(self):
		self.progress=self.maximum
		self.progressCompleted.emit()

class ProgressView(QWidget):
	def __init__(self,progress=None,parent=None):
		QWidget.__init__(self,parent)
		self.progressBar=QProgressBar()
		self.abortButton=QPushButton()
		
		layout=QHBoxLayout()
		layout.addWidget(self.progressBar)
		layout.addWidget(self.abortButton)
		self.setLayout(layout)
		
		if progress:
			self.setProgress(progress)
	
	def setProgress(self,progress):
		self.progress=progress
		self.progress.progressSetup.connect(self.progressBar.setMaximum)
		self.progress.progressNotified.connect(self.progressBar.setValue)
		self.progress.progressCompleted.connect(self.progressCompleted)
		self.abortButton.clicked.connect(self.progress.abort)
	
	def progressCompleted(self):
		self.progressBar.setValue(self.progress.maximum)

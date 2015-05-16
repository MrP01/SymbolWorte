#!/usr/bin/env python
# -*- coding: utf-8 -*-

# BEGIN LICENSE
# Copyright (C) 2015 Peter Waldert <peter@waldert.at>
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
# END LICENSE

from PySide.QtGui import (QApplication,QDialog,QLineEdit,QLabel,QPushButton,
						QGridLayout,QTableWidget,QCheckBox,QFrame,QAbstractItemView,
						QTableWidgetItem,QAction,QProgressBar,QWidget,QHBoxLayout,
						QFrame,QRegExpValidator,QSizePolicy,QAction,QIcon,QMessageBox)
from PySide.QtCore import (QRegExp,QSize,Qt,QEventLoop,Signal,QThread,QMutex)

from Progress import ProgressView,Worker
from SymbolWordCalculator import SymbolWordCalculator
import PeriodicSystem,sys,time

class MyWorker(Worker):
	def __init__(self,parent=None):
		Worker.__init__(self,parent)
	
	def createCalculator(self):
		return SymbolWordCalculator(PeriodicSystem.PeriodicSystem.load("Elements.csv"))

class SymbolWort(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		self.setWindowTitle("Symbol-Worte")
		
		self.thread=MyWorker(self)
		self.thread.start()
		self.thread.calculator.calculationDone.connect(self.calculationDone)
		
		self.initUI()
	
	def about(self):
		QMessageBox.information(self,u"Über Symbol-Worte",u"Symbol-Worte ist ein kleines, zum Spaß entwickeltes, Programm. Es nutzt die Open-Source Entwicklungsumgebung Python (www.python.org) und PySide (Qt-Schnittstelle). Es ist unter GPL v.3 veröffentlicht. Entwickelt von Peter Waldert.")
	
	def update(self):
		text=self.lineEdit.text()
		if text.lower() != self.responseLabel.text().lower():
			self.thread.startCalculation(text)
	
	def calculationDone(self,ok):
		if ok:
			self.responseLabel.setText(self.thread.calculator.result)
		else:
			self.responseLabel.setText(u"Keine Treffer")
		self.updateTable(self.thread.calculator.resultElements)
	
	def updateAuto(self,checked):
		if checked:
			self.lineEdit.textEdited.connect(self.update)
		else:
			self.lineEdit.textEdited.disconnect(self.update)
	
	def updateMaxLength(self,checked):
		if checked:
			self.lineEdit.setMaxLength(10)
		else:
			self.lineEdit.setMaxLength(100)
	
	def setupTable(self):
		self.tableWidget.setColumnCount(3)
		self.tableWidget.setHorizontalHeaderLabels(["OZ","Sym","Name"])
		self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.tableWidget.setSelectionMode(QTableWidget.SingleSelection)
		self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
		self.tableWidget.setAlternatingRowColors(True)
	
	def updateTable(self,elements):
		self.tableWidget.clearContents()
		self.tableWidget.setRowCount(len(elements))
		row=0
		for element in elements:
			self.tableWidget.setItem(row,0,QTableWidgetItem(str(element.atomicNumber)))
			self.tableWidget.setItem(row,1,QTableWidgetItem(elements[row].symbol))
			self.tableWidget.setItem(row,2,QTableWidgetItem(elements[row].name))
			row+=1
		self.tableWidget.resizeColumnsToContents()
	
	def initUI(self):
		wordLabel=QLabel("&Wort:")
		responseLabel=QLabel("Symbol-Wort:")
		progressLabel=QLabel("Rechen-Fortschritt:")
		
		self.lineEdit=QLineEdit()
		self.updateButton=QPushButton("&Berechnen")
		self.autoUpdate=QCheckBox("&Auto-Berechnung")
		self.responseLabel=QLabel()
		wordLabel.setBuddy(self.lineEdit)
		self.tableWidget=QTableWidget()
		self.progressView=ProgressView()
		
		self.disableMaxLengthAction=QAction("Zeichenmaximum (Achtung!)",self)
		self.disableMaxLengthAction.setCheckable(True)
		self.disableMaxLengthAction.toggled.connect(self.updateMaxLength)
		self.disableMaxLengthAction.setChecked(True)
		
		self.setupTable()
		self.progressView.setProgress(self.thread.calculator.progress)
		self.progressView.abortButton.setIcon(QIcon.fromTheme("process-stopp",QIcon("Abort.png")))
		self.progressView.abortButton.setToolTip("Stoppe die Berechnung")
		self.lineEdit.setValidator(QRegExpValidator(QRegExp("[A-Za-z]+")))
		self.lineEdit.setToolTip("Nur Zeichen von A-Z")
		self.lineEdit.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.lineEdit.addAction(self.disableMaxLengthAction)
		self.responseLabel.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Fixed)
		self.responseLabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
		self.aboutButton=QPushButton(u"Über")
		f=self.responseLabel.font()
		f.setPointSize(24)
		self.responseLabel.setFont(f)
		
		self.lineEdit.returnPressed.connect(self.update)
		self.updateButton.clicked.connect(self.update)
		self.autoUpdate.stateChanged.connect(self.updateAuto)
		self.aboutButton.clicked.connect(self.about)
		
		layout=QGridLayout()
		layout.addWidget(wordLabel,0,0)
		layout.addWidget(self.lineEdit,0,1)
		layout.addWidget(self.updateButton,0,2)
		layout.addWidget(self.autoUpdate,1,1,1,2)
		layout.addWidget(responseLabel,2,0)
		layout.addWidget(self.responseLabel,2,1,1,2)
		layout.addWidget(self.tableWidget,3,0,1,3)
		layout.addWidget(progressLabel,4,0)
		layout.addWidget(self.progressView,5,0,1,3)
		layout.addWidget(self.aboutButton,6,2)
		self.setLayout(layout)
	
	def closeEvent(self,event):
		self.thread.quit()
		self.thread.wait()
		event.accept()
	
	def keyPressEvent(self,event):
		if event.key() == Qt.Key_Escape:
			self.thread.calculator.progress.abort()
			event.accept()
		else:
			event.ignore()

app=QApplication(sys.argv)
app.setOrganizationName("Peter Waldert")
app.setApplicationName("SymbolWorte")
app.setApplicationVersion("v0.3")
f=SymbolWort()
f.show()
sys.exit(app.exec_())

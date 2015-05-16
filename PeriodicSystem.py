#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv

class Element(object):
	def __init__(self,atomicNumber,symbol,name):
		self.atomicNumber=atomicNumber
		self.symbol=symbol
		self.name=name
	
	def __str__(self):
		return self.symbol+": "+self.name+", "+str(self.ordnungszahl)

class PeriodicSystem(object):
	def __init__(self):
		self._elements={}
	
	def addElement(self,element):
		self._elements[element.atomicNumber]=element
	
	def getElemet(self,atomicNumber):
		return self._elements[atomicNumber]
	
	def getElementBySymbol(self,symbol):
		for element in self:
			if symbol == element.symbol:
				return element
	
	def __iter__(self):
		return iter(self._elements.values())
	
	def __len__(self):
		return len(self._elements.values())
	
	@staticmethod
	def load(filename):
		perSys=PeriodicSystem()
		file=open(filename,"r")
		reader=csv.reader(file,delimiter=",")
		for line in reader:
			perSys.addElement(Element(int(line[2]),str(line[1]),str(line[0])))
		return perSys

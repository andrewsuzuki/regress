#! /usr/bin/env python3

import sys
from collections import OrderedDict

class Book:
	def __init__(self, title, pages, currentPage):
		self.title = title
		self.pages = pages
		self.currentPage = currentPage
	
	def ratio(self):
		if self.pages == 0:
			return 1

		return self.currentPage / self.pages

	def percent(self):
		return self.ratio() * 100

	def bar(self, width):
		filled = int(self.ratio() * width) # floor round
		nonfilled = width - filled
		print("|{}{}|".format("o" * filled, "-" * nonfilled))

class Regress:
	def __init__(self):
		self.books = []
	
	def addBook(self, title, pages, currentPage):
		self.books.append(Book(title, pages, currentPage))
	
	def deleteBook(self, n):
		if n > 0 and n <= len(self.books):
			self.books.pop(n-1)
	
	def listBooks(self, withBar = True):
		i = 1
		for book in self.books:
			print("{}. {} [Page {} of {} : {}%]".format(i, book.title, book.currentPage, book.pages, book.percent()))
			if withBar:
				book.bar(30)
			i += 1

class Filer:
	def __init__(self):
		pass

	def read(self, regress):
		pass

	def save(self, regress):
		pass

class App:
	def __init__(self):
		self.regress = Regress()
		self.filer = Filer()
		
		self.commands = OrderedDict()
		self.commands['q'] = ["Quit this program", lambda: self.quit()]
		self.commands['h'] = ["Show help", lambda: self.showHelp()]
		self.commands['l'] = ["List books", lambda: self.listBooks()]
		self.commands['a'] = ["Add book", lambda: self.addBook()]
		self.commands['d'] = ["Delete book", lambda: self.deleteBook()]
		self.commands['c'] = ["Connect to file", lambda: self.connectToFile()]

	def run(self):
		while True:
			self.newlines(1)
			sys.stdout.write("> ")
			cmd = input()
			lamb = self.commands.get(cmd)
			if lamb != None:
				lamb[1]()
			else:
				print("Command does not exist. Type h for help.")

	def quit(self):
		print("Bye!")
		self.newlines(1)
		sys.exit(0)
	
	def showHelp(self):
		print("Available commands:")
		for command, lamb in self.commands.items():
			print("{}: {}".format(command, lamb[0]))
		

	def listBooks(self):
		self.regress.listBooks()

	def addBook(self):
		title = input("Title: ")
		pages = abs(int(input("Total pages: ")))
		currentPage = abs(int(input("Current page: ")))
		
		self.regress.addBook(title, pages, currentPage)

	def deleteBook(self):
		self.regress.listBooks(False)

		n = int(input("Number: "))

		self.regress.deleteBook(n)
	
	def connectToFile(self):
		self.filer.read()

	def newlines(self, n = 1):
		print("\n" * abs(n - 1))

app = App()
app.run()

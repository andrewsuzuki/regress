#! /usr/bin/env python3

import csv
import sys
import os.path
from collections import OrderedDict

class Book:
	def __init__(self, title, pages, current_page):
		self.title = title
		self.pages = pages
		self.current_page = current_page
	
	def ratio(self):
		if self.pages == 0:
			return 1

		return self.current_page / self.pages

	def percent(self):
		return self.ratio() * 100

	def bar(self, width):
		filled = int(self.ratio() * width) # floor round
		nonfilled = width - filled
		print("|{}{}|".format("o" * filled, "-" * nonfilled))
	
	def write_csv_line(self, writer):
		writer.writerow((self.title, self.pages, self.current_page))

class Regress:
	def __init__(self):
		self.books = []
	
	def add_book(self, title, pages, current_page, dont_replicate = False):
		if dont_replicate == False or not self.book_exists(title):
			self.books.append(Book(title, pages, current_page))
	
	def book_exists(self, title):
		for book in self.books:
			if book.title == title:
				return True
		return False
	
	def delete_book(self, n):
		if n > 0 and n <= len(self.books):
			self.books.pop(n-1)
	
	def list_books(self, with_bar = True):
		i = 1
		for book in self.books:
			print("{}. {} [Page {} of {} : {}%]".format(i, book.title, book.current_page, book.pages, book.percent()))
			if with_bar:
				book.bar(30)
			i += 1

class Filer:
	def __init__(self):
		self.filename = None

	def set_file(self, filename):
		self.filename = filename

	def has_file(self):
		return self.filename != None

	def read(self, regress):
		if not os.path.isfile(self.filename):
			return

		f = self.open_file("r")
		try:
			reader = csv.reader(f)
			for row in reader:
				regress.add_book(row[0], int(row[1]), int(row[2]), True)
		finally:
			f.close()

	def save(self, regress):
		f = self.open_file("w")
		try:
			writer = csv.writer(f)
			for book in regress.books:
				book.write_csv_line(writer)
		finally:
			f.close()
			
	def open_file(self, mode):
		return open(self.filename, mode)

class App:
	def __init__(self):
		self.regress = Regress()
		self.filer = Filer()
		
		self.commands = OrderedDict()
		self.commands['q'] = ["Quit this program", lambda: self.quit()]
		self.commands['h'] = ["Show help", lambda: self.show_help()]
		self.commands['l'] = ["List books", lambda: self.list_books()]
		self.commands['a'] = ["Add book", lambda: self.add_book()]
		self.commands['d'] = ["Delete book", lambda: self.delete_book()]
		self.commands['c'] = ["Connect to file", lambda: self.connect_to_file()]

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
	
	def show_help(self):
		print("Available commands:")
		for command, lamb in self.commands.items():
			print("{}: {}".format(command, lamb[0]))
		

	def list_books(self):
		self.regress.list_books()

	def add_book(self):
		title = input("Title: ")
		pages = abs(int(input("Total pages: ")))
		current_page = abs(int(input("Current page: ")))
		
		self.regress.add_book(title, pages, current_page)
		self.file_sync()

	def delete_book(self):
		self.regress.list_books(False)

		n = int(input("Number: "))

		self.regress.delete_book(n)
		self.file_sync()
	
	def connect_to_file(self):
		self.filer.set_file("books.txt")
		self.filer.read(self.regress)
	
	def file_sync(self):
		if self.filer.has_file():
			self.filer.save(self.regress)

	def newlines(self, n = 1):
		print("\n" * abs(n - 1))

app = App()
app.run()

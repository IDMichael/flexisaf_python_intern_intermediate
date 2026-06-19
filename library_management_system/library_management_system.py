# ==== BOOK IMPLEMENTATION ====
class Book:
	def __init__(self, title, author):
		self.title = title
		self.author = author
		self.available = True

	def borrow_book(self):
		if self.available:
			self.available = False
			return f"'{self.title}' borrowed successfully!"
		return f"'{self.title}' is already borrowed."

	def return_book(self):
		if not self.available:
			self.available = True
			return f"'{self.title}' returned successfully."
		return f"'{self.title}' was not borrowed."
		
	def __str__(self):
		status = "Available" if self.available else "Borrowed"
		return f"'{self.title}' by {self.author} - ({status})"

# ==== LIBRARY IMPLEMENTATION ====
class Library:
	def __init__(self):
		self.books = []
	
	def add_book(self, book):
		self.books.append(book)

	def find_book(self, title):
		for book in self.books:
			if book.title.lower() == title.lower():
				return book
		return None

	def search_by_title(self, title):
		return self.find_book(title)

	def search_by_author(self, author):
		return [
			book
			for book in self.books
			if book.author.lower() == author.lower()
				]

	def borrow_a_book(self, title):
		book = self.find_book(title)

		if book:
			return book.borrow_book()
		return "Book not found."

	def return_a_book(self, title):
		book = self.find_book(title)

		if book:
			return book.return_book()
		return "Book not found."

	def display_books(self):
		for book in self.books:
			print(book)

print("\n==== DEMONSTRATE USAGE ====")
library = Library()

book1 = Book("Learning Python", "Mark Lutz")
book2 = Book("Python for Everybody", "Charles Severance")
book3 = Book("Automate the Boring Stuff with Python", "Al Sweigart")
book4 = Book("Python Crash Course", "Eric Matthes",)

library.add_book(book1)
library.add_book(book2)
library.add_book(book3)
library.add_book(book4)

print("\n==== PRINT ALL BOOKS ====")
library.display_books()

print("\n==== SEARCH BY TITLE ====")
print(library.search_by_title("Automate the Boring Stuff with Python"))

print("\n==== SEARCH BY AUTHOR ====")
# print(library.search_by_author("Al Sweigart"))
for book in library.search_by_author("Al Sweigart"):
	print(book)

print("\n==== BORROW BOOK ====")
print(library.borrow_a_book("Python Crash Course"))

print("\n==== RETIURN BOOK ====")
print(library.return_a_book("Python Crash Course"))

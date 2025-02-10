import json
import jsonpickle

class Book:
    def __init__(self, title="title", author="author", content="content"):
        self.__title = title
        self.__author = author
        self.__content = content

    @property
    def title(self):
        return self.__title

    @property
    def author(self):
        return self.__author

    @property
    def content(self):
        return self.__content

    @title.setter
    def title(self, new_value):
        self.__title = new_value

    @author.setter
    def author(self, new_value):
        self.__author = new_value

    @content.setter
    def content(self, new_value):
        self.__content = new_value

class BookStore:
    def __init__(self):
        self.__books = []

    def add(self, book):
        self.__books.append(book)

    def remove(self, title):
        self.__books = [book for book in self.__books if book.title != title]

    def get(self, title):
        for book in self.__books:
            if book.title == title:
                return book
        return None

    def list(self):
        return [{'title': book.title, 'author': book.author} for book in self.__books]

class User:
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_value):
        self.__name = new_value

class Library:
    def __init__(self):
        self.__users = []

    def add_user(self, user):
        self.__users.append(user)

    def remove_user(self, name):
        self.__users = [user for user in self.__users if user.name != name]

    def get_user(self, name):
        for user in self.__users:
            if user.name == name:
                return user
        return None

    def list_users(self):
        return [user.name for user in self.__users]

class App:
    def __init__(self):
        self.__actions = {
            'ls': self.list_books,
            'new': self.new_book,
            'del': self.delete_book,
            'get': self.get_book,
            'save': self.save_to_disk,
            'load': self.load_from_disk
        }
        self.__book_store = BookStore()
        self.__library = Library()

    def list_books(self):
        books = self.__book_store.list()
        for book in books:
            print(f"Title: {book['title']}, Author: {book['author']}")

    def new_book(self):
        title = input('Title: ')
        author = input('Author: ')
        content = input('Content: ')
        book = Book(title, author, content)
        self.__book_store.add(book)
        print('Book added successfully.')

    def delete_book(self):
        title = input('Title of the book to delete: ')
        self.__book_store.remove(title)
        print('Book deleted successfully.')

    def get_book(self):
        title = input('Title of the book to get: ')
        book = self.__book_store.get(title)
        if book:
            print(f"Title: {book.title}, Author: {book.author}, Content: {book.content}")
        else:
            print('Book not found.')

    def save_to_disk(self):
        for filename, obj in [('my_lib.json', self.__library), ('my_book_store.json', self.__book_store)]:
            with open(filename, 'w') as lib_file:
                raw_json = jsonpickle.encode(obj)
                lib_file.write(raw_json)
        print('Data saved to disk.')

    def load_from_disk(self):
        for filename, obj in [('my_lib.json', self.__library), ('my_book_store.json', self.__book_store)]:
            try:
                with open(filename, 'r') as lib_file:
                    raw_json = lib_file.read()
                    obj = jsonpickle.decode(raw_json)
            except FileNotFoundError:
                print(f'{filename} not found.')
        print('Data loaded from disk.')

    def run(self):
        while True:
            action = input('Action? (ls, new, del, get, save, load, quit): ')
            if action == 'quit':
                break
            if action in self.__actions:
                self.__actions[action]()
            else:
                print('Invalid action. Please try again.')

if __name__ == '__main__':
    app = App()
    app.run()

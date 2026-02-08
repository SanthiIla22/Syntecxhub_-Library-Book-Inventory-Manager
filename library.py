import json

class Book:
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.issued = False

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "issued": self.issued
        }


class Library:
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.books = {}
        self.load_data()

    def add_book(self, book_id, title, author):
        if book_id in self.books:
            print("Book ID already exists!")
            return
        self.books[book_id] = Book(book_id, title, author)
        self.save_data()
        print("Book added successfully.")

    def search_book(self, keyword):
        for book in self.books.values():
            if keyword.lower() in book.title.lower() or keyword.lower() in book.author.lower():
                status = "Issued" if book.issued else "Available"
                print(book.book_id, book.title, book.author, status)

    def issue_book(self, book_id):
        if book_id in self.books and not self.books[book_id].issued:
            self.books[book_id].issued = True
            self.save_data()
            print("Book issued successfully.")
        else:
            print("Book not available.")

    def return_book(self, book_id):
        if book_id in self.books and self.books[book_id].issued:
            self.books[book_id].issued = False
            self.save_data()
            print("Book returned successfully.")
        else:
            print("Invalid return.")

    def report(self):
        total = len(self.books)
        issued = sum(1 for b in self.books.values() if b.issued)
        print("Total books:", total)
        print("Issued books:", issued)

    def save_data(self):
        with open(self.filename, "w") as f:
            json.dump({bid: b.to_dict() for bid, b in self.books.items()}, f)

    def load_data(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                for bid, info in data.items():
                    book = Book(info["book_id"], info["title"], info["author"])
                    book.issued = info["issued"]
                    self.books[bid] = book
        except FileNotFoundError:
            pass


# ----------- Main Menu -----------
library = Library()

while True:
    print("\n1. Add Book")
    print("2. Search Book")
    print("3. Issue Book")
    print("4. Return Book")
    print("5. Report")
    print("6. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        library.add_book(input("ID: "), input("Title: "), input("Author: "))
    elif choice == "2":
        library.search_book(input("Enter title/author: "))
    elif choice == "3":
        library.issue_book(input("Book ID: "))
    elif choice == "4":
        library.return_book(input("Book ID: "))
    elif choice == "5":
        library.report()
    elif choice == "6":
        break
    else:
        print("Invalid choice")
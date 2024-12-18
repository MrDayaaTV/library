import json
from datetime import datetime, timedelta

class Book:
    def __init__(self, title, author, year, genre, copies):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.copies = copies

class Reader:
    def __init__(self, first_name, last_name, card_number, borrowed_books=None):
        self.first_name = first_name
        self.last_name = last_name
        self.card_number = card_number
        # borrowed_books хранит список кортежей: (название книги, дата выдачи)
        self.borrowed_books = borrowed_books or []

class Library:
    def __init__(self):
        self.books = []
        self.readers = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, title):
        self.books = [book for book in self.books if book.title != title]

    def update_book(self, title, **kwargs):
        for book in self.books:
            if book.title == title:
                book.__dict__.update(kwargs)

    def add_reader(self, reader):
        self.readers.append(reader)

    def remove_reader(self, card_number):
        self.readers = [reader for reader in self.readers if reader.card_number != card_number]

    def update_reader(self, card_number, **kwargs):
        for reader in self.readers:
            if reader.card_number == card_number:
                reader.__dict__.update(kwargs)

    def issue_book(self, card_number, book_title):
        reader = next((reader for reader in self.readers if reader.card_number == card_number), None)
        book = next((book for book in self.books if book.title == book_title), None)
        if not reader:
            print("Читатель с таким номером не найден.")
            return
        if not book:
            print("Книга с таким названием не найдена.")
            return
        if book.copies <= 0:
            print("Нет доступных экземпляров книги.")
            return
        overdue_books = [b for b, date in reader.borrowed_books if (datetime.now() - date).days > 14]
        if overdue_books:
            print(f"Читатель имеет просроченные книги: {', '.join(overdue_books)}. Сначала нужно вернуть их.")
            return
        reader.borrowed_books.append((book_title, datetime.now()))
        book.copies -= 1
        print(f"Книга '{book_title}' успешно выдана читателю {reader.first_name} {reader.last_name}.")

    def return_book(self, card_number, book_title):
        reader = next((reader for reader in self.readers if reader.card_number == card_number), None)
        if reader:
            borrowed_book = next((b for b in reader.borrowed_books if b[0] == book_title), None)
            if borrowed_book:
                reader.borrowed_books.remove(borrowed_book)
                book = next((book for book in self.books if book.title == book_title), None)
                if book:
                    book.copies += 1

    def search_books(self, **criteria):
        return [book for book in self.books if all(getattr(book, key, None) == value for key, value in criteria.items())]

    def search_readers(self, **criteria):
        return [reader for reader in self.readers if all(getattr(reader, key, None) == value for key, value in criteria.items())]

    def genre_report(self, genre):
        return sum(book.copies for book in self.books if book.genre == genre)

    def total_books_report(self):
        return sum(book.copies for book in self.books)

    def reader_report(self, card_number):
        reader = next((reader for reader in self.readers if reader.card_number == card_number), None)
        return [b[0] for b in reader.borrowed_books] if reader else []

    def issued_books_report(self):
        report = []
        for reader in self.readers:
            for book_title, borrow_date in reader.borrowed_books:
                report.append({
                    "reader": f"{reader.first_name} {reader.last_name}",
                    "book_title": book_title,
                    "borrow_date": borrow_date.strftime("%Y-%m-%d")
                })
        return report

    def overdue_report(self):
        overdue_list = []
        now = datetime.now()
        overdue_limit = timedelta(days=14)  # срок возврата книги — 14 дней

        for reader in self.readers:
            for book_title, borrow_date in reader.borrowed_books:
                if now - borrow_date > overdue_limit:
                    overdue_list.append({
                        "reader": f"{reader.first_name} {reader.last_name}",
                        "book_title": book_title,
                        "days_overdue": (now - borrow_date).days - 14
                    })

        return overdue_list

    def save_to_file(self, filename):
        data = {
            "books": [book.__dict__ for book in self.books],
            "readers": [
                {
                    "first_name": reader.first_name,
                    "last_name": reader.last_name,
                    "card_number": reader.card_number,
                    "borrowed_books": [
                        {"title": b[0], "borrow_date": b[1].isoformat()} for b in reader.borrowed_books
                    ]
                } for reader in self.readers
            ]
        }
        with open(filename, "w") as file:
            json.dump(data, file)

    def load_from_file(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)
        self.books = [Book(**book) for book in data["books"]]
        self.readers = [
            Reader(
                first_name=reader["first_name"],
                last_name=reader["last_name"],
                card_number=reader["card_number"],
                borrowed_books=[
                    (b["title"], datetime.fromisoformat(b["borrow_date"])) for b in reader["borrowed_books"]
                ]
            ) for reader in data["readers"]
        ]

# Пример использования
if __name__ == "__main__":
    library = Library()

    def display_menu():
        print("\nСистема управления библиотекой")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Добавить читателя")
        print("4. Удалить читателя")
        print("5. Выдать книгу")
        print("6. Загрузить данные из файла")
        print("7. Сохранить данные в файл")
        print("8. Показать отчёт о выданных книгах")
        print("9. Выйти")

    while True:
        display_menu()
        choice = input("Введите номер действия: ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = int(input("Введите год издания книги: "))
            genre = input("Введите жанр книги: ")
            copies = int(input("Введите количество экземпляров книги: "))
            library.add_book(Book(title, author, year, genre, copies))
            print(f"Книга '{title}' успешно добавлена.")

        elif choice == "2":
            title = input("Введите название книги для удаления: ")
            library.remove_book(title)
            print(f"Книга '{title}' успешно удалена.")

        elif choice == "3":
            first_name = input("Введите имя читателя: ")
            last_name = input("Введите фамилию читателя: ")
            card_number = input("Введите номер читательского билета: ")
            library.add_reader(Reader(first_name, last_name, card_number))
            print(f"Читатель '{first_name} {last_name}' успешно добавлен.")

        elif choice == "4":
            card_number = input("Введите номер читательского билета для удаления: ")
            library.remove_reader(card_number)
            print(f"Читатель с номером '{card_number}' успешно удалён.")

        elif choice == "5":
            card_number = input("Введите номер читательского билета: ")
            book_title = input("Введите название книги: ")
            library.issue_book(card_number, book_title)

        elif choice == "6":
            filename = input("Введите имя файла сохранённых данных: ")
            library.load_from_file(filename)
            print(f"Данные успешно загружены из файла'{filename}'.")

        elif choice == "7":
            filename = input("Введите имя файла для сохранения данных: ")
            library.save_to_file(filename)
            print(f"Данные успешно сохранены в файл '{filename}'.")

        elif choice == "8":
            issued_books = library.issued_books_report()
            if issued_books:
                print("\nОтчёт о выданных книгах:")
                for entry in issued_books:
                    print(f"Читатель: {entry['reader']} \nКнига: {entry['book_title']}\n"
                          f"Дата выдачи: {entry['borrow_date']}")
            else:
                print("\nНет выданных книг на данный момент.")

        elif choice == "9":
            print("Выход из системы. До свидания!")
            break

        else:
            print("Неверный ввод. Пожалуйста, выберите правильное действие.")

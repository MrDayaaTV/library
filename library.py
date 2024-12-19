import json
from datetime import datetime, timedelta

from book import Book
from reader import Reader


class Library:  # Предоставление библеотеки
    def __init__(self):
        self.books = []  # Создаёт пустой список для Книг
        self.readers = []  # Создаёт пустой список для Читателей

    def add_book(self, book):  # Добавляет книгу в список
        self.books.append(book)

    def remove_book(self, title):  # Удаляет книгу из списка
        self.books = [book for book in self.books if book.title != title]

    def update_book(self, title, **kwargs):  # Обновляет информацию о книге
        for book in self.books:
            if book.title == title:
                book.__dict__.update(kwargs)

    def add_reader(self, reader):  # Добавляет читателя
        self.readers.append(reader)

    def remove_reader(self, card_number):  # Удаялет читателя
        self.readers = [reader for reader in self.readers if reader.card_number != card_number]

    def update_reader(self, card_number, **kwargs):  # Обновляет информацию о читателе
        for reader in self.readers:
            if reader.card_number == card_number:
                reader.__dict__.update(kwargs)

    def issue_book(self, card_number, book_title):  # Выдаёт книгу читателю
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
        overdue_books = [b for b, date in reader.borrowed_books if
                         (datetime.now() - date).days > 14]  # Проверяет наличие просроченных книг у читателя.
        if overdue_books:
            print(f"Читатель имеет просроченные книги: {', '.join(overdue_books)}. Сначала нужно вернуть их.")
            return
        reader.borrowed_books.append((book_title, datetime.now()))  # Добавляет запись о взятой книге в список
        book.copies = book.copies - 1  # Уменьшает количество доступных экземпляров книги.
        print(f"Книга '{book_title}' успешно выдана читателю {reader.first_name} {reader.last_name}.")

    def return_book(self, card_number, book_title):  # Возвращает книгу
        reader = next((reader for reader in self.readers if reader.card_number == card_number), None)
        if reader:  # Проверяет, найден ли читатель.
            borrowed_book = next((b for b in reader.borrowed_books if b[0] == book_title),
                                 None)  # Ищет запись о взятой книге в списке borrowed_books читателя
            if borrowed_book:  # Проверяет, найдена ли запись о взятой книге
                reader.borrowed_books.remove(borrowed_book)  # Удаляет запись о взятой книге из списка
                book = next((book for book in self.books if book.title == book_title), None)  # Ищет книгу по названию
                if book:
                    book.copies = book.copies + 1

    def search_books(self, **criteria):  # Осуществляет поиск книг по заданным критериям
        return [book for book in self.books if all(getattr(book, key, None) == value for key, value in
                                                   criteria.items())]
        # Возвращает список книг, которые удовлетворяют всем заданным критериям

    def search_readers(self, **criteria):
        return [reader for reader in self.readers if
                all(getattr(reader, key, None) == value for key, value in criteria.items())]

    def genre_report(self, genre):
        return sum(book.copies for book in self.books if
                   book.genre == genre)  # Суммирует количество экземпляров для всех книг с заданным жанром

    def total_books_report(self):
        return sum(book.copies for book in self.books)  # Суммирует количество экземпляров всех книг

    def reader_report(self, card_number):  # Создаёт отчёт о книгах, взятых определённым читателем
        reader = next((reader for reader in self.readers if reader.card_number == card_number),
                      None)  # Ищет читателя по его номеру
        return [b[0] for b in reader.borrowed_books] if reader else []  # Извлекает названия книг, которые взял читатель

    def issued_books_report(self):  # Cоздает отчёт о всех выданных книгах
        report = []
        for reader in self.readers:
            for book_title, borrow_date in reader.borrowed_books:
                report.append({
                    "reader": f"{reader.first_name} {reader.last_name}",
                    "book_title": book_title,
                    "borrow_date": borrow_date.strftime("%d-%m-%Y")
                })
        return report

    def overdue_report(self):  # Создает отчёт о просроченных книгах
        overdue_list = []
        now = datetime.now()
        overdue_limit = timedelta(days=14)  # Срок возврата книги — 14 дней

        for reader in self.readers:
            for book_title, borrow_date in reader.borrowed_books:
                if now - borrow_date > overdue_limit:
                    overdue_list.append({
                        "reader": f"{reader.first_name} {reader.last_name}",
                        "book_title": book_title,
                        "days_overdue": (now - borrow_date).days - 14
                    })

        return overdue_list

    def save_to_file(self, filename):  # Сохраняет данные библиотеки в файл формата json
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

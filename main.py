from library import Library
from book import Book
from reader import Reader


if __name__ == "__main__":
    library = Library()

    def display_menu():
        print("Система управления библиотекой")
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

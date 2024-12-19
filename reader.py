class Reader:  # Ввод данных о добавляемом читателе
    def __init__(self, first_name, last_name, card_number, borrowed_books=None):
        self.first_name = first_name  # Имя
        self.last_name = last_name  # Фамилия
        self.card_number = card_number  # Читательский номер

        self.borrowed_books = borrowed_books or []  # Список взятых книг

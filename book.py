class Book:         # Ввод данных о добавляемой книги
    def __init__(self, title, author, year, genre, copies):
        self.title = title      # Название книги
        self.author = author    # Автор
        self.year = year        # Год
        self.genre = genre      # Жанр
        self.copies = copies    # Количество копий

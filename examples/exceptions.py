class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return
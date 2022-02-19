class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return f'Выстрел в клетку за пределами игрового поля!')

class CellOccupied(BoardException):
    def __str__(self):
        return f'Клетка уже занята!'

class AlreadyShot(BoardException):
    def __str__(self):
        return f'Вы уже стреляли в эту клетку'

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Ship:
    def __init__(self, bow, length, pos, lives):
        self.bow = bow
        self.length = length
        self.pos = pos
        self.lives = lives

    def dots(self): # возвращает список всех точек корабля
        pass


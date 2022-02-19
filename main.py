# Не могу найти, почему при выигрыше компьютера он печатает кучу ходов,
# а потом только завершает игру...

from random import randint


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return 'Выстрел в клетку за пределами игрового поля!'


class AlreadyShotException(BoardException):
    def __str__(self):
        return 'Вы уже стреляли в эту клетку'


class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'({self.x}, {self.y})'


class Ship:
    def __init__(self, bow, length, pos):
        self.bow = bow
        self.length = length
        self.pos = pos
        self.lives = length

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            ship_x = self.bow.x
            ship_y = self.bow.y

            if self.pos == 0:
                ship_x += i

            elif self.pos == 1:
                ship_y += i

            ship_dots.append(Dot(ship_x, ship_y))

        return ship_dots

    def hit(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid = False, size = 6):
        self.hid = hid
        self.size = size
        self.count = 0
        self.field = [['□'] * size for i in range(size)]
        self.busy = []
        self.ships = []

    def out_field(self, dot):
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))

    def contour(self, ship, verb=False):
        near_ship = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for i in ship.dots:
            for ix, iy in near_ship:
                cur = Dot(i.x + ix, i.y + iy)
                if not self.out_field(cur) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = '◦'
                    self.busy.append(cur)

    def add_ship(self, ship):
        for i in ship.dots:
            if self.out_field(i) or i in self.busy:
                raise BoardWrongShipException()
            else:
                self.field[i.x][i.y] = '■'
                self.busy.append(i)

        self.ships.append(ship)
        self.contour(ship)

    def __str__(self):
        result = ''
        result += '   | 1 | 2 | 3 | 4 | 5 | 6 |'
        for i, r in enumerate(self.field):
            result += f"\n {i + 1} | " + " | ".join(r) + " | "

        if self.hid:
            result = result.replace('■', '□')

        return result

    def shot(self, dot):
        if self.out_field(dot):
           raise BoardOutException()

        elif dot in self.busy:
           raise AlreadyShotException()

        self.busy.append(dot)

        for ship in self.ships:
            if ship.hit(dot):
                ship.lives -= 1
                self.field[dot.x][dot.y] = 'X'
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print('Корабль уничтожен!')
                    return False
                else:
                    print('Корабль ранен!')
                    return True
        self.field[dot.x][dot.y] = '◦'
        print('Мимо!')
        return False

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, main, enemy):
        self.main = main
        self.enemy = enemy

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        Dot_ = Dot(randint(0, 5), randint(0, 5))
        print(f'Ход компьютера: {Dot_.x+1}, {Dot_.y+1}')
        return Dot_


class User(Player):
    def ask(self):
        while True:
            cords = input('Введите координаты через пробел: ').split(' ')
            if len(cords) != 2:
                print('Введите 2 координаты!')
                continue

            x, y = cords
            if not x.isdigit() or not y.isdigit():
                print('Введите числа!')
                continue

            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        user_board = self.random_board()
        ai_board = self.random_board()
        ai_board.hid = False ################# !!!

        self.ai = AI(ai_board, user_board)
        self.us = User(user_board, ai_board)

    def try_board(self):
        lengths = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0

        for i in lengths:
            while True:
                attempts += 1
                if attempts > 500:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), i, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def greet(self):
        print('■ □ ■ □ ■ □ ■ □ ■ □ ■ ')
        print('■    МОРСКОЙ БОЙ    ■ ')
        print('■ □ ■ □ ■ □ ■ □ ■ □ ■ ')
        print('  Формат ввода: x y')
        print('  x - номер строки')
        print('  y - номер столбца')

    def loop(self):
        num = 0
        while True:
            print('-' * 15)
            print('Пользователь:')
            print(self.us.main)
            print('-' * 15)
            print('Компьютер:')
            print(self.ai.main)
            if num % 2 == 0:
                print('-' * 15)
                print('Ходит пользователь: ')
                repeat = self.us.move()
            else:
                print('-' * 15)
                print('Ходит компьютер: ')
                repeat = self.ai.move()

            if repeat:
                num -= 1

            if self.ai.main.count == 7:
                print('-' * 15)
                print('Пользователь выиграл!')
                break

            if self.us.main.count == 7:
                print('-' * 15)
                print('Компьютер выиграл!')
                break

            num += 1

    def start_game(self):
        self.greet()
        self.loop()


g = Game()
g.start_game()



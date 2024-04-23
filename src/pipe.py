from sys import stdin

class Board:
    """ Representação interna de uma grelha de PipeMania. """

    def __init__(self):
        self.matrix = []

    def add_line(self, line):
        self.matrix.append(line)
        
    def adjacent_vertical_values(self, row: int, col: int):
        """ Devolve os valores imediatamente acima e abaixo,
        respectivamente. """
        if row - 1 <= 0:
            up = None
        else:
            up = self.matrix[row - 1][col]
        
        if row + 1 >= self.matrix.size() - 1:
            down = None
        else:
            down = self.matrix[row + 1][col]
        
        return (up, down)

    def adjacent_horizontal_values(self, row: int, col: int):
        """ Devolve os valores imediatamente à esquerda e à direita,
        respectivamente. """
        if col - 1 <= 0:
            left = None
        else:
            left = self.matrix[row][col - 1]
        
        if col + 1 >= self.matrix.size() - 1:
            right = None
        else:
            right = self.matrix[row][col + 1]
        
        return (left, right)

    # TODO: outros metodos da classe

    @staticmethod
    def parse_instance(board):
        """Lê a instância do problema do standard input (stdin)
        e retorna uma instância da classe Board.
        Por exemplo:
        $ python3 pipe_mania.py < input_T01
        > from sys import stdin
        > line = stdin.readline().split()
        """
        while stdin.isatty():
        line = stdin.readline().split('\t')
        board.add_line(line)

        return
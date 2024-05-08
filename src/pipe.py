# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 107061 David Antunes
# 107251 João Ribeiro

import sys 
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


pieces = ["FC", "FB", "FE", "FD", "BC", "BB", "BE", "BD", "VC", "VB", "VE", "VD", "LH", "LV"]

connections = {      # (up, right, down, left)
    "FC" : (True,False,False,False,1),
    "FD" : (False,True,False,False,1),
    "FB" : (False,False,True,False,1),
    "FE" : (False,False,False,True,1),
    "BC" : (True,True,False,True,3),
    "BD" : (True,True,True,False,3),
    "BB" : (False,True,True,True,3),
    "BE" : (True,False,True,True,3),
    "VC" : (True,False,False,True,2),
    "VD" : (True,True,False,False,2),
    "VB" : (False,True,True,False,2),
    "VE" : (False,False,True,True,2),
    "LH" : (False,True,False,True,2),
    "LV" : (True,False,True,False,2)
}

actions = {
    "FC": ("FB", "FE", "FD"),
    "FB": ("FC", "FE", "FD"),
    "FE": ("FC", "FB", "FD"),
    "FD": ("FB", "FE", "FC"),
    
    "BC": ("BB", "BE", "BD"),
    "BB": ("BC", "BE", "BD"),
    "BE": ("BC", "BB", "BD"),
    "BD": ("BB", "BE", "BC"),

    "VC": ("VB", "VE", "VD"),
    "VB": ("VC", "VE", "VD"),
    "VE": ("VC", "VB", "VD"),
    "VD": ("VB", "VE", "VC"),

    "LH": ("LV"),
    "LV": ("LH")
}

class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de PipeMania."""

    def __init__(self):
        self.matrix = []

    def get_value(self, row: int, col: int):
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.matrix[row][col]

    def set_value(self, row, col, piece):
        self.matrix[row][col] = piece
    
    def __len__(self):
        return self.matrix.__len__()

    def add_line(self, line):
        self.matrix.append(line)
        
    def adjacent_vertical_values(self, row: int, col: int):
        """ Devolve os valores imediatamente acima e abaixo,
        respectivamente. """
        if row - 1 < 0:
            up = None
        else:
            up = self.matrix[row - 1][col]
        
        if row + 1 >= self.matrix.__len__():
            down = None
        else:
            down = self.matrix[row + 1][col]
        
        return (up, down)

    def adjacent_horizontal_values(self, row: int, col: int):
        """ Devolve os valores imediatamente à esquerda e à direita,
        respectivamente. """
        if col - 1 < 0:
            left = None
        else:
            left = self.matrix[row][col - 1]
        
        if col + 1 >= self.matrix.__len__():
            right = None
        else:
            right = self.matrix[row][col + 1]
        
        return (left, right)

    # TODO: outros metodos da classe

    def print(self):
        print(self.matrix)

    def number_piece_connections(self, row:int, col:int):
        piece = self.matrix[row][col]
        number_connections = 0
        vertical = self.adjacent_vertical_values(row,col)
        horizontal = self.adjacent_horizontal_values(row,col)
        pieceCon = connections.get(piece)
        if vertical[0] and pieceCon[0] and connections.get(vertical[0])[2]:
            number_connections += 1
        if vertical[1] and pieceCon[2] and connections.get(vertical[1])[0]:
            number_connections += 1 
        if horizontal[0] and pieceCon[3] and connections.get(horizontal[0])[1]:
            number_connections += 1 
        if horizontal[1] and pieceCon[1] and connections.get(horizontal[1])[3]:
            number_connections += 1
        return number_connections
     
    @staticmethod
    def parse_instance():
        """Lê a instância do problema do standard input (stdin)
        e retorna uma instância da classe Board.
        Por exemplo:
        $ python3 pipe_mania.py < input_T01
        > from sys import stdin
        > line = stdin.readline().split()
        """
        board = Board()
        line = sys.stdin.readline().split()
        size = line.__len__()
        board.add_line(line)

        for i in range(size-1):
            line = sys.stdin.readline().split()
            board.add_line(line)
        return board


class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.state = PipeManiaState(board)


    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        res = []
        size = state.board.__len__()
        for row in range(size):
            for col in range(size):
                curr_piece = state.board.get_value(row, col)
                for piece in actions.get(curr_piece):
                    res.append((row, col, piece))
        return res

        

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        state.board.set_value(action[0], action[1], action[2])
        return state

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input
    board = Board.parse_instance()
    board.print()
    problem = PipeMania(board)
    print(board.number_piece_connections(0,1))
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass

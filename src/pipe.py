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

connections = {      # (up, right, down, left, max connections)
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
    "FC": ("FB", "FE", "FD", "FC"),
    "FB": ("FC", "FE", "FD", "FB"),
    "FE": ("FC", "FB", "FD", "FE"),
    "FD": ("FB", "FE", "FC", "FD"),
    
    "BC": ("BB", "BE", "BD", "BC"),
    "BB": ("BC", "BE", "BD", "BB"),
    "BE": ("BC", "BB", "BD", "BE"),
    "BD": ("BB", "BE", "BC", "BD"),

    "VC": ("VB", "VE", "VD", "VC"),
    "VB": ("VC", "VE", "VD", "VB"),
    "VE": ("VC", "VB", "VD", "VE"),
    "VD": ("VB", "VE", "VC", "VD"),

    "LH": ("LV", "LH"),
    "LV": ("LH", "LV")
}

class PipeManiaState:
    state_id = 0

    def __init__(self, board, row, col, connections, possiblePieces):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1
        self.connections = connections
        self.curr_coords = [row, col]
        self.possiblePieces = possiblePieces

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe

    def set_connections(self, connections):
        self.connections = connections

    def get_connections(self):
        return self.connections
    
    def get_curr_coords(self):
        return self.curr_coords

    def next_piece(self):
        if self.curr_coords[1] == self.board.__len__() - 1:
            self.curr_coords[0] += 1
            self.curr_coords[1] = 0
        else:
            self.curr_coords[1] += 1
    
    def pre_processing(self):
        size = self.board.__len__()
        change = True
        while(change):
            change = False
            for row in range(size):
                for col in range(size):
                    if self.possiblePieces[row][col].__len__() == 1:
                        continue
                    for piece in self.possiblePieces[row][col]:
                        connect = connections.get(piece)
                        if row == 0 and connect[0]:
                            self.possiblePieces[row][col].remove(piece)
                            change = True
                            continue
                        elif row == (size-1) and connect[2]:
                            self.possiblePieces[row][col].remove(piece)
                            change = True
                            continue
                        elif col == 0 and connect[3]:
                            self.possiblePieces[row][col].remove(piece)
                            change = True
                            continue
                        elif col == (size-1) and connect[1]:
                            self.possiblePieces[row][col].remove(piece)
                            change = True
                            continue
                        
                        if row != 0:
                            remove = True
                            for adjPiece in self.possiblePieces[row-1][col]:
                                if connect[0] == connections.get(adjPiece)[2]:
                                    remove = False
                            if remove:
                                self.possiblePieces[row][col].remove(piece)
                                change = True
                                continue

                        if row != size-1:
                            remove = True
                            for adjPiece in self.possiblePieces[row+1][col]:
                                if connect[2] == connections.get(adjPiece)[0]:
                                    remove = False
                            if remove:
                                self.possiblePieces[row][col].remove(piece)
                                change = True
                                continue

                        if col != 0:
                            remove = True
                            for adjPiece in self.possiblePieces[row][col-1]:
                                if connect[3] == connections.get(adjPiece)[1]:
                                    remove = False
                            if remove:
                                self.possiblePieces[row][col].remove(piece)
                                change = True
                                continue

                        if col != size-1:
                            remove = True
                            for adjPiece in self.possiblePieces[row][col+1]:
                                if connect[1] == connections.get(adjPiece)[3]:
                                    remove = False
                            if remove:
                                self.possiblePieces[row][col].remove(piece)
                                change = True
                                continue
        return

    def deep_copy(self):
        newBoard = Board()
        newPossiblePieces = []
        size = self.board.__len__()
        for row in range(size):
            line = []
            possibleLine = []
            for col in range(size):
                line.append(self.board.get_value(row,col))
                possibleLine.append(self.possiblePieces[row][col].copy())
            newBoard.add_line(line)
            newPossiblePieces.append(possibleLine)
        currCords = self.get_curr_coords()
        return PipeManiaState(newBoard,currCords[0],currCords[1], self.get_connections(), newPossiblePieces)




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
        size = self.__len__()
        for row in range(size):
            for col in range(size):
                if col == size - 1:
                    print(self.get_value(row,col))
                else: 
                    print(self.get_value(row,col), end = "\t")

    def number_piece_connections(self, row:int, col:int):
        piece = self.matrix[row][col]
        numberConnections = 0
        vertical = self.adjacent_vertical_values(row,col)
        horizontal = self.adjacent_horizontal_values(row,col)
        pieceCon = connections.get(piece)
        if vertical[0] and pieceCon[0] and connections.get(vertical[0])[2]:
            numberConnections += 1
        if vertical[1] and pieceCon[2] and connections.get(vertical[1])[0]:
            numberConnections += 1 
        if horizontal[0] and pieceCon[3] and connections.get(horizontal[0])[1]:
            numberConnections += 1 
        if horizontal[1] and pieceCon[1] and connections.get(horizontal[1])[3]:
            numberConnections += 1
        return numberConnections
     
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
        (self.maxConnections, curr,possiblePieces) = self.get_connections(board)
        self.initial = PipeManiaState(board, 0, 0, curr,possiblePieces)

    def get_connections(self,board: Board):
        size = board.__len__()
        max = 0
        curr = 0
        possiblePieces = []
        for row in range(size):
            line = []
            for col in range(size):
                max += connections.get(board.get_value(row,col))[4]
                curr += board.number_piece_connections(row,col)
                piece = board.get_value(row,col)
                line.append([x for x in actions.get(piece)])
            possiblePieces.append(line)
        return (max, curr,possiblePieces)
                    
        
    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        res = []
        size = state.board.__len__()

        curr_coords = state.get_curr_coords()
        row = curr_coords[0]
        col = curr_coords[1]

        if row >= size:
            return []

        while state.possiblePieces[row][col].__len__() == 1:
            piece = state.possiblePieces[row][col][0]

            oldPieceCon = state.board.number_piece_connections(row, col)
            state.board.set_value(row, col, piece)
            newPieceCon = state.board.number_piece_connections(row, col)
            diff = (newPieceCon - oldPieceCon) * 2
            update = state.get_connections() + diff
            state.set_connections(update)
            if row == size-1 and col == size-1:
                #state.board.print()
                break
            state.next_piece()
            curr_coords = state.get_curr_coords()
            row = curr_coords[0]
            col = curr_coords[1]

        for piece in state.possiblePieces[row][col]:
            res.append((row, col, piece))
        return res  


    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        #Deep copy State and apply action
        newState = state.deep_copy()
        newState.board.set_value(action[0], action[1], action[2])
        #Add next valid pieces to action
        #Verify if current connections change and update them on newState
        oldPieceCon = state.board.number_piece_connections(action[0], action[1])
        newPieceCon = newState.board.number_piece_connections(action[0], action[1])
        diff = (newPieceCon - oldPieceCon) * 2
        update = newState.get_connections() + diff
        newState.set_connections(update)
        newState.possiblePieces[action[0]][action[1]] = [action[2]]
        newState.pre_processing()
        newState.next_piece()
        return newState

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # If Max Connections == Current Connection and Conexo 
        if state.get_connections() == self.maxConnections:
            return True
        return False
    
    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # Max Connections - Current Connections
        return self.maxConnections - node.state.get_connections()

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input
    board = Board.parse_instance()
    #Criar uma instancia do PipeMania
    problem = PipeMania(board)
    problem.initial.pre_processing()
    # Usar uma técnica de procura para resolver a instância, Retirar a solução a partir do nó resultante,
    goal_node = depth_first_tree_search(problem)
    # Imprimir para o standard output no formato indicado.
    goal_node.state.board.print()
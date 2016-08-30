#!/usr/bin/python3

# board.py

class Board():
    'Class for handling the board state. This class is ignorant of game logic rules.'

    def __init__(self):
        'Creates a blank 9x9 board and sets the current display_method.'
        self._board = [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]
        ]

    def get_board(self):
        'Returns the current board.'

        return self._board

    def get_cell(self, row: int, column: int):
        'Returns the value of a cell.'

        return self._board[row][column]

    def get_row(self, row: int):
        'Returns the values of a row.'

        row_list = []
        for value in self._board[row]:
            row_list.append(value)

        return row_list
        
    def get_column(self, column: int):
        'Returns the values of a column.'

        col_list = []
        for row in range(len(self._board)):
            col_list.append(self._board[row][column])
        return col_list

    def get_box(self, row: int, column: int):
        'Returns the values of the 3x3 box that the given cell is a member of.'
        values = []
        for index in self._box_indices(row, column):
            values.append(self._board[index[0]][index[1]])

        return values
    
    def add(self, row: int, column: int, number: int):
        'Changes the value of a cell to a certain number.'
        self._board[row][column] = number

    def clear(self, row: int, column: int):
        'Clears the given cell and returns the number that was there.'
        pass

    def to_csv(self, filename):
        'Saves board to a csv file format at the given filename.'
        pass

    def read_csv(self, filename):
        'Loads board from the csv file at the given filename.'
        pass

    def print_board(self):
        'Prints the board.'
        pass

    def display_board(self, display_method):
        'Displays the board, defaulting to the current display method.'
        pass

    def set_board(self, board):
        'Takes a representation of a board state as input and sets it as the current board state'
        pass

    def set_display_method(self, display_method):
        'Sets the current display method.'
        pass

    def _box_indices(self, row: int, column: int):
        'Returns the indices for all the members of the given 3x3 box.'
        indices = []

        row_bounds = self._box_bounds(row, column)[0]
        column_bounds = self._box_bounds(row, column)[1]

        for row_index in range(row_bounds[0], row_bounds[1] + 1):

            row = row_index

            for column_index in range(column_bounds[0], column_bounds[1] + 1):

                column = column_index
                indices.append((row, column))

        return indices


    def _box_bounds(self, row: int, column: int):
        '''
        Returns a list of two tuples that indicates the index bounds for the box that the given cell is in. First tuple represents the index bounds of the row.
        Second tuple represents the index bounds of the column
        '''

        # first section

        box_bounds = []
        
        if  0 <= row <= 2 and 0 <= column <= 2:
            box_bounds = [(0,2),(0,2)]

        elif 0 <= row <= 2 and 3 <= column <= 5:
            box_bounds = [(0,2),(3,5)]

        elif 0 <= row <= 2 and 6 <= column <= 8:
            box_bounds = [(0,2),(6,8)]

        # second section

        elif 3 <= row <= 5 and 0 <= column <= 2:
            box_bounds = [(3,5),(0,2)]

        elif 3 <= row <= 5 and 3 <= column <= 5:
            box_bounds = [(3,5),(3,5)]

        elif 3 <= row <= 5 and 6 <= column <= 8:
            box_bounds = [(3,5),(6,8)]

        # third section

        elif 6 <= row <= 8 and 0 <= column <= 2:
            box_bounds = [(6,8),(0,2)]

        elif 6 <= row <= 8 and 3 <= column <= 5:
            box_bounds = [(6,8),(3,5)]

        elif 6 <= row <= 8 and 6 <= column <= 8:
            box_bounds = [(6,8),(6,8)]

        return box_bounds


        


                        

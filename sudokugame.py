#!/usr/bin/python3

# sudokugame.py

import board
from collections import namedtuple
import os
import prompt
from tkinter.tix import ROW


CONTROLS = '''
CONTROLS
a: add a number
c: change a number
r: remove a number
<: undo move
>: redo move
'''

class Game():
    '''Handles all the game logic and interfaces with the board to execute moves.'''

    def __init__(self):
        'Starts a new game'
        self._board = board.Board()
        self._undo_list = []
        self._redo_list = []
        self._permanency = [[False,False,False,False,False,False,False,False,False] for row in range(9)]
            
    def new_game(self):
        'resets board to orignial state'
        for move in range(len(self._undo_list)):
            self.undo_move()

    def get_board(self):
        'Returns a representation of the game board.'
        return self._board._state

    def open_cells(self):
        'Returns a list of the cells that are empty.'
        open_cells_list = []
        for row in range(len(self._board._state)):
            for col in range(len(self._board._state)):
                if self._board._state[row][col] == 0:
                    open_cells_list.append((row, col))
        return open_cells_list


    def add_number(self, row: int, col: int, number: int):
        "Executes a move if it's valid. Adds move to undo list and clears redo list"
        self._validate_move('a', row, col, number)
        self._board.add(row, col, number)

        action = Add(row, col, number)
        self._undo_list.append(action)
        self._redo_list = []
    
    def change_number(self, row: int, col: int, new_num: int):
        "Allows a cell that is not zero to be changed to a new number if the cell is non-permanent. Executes change if move is valid"
        if self._permanency[row][col] == True:
            raise PermanencyError(row,col)
        
        self._validate_move('c', row, col, new_num)
        
        old_num = self._board.clear(row, col)
        self._board._state[row][col] = new_num
        action = Change(row, col, old_num, new_num)
        self._undo_list.append(action)
        self._redo_list = []
        
    def remove_number(self, row: int, col: int):
        "Remove a number from the given cell"
        if self._permanency[row][col] == True:
            raise PermanencyError(row,col)
        number = self._board.clear(row, col)
        move = self._store_move('remove', row, col, number)
        
        self._undo_list.append(move)
        self._redo_list = []

    def undo_move(self):
        'Undoes the last move if there are any. Otherwise raises exception.'
        if len(self._undo_list) == 0:
            raise UndoError

        else:
            last_action = self._undo_list.pop()
            number = last_action.get_old_num()
            row, col = last_action.get_coordinates()
            self._board._state[row][col] = number
            
            self._redo_list.append(last_action)


    def redo_move(self):
        'Redoes the last undo if there are any. Otherwise raises exception.'
        if len(self._redo_list) == 0:
            raise RedoError

        else:
            last_undo = self._redo_list.pop()
            number = last_undo.get_new_num()
            row, col = last_undo.get_coordinates()
            self._board._state[row][col] = number
            
            self._undo_list.append(last_undo)

    def save_state(self, state_name: str='save'):
        '''
        Saves the current state. Uses state_name to name the csv file in
        the board's to_csv call. 
        '''
        self._board.to_csv(state_name + '.csv')


    def load_state(self, state_name: str='save'):
        'Loads a board state'
        self._board.read_csv(state_name + '.csv')

    def check_victory(self) -> bool:
        'Checks the victory conditions have been met.'
        win_entries = [1,2,3,4,5,6,7,8,9]

        for row_index in range(len(self._board._state)):
        	row_entries = self._board.get_row(row_index)
        	if not sorted(row_entries) == win_entries:
        		return False

        for col_index in range(len(self._board._state)):
        	col_entries = self._board.get_column(col_index)
        	if not sorted(col_entries) == win_entries:
        		return False

        for box_coord in [(0, 0), (3, 0), (6, 0), (0, 3), (3, 3), (6, 3), (0, 6), (3, 6), (6, 6)]: 
        	box_entries = self._board.get_box(box_coord[0], box_coord[1])
        	if not sorted(box_entries) == win_entries:
        		return False

        return True

    def print_board(self):
        "Prints the board using the board's print_board method"
        self._board.print_board()
    
    def set_permanency(self):
        "Returns an array of bool values that indicate whether a cell can't be removed. True if cell can't be removed"
        for row in range(len(self._board._state)):
            for col in range(len(self._board._state)):
                if self._board._state[row][col] != 0:
                    self._permanency[row][col] = True
    
    def _store_move(self, move_type: str, row: int, col: int, number: int):
        'Creates a Move namedtuple that stores information about the move for undo and redo. Type will be "add" or "remove" depending on what was done'
        move = Move(move_type, row, col, number)
        
        return move

    def _validate_move(self, type: str, row: int, col: int, number: int):
        '''
        Raises an exception if the given move is valid on the board.
        Needs to check:
            (1) Cell is within the board's bounds
            (2) Cell is not occupied
            (3) The move doesn't have any of the same entry in the same column, row, or box.
            (4) The number is valid (1-9)
        '''                
        if type in ['a', 'r']:
            if not self._valid_number(number):
                raise InvalidNumberError(number)
            
            elif not self._cell_in_bounds(row, col):
                raise CellOutOfBoundsError(row, col)
            
            elif self._cell_is_occupied(row, col):
                raise OccupiedCellError(row, col, self._board.get_cell(row,col))
    
            elif self._same_num_in_row(row, number):
                col_of_repeater = self._board.get_row(row).index(number)
                raise SameRowError(col, col_of_repeater, row, number)
            
            elif self._same_num_in_col(col, number):
                row_of_repeater = self._board.get_column(col).index(number)
                raise SameColumnError(row, row_of_repeater, col, number)
            
            elif self._same_num_in_box(row, col, number):
                raise SameBoxError(row, col, number)
        elif type == 'c':
            'Move is valid if cell is occupied'
            if not self._valid_number(number):
                raise InvalidNumberError(number)
            
            elif not self._cell_in_bounds(row, col):
                raise CellOutOfBoundsError(row, col)
            
            elif self._same_num_in_row(row, number):
                col_of_repeater = self._board.get_row(row).index(number)
                raise SameRowError(col, col_of_repeater, row, number)
            
            elif self._same_num_in_col(col, number):
                row_of_repeater = self._board.get_column(col).index(number)
                raise SameColumnError(row, row_of_repeater, col, number)
            
            elif self._same_num_in_box(row, col, number):
                raise SameBoxError(row, col, number)

    def _cell_is_occupied(self, row: int, col: int):
        'Returns a bool that indicates if a cell is occupied'
        return self._board._state[row][col] != 0

    def _cell_in_bounds(self, row: int, col: int):
        'Returns a bool that indicates if the given row and column are in the dimension of the board'

        return (0 <= row <= 8) and (0 <= col <= 8)

    def _same_num_in_row(self, row: int, number: int):
        'Returns a bool that indicates if the given number is already in the given row'
        return number in self._board.get_row(row)

    def _same_num_in_col(self, col: int, number: int):
        'Returns a bool that indicates if the given number is already in the given column'

        return number in self._board.get_column(col)

    def _same_num_in_box(self, row: int, col: int, number: int):
        'Returns a bool that indicates if the given number is already in the respective box of the given cell'

        return number in self._board.get_box(row, col)

    def _valid_number(self, number: int):
        'Returns a bool that indicates if the given number is valid'

        return 1 <= number <= 9

#ACTION OBJECTS

class Action:
    'Base class for all actions made in the game. Stores row, col, and num of action'
    
    def __init__(self, row, col):
        self._row = row
        self._col = col
    
    def get_coordinates(self):
        return self._row, self._col
    
    def get_old_num(self):
        return self._old_num
    
    def get_new_num(self):
        return self._new_num
    
    
class Add(Action):
    'Class for adding a number'
    
    def __init__(self, row, col, num):
        Action.__init__(self, row, col)
        self._new_num = num
        self._old_num = 0
    
class Remove(Action):
    'Class for removing a number'
    
    def __init__(self, row, col, old_num):
        Action.__init__(self, row, col)
        self._new_num = 0
        self._old_num = old_num 

class Change(Action):
    'Class for changing a non-permanent cell to a new number'
    
    def __init__(self, row, col, old_num, new_num):
        Action.__init__(self, row, col)
        self._old_num = old_num
        self._new_num = new_num

#EXCEPTIONS

class OccupiedCellError(Exception):
    'Exception for trying to make a move on an occupied cell.'
    def __init__(self, row, column, cell_value):
        message = 'OccupiedCellError: ({}, {}) is already occupied by the number {}.'
        super().__init__(message.format(row, column, cell_value))

class CellOutOfBoundsError(Exception):
    'Exception for giving coordinates that are outside of the board.'
    def __init__(self, row, column):
        message = 'CellOutOfBoundsError: ({}, {}) is out of bounds. Rows and Columns must be from 0-8.'
        super().__init__(message.format(row, column))

class SameRowError(Exception):
    'Exception for moves whose numbers have already been seen in the same row.'
    def __init__(self, col_of_move, col_of_repeater, row, number):
        message = 'SameRowError: ({}, {}) is in the same row as your move ({}, {}) and already contains the number {}.'
        super().__init__(message.format(row, col_of_repeater, row, col_of_move, number))

class SameColumnError(Exception):
    'Exception for moves whose numbers have already been seen in the same column.'
    def __init__(self, row_of_move, row_of_repeater, column, number):
        message = 'SameColumnError: ({}, {}) is in the same column as your move ({}, {}) and already contains the number {}.'
        super().__init__(message.format(row_of_repeater, column, row_of_move, column, number))

class SameBoxError(Exception):
    'Exception for moves whose numbers have already been seen in the same box.'
    def __init__(self, row, col, number):
        message = 'SameBoxError: The box that contains your move ({}, {}) already contains the number {}.'
        super().__init__(message.format(row, col, number))

class InvalidNumberError(Exception):
    'Exception for attempts to place an invalid number (any number not 1-9) in a cell'
    def __init__(self, number):
        message = '{} is not a valid number. Please enter a number from 1-9.'
        super().__init__(message.format(number))

class UndoError(Exception):
    'Exception for attempts to undo when there are no moves to undo'
    def __init__(self):
        super().__init__('UndoError: No moves available to undo')

class RedoError(Exception):
    'Exception for attempts to redo when there are no moves to redo'
    def __init__(self):
        super().__init__('RedoError: No moves available to redo')

class PermanencyError(Exception):
    'Exception for attempts to remove a number that is permanent in the game'
    def __init__(self, row, column):
        super().__init__('PermanencyError: Unable to remove the cell. ({}, {}) is permanent in the game.'.format(row,column))






if __name__ == '__main__':
    turn = 0

    game = Game()
    sudoku_pack = prompt.for_string('Choose the sudoku pack you want to use ',
                                    default='0', error_message='Not a valid sudoku pack.')
    sudoku_number = prompt.for_int('Choose the sudoku number you want to use ',
                                   default=0,error_message='Not a valid sudoku game in the pack.')
    game.load_state(os.path.join('sudoku_states', '{}_{:05d}'.format(sudoku_pack, sudoku_number)))
    game.set_permanency()

    print(CONTROLS)
    while True:
        try:
            print('TURN: {}'.format(turn))
            game.print_board()
            if game.check_victory():
                print('All cells filled! You win!')
                break
            else:
                move_type = prompt.for_string('Choose your move')
                if move_type == 'a':
                    cell = prompt.for_string('Enter move (e.g. add 3 to row 0 column 1 = 0 1 3)')
                    row, col, num = cell.split()
                    game.add_number(int(row),int(col),int(num))
                    turn += 1
                elif move_type == 'r':
                    cell = prompt.for_string('Enter move (e.g. remove row 0 column 1 = 0 1)')
                    row, col = cell.split()
                    game.remove_number(int(row),int(col))
                    turn += 1
                elif move_type == 'c':
                    cell = prompt.for_string('Enter move (e.g. change row 0 column 1 to number 3 = 0 1 3)')
                    row, col, num = cell.split()
                    game.change_number(int(row), int(col), int(num))
                    turn += 1
                elif move_type == '<':
                    game.undo_move()
                    turn += 1
                elif move_type == '>':
                    game.redo_move()
                    turn += 1
                else:
                    print('Not a valid move')
        except Exception as inst:
            print(inst)

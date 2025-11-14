from __future__ import annotations
from abc import ABC, abstractmethod
from chessington.engine.data import Player, Square
from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from chessington.engine.board import Board

class Piece(ABC):
    """
    An abstract base class from which all pieces inherit.
    """

    def __init__(self, player: Player):
        self.player = player

    def to_json(self) -> dict[str, Any]:
        return {
            "piece": self.__class__.__name__,
            "player": self.player._name_.lower()
        }

    @abstractmethod
    def get_available_moves(self, board: Board) -> List[Square]:
        """
        Get all squares that the piece is allowed to move to.
        """
        pass

    def move_to(self, board: Board, new_square):
        """
        Move this piece to the given square on the board.
        """
        current_square = board.find_piece(self)
        board.move_piece(current_square, new_square)


class Pawn(Piece):
    BOARD_MIN = 0
    BOARD_MAX = 7

    def get_available_moves(self, board: Board) -> list:
        current_square = board.find_piece(self)
        moves = []

        # Determine direction based on player
        direction = 1 if self.player == Player.WHITE else -1
        next_row = current_square.row + direction
        col = current_square.col

        # Move forward if square is empty
        if 0 <= next_row <= 7:
            forward_square = board.squares[next_row][col]
            if forward_square.is_empty():
                moves.append(forward_square)

        # Add diagonal captures
        for col_offset in [-1, 1]:
            new_col = col + col_offset
            if 0 <= new_col <= 7 and 0 <= next_row <= 7:
                diag_square = board.squares[next_row][new_col]
                if not diag_square.is_empty() and diag_square.piece.player != self.player:
                    moves.append(diag_square)

        return moves

    def promote_if_needed(self, board: Board):
        """
        Call this after the pawn moves. Promotes pawn to a queen automatically.
        """
        current_square = board.find_piece(self)
        # White promotion on row 7, Black promotion on row 0
        if (self.player == Player.WHITE and current_square.row == 7) or \
           (self.player == Player.BLACK and current_square.row == 0):
            # Replace pawn with a new Queen of same player
            board.squares[current_square.row][current_square.col].piece = Queen(self.player)



class Knight(Piece):
    """
    A class representing a chess knight.
    """
    BOARD_MIN = 0
    BOARD_MAX = 7

    # All possible L-shaped moves for a knight
    KNIGHT_MOVES = [
        (2, 1), (2, -1),
        (-2, 1), (-2, -1),
        (1, 2), (1, -2),
        (-1, 2), (-1, -2)
    ]

    def _is_on_board(self, row: int, col: int) -> bool:
        return self.BOARD_MIN <= row <= self.BOARD_MAX and self.BOARD_MIN <= col <= self.BOARD_MAX

    def get_available_moves(self, board: Board) -> list:
        """
        Returns a list of Squares the knight can move to.
        """
        current_square = board.find_piece(self)
        possible_moves = []

        for row_offset, col_offset in self.KNIGHT_MOVES:
            new_row = current_square.row + row_offset
            new_col = current_square.col + col_offset

            if self._is_on_board(new_row, new_col):
                square = board.squares[new_row][new_col]
                if square.is_empty() or square.piece.player != self.player:
                    possible_moves.append(square)

        return possible_moves



class Bishop(Piece):
    """
    A class representing a chess bishop.
    """

    BOARD_MIN = 0
    BOARD_MAX = 7

    #All possible moves for a bishop
    BISHOP_MOVES = {




    }


    def get_available_moves(self, board):
        return []


class Rook(Piece):
    """
    A class representing a chess rook.
    """

    def get_available_moves(self, board):
        return []


class Queen(Piece):
    """
    A class representing a chess queen.
    """

    def get_available_moves(self, board):
        return []


class King(Piece):
    """
    A class representing a chess king.
    """

    def get_available_moves(self, board):
        return []
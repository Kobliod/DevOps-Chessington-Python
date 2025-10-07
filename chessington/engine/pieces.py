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

    def _is_on_board(self, row: int, col: int) -> bool:
        return self.BOARD_MIN <= row <= self.BOARD_MAX and self.BOARD_MIN <= col <= self.BOARD_MAX

    def get_available_moves(self, board) -> list[Square]:
        current = board.find_piece(self)
        moves = []

        # Direction and starting row
        direction = -1 if self.player == Player.BLACK else 1
        start_row = 6 if self.player == Player.BLACK else 1

        # Forward moves
        forward_one_row = current.row + direction
        forward_two_row = current.row + 2 * direction

        if self._is_on_board(forward_one_row, current.col) and not board.get_piece(Square.at(forward_one_row, current.col)):
            moves.append(Square.at(forward_one_row, current.col))

            # Two-step forward from starting row
            if current.row == start_row and self._is_on_board(forward_two_row, current.col) and not board.get_piece(Square.at(forward_two_row, current.col)):
                moves.append(Square.at(forward_two_row, current.col))

        # Diagonal captures
        for col_offset in (-1, 1):
            diag_col = current.col + col_offset
            if not self._is_on_board(forward_one_row, diag_col):
                continue
            target_piece = board.get_piece(Square.at(forward_one_row, diag_col))
            if target_piece is not None and target_piece.player != self.player:
                moves.append(Square.at(forward_one_row, diag_col))

        return moves


class Knight(Piece):
    """
    A class representing a chess knight.
    """

    def get_available_moves(self, board):
        return []


class Bishop(Piece):
    """
    A class representing a chess bishop.
    """

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
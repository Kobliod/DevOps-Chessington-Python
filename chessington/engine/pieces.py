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
    """
    A class representing a chess pawn.
    """
    # board coordinates assumed 0..7 (standard 8x8)
    BOARD_MIN = 0
    BOARD_MAX = 7

    def _in_bounds(self, row: int, col: int) -> bool:
        return self.BOARD_MIN <= row <= self.BOARD_MAX and self.BOARD_MIN <= col <= self.BOARD_MAX

    def get_available_moves(self, board) -> List[Square]:
        current_square = board.find_piece(self)
        moves = []

        if self.player == Player.BLACK:
            # one step forward
            r1, c = current_square.row - 1, current_square.col
            if self._in_bounds(r1, c):
                one_step = Square.at(r1, c)
                if board.get_piece(one_step) is None:
                    moves.append(one_step)

                    # two-step from starting row (6 for black)
                    if current_square.row == 6:
                        r2 = current_square.row - 2
                        if self._in_bounds(r2, c):
                            two_step = Square.at(r2, c)
                            if board.get_piece(two_step) is None:
                                moves.append(two_step)

        else:  # Player.WHITE
            r1, c = current_square.row + 1, current_square.col
            if self._in_bounds(r1, c):
                one_step = Square.at(r1, c)
                if board.get_piece(one_step) is None:
                    moves.append(one_step)

                    # two-step from starting row (1 for white)
                    if current_square.row == 1:
                        r2 = current_square.row + 2
                        if self._in_bounds(r2, c):
                            two_step = Square.at(r2, c)
                            if board.get_piece(two_step) is None:
                                moves.append(two_step)

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
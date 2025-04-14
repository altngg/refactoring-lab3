from typing import Union
from uuid import UUID
from itertools import product


class ChessBoard():

    pieceList = []

    chessBoard = dict()

    def __init__(self) -> None:
        # Chessboard position as the key, the value will be the piece on it
        for letter in range(ord("a"), ord("h") + 1):
            for number in range(1, 9):
                position = chr(letter) + str(number)
                self.chessBoard[position] = None

    def addPieceToList(self, piece: dict) -> None:
        self.pieceList.append(piece)

    def addPieceToBoard(self, pieceId: UUID, position: str) -> Union[list, str]:

        position = position.lower()
        piece = dict()

        if position not in self.chessBoard.keys():
            return "INVALID POSITION"

        for value in self.chessBoard.values():
            if value is not None and value["id"] == pieceId:
                return "PIECE ALREADY ADDED TO THE BOARD"

        for p in self.pieceList:
            if p["id"] == pieceId:
                piece = p

        if len(piece) == 0:
            return "PIECE DOES NOT EXIST"

        if piece["type"] != "knight":
            # This will override any current piece on this position
            self.chessBoard[position] = piece
            return "PIECE ADDED"

        if piece["type"] == "knight":
            # This will override any current piece on this position
            results = self.checkKnightMovements(position, piece)
            self.chessBoard[position] = piece
            return results

        return "INVALID PIECE"

    def checkKnightMovements(self, position: str, piece: dict) -> list:

        validFirstMovements = self.validMoves(position, piece)

        validSecondMovements = []

        for move in validFirstMovements:
            validSecondMovements.extend(self.validMoves(move, piece))

        return validSecondMovements

    def validMoves(self, position: str, piece: dict) -> list:
        x, y = position
        x = ord(x) - ord('a')
        y = int(y)
        moves = list(product([x - 1, x + 1], [y - 2, y + 2])) + \
            list(product([x - 2, x + 2], [y - 1, y + 1]))
        moves = [(x, y)
                 for x, y in moves if x > 0 and y > 0 and x < 8 and y < 8]

        validMoves = []

        for move in moves:
            possiblePosition = chr(move[0] + ord('a')) + str(move[1])
            if self.chessBoard[possiblePosition] is None or self.chessBoard[possiblePosition]["color"] != piece["color"]:
                validMoves.append(possiblePosition)

        return validMoves

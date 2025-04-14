from typing import Union
from uuid import uuid4 as generateID


class ChessPiece():

    def __new__(self, type: str, color: str) -> Union[dict, str]:

        type = type.lower()
        color = color.lower()

        if type not in ("king", "queen", "rook", "bishop", "knight", "pawn"):
            return "INVALID PIECE TYPE"

        if color not in ("black", "white"):
            return "INVALID PIECE COLOR"

        self.type = type
        self.color = color
        self.id = generateID()

        return {"id": self.id, "type": self.type, "color": self.color}

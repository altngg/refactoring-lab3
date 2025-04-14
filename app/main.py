from .chessboard import ChessBoard
from .chesspiece import ChessPiece
from uuid import UUID
from fastapi import FastAPI, Response, status
from pymongo import MongoClient

board = ChessBoard()

app = FastAPI()

connectedToDababase = False

try:
    f = open("../mongopassword.txt", "r")
    user, password = f.read().split("\n")
    client = MongoClient(
        f"mongodb+srv://{user}:{password}@cluster0.4uknf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.chess
    connectedToDababase = True
except Exception:
    print("COULD NOT CONNECT TO DATABASE")


@app.post("/", status_code=status.HTTP_202_ACCEPTED)
def post_piece(pieceType: str, pieceColor: str, response: Response):
    piece = ChessPiece(pieceType, pieceColor)

    if type(piece) is dict:
        board.addPieceToList(piece)
        db.actions.insert_one({"New Piece Created": str(
            piece["id"])}) if connectedToDababase else None
        response.status_code = status.HTTP_201_CREATED
        return {"Id": piece["id"]}

    db.errors.insert_one({"error": piece}) if connectedToDababase else None
    response.status_code = status.HTTP_400_BAD_REQUEST
    return {"error": piece}


@app.put("/", status_code=status.HTTP_202_ACCEPTED)
def put_board(id: UUID, position: str, response: Response):
    result = board.addPieceToBoard(id, position)

    if type(result) is str:
        if result == "PIECE ADDED":
            db.actions.insert_one({"New Piece Added To Board": str(
                str(id) + "@" + position)}) if connectedToDababase else None
            response.status_code = status.HTTP_202_ACCEPTED
            return {"success": result}
        db.errors.insert_one(
            {"error": result}) if connectedToDababase else None
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": result}

    db.actions.insert_one({"Calculated Possible Locations": str(
        result)}) if connectedToDababase else None
    response.status_code = status.HTTP_200_OK
    return {"possibleLocations": result}

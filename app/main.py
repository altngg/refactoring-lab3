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
except Exception as e:
    print("COULD NOT CONNECT TO DATABASE")


@app.post("/", status_code=status.HTTP_202_ACCEPTED)
def post_piece(pieceType: str, pieceColor: str, response: Response):
    piece = ChessPiece(pieceType, pieceColor)

    if type(piece) is dict:
        board.addPieceToList(piece)
        if connectedToDababase:
            db.actions.insert_one({"New Piece Created": str(piece["id"])})
        response.status_code = status.HTTP_201_CREATED
        return {"Id": piece["id"]}

    if connectedToDababase:
        db.errors.insert_one({"error": piece})
    response.status_code = status.HTTP_400_BAD_REQUEST
    return {"error": piece}


@app.put("/", status_code=status.HTTP_202_ACCEPTED)
def put_board(id: UUID, position: str, response: Response):
    result = board.addPieceToBoard(id, position)

    if type(result) is str:
        if result == "PIECE ADDED":
            if connectedToDababase:
                db.actions.insert_one({"New Piece Added To Board": str(str(id) + "@" + position)})
            response.status_code = status.HTTP_202_ACCEPTED
            return {"success": result}
        if connectedToDababase:
            db.errors.insert_one({"error": result})
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": result}

    if connectedToDababase:
        db.actions.insert_one({"Calculated Possible Locations": str(result)})
    response.status_code = status.HTTP_200_OK
    return {"possibleLocations": result}
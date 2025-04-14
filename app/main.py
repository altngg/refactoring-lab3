from .chessboard import ChessBoard
from .chesspiece import ChessPiece
from uuid import UUID
from fastapi import FastAPI, Response, status
from pymongo import MongoClient

board = ChessBoard()

app = FastAPI()

connected_to_database = False

try:
    with open("../mongopassword.txt", "r") as f:
        user, password = f.read().split("\n")
    client = MongoClient(
        f"mongodb+srv://{user}:{password}@cluster0.4uknf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.chess
    connected_to_database = True
except Exception as e:
    print(f"COULD NOT CONNECT TO DATABASE: {str(e)}")

# вспомогательная функция для логирования в базу данных
def log_to_db(event_type: str, data: str):
    if connected_to_database:
        db.actions.insert_one({"type": event_type, "data": data})

@app.post(
        "/",
        status_code=status.HTTP_202_ACCEPTED,
        responses={
            201: {"description": "Piece successfully created"},
            400: {"description": "Invalid piece parameters"}
        }
        )
def create_piece(pieceType: str, pieceColor: str, response: Response):
    piece = ChessPiece(pieceType, pieceColor)

    if isinstance(piece, dict):
        board.addPieceToList(piece)
        log_to_db("PIECE_CREATED", str(piece["id"]))
        response.status_code = status.HTTP_201_CREATED
        return {"Id": piece["id"]}

    log_to_db("CREATION_ERROR", str(piece))
    response.status_code = status.HTTP_400_BAD_REQUEST
    return {"error": str(piece)}


@app.put(
        "/",
        status_code=status.HTTP_202_ACCEPTED,
        responses={
            200: {"description": "Possible locations calculated"},
            202: {"description": "Piece successfully placed on board"},
            400: {"description": "Invalid placement parameters"}
        }
        )
def update_piece_position(id: UUID, position: str, response: Response):
    result = board.addPieceToBoard(id, position)

    if isinstance(result, str):
        if result == "PIECE ADDED":
            log_to_db("PIECE_PLACED", f"{id}@{position}")
            response.status_code = status.HTTP_202_ACCEPTED
            return {"success": result}
        log_to_db("PLACEMENT_ERROR", result)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": result}

    log_to_db("POSSIBLE_MOVES_CALCULATED", str(result))
    response.status_code = status.HTTP_200_OK
    return {"possibleLocations": result}
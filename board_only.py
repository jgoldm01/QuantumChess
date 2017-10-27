# Quantum Chess
# 
# Steps for development:
# 1. create the python GUI
# 2. create the checkerboard of the gui
# 3. create each chess piece superimposed over the gui
# 4. show possible chess piece movement for each piece
# 4.5. include the 'check' mechanic
# 5. allow said movement with mouse clicks

import Tkinter
from enum import Enum

class ChessPiece(Enum):
  pawn = 'pawn'
  knight = 'knight'
  bishop = 'bishop'
  rook = 'rook'
  queen = 'queen'
  king = 'king'

class Side(Enum):
  white = 'white'
  black = 'black'

start_pos = {
  ChessPiece.rook: [0, 7],
  ChessPiece.knight: [1, 6],
  ChessPiece.bishop: [2, 5],
  ChessPiece.king: [3],
  ChessPiece.queen: [4],
  ChessPiece.pawn: range(8, 16),
}


class GameState:
  def __init__(self, root):
    self.board = Board(root, self.SmartSquarePress)
    self.pieces = self.GeneratePieces()
    self.selected_piece = None
    # self.turn = Side.White
    for piece in self.pieces:
      self.DisplayNewState(None, piece)

  def GeneratePieces(self):
    pieces = []
    for piece, positions in start_pos.iteritems():
      for pos in positions:
        pieces.append(Piece(pos, Side.white, piece))
        if piece == ChessPiece.king:
          pieces.append(Piece(59, Side.black, piece))
        if piece == ChessPiece.queen:
          pieces.append(Piece(60, Side.black, piece))
        else:
          pieces.append(Piece(63-pos, Side.black, piece))
    return pieces

  def DisplayNewState(self, former_pos, piece):
    # displays updated game state after a player has conducted a move.
    # todo: maybe we'll have to add something to remove deleted pieces
    # self.board.ResetBackground()
    if former_pos:
      self.board.ClearSquare(former_pos)
    self.board.RenderPiece(piece)

  def GetPieceAt(self, pos):
    for piece in self.pieces:
      if piece.pos == pos:
        return piece


  def SmartSquarePress(self, press_index):
    def SquarePress(event):
      self.board.ResetBackground()
      piece = self.GetPieceAt(press_index)
    return SquarePress


class Piece:
  def __init__(self, pos, side, kind):
    self.pos = pos
    self.side = side
    self.kind = kind

class Board:
  def __init__(self, root, callback):
    self.squares = []
    # a dict {int: str} of square indexes and former background colors for when new squares are pressed.
    for i in range(64):
      row = i/8 
      col = i%8
      background = 'gray88' if (row % 2 == col % 2) else 'saddle brown'
      square = Tkinter.Canvas(root, height=100, width=100, background=background,  highlightthickness=0)
      square.grid(row=row, column=col)
      square.bind("<ButtonPress>", callback(i))
      self.squares.append(square)

  def IsWhiteBackground(self, i):
    return True if ((i/8)  % 2 == (i%8) % 2) else False

  def ResetBackground(self):
    for i in range(64):
      background = 'gray88' if (self.IsWhiteBackground(i)) else 'saddle brown'
      self.squares[i].configure(background = background)

  def RenderPiece(self, piece):
    img = Tkinter.PhotoImage(file="images/%s_%s.gif" % (piece.kind, piece.side))
    self.squares[piece.pos].create_image(50, 50, image=img)
    self.squares[piece.pos].image = img

def main():
  root = Tkinter.Tk()
  b = GameState(root)
  root.mainloop()

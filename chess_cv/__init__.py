import game, cv
from Square import Square
import json

def start_game(orig, sobel):
    squares = cv.find_everything(orig, sobel)
    info = game.initialize_game(squares)
    fen = info['fen']
    output = {fen: fen, game_state: info}
    return json.encode(output)

    #GET FEN STRING SOMEHOW

    

def process_input(orig, sobel, board_state):
    squares = cv.find_everything(orig, sobal, board_state)
    

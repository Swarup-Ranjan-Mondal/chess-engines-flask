from flask import Flask, request, jsonify
import chess.engine
import chess

app = Flask(__name__)

engines = {
    'stockfish': chess.engine.SimpleEngine.popen_uci(
        'engines/stockfish_13/stockfish'
    ),
    'komodo': chess.engine.SimpleEngine.popen_uci(
        'engines/komodo_12/komodo'
    ),
    'critter': chess.engine.SimpleEngine.popen_uci(
        'engines/critter_1.6a/critter'
    ),
    'minkochess': chess.engine.SimpleEngine.popen_uci(
        'engines/minkochess_1.3/minkochess'
    ),
}

@app.route('/', methods=['POST'])
def engine_response():
    try:
        data = request.get_json()
        board = chess.Board(str(data['fen']))
        engine_name = str(data['engine_name'])
        result = engines[engine_name].play(
            board,
            chess.engine.Limit(time=0.1),
        )

        return jsonify(
            {
                'success': True,
                'engine_move': {
                    str(result.move):
                    board.san(chess.Move.from_uci(str(result.move)))
                },
            }
        ), 200

    except KeyError as ke:
        response = {'error': True}

        if 'fen' in str(ke) or 'engine_name' in str(ke):
            response['message'] = f"key {ke} is missing!"
        elif engine_name in str(ke):
            response['message'] = "chess engine name error!"
            response['description'] = f"no chess engine exists with the name: {ke}"
        else:
            response['message'] = str(ke)

        return jsonify(response), 400

    except ValueError as ve:
        return jsonify(
            {
                'error': True,
                'message': "fen is syntactically invalid!",
                'description': str(ve)
            }
        ), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
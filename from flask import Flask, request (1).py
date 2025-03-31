from flask import Flask, request

app = Flask(__name__)

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    direction = data.get('direction')
    # This could store or log a move command to be processed
    print(f"Received move command: {direction}")
    return {'status': 'success'}

if __name__ == '__main__':
    app.run(port=5000)

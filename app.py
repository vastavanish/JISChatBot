from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from driver import get_response
from update_model import update_chatbot

app = Flask(__name__)
CORS(app)

#app.debug = True


@app.get('/')
def get_index():
    return render_template('base.html')


@app.post('/predict')
def predict():
    text = request.get_json().get('message')
    # TODO : check if the text is valid or not
    response = get_response(text)
    message = {'answer': response}

    return jsonify(message)


@app.post('/updatemodel')
def updatemodel():
    text = request.get_json().get('message')
    response = update_chatbot(text)
    print(response)
    return jsonify({'response': response})


if __name__ == '__main__':
    app.run()

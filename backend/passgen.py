#!/usr/bin/python3


from flask import Flask, request, jsonify 
from flask_cors import CORS
import string
import random
import secrets

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET','POST'])
def complexgen():
        data = request.get_json()

        length = data.get('length')
        has_lower = data.get('hasLower')
        has_upper = data.get('hasUpper')
        has_digits = data.get('hasDigits')
        has_symbols = data.get('hasSymbols')
    
        char_list = ""

        if(has_lower):
            char_list += string.ascii_lowercase

        if(has_upper):
            char_list += string.ascii_uppercase

        if(has_digits):
            char_list += string.digits

        if(has_symbols):
            char_list += string.punctuation

        result = []

        for i in range (length):
            randomChar = secrets.choice(char_list)
            result.append(randomChar)

        password = "".join(result)
        return jsonify({'password': password})

if __name__ == "__main__":
    app.run(debug=True)

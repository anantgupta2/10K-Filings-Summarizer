from flask import Flask, render_template, request
from data_parser import *

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        processing_option = request.form['processing_option']
        llm_response = generate_insights(user_input.upper(), processing_option.lower())[0].text
        if llm_response:
            return render_template('index.html', user_input=user_input, llm_response = llm_response)
        else:
            return render_template('index.html', user_input=user_input)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
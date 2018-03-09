from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blank')
def camp():
    return render_template('blank.html')

@app.route('/charts')
def charts():
    return render_template('charts.html')

@app.route('/cards')
def cards():
    return render_template('cards.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0')

from flask import Flask, jsonify
app = Flask(__name__)


@app.route('/api')
def hello():
    print("hello world 55")
    return "Hello Flask-Heroku"



# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    app.run(debug=False)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

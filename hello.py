from flask import Flask , render_template
app = Flask(__name__)

@app.route('/')
@app.route('/hello')
def hello():
    return 'Hello, Kirigo Karanja!'

@app.route('/home')
def home():
    title = "My Name"
    application = {
        'heading': 'new intro to andela'
    }
    return render_template("home.html", name=title, application = application)

if __name__ == '__main__':
    app.run(debug=True)
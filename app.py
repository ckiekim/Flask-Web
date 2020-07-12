from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
@app.route('/grid')
def index():
    return render_template('grid.html')

@app.route('/container')
def container():
    return render_template('container.html')

@app.route('/list')
def list():
    return render_template('list.html')

@app.route('/navbar')
def navbar():
    return render_template('navbar.html')

@app.route('/jumbotron')
def jumbotron():
    return render_template('jumbotron.html')

@app.route('/bottom')
def bottom():
    return render_template('bottom.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
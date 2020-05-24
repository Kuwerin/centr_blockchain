from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mongoengine import *
from models import *

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {'DB': 'blockchain'}
db = MongoEngine(app)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        lender = request.form['lender']
        amount = request.form['amount']
        borrower = request.form['borrower']
        Block.objects.create(name=lender, amount=amount, to_whom=borrower)
        return redirect(url_for('index'))

    return render_template('index.html')


@app.route('/check')
def check():
    chain = Block.objects.all()
    results={}
    for block in chain:
        results[block.number] = block.check_integrity()
    return render_template('index.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)

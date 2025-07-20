from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = 'CHANGE_THIS_SECRET'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'secret':
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template('index.html')

@app.route('/home')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return '''
        <h2>Welcome to AJ Ricardo Apps</h2>
        <a href="http://localhost:8000">Launch ENGINE-AJ</a>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

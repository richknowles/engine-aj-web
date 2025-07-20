from flask import Flask
import engine_aj_web_demo as app_logic

app = Flask(__name__)

@app.route('/')
def home():
    return "ENGINE-AJ is Live"

@app.route('/run')
def run_main():
    return app_logic.main()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

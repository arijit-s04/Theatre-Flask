#!.venv/bin/python
from theatre import app

if __name__ == '__main__':
    print("Running...")
    app.run(debug=True, host='0.0.0.0')

import os, sys, importlib

# Ensure src is on path
SRC = os.path.join(os.path.dirname(__file__), 'src')
if SRC not in sys.path:
    sys.path.insert(0, SRC)

app = importlib.import_module('app')
application = app.create_app()

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=6868, debug=True)

from flask import Flask, render_template, request, url_for 
from threading import Thread, Lock
import logging
import sys 
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

import os , stat
mtx = Lock()

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('site.html')
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save("web/binary.bin")
      os.chmod( "web/binary.bin", stat.S_IRWXU | stat.S_IRWXO)
      mtx.release()
      return render_template('uploaded.html')
@app.route('/tm')
def tm():
    return render_template('tm.html'  )

def run_web():
    logging.getLogger('werkzeug').disabled = True
    

    app.run( debug=False, host="0.0.0.0", port=7100)

if __name__ == "__main__":
    app.run()
from app import app
from db_setup import init_db
from flask import Flask, render_template

init_db()

@app.route('/')
def test():
  return render_template("index.html")
  
if __name__ == '__main__':
  app.run()
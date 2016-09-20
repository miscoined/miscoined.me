from flask import Flask
app = Flask(__name__)

@app.route("/")
def placeholder():
  return "Work in progress!"

if __name__ == "__main__":
  app.run()

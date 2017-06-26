from flask import Flask


# Flask object
app = Flask(__name__)

# route
@app.route('/')
def show_entries():
    return "show entries"

# entry point
if __name__ == "__main__":
    app.run(host='0.0.0.0')
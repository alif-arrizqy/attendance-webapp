from flask import Flask

app = Flask(__name__)
from views import views
app.secret_key = '83dcdc455025cedcfe64b21e620564fb'
app.register_blueprint(views, url_prefix="/")

if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=8080, debug=True, threaded=True)
    app.run()


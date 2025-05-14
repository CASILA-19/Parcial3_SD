from flask import Flask
from api.routes import booking_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(booking_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)

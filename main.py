from flask import Flask
from app.db import db
from app.routes.auth import auth_bp
from app.models.user import User  # Make sure this import exists!
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # Allow all origins by default

app.config.from_object('app.config.Config')

db.init_app(app)
app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure tables are created

        # ✅ Insert test user
        existing_user = User.query.filter_by(username="test_user").first()
        if not existing_user:
            new_user = User(
             username="test_user",
              userlevel="ADMIN"
            )
            new_user.set_password("test_password")
            db.session.add(new_user)
            db.session.commit()
            print("✅ Test user created.")
        else:
            print("ℹ️ Test user already exists.")
            
            import sys
            sys.stdout.flush()
    
    # Move the app.run() outside the app context
    app.run(debug=True)

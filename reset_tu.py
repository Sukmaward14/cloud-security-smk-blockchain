from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():

    user = User.query.filter_by(username="tu").first()

    if user:
        user.password = generate_password_hash("tu123")
        user.role = "tu"

        db.session.commit()

        print("Password akun TU berhasil direset.")
        print("Username: tu")
        print("Password: tu123")

    else:
        user = User(
            username="tu",
            password=generate_password_hash("tu123"),
            role="tu"
        )

        db.session.add(user)
        db.session.commit()

        print("Akun TU berhasil dibuat.")
        print("Username: tu")
        print("Password: tu123")
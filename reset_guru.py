from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():

    user = User.query.filter_by(username="guru").first()

    if user:
        user.password = generate_password_hash("guru123")
        user.role = "guru"

        db.session.commit()

        print("Password akun Guru berhasil direset.")
        print("Username: guru")
        print("Password: guru123")

    else:
        user = User(
            username="guru",
            password=generate_password_hash("guru123"),
            role="guru"
        )

        db.session.add(user)
        db.session.commit()

        print("Akun Guru berhasil dibuat.")
        print("Username: guru")
        print("Password: guru123")
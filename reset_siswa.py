from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():

    user = User.query.filter_by(username="siswa").first()

    if user is None:
        print("User siswa tidak ditemukan.")
    else:
        user.password = generate_password_hash("siswa123")
        db.session.commit()

        print("Password siswa berhasil direset.")
        print("Username : siswa")
        print("Password : siswa123")
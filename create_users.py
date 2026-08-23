from app import app, db, User
from werkzeug.security import generate_password_hash


users = [
    {
        "username": "siswa",
        "password": "siswa123",
        "role": "siswa"
    },
    {
        "username": "guru",
        "password": "guru123",
        "role": "guru"
    },
    {
        "username": "tu",
        "password": "tu123",
        "role": "tu"
    },
    {
        "username": "kepala",
        "password": "kepala123",
        "role": "kepala_sekolah"
    },
    {
        "username": "dudi",
        "password": "dudi123",
        "role": "dudi"
    }
]


with app.app_context():

    db.create_all()

    for data in users:

        existing = User.query.filter_by(
            username=data["username"]
        ).first()

        if existing:
            continue

        user = User(

            username=data["username"],

            password=generate_password_hash(
                data["password"]
            ),

            role=data["role"]

        )

        db.session.add(user)

    db.session.commit()

    print("User berhasil dibuat.")
    
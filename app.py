from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import os
import hashlib
import uuid
from blockchain import (
    register_document_on_blockchain,
    get_document_from_blockchain
)

app = Flask(__name__)

# =========================
# KONFIGURASI
# =========================

app.config["SECRET_KEY"] = "cloud-security-smk-secret"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# =========================
# KONFIGURASI UPLOAD
# =========================

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(__file__),
    "uploads"
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

db = SQLAlchemy(app)

os.makedirs(
    app.config["UPLOAD_FOLDER"],
    exist_ok=True
)

# =========================
# MODEL USER
# =========================

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(30),
        nullable=False
    )


# =========================
# MODEL SISWA
# =========================

class Student(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nis = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    class_name = db.Column(
        db.String(50),
        nullable=False
    )


# =========================
# MODEL NILAI
# =========================

class Grade(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id"),
        nullable=False
    )

    subject = db.Column(
        db.String(100),
        nullable=False
    )

    score = db.Column(
        db.Float,
        nullable=False
    )

    teacher = db.Column(
        db.String(100),
        nullable=False
    )

# =========================
# MODEL DOKUMEN
# =========================

class Document(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id"),
        nullable=False
    )

    document_type = db.Column(
        db.String(50),
        nullable=False
    )

    filename = db.Column(
        db.String(255),
        nullable=False
    )

    file_hash = db.Column(
        db.String(64),
        nullable=False
    )

    uploaded_by = db.Column(
        db.String(100),
        nullable=False
    )

# =========================
# DECORATOR LOGIN
# =========================

def login_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:

            return redirect("/login")

        return function(*args, **kwargs)

    return wrapper


# =========================
# DECORATOR ROLE
# =========================

def role_required(*allowed_roles):

    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):

            if "user_id" not in session:

                return redirect("/login")

            user = db.session.get(
                User,
                session["user_id"]
            )

            if user is None:

                session.clear()

                return redirect("/login")

            if user.role not in allowed_roles:

                flash(
                    "Anda tidak memiliki hak akses.",
                    "danger"
                )

                return redirect("/dashboard")

            return function(*args, **kwargs)

        return wrapper

    return decorator


# =========================
# HALAMAN LOGIN
# =========================

@app.route("/")
def index():

    if "user_id" in session:

        return redirect("/dashboard")

    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        user = User.query.filter_by(
            username=username
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            session["user_id"] = user.id

            session["username"] = user.username

            session["role"] = user.role

            return redirect("/dashboard")

        flash(
            "Username atau password salah.",
            "danger"
        )

    return render_template("login.html")


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

# =========================
# HAPUS DOKUMEN
# =========================

@app.route("/documents/delete/<int:document_id>", methods=["POST"])
@role_required("tu")
def delete_document(document_id):

    document = db.session.get(
        Document,
        document_id
    )

    if document is None:

        flash(
            "Dokumen tidak ditemukan.",
            "danger"
        )

        return redirect("/documents")

    # =========================
    # HAPUS FILE FISIK
    # =========================

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        document.filename
    )

    if os.path.exists(file_path):

        os.remove(file_path)

    # =========================
    # HAPUS DATA DATABASE
    # =========================

    db.session.delete(document)

    db.session.commit()

    flash(
        "Dokumen berhasil dihapus.",
        "success"
    )

    return redirect("/documents")

# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")
@login_required
def dashboard():

    students_count = Student.query.count()

    grades_count = Grade.query.count()

    return render_template(
        "dashboard.html",
        students_count=students_count,
        grades_count=grades_count
    )


# =========================
# DATA SISWA
# =========================

@app.route("/students")
@login_required
def students():

    data = Student.query.all()

    return render_template(
        "students.html",
        students=data
    )


# =========================
# TAMBAH SISWA
# =========================

@app.route("/students/add", methods=["POST"])
@role_required("tu")
def add_student():

    nis = request.form["nis"]

    name = request.form["name"]

    class_name = request.form["class_name"]

    existing = Student.query.filter_by(
        nis=nis
    ).first()

    if existing:

        flash(
            "NIS sudah digunakan.",
            "danger"
        )

        return redirect("/students")

    student = Student(

        nis=nis,

        name=name,

        class_name=class_name

    )

    db.session.add(student)

    db.session.commit()

    flash(
        "Data siswa berhasil ditambahkan.",
        "success"
    )

    return redirect("/students")


# =========================
# DATA NILAI
# =========================

@app.route("/grades")
@login_required
def grades():

    data = Grade.query.all()

    return render_template(
        "grades.html",
        grades=data
    )

# =========================
# DATA DOKUMEN
# =========================

@app.route("/documents")
@login_required
def documents():

    data = Document.query.all()

    students = Student.query.all()

    return render_template(
        "documents.html",
        documents=data,
        students=students
    )


# =========================
# UPLOAD DOKUMEN
# =========================

@app.route("/documents/upload", methods=["POST"])
@role_required("tu")
def upload_document():

    student_id = request.form["student_id"]

    document_type = request.form["document_type"]

    file = request.files.get("file")

    if not file or file.filename == "":
        flash(
            "File belum dipilih.",
            "danger"
        )
        return redirect("/documents")

    if not file.filename.lower().endswith(".pdf"):
        flash(
            "Dokumen harus berupa file PDF.",
            "danger"
        )
        return redirect("/documents")

    # =========================
    # NAMA FILE ASLI
    # =========================

    original_filename = secure_filename(
        file.filename
    )

    # =========================
    # MEMBUAT NAMA FILE UNIK
    # =========================

    unique_filename = (
        uuid.uuid4().hex
        + "_"
        + original_filename
    )

    # =========================
    # LOKASI FILE
    # =========================

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        unique_filename
    )

    # =========================
    # SIMPAN FILE
    # =========================

    file.save(file_path)

    # =========================
    # HITUNG SHA-256
    # =========================

    file_hash = calculate_sha256(
        file_path
    )

    # =========================
    # SIMPAN KE DATABASE
    # =========================

    document = Document(
        student_id=int(student_id),
        document_type=document_type,
        filename=unique_filename,
        file_hash=file_hash,
        uploaded_by=session["username"]
    )

    db.session.add(document)

    db.session.commit()

    # =========================
    # SIMPAN HASH KE BLOCKCHAIN
    # =========================

    transaction_hash = register_document_on_blockchain(
        document.id,
        document.file_hash
    )

    if transaction_hash:

        flash(
            "Dokumen berhasil diupload dan hash berhasil disimpan ke blockchain.",
            "success"
        )

    else:

        flash(
            "Dokumen berhasil diupload, tetapi gagal disimpan ke blockchain.",
            "warning"
        )

    return redirect("/documents")
# =========================
# VERIFIKASI INTEGRITAS DOKUMEN
# =========================


@app.route("/documents/verify/<int:document_id>")
@login_required
def verify_document(document_id):

    # Ambil data dokumen dari database
    document = db.session.get(Document, document_id)

    if document is None:
        flash("Dokumen tidak ditemukan.", "danger")
        return redirect("/documents")

    # Lokasi file
    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        document.filename
    )

    # Pastikan file masih ada
    if not os.path.exists(file_path):
        flash("File dokumen tidak ditemukan.", "danger")
        return redirect("/documents")

    # Hitung ulang SHA-256 file
    current_hash = calculate_sha256(file_path)

    # Ambil hash dari blockchain
    blockchain_data = get_document_from_blockchain(document.id)

    if blockchain_data is None:
        flash("Blockchain tidak dapat diakses.", "danger")
        return redirect("/documents")

    blockchain_hash = blockchain_data["document_hash"]
    print("========== DEBUG VERIFIKASI ==========")
    print("Document ID:", document.id)
    print("Current Hash :", current_hash)
    print("Blockchain Hash:", blockchain_hash)
    print("Hash Sama?:", current_hash == blockchain_hash)
    print("======================================")
    
    # Bandingkan hash
    if current_hash == blockchain_hash:
        flash("DOKUMEN VALID - Hash sesuai dengan blockchain.", "success")
    else:
        flash("DOKUMEN TIDAK VALID - Hash berbeda dengan blockchain.", "danger")

    return redirect("/documents")

    # =========================
    # AMBIL HASH DARI BLOCKCHAIN
    # =========================
    blockchain_data = get_document_from_blockchain(document.id)

    if blockchain_data is None:
        flash("Blockchain tidak dapat diakses.", "danger")
        return redirect("/documents")

    blockchain_hash = blockchain_data["document_hash"]

    if current_hash == blockchain_hash:
        flash("DOKUMEN VALID - Hash sesuai dengan blockchain.", "success")
    else:
        flash("DOKUMEN TIDAK VALID - Hash berbeda dengan blockchain.", "danger")

    return redirect("/documents")

    # =========================
    # BANDINKAN HASH
    # =========================

    if current_hash == blockchain_hash:

        flash(
            "DOKUMEN VALID - Hash sesuai dengan blockchain.",
            "success"
        )

    else:

        flash(
            "DOKUMEN TIDAK VALID - Hash berbeda dengan blockchain.",
            "danger"
        )
        
# =========================
# TAMBAH NILAI
# =========================

@app.route("/grades/add", methods=["POST"])
@role_required("guru", "tu")
def add_grade():

    student_id = request.form["student_id"]

    subject = request.form["subject"]

    score = request.form["score"]

    teacher = session["username"]

    grade = Grade(

        student_id=student_id,

        subject=subject,

        score=float(score),

        teacher=teacher

    )

    db.session.add(grade)

    db.session.commit()

    flash(
        "Nilai berhasil ditambahkan.",
        "success"
    )

    return redirect("/grades")

# =========================
# FUNGSI SHA-256
# =========================

def calculate_sha256(file_path):

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:

        while True:

            data = file.read(4096)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()

# =========================
# MEMBUAT DATABASE
# =========================

with app.app_context():

    db.create_all()


# =========================
# MENJALANKAN SERVER
# =========================

if __name__ == "__main__":

    app.run(
        debug=True
    )
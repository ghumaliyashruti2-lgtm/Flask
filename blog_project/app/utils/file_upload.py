import os
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):

    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_profile_picture(file):

    filename = secure_filename(file.filename)

    upload_folder = os.path.join(
        current_app.root_path,
        "static/images/profile_picture"
    )

    os.makedirs(upload_folder, exist_ok=True)

    filepath = os.path.join(upload_folder, filename)

    file.save(filepath)

    return filename


def delete_profile_picture(filename):

    image_path = os.path.join(
        current_app.root_path,
        "static/images/profile_picture",
        filename
    )

    if os.path.exists(image_path):
        os.remove(image_path)
        

def save_profile_picture(file):

    filename = secure_filename(file.filename)

    upload_folder = os.path.join(
        current_app.root_path,
        "static/images/profile_picture"
    )

    os.makedirs(upload_folder, exist_ok=True)

    filepath = os.path.join(upload_folder, filename)

    file.save(filepath)

    return filename
from flask import Blueprint, request, send_file, current_app, jsonify
from PIL import Image, ImageOps
from io import BytesIO
# from uuid import uuid4
from deta import Deta
from os import getcwd, listdir

bp = Blueprint("deta_photo", __name__)


def photo_drive():
    return Deta(current_app.config["DETA_KEY"]).Drive("astra")


# def upload(photo, type_, file_name):
# def upload(photo, v, width=512, height=512):
    # file_name = f"{uuid4().hex}.jpg"
    # photo_byte = BytesIO()

    # if v != "item":
    # photo = Image.open(photo).convert('RGBA')
    # white = Image.new('RGBA', photo.size, (255, 255, 255))
    # photo = Image.alpha_composite(white, photo).convert('RGB')
    # photo = ImageOps.fit(photo, (width, height), Image.ANTIALIAS)

    # photo.save(photo_byte, format="JPEG")
    # else:
    # photo.save(photo_byte)

    # photo_drive().put(f"{type_}/{file_name}", photo_byte.getvalue())
    # return file_name


# def remove(photo, type_):
#     return photo_drive().delete(f"{type_}/{photo}")


@bp.get("/photo/<type_>/<photo>")
def get(type_, photo):

    thumbnail = False
    if type_ == "item_thumbnail":
        type_ = "item"
        thumbnail = True

    photo_file = photo_drive().get(f"{type_}/{photo}")

    if thumbnail:
        temp = Image.open(BytesIO(photo_file.read()))
        temp = ImageOps.fit(temp, (512, 512), Image.ANTIALIAS)

        photo_file = BytesIO()
        temp.save(photo_file, format="JPEG")
        photo_file.seek(0)

    return send_file(photo_file, mimetype="image/jpg")


def upload(source, dest):
    # photo = Image.open(photo).convert('RGBA')
    photo = Image.open(source)
    photo_byte = BytesIO()
    photo.save(photo_byte, format="PNG")
    photo_drive().put(dest, photo_byte.getvalue())


def photo_url(photo, type_):
    return f"{request.host_url}photo/{type_}/{photo}"


@bp.post("/photo")
def post():
    base = f"{getcwd()}/assets"

    def one(gender, att):
        path = f"{gender}/{att}"

        for filename in listdir(f"{base}/{path}"):
            source = f"{base}/{path}/{filename}"

            filename = filename.split("#")[0]
            filename = f"{filename}.png"
            dest = f"{path}/{filename}"
            upload(source, dest)

    attrubutes = ["accessory", "attire", "back_accessory",
                  "hairstyle", "headgear", "skin_tone"]

    for att in attrubutes:
        one("male", att)
    # for att in attrubutes:
    #     one("female", att)
    # one("background", "")

    return jsonify({
        "status": 200,
        "message": "ok"
    })

from flask import Blueprint, send_file, jsonify
from PIL import Image, ImageOps
from os import path, getcwd, mkdir
import json
from io import BytesIO

bp = Blueprint("photo", __name__)


def generate_photo(meta):

    asset_path = f"{getcwd()}/assets"

    ethnicity = Image.open(
        f"{asset_path}/{meta['gender']}/ethnicity/{meta['ethnicity']}")
    nose = Image.open(
        f"{asset_path}/{meta['gender']}/nose/{meta['ethnicity'].split('.')[0]}/{meta['nose']}")
    eye = Image.open(f"{asset_path}/{meta['gender']}/eye/{meta['eye']}")
    eyebrow = Image.open(
        f"{asset_path}/{meta['gender']}/eyebrow/{meta['eyebrow']}")
    mouth = Image.open(
        f"{asset_path}/{meta['gender']}/mouth/{meta['mouth']}")
    costume = Image.open(
        f"{asset_path}/{meta['gender']}/costume/{meta['costume']}")
    hair = Image.open(f"{asset_path}/{meta['gender']}/hair/{meta['hair']}")

    hair_back = None
    hair_back_name = meta['hair'].split(".")
    hair_back_name = f"{hair_back_name[0]}_back.{hair_back_name[1]}"
    hair_back_path = f"{asset_path}/{meta['gender']}/hair/{hair_back_name}"
    if path.exists(hair_back_path):
        hair_back = Image.open(hair_back_path)

    background = Image.open(f"{asset_path}/background/{meta['background']}")

    photo = Image.alpha_composite(ethnicity, nose)
    photo = Image.alpha_composite(photo, eye)
    photo = Image.alpha_composite(photo, eyebrow)
    photo = Image.alpha_composite(photo, mouth)
    photo = Image.alpha_composite(photo, costume)
    photo = Image.alpha_composite(photo, hair)
    if hair_back:
        photo = Image.alpha_composite(hair_back, photo)
    photo = Image.alpha_composite(background, photo)

    return photo


@bp.get("/build_collection")
def build_collection():

    output = f"{getcwd()}/static"

    with open(f"{output}/meta.json") as f:
        data = json.load(f)

    output = f"{getcwd()}/static"
    if not path.exists(output):
        mkdir(output)

    for x in data:
        photo = generate_photo(x)
        photo.save(f"{output}/{x['id']}.png")

    return jsonify({
        "status": 200,
        "message": "ok"
    })


@bp.get("/photo/<id>")
@bp.get("/photo/<id>/<thumbnail>")
def photo(id, thumbnail=False):

    output = f"{getcwd()}/static"

    with open(f"{output}/meta.json") as f:
        data = json.load(f)

    meta = None
    for i in data:
        if i["id"] == int(id):
            meta = i
            break

    if not meta:
        return jsonify({
            "status": 401,
            "message": "invalid request",
        })

    photo = generate_photo(meta)

    if thumbnail:
        x = 5
        width = int(1000/x)
        height = int(1200/x)
        photo = ImageOps.fit(photo, (width, height), Image.ANTIALIAS)

    photo_file = BytesIO()
    photo.save(photo_file, format="PNG")
    photo_file.seek(0)
    return send_file(photo_file, mimetype="image/png")

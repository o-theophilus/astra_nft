from flask import Blueprint, send_file, jsonify
from PIL import Image, ImageOps
from os import path, getcwd, mkdir
import json
from io import BytesIO

bp = Blueprint("photo", __name__)


def generate_photo(meta):
    """Build photos"""

    asset_path = f"{getcwd()}/assets"

    skin_tone = Image.open(
        f"{asset_path}/{meta['gender']}/skin_tone/{meta['skin_tone']}")
    hair_style = Image.open(
        f"{asset_path}/{meta['gender']}/hair_style/{meta['hair_style']}")
    cloth = Image.open(
        f"{asset_path}/{meta['gender']}/cloth/{meta['cloth']}")
    earring = Image.open(
        f"{asset_path}/{meta['gender']}/earring/{meta['earring']}")
    eye_glass = Image.open(
        f"{asset_path}/{meta['gender']}/eye_glass/{meta['eye_glass']}")
    necklace = Image.open(
        f"{asset_path}/{meta['gender']}/necklace/{meta['necklace']}")
    face_mask = Image.open(
        f"{asset_path}/{meta['gender']}/face_mask/{meta['face_mask']}")
    head_gear = Image.open(
        f"{asset_path}/{meta['gender']}/head_gear/{meta['head_gear']}")
    back_accessory = Image.open(
        f"{asset_path}/{meta['gender']}/back_accessory/{meta['back_accessory']}")
    background = Image.open(
        f"{asset_path}/background/{meta['background']}").convert(mode="RGBA")

    # size = 100
    # skin_tone = ImageOps.fit(skin_tone, (size, size), Image.ANTIALIAS)
    # hair_style = ImageOps.fit(hair_style, (size, size), Image.ANTIALIAS)
    # cloth = ImageOps.fit(cloth, (size, size), Image.ANTIALIAS)
    # earring = ImageOps.fit(earring, (size, size), Image.ANTIALIAS)
    # eye_glass = ImageOps.fit(eye_glass, (size, size), Image.ANTIALIAS)
    # necklace = ImageOps.fit(necklace, (size, size), Image.ANTIALIAS)
    # face_mask = ImageOps.fit(face_mask, (size, size), Image.ANTIALIAS)
    # head_gear = ImageOps.fit(head_gear, (size, size), Image.ANTIALIAS)
    # back_accessory = ImageOps.fit(back_accessory, (size, size), Image.ANTIALIAS)
    # background = ImageOps.fit(background, (size, size), Image.ANTIALIAS)

    photo = Image.alpha_composite(skin_tone, hair_style)
    photo = Image.alpha_composite(photo, cloth)
    photo = Image.alpha_composite(photo, earring)
    photo = Image.alpha_composite(photo, eye_glass)
    photo = Image.alpha_composite(photo, necklace)
    photo = Image.alpha_composite(photo, face_mask)
    photo = Image.alpha_composite(photo, head_gear)
    photo = Image.alpha_composite(back_accessory, photo)
    photo = Image.alpha_composite(background, photo)

    # items = [
    #     # "skin_tone",
    #     "hair_style",
    #     "cloth",
    #     "earring",
    #     "eye_glass",
    #     "necklace",
    #     "face_mask",
    #     "head_gear",
    #     # "back_accessory",
    #     # "background"
    # ]

    # # size = 100

    # file = Image.open(
    #     f"{asset_path}/{meta['gender']}/skin_tone/{meta['skin_tone']}")
    # # file = ImageOps.fit(file, (size, size), Image.ANTIALIAS)
    # photo = Image.alpha_composite(file, file)

    # for x in items:
    #     file = Image.open(
    #         f"{asset_path}/{meta['gender']}/{x}/{meta[x]}")
    #     # file = ImageOps.fit(file, (size, size), Image.ANTIALIAS)
    #     photo = Image.alpha_composite(photo, file)

    return photo


@bp.get("/build_collection")
def build_collection():
    """Save from meta.json to folder"""

    output = f"{getcwd()}/static"

    with open(f"{output}/meta.json") as f:
        data = json.load(f)

    output = f"{getcwd()}/static/images"
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
    """Return photo to frontend"""

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
        height = int(1000/x)
        photo = ImageOps.fit(photo, (width, height), Image.ANTIALIAS)

    photo_file = BytesIO()
    photo.save(photo_file, format="PNG")
    photo_file.seek(0)
    return send_file(photo_file, mimetype="image/png")

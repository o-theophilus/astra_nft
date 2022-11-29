from flask import Blueprint, send_file, jsonify
from PIL import Image, ImageOps
from os import path, getcwd, mkdir, listdir
import json
from io import BytesIO

bp = Blueprint("photo", __name__)


def generate_photo(meta):
    """Build photos"""

    def get_v(v, bg=False):
        if meta[v] != "none":
            asset_path = f"{getcwd()}/assets/{meta['gender']}/{v}"
            if bg:
                asset_path = f"{getcwd()}/assets/background"

            for img_name in listdir(asset_path):
                if img_name.split("#")[0] == meta[v]:
                    photo = Image.open(f"{asset_path}/{img_name}")
        else:
            photo = Image.new('RGBA', (2000, 2000), (0, 0, 0, 0))
        return photo

    photo = Image.alpha_composite(get_v("skin_tone"), get_v("hairstyle"))
    if (
        meta['gender'] == "female"
        and meta['attire'] in [
            "astra attire 24", "astra attire 21", "astra attire 35"]
        or meta['gender'] == "male"
        and meta['attire'] in ["astra attire 24", "astra attire 25"]
    ):
        photo = Image.alpha_composite(photo, get_v("headgear"))
        photo = Image.alpha_composite(photo, get_v("attire"))
        photo = Image.alpha_composite(photo, get_v("accessory"))
    elif (
        meta['gender'] == "male"
        and meta['headgear'] in ["blackasspke red", "focus mask",
                                 "helmetenticls", "memask",
                                 "punkhelmet", "whyeemaskt"]
        and meta['accessory'] in ["astra accessory 2", "astra accessory 3",
                                  "astra accessory 4"]
        or meta['gender'] == "female"
        and meta['headgear'] in ["gob mask", "mask"]
        and meta['accessory'] == "white pearrl neclace"
    ):
        photo = Image.alpha_composite(photo, get_v("attire"))
        photo = Image.alpha_composite(photo, get_v("accessory"))
        photo = Image.alpha_composite(photo, get_v("headgear"))
    else:
        photo = Image.alpha_composite(photo, get_v("attire"))
        photo = Image.alpha_composite(photo, get_v("headgear"))
        photo = Image.alpha_composite(photo, get_v("accessory"))
    photo = Image.alpha_composite(get_v("back_accessory"), photo)
    photo = Image.alpha_composite(
        get_v("background", True).convert(mode="RGBA"), photo)

    return photo


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


@bp.get("/build_collection")
def save_photo_to_folder():
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

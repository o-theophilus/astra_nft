from flask import Blueprint, jsonify, request, send_file
from os import getcwd
import json
from math import ceil
from PIL import Image, ImageOps
from io import BytesIO
from .tools import generate_photo

bp = Blueprint("urls", __name__)


@bp.get("/nft")
def get_all():
    output = f"{getcwd()}/static"

    with open(f"{output}/meta.json") as f:
        data = json.load(f)

    male = 0
    female = 0
    filter = {}
    for x in data:
        if x["gender"] == "male":
            male += 1
        else:
            female += 1

        for y in x:
            if y in ["rarity", "id"]:
                continue
            elif y not in filter:
                filter[y] = []

            if x[y] not in filter[y]:
                filter[y].append(x[y])

    page_no = 1
    if "page" in request.args:
        page_no = int(request.args["page"])

    fk = None
    fv = None
    if "filter" in request.args:
        fk, fv = request.args["filter"].split("700")

    if fk and fv:
        data = [x for x in data if x[fk].lower() == fv.lower()]

    page_size = 100
    total_page = ceil(len(data) / page_size)

    start = (page_no - 1) * page_size
    stop = start + page_size
    data = data[start: stop]

    return jsonify({
        "status": 200,
        "metas": data,
        "total_page": total_page,
        "filter": filter,
        "count": {
            "male": male,
            "female": female
        }
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

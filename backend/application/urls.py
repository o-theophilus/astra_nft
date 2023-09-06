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
    for nft in data:
        if nft["gender"] == "male":
            male += 1
        else:
            female += 1

        for ppt in nft:
            if ppt in ["rarity", "id"]:
                continue
            elif ppt not in filter:
                filter[ppt] = []

            if nft[ppt] not in filter[ppt]:
                filter[ppt].append(nft[ppt])

    page_no = 1
    if "page_no" in request.args:
        page_no = int(request.args["page_no"])
    fk1 = None
    if "fk1" in request.args:
        fk1 = request.args["fk1"]
    fv1 = None
    if "fv1" in request.args:
        fv1 = request.args["fv1"]

    if fk1 and fv1:
        data = [x for x in data if x[fk1].lower() == fv1.lower()]

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
        "nft_count": {
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

    scale = 1000
    if thumbnail:
        scale = 200

    photo = ImageOps.fit(photo, (scale, scale), Image.LANCZOS)

    photo_file = BytesIO()
    photo.save(photo_file, format="PNG")
    photo_file.seek(0)
    return send_file(photo_file, mimetype="image/png")

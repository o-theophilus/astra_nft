from flask import Blueprint, jsonify, request
from os import getcwd
import json
from math import ceil

bp = Blueprint("nft", __name__)


@bp.get("/nft")
def get_all():

    output = f"{getcwd()}/static"

    with open(f"{output}/meta.json") as f:
        data = json.load(f)

    page_no = request.args.get("page")
    if not page_no:
        page_no = 1
    page_no = int(page_no)

    page_size = 50
    total_page = ceil(len(data) / page_size)

    start = (page_no - 1) * page_size
    stop = start + page_size
    data = data[start: stop]

    _temp = []
    for i in data:
        m = {}
        for key, value in i.items():
            if type(value) == str:
                m[key] = value.split("#")[0]
            else:
                m[key] = value
        _temp.append(m)

    data = _temp

    return jsonify({
        "status": 200,
        "message": "ok",
        "data": {
            "metas": data,
            "total_page": total_page
        }
    })


@bp.get("/nft/<id>")
def get(id):

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

    return jsonify({
        "status": 200,
        "message": "ok",
        "data": meta
    })

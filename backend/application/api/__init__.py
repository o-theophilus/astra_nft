from flask import Blueprint, jsonify
from os import getcwd, listdir, path, mkdir
import json
import re
from random import randrange, shuffle, sample
import time

bp = Blueprint("api", __name__)


@bp.get("/")
def index():
    return jsonify({
        "status": 200,
        "message": "Welcome"
    })


@bp.get("/generate_meta")
def generate_meta():
    output = f"{getcwd()}/static"
    if not path.exists(output):
        mkdir(output)

    def one(in_list, variation, gender=""):
        asset_path = f"{getcwd()}/assets"
        assets = [y for y in listdir(f"{asset_path}/{gender}/{variation}")]

        a = 0
        for x in in_list:
            x[variation] = assets[a]

            a += 1
            if a >= len(assets):
                a = 0

        shuffle(in_list)
        return in_list

    def two(gender):
        meta = [{"id": x, "gender": gender} for x in range(5000)]
        meta = one(meta, "skin_tone", gender)
        meta = one(meta, "hair_style", gender)
        meta = one(meta, "cloth", gender)
        meta = one(meta, "earring", gender)
        meta = one(meta, "eye_glass", gender)
        meta = one(meta, "necklace", gender)
        meta = one(meta, "face_mask", gender)
        meta = one(meta, "head_gear", gender)
        meta = one(meta, "back_accessory", gender)
        meta = one(meta, "background")
        return meta

    tic = time.perf_counter()

    male = two("male")
    female = two("female")
    meta = [*male, *female]
    shuffle(meta)

    i = 1
    for x in meta:
        x["id"] = i
        i += 1

    with open(f"{output}/meta.json", 'w+') as f:
        json.dump(meta, f, indent=4)

    print(time.perf_counter() - tic)

    return jsonify({
        "status": 200,
        "message": "ok"
    })

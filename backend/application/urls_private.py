from flask import Blueprint, jsonify
from os import getcwd, path, mkdir
import json
from random import shuffle
import time
from .tools import (is_good, has_duplicate, assign_rarity,
                    assign_id, save, get_meta, generate_photo)

bp = Blueprint("urls_private", __name__)


@bp.get("/generate_meta")
def generate_meta():
    amount_to_generate = 10000

    tic = time.perf_counter()

    female = []
    for _ in range(int(amount_to_generate/2)):
        female.append(get_meta("female", female))
    male = []
    for _ in range(int(amount_to_generate/2)):
        male.append(get_meta("male", male))

    meta = [*male, *female]

    if has_duplicate(meta):
        print("has duplicate")
        generate_meta()

    shuffle(meta)
    assign_rarity(meta)
    assign_id(meta)
    save(meta)

    print(time.perf_counter() - tic)

    return jsonify({
        "status": 200,
        "message": "ok"
    })


@bp.post("/cleanup")
def cleanup():
    replace = []
    tic = time.perf_counter()

    output = f"{getcwd()}/static"
    with open(f"{output}/meta.json") as f:
        data = json.load(f)

    meta = []
    bare_meta = []
    female = []
    male = []

    for x in data:
        if is_good(x) and x["id"] not in replace:
            meta.append(x)
            bare_meta.append({
                "skin_tone": x["skin_tone"],
                "hairstyle": x["hairstyle"],
                "attire": x["attire"],
                "accessory": x["accessory"],
                "headgear": x["headgear"],
                "back_accessory": x["back_accessory"],
                "background": x["background"],
                "gender": x["gender"],
            })
        else:
            if x["gender"] == "female":
                female.append(x)
            else:
                male.append(x)

    for x in female:
        gen = get_meta("female", bare_meta)
        bare_meta.append(gen)
        gen["id"] = x["id"]
        meta.append(gen)
    for x in male:
        gen = get_meta("male", bare_meta)
        bare_meta.append(gen)
        gen["id"] = x["id"]
        meta.append(gen)

    if has_duplicate(bare_meta):
        print("has duplicate")
        cleanup()

    meta = sorted(meta, key=lambda d: d["id"], reverse=False)
    assign_rarity(meta)
    save(meta)

    print(time.perf_counter() - tic)

    return jsonify({
        "status": 200,
        "message": "ok"
    })


@bp.post("/shuffle")
def shuffle_it():
    output = f"{getcwd()}/static"
    with open(f"{output}/meta.json") as f:
        meta = json.load(f)

    shuffle(meta)
    assign_id(meta)
    save(meta)

    return jsonify({
        "status": 200,
        "message": "ok"
    })


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

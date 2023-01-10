from flask import Blueprint, jsonify
from os import getcwd, path, mkdir
import json
from random import shuffle, choices
import time
from .tool import weights, is_good

bp = Blueprint("api", __name__)


@bp.get("/")
def index():
    return jsonify({
        "status": 200,
        "message": "Welcome"
    })


amount_to_generate = 10000


def assign_rarity(meta):
    all_variation = []
    unique_variation = []
    for x in meta:
        for k, v in x.items():
            if k in ["rarity", "id"]:
                continue
            kv = f"{k}:::{v}"
            all_variation.append(kv)
            if kv not in unique_variation:
                unique_variation.append(kv)

    items_count = {}
    for x in unique_variation:
        kv = x.split(":::")
        k = kv[0]
        v = kv[1]

        if k not in items_count:
            items_count[k] = {}
        items_count[k][v] = all_variation.count(x)

    for x in meta:
        x["rarity"] = 0
        for k, v in x.items():
            if k in ["rarity", "id"]:
                continue
            x["rarity"] += items_count[k][v]

    meta = sorted(meta, key=lambda d: d["rarity"], reverse=False)
    for i, x in enumerate(meta):
        x["rarity"] = i + 1


def assign_id(meta):
    for i, x in enumerate(meta):
        x["id"] = i + 1


def save(meta):
    output_folder = f"{getcwd()}/static"
    if not path.exists(output_folder):
        mkdir(output_folder)

    with open(f"{output_folder}/meta.json", 'w+') as f:
        json.dump(meta, f, indent=4)


def has_duplicate1(a_list):
    a = len(a_list)
    a_list = list(map(dict, set(
        tuple(sorted(sub.items())) for sub in a_list)))
    return a != len(a_list)


def has_duplicate2(a_list):
    seen = []
    return any(i in seen or seen.append(i) for i in a_list)


def get_meta(gender, a_list):
    gen = {}

    traits = ["skin_tone", "hairstyle", "attire",
              "accessory", "headgear", "back_accessory"]

    for trait in traits:
        gen[trait] = choices(
            [k for k in weights[gender][trait]],
            [weights[gender][trait][k] for k in weights[gender][trait]]
        )[0]
    gen["background"] = choices(
        [k for k in weights["background"]],
        [weights["background"][k] for k in weights["background"]]
    )[0]
    gen["gender"] = gender

    if gen in a_list or not is_good(gen):
        return get_meta(gender, a_list)
    else:
        return gen


@bp.get("/generate_meta")
def generate_meta():

    tic = time.perf_counter()

    female = []
    for _ in range(int(amount_to_generate/2)):
        female.append(get_meta("female", female))
    male = []
    for _ in range(int(amount_to_generate/2)):
        male.append(get_meta("male", male))

    meta = [*male, *female]

    print("has_duplicate?", has_duplicate1(meta))
    print("has_duplicate?", has_duplicate2(meta))

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

    print("has_duplicate?", has_duplicate1(bare_meta))
    print("has_duplicate?", has_duplicate2(bare_meta))

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

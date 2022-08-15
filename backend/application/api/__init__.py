from flask import Blueprint, jsonify
from os import getcwd, listdir, path, mkdir
import json
from random import shuffle
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
    output_folder = f"{getcwd()}/static"
    if not path.exists(output_folder):
        mkdir(output_folder)
    asset_path = f"{getcwd()}/assets"

    def get_list(variation, gender=""):
        output = []
        for img_name in listdir(f"{asset_path}/{gender}/{variation}"):
            amount = img_name.split(".")[0].split("#")[1]
            temp = [img_name for _ in range(int(amount))]
            output = [*output, *temp]
        shuffle(output)
        return output

    tic = time.perf_counter()

    def get_meta(gender):
        skin_tone = get_list("skin_tone", gender)
        hair_style = get_list("hair_style", gender)
        cloth = get_list("cloth", gender)
        earring = get_list("earring", gender)
        eye_glass = get_list("eye_glass", gender)
        necklace = get_list("necklace", gender)
        head_gear = get_list("head_gear", gender)
        back_accessory = get_list("back_accessory", gender)

        output = []
        while len(output) < 2500:
            output.append({
                "gender": gender,
                "skin_tone": skin_tone[0],
                "hair_style": hair_style[0],
                "cloth": cloth[0],
                "earring": earring[0],
                "eye_glass": eye_glass[0],
                "necklace": necklace[0],
                "head_gear": head_gear[0],
                "back_accessory": back_accessory[0]
            })
            count = len(output)
            output = list(map(dict, set(
                tuple(sorted(sub.items())) for sub in output)))

            if count == len(output):
                skin_tone = skin_tone[1:]
                hair_style = hair_style[1:]
                cloth = cloth[1:]
                earring = earring[1:]
                eye_glass = eye_glass[1:]
                necklace = necklace[1:]
                head_gear = head_gear[1:]
                back_accessory = back_accessory[1:]
            elif len(output) == 4999:
                raise ValueError("stalemate")
            else:
                shuffle(skin_tone)
                shuffle(hair_style)
                shuffle(cloth)
                shuffle(earring)
                shuffle(eye_glass)
                shuffle(necklace)
                shuffle(head_gear)
                shuffle(back_accessory)
                print("shuffle")

        return output

    male = get_meta("male")
    female = get_meta("female")
    meta = [*male, *female]

    background = get_list("background")
    for i, x in enumerate(meta):
        x["background"] = background[i]

    all_variation = []
    unique_variation = []
    for x in meta:
        for k, v in x.items():
            if k == "rarity":
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
            if k == "rarity":
                continue
            x["rarity"] += items_count[k][v]

    meta = sorted(meta, key=lambda d: d["rarity"], reverse=False)
    for i, x in enumerate(meta):
        x["rarity"] = i + 1

    shuffle(meta)

    for i, x in enumerate(meta):
        x["id"] = i + 1

    with open(f"{output_folder}/meta.json", 'w+') as f:
        json.dump(meta, f, indent=4)

    print(time.perf_counter() - tic)

    return jsonify({
        "status": 200,
        "message": "ok"
    })

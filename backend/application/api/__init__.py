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
    total_count = 5000

    def get_list(variation, gender=""):
        output = []
        for img_name in listdir(f"{asset_path}/{gender}/{variation}"):
            img_name, amount = img_name.split("#")
            amount = amount.split(".")[0]
            amount = int(amount)

            temp = [img_name for _ in range(amount)]
            output = [*output, *temp]

        amount = int(total_count/2 - len(output))
        if amount > 0:
            temp = ["none" for _ in range(amount)]
            output = [*output, *temp]

        shuffle(output)
        return output

    tic = time.perf_counter()

    def get_meta(gender):
        skin_tone = get_list("skin_tone", gender)
        hairstyle = get_list("hairstyle", gender)
        attire = get_list("attire", gender)
        accessory = get_list("accessory", gender)
        headgear = get_list("headgear", gender)
        back_accessory = get_list("back_accessory", gender)

        output = []
        while len(output) < total_count/2:
            output.append({
                "gender": gender,
                "skin_tone": skin_tone[0],
                "hairstyle": hairstyle[0],
                "attire": attire[0],
                "accessory": accessory[0],
                "headgear": headgear[0],
                "back_accessory": back_accessory[0]
            })
            count = len(output)
            output = list(map(dict, set(
                tuple(sorted(sub.items())) for sub in output)))

            if count == len(output):
                skin_tone = skin_tone[1:]
                hairstyle = hairstyle[1:]
                attire = attire[1:]
                accessory = accessory[1:]
                headgear = headgear[1:]
                back_accessory = back_accessory[1:]
            elif len(output) == total_count - 1:
                raise ValueError("stalemate")
            else:
                shuffle(skin_tone)
                shuffle(hairstyle)
                shuffle(attire)
                shuffle(accessory)
                shuffle(headgear)
                shuffle(back_accessory)
                print("shuffle")

        return output

    male = get_meta("male")
    female = get_meta("female")
    meta = [*male, *female]

    background = get_list("background")
    for i, x in enumerate(meta):
        x["background"] = background[i]


# calculate rarity

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

# give ID

    for i, x in enumerate(meta):
        x["id"] = i + 1

# save meta

    with open(f"{output_folder}/meta.json", 'w+') as f:
        json.dump(meta, f, indent=4)

    print(time.perf_counter() - tic)

    return jsonify({
        "status": 200,
        "message": "ok"
    })

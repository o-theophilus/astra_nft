from flask import Blueprint, jsonify
from os import getcwd, listdir, path, mkdir, rename
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


amount_to_generate = 5000


def assign_rearity(meta):
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


def assign_id_and_save(meta):
    output_folder = f"{getcwd()}/static"
    if not path.exists(output_folder):
        mkdir(output_folder)

    for i, x in enumerate(meta):
        x["id"] = i + 1

    with open(f"{output_folder}/meta.json", 'w+') as f:
        json.dump(meta, f, indent=4)


def is_good(x):
    if (
        x["gender"] == "female"
        and x["headgear"] in ["astra helmet spike",
                              "AstraCap", "Astrahelmet", "blackasmask"]
        and x["hairstyle"] in ["astra hairstyle 4", "astra hairstyle 5",
                               "astra hairstyle 13", "astra hairstyle 15"]
    ):
        return False
    elif (
        x["gender"] == "female"
        and x["headgear"] in ["astra helmet spike",
                              "Astrahelmet", "blackasmask"]
        and x["accessory"] == "white pearrl neclace"
    ):
        return False
    elif (
        x["gender"] == "female"
        and x["attire"] == "astra attire 21"
        and x["accessory"] == "white pearrl neclace"
        and x['headgear'] in ["gob mask", "mask"]
    ):
        return False
    elif (
        x["gender"] == "female"
        and x["headgear"] in ["astra helmet spike",
                              "AstraCap", "Astrahelmet", "blackasmask"]
        and x['attire'] in [
            "astra attire 24", "astra attire 21", "astra attire 35"]
    ):
        return False
    elif (
        x["gender"] == "female"
        and x["attire"] == "astra attire 35"
        and (
            x["accessory"] == "white pearrl neclace"
            or x["hairstyle"] in ["astra hairstyle 5",
                                  "astra hairstyle 15", "astra hairstyle 13"]
            or x["headgear"] in ["astra helmet spike"]
        )
    ):
        return False

    elif (
        x["gender"] == "male"
        and x["headgear"] in ["blackasspke red", "helmetenticls",
                              "IMG-3396", "mech had", "punkhelmet", "AstraCap"]
        and x["hairstyle"] in ["astra hairstyle 4", "astra hairstyle 5",
                               "astra hairstyle 7", "astra hairstyle 8",
                               "astra hairstyle 9", "astra hairstyle 13"]
    ):
        return False
    elif (
        x["gender"] == "male"
        and x["attire"] in ["astra attire 11", "astra attire 24",
                            "astra attire 25", "astra attire 32",
                            "astra attire 33", "astra attire 34"]
        and x["headgear"] in ["AstraCap", "mech had", "whyeemaskt"]
    ):
        return False
    elif (
        x["gender"] == "male"
        and x["attire"] in ["astra attire 24", "astra attire 25",
                            "astra attire 34"]
        and x["headgear"] in ["blackasspke red", "helmetenticls",
                              "punkhelmet"]
    ):
        return False
    elif (
        x["gender"] == "male"
        and x["attire"] in ["astra attire 34"]
        and x["headgear"] in ["IMG-2971", "IMG-3376", "IMG-3385",
                              "IMG-3397", "IMG-4122", "obsidian shades"]
    ):
        return False
    elif (
        x["gender"] == "male"
        and x["attire"] in ["astra attire 11", "astra attire 24",
                            "astra attire 25", "astra attire 32",
                            "astra attire 33", "astra attire 34"]
        and x["hairstyle"] in ["astra hairstyle 4", "astra hairstyle 5",
                               "astra hairstyle 7", "astra hairstyle 8",
                               "astra hairstyle 9", "astra hairstyle 13"]
    ):
        return False

    return True


@bp.post("/distribute_assets")
def distribute_assets():

    def distribute(amount_, full_path, allow_empty):
        files_in_folder = listdir(full_path)
        last_file = files_in_folder[-1]
        count_files = len(files_in_folder)
        if allow_empty:
            count_files += 1
        sub_count = int(amount_ / count_files)

        for old_name in files_in_folder:
            img_name, second_part = old_name.split("#")
            ext = second_part.split(".")[1]

            if not allow_empty and old_name == last_file:
                sub_count += amount_ % count_files

            new_name = f"{img_name}#{sub_count}.{ext}"
            rename(
                f"{full_path}/{old_name}",
                f"{full_path}/{new_name}"
            )

    base_path = f"{getcwd()}/assets"

    for g in ["male", "female"]:
        for v in [
            "skin_tone",
            "hairstyle",
            "attire",
            "accessory",
            "headgear",
            "back_accessory"
        ]:
            e = True
            if (
                v == "skin_tone"
                or g == "female" and v == "attire"
            ):
                e = False

            distribute(
                amount_to_generate/2 + 500,
                f"{base_path}/{g}/{v}", e
            )

    distribute(amount_to_generate, f"{base_path}/background", False)

    return jsonify({
        "status": 200,
        "message": "ok"
    })


@bp.get("/generate_meta")
def generate_meta():
    asset_path = f"{getcwd()}/assets"

    def get_list(variation, gender=""):
        output = []
        for img_name in listdir(f"{asset_path}/{gender}/{variation}"):
            img_name, amount = img_name.split("#")
            amount = amount.split(".")[0]
            amount = int(amount)

            temp = [img_name for _ in range(amount)]
            output = [*output, *temp]

        amount = int(amount_to_generate/2 - len(output))
        if amount > 0:
            temp = ["none" for _ in range(amount)]
            output = [*output, *temp]

        shuffle(output)
        return output

    def get_meta(gender):
        skin_tone = get_list("skin_tone", gender)
        hairstyle = get_list("hairstyle", gender)
        attire = get_list("attire", gender)
        accessory = get_list("accessory", gender)
        headgear = get_list("headgear", gender)
        back_accessory = get_list("back_accessory", gender)

        shuffle_count = 0

        def shuffle_it():
            nonlocal shuffle_count
            shuffle_count += 1
            if shuffle_count == 100:
                raise ValueError("stalemate")

            shuffle(skin_tone)
            shuffle(hairstyle)
            shuffle(attire)
            shuffle(accessory)
            shuffle(headgear)
            shuffle(back_accessory)

        output = []
        while len(output) < amount_to_generate/2:
            gen = {
                "gender": gender,
                "skin_tone": skin_tone[0],
                "hairstyle": hairstyle[0],
                "attire": attire[0],
                "accessory": accessory[0],
                "headgear": headgear[0],
                "back_accessory": back_accessory[0]
            }

            if not is_good(gen):
                shuffle_it()
                continue
            else:
                shuffle_count = 0

            temp = [*output, gen]
            temp = list(map(dict, set(
                tuple(sorted(sub.items())) for sub in temp)))

            if len(output) == len(temp):
                shuffle_it()
                continue
            else:
                shuffle_count = 0

            output.append(gen)
            skin_tone = skin_tone[1:]
            hairstyle = hairstyle[1:]
            attire = attire[1:]
            accessory = accessory[1:]
            headgear = headgear[1:]
            back_accessory = back_accessory[1:]

        return output

    tic = time.perf_counter()

    male = get_meta("male")
    female = get_meta("female")
    meta = [*male, *female]

    background = get_list("background")
    for i, x in enumerate(meta):
        x["background"] = background[i]

    shuffle(meta)
    assign_rearity(meta)
    assign_id_and_save(meta)

    print(time.perf_counter() - tic)

    return jsonify({
        "status": 200,
        "message": "ok"
    })


@bp.post("/cleanup")
def cleanup():
    output = f"{getcwd()}/static"

    with open(f"{output}/meta.json") as f:
        data = json.load(f)

    to_del = []
    for x in data:
        if not is_good(x):
            to_del.append(x["id"])

    meta = [x for x in data if x["id"] not in to_del]
    assign_rearity(meta)
    assign_id_and_save(meta)

    return jsonify({
        "status": 200,
        "message": "ok"
    })

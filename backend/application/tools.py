from os import getcwd, path, mkdir, listdir
import json
from random import choices
from PIL import Image
from .weights import weights


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


def has_duplicate(a_list):
    seen = []
    return any(i in seen or seen.append(i) for i in a_list)


def get_meta(gender, a_list):
    gen = {}

    for x in ["skin_tone", "hairstyle", "attire", "accessory", "headgear",
              "back_accessory", "background", "frame"]:
        if x in ["background", "frame"]:
            trait = weights[x]
        else:
            trait = weights[gender][x]

        gen[x] = choices([k for k in trait], [trait[k] for k in trait])[0]
    gen["gender"] = gender

    if gen in a_list or not is_good(gen):
        return get_meta(gender, a_list)
    else:
        return gen


def is_good(x):
    if x["gender"] == "female":
        if (
            x["headgear"] == "AstraCap"
            and x["hairstyle"] in ["astra hairstyle 4", "astra hairstyle 11",
                                   "astra hairstyle 5", "astra hairstyle 1",
                                   "astra hairstyle 7",
                                   "astra hairstyle 10", "astra hairstyle 18",
                                   "astra hairstyle 16", "astra hairstyle 3",
                                   "astra hairstyle 13", "astra hairstyle 15"]
        ):
            return False
        elif x["attire"] == "none":
            return False
        elif (
            x["headgear"] in ["astra helmet spike",
                              "Astrahelmet", "blackasmask"]
            and x["hairstyle"] in ["astra hairstyle 1", "astra hairstyle 3",
                                   "astra hairstyle 4", "astra hairstyle 5",
                                   "astra hairstyle 7", "astra hairstyle 12",
                                   "astra hairstyle 13", "astra hairstyle 15",
                                   "astra hairstyle 16", "astra hairstyle 18"]
        ):
            return False
        elif (
            x["headgear"] in ["astra helmet spike",
                              "Astrahelmet", "blackasmask"]
            and x["accessory"] == "white pearrl neclace"
        ):
            return False
        elif (
            x["attire"] == "astra attire 21"
            and x["accessory"] == "white pearrl neclace"
            and x['headgear'] in ["gob mask", "mask"]
        ):
            return False
        elif (
            x["attire"] == "astra attire 23"
            and x['hairstyle'] not in ["astra hairstyle 2",
                                       "astra hairstyle 8", "none"]
        ):
            return False
        elif (
            x["attire"] == "astra attire 7"
            and x['hairstyle'] in ["astra hairstyle 5", "astra hairstyle 13"]
        ):
            return False
        elif (
            x["attire"] == "astra attire 23"
            and x['accessory'] == "white pearrl neclace"
        ):
            return False
        elif (
            x["headgear"] in ["astra helmet spike",
                              "AstraCap", "Astrahelmet", "blackasmask"]
            and x['attire'] in ["astra attire 24", "astra attire 21",
                                "astra attire 35"]
        ):
            return False
        elif (
            x["attire"] == "astra attire 35"
            and (
                x["accessory"] == "white pearrl neclace"
                or x["headgear"] == "astra helmet spike"
                or x["hairstyle"] in ["astra hairstyle 5",
                                      "astra hairstyle 15",
                                      "astra hairstyle 13"]
            )
        ):
            return False
    else:
        if (
            x["headgear"] in ["blackasspke red", "helmetenticls",
                              "mech had", "punkhelmet", "AstraCap",
                              "IMG-4101", "IMG-4102",
                              "IMG-4103", "IMG-4104",
                              ]
            and x["hairstyle"] in ["astra hairstyle 4", "astra hairstyle 5",
                                   "astra hairstyle 7", "astra hairstyle 8",
                                   "astra hairstyle 9", "astra hairstyle 13"]
        ):
            return False
        elif (
            x["headgear"] == "AstraCap"
            and x["hairstyle"] in [
                "astra hairstyle 1", "astra hairstyle 2",
                "astra hairstyle 3", "astra hairstyle 4",
                "astra hairstyle 6", "astra hairstyle 15",
            ]
        ):
            return False
        elif (
            x["attire"] in ["astra attire 11", "astra attire 24",
                            "astra attire 25", "astra attire 32",
                            "astra attire 33", "astra attire 34"]
            and (
                x["headgear"] in ["AstraCap", "mech had", "whyeemaskt",
                                  "blackasspke red", "helmetenticls",
                                  "punkhelmet",
                                  "IMG-4101", "IMG-4102",
                                  "IMG-4103", "IMG-4104",
                                  ]
                or x["hairstyle"] in ["astra hairstyle 3", "astra hairstyle 4",
                                      "astra hairstyle 5", "astra hairstyle 7",
                                      "astra hairstyle 8", "astra hairstyle 9",
                                      "astra hairstyle 13",
                                      "astra hairstyle 15"]
                or x["accessory"] in ["astra accessory 2", "astra accessory 3",
                                      "astra accessory 4"]
            )
        ):
            return False
        elif (
            x["attire"] == "astra attire 34"
            and x["headgear"] in ["IMG-2971", "IMG-3376", "IMG-3385",
                                  "IMG-3397", "IMG-4122", "obsidian shades"]
        ):
            return False

    return True


def generate_photo(meta):
    """Build photo from meta"""

    def get_v(v, root=False):
        if meta[v] != "none":
            asset_path = f"{getcwd()}/assets/{meta['gender']}/{v}"
            if root:
                asset_path = f"{getcwd()}/assets/{v}"

            for img_name in listdir(asset_path):
                if img_name.split(".")[0] == meta[v]:
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
        and meta['headgear'] not in ["focus mask", "memask"]
    ):
        photo = Image.alpha_composite(photo, get_v("headgear"))
        photo = Image.alpha_composite(photo, get_v("attire"))
        photo = Image.alpha_composite(photo, get_v("accessory"))
    elif (
        meta['gender'] == "male"
        and meta['headgear'] in ["blackasspke red", "focus mask",
                                 "helmetenticls", "memask",
                                 "punkhelmet", "whyeemaskt"
                                 "IMG-4101", "IMG-4102",
                                 "IMG-4103", "IMG-4104"]
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
    photo = Image.alpha_composite(photo, get_v("frame", True))

    return photo

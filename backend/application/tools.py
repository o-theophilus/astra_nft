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
            x["headgear"] == "astra_cap"
            and x["hairstyle"] in ["female_hairstyle_4", "female_hairstyle_11",
                                   "female_hairstyle_5", "female_hairstyle_1",
                                   "female_hairstyle_7",
                                   "female_hairstyle_10",
                                   "female_hairstyle_18",
                                   "female_hairstyle_16", "female_hairstyle_3",
                                   "female_hairstyle_13",
                                   "female_hairstyle_15"]
        ):
            return False
        elif x["attire"] == "none":
            return False
        elif (
            x["headgear"] in ["astra_helmet_spike",
                              "astrahelmet", "blackasmask"]
            and x["hairstyle"] in ["female_hairstyle_1", "female_hairstyle_3",
                                   "female_hairstyle_4", "female_hairstyle_5",
                                   "female_hairstyle_7", "female_hairstyle_12",
                                   "female_hairstyle_13",
                                   "female_hairstyle_15",
                                   "female_hairstyle_16",
                                   "female_hairstyle_18"]
        ):
            return False
        elif (
            x["headgear"] in ["astra_helmet_spike",
                              "astrahelmet", "blackasmask"]
            and x["accessory"] == "white_pearrl_neclace"
        ):
            return False
        elif (
            x["attire"] == "female_attire_21"
            and x["accessory"] == "white_pearrl_neclace"
            and x['headgear'] in ["gob_mask", "mask"]
        ):
            return False
        elif (
            x["attire"] == "female_attire_23"
            and x['hairstyle'] not in ["female_hairstyle_2",
                                       "female_hairstyle_8", "none"]
        ):
            return False
        elif (
            x["attire"] == "female_attire_7"
            and x['hairstyle'] in ["female_hairstyle_5", "female_hairstyle_13"]
        ):
            return False
        elif (
            x["attire"] == "female_attire_23"
            and x['accessory'] == "white_pearrl_neclace"
        ):
            return False
        elif (
            x["headgear"] in ["astra_helmet_spike",
                              "astra_cap", "astrahelmet", "blackasmask"]
            and x['attire'] in ["female_attire_24", "female_attire_21",
                                "female_attire_35"]
        ):
            return False
        elif (
            x["attire"] == "female_attire_35"
            and (
                x["accessory"] == "white_pearrl_neclace"
                or x["headgear"] == "astra_helmet_spike"
                or x["hairstyle"] in ["female_hairstyle_5",
                                      "female_hairstyle_15",
                                      "female_hairstyle_13"]
            )
        ):
            return False
    else:
        if (
            x["headgear"] in ["blackasspke_red", "helmetenticls",
                              "mech_had", "punkhelmet", "astra_cap",
                              "male_headgear_5", "male_headgear_6",
                              "male_headgear_7", "male_headgear_8",
                              ]
            and x["hairstyle"] in ["male_hairstyle_4", "male_hairstyle_5",
                                   "male_hairstyle_7", "male_hairstyle_8",
                                   "male_hairstyle_9", "male_hairstyle_13"]
        ):
            return False
        elif (
            x["headgear"] == "astra_cap"
            and x["hairstyle"] in [
                "male_hairstyle_1", "male_hairstyle_2",
                "male_hairstyle_3", "male_hairstyle_4",
                "male_hairstyle_6", "male_hairstyle_15",
            ]
        ):
            return False
        elif (
            x["attire"] in ["male_attire_11", "male_attire_24",
                            "male_attire_25", "male_attire_32",
                            "male_attire_33", "male_attire_34"]
            and (
                x["headgear"] in ["astra_cap", "mech_had", "whyeemaskt",
                                  "blackasspke_red", "helmetenticls",
                                  "punkhelmet",
                                  "male_headgear_5", "male_headgear_6",
                                  "male_headgear_7", "male_headgear_8",
                                  ]
                or x["hairstyle"] in ["male_hairstyle_3", "male_hairstyle_4",
                                      "male_hairstyle_5", "male_hairstyle_7",
                                      "male_hairstyle_8", "male_hairstyle_9",
                                      "male_hairstyle_13",
                                      "male_hairstyle_15"]
                or x["accessory"] in ["astra_gold", "astra_silver",
                                      "astra_bronze"]
            )
        ):
            return False
        elif (
            x["attire"] == "male_attire_34"
            and x["headgear"] in ["male_headgear_1", "male_headgear_2",
                                  "male_headgear_3", "male_headgear_4",
                                  "male_headgear_9", "obsidian_shades"]
        ):
            return False

    return True


def generate_photo(meta):
    """Build photo from meta"""

    def get_v(v, root=False):
        photo = Image.new('RGBA', (2000, 2000), (0, 0, 0, 0))
        if meta[v] != "none":
            asset_path = f"{getcwd()}/assets/{meta['gender']}/{v}"
            if root:
                asset_path = f"{getcwd()}/assets/{v}"

            for img_name in listdir(asset_path):
                if img_name.split(".")[0] == meta[v]:
                    photo = Image.open(f"{asset_path}/{img_name}")

        return photo

    photo = Image.alpha_composite(get_v("skin_tone"), get_v("hairstyle"))
    if (
        meta['gender'] == "female"
        and meta['attire'] in [
            "female_attire_24", "female_attire_21", "female_attire_35"]
        or meta['gender'] == "male"
        and meta['attire'] in ["male_attire_24", "male_attire_25"]
        and meta['headgear'] not in ["focus_mask", "memask"]
    ):
        photo = Image.alpha_composite(photo, get_v("headgear"))
        photo = Image.alpha_composite(photo, get_v("attire"))
        photo = Image.alpha_composite(photo, get_v("accessory"))
    elif (
        meta['gender'] == "male"
        and meta['headgear'] in ["blackasspke_red", "focus_mask",
                                 "helmetenticls", "memask",
                                 "punkhelmet", "whyeemaskt"
                                 "male_headgear_5", "male_headgear_6",
                                 "male_headgear_7", "male_headgear_8"]
        and meta['accessory'] in ["astra_gold", "astra_silver",
                                  "astra_bronze"]
        or meta['gender'] == "female"
        and meta['headgear'] in ["gob_mask", "mask"]
        and meta['accessory'] == "white_pearrl_neclace"
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

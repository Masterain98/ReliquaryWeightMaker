import json
import os
import requests


def element_text_to_id(element_name: str) -> int:
    element_id = {
        "None": 0,
        "Pyro": 1,
        "Hydro": 2,
        "Dendro": 3,
        "Electro": 4,
        "Cryo": 5,
        "Anemo": 7,
        "Geo": 8
    }
    try:
        return element_id[element_name]
    except KeyError:
        return 0


def push():
    with open('./Output/ReliquaryWeightConfiguration.json', 'r', encoding="utf-8") as file:
        reliquary_weight_content = json.loads(file.read())
    new_json_list = []
    for k, v in reliquary_weight_content.items():
        new_json_list.append({
            "avatarId": int(k),
            "hpPercent": v.get("hp", 0),
            "attackPercent": v.get("atk", 0),
            "defendPercent": v.get("def", 0),
            "critical": v.get("cpct", 0),
            "criticalHurt": v.get("cdmg", 0),
            "elementMastery": v.get("mastery", 0),
            "chargeEfficiency": v.get("recharge", 0),
            "healAdd": v.get("heal", 0),
            "addHurt": v.get("dmg", 0),
            "elementType": element_text_to_id(v["element"]),
            "physicalAddHurt": v.get("phy", 0),
        })
    result = requests.post(os.getenv("POST_URL"), json=new_json_list)
    print("Pushed result: %s" % result.status_code)

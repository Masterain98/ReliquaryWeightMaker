import requests
import chompjs
import json

if __name__ == "__main__":
    # Original File
    req = requests.get("https://raw.githubusercontent.com/yoimiya-kokomi/miao-plugin/master/resources/meta/artifact"
                       "/artis-mark.js")
    with open("artis-mark.js", "w", encoding="utf-8") as f:
        f.write(req.text)
    # Metadata
    element_chs_to_eng = {
        "风": "Anemo",
        "岩": "Geo",
        "雷": "Electro",
        "草": "Dendro",
        "水": "Hydro",
        "火": "Pyro",
        "冰": "Cryo"
    }
    metadata_json = json.loads(
        requests.get("https://raw.githubusercontent.com/DGP-Studio/Snap.Metadata/main/Output/CHS/Avatar"
                     ".json").text)
    character_to_element_list = [{item["Name"]: element_chs_to_eng[item["FetterInfo"]["VisionBefore"]]}
                                 for item in metadata_json]
    character_to_element_dict = {list(item.keys())[0]: list(item.values())[0] for item in character_to_element_list}
    # CHS to ID Dict
    chs_dict = json.loads(requests.get("https://api.uigf.org/dict/chs.json").text)

    # Read MiaoMiao
    original_file = open('artis-mark.js', 'r', encoding="utf-8")
    lines = original_file.readlines()
    # Build New File
    new_file = open("./Output/ReliquaryWeight.cs.json", "w+", encoding="utf-8")
    new_file.write("{ \n")

    for line in lines:
        if " hp: " in line:
            if "旅行者" not in line and "空" not in line and "荧" not in line:
                new_file.write(line)
    new_file.write("}")
    new_file.close()

    # Read Entire New File
    with open('./Output/ReliquaryWeight.cs.json', 'r', encoding="utf-8") as file:
        ReliquaryWeight_content = file.read()

    miaomiao_dict = chompjs.parse_js_object(ReliquaryWeight_content)
    final_dict = {}
    for key_name in miaomiao_dict.keys():
        if key_name != "旅行者" and key_name != "空" and key_name != "荧":
            item_id = chs_dict[key_name]
            final_dict[item_id] = miaomiao_dict[key_name]
            final_dict[item_id]["element"] = character_to_element_dict[key_name]
    with open("./Output/ReliquaryWeight.cs.ID.json", "w+") as write_file:
        json.dump(final_dict, write_file, indent=4)

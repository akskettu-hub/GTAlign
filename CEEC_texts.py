import xml.etree.ElementTree as ET
import os


def get_tei_collection_id(collection_xml: str) -> str:
    root = find_root(collection_xml=collection_xml)
    xml_id = root.attrib["{http://www.w3.org/XML/1998/namespace}id"]

    return xml_id


def find_xml_recursive(path: str, xml_path_d: dict) -> None:
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)

        if os.path.isdir(full_path):
            find_xml_recursive(full_path, xml_path_d=xml_path_d)
        elif entry.endswith(".xml"):
            teiId = get_tei_collection_id(full_path)
            xml_path_d[teiId] = full_path


def construct_xml_path_dict(data_path: str) -> dict:
    tei_xml_path_d = {}
    find_xml_recursive(path=data_path, xml_path_d=tei_xml_path_d)

    return tei_xml_path_d


def find_root(collection_xml: str):
    tree = ET.parse(collection_xml)
    root = tree.getroot()

    return root


def paragraph_to_text(p_el):
    parts = []

    if p_el.text:
        parts.append(p_el.text)
    for child in p_el:
        parts.append(paragraph_to_text(child))
        if child.tail:
            parts.append(child.tail)

    return "".join(parts)


def get_tei_text(tei):
    textElement = tei.find("text")

    tei_text = ""

    if textElement is not None:
        for paragraph in textElement.findall("p"):
            p_text = paragraph_to_text(paragraph)
            tei_text += p_text + "\n"

    return tei_text


def find_letter_from_tei_list(tei_list: list, wanted_letter_id: str):
    ns = {"letterID": "{http://www.w3.org/XML/1998/namespace}id"}
    for tei in tei_list:
        letter_id = tei.get(ns["letterID"])
        if letter_id == wanted_letter_id:
            return get_tei_text(tei=tei)


def get_CEEC_texts(dfs_dict: dict) -> dict:
    ceec_txt_dict = {}
    letter_ids = list(dfs_dict.keys())
    xml_paths = construct_xml_path_dict(data_path="./data/CEEC-400/")
    for letter_id in letter_ids:
        collection_name = "F" + letter_id.split("_")[0]
        # print(letter_id, collection_name)
        # print(xml_paths[collection_name])

        root = find_root(collection_xml=xml_paths[collection_name])
        tei_list = root.findall("TEI")
        letter_txt = find_letter_from_tei_list(tei_list, letter_id)

        ceec_txt_dict[letter_id] = letter_txt

    return ceec_txt_dict

import os
from CEECxml import get_tei_collection_id


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


if __name__ == "__main__":
    d = construct_xml_path_dict(data_path="./data/CEEC-400/")
    print(len(d.keys()))
    print(d)
    # print(d)
    # xmls = find_xml_recursive(path="./data/CEEC-400/", xml_path_l=l)

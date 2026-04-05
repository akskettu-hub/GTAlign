import xml.etree.ElementTree as ET


def get_tei_collection_id(collection_xml: str) -> str:
    root = find_root(collection_xml=collection_xml)
    xml_id = root.attrib["{http://www.w3.org/XML/1998/namespace}id"]

    return xml_id


def parse_tei_collection(
    collection_xml: str,
    print_letter_text: bool,
    letters_to_print: dict,
    return_single_letter: bool,
):
    root = find_root(collection_xml=collection_xml)

    tei_list = find_TEIs_from_root(root)

    return parse_teis(
        tei_list, print_letter_text, letters_to_print, return_single_letter
    )


def parse_teis(
    tei_list,
    print_letter_text: bool,
    letters_to_print: dict,
    return_single_letter: bool,
):
    ns = {"letterID": "{http://www.w3.org/XML/1998/namespace}id"}

    for tei in tei_list:
        letterid = tei.get(ns["letterID"])
        letter_n = int(letterid[-3:])

        if letter_n in letters_to_print:
            if print_letter_text:
                print_tei_text(tei=tei, letterid=letterid)
            if return_single_letter:
                # print(get_tei_text(tei=tei))
                return get_tei_text(tei=tei)


def find_root(collection_xml: str):
    tree = ET.parse(collection_xml)
    root = tree.getroot()

    return root


def find_TEIs_from_root(root):
    # ns = {"letterID": "{http://www.w3.org/XML/1998/namespace}id"}

    tei_list = root.findall("TEI")
    # print(type(tei_list))
    # print(type(tei_list[0]))

    # for tei in tei_list:
    # letterid = tei.get(ns["letterID"])
    # print(letterid)

    return tei_list


def print_tei_text(tei, letterid):
    textElement = tei.find("text")

    if textElement is not None:
        print(letterid)
        for paragraph in textElement.findall("p"):
            p_text = paragraph_to_text(paragraph)
            print_paragraph(p_text)


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


def print_paragraph(p: str):
    print(p, "\n")


# def write_letter_to_txt()

if __name__ == "__main__":
    letters_to_print = [1]
    # letters_to_print = [1, 2, 5, 10]
    lettersd = {letter: True for letter in letters_to_print}

    print(
        parse_tei_collection(
            "FMARCHAL.xml",
            print_letter_text=False,
            letters_to_print=lettersd,
            return_single_letter=True,
        )
    )

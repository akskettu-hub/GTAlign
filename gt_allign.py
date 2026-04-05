import pandas as pd
import glob
import xml.etree.ElementTree as ET
from nltk.tokenize import word_tokenize
import Levenshtein

from CEEC_400_data_parser import construct_xml_path_dict


def get_dfs_form_xlsx(path: str) -> dict[str, pd.DataFrame]:
    files = glob.glob(path + "*.xlsx")
    # dfs = [pd.read_excel(file) for file in files]

    # dfs = {file: pd.read_excel(file) for file in files}

    dfs_dict = {}
    for file in files:
        letter_id = file.split("/")[-1].replace(".xlsx", "")
        dfs_dict[letter_id] = {}
        dfs_dict[letter_id]["path"] = file
        dfs_dict[letter_id]["df"] = pd.read_excel(file)

    return dfs_dict


def get_strs_from_df(dfs: dict[str, pd.DataFrame]):

    filtered_dfs = []
    for key in dfs.keys():
        df = dfs[key]["df"]
        filtered_df = df[df["C7 correct"].notna()]
        filtered_dfs.append(filtered_df)

    print(filtered_dfs[0].head(30))


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


def tokenize_text(text: str):
    tokenized_text = word_tokenize(text, language="english")

    return tokenized_text


def word_cost(w1, w2):
    return Levenshtein.distance(w1, w2) / max(len(w1), len(w2))


def align_tokens(norm_tokens: list[tuple], orig_tokens: list[str]):
    aligned_tokens = []
    i = 0
    print(len(orig_tokens))
    for norm_token in norm_tokens:
        if i > len(orig_tokens):
            break
        matching_token = orig_tokens[i]
        word_cost_current_pair = word_cost(norm_token[1], matching_token)
        if type(norm_token[0]) == str:
            if "-" in norm_token[0] or "–" in norm_token[0]:
                matching_token += orig_tokens[i + 1]
                # i += 1
                i += 1
        elif word_cost_current_pair >= 0.33:
            combined_with_next = matching_token + " " + orig_tokens[i + 1]
            if word_cost_current_pair > word_cost(norm_token[1], combined_with_next):
                matching_token = combined_with_next
                # i += 1
                i += 1
        aligned_tokens.append((norm_token[0], norm_token[1], matching_token))
        i += 1

    return aligned_tokens


if __name__ == "__main__":
    dfs = get_dfs_form_xlsx("./data/silver_standard/silver_standard/")
    # print(dfs.keys())

    # print(dfs["BURNEYF_013"])
    # get_strs_from_df(dfs)
    ceec_txt_dict = get_CEEC_texts(dfs)
    # print(ceec_txt_dict["BURNEYF_013"])

    # print(df[df["C7 correct"].notna()].head(50))

    tok_test = tokenize_text(ceec_txt_dict["BURNEYF_013"])
    # print(tok_test)

    df = dfs["BURNEYF_013"]["df"]
    filtered_df = df[df["C7 correct"].notna()]

    tuples_list = list(zip(filtered_df["Token id"], filtered_df["Token"]))
    # print(tuples_list)
    print(len(tok_test), len(tuples_list))

    # for i in range(len(tuples_list)):
    #    print(tuples_list[i][0], tuples_list[i][1], tok_test[i])
    res = align_tokens(tuples_list, tok_test)

    orig_map = {token_id: orig_token for token_id, _, orig_token in res}

    df["Original Token"] = df["Token id"].map(orig_map)

    print(df)
    df.to_excel("./results/aligned_tokens.xlsx", index=False)
    """
    filtered_df = df[df["C7 correct"].notna()]

    tuples_list = list(zip(filtered_df["Token id"], filtered_df["Token"]))
    # print(tuples_list)
    print(len(tok_test), len(tuples_list))

    # for i in range(len(tuples_list)):
    #    print(tuples_list[i][0], tuples_list[i][1], tok_test[i])
    res = align_tokens(tuples_list, tok_test)
    for thing in res:
        print(thing)
    df["Original Token"] = pd.Series(tok_test)

    df.to_excel("./results/aligned_tokens.xlsx", index=False)
    """

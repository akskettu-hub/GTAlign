import pandas as pd
import glob
from nltk.tokenize import word_tokenize
from CEEC_texts import get_CEEC_texts
from nw import align_words
from utils import load_tuple_list_from_json, save_tuple_list_to_json


def get_dfs_form_xlsx(path: str) -> dict[str, pd.DataFrame]:
    files = glob.glob(path + "*.xlsx")

    dfs_dict = {}
    for file in files:
        letter_id = file.split("/")[-1].replace(".xlsx", "")
        dfs_dict[letter_id] = {}
        dfs_dict[letter_id]["path"] = file
        dfs_dict[letter_id]["df"] = pd.read_excel(file)

    return dfs_dict


def tokenize_text(text: str) -> list[str]:
    tokenized_text = word_tokenize(text, language="english")

    return tokenized_text


def generate_alignment_tuple_list(ceec_text: str, df) -> list:
    tokenized_orig_text = tokenize_text(ceec_text)

    filtered_df = df[df["C7 correct"].notna()]
    tuples_list = list(zip(filtered_df["Token id"], filtered_df["Token"]))

    print(len(tokenized_orig_text), len(tuples_list))
    res = align_words(tuples_list, tokenized_orig_text)

    return res


def process_all_to_tuple_list(gt_dir_path: str) -> None:
    gts = get_dfs_form_xlsx(gt_dir_path)
    ceec_txt_dict = get_CEEC_texts(gts)

    for letter_id in gts.keys():
        print(letter_id)
        alignment_tuple = generate_alignment_tuple_list(
            ceec_txt_dict[letter_id], gts[letter_id]["df"]
        )
        save_tuple_list_to_json(alignment_tuple, "./results/alignments/", letter_id)


def save_to_excel(alignment_tuple_list: list[tuple], df, gt_key: str) -> None:
    orig_map = {
        token_id: orig_token for token_id, _, orig_token in alignment_tuple_list
    }

    insert_pos = df.columns.get_loc("><") + 1
    df.insert(insert_pos, "Original Token", df["Token id"].map(orig_map))

    print(df)
    df.to_excel(f"./results/{gt_key}.xlsx", index=False)


def alignment_lists_to_excel(alignment_tuple_dir_path: str, gt_dir_path: str) -> None:
    files = glob.glob(alignment_tuple_dir_path + "*.json")

    gts = get_dfs_form_xlsx(gt_dir_path)

    for file in files:
        print(file)
        letter_id = file.split("/")[-1].replace(".json", "")
        print(letter_id)

        df = gts[letter_id]["df"]
        alignment_tuple_list = load_tuple_list_from_json(file)

        save_to_excel(alignment_tuple_list, df, letter_id)

        print()


if __name__ == "__main__":
    # NOTE: Uncomment one of the below to generate alignment tuple lists or generate .xlsx from them.
    # NOTE: Only run one at a time. Alignment tuple lists need manual parsing.
    #
    alginment_tuples_dir_path = "./results/alignments/checked/"
    gt_dir_path = "./data/silver_standard/silver_standard/"
    process_all_to_tuple_list(gt_dir_path=gt_dir_path)
    # alignment_lists_to_excel(alignment_tuple_dir_path=alginment_tuples_dir_path, gt_dir_path=gt_dir_path)

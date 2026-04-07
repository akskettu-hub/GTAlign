import json


def save_tuple_list_to_json(data: list[tuple], dest_dir: str, file_name: str) -> None:
    with open(dest_dir + file_name + ".json", "w") as f:
        for item in data:
            f.write(json.dumps(item) + "\n")


def load_tuple_list_from_json(path: str) -> list[tuple]:
    with open(path) as f:
        data = [tuple(json.loads(line)) for line in f]
    return data


if __name__ == "__main__":
    pass

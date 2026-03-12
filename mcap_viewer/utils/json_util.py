import json
import os


def json_to_string(json_data):
    return json.dumps(json_data, ensure_ascii=False, indent=4)


def load_json(fp, nullable=True, default=None):
    if fp is None and nullable:
        return default
    elif not os.path.exists(fp):
        raise FileNotFoundError(fp)
    with open(fp, "r") as fr:
        text = fr.read().strip()
        if not text:
            return default
        try:
            data = json.loads(text)
            return data
        except Exception as e:
            print(fp, e)
            return default


def save_json(data, fname):
    with open(fname, "w") as f:
        if isinstance(data, str):
            text = data
        else:
            text = json.dumps(data, indent=4, ensure_ascii=False)
        f.write(text)
    return fname


def dumps_json(data):
    return json.dumps(data, indent=4, ensure_ascii=False)

from bs4 import BeautifulSoup  # type: ignore
from lxml import etree  # type: ignore
import json
import os


def get_filename(label_studio_str: str):
    split = label_studio_str.split("-")  # strip id
    full = "".join(split[1:])
    split = full.split(".")
    result = "".join(split[:-1])
    return result


def get_html_tree_from_string(html_string):
    soup = BeautifulSoup(html_string)
    dom = etree.HTML(str(soup))
    root = dom.getroottree()
    return root


def get_absolute_xpath(rel_xpath, dom):
    res = dom.xpath("/" + rel_xpath)[0]
    return dom.getpath(res.getparent())


def parse_export(ls_export):
    with open(ls_export, "r") as fin:
        export = json.load(fin)

    docs = []
    for i, annotated_doc in enumerate(export):
        filename = get_filename(annotated_doc["file_upload"])
        tree = get_html_tree_from_string(annotated_doc["data"]["text"])

        for j, annotations in enumerate(annotated_doc["annotations"]):
            if not annotations["result"]:
                continue
            for k, entety in enumerate(annotations["result"]):
                if entety.get("value"):
                    xpath_rel = entety["value"]["start"]
                    text = entety["value"]["text"]

                    xpath_abs = get_absolute_xpath(xpath_rel, tree)

                    export[i]["annotations"][j]["result"][k]["value"][
                        "start_abs"
                    ] = xpath_abs

                    # label = entety["value"]["labels"][0]

                    # offset = entety["value"]["globalOffsets"]
                    # doc["spots"].append({"xpath_rel": xpath, "label":label, "text":text, "offset":offset})
        # docs.append(doc)
    # return docs
    return export


if __name__ == "__main__":
    base_dir = "data"

    export_dir = os.path.join(base_dir, "export")

    print(parse_export(os.path.join(export_dir, "export_1.json")))

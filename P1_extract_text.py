import tarfile
from tqdm import tqdm
from pathlib import Path
import io
import json
import tempfile
import bs4
import jsonlines
from dspipe import Pipe
from wasabi import msg

f_tar = "data/source/opinions_all.tar"
f_save = "data/FreeLaw_Opinions.jsonl"


def jurisdiction_iter():

    # Handle nested tars
    with tarfile.open(f_tar, "r") as ALL:

        for packet in ALL:

            with tempfile.TemporaryDirectory() as tmp_dir:
                ALL.extract(packet, path=tmp_dir)
                f_subtar = Path(tmp_dir) / packet.name

                with open(f_subtar, "rb") as FIN:
                    raw = FIN.read()

                yield packet.name, io.BytesIO(raw)

            """
                with tarfile.open(f_subtar, "r") as TAR:
                    for k, subpacket in enumerate(TAR):

                        js = TAR.extractfile(subpacket).read()
                        yield packet.name, subpacket.name, js
            """


def idempotent(x):
    return x


def html2text(x):
    soup = bs4.BeautifulSoup(x, "lxml")
    return soup.get_text()


field_order = [
    ("plain_text", idempotent),
    ("html", html2text),
    ("html_lawbox", html2text),
    ("html_columbia", html2text),
    ("html_anon_2020", html2text),
    ("html_with_citations", html2text),
    ("xml_harvard", html2text),
]

error_str = (
    "Unable to extract the content from this file. Please try reading the original."
)


def parse_json(item):

    name0, name1, raw_str = item
    js = json.loads(raw_str)

    text = None

    if "html" in js and js["html"] == error_str:
        return None

    for k, func in field_order:
        if k in js and isinstance(js[k], str) and len(js[k]):
            text = func(js[k])

    if text is None:
        msg.fail(f"No text found for {name0} {name1}")
        return None

    meta = {}
    meta["case_jurisdiction"] = name0
    meta["case_ID"] = name1
    meta["date_created"] = js["date_created"]

    data = {"meta": meta, "text": text}

    return data


def data_iter(name0, tar_bytes):

    with tarfile.open(fileobj=tar_bytes) as TAR:
        for k, subpacket in enumerate(TAR):
            raw_json = TAR.extractfile(subpacket).read()
            name1 = subpacket.name
            yield name0, name1, raw_json


with jsonlines.open(f_save, "w") as FOUT:

    for name0, tar_bytes in jurisdiction_iter():
        msg.info(f"Processing {name0}")

        for js in Pipe(data_iter(name0, tar_bytes))(parse_json, -1):

            if js is None:
                continue

            FOUT.write(js)

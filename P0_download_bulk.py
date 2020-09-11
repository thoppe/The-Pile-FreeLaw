from pathlib import Path
import os

save_dest = Path("data/source")
save_dest.mkdir(exist_ok=True, parents=True)


def download_set(name):

    url = f"https://www.courtlistener.com/api/bulk-data/{name}/all.tar"
    f_save = save_dest / f"{name}_all.tar"

    if not f_save.exists():
        os.system(f"curl {url} -o {f_save}")


# Dockets look like detailed meta information, not text
# datasets = ['dockets', 'opinions']

datasets = ["opinions"]

for name in datasets:
    download_set(name)

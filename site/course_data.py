"""Download the original public Kaggle datasets to a local, reusable cache."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import tempfile
import urllib.request
import zipfile

DATASETS = {
    'ner': 'abhinavwalia95/entity-annotated-corpus',
    'body': 'tapakah68/segmentation-full-body-mads-dataset',
}

def fetch_dataset(name):
    slug = DATASETS[name]
    cache = Path(os.environ.get('XDG_CACHE_HOME', Path.home() / '.cache')) / 'ai-for-beginners' / name
    ready = cache / 'complete.json'
    if ready.is_file():
        return cache / 'files'
    cache.mkdir(parents=True, exist_ok=True)
    url = 'https://www.kaggle.com/api/v1/datasets/download/' + slug
    print('Downloading original dataset to local cache:', slug, flush=True)
    with tempfile.TemporaryDirectory(dir=cache) as temporary:
        temporary = Path(temporary)
        archive = temporary / 'dataset.zip'
        checksum = hashlib.sha256()
        with urllib.request.urlopen(url, timeout=120) as response, archive.open('wb') as output:
            prefix = response.read(8192)
            if not prefix.startswith(b'PK\x03\x04'):
                raise RuntimeError('Dataset endpoint did not return a ZIP. Download it from Kaggle and set the notebook local-data variable.')
            output.write(prefix)
            checksum.update(prefix)
            while chunk := response.read(1024 * 1024):
                output.write(chunk)
                checksum.update(chunk)
        extracted = temporary / 'files'
        extracted.mkdir()
        with zipfile.ZipFile(archive) as zipped:
            for item in zipped.infolist():
                target = (extracted / item.filename).resolve()
                if not target.is_relative_to(extracted.resolve()):
                    raise ValueError('Unsafe archive path')
            # Extraction validates each file's CRC; failed downloads never get a ready marker.
            zipped.extractall(extracted)
        if (cache / 'files').exists():
            raise RuntimeError('Incomplete previous extraction: inspect ' + str(cache / 'files'))
        shutil.move(str(extracted), cache / 'files')
        ready.write_text(json.dumps({'source': url, 'sha256': checksum.hexdigest()}, indent=2))
    return cache / 'files'

"""Cache the original CIFAR-10 archive for both framework notebooks.

Mirrors are accepted only when the archive matches Keras 3.5.0's SHA-256.
No samples or labels are replaced. CIFAR10_ARCHIVE can supply a local copy.
"""
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[1]
SHA256 = '6d958be074577803d12ecdefd02955f39262c83c16fe9348329d7fe0b5c001ce'
URLS = (
    'https://data.brainchip.com/dataset-mirror/cifar10/cifar-10-python.tar.gz',
    'https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz',
)

def verified(path):
    if not path.is_file():
        return False
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest() == SHA256

def main():
    cache = ROOT / '.cache' / 'cifar10'
    cache.mkdir(parents=True, exist_ok=True)
    archive = Path(os.environ.get('CIFAR10_ARCHIVE', cache / 'cifar-10-python.tar.gz')).resolve()
    if not verified(archive):
        if 'CIFAR10_ARCHIVE' in os.environ:
            raise ValueError('CIFAR10_ARCHIVE is missing or fails the official SHA-256 check')
        for url in URLS:
            partial = cache / 'download.partial'
            result = subprocess.run(['curl', '--fail', '--location', '--connect-timeout', '20',
                                     '--max-time', '240', '--retry', '1', '--output', str(partial), url])
            if result.returncode == 0 and verified(partial):
                partial.replace(archive)
                break
        else:
            raise RuntimeError('Original CIFAR-10 download unavailable; provide CIFAR10_ARCHIVE')
    keras_cache = Path(os.environ.get('KERAS_HOME', str(Path.home() / '.keras'))) / 'datasets'
    torch_cache = ROOT / 'lessons/4-ComputerVision/07-ConvNets/data'
    for target in (keras_cache, torch_cache):
        target.mkdir(parents=True, exist_ok=True)
        with tarfile.open(archive, 'r:gz') as source:
            source.extractall(target, filter='data')
    shutil.copyfile(archive, keras_cache / 'cifar-10-batches-py.tar.gz')
    print('CIFAR10_CACHE_VERIFIED', SHA256, 'original 50000 training + 10000 test images')

if __name__ == '__main__':
    main()

"""Prepare browser-compatible copies; preserve original lessons and training scope."""
import json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'lite-content'
SPECS = {
    'lessons/2-Symbolic/FamilyOntology.ipynb': ['python-gedcom==1.1.0', 'rdflib==7.1.4', 'owlrl==7.1.4', 'matplotlib'],
    'lessons/2-Symbolic/Animals.ipynb': ['matplotlib'],
    'lessons/3-NeuralNetworks/03-Perceptron/lab/PerceptronMultiClass.ipynb': ['numpy', 'matplotlib'],
    'lessons/3-NeuralNetworks/04-OwnFramework/lab/MyFW_MNIST.ipynb': ['numpy', 'scikit-learn'],
    'lessons/3-NeuralNetworks/03-Perceptron/Perceptron.ipynb': ['numpy', 'matplotlib', 'scikit-learn', 'ipywidgets'],
    'lessons/3-NeuralNetworks/04-OwnFramework/OwnFramework.ipynb': ['numpy', 'matplotlib', 'scikit-learn'],
    'lessons/6-Other/21-GeneticAlgorithms/Genetic.ipynb': ['numpy', 'matplotlib'],
}

def main():
    DEST.mkdir(exist_ok=True)
    for name, packages in SPECS.items():
        notebook = json.loads((ROOT / name).read_text())
        for cell in notebook['cells']:
            if cell['cell_type'] == 'code':
                cell['execution_count'] = None
                cell['outputs'] = []
        bootstrap = 'import piplite\nawait piplite.install(' + repr(packages) + ')\n%matplotlib inline\n'
        if name.endswith('/Animals.ipynb'):
            wheels = sorted((ROOT / 'website/wheels').glob('*.whl'))
            if len(wheels) != 3:
                raise RuntimeError('Build the three pure-Python expert-system wheels first')
            bootstrap += 'from urllib.parse import urljoin\nfrom js import location\n'
            bootstrap += 'await piplite.install([urljoin(str(location.href), \"../files/wheels/\" + name) for name in ' + repr([p.name for p in wheels]) + '])\n'
        notebook['cells'].insert(0, {'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [], 'source': bootstrap.splitlines(True)})
        notebook['cells'].insert(0, {'cell_type': 'markdown', 'metadata': {}, 'source': ['# 浏览器实践\n', '代码在你的浏览器中执行。首次运行需要下载 Python 和依赖包，请等待内核就绪。可拖入本地数据；修改保存在此浏览器，请下载 Notebook 备份。\n']})
        notebook['metadata']['kernelspec'] = {'display_name': 'Python (Pyodide)', 'language': 'python', 'name': 'python'}
        target = DEST / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + '\n')
    shutil.copytree(ROOT / 'lessons/2-Symbolic/data', DEST / 'lessons/2-Symbolic/data', dirs_exist_ok=True)
    shutil.copytree(ROOT / 'website/wheels', DEST / 'wheels', dirs_exist_ok=True)
    (DEST / 'data').mkdir(exist_ok=True)
    shutil.copy2(ROOT / 'data/mnist.pkl.gz', DEST / 'data/mnist.pkl.gz')
    (ROOT / 'website/browser-notebooks.json').write_text(json.dumps(list(SPECS), indent=2) + '\n')

if __name__ == '__main__':
    main()

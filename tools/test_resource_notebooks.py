"""Exercise complete resource-dependent notebooks; limit only NER training size."""
from pathlib import Path
import json
import nbformat
from nbclient import NotebookClient

ROOT=Path(__file__).resolve().parents[1]
specs={
 'lessons/4-ComputerVision/12-Segmentation/lab/BodySegmentation.ipynb': ('original preparation cells', '', 'assert img.shape[:2] == mask.shape[:2]'),
 'lessons/X-Extras/X1-MultiModal/Clip.ipynb': ('full pretrained inference', '', 'assert np.isfinite(probs).all() and np.allclose(probs.sum(axis=1),1)\nassert 0 <= int(res) < len(image_paths)'),
 'lessons/5-NLP/19-NER/NER-TF.ipynb': ('all cells; NER training uses 64 real sequences, one epoch', '''import tensorflow as tf
import numpy as np
original_fit=tf.keras.Model.fit
training_calls=[]
def small_fit(self,x,y=None,*args,**kwargs):
    kwargs['epochs']=1
    kwargs['batch_size']=32
    result=original_fit(self,x[:64],None if y is None else y[:64],*args,**kwargs)
    assert np.isfinite(result.history['loss']).all()
    training_calls.append(self.name)
    return result
tf.keras.Model.fit=small_fit
''', 'assert training_calls\nassert np.isfinite(res.numpy()).all()'),
}
results=[]
for name,(scope,before,after) in specs.items():
 path=ROOT/name;n=nbformat.read(path,as_version=4)
 if before:n.cells.insert(0,nbformat.v4.new_code_cell(before))
 n.cells.append(nbformat.v4.new_code_cell(after))
 try:
  NotebookClient(n,kernel_name='python3',timeout=600,resources={'metadata':{'path':str(path.parent)}}).execute()
  errors=[o for c in n.cells for o in c.get('outputs',[]) if o.output_type=='error']
  assert not errors,errors
  row={'path':name,'status':'passed','scope':scope}
 except Exception as error:
  row={'path':name,'status':'failed','scope':scope,'error':str(error)[-6000:]}
 results.append(row)
 print(json.dumps(row),flush=True)
 (ROOT/'resource-notebook-results.json').write_text(json.dumps(results,indent=2))
assert all(r['status']=='passed' for r in results),results

"""All-cell compatibility checks on real data with explicitly reduced training budgets.
These results never replace full-execution results or measure model quality.
"""
import argparse,json,re
from pathlib import Path
import nbformat
from nbclient import NotebookClient

ROOT=Path(__file__).resolve().parents[1]
SPECS={
 'gan_torch':'4-ComputerVision/10-GANs/GANPyTorch.ipynb',
 'autoencoders_torch':'4-ComputerVision/09-Autoencoders/AutoEncodersPyTorch.ipynb',
 'conv_torch':'4-ComputerVision/07-ConvNets/ConvNetsPyTorch.ipynb',
 'conv_tf':'4-ComputerVision/07-ConvNets/ConvNetsTF.ipynb',
 'transfer_torch':'4-ComputerVision/08-TransferLearning/TransferLearningPyTorch.ipynb',
 'transfer_tf':'4-ComputerVision/08-TransferLearning/TransferLearningTF.ipynb',
 'style_tf':'4-ComputerVision/10-GANs/StyleTransfer.ipynb',
 'adversarial_tf':'4-ComputerVision/08-TransferLearning/AdversarialCat_TF.ipynb',
 'cbow_torch':'5-NLP/15-LanguageModeling/CBoW-PyTorch.ipynb',
 'cbow_tf':'5-NLP/15-LanguageModeling/CBoW-TF.ipynb',
 'transformers_torch':'5-NLP/18-Transformers/TransformersPyTorch.ipynb',
 'generative_tf':'5-NLP/17-GenerativeNetworks/GenerativeTF.ipynb',
}
p=argparse.ArgumentParser();p.add_argument('lesson',choices=SPECS);a=p.parse_args()
path=ROOT/'lessons'/SPECS[a.lesson];n=nbformat.read(path,as_version=4)
changes=[]
for i,c in enumerate(n.cells):
 if c.cell_type!='code':continue
 source=c.source
 c.source=re.sub(r'\bepochs\s*=\s*\d+', 'epochs=2', c.source)
 c.source=re.sub(r'\bsteps_per_epoch\s*=\s*\d+', 'steps_per_epoch=2', c.source)
 c.source=re.sub(r'\biterations\s*=\s*\d+', 'iterations=2', c.source)
 if a.lesson.startswith('cbow_'):c.source=c.source.replace('range(10000)','range(32)')
 if a.lesson=='autoencoders_torch':c.source=c.source.replace('optimizer, 100, device','optimizer, 2, device')
 if a.lesson=='transfer_torch':
  c.source=c.source.replace('num = bs*100','num = bs*2').replace('[700,100]','[14,2]')
 if a.lesson=='transfer_tf':c.source=c.source.replace('batch_size = 64','batch_size = 4')
 if a.lesson=='transformers_torch':c.source=re.sub(r'batch_size\s*=\s*\d+','batch_size=2',c.source)
 if a.lesson=='adversarial_tf':
  c.source=c.source.replace('            x.assign_sub(eta*grads)', "            before = x.numpy().copy()\n            x.assign_sub(eta*grads)\n            tf.debugging.assert_all_finite(x, 'Non-finite image')\n            assert not np.array_equal(before, x.numpy())\n            compatibility_training_steps.append('pixel_gradient')")
 if c.source!=source:changes.append({'cell':i,'original':source,'validation_source':c.source})
bootstrap='''import numpy as np
compatibility_training_steps=[]
'''
if a.lesson.endswith('_torch'):
 bootstrap+='''import torch
from itertools import islice
original_iterator=torch.utils.data.DataLoader.__iter__
original_length=torch.utils.data.DataLoader.__len__
def two_batches(self):
    yield from islice(original_iterator(self),2)
torch.utils.data.DataLoader.__iter__=two_batches
torch.utils.data.DataLoader.__len__=lambda self:min(2,original_length(self))
def checked_step(original):
    def step(self,*args,**kwargs):
        result=original(self,*args,**kwargs)
        parameters=[p for group in self.param_groups for p in group['params'] if p.grad is not None]
        assert parameters, 'No gradients in optimizer update'
        assert all(torch.isfinite(p).all() for p in parameters), 'Non-finite model weights'
        compatibility_training_steps.append(type(self).__name__)
        return result
    return step
for optimizer_type in (torch.optim.Adam,torch.optim.SGD,torch.optim.RMSprop):
    optimizer_type.step=checked_step(optimizer_type.step)
'''
else:
 bootstrap+='''import tensorflow as tf
original_fit=tf.keras.Model.fit
def limited_fit(self,x,y=None,*args,**kwargs):
    if isinstance(x,tf.data.Dataset):x=x.take(2)
    else:
        x=x[:128]
        if y is not None:y=y[:128]
    validation=kwargs.get('validation_data')
    if isinstance(validation,tf.data.Dataset):kwargs['validation_data']=validation.take(1)
    elif isinstance(validation,tuple):kwargs['validation_data']=tuple(v[:64] for v in validation)
    kwargs['epochs']=1
    if 'steps_per_epoch' in kwargs:kwargs['steps_per_epoch']=2
    if 'validation_steps' in kwargs:kwargs['validation_steps']=1
    result=original_fit(self,x,y,*args,**kwargs)
    assert np.isfinite(result.history['loss']).all(), 'Non-finite training loss'
    compatibility_training_steps.append(self.name)
    return result
tf.keras.Model.fit=limited_fit
original_apply=tf.keras.optimizers.Optimizer.apply_gradients
def checked_apply(self,grads_and_vars,*args,**kwargs):
    pairs=list(grads_and_vars)
    assert pairs and all(g is not None for g,v in pairs), 'Missing gradients'
    for g,v in pairs:
        tf.debugging.assert_all_finite(g.values if isinstance(g,tf.IndexedSlices) else g, 'Non-finite gradients')
    result=original_apply(self,pairs,*args,**kwargs)
    compatibility_training_steps.append(type(self).__name__)
    return result
tf.keras.optimizers.Optimizer.apply_gradients=checked_apply
'''
n.cells.insert(0,nbformat.v4.new_code_cell(bootstrap))
n.cells.append(nbformat.v4.new_code_cell("assert compatibility_training_steps, 'No actual training occurred'\nprint('ACTUAL_TRAINING_UPDATES', len(compatibility_training_steps))"))
result={'path':str(path.relative_to(ROOT)),'scope':'all cells; original data and models, bounded epochs and batches','source_adjustments':changes}
try:
 NotebookClient(n,kernel_name='python3',timeout=900,resources={'metadata':{'path':str(path.parent)}}).execute()
 errors=[o for c in n.cells for o in c.get('outputs',[]) if o.output_type=='error']
 assert not errors,errors
 result['status']='passed'
except Exception as error:
 result.update(status='failed',error=re.sub(r'\x1b\[[0-9;]*m','',str(error))[-7000:])
out=ROOT/'compatibility-results';out.mkdir(exist_ok=True)
(out/(a.lesson+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in result.items() if k!='source_adjustments'},ensure_ascii=False),flush=True)
assert result['status']=='passed',result.get('error')

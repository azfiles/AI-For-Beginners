"""Execute original notebook cells in isolated processes; retain failures."""
from pathlib import Path
import argparse, concurrent.futures, contextlib, hashlib, io, json, os, subprocess, sys, time, traceback, shutil, tempfile, signal
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser()
p.add_argument("--root");p.add_argument("--progress");p.add_argument("--one");p.add_argument("--workers",type=int,default=4)
p.add_argument("--timeout",type=int,default=120);a=p.parse_args()
if a.root:ROOT=Path(a.root)
if a.one:
    from IPython.terminal.interactiveshell import TerminalInteractiveShell
    path=ROOT/a.one;notebook=json.loads(path.read_text())
    os.chdir(path.parent);sys.path.insert(0,str(path.parent))
    shell=TerminalInteractiveShell.instance();output=io.StringIO();count=0;index=-1
    try:
        with contextlib.redirect_stdout(output),contextlib.redirect_stderr(output):
            for index,cell in enumerate(notebook["cells"]):
                if cell["cell_type"]!="code":continue
                code="".join(cell.get("source",[]))
                if not code.strip():continue
                result=shell.run_cell(code,store_history=True)
                if result.error_before_exec:raise result.error_before_exec
                if result.error_in_exec:raise result.error_in_exec
                count+=1
                if a.progress:Path(a.progress).write_text(json.dumps({"executed_cells":count,"cell_index":index}))
        if "❌ Error:" in output.getvalue():
            raise RuntimeError("Notebook printed a runtime error: "+output.getvalue()[-2000:])
        result={"status":"passed","executed_cells":count}
    except Exception as e:
        result={"status":"manual_input" if isinstance(e,EOFError) else "failed",
                "executed_cells":count,"cell_index":index,"error":str(e),
                "traceback":traceback.format_exc()[-4000:]}
    print(json.dumps(result));sys.exit(0)
paths=sorted(list((ROOT/"lessons").rglob("*.ipynb"))+list((ROOT/"examples").rglob("*.ipynb")))
tracked=set(subprocess.check_output(["git","ls-files"],cwd=ROOT,text=True).splitlines())
paths=[x for x in paths if str(x.relative_to(ROOT)) in tracked]
def run(path):
    rel=str(path.relative_to(ROOT));n=json.loads(path.read_text());start=time.monotonic()
    code="\n".join("".join(c.get("source",[])) for c in n["cells"] if c["cell_type"]=="code")
    category="exercise" if "/lab/" in rel else "experimental" if path.name in ("tmp.ipynb","notebook.ipynb") else "lesson"
    if not code.strip():return {"path":rel,"category":category,"status":"no_code"}
    env=dict(os.environ,OMP_NUM_THREADS="1",OPENBLAS_NUM_THREADS="1",
        TF_NUM_INTEROP_THREADS="1",TF_NUM_INTRAOP_THREADS="1",TOKENIZERS_PARALLELISM="false",
        MPLBACKEND="Agg",PIP_CONSTRAINT=str(ROOT/"site/requirements-advanced.txt"))
    try:
        with tempfile.TemporaryDirectory(prefix="ai4beg-") as directory:
            isolated=Path(directory)
            # Copy tracked source only: downloads and image cleanup cannot race across notebooks.
            chapter=path.parent.parent if path.parent.name=="lab" else path.parent
            prefix=str(chapter.relative_to(ROOT))+"/"
            for name in tracked:
                if name.startswith((prefix,"data/","site/")):
                    source=ROOT/name
                    if source.is_file():
                        target=isolated/name;target.parent.mkdir(parents=True,exist_ok=True)
                        shutil.copy2(source,target)
            progress=isolated/"progress.json"
            proc=subprocess.Popen([sys.executable,__file__,"--root",str(isolated),"--one",rel,"--progress",str(progress)],
                stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env=env,start_new_session=True)
            try:
                stdout,stderr=proc.communicate(timeout=a.timeout)
                result=json.loads(stdout.strip().splitlines()[-1]) if stdout.strip() else {"status":"failed","error":stderr[-3000:] or f"Exit code {proc.returncode}"}
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid,signal.SIGKILL);proc.communicate()
                result=json.loads(progress.read_text()) if progress.exists() else {}
                result.update(status="timeout",error=f"Full execution exceeded {a.timeout}s; not verified.")
    except subprocess.TimeoutExpired:result={"status":"timeout","error":f"Full execution exceeded {a.timeout}s; not verified."}
    except Exception as e:result={"status":"failed","error":str(e)}
    result.update(path=rel,category=category,seconds=round(time.monotonic()-start,1),code_sha256=hashlib.sha256(code.encode()).hexdigest())
    print(json.dumps(result,ensure_ascii=False),flush=True);return result
out=ROOT/"validation";out.mkdir(exist_ok=True);results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as pool:
    futures={pool.submit(run,path):path for path in paths}
    for future in concurrent.futures.as_completed(futures):
        results.append(future.result())
        (out/"notebooks.json").write_text(json.dumps(results,ensure_ascii=False,indent=2))
for path in sorted((ROOT/"examples").glob("*.py")):
    try:
        r=subprocess.run([sys.executable,str(path)],input="quit\n",capture_output=True,text=True,timeout=60,cwd=ROOT)
        result={"path":str(path.relative_to(ROOT)),"category":"script","status":"passed" if r.returncode==0 else "failed","output":r.stdout,"error":r.stderr}
    except subprocess.TimeoutExpired:result={"path":str(path.relative_to(ROOT)),"category":"script","status":"timeout"}
    results.append(result)
(out/"results.json").write_text(json.dumps(results,ensure_ascii=False,indent=2))
print(json.dumps({s:sum(x["status"]==s for x in results) for s in {x["status"] for x in results}}),flush=True)
sys.exit(any(x["status"]!="passed" for x in results if x["category"] in ("lesson","script") and x["status"]!="no_code"))

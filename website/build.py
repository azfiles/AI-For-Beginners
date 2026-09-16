"""Build static Chinese curriculum pages with local assets and notebook source views."""
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit
from html.parser import HTMLParser
import html, json, re, shutil, subprocess
import markdown
from prepare_lite import SPECS
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/"site-dist";ZH="translations/zh-CN/"
OUT.mkdir(exist_ok=True)
REPO="https://github.com/azfiles/AI-For-Beginners"
_validation_file = ROOT / "website/validation-status.json"
VALIDATION = json.loads(_validation_file.read_text())["files"] if _validation_file.exists() else {}
_status_file = ROOT / "website/notebook-status.json"
NOTEBOOK_STATUS = json.loads(_status_file.read_text()) if _status_file.exists() else {}
BLOCKED = NOTEBOOK_STATUS.get("blocked", {})
SHORT_VERIFIED = NOTEBOOK_STATUS.get("short_verified", {})
REV=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
tracked=subprocess.check_output(["git","ls-files"],cwd=ROOT,text=True).splitlines()
files={key:ROOT/key for key in tracked if (key.startswith(("lessons/","examples/")) and "/translations/" not in key and Path(key).suffix in (".md",".ipynb",".py")) or (key.startswith(ZH) and key.endswith(".md") and Path(key).name not in ("AGENTS.md","CONTRIBUTING.md","SECURITY.md")) or key in ("site/RUNNING.zh-CN.md", "site/VALIDATION.zh-CN.md")}
aliases={key:ZH+key if ZH+key in files else key for key in files}
def route(key):return "/pages/"+quote(aliases.get(key,key),safe="/")+".html"
def notebook_status(source):
    record = VALIDATION.get(source, {})
    if source in BLOCKED:
        return ("blocked", BLOCKED[source]["label"], BLOCKED[source]["note"])
    if source in SPECS:
        return ("verified", "浏览器运行已验证", "代码直接在当前浏览器中运行")
    if record.get("full_status") == "passed":
        return ("verified", "完整执行已验证", record.get("note", ""))
    if source in SHORT_VERIFIED or record.get("short_test"):
        item = SHORT_VERIFIED.get(source, {})
        scope = item.get("scope") or record.get("short_test", {}).get("scope") or record.get("note", "")
        return ("testing", "短训练已验证 · 完整训练验证中", scope)
    if record.get("full_status") == "no_code":
        return ("info", "说明型 Notebook", "没有可执行代码")
    return ("testing", "验证中", record.get("note") or "等待当前完整审计结果")
def status_html(source):
    kind, label, note = notebook_status(source)
    detail = '<small class="status-note">'+html.escape(note)+'</small>' if note else ''
    return '<span class="status '+kind+'">'+html.escape(label)+'</span>'+detail
def notebook_actions(source, browser=False):
    download = '<a class="download-link" href="/downloads/'+quote(source,safe="/")+'" download>下载 .ipynb（本地运行）</a>'
    if not browser:
        return '<div class="notebook-actions">'+download+'<a class="source-link" href="'+REPO+'/blob/'+REV+'/'+quote(source,safe="/")+'">查看源码</a></div>'
    run = '<a class="browser-link" href="/lite/lab/index.html?path='+quote(source,safe="/")+'">浏览器运行 Notebook ▶</a>'
    return '<div class="notebook-actions">'+run+download+'<a class="source-link" href="'+REPO+'/blob/'+REV+'/'+quote(source,safe="/")+'">查看源码</a></div>'
def title(md,fallback):
    match=re.search(r"^#\s+(.+)",md,re.M)
    return re.sub(r"<[^>]*>|[*\x60]", "", match.group(1)) if match else fallback
issues=[];assets=set()
fixes={
"lessons/3-NeuralNetworks/05-Frameworks/IntroKerasTF.md":"lessons/3-NeuralNetworks/05-Frameworks/IntroKerasTF.ipynb",
"lessons/3-NeuralNetworks/05-Frameworks/Overfitting.md":"lessons/3-NeuralNetworks/05-Frameworks/README.md",
"lessons/5-NLP/20-LanguageModels/README.md":"lessons/5-NLP/20-LangModels/README.md",
"lessons/4-ComputerVision/11-ObjectDetection/ObjectDetection-TF.ipynb":"lessons/4-ComputerVision/11-ObjectDetection/ObjectDetection.ipynb"}
def resolve(url,source):
    url=html.unescape(url)
    if not url or url.startswith(("#","data:","mailto:")):return url
    u=urlsplit(url);path=unquote(u.path);fragment="#"+u.fragment if u.fragment else ""
    if u.netloc:
        if u.netloc.lower() in ("github.com","raw.githubusercontent.com"):
            match=re.match(r"/(?:microsoft|azfiles)/AI-For-Beginners/(?:blob/|raw/)?(?:main|master)/(.*)",path,re.I)
            if not match:return url
            path=match.group(1)
        elif u.netloc=="microsoft.github.io" and path.startswith("/AI-For-Beginners/"):path=path[len("/AI-For-Beginners/"):]
        else:return url
    else:
        candidate=(ROOT/Path(source).parent/path).resolve()
        if not candidate.is_relative_to(ROOT):return url
        path=str(candidate.relative_to(ROOT))
    if path==".":return "/"
    if path.startswith(ZH) and not (ROOT/path).is_file():path=path[len(ZH):]
    if path=="lessons/4-ComputerVision/11-ObjectDetection/lab/PASCAL VOC":return "https://host.robots.ox.ac.uk/pascal/VOC/"
    # Translated pages can retain a translations/zh-CN prefix in relative links.
    # Normalize it before matching the browser-supported source Notebook.
    if "lessons/" in path and path[path.index("lessons/"):] in SPECS:
        path = path[path.index("lessons/"):]
    path=fixes.get(path,path)
    # Point curriculum links at the browser kernel when a Pyodide copy exists.
    # Keep the explicit download button on Notebook pages for exporting work.
    if path in SPECS:
        return "/lite/lab/index.html?path="+quote(path,safe="/")+fragment
    if path in files:return route(path)+fragment
    p=ROOT/path
    if not p.exists():
        matches=[x for x in p.parent.glob("*") if x.name.lower()==p.name.lower()]
        if len(matches)==1:p=matches[0];path=str(p.relative_to(ROOT))
    if "translated_images/zh-CN/DALL" in path and not p.is_file():
        needle=p.name.rsplit(".",2)[0]
        matches=list((ROOT/"lessons/X-Extras/X1-MultiModal/images").glob(needle+"*"))
        if len(matches)==1:p=matches[0];path=str(p.relative_to(ROOT))
    if p.is_dir():return REPO+"/tree/"+REV+"/"+quote(path,safe="/")+fragment
    if p.is_file():
        dest=OUT/"assets"/path;dest.parent.mkdir(parents=True,exist_ok=True)
        if path not in assets:shutil.copyfile(p,dest);assets.add(path)
        return "/assets/"+quote(path,safe="/")+fragment
    if path.startswith("translations/") and not path.startswith(ZH):return REPO+"/blob/"+REV+"/"+quote(path,safe="/")+fragment
    issues.append({"source":source,"target":url})
    return REPO+"/blob/"+REV+"/"+quote(path,safe="/")+fragment
def render(md,source):
    maths=[]
    def protect(match):maths.append(match.group(0));return "MATHPLACEHOLDER"+str(len(maths)-1)+"END"
    md=re.sub(r"\$\$[\s\S]+?\$\$|\\\[[\s\S]+?\\\]|\\\([^\n]+?\\\)|(?<!\$)\$(?!\s)[^\n$]+?(?<!\s)\$(?!\$)",protect,md)
    body=markdown.markdown(md,extensions=["tables","fenced_code","toc","sane_lists"])
    for i,value in enumerate(maths):body=body.replace("MATHPLACEHOLDER"+str(i)+"END",html.escape(value))
    body=re.sub(r"""(href|src)=["']([^"']*)["']""",lambda m:m.group(1)+'="'+html.escape(resolve(m.group(2),source),quote=True)+'"',body)
    def decorate(match):
        target=unquote(match.group(1))
        params=re.search(r"(?:^|&)path=([^&]+)",urlsplit(target).query)
        if not params:return match.group(0)
        notebook=unquote(params.group(1))
        if notebook not in SPECS:return match.group(0)
        label=re.sub(r"<[^>]+>","",match.group(2)).strip() or Path(notebook).name
        return '<span class="inline-notebook">'+status_html(notebook)+'<span class="inline-notebook-actions"><a class="browser-link" href="'+html.escape(target,quote=True)+'">浏览器运行：'+html.escape(label)+'</a><a class="download-link" href="/downloads/'+quote(notebook,safe="/")+'" download>下载 .ipynb</a></span></span>'
    return re.sub(r'<a href="([^"]*?/lite/lab/index\.html\?[^"]+)">([\s\S]*?)</a>',decorate,body)
readme=(ROOT/ZH/"README.md").read_text();rows=[]
for line in readme.splitlines():
    if re.match(r"\|\s*\d+\s*\|",line):
        m=re.search(r"\[([^\]]+)\]\(([^)]+\.md)\)",line)
        if m:rows.append((line.split("|")[1].strip(),m.group(1),ZH+m.group(2).removeprefix("./")))
def shell(name,body,source=""):
    nav='<a href="/">课程目录</a><a href="/notebooks.html">运行 Notebook</a><a href="'+route("site/RUNNING.zh-CN.md")+'">运行说明与验证范围</a><a href="'+route(ZH+"README.md")+'">完整课程说明</a><p class="label">12 周 · 系统学习</p>'
    for num,label,key in rows:nav+='<a href="'+route(key)+'"'+(' aria-current="page"' if aliases.get(source,source)==key else '')+'>'+num.zfill(2)+' &nbsp; '+html.escape(label)+'</a>'
    return '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Microsoft AI-For-Beginners 中文课程与代码实践"><title>'+html.escape(name)+' · AI 入门</title><link rel="stylesheet" href="/style.css"><link rel="icon" href="/favicon.svg"><link rel="stylesheet" href="/vendor/katex/katex.min.css"><script defer src="/vendor/katex/katex.min.js"></script><script defer src="/vendor/katex/contrib/auto-render.min.js"></script><script defer src="/math.js"></script></head><body><header><a class="brand" href="/"><b>AI</b> 入门 · 中文学习站</a><a href="'+REPO+'">GitHub 源码 ↗</a></header><div class="shell"><nav aria-label="课程导航">'+nav+'</nav><main>'+body+'<footer>课程 © Microsoft · <a href="/LICENSE.txt">MIT 许可证</a> · 中文来自上游 Co-op Translator，原文为准。<br>Notebook 注释保留原语言。来源版本 '+REV[:8]+'</footer></main></div></body></html>'
for source,path in files.items():
    if aliases[source]!=source:continue
    if path.suffix==".md":
        md=path.read_text();name=title(md,path.stem);body='<p class="label">AI FOR BEGINNERS / 中文课程</p>'+render(md,source)
    else:
        name=path.stem;body='<p class="label">动手实践 / '+("NOTEBOOK" if path.suffix==".ipynb" else "PYTHON")+'</p><h1>'+html.escape(name)+'</h1>'
        dest=OUT/"downloads"/source;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,dest)
        if source in SPECS:
            body+='<div class="notice">'+status_html(source)+'<br>此 Notebook 支持浏览器内执行。首次运行需加载 Python 和依赖，数据可从本机拖入；请下载备份你的修改。'+('本页为练习模板，需自行完成题目。' if '/lab/' in source else '')+'</div>'+notebook_actions(source,True)
        else:
            body+='<div class="notice">'+(status_html(source)+'<br>' if path.suffix==".ipynb" else '')+'此代码使用完整 Python 环境。请先按<a href="'+route("site/RUNNING.zh-CN.md")+'">运行说明</a>准备依赖和数据，并查看当前验证范围。</div>'
            body+=notebook_actions(source,False) if path.suffix==".ipynb" else '<div class="notebook-actions"><a class="download-link" href="/downloads/'+quote(source,safe="/")+'" download>下载代码（本地运行）</a><a class="source-link" href="'+REPO+'/blob/'+REV+'/'+quote(source,safe="/")+'">查看源码</a></div>'
        if path.suffix==".ipynb":body+='<div class="secondary-actions"><a href="https://colab.research.google.com/github/azfiles/AI-For-Beginners/blob/'+REV+'/'+quote(source,safe="/")+'">在 Colab 打开 ↗</a></div>'
        if path.suffix==".py":body+="<pre><code>"+html.escape(path.read_text())+"</code></pre>"
        else:
            for cell in json.loads(path.read_text()).get("cells",[]):
                code="".join(cell.get("source",[]))
                body+=render(code,source) if cell["cell_type"]=="markdown" else "<pre><code>"+html.escape(code)+"</code></pre>" if cell["cell_type"]=="code" else ""
    out=OUT/"pages"/(source+".html");out.parent.mkdir(parents=True,exist_ok=True);out.write_text(shell(name,body,source))
notebooks='<h1>运行 Notebook</h1><p>每个 Notebook 都提供本地下载；带蓝色“浏览器运行”按钮的课程还能直接在本站执行。</p><div class="legend"><span class="status verified">已验证可运行</span><span class="status testing">验证中 / 完整训练验证中</span><span class="status blocked">需要数据或凭据</span></div><div class="audit-banner"><b>当前验证说明：</b>统一全单元短训练已通过；原始训练规模的完整审计仍在进行。状态会区分两种验证范围。</div><h2>浏览器内运行</h2><p>打开后等待内核就绪，选择「运行 → 运行所有单元格」。修改保存在当前浏览器，请下载 Notebook 备份。</p><div class="notebook-list">'
for source in SPECS:
    notebooks+='<article class="notebook-row"><div><h3>'+html.escape(Path(source).stem)+'</h3>'+status_html(source)+(' <small>练习准备代码</small>' if '/lab/' in source else '')+'</div>'+notebook_actions(source,True)+'</article>'
notebooks+='</div><h2>完整 Python 环境</h2><p>这些 Notebook 使用本机 Python、TensorFlow 或 PyTorch。请按<a href="'+route("site/RUNNING.zh-CN.md")+'">运行说明</a>准备环境。</p><div class="notebook-list">'
for source in sorted(files):
    if source.endswith('.ipynb') and source not in SPECS:
        notebooks+='<article class="notebook-row"><div><h3><a href="'+route(source)+'">'+html.escape(source.removeprefix('lessons/'))+'</a></h3>'+status_html(source)+'</div>'+notebook_actions(source,False)+'</article>'
notebooks+='</div>'
(OUT/'notebooks.html').write_text(shell('运行 Notebook',notebooks))
body='<p class="label">AI FOR BEGINNERS / 简体中文</p><h1>人工智能，从理解到实践</h1><p>12 周 · 24 课 · 附多模态拓展<br>阅读中文讲义，结合 Python、PyTorch 与 TensorFlow 完成动手练习。</p><div class="actions"><a href="'+route(rows[1][2])+'">阅读第一课</a><a href="/notebooks.html">运行 Notebook</a><a href="'+route("site/RUNNING.zh-CN.md")+'">准备运行环境</a></div><h2>课程目录</h2>'
body+=render(readme[readme.index("|     |"):readme.index("## 每节课包含")],ZH+"README.md")
(OUT/"index.html").write_text(shell("课程目录",body))
for filename in ("style.css","math.js","favicon.svg"):shutil.copyfile(ROOT/"website"/filename,OUT/filename)
shutil.copyfile(ROOT/"LICENSE",OUT/"LICENSE.txt")
shutil.copytree(ROOT/"website/vendor/katex",OUT/"vendor/katex",dirs_exist_ok=True)
(OUT/"source-link-report.json").write_text(json.dumps(issues,ensure_ascii=False,indent=2))
class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
        for key,value in attrs:
            if key in ("src","href") and value and value.startswith("/") and not value.startswith("//"):
                target=OUT/unquote(urlsplit(value).path).lstrip("/")
                if target==OUT:target=OUT/"index.html"
                if not target.exists():raise ValueError("Missing local asset: "+value)
for page in OUT.rglob("*.html"):
    if not page.is_relative_to(OUT/'lite'):Links().feed(page.read_text())
print(json.dumps({"pages":len(list(OUT.rglob("*.html"))),"local_assets":len(assets),"upstream_links_to_review":len(issues),"commit":REV}))

print(json.dumps({'source_links_to_review':issues},ensure_ascii=False))

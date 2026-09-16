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
VALIDATION=json.loads((ROOT/"website/validation-status.json").read_text())["files"]
REV=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
tracked=subprocess.check_output(["git","ls-files"],cwd=ROOT,text=True).splitlines()
files={key:ROOT/key for key in tracked if (key.startswith(("lessons/","examples/")) and "/translations/" not in key and Path(key).suffix in (".md",".ipynb",".py")) or (key.startswith(ZH) and key.endswith(".md") and Path(key).name not in ("AGENTS.md","CONTRIBUTING.md","SECURITY.md")) or key in ("site/RUNNING.zh-CN.md", "site/VALIDATION.zh-CN.md")}
aliases={key:ZH+key if ZH+key in files else key for key in files}
def route(key):return "/pages/"+quote(aliases.get(key,key),safe="/")+".html"
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
    return re.sub(r"""(href|src)=["']([^"']*)["']""",lambda m:m.group(1)+'="'+html.escape(resolve(m.group(2),source),quote=True)+'"',body)
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
            body+='<div class="notice">此 Notebook 支持浏览器内执行。首次运行需加载 Python 和依赖，数据可从本机拖入；请下载备份你的修改。'+('本页为练习模板，需自行完成题目。' if '/lab/' in source else '')+'</div><div class="actions"><a href="/lite/lab/index.html?path='+quote(source,safe="/")+'">在 Site 运行 ▶</a>'
        else:
            body+='<div class="notice">此代码使用完整 Python 环境。请先按<a href="'+route("site/RUNNING.zh-CN.md")+'">运行说明</a>准备依赖和数据，并查看当前验证范围。</div><div class="actions">'
        body+='<a href="/downloads/'+quote(source,safe="/")+'" download>下载代码</a><a href="'+REPO+'/blob/'+REV+'/'+quote(source,safe="/")+'">查看源码</a>'
        if path.suffix==".ipynb":body+='<a href="https://colab.research.google.com/github/azfiles/AI-For-Beginners/blob/'+REV+'/'+quote(source,safe="/")+'">在 Colab 打开 ↗</a>'
        body+="</div>"
        if path.suffix==".py":body+="<pre><code>"+html.escape(path.read_text())+"</code></pre>"
        else:
            for cell in json.loads(path.read_text()).get("cells",[]):
                code="".join(cell.get("source",[]))
                body+=render(code,source) if cell["cell_type"]=="markdown" else "<pre><code>"+html.escape(code)+"</code></pre>" if cell["cell_type"]=="code" else ""
    out=OUT/"pages"/(source+".html");out.parent.mkdir(parents=True,exist_ok=True);out.write_text(shell(name,body,source))
notebooks='<h1>运行 Notebook</h1><p>选择课程，边阅读边执行。浏览器内运行使用你当前设备的算力；完整 Python 课程请准备本机环境。</p><h2>浏览器内运行</h2><p>打开后等待内核就绪，选择「运行 → 运行所有单元格」。可拖入本机数据，也可下载修改后的 Notebook。</p><ul>'
for source in SPECS:
    notebooks+='<li><a href="/lite/lab/index.html?path='+quote(source,safe="/")+'">'+html.escape(Path(source).stem)+'</a>'+(' · 练习准备代码' if '/lab/' in source else '')+'</li>'
notebooks+='</ul><h2>完整 Python 环境</h2><p>下列 Notebook 保留原版框架。安装说明、数据要求与验证结果请见<a href="'+route("site/RUNNING.zh-CN.md")+'">运行说明</a>。</p><ul>'
for source in sorted(files):
    if source.endswith('.ipynb') and source not in SPECS:
        record=VALIDATION.get(source,{})
        detail=record.get('label','未验证') + ('；'+record['note'] if record.get('note') else '')
        notebooks+='<li><a href="'+route(source)+'">'+html.escape(source.removeprefix('lessons/'))+'</a><br><small>'+html.escape(detail)+'</small></li>'
notebooks+='</ul>'
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

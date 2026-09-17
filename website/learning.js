(() => {
  "use strict";

  const STORAGE_KEY = "ai-beginners-learning-v1";
  const body = document.body;
  const main = document.querySelector("main");
  const openButton = document.querySelector("#learning-open");
  if (!main || !openButton) return;

  const page = {
    path: location.pathname,
    title: body.dataset.pageTitle || document.title.replace(" · AI 入门", ""),
    source: body.dataset.source || "",
    isCourse: body.dataset.coursePage === "true",
  };
  const totalLessons = Number(body.dataset.totalLessons || 0);

  const load = () => {
    try {
      const value = JSON.parse(localStorage.getItem(STORAGE_KEY) || "null");
      if (value && value.version === 1 && Array.isArray(value.notes) && value.completed) return value;
    } catch (_) {}
    return { version: 1, notes: [], completed: {} };
  };
  let state = load();
  const save = () => localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  const id = () => (crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random().toString(16).slice(2)}`);
  const formatDate = (value) => {
    try { return new Intl.DateTimeFormat("zh-CN", { dateStyle: "medium", timeStyle: "short" }).format(new Date(value)); }
    catch (_) { return "未知时间"; }
  };
  const safePath = (value) => typeof value === "string" && value.startsWith("/") && !value.startsWith("//") ? value : "/";
  const blocks = () => [...main.querySelectorAll("p,li,h2,h3,blockquote")].filter((element) => !element.closest(".learning-progress-card, .learning-drawer"));

  const backdrop = document.createElement("div");
  backdrop.className = "learning-backdrop";
  backdrop.hidden = true;
  const drawer = document.createElement("aside");
  drawer.className = "learning-drawer";
  drawer.id = "learning-drawer";
  drawer.setAttribute("aria-label", "个人学习记录");
  drawer.setAttribute("aria-hidden", "true");
  drawer.innerHTML = `
    <div class="learning-drawer-head">
      <div><span class="learning-eyebrow">仅保存在此浏览器</span><h2>个人学习记录</h2></div>
      <button class="learning-icon-button" type="button" data-learning-close aria-label="关闭学习记录">×</button>
    </div>
    <div class="learning-summary" aria-live="polite"></div>
    <div class="learning-tabs" role="tablist" aria-label="学习记录内容">
      <button type="button" role="tab" aria-selected="true" data-learning-tab="notes">文字笔记</button>
      <button type="button" role="tab" aria-selected="false" data-learning-tab="progress">学习进度</button>
    </div>
    <section data-learning-panel="notes">
      <label class="learning-filter"><input type="checkbox" data-current-page-only> 只看当前页面</label>
      <div class="learning-note-list"></div>
    </section>
    <section data-learning-panel="progress" hidden>
      <div class="learning-progress-list"></div>
    </section>
    <div class="learning-data-actions">
      <button type="button" data-learning-export>导出备份</button>
      <label class="learning-import">导入备份<input type="file" accept="application/json" data-learning-import></label>
    </div>
    <p class="learning-local-note">笔记与进度使用浏览器本地存储。更换浏览器、设备或清理网站数据前，请先导出备份。</p>`;
  document.body.append(backdrop, drawer);

  const editor = document.createElement("dialog");
  editor.className = "learning-editor";
  editor.innerHTML = `
    <form method="dialog">
      <div class="learning-editor-head"><h2>添加文字笔记</h2><button class="learning-icon-button" value="cancel" aria-label="关闭">×</button></div>
      <blockquote data-learning-quote></blockquote>
      <label>我的笔记<textarea rows="5" maxlength="4000" placeholder="写下理解、疑问或待复习内容……"></textarea></label>
      <div class="learning-editor-actions"><button value="cancel">取消</button><button class="learning-primary" value="save">保存笔记</button></div>
    </form>`;
  document.body.append(editor);

  const selectionButton = document.createElement("button");
  selectionButton.type = "button";
  selectionButton.className = "selection-note-button";
  selectionButton.textContent = "添加笔记";
  selectionButton.hidden = true;
  document.body.append(selectionButton);

  let pendingSelection = null;
  const updateBadge = () => {
    const completed = Object.keys(state.completed).length;
    openButton.querySelector("span").textContent = totalLessons ? `${Math.min(completed, totalLessons)}/${totalLessons}` : `${state.notes.length}`;
  };

  const renderSummary = () => {
    const completed = Object.keys(state.completed).length;
    const percent = totalLessons ? Math.min(100, Math.round((completed / totalLessons) * 100)) : 0;
    const summary = drawer.querySelector(".learning-summary");
    summary.innerHTML = `<div><b>${completed}</b><span>已完成课程</span></div><div><b>${state.notes.length}</b><span>文字笔记</span></div><div><b>${percent}%</b><span>总体进度</span></div>`;
  };

  const renderNotes = () => {
    const onlyCurrent = drawer.querySelector("[data-current-page-only]").checked;
    const notes = [...state.notes]
      .filter((note) => !onlyCurrent || note.path === page.path)
      .sort((a, b) => b.createdAt.localeCompare(a.createdAt));
    const list = drawer.querySelector(".learning-note-list");
    list.replaceChildren();
    if (!notes.length) {
      const empty = document.createElement("p");
      empty.className = "learning-empty";
      empty.textContent = onlyCurrent ? "当前页面还没有笔记。选中正文即可添加。" : "还没有笔记。阅读时选中一段文字开始记录。";
      list.append(empty);
      return;
    }
    notes.forEach((note) => {
      const card = document.createElement("article");
      card.className = "learning-note-card";
      const pageLink = document.createElement("a");
      pageLink.href = `${safePath(note.path)}${note.anchor ? `#${encodeURIComponent(note.anchor)}` : ""}`;
      pageLink.textContent = note.pageTitle;
      const quote = document.createElement("blockquote");
      quote.textContent = note.quote;
      const noteText = document.createElement("p");
      noteText.textContent = note.text || "仅保存了选中文字";
      const footer = document.createElement("div");
      const time = document.createElement("time");
      time.dateTime = note.createdAt;
      time.textContent = formatDate(note.createdAt);
      const remove = document.createElement("button");
      remove.type = "button";
      remove.textContent = "删除";
      remove.addEventListener("click", () => {
        if (!confirm("删除这条笔记？")) return;
        state.notes = state.notes.filter((item) => item.id !== note.id);
        save();
        renderAll();
        markAnnotatedBlocks();
      });
      footer.append(time, remove);
      card.append(pageLink, quote, noteText, footer);
      list.append(card);
    });
  };

  const renderProgress = () => {
    const list = drawer.querySelector(".learning-progress-list");
    list.replaceChildren();
    const entries = Object.values(state.completed).sort((a, b) => b.completedAt.localeCompare(a.completedAt));
    if (!entries.length) {
      const empty = document.createElement("p");
      empty.className = "learning-empty";
      empty.textContent = "还没有完成记录。进入课程页面后可标记为已完成。";
      list.append(empty);
      return;
    }
    entries.forEach((entry) => {
      const row = document.createElement("div");
      row.className = "learning-progress-row";
      const link = document.createElement("a");
      link.href = safePath(entry.path);
      link.textContent = entry.title;
      const meta = document.createElement("span");
      meta.textContent = formatDate(entry.completedAt);
      const remove = document.createElement("button");
      remove.type = "button";
      remove.textContent = "撤销";
      remove.addEventListener("click", () => {
        delete state.completed[entry.path];
        save();
        renderAll();
        renderPageProgress();
      });
      row.append(link, meta, remove);
      list.append(row);
    });
  };

  const renderAll = () => {
    updateBadge();
    renderSummary();
    renderNotes();
    renderProgress();
  };

  const openDrawer = () => {
    renderAll();
    backdrop.hidden = false;
    drawer.classList.add("open");
    drawer.setAttribute("aria-hidden", "false");
    drawer.querySelector("[data-learning-close]").focus();
  };
  const closeDrawer = () => {
    drawer.classList.remove("open");
    drawer.setAttribute("aria-hidden", "true");
    backdrop.hidden = true;
    openButton.focus();
  };

  const renderPageProgress = () => {
    if (!page.isCourse) return;
    let card = main.querySelector(".learning-progress-card");
    if (!card) {
      card = document.createElement("section");
      card.className = "learning-progress-card";
      main.insertBefore(card, main.firstChild);
    }
    const done = Boolean(state.completed[page.path]);
    card.innerHTML = `<div><span>本课学习状态</span><b>${done ? "已完成" : "学习中"}</b></div><button type="button" class="${done ? "is-complete" : ""}">${done ? "撤销完成" : "标记本课已完成"}</button>`;
    card.querySelector("button").addEventListener("click", () => {
      if (done) delete state.completed[page.path];
      else state.completed[page.path] = { path: page.path, title: page.title, source: page.source, completedAt: new Date().toISOString() };
      save();
      renderAll();
      renderPageProgress();
    });
  };

  const markAnnotatedBlocks = () => {
    const pageBlocks = blocks();
    pageBlocks.forEach((block) => {
      block.classList.remove("has-learning-note");
      block.querySelectorAll(":scope > .learning-note-marker").forEach((marker) => marker.remove());
    });
    const counts = new Map();
    state.notes.filter((note) => note.path === page.path && Number.isInteger(note.blockIndex)).forEach((note) => counts.set(note.blockIndex, (counts.get(note.blockIndex) || 0) + 1));
    counts.forEach((count, index) => {
      const block = pageBlocks[index];
      if (!block) return;
      block.classList.add("has-learning-note");
      const marker = document.createElement("button");
      marker.type = "button";
      marker.className = "learning-note-marker";
      marker.textContent = `${count} 条笔记`;
      marker.addEventListener("click", () => {
        drawer.querySelector("[data-current-page-only]").checked = true;
        openDrawer();
      });
      block.append(marker);
    });
  };

  const captureSelection = () => {
    const selection = getSelection();
    if (!selection || selection.isCollapsed || !selection.rangeCount) {
      selectionButton.hidden = true;
      return;
    }
    const range = selection.getRangeAt(0);
    const container = range.commonAncestorContainer.nodeType === Node.TEXT_NODE ? range.commonAncestorContainer.parentElement : range.commonAncestorContainer;
    if (!container || !main.contains(container) || container.closest("pre,code,.learning-progress-card,.learning-drawer")) {
      selectionButton.hidden = true;
      return;
    }
    const quote = selection.toString().replace(/\s+/g, " ").trim();
    if (quote.length < 2) {
      selectionButton.hidden = true;
      return;
    }
    const block = container.closest("p,li,h2,h3,blockquote");
    const pageBlocks = blocks();
    const rect = range.getBoundingClientRect();
    pendingSelection = { quote: quote.slice(0, 1200), blockIndex: block ? pageBlocks.indexOf(block) : -1, anchor: block?.id || "" };
    selectionButton.style.left = `${Math.max(12, Math.min(innerWidth - 120, rect.left + scrollX + rect.width / 2 - 48))}px`;
    selectionButton.style.top = `${Math.max(12, rect.bottom + scrollY + 8)}px`;
    selectionButton.hidden = false;
  };

  selectionButton.addEventListener("mousedown", (event) => event.preventDefault());
  selectionButton.addEventListener("click", () => {
    if (!pendingSelection) return;
    editor.querySelector("[data-learning-quote]").textContent = pendingSelection.quote;
    editor.querySelector("textarea").value = "";
    selectionButton.hidden = true;
    editor.showModal();
    editor.querySelector("textarea").focus();
  });
  editor.addEventListener("close", () => {
    if (editor.returnValue !== "save" || !pendingSelection) return;
    state.notes.push({
      id: id(),
      path: page.path,
      pageTitle: page.title,
      source: page.source,
      quote: pendingSelection.quote,
      text: editor.querySelector("textarea").value.trim(),
      blockIndex: pendingSelection.blockIndex,
      anchor: pendingSelection.anchor,
      createdAt: new Date().toISOString(),
    });
    pendingSelection = null;
    getSelection()?.removeAllRanges();
    save();
    renderAll();
    markAnnotatedBlocks();
    openDrawer();
  });

  drawer.querySelectorAll("[data-learning-tab]").forEach((tab) => tab.addEventListener("click", () => {
    drawer.querySelectorAll("[data-learning-tab]").forEach((item) => item.setAttribute("aria-selected", String(item === tab)));
    drawer.querySelectorAll("[data-learning-panel]").forEach((panel) => { panel.hidden = panel.dataset.learningPanel !== tab.dataset.learningTab; });
  }));
  drawer.querySelector("[data-current-page-only]").addEventListener("change", renderNotes);
  drawer.querySelector("[data-learning-export]").addEventListener("click", () => {
    const blob = new Blob([JSON.stringify(state, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `ai-beginners-learning-${new Date().toISOString().slice(0, 10)}.json`;
    link.click();
    URL.revokeObjectURL(url);
  });
  drawer.querySelector("[data-learning-import]").addEventListener("change", async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    try {
      const imported = JSON.parse(await file.text());
      if (imported.version !== 1 || !Array.isArray(imported.notes) || !imported.completed || Array.isArray(imported.completed)) throw new Error("invalid backup");
      if (!confirm("导入将覆盖当前浏览器中的笔记与进度，继续吗？")) return;
      const notes = imported.notes.filter((note) => note && typeof note.quote === "string" && typeof note.createdAt === "string").map((note) => ({
        id: typeof note.id === "string" ? note.id : id(),
        path: safePath(note.path),
        pageTitle: typeof note.pageTitle === "string" ? note.pageTitle.slice(0, 300) : "课程页面",
        source: typeof note.source === "string" ? note.source.slice(0, 1000) : "",
        quote: note.quote.slice(0, 1200),
        text: typeof note.text === "string" ? note.text.slice(0, 4000) : "",
        blockIndex: Number.isInteger(note.blockIndex) ? note.blockIndex : -1,
        anchor: typeof note.anchor === "string" ? note.anchor.slice(0, 300) : "",
        createdAt: note.createdAt,
      }));
      const completed = {};
      Object.values(imported.completed).forEach((entry) => {
        if (!entry || typeof entry.completedAt !== "string") return;
        const path = safePath(entry.path);
        completed[path] = { path, title: typeof entry.title === "string" ? entry.title.slice(0, 300) : "课程页面", source: typeof entry.source === "string" ? entry.source.slice(0, 1000) : "", completedAt: entry.completedAt };
      });
      state = { version: 1, notes, completed };
      save();
      renderAll();
      renderPageProgress();
      markAnnotatedBlocks();
    } catch (_) {
      alert("无法导入：请选择本站导出的 JSON 备份文件。");
    } finally {
      event.target.value = "";
    }
  });

  openButton.addEventListener("click", openDrawer);
  drawer.querySelector("[data-learning-close]").addEventListener("click", closeDrawer);
  backdrop.addEventListener("click", closeDrawer);
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && drawer.classList.contains("open")) closeDrawer();
  });
  document.addEventListener("mouseup", () => setTimeout(captureSelection));
  document.addEventListener("keyup", (event) => {
    if (event.key === "Shift" || event.key.startsWith("Arrow")) setTimeout(captureSelection);
  });
  document.addEventListener("scroll", () => { selectionButton.hidden = true; }, { passive: true });

  updateBadge();
  renderPageProgress();
  markAnnotatedBlocks();
})();

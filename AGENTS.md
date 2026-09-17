# Repository working agreement

This repository is the source of the Chinese learning Site, not a style-preserving mirror of the Microsoft upstream project.

## Product priorities

1. Keep the published Chinese Site navigable and honest about execution support.
2. Keep notebooks runnable in their declared environment.
3. Preserve upstream attribution and licensing.
4. Prefer explicit compatibility fixes over cosmetic parity with upstream.

## Source of truth

- `translations/zh-CN/`, `lessons/`, and `examples/` contain learning content.
- `website/build.py` produces the static site in `site-dist/`.
- `website/prepare_lite.py` is the allowlist for browser-runnable notebooks.
- `website/notebook-status.json` records browser, short-training, and blocked-resource status.
- `website/validation-status.json` records full-audit evidence and code hashes.
- `site/RUNNING.zh-CN.md` and `site/VALIDATION.zh-CN.md` explain those states to learners.

Do not edit generated `site-dist/` output as source. Do not label a notebook “verified” without a successful run that covers the stated scope. Full-pass evidence is valid only while its recorded code hash matches the notebook.

## Execution labels

- Browser runnable: included in `prepare_lite.py` and verified in a real browser.
- Fully verified: every code cell passed at the recorded code hash and original declared scope.
- Short-training verified: real code/data path passed with documented reductions.
- Revalidating: compatibility changed or the long run timed out.
- Credentials/data required: execution depends on a secret, restricted dataset, or external service.

Never collapse these labels into “all notebooks pass.” Exercise scaffolding passing does not mean the learner solution is complete.

## Required checks

For documentation or status changes:

```bash
python tools/check_repository_contract.py
python website/build.py
```

For browser notebook changes, also run `tools/test_browser_notebooks.py` or the Browser notebook execution workflow. For TensorFlow/PyTorch notebook changes, use the narrowest matching smoke workflow first, then the long compatibility or full audit workflow when appropriate.

Any `website/`, `site/`, lesson, example, or Chinese translation change must leave the Build Chinese learning site workflow green. Security workflow failures are not ignored merely because they are unrelated to rendering.

## Data and secrets

Never commit API keys, tokens, downloaded restricted datasets, model caches, or executed notebooks containing sensitive output. PH2 is user-supplied through `PH2_DATA_DIR`. Microsoft Concept Graph uses `NEWSAPI_KEY` or a local `NEWS_TITLES_JSON` file and still requires network access for concept lookup.

## Upstream sync

Treat `microsoft/AI-For-Beginners` as a content source. Review and merge upstream changes selectively. Preserve this repository's Chinese-first README, runtime, status metadata, compatibility fixes, and Site build system unless a replacement is deliberately implemented and tested.

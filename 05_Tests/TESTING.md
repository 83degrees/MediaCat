# Source-baseline verification

The regression suite verifies the source-controlled MediaCat implementation,
including schema-v2 model compatibility, the active schema-v3 catalogue, and
the post-retirement single-domain `mediacat` registration and Media Source
behaviour. It also asserts that active legacy `curated_media` component and
catalogue paths are absent while logical `catalogue_id: curated_media` remains.
It does not connect to or change a live Home Assistant system and is not evidence of
production deployment, runtime activation, production Home Assistant version
compatibility, or snapshot freshness.

The recorded ASTV-71 verification environment is:

- Python 3.12.13
- Home Assistant 2024.12.5 (test-only)
- pytest 9.1.1
- Windows 11

Home Assistant 2024.12.5 is deliberately a pinned test dependency compatible
with the available Python 3.12 runtime. The production Home Assistant version
is unknown, so passing results establish source-baseline behaviour only.

Pytest discovers the suite from `05_Tests/` and imports the maintained
implementation from `04_Source/` using the repository's `pyproject.toml`
configuration.

From the MediaCat repository root, create an isolated environment and run:

```powershell
& 'C:\Users\Graham\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m venv .venv
& '.\.venv\Scripts\python.exe' -m pip install -r requirements-test.txt
& '.\.venv\Scripts\python.exe' -m pytest
```


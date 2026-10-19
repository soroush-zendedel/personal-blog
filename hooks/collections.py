"""Generate collection landing pages from collection metadata and post files."""

from __future__ import annotations

import os
import json

import yaml
from mkdocs.plugins import event_priority
from mkdocs.structure.files import File


def _metadata(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as source:
            value = yaml.safe_load(source) or {}
        return value if isinstance(value, dict) else {}
    except (OSError, yaml.YAMLError):
        return {}


@event_priority(100)
def on_config(config):
    """Read each .collection.yml and expose the same collection map to templates."""
    docs_dir = config["docs_dir"]
    collections = []
    for root, dirs, files in os.walk(docs_dir):
        dirs[:] = [name for name in dirs if not name.startswith(".")]
        if ".collection.yml" not in files:
            continue
        metadata = _metadata(os.path.join(root, ".collection.yml"))
        if not metadata.get("title"):
            continue
        path = os.path.relpath(root, docs_dir).replace(os.sep, "/")
        collections.append({
            "path": path,
            "title": str(metadata["title"]),
            "description": str(metadata.get("description", "")),
            "english": bool(metadata.get("english", False)),
        })
    collections.sort(key=lambda item: item["path"])
    config.extra["collections"] = collections
    return config


def on_files(files, *, config):
    """Add virtual index pages so every collection gets a canonical MkDocs page."""
    for collection in config.extra.get("collections", []):
        source = f"{collection['path']}/index.md"
        if files.get_file_from_path(source):
            raise ValueError(
                f"{source} is maintained manually; remove it so the collection page can be generated."
            )
        content = "---\n"
        content += "title: " + json.dumps(collection["title"], ensure_ascii=False) + "\n"
        if collection["description"]:
            content += "description: " + json.dumps(collection["description"], ensure_ascii=False) + "\n"
        if collection["english"]:
            content += "english: true\n"
        content += "---\n\n"
        if collection["description"]:
            content += collection["description"] + "\n\n"
        content += f"{{{{ collection_posts('{collection['path']}') }}}}\n"
        files.append(File.generated(config, source, content=content))
    return files


def on_post_page(output, *, page, config):
    """Keep generated English collection indexes aligned with their content language."""
    if page.meta.get("english"):
        return output.replace('<html lang="fa"', '<html lang="en"', 1)
    return output

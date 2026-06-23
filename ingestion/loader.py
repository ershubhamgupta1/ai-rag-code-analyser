from pathlib import Path
from typing import List, Dict


SUPPORTED_EXTENSIONS = {
    ".js",
    ".jsx",
    ".ts",
    ".tsx"
}

IGNORE_DIRS = {
    "node_modules",
    ".git",
    ".next",
    "dist",
    "build",
    "coverage",
    ".turbo"
}


class ProjectLoader:

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)

    def load_project(self) -> List[Dict]:

        files = []

        project_tree = self.build_project_tree()

        for file_path in self.project_root.rglob("*"):

            if self._should_ignore(file_path):
                continue

            if file_path.suffix not in SUPPORTED_EXTENSIONS:
                continue

            try:

                content = file_path.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                files.append({
                    "file_name": file_path.name,
                    "path": str(
                        file_path.relative_to(
                            self.project_root
                        )
                    ),
                    "folder": str(
                        file_path.parent.relative_to(
                            self.project_root
                        )
                    ),
                    "extension": file_path.suffix,
                    "size": len(content),
                    "content": content,
                    "project_tree": project_tree
                })

            except Exception as ex:

                print(
                    f"Failed reading {file_path}: {ex}"
                )

        return files

    def build_project_tree(self) -> str:

        tree = []

        for item in sorted(
            self.project_root.rglob("*")
        ):

            if self._should_ignore(item):
                continue

            tree.append(
                str(
                    item.relative_to(
                        self.project_root
                    )
                )
            )

        return "\n".join(tree)

    def _should_ignore(self, path: Path) -> bool:

        return any(
            part in IGNORE_DIRS
            for part in path.parts
        )
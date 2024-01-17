from typing import List, Optional
import json
import os
import ast

from .docstring_extractor import Visitor


class Builder:
    """This class builds the json file which contains
    all the docstring extracted from the package selected."""

    def __init__(
        self,
        name: str,
        path: str,
        exclude_directories: Optional[List[str]] = None,
        recursive_search: bool = True,
    ):
        self.name = name
        self.path: str = path
        self.exclude_directories = None
        if exclude_directories is not None:
            self.exclude_directories: Optional[List[str]] = exclude_directories
        self.recursive_search: bool = recursive_search

        self.included_packages = []
        self.included_directories = []

        self.files: List[dict] = []

        self.final_build = {}

    def find_directories(self, path: str):
        list_of_directories = [d for d in os.listdir(path)]

        is_this_a_package = False
        if "__init__.py" in list_of_directories and os.path.isfile(
            os.path.join(path, "__init__.py")
        ):
            is_this_a_package = True
            self.included_packages.append(path)
        else:
            self.included_directories.append(path)

        for i in list_of_directories:
            if i.endswith(".py"):
                self.files.append(
                    {
                        "name": i,
                        "is_in_package": is_this_a_package,
                        "path": os.path.join(path, i),
                    }
                )
            elif os.path.isdir(os.path.join(path, i)):
                if not i.startswith("."):
                    if i not in self.exclude_directories:
                        self.find_directories(os.path.join(path, i))

    def compile_docs(self):
        self.final_build["name"] = self.name

        self.final_build["packages"] = self.included_packages
        self.final_build["directories"] = self.included_directories

        self.final_build["content"] = {}

        for i in self.files:
            visitor = Visitor()
            with open(i["path"], encoding="utf8") as file:
                print(i["path"])
                tree = ast.parse(file.read())
                visitor.call_visit(tree)

            self.final_build["content"][i["name"]] = {
                "name": i["name"],
                "is_in_package": i["is_in_package"],
                "path": i["path"],
                "docs": visitor.out(),
            }

    def build(self) -> str:
        self.find_directories(self.path)
        self.compile_docs()
        return json.dumps(self.final_build, indent=10)

import importlib

from pyharbor_shared_library.Disk import Disk


if __name__ == "__main__":
    d = "/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/tests/recruits"
    files = [x for x in Disk.Sync.rglob(directory=d) if x.is_file() and x.name != ".DS_Store" and x.name != "__init__.py"]
    py_files = [x for x in files if x.name.endswith(".py")]
    modules = []
    for x in py_files:
        z = str(x).split("/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/")[-1]
        modules.append((z.replace("/", ".").replace(".py", ""), x))
    for x, path in modules:
        try:
            module = importlib.import_module(x)
            module.asdf()
        except Exception as e:
            raise Exception(f'''{e}\nFailed to run module: \n\tTraceback (most recent call last):
  File "{path}", line 19, in <module>''')

    print("All modules ran successfully.")
    for x in modules:
        print(x[0])

from PIL import Image
from pyharbor_shared_library.Disk import Disk

if __name__ == "__main__":
    for x in [x for x in Disk.Sync.rglob(directory="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/assets/backgrounds/resize") if x.is_file() and x.name != ".DS_Store" and x.suffix == ".png" and ".image" not in str(x)]:
        print(str(x))
        filename = x.name
        try:
            with Image.open(str(x)) as im:
                if im.size != (1920, 1080):
                    print(f"Resizing {str(x)}")
                    x1 = im.resize(size=(1920, 1080))
                    x1.save(fp=x)
        except Exception as e:
            print(e)
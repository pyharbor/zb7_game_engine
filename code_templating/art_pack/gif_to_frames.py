from PIL import Image

num_key_frames = 8

with Image.open('/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/code_templating/art_pack/Pixaloop_28_06_2023_14_08_08_5390000.gif') as im:
    for i in range(num_key_frames):
        im.seek(im.n_frames // num_key_frames * i)
        im.save('{}.png'.format(i))
from pyharbor_shared_library.Disk import Disk

from zb7_game_engine.code_templating.tests.RecruitTestTemplate import RecruitTestTemplate
from zb7_game_engine.code_templating.tests.RelicTestTemplate import RelicTestTemplate
from zb7_game_engine.runtime.misc.debugging.Debug import Debug
from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
from zb7_game_engine.serialization.RelicSerializer import RelicSerializer


class TestGenerator:
    @staticmethod
    def run():
        sub_types = Disk.Sync.load_file_json(
            filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/sub_types.json")
        objects = []
        relics = []
        for i, x in enumerate(sub_types):
            if x["type"] == "Recruit":
                objects.append(RecruitSerializer.from_config_json(x))
            elif x["type"] == "Relic":
                relics.append(RelicSerializer.from_config_json(x))
        objects.extend(relics)
        for i, x in enumerate(objects):
            if x.type == "Recruit":
                recruit_path = f"/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/" \
                               f"git/projects/games/zb7_game_engine/zb7_game_engine/tests/" \
                               f"recruits/{x.main_species}/t_{x.sub_type_as_text}.py"
                if not Disk.Sync.check_path_exists(filename=recruit_path):
                    print(i, Debug.RecruitSerializer.study_info(x))
                    recruit_text = RecruitTestTemplate(recruit=x)
                    Disk.Sync.write_file_text(data=recruit_text,
                                              filename=f"/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/" \
                                                       f"git/projects/games/zb7_game_engine/zb7_game_engine/tests/" \
                                                       f"recruits/{x.main_species}/gt_{x.sub_type_as_text}.py")
            elif x.type == "Relic":
                relic_path = f"/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/" \
                             f"git/projects/games/zb7_game_engine/zb7_game_engine/tests/" \
                             f"relics/t_{x.sub_type_as_text}.py"
                if not Disk.Sync.check_path_exists(filename=relic_path):
                    relic_text = RelicTestTemplate(relic=x)
                    Disk.Sync.write_file_text(data=relic_text,
                                              filename=f"/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/" \
                                                   f"git/projects/games/zb7_game_engine/zb7_game_engine/tests/" \
                                                   f"relics/gt_{x.sub_type_as_text}.py")


if __name__ == "__main__":
    TestGenerator.run()

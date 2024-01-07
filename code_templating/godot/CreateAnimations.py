from collections import defaultdict

from pyharbor_shared_library.Disk import Disk

from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.serialization.animation_events.Animations import Animations


class CreateAnimations:
    @staticmethod
    def create():
        animations = []
        for i, (k, v) in enumerate(Animations.__dict__.items()):
            if k.startswith("__"):
                continue
            animations.append(k)
        animations.sort()
        # for i, animation in enumerate(animations):
        #     print(f"{str(i).ljust(3)} {animation.ljust(30)}")

        parent = "/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb6/scenes/shared/add_ons"
        for i, animation in enumerate(animations):
            if Disk.Sync.check_path_exists(filename=f"{parent}/Animations/{animation}/{animation}.tscn") or \
                    Disk.Sync.check_path_exists(filename=f"{parent}/Animations/{animation}/{animation}.gd"):
                continue
            else:
                # print(f"{str(i).ljust(3)} {animation.ljust(30)}")
                # Disk.Sync.create_directories(filename=f"{parent}/Animations/{animation}/{animation}.gd")
                pass

        files = [x for x in Disk.Sync.rglob(
            directory="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb6/scenes/shared/add_ons/Animations")
                 if x.is_dir()]

        bad_directories = []
        for x in files:
            if x.stem not in Animations.__dict__:
                bad_directories.append(x)

        bad_directories.sort()
        for i, x in enumerate(bad_directories):
            print(f"{str(i).ljust(3)} {str(x.name)}")

        print()
        animations = Disk.Sync.load_file_json(
            filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/animation_events.json")
        unique_custom_data = set()
        animation_event_by_custom_data = defaultdict(list)
        for i, x in enumerate(animations.values()):
            print(f"{str(i).ljust(3)} {str(x['custom_data'])}")
            unique_custom_data.add(x["custom_data"])
            animation_event_by_custom_data[x["custom_data"]].append(x['animation_type_as_text'])

        unique_custom_data = list(unique_custom_data)
        unique_custom_data.sort()
        for i, x in enumerate(unique_custom_data):
            print(f"{str(i).ljust(3)} {str(x).ljust(30)} {str(animation_event_by_custom_data[x][:2])}")

        g = Animations.Group()
        for i in range(3):
            g.add_animation_event(Animations.LightningDamage(state_id=2, shop_id=3, battle_id=4, amount=16))
        g.set_state_id(state_id=5)

        animation_events = [
            Animations.AdaptToNewSpecies(state_id=2, shop_id=3, battle_id=4, type_as_int=21),
            Animations.AddHabitat(state_id=2, shop_id=3, battle_id=4, habitat_as_int=21),
            Animations.AddSpecies(state_id=2, shop_id=3, battle_id=4, species_as_int=21),
            Animations.AddStatus(state_id=2, shop_id=3, battle_id=4, status_sub_type_as_int=21,
                                 amount=19),
            Animations.Taunt(state_id=2, shop_id=3, battle_id=4),
            Animations.LightningDamage(state_id=2, shop_id=3, battle_id=4, amount=16),
            Animations.ChlorotoxinEffect(battle_id=5, state_id=2),
            Animations.ReceiveDamage(state_id=2, shop_id=3, battle_id=4, damage_reduction_stack=[
                dict(amount=15, sub_type_as_int=GameConstants.DamageReductionStack.UnModifiedDamage),
                dict(amount=10, sub_type_as_int=GameConstants.DamageReductionStack.BasicArmor)
            ], damage_after_modifications=5, damage_before_modifications=15),
            Animations.GenericAbilityNotification(state_id=2, shop_id=3, battle_id=4, description="This is a test description"),
            g,
            Animations.ReceiveStatusDamage(state_id=2, shop_id=3, battle_id=4, amount=16, status_sub_type_as_int=21),
            Animations.SeaOtter(state_id=2, shop_id=3, battle_id=4, result_as_int=3),
            Animations.TreasureChest(state_id=3),
            Animations.BuffStats(state_id=2, shop_id=3, battle_id=4, health=5, melee=257, ranged=3, armor=4, initiative=1,
                                 max_health=5),
            Animations.Consume(state_id=2, shop_id=3, battle_id=4, target_shop_id=7, target_battle_id=7),
            Animations.NarwhalTusk(state_id=2, shop_id=3, battle_id=4, target_shop_id=7, target_battle_id=7, amount=10)

        ]
        text = []
        for i,x in enumerate(animation_events):
            print(i, x.to_base64())
            text.append(f'"{x.to_base64()}",')
        print("\n".join(text))



if __name__ == "__main__":
    CreateAnimations.create()

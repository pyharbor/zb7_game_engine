import importlib
import os
import random
import sys

from pyharbor_shared_library.Disk import Disk

from zb7_game_engine.runtime.misc.BinomialNomenclature import BinomialNomenclature


class ImmutableData:

    __possible_parent_paths = [
        "configs",
        "../configs",
        "immutable_data/configs",
        "../immutable_data/configs",
        "../../../immutable_data/configs",
        "/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/"
    ]
    __found = False
    # get the initiative immutable data
    for _path in __possible_parent_paths:
        try:
            _initiative_int_to_float = Disk.Sync.load_file_json(filename=f"{_path}/initiative_int_to_float_map.json")
            _initiative_float_to_int = Disk.Sync.load_file_json(filename=f"{_path}/initiative_float_to_int_map.json")
            __found = True
            break
        except FileNotFoundError:
            pass
    if not __found:
        raise FileNotFoundError("File not found in any of the possible paths: {path}/initiative_int_to_float_map.json")
    __found = False
    __start = 0.0
    _initiative_resolution = []
    for _x in range(100):
        _initiative_resolution.append(round(__start, 3))
        __start += 0.01

    # get the scientific nomenclature immutable data
    for _path in __possible_parent_paths:
        try:
            _scientific_name_to_int = Disk.Sync.load_file_json(filename=f"{_path}/scientific_nomenclature_as_int.json")
            _int_to_scientific_name = {_v: _k for _k, _v in _scientific_name_to_int.items()}
            __found = True
            break
        except FileNotFoundError:
            pass

    if not __found:
        raise FileNotFoundError("File not found in any of the possible paths: {path}/initiative_int_to_float_map.json")
    __found = False

    # get the sub_type immutable data
    for _path in __possible_parent_paths:
        try:
            _json = Disk.Sync.load_file_json(filename=f"{_path}/sub_types.json")
            _int_to_subtype = {
                _x["sub_type_as_int"]: _x for _x in _json
            }
            _subtype_text_to_int = {
                _x["sub_type_as_text"]: _x for _x in _json
            }

            __found = True
            break
        except FileNotFoundError:
            pass

    if not __found:
        raise FileNotFoundError("File not found in any of the possible paths: {path}/initiative_int_to_float_map.json")

    for _path in __possible_parent_paths:
        try:
            _animation_events = Disk.Sync.load_file_json(filename=f"{_path}/animation_events.json")
            _int_to_animation_events = {_v['animation_type_as_int']: _k for _k, _v in _animation_events.items()}
            _animation_events = {k: v['animation_type_as_int'] for k, v in _animation_events.items()}
            __found = True
            break
        except FileNotFoundError:
            pass

    if not __found:
        raise FileNotFoundError("File not found in any of the possible paths: {path}/animation_events_as_int.json")

    for _path in __possible_parent_paths:
        try:
            _custom_data_as_int = Disk.Sync.load_file_json(filename=f"{_path}/custom_data_as_int.json")
            _int_to_custom_data = {_v: _k for _k, _v in _custom_data_as_int.items()}
            __found = True
            break
        except FileNotFoundError:
            pass

    if not __found:
        raise FileNotFoundError("File not found in any of the possible paths: {path}/custom_data_as_int.json")

    __found = False
    for _path in __possible_parent_paths:
        try:
            _int_to_misc_types = Disk.Sync.load_file_json(filename=f"{_path}/misc_types_to_int.json")
            _misc_types_as_int = {_v: _k for _k, _v in _int_to_misc_types.items()}
            __found = True
            break
        except FileNotFoundError:
            pass

    if not __found:
        raise FileNotFoundError("File not found in any of the possible paths: {path}/misc_types_as_int.json")

    __found = False
    for _path in __possible_parent_paths:
        try:
            _int_to_habitat_types = Disk.Sync.load_file_json(filename=f"{_path}/habitats_as_int.json")
            _habitats_as_int = {_v: _k for _k, _v in _int_to_habitat_types.items()}
            __found = True
            break
        except FileNotFoundError:
            pass

    del __found
    del __possible_parent_paths

    class ScientificNomenclature:
        @staticmethod
        def from_int(name_as_int: int):
            return ImmutableData._int_to_scientific_name[name_as_int]

        @staticmethod
        def to_int(name_as_text: str):
            return ImmutableData._scientific_name_to_int[name_as_text]

    class Subtype:
        @staticmethod
        def from_int(subtype_as_int: int):
            return ImmutableData._int_to_subtype[subtype_as_int]

        @staticmethod
        def from_text(subtype_as_text: str):
            return ImmutableData._subtype_text_to_int[subtype_as_text]

    class Initiative:
        @staticmethod
        def from_int(initiative_as_int: int):
            return ImmutableData._initiative_int_to_float[str(initiative_as_int)]

        @staticmethod
        def to_int(initiative_as_float: float):
            return ImmutableData._initiative_float_to_int[str(float(initiative_as_float))]

        @staticmethod
        def get_random_intiative() -> float:
            new = random.choice(ImmutableData._initiative_resolution)
            return new

    class AnimationEvents:
        @staticmethod
        def from_int(subtype_as_int: int):
            return ImmutableData._int_to_animation_events[subtype_as_int]

        @staticmethod
        def from_text(subtype_as_text: str):
            return ImmutableData._animation_events[subtype_as_text]

    class CustomData:
        @staticmethod
        def from_int(subtype_as_int: int):
            return ImmutableData._int_to_custom_data[subtype_as_int]

        @staticmethod
        def from_text(subtype_as_text: str):
            return ImmutableData._custom_data_as_int[subtype_as_text]

    class Misc:
        @staticmethod
        def from_int(subtype_as_int: int):
            return ImmutableData._int_to_misc_types[str(subtype_as_int)]

        @staticmethod
        def from_text(subtype_as_text: str):
            return int(ImmutableData._misc_types_as_int[subtype_as_text])

    class Habitats:
        @staticmethod
        def from_int(name_as_int: int):
            return ImmutableData._int_to_habitat_types[str(name_as_int)]

        @staticmethod
        def from_text(name_as_text: str):
            return int(ImmutableData._habitats_as_int[name_as_text])


import json
from collections import defaultdict
from typing import Union, Dict, List

from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.runtime.objects.base.BaseRecruit import BaseRecruit
from zb7_game_engine.runtime.objects.base.BaseRelic import BaseRelic
from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
from zb7_game_engine.serialization.RelicSerializer import RelicSerializer


class Deck:

    def __init__(self, objects: list[Union[RelicSerializer, RecruitSerializer]], validate=False,
                 number_of_objects_per_deck: int = 26):
        self.objects: list[Union[RelicSerializer, RecruitSerializer]] = sorted(list(set(objects)), key=lambda x: x.sub_type_as_text)
        self.relics = [x for x in self.objects if isinstance(x, BaseRelic)]
        self.recruits = [x for x in self.objects if isinstance(x, BaseRecruit)]
        self.number_of_objects_per_deck = number_of_objects_per_deck
        if validate:
            self.validate_custom_deck()

    def validate_custom_deck(self):
        # there are 3/4/5 (12 relics)
        is_invalid = False
        errors = []
        common_relics = [x for x in self.relics if x.rarity == "Common"]
        if len(common_relics) < GameConstants.DeckConstraints.Relics.common_count:
            is_invalid = True
            errors.append(
                f"this deck is missing {GameConstants.DeckConstraints.Relics.common_count - len(common_relics)} common relics")
        if len(common_relics) > GameConstants.DeckConstraints.Relics.common_count:
            is_invalid = True
            errors.append(
                f"this deck has too many common relics, should have {GameConstants.DeckConstraints.Relics.common_count} but has {len(common_relics)}")
        uncommon_relics = [x for x in self.relics if x.rarity == "Uncommon"]
        if len(uncommon_relics) < GameConstants.DeckConstraints.Relics.uncommon_count:
            is_invalid = True
            errors.append(
                f"this deck is missing {GameConstants.DeckConstraints.Relics.uncommon_count - len(uncommon_relics)} uncommon relics")
        if len(uncommon_relics) > GameConstants.DeckConstraints.Relics.uncommon_count:
            is_invalid = True
            errors.append(
                f"this deck has too many uncommon relics, should have {GameConstants.DeckConstraints.Relics.uncommon_count} but has {len(uncommon_relics)}")
        rare_relics = [x for x in self.relics if x.rarity == "Rare"]
        if len(rare_relics) < GameConstants.DeckConstraints.Relics.rare_count:
            is_invalid = True
            errors.append(
                f"this deck is missing {GameConstants.DeckConstraints.Relics.rare_count - len(rare_relics)} rare relics")
        if len(rare_relics) > GameConstants.DeckConstraints.Relics.rare_count:
            is_invalid = True
            errors.append(
                f"this deck has too many rare relics, should have {GameConstants.DeckConstraints.Relics.rare_count} but has {len(rare_relics)}")

        common_recruits = [x for x in self.recruits if x.rarity == "Common"]
        if len(common_recruits) < GameConstants.DeckConstraints.Recruits.common_count:
            is_invalid = True
            errors.append(
                f"this deck is missing {GameConstants.DeckConstraints.Recruits.common_count - len(common_recruits)} common recruits")
        if len(common_recruits) > GameConstants.DeckConstraints.Recruits.common_count:
            is_invalid = True
            errors.append(
                f"this deck has too many common recruits, should have {GameConstants.DeckConstraints.Recruits.common_count} but has {len(common_recruits)}")

        uncommon_recruits = [x for x in self.recruits if x.rarity == "Uncommon"]
        if len(uncommon_recruits) < GameConstants.DeckConstraints.Recruits.uncommon_count:
            is_invalid = True
            errors.append(
                f"this deck is missing {GameConstants.DeckConstraints.Recruits.uncommon_count - len(uncommon_recruits)} uncommon recruits")
        if len(uncommon_recruits) > GameConstants.DeckConstraints.Recruits.uncommon_count:
            is_invalid = True
            errors.append(
                f"this deck has too many uncommon recruits, should have {GameConstants.DeckConstraints.Recruits.uncommon_count} but has {len(uncommon_recruits)}")
        rare_recruits = [x for x in self.recruits if x.rarity == "Rare"]
        if len(rare_recruits) < GameConstants.DeckConstraints.Recruits.rare_count:
            is_invalid = True
            errors.append(
                f"this deck is missing {GameConstants.DeckConstraints.Recruits.rare_count - len(rare_recruits)} rare recruits")
        if len(rare_recruits) > GameConstants.DeckConstraints.Recruits.rare_count:
            is_invalid = True
            errors.append(
                f"this deck has too many rare recruits, should have {GameConstants.DeckConstraints.Recruits.rare_count} but has {len(rare_recruits)}")

        if is_invalid:
            raise ValueError("\nInvalid deck: \n\t" + "\n\t".join(errors))

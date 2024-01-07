from typing import Type


class GameConstants:
    class Levels:
        all = [3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91, 105, 120, 136, 153, 171, 190, 210, 231, 253, 276, 300, 325,
               351, 378, 406, 435, 465, 496, 528, 561, 595, 630, 666, 703, 741, 780, 820, 861, 903, 946, 990, 1035]
        level_1 = 1
        level_2 = 3
        level_3 = 6
        level_4 = 10
        level_5 = 15
        level_6 = 21
        level_7 = 28
        level_8 = 36
        level_9 = 45
        level_10 = 55
        level_11 = 66
        level_12 = 78
        level_13 = 91
        level_14 = 105
        level_15 = 120
        level_16 = 136
        level_17 = 153
        level_18 = 171
        level_19 = 190
        level_20 = 210
        level_21 = 231
        level_22 = 253
        level_23 = 276
        level_24 = 300
        level_25 = 325
        level_26 = 351
        level_27 = 378
        level_28 = 406
        level_29 = 435
        level_30 = 465
        level_31 = 496
        level_32 = 528
        level_33 = 561
        level_34 = 595
        level_35 = 630
        level_36 = 666
        level_37 = 703
        level_38 = 741
        level_39 = 780
        level_40 = 820
        level_41 = 861
        level_42 = 903
        level_43 = 946
        level_44 = 990
        level_45 = 1035

    class Run:
        class Status:
            won = "won"
            draw = "draw"
            lost = "lost"
            pending = "pending"
            abandoned = "abandoned"

    class Battle:
        won = 1
        draw = 2
        lost = 3

    class Habitats:
        # Marine Ecosystems
        CoralReef = "CoralReef"
        Coastline = "Coastline"
        Mangrove = "Mangrove"
        OpenOcean = "OpenOcean"
        SeagrassMeadows = "SeagrassMeadows"
        Estuaries = "Estuaries"
        Lagoons = "Lagoons"
        SaltMarshes = "SaltMarshes"
        Beach = "Beach"
        DeepSea = "DeepSea"

        # Freshwater Ecosystems
        # Lentic
        Lakes = "Lakes"
        Ponds = "Ponds"
        Pools = "Pools"
        # Lotic
        Streams = "Streams"
        Rivers = "Rivers"

        Wetlands = "Wetlands"

        # Forest Ecosystems
        Alpine = "Alpine"
        BorealForest = "BorealForest"
        TemperateForest = "TemperateForest"
        TropicalRainForest = "TropicalRainForest"
        SubtropicalForest = "SubtropicalForest"
        TemperateDeciduousForest = "TemperateDeciduousForest"
        TemperateConiferousForest = "TemperateConiferousForest"
        Woodland = "Woodland"
        TemperateRainForest = "TemperateRainForest"

        # Arid Ecosystems
        Desert = "Desert"
        Steppe = "Steppe"

        # Wetland and riparian ecosystems
        Marsh = "Marsh"
        Swamp = "Swamp"

        # Field Ecosystems
        Field = "Field"
        Meadow = "Meadow"
        Prairie = "Prairie"
        Pasture = "Pasture"
        Grassland = "Grassland"
        Savanna = "Savanna"

        # Arctic Ecosystems
        Arctic = "Arctic"
        Tundra = "Tundra"
        Taiga = "Taiga"

        Arid = [Desert, Steppe]
        ArcticLike = [Arctic, Tundra, Taiga, Alpine]
        Oceanic = [CoralReef, Coastline, OpenOcean, DeepSea]
        Freshwater = [Lakes, Ponds, Pools, Streams, Rivers, Wetlands]
        Swampy = [Marsh, Swamp, Wetlands]
        Coastal = [Beach, Coastline, Mangrove]
        OpenWater = [OpenOcean, DeepSea]
        TemperateForests = [BorealForest, TemperateForest, TemperateDeciduousForest,
                            TemperateConiferousForest, Woodland]
        TropicalForests = [TropicalRainForest, SubtropicalForest]
        FieldMeadowLike = [Field, Meadow, Prairie, Pasture]
        GrasslandLike = [Grassland, Savanna]

    class ScientificNames:
        # for a special case
        EmptySlot = "EmptySlot"

        Amphibia = "Amphibia"

        # Koala
        Diprotodontia = "Diprotodontia"

        # Fish/Sharks
        Chondrichthyes = "Chondrichthyes"
        Actinopterygii = "Actinopterygii"

        # Birds/lizards/turtles/crocodiles
        Aves = "Aves"
        Reptilia = "Reptilia"
        Testudines = "Testudines"
        Squamata = "Squamata"
        Crocodilia = "Crocodilia"

        # Mammals
        Carnivora = "Carnivora"
        Primates = "Primates"
        Pinnipedia = "Pinnipedia"
        Ursidae = "Ursidae"
        Canidae = "Canidae"
        Carniformia = "Carniformia"
        Cetacea = "Cetacea"
        Hippopotamidae = "Hippopotamidae"
        Mephitidae = "Mephitidae"

        # Invertebrates
        # Mollusks/snails
        Cephalopoda = "Cephalopoda"
        Bivalvia = "Bivalvia"
        Gastropoda = "Gastropoda"
        Mollusca = "Mollusca"

        # Crabs
        Crustacea = "Crustacea"

        # spiders
        Arachnida = "Arachnida"

        # Insects
        Insecta = "Insecta"
        Hymenoptera = "Hymenoptera"

        # beetles
        Coleoptera = "Coleoptera"

        # crickets/mantids/
        Polyneoptera = "Polyneoptera"
        Orthoptera = "Orthoptera"
        Mantodea = "Mantodea"
        Phasmatodea = "Phasmatodea"
        Blattodea = "Blattodea"

    class Animations:
        Swallow = "Swallow"
        SandDamage = "SandDamage"
        ShopUpdatedRelic = "ShopUpdatedRelic"
        SandstormDamage = "SandstormDamage"
        Targeted = "Targeted"
        LightningDamage = "LightningDamage"
        FireDamage = "FireDamage"
        DebuffStats = "DebuffStats"
        NarwhalTusk = "NarwhalTusk"
        SharkBite = "SharkBite"
        ChlorotoxinEffect = "ChlorotoxinEffect"
        EntangledWebEffect = "EntangledWebEffect"
        AddSpecies = "AddSpecies"
        AddStatus = "AddStatus"
        ReceiveStatusDamage = "ReceiveStatusDamage"
        GenericAbilityNotification = "GenericAbilityNotification"
        FullBlock = "FullBlock"
        UpgradeRelic = "UpgradeRelic"
        TreasureChest = "TreasureChest"
        Taunt = "Taunt"
        Overkill = "Overkill"
        SetObjectData = "SetObjectData"
        ChumBucket = "ChumBucket"
        Dodge = "Dodge"
        Immune = "Immune"
        Faint = "Faint"
        ShopGainMoney = "ShopGainMoney"
        ReceiveDamage = "ReceiveDamage"
        ReceiveUnblockableDamage = "ReceiveUnblockableDamage"
        SuddenDeath = "SuddenDeath"
        ShoalDeath = "ShoalDeath"
        Revive = "Revive"
        Heal = "Heal"
        Meteor = "Meteor"
        MeleeAttack = "MeleeAttack"
        RangedAttack = "RangedAttack"
        BuffStats = "BuffStats"
        BattleGainExperience = "BattleGainExperience"
        BattleStart = "BattleStart"
        BattleLost = "BattleLost"
        BattleDraw = "BattleDraw"
        BattleWon = "BattleWon"
        ShopBuy = "ShopBuy"
        ShopSell = "ShopSell"
        ShopMove = "ShopMove"
        ShopRoll = "ShopRoll"
        ShopEndOfTurn = "ShopEndOfTurn"
        ShopStartOfTurn = "ShopStartOfTurn"
        ShopUpdatedRecruit = "ShopUpdatedRecruit"
        ShopLevelUp = "ShopLevelUp"
        ShopGainExperience = "ShopGainExperience"
        PerfectCopy = "PerfectCopy"
        HymenopteraReinforcements = "HymenopteraReinforcements"
        Group = "Group"
        BattleLevelUp = "BattleLevelUp"
        PufferfishAttack = "PufferfishAttack"
        Consume = "Consume"
        ScorpionSting = "ScorpionSting"
        AddHabitat = "AddHabitat"
        Vengeance = "Vengeance"
        AdaptToNewSpecies = "AdaptToNewSpecies"
        Construction = "Construction"
        SeaOtter = "SeaOtter"
        BacterialInfection = "BacterialInfection"
        SnappingTurtle = "SnappingTurtle"

    # class CustomDataTypes:
    #     int_to_func_map = {
    #         1: JsonCustomData,
    #         2: ShopIdCustomData,
    #         3: DebuffCustomData,
    #         4: StatusCustomData,
    #         5: AmountCustomData,
    #         6: BuffCustomData,
    #         7: GroupCustomData,
    #     }
    #
    #     @classmethod
    #     def get_handler(cls, custom_data: dict) -> Type[BaseCustomData]:
    #         custom_data_type_as_int = custom_data["type"]
    #         return cls.int_to_func_map[custom_data_type_as_int]

    class Rarity:
        Common = 12
        Uncommon = 10
        Rare = 6
        rarity_to_probability_map = {
            "Common": Common,
            "Uncommon": Uncommon,
            "Rare": Rare
        }

    class Opcodes:
        class Stack:
            battle_attack_with_melee = "battle_attack_with_melee"
            battle_attack_with_ranged = "battle_attack_with_ranged"
            passive_battle_ability = "passive_battle_ability"
            start_of_battle = "start_of_battle"
            battle_faint = "battle_faint"
            status_effect = "status_effect"
            battle_revive = "battle_revive"
            battle_friendly_recruit_faints = "battle_friendly_recruit_faints"
            battle_friendly_recruit_summoned = "battle_friendly_recruit_summoned"
            battle_level_up = "battle_level_up"
            battle_gain_experience = "battle_gain_experience"
            shop_buy = "shop_buy"
            shop_abandon = "shop_abandon"
            shop_sell = "shop_sell"
            shop_move = "shop_move"
            shop_roll = "shop_roll"
            shop_end_of_turn = "shop_end_of_turn"
            shop_start_of_turn = "shop_start_of_turn"
            shop_set_object_data = "shop_set_object_data"
            shop_level_up = "shop_level_up"
            shop_gain_experience = "shop_gain_experience"
            shop_bought = "shop_bought"
            shop_sold = "shop_sold"
            shop_friendly_recruit_summoned = "shop_friendly_recruit_summoned"
            shop_friendly_recruit_sold = "shop_friendly_recruit_sold"
            shop_player_decision = "shop_player_decision"
            shop_player_decision_made = "shop_player_decision_made"
            shop_set_name = "set_name"
            shop_set_custom = "set_custom"
            shop_set_aaid = "set_aaid"
            shop_faint = "shop_faint"
            shop_friendly_recruit_faints = "shop_friendly_recruit_faints"

        class Shop:
            shop_buy = "shop_buy"
            shop_abandon = "shop_abandon"
            shop_sell = "shop_sell"
            shop_move = "shop_move"
            shop_roll = "shop_roll"
            shop_end_of_turn = "shop_end_of_turn"
            shop_start_of_turn = "shop_start_of_turn"
            shop_set_object_data = "shop_set_object_data"
            shop_level_up = "shop_level_up"
            shop_gain_experience = "shop_gain_experience"
            shop_bought = "shop_bought"
            shop_sold = "shop_sold"
            shop_friendly_recruit_summoned = "shop_friendly_recruit_summoned"
            shop_player_decision = "shop_player_decision"
            shop_player_decision_made = "shop_player_decision_made"

        class ObjectData:
            shop_set_name = "set_name"
            shop_set_custom = "set_custom"
            shop_set_aaid = "set_aaid"
            shop_upgrade_object = "shop_upgrade_object"

    class DeckConstraints:
        class Relics:
            rare_count = 3
            uncommon_count = 4
            common_count = 3
            total_count = 10

        class Recruits:
            rare_count = 5
            uncommon_count = 6
            common_count = 5
            total_count = 16

    class Numbers:
        shop_object_count = 12
        shop_roll_cost = 5
        team_recruit_object_count = 7

    class SnapshotTypes:
        # regular shop states
        shop_default = "shop_default"
        shop_start_of_run = "shop_start_of_run"
        shop_buy = "shop_buy"
        shop_sell = "shop_sell"
        shop_end_of_turn = "shop_end_of_turn"
        shop_combine = "shop_combine"
        shop_move = "shop_move"
        shop_freeze = "shop_freeze"
        shop_roll = "shop_roll"
        shop_start_of_turn = "shop_start_of_turn"
        shop_set_object_data = "shop_set_object_data"

        # irregular states that require drastically different UI rendering
        battle = "battle"
        player_decision = "player_decision"
        run_end = "run_end"

    class DamageReductionStack:
        UnModifiedDamage = 1
        BasicArmor = 2
        Protected = 3
        ProtectiveCanopy = 4
        ThickBlubber = 5
        Burrowed = 6
        Evasion = 7
        AirborneDefense = 8
        CoralProtection = 9
        ShellArmor = 10
        ShedTail = 11
        DivingDefense = 12
        Vengeance = 13
        Adaptability = 14
        Carapace = 15
        EntrenchedDugout = 16
        FattyTissue = 17
        BearHide = 18
        WarningCall = 19
        ClamShell = 20
        HippoHide = 21

        @staticmethod
        def from_int(i: int) -> str:
            return {
                1: "UnModifiedDamage",
                2: "BasicArmor",
                3: "Protected",
                4: "ProtectiveCanopy",
                5: "ThickBlubber",
                6: "Burrowed",
                7: "AirborneEvasion",
                8: "AirborneDefense",
                9: "CoralProtection",
                10: "ShellArmor",
                11: "ShedTail",
                12: "DivingDefense",
                13: "Vengeance",
                14: "Adaptability",
                15: "Carapace",
                16: "EntrenchedDugout",
                17: "FattyTissue",
                18: "BearHide",
                19: "WarningCall",
                20: "ClamShell",
                21: "HippoHide"
            }[i]

    class PDInfoType:
        TreasureChest = "TreasureChest"

    class SnapshotSubTypes:
        class Int:
            start_of_run = 8
            start_of_turn = 9
            end_of_turn = 10
            end_of_run = 11
            buy = 12
            sell = 13
            move = 14
            roll = 15
            name = 16
            change_art = 17
            custom = 18
            reward = 19
            battle = 20

        class String:
            start_of_run = "start_of_run"
            start_of_battle = "start_of_battle"
            start_of_turn = "start_of_turn"
            end_of_turn = "end_of_turn"
            end_of_run = "end_of_run"
            buy = "buy"
            sell = "sell"
            move = "move"
            roll = "roll"
            name = "name"
            change_art = "change_art"
            custom = "custom"
            reward = "reward"
            battle = "battle"

    class Statuses:
        Negative = {
            "Bacteria",
            "Batrachotoxin",
            "Chlorotoxin",
            "CorrosiveSpitStatus",
            "Cytotoxin",
            "Dendrotoxin",
            "EntangledWeb",
            "IncendiaryMaterial",
            "InkSpray",
            "MildPoison",
            "NeuromuscularToxin",
            "NeurotoxicPeptides",
            "SkunkSpray",
            "Tetrodotoxin"
        }
        Positive = {
            "AcridSlimeSkin",
            "Adaptability",
            "Airborne",
            "AnemoneAttachment",
            "Burrowed",
            "Camouflage",
            "Carapace",
            "CoralProtection",
            "Diving",
            "EntrenchedDugout",
            "Flock",
            "HiveDurability",
            "MolluskMucus",
            "Protected",
            "ShellArmor",
            "Shoal",
            "Submerged",
            "ThickBlubber",
            "Vengeance"
        }

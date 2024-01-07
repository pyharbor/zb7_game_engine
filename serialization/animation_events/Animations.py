from zb7_game_engine.serialization.animation_events.S.SandstormDamage import SandstormDamage
from zb7_game_engine.serialization.animation_events.L.LightningDamage import LightningDamage
from zb7_game_engine.serialization.animation_events.F.FireDamage import FireDamage
from zb7_game_engine.serialization.animation_events.D.DebuffStats import DebuffStats
from zb7_game_engine.serialization.animation_events.N.NarwhalTusk import NarwhalTusk
from zb7_game_engine.serialization.animation_events.S.SharkBite import SharkBite
from zb7_game_engine.serialization.animation_events.C.ChlorotoxinEffect import ChlorotoxinEffect
from zb7_game_engine.serialization.animation_events.E.EntangledWebEffect import EntangledWebEffect
from zb7_game_engine.serialization.animation_events.A.AddSpecies import AddSpecies
from zb7_game_engine.serialization.animation_events.A.AddStatus import AddStatus
from zb7_game_engine.serialization.animation_events.R.ReceiveStatusDamage import ReceiveStatusDamage
from zb7_game_engine.serialization.animation_events.G.GenericAbilityNotification import GenericAbilityNotification
from zb7_game_engine.serialization.animation_events.F.FullBlock import FullBlock
from zb7_game_engine.serialization.animation_events.U.UpgradeRelic import UpgradeRelic
from zb7_game_engine.serialization.animation_events.T.TreasureChest import TreasureChest
from zb7_game_engine.serialization.animation_events.T.Taunt import Taunt
from zb7_game_engine.serialization.animation_events.O.Overkill import Overkill
from zb7_game_engine.serialization.animation_events.S.SetObjectData import SetObjectData
from zb7_game_engine.serialization.animation_events.C.ChumBucket import ChumBucket
from zb7_game_engine.serialization.animation_events.D.Dodge import Dodge
from zb7_game_engine.serialization.animation_events.I.Immune import Immune
from zb7_game_engine.serialization.animation_events.F.Faint import Faint
from zb7_game_engine.serialization.animation_events.S.ShopGainMoney import ShopGainMoney
from zb7_game_engine.serialization.animation_events.R.ReceiveDamage import ReceiveDamage
from zb7_game_engine.serialization.animation_events.R.ReceiveUnblockableDamage import ReceiveUnblockableDamage
from zb7_game_engine.serialization.animation_events.S.SuddenDeath import SuddenDeath
from zb7_game_engine.serialization.animation_events.S.ShoalDeath import ShoalDeath
from zb7_game_engine.serialization.animation_events.R.Revive import Revive
from zb7_game_engine.serialization.animation_events.H.Heal import Heal
from zb7_game_engine.serialization.animation_events.M.Meteor import Meteor
from zb7_game_engine.serialization.animation_events.M.MeleeAttack import MeleeAttack
from zb7_game_engine.serialization.animation_events.R.RangedAttack import RangedAttack
from zb7_game_engine.serialization.animation_events.B.BuffStats import BuffStats
from zb7_game_engine.serialization.animation_events.B.BattleGainExperience import BattleGainExperience
from zb7_game_engine.serialization.animation_events.B.BattleStart import BattleStart
from zb7_game_engine.serialization.animation_events.B.BattleLost import BattleLost
from zb7_game_engine.serialization.animation_events.B.BattleDraw import BattleDraw
from zb7_game_engine.serialization.animation_events.B.BattleWon import BattleWon
from zb7_game_engine.serialization.animation_events.S.ShopBuy import ShopBuy
from zb7_game_engine.serialization.animation_events.S.ShopSell import ShopSell
from zb7_game_engine.serialization.animation_events.S.ShopMove import ShopMove
from zb7_game_engine.serialization.animation_events.S.ShopRoll import ShopRoll
from zb7_game_engine.serialization.animation_events.S.ShopEndOfTurn import ShopEndOfTurn
from zb7_game_engine.serialization.animation_events.S.ShopStartOfTurn import ShopStartOfTurn
from zb7_game_engine.serialization.animation_events.S.ShopUpdatedRecruit import ShopUpdatedRecruit
from zb7_game_engine.serialization.animation_events.S.ShopLevelUp import ShopLevelUp
from zb7_game_engine.serialization.animation_events.S.ShopGainExperience import ShopGainExperience
from zb7_game_engine.serialization.animation_events.P.PerfectCopy import PerfectCopy
from zb7_game_engine.serialization.animation_events.H.HymenopteraReinforcements import HymenopteraReinforcements
from zb7_game_engine.serialization.animation_events.G.Group import Group
from zb7_game_engine.serialization.animation_events.B.BattleLevelUp import BattleLevelUp
from zb7_game_engine.serialization.animation_events.P.PufferfishAttack import PufferfishAttack
from zb7_game_engine.serialization.animation_events.C.Consume import Consume
from zb7_game_engine.serialization.animation_events.S.ScorpionSting import ScorpionSting
from zb7_game_engine.serialization.animation_events.A.AddHabitat import AddHabitat
from zb7_game_engine.serialization.animation_events.V.Vengeance import Vengeance
from zb7_game_engine.serialization.animation_events.A.AdaptToNewSpecies import AdaptToNewSpecies
from zb7_game_engine.serialization.animation_events.C.Construction import Construction
from zb7_game_engine.serialization.animation_events.S.SeaOtter import SeaOtter
from zb7_game_engine.serialization.animation_events.B.BacterialInfection import BacterialInfection
from zb7_game_engine.serialization.animation_events.S.SnappingTurtle import SnappingTurtle
from zb7_game_engine.serialization.animation_events.S.ShopUpdatedRelic import ShopUpdatedRelic
from zb7_game_engine.serialization.animation_events.S.SandDamage import SandDamage
from zb7_game_engine.serialization.animation_events.S.Swallow import Swallow


class Animations:

    SandstormDamage = SandstormDamage
    LightningDamage = LightningDamage
    FireDamage = FireDamage
    DebuffStats = DebuffStats
    NarwhalTusk = NarwhalTusk
    SharkBite = SharkBite
    ChlorotoxinEffect = ChlorotoxinEffect
    EntangledWebEffect = EntangledWebEffect
    AddSpecies = AddSpecies
    AddStatus = AddStatus
    ReceiveStatusDamage = ReceiveStatusDamage
    GenericAbilityNotification = GenericAbilityNotification
    FullBlock = FullBlock
    UpgradeRelic = UpgradeRelic
    TreasureChest = TreasureChest
    Taunt = Taunt
    Overkill = Overkill
    SetObjectData = SetObjectData
    ChumBucket = ChumBucket
    Dodge = Dodge
    Immune = Immune
    Faint = Faint
    ShopGainMoney = ShopGainMoney
    ReceiveDamage = ReceiveDamage
    ReceiveUnblockableDamage = ReceiveUnblockableDamage
    SuddenDeath = SuddenDeath
    ShoalDeath = ShoalDeath
    Revive = Revive
    Heal = Heal
    Meteor = Meteor
    MeleeAttack = MeleeAttack
    RangedAttack = RangedAttack
    BuffStats = BuffStats
    BattleGainExperience = BattleGainExperience
    BattleStart = BattleStart
    BattleLost = BattleLost
    BattleDraw = BattleDraw
    BattleWon = BattleWon
    ShopBuy = ShopBuy
    ShopSell = ShopSell
    ShopMove = ShopMove
    ShopRoll = ShopRoll
    ShopEndOfTurn = ShopEndOfTurn
    ShopStartOfTurn = ShopStartOfTurn
    ShopUpdatedRecruit = ShopUpdatedRecruit
    ShopLevelUp = ShopLevelUp
    ShopGainExperience = ShopGainExperience
    PerfectCopy = PerfectCopy
    HymenopteraReinforcements = HymenopteraReinforcements
    Group = Group
    BattleLevelUp = BattleLevelUp
    PufferfishAttack = PufferfishAttack
    Consume = Consume
    ScorpionSting = ScorpionSting
    AddHabitat = AddHabitat
    Vengeance = Vengeance
    AdaptToNewSpecies = AdaptToNewSpecies
    Construction = Construction
    SeaOtter = SeaOtter
    BacterialInfection = BacterialInfection
    SnappingTurtle = SnappingTurtle
    ShopUpdatedRelic = ShopUpdatedRelic
    SandDamage = SandDamage
    Swallow = Swallow

"""
1   SandstormDamage                state_id: int
2   LightningDamage                state_id: int, battle_id: int, shop_id: int, amount: int
3   FireDamage                     state_id: int, battle_id: int, shop_id: int, amount: int
4   DebuffStats                    state_id: int, shop_id: int, battle_id: int, health: int, melee: int, ranged: int, armor: int, initiative: int, max_health: int
5   NarwhalTusk                    state_id: int, shop_id: int, battle_id: int, amount: int
6   SharkBite                      state_id: int, battle_id: int, shop_id: int, target_battle_id: int, target_shop_id: int, amount: int
7   ChlorotoxinEffect              state_id: int, battle_id: int
8   EntangledWebEffect             state_id: int, battle_id: int
9   AddSpecies                     state_id: int, shop_id: int = None, battle_id: int = None, species_as_int: int = None
10  AddStatus                      state_id: int, battle_id: int, shop_id: int, status_sub_type_as_int: int, amount: int
11  ReceiveStatusDamage            state_id: int, battle_id: int, shop_id: int, status_sub_type_as_int: int, amount: int
12  GenericAbilityNotification     state_id: int, shop_id: int, battle_id: int, description: str
13  FullBlock                      state_id: int, battle_id: int, shop_id: int, damage_reduction_stack: list, damage_after_modifications: int, damage_before_modifications: int
14  UpgradeRelic                   state_id: int
15  TreasureChest                  state_id: int
16  Taunt                          state_id: int, shop_id: int, battle_id: int
17  Overkill                       state_id: int, shop_id: int, battle_id: int, target_battle_id: int, target_shop_id: int, amount: int
18  SetObjectData                  state_id: int
19  ChumBucket                     state_id: int
20  Dodge                          state_id: int, battle_id: int, shop_id: int, amount: int
21  Immune                         state_id: int, shop_id: int, battle_id: int
22  Faint                          state_id: int, battle_id: int, shop_id: int
23  ShopGainMoney                  state_id: int
24  ReceiveDamage                  state_id: int, damage_reduction_stack: list, damage_after_modifications: int, damage_before_modifications: int, battle_id: int, shop_id: int
25  ReceiveUnblockableDamage       state_id: int, battle_id: int, shop_id: int, amount: int
26  SuddenDeath                    state_id: int
27  ShoalDeath                     state_id: int, battle_id: int, shop_id: int
28  Revive                         state_id: int, shop_id: int, battle_id: int
29  Heal                           state_id: int, battle_id: int, shop_id: int, amount: int
30  Meteor                         state_id: int
31  MeleeAttack                    state_id: int, battle_id: int, shop_id: int, target_battle_id: int, target_shop_id: int, amount: int
32  RangedAttack                   state_id: int, shop_id: int, battle_id: int, target_battle_id: int, target_shop_id: int, amount: int
33  BuffStats                      state_id: int, shop_id: int, battle_id: int, health: int, melee: int, ranged: int, armor: int, initiative: int, max_health: int
34  BattleGainExperience           state_id: int, battle_id: int, shop_id: int, amount: int
35  BattleStart                    state_id: int
36  BattleLost                     state_id: int
37  BattleDraw                     state_id: int
38  BattleWon                      state_id: int
39  ShopBuy                        state_id: int
40  ShopSell                       state_id: int
41  ShopMove                       state_id: int
42  ShopRoll                       state_id: int
43  ShopEndOfTurn                  state_id: int
44  ShopStartOfTurn                state_id: int
45  ShopUpdatedRecruit             state_id: int, shop_id: int
46  ShopLevelUp                    state_id: int, amount: int, shop_id: int
47  ShopGainExperience             state_id: int, amount: int, shop_id: int
48  PerfectCopy                    state_id: int, shop_id: int, battle_id: int
49  HymenopteraReinforcements      state_id: int, battle_id: int, shop_id: int
50  Group                          state_id: int = None
51  BattleLevelUp                  state_id: int, battle_id: int, shop_id: int
52  PufferfishAttack               state_id: int, shop_id: int, battle_id: int, target_battle_id: int, target_shop_id: int, amount: int
53  Consume                        state_id: int, shop_id: int = None, battle_id: int = None, target_shop_id: int = None, target_battle_id: int = None
54  ScorpionSting                  state_id: int, shop_id: int, battle_id: int, target_battle_id: int, target_shop_id: int, amount: int
55  AddHabitat                     state_id: int, shop_id: int = None, battle_id: int = None, habitat_as_int: int = None
56  Vengeance                      state_id: int, battle_id: int, shop_id: int
57  AdaptToNewSpecies              state_id: int, shop_id: int, battle_id: int, type_as_int: int
58  Construction                   state_id: int, shop_id: int
59  SeaOtter                       state_id: int, shop_id: int, battle_id: int, result: int
60  BacterialInfection             state_id: int, shop_id: int, battle_id: int, amount: int






"""
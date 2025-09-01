"""
Embedded tweak definitions for bundled applications.
This module contains all tweak data as Python dictionaries to avoid
dependency on external JSON files at first launch.
"""

AC_ODYSSEY_TWEAKS = {
    "game_info": {
        "game_id": "ac_odyssey",
        "name": "Assassin's Creed Odyssey",
        "short_name": "AC Odyssey",
        "steam_app_id": "812140",
        "executable_name": "ACOdyssey.exe",
        "nexus_mods_url": "https://www.nexusmods.com/assassinscreedodyssey/mods/12",
        "main_title": "Vahndaar's AC Odyssey Tweak Pack",
        "tweak_pack_version": "V1.0.2.5",
        "subtitle": "Compatible with Assassin's Creed Odyssey {compatible_version}",
        "compatible_version": "V1.5.6",
        "default": True
    },
    "horse_mods": {
        "horse": {
            "name": "Disable Horse Speed Restriction",
            "type": "bool",
            "description": "This removes the forced horse speed cap when approaching towns and cities.",
            "originalByteArray": "0x7417F30F104C2440F30F104424300F2FC17606F30F114C2430498BCF",
            "modifiedByteArray": "0xEB17F30F104C2440F30F104424300F2FC17606F30F114C2430498BCF",
            "variableOffset": 0,
            "variableType": "bool",
            "group": "horse_speed",
            "visible": True,
            "section": "Horse Mods",
            "help": "This removes the forced horse speed cap when approaching towns and cities. This allows you to maintain full horse speed even when entering populated areas."
        }
    },
    "boat_mods": {
        "infiniteBoatRowStamina": {
            "name": "Infinite Boat Row Stamina",
            "type": "bool",
            "description": "Removes stamina consumption when rowing boats, allowing unlimited rowing.",
            "originalByteArray": "0x450F2EC8F3440F1143507407",
            "modifiedByteArray": "0x450F2EC8E959A8D1FD907407",
            "variableOffset": 0,
            "variableType": "bool",
            "group": "boat_stamina",
            "visible": True,
            "section": "Boat Mods",
            "help": "Removes stamina consumption when rowing boats, allowing unlimited rowing. This makes boat travel much more convenient and removes the need to wait for stamina to regenerate."
        },
        "infiniteBoatRowStamina2": {
            "name": "Infinite Boat Row Stamina Patch 2",
            "type": "bool",
            "description": "Secondary patch for infinite boat row stamina.",
            "originalByteArray": "0xCCCCE94B61680BCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
            "modifiedByteArray": "0xCCCCE94B61680BCCCC9C837B48040F85110000004157448B7B3C44897B5066450F6EC7415F9DF3440F114350E980572E02",
            "variableOffset": 0,
            "variableType": "bool",
            "group": "boat_stamina",
            "visible": False,
            "section": "Boat Mods"
        }
    },
    "player_mods": {
        "infiniteBreathUnderwater": {
            "name": "Infinite Breath Underwater",
            "type": "bool",
            "description": "Prevents the breath meter from depleting when swimming underwater, allowing unlimited underwater exploration.",
            "originalByteArray": "0xF30F1189F0050000488B4338488B100F2F82F0050000",
            "modifiedByteArray": "0xE9B8E2DBFC0F1F00488B4338488B100F2F82F0050000",
            "variableOffset": 0,
            "variableType": "bool",
            "group": "breath_underwater",
            "visible": True,
            "section": "Player Mods",
            "help": "Prevents the breath meter from depleting when swimming underwater, allowing unlimited underwater exploration. This makes underwater activities much more enjoyable and removes the need to surface for air."
        },
        "infiniteBreathUnderwater2": {
            "name": "Infinite Breath Underwater Patch 2",
            "type": "bool",
            "description": "Secondary patch for infinite breath underwater.",
            "originalByteArray": "0xCCCCE99B206207CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
            "modifiedByteArray": "0xCCCCE99B206207CCCCF30F1089EC050000F30F1189F0050000E9361D2403",
            "variableOffset": 0,
            "variableType": "bool",
            "group": "breath_underwater",
            "visible": False,
            "section": "Player Mods"
        },
        "customXPMultiplier": {
            "name": "Custom XP Multiplier",
            "type": "float",
            "description": "This sets the master XP multiplier. You can check this is active as there should be a little yellow circle next to the XP bar when in the menu in the game. This can be used to enable and disable the multiplier.",
            "originalByteArray": "0xC333C0C3CC488B81880000004885C0741280B8D1000000007409F30F1080E4000000C3F30F10057EF05F02C3CC",
            "modifiedByteArray": "0x9033C0C3CC488B81880000004885C0740980B8D1000000007400C780E40000000000C03FF30F1080E4000000C3",
            "variableOffset": 64,
            "variableType": "float",
            "group": "xp_multiplier",
            "visible": True,
            "section": "Player Mods",
            "help": "This sets the master XP multiplier. You can check this is active as there should be a little yellow circle next to the XP bar when in the menu in the game. This can be used to enable and disable the multiplier. Higher values will give you more XP per action, making leveling up faster."
        },
        "customXPMultiplierDisableLowerBound1": {
            "name": "Custom XP Multiplier - Disable Lower Bound 1",
            "type": "bool",
            "description": "Disable lower bound for XP multiplier.",
            "originalByteArray": "0x0F2F0D8DCA78017208F30F1189C0050000C3",
            "modifiedByteArray": "0x0F2F0D8DCA78017200F30F1189C0050000C3",
            "variableOffset": 0,
            "variableType": "bool",
            "group": "xp_multiplier",
            "bounds_logic": "disable_lower_bound",
            "visible": False,
            "section": "Player Mods",
            "help": "Disable lower bound for XP multiplier. This is automatically applied when the main XP multiplier tweak is enabled."
        },
        "customXPMultiplierDisableLowerBound2": {
            "name": "Custom XP Multiplier - Disable Lower Bound 2",
            "type": "bool",
            "description": "Disable lower bound for XP multiplier.",
            "originalByteArray": "0x0F2F0D5AC8750176300F57C0F3480F2AC5F30F59C1F3480F2CC00F57C08987B4",
            "modifiedByteArray": "0x0F2F0D5AC8750176000F57C0F3480F2AC5F30F59C1F3480F2CC00F57C08987B4",
            "variableOffset": 0,
            "variableType": "bool",
            "group": "xp_multiplier",
            "bounds_logic": "disable_lower_bound",
            "visible": False,
            "section": "Player Mods"
        },
        "customXPMultiplierDisableLowerBound3": {
            "name": "Custom XP Multiplier - Disable Lower Bound 3",
            "type": "bool",
            "description": "Disable lower bound for XP multiplier.",
            "originalByteArray": "0x0F2FB1C005000073740F28CEE8000FCAFF488B8F00020000",
            "modifiedByteArray": "0x0F2FB1C005000074740F28CEE8000FCAFF488B8F00020000",
            "variableOffset": 0,
            "variableType": "bool",
            "group": "xp_multiplier",
            "bounds_logic": "disable_lower_bound",
            "visible": False,
            "section": "Player Mods"
        },
        "customXPMultiplierDisableLowerBound4": {
            "name": "Custom XP Multiplier - Disable Lower Bound 4",
            "type": "bool",
            "description": "Disable lower bound for XP multiplier.",
            "originalByteArray": "0x0F86FF01000084C00F85F70100004038B70B0200000F844A01000048",
            "modifiedByteArray": "0x0F84FF01000084C00F85F70100004038B70B0200000F844A01000048",
            "variableOffset": 0,
            "variableType": "bool",
            "group": "xp_multiplier",
            "bounds_logic": "disable_lower_bound",
            "visible": False,
            "section": "Player Mods"
        },
        "customHealingReduction1": {
            "name": "Custom Healing Factor",
            "type": "int",
            "min": 1,
            "max": 15,
            "description": "Experimental tweak to out of combat healing. The purpose of this tweak is to increase challenge and reduce players' ability to simply run away and heal.",
            "originalByteArray": "0x488B4F18428D149D00000000F3440F2C040A440FAF453841F7E841B801000000C1FA058BC2C1E81F03D0440F45C2418BC8",
            "modifiedByteArray": "0x4C8B1DCE736903909090909090904831C9418B8BB00300004D31C0498BD1C1FA0A85C97605D1E283C201488BCA90909090",
            "variableOffset": 64,
            "variableType": "byte",
            "group": "healing_factor",
            "visible": True,
            "section": "Player Mods",
            "help": "Experimental tweak to out of combat healing. The purpose of this tweak is to increase challenge and reduce players' ability to simply run away and heal. Players can set a healing factor between 1 and 15. 1 means almost instant healing, 15 will effectively disable healing."
        },
        "customHealingReduction2": {
            "name": "Custom Health Boosts",
            "type": "int",
            "min": 1,
            "max": 5,
            "description": "This reduces the health awarded when using adrenaline based abilities as well as when using the second wind ability.",
            "originalByteArray": "0x8D1431488BCFE88A9D13003BF30F94C084C074304084ED752BE8E7DCAD00488BD84885C0741E488D4C2420E8350F95FE488D8B200600004533C0488D542420E8914860FF488B9C247002000033C0488B8C24300200004833CCE8E774BC014881C4400200005F5E5DC3CCCCCCCCCCCCCCCCCCCCCCCC",
            "modifiedByteArray": "0xEB6790488BCFE88A9D13003BF30F94C084C074304084ED752BE8E7DCAD00488BD84885C0741E488D4C2420E8350F95FE488D8B200600004533C0488D542420E8914860FF488B9C247002000033C0488B8C24300200004833CCE8E774BC014881C4400200005F5E5DC3C1FE018D1431EB92CCCCCCCC",
            "variableOffset": 214,
            "variableType": "byte",
            "group": "health_boosts",
            "visible": True,
            "section": "Player Mods",
            "help": "This reduces the health awarded when using adrenaline based abilities as well as when using the second wind ability. This increases the challenge by making combat abilities less forgiving."
        }
    },
    "pickup_mods": {
        "customDrachmaeMultiplier": {
            "name": "Custom Drachmae Multiplier",
            "type": "float",
            "description": "This permits the customisation of drachmae rewards, including random loot. Values less than 1.00 permitted if users want to tone down drachmae rewards.",
            "originalByteArray": "0xC333C0C3CC488B81880000004885C0741280B8D1000000007409F30F1080E8000000C3F30F1005CEF05F02C3CCCCCCCCCCCCCCCCCC",
            "modifiedByteArray": "0x9033C0C3CC488B81880000004885C0741B80B8D1000000007412C780E80000000000E03FF30F1080E8000000C3CCCCCCCCCCCCCCCC",
            "variableOffset": 64,
            "variableType": "float",
            "group": "drachmae_multiplier",
            "visible": True,
            "section": "Player Pickup Mods",
            "help": "This permits the customisation of drachmae rewards, including random loot. Values less than 1.00 permitted if users want to tone down drachmae rewards. Higher values will give you more drachmae from all sources."
        },
        "customDrachmaeMultiplierDisableLowerBound1": {
            "name": "Custom Drachmae Multiplier - Disable Lower Bound",
            "type": "bool",
            "description": "Disable lower bound for drachmae multiplier.",
            "originalByteArray": "0x7208F30F1189C4050000C3CCCCCCCCCCCCCCCCCCCCCCCCCCCC",
            "modifiedByteArray": "0x7200F30F1189C4050000C3CCCCCCCCCCCCCCCCCCCCCCCCCCCC",
            "variableOffset": 0,
            "variableType": "bool",
            "group": "drachmae_multiplier",
            "bounds_logic": "disable_lower_bound",
            "visible": False,
            "section": "Player Pickup Mods"
        },
        "customDrachmaeMultiplierDisableLowerBound2": {
            "name": "Custom Drachmae Multiplier - Disable Lower Bound 2",
            "type": "bool",
            "description": "Disable lower bound for drachmae multiplier.",
            "originalByteArray": "0x76198BC70F57C0F3480F2AC0F30F59C1F3480F2CC08986B00000",
            "modifiedByteArray": "0x76008BC70F57C0F3480F2AC0F30F59C1F3480F2CC08986B00000",
            "variableOffset": 0,
            "variableType": "bool",
            "group": "drachmae_multiplier",
            "bounds_logic": "disable_lower_bound",
            "visible": False,
            "section": "Player Pickup Mods"
        },
        "customDrachmaeMultiplierDisableLowerBound3": {
            "name": "Custom Drachmae Multiplier - Disable Lower Bound 3",
            "type": "bool",
            "description": "Disable lower bound for drachmae multiplier.",
            "originalByteArray": "0x0F2FB1C405000073740F28CEE80B0CCAFF488B8F00020000",
            "modifiedByteArray": "0x0F2FB1C405000074740F28CEE80B0CCAFF488B8F00020000",
            "variableOffset": 0,
            "variableType": "bool",
            "group": "drachmae_multiplier",
            "bounds_logic": "disable_lower_bound",
            "visible": False,
            "section": "Player Pickup Mods"
        },
        "customDrachmaeMultiplierDisableLowerBound4": {
            "name": "Custom Drachmae Multiplier - Disable Lower Bound 4",
            "type": "bool",
            "description": "Disable lower bound for drachmae multiplier.",
            "originalByteArray": "0x0F862B02000084C00F85230200004038B70C0200000F847601000048",
            "modifiedByteArray": "0x0F842B02000084C00F85230200004038B70C0200000F847601000048",
            "variableOffset": 0,
            "variableType": "bool",
            "group": "drachmae_multiplier",
            "bounds_logic": "disable_lower_bound",
            "visible": False,
            "section": "Player Pickup Mods"
        },
        "customResourceLootModifier1": {
            "name": "Custom Resource Loot Modifier 2",
            "type": "bool",
            "description": "Primary patch for resource loot modifier.",
            "originalByteArray": "0xFF50700F57C9B801000000F3480F2ACBF30F59C1F3480F2CC885C90F45C1",
            "modifiedByteArray": "0xFF50700F57C9B801000000F3480F2ACBF30F59C1E953CF160085C90F45C1",
            "variableOffset": 0,
            "variableType": "bool",
            "group": "resource_loot_modifier",
            "visible": False,
            "section": "Player Pickup Mods"
        },
        "customResourceLootModifier2": {
            "name": "Custom Resource Loot Modifier",
            "type": "float",
            "min": 1.0,
            "description": "The amount of resources received when looting can be modified using this tweak. Amounts are scaled by a factor of 2, so setting this to 1 gives 1×2 = 2 times the amount. Setting to 5 yields 1×2×2×2×2×2 = 32 times the amount.",
            "originalByteArray": "0x488B5C24304883C4205FC3CCCCCCCCE93B49F30DCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
            "modifiedByteArray": "0x488B5C24304883C4205FC3CCCCCCCCE93B49F30DCCCCCCB80000C03F660F6ED0F30F59C2F3480F2CC8B801000000E99130E9FF",
            "variableOffset": 48,
            "variableType": "float",
            "group": "resource_loot_modifier",
            "visible": True,
            "section": "Player Pickup Mods",
            "help": "The amount of resources received when looting can be modified using this tweak. Amounts are scaled by a factor of 2, so setting this to 1 gives 1×2 = 2 times the amount. Setting to 5 yields 1×2×2×2×2×2 = 32 times the amount. This applies to all resources except drachmae which has its own dedicated modifier."
        }
    },
    "animal_mods": {
        "customTamedAnimalHealthBoost1": {
            "name": "Tamed Animal Health Boost 2",
            "type": "bool",
            "description": "Primary patch for tamed animal health boost.",
            "originalByteArray": "0x488BCB0F5BC0F30F5980F8010000F3440F2CC0",
            "modifiedByteArray": "0x488BCB0F5BC0F30F5980F8010000E9B9452100",
            "variableOffset": 0,
            "variableType": "bool",
            "group": "tamed_animal_health_boost",
            "visible": False,
            "section": "Animal Mods"
        },
        "customTamedAnimalHealthBoost2": {
            "name": "Animal Companion Health Boost",
            "type": "float",
            "min": 1.0,
            "description": "A tamed animal's max health will be set according to the multiplier the player defines. This stacks with other animal HP bonuses.",
            "originalByteArray": "0xCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC48895C240848896C24104889742418574883EC20488B4228",
            "modifiedByteArray": "0x448B90F4010000C780F40100000000C03FF30F5980F4010000448990F4010000F3440F2CC0E91DBADEFFCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC48895C240848896C24104889742418574883EC20488B4228",
            "variableOffset": 26,
            "variableType": "float",
            "group": "tamed_animal_health_boost",
            "visible": True,
            "section": "Animal Mods",
            "help": "A tamed animal's max health will be set according to the multiplier the player defines. This stacks with other animal HP bonuses. Higher values make your animal companions more durable in combat."
        },
        "customTamedAnimalInCombatHealing": {
            "name": "Animal In Combat Healing",
            "type": "bool",
            "description": "Allows tamed animals to heal whilst in combat.",
            "originalByteArray": "0x837E3802660F6EF00F5BF60F84B0000000",
            "modifiedByteArray": "0x837E3802660F6EF00F5BF6740490909090",
            "variableOffset": 0,
            "variableType": "bool",
            "group": "animal_combat_healing",
            "visible": True,
            "section": "Animal Mods",
            "help": "Allows tamed animals to heal whilst in combat. This makes animal companions much more useful in battle as they can recover health during fights."
        },
        "customTamedAnimalHealingMultiplier1": {
            "name": "Tamed Animal Healing Multiplier 2",
            "type": "bool",
            "description": "Primary patch for tamed animal healing multiplier.",
            "originalByteArray": "0xF30F59059F89C001F30F5886580100000F28C8F30F118658010000",
            "modifiedByteArray": "0xE91B73610E909090F30F5886580100000F28C8F30F118658010000",
            "variableOffset": 0,
            "variableType": "bool",
            "group": "tamed_animal_healing_multiplier",
            "visible": False,
            "section": "Animal Mods"
        },
        "customTamedAnimalHealingMultiplier2": {
            "name": "Animal Healing Multiplier",
            "type": "float",
            "description": "Sets how quickly tamed animals heal. It's usually quite fast, to slow it down ranges between 0.1 and 0.5 are recommended.",
            "originalByteArray": "0xCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC4883EC28488B094885C9742B448B41F848895C2420488D59F84C8D0D909DFFFFBA10000000",
            "modifiedByteArray": "0xF30F59057F165FF341BB0000803E66450F6EDBF3410F59C341BB0000803F66450F6EDBF3410F58C3E9BB8C9EF1CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC4883EC28488B094885C9742B448B41F848895C2420488D59F84C8D0D909DFFFFBA10000000",
            "variableOffset": 20,
            "variableType": "float",
            "group": "tamed_animal_healing_multiplier",
            "visible": True,
            "section": "Animal Mods",
            "help": "Sets how quickly tamed animals heal. It's usually quite fast, to slow it down ranges between 0.1 and 0.5 are recommended. Lower values make animals heal more slowly, while higher values make them heal faster."
        }
    },
    "enemy_mods": {
        "customEnemyHealthMultiplier": {
            "name": "Custom Enemy Health Multiplier",
            "type": "float",
            "description": "This multiplier defines how much health melee opponents will have. Doesn't affect ships.",
            "originalByteArray": "0x74124883C208483BD175EEF30F1005F77A9D01C34885C074F2F30F104010C3CCCCCCCCCCCCCC",
            "modifiedByteArray": "0x74124883C208483BD175EEF30F1005F77A9D01C34885C074F2C740100000C03FF30F104010C3",
            "variableOffset": 56,
            "variableType": "float",
            "group": "enemy_health",
            "visible": True,
            "section": "Enemy Mods",
            "help": "This multiplier defines how much health melee opponents will have. Doesn't affect ships. Higher values make enemies more challenging to defeat."
        },
        "customEnemyDamageMultiplier": {
            "name": "Custom Enemy Damage Multiplier",
            "type": "float",
            "description": "This multiplier defines how much damage melee opponents will do. Doesn't affect ships.",
            "originalByteArray": "0x74124883C208483BD175EEF30F1005477B9D01C34885C074F2F30F10400CC3CCCCCCCCCCCCCC",
            "modifiedByteArray": "0x74124883C208483BD175EEF30F1005477B9D01C34885C074F2C7400C0000C03FF30F10400CC3",
            "variableOffset": 56,
            "variableType": "float",
            "group": "enemy_damage",
            "visible": True,
            "section": "Enemy Mods",
            "help": "This multiplier defines how much damage melee opponents will do. Doesn't affect ships. Higher values make enemies more dangerous in combat."
        },
        "customMaxEnemyLevelDelta": {
            "name": "Custom Max Enemy Level Delta",
            "type": "int",
            "min": 0,
            "max": 255,
            "description": "This sets the maximum level the player can out-level areas and opponent. It basically configures the whole scaling mechanism.",
            "originalByteArray": "0x4883EC28E8372100004885C074088B40184883C428C3B8040000004883C428C3",
            "modifiedByteArray": "0x4883EC28E8372100004885C07400B8FF0000004883C428C3CCCCCCCCCCCCCCCCCC",
            "variableOffset": 30,
            "variableType": "byte",
            "group": "enemy_level_delta",
            "visible": True,
            "section": "Enemy Mods",
            "help": "This sets the maximum level the player can out-level areas and opponent. It basically configures the whole scaling mechanism. Higher values allow for more level difference between player and enemies."
        }
    },
    "misc_mods": {
        "customReducedBountyCooldown": {
            "name": "Reduced Bounty Cooldown",
            "type": "bool",
            "description": "This doubles the cooldown speed for player bounties. It's intended for those who don't like simply paying off bounties and would rather go after bounty sponsors or otherwise feel consequences.",
            "originalByteArray": "0xF30F114B600F2F055003BC01F30F11432C730BC7432C00000000C6434C01488BCBE8420C0500488BCB4883C4205BE9753B0900CCCCCCCCCC",
            "modifiedByteArray": "0xF3410F58C9F30F114B600F2F054B03BC01F30F11432C730BC7432C00000000C6434C01488BCBE83D0C0500488BCB4883C4205BE9703B0900",
            "variableOffset": 0,
            "variableType": "bool",
            "group": "bounty_cooldown",
            "visible": True,
            "section": "Misc Mods",
            "help": "This doubles the cooldown speed for player bounties. It's intended for those who don't like simply paying off bounties and would rather go after bounty sponsors or otherwise feel consequences."
        },
        "customDisableRegionLevels1": {
            "name": "Disable Region Levels",
            "type": "bool",
            "description": "Sets all regions to the player level, and therefore also makes all content based on region level the same level as the player therefore removing the level gating in the game.",
            "originalByteArray": "0x8BC803C63BD876112BD9B80100000083FB010F46D88BFBEB",
            "modifiedByteArray": "0x8BC803C63BD890902BD9B80100000083FB010F46D88BFBEB",
            "variableOffset": 0,
            "variableType": "bool",
            "group": "disable_region_levels",
            "visible": True,
            "section": "Misc Mods",
            "help": "Sets all regions to the player level, and therefore also makes all content based on region level the same level as the player therefore removing the level gating in the game. This makes the world truly open for players to explore at will."
        },
        "customDisableRegionLevels2": {
            "name": "Disable Region Levels Patch 2",
            "type": "bool",
            "description": "Secondary patch for disabling region levels.",
            "originalByteArray": "0x8D0C383BD9760E2BD8413BDD410F46DD41891EEB",
            "modifiedByteArray": "0x8D0C383BD990902BD8413BDD410F46DD41891EEB",
            "variableOffset": 0,
            "variableType": "bool",
            "group": "disable_region_levels",
            "visible": False,
            "section": "Misc Mods"
        }
    }
}

DEADSPACE_TWEAKS = {
    "game_info": {
        "game_id": "deadspace",
        "name": "Dead Space",
        "short_name": "Dead Space",
        "steam_app_id": "1693980",
        "executable_name": "Dead Space.exe",
        "nexus_mods_url": "https://next.nexusmods.com/profile/SparkNV",
        "main_title": "Dead Space Tweaks",
        "tweak_pack_version": "V1.0",
        "subtitle": "Compatible with Dead Space 2023 {compatible_version}",
        "compatible_version": "1.1.14.17871",
        "default": False
    },
    "player_mods": {
        "infinite_stasis": {
            "name": "Infinite Stasis",
            "type": "bool",
            "description": "This makes stasis infinite.",
            "originalByteArray": "0x8B433C89470C8B43388947100FB64348884774",
            "modifiedByteArray": "0xE95C3C5AFF908B43388947100FB64348884774",
            "variableOffset": 0,
            "variableType": "bool",
            "group": "stasis_infinite",
            "visible": True,
            "section": "Stasis",
            "help": "This makes stasis infinite."
        },
        "infinite_stasis2": {
            "name": "Infinite Stasis Patch 2",
            "type": "bool",
            "description": "Secondary patch for infinite stasis.",
            "originalByteArray": "0xCCCCE94B61680BCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
            "modifiedByteArray": "0xCCCCE94B61680BCCCC9C837B48040F85110000004157448B7B3C44897B5066450F6EC7415F9DF3440F114350E980572E02",
            "variableOffset": 0,
            "variableType": "bool",
            "group": "stasis_infinite",
            "visible": False,
            "section": "Stasis"
        }
    },
    "pickup_mods": {
        "infinite_ammo_pouch": {
            "name": "Infinite Ammo Pouch",
            "type": "bool",
            "description": "This makes ammo pouch infinite.",
            "originalByteArray": "0xCC8B4218894118C3",
            "modifiedByteArray": "0xCCE9A4B14CFFC3C3",
            "variableOffset": 0,
            "variableType": "bool",
            "group": "pouch_infinite",
            "visible": True,
            "section": "Ammo",
            "help": "This makes stasis infinite."
        },
        "infinite_ammo_pouch2": {
            "name": "Infinite Ammo Pouch 2",
            "type": "bool",
            "description": "Secondary patch for infinite pouch.",
            "originalByteArray": "0xE9BB5B410ECCCCAACCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
            "modifiedByteArray": "0xE9BB5B410ECCCCAACCC74218200000008B4218894118E94A4EB300CC",
            "variableOffset": 0,
            "variableType": "bool",
            "group": "pouch_infinite",
            "visible": False,
            "section": "Ammo"
        }
    }
}

EMBEDDED_TWEAKS = {
    "ac_odyssey": AC_ODYSSEY_TWEAKS,
    "deadspace": DEADSPACE_TWEAKS
}

def get_embedded_tweak_data(game_id: str):
    return EMBEDDED_TWEAKS.get(game_id, {})

def get_all_embedded_game_ids():
    return list(EMBEDDED_TWEAKS.keys())

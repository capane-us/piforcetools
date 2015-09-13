# This file contains a dictionary of game names to file names.  Keep in mind game names are displayed on a 16x2 LCD display,
# so some game names must be split with a newline or abbreviated to fit.  Feel free to change names to whatever
# you like.  At load time, files that don't exist will be purged from the dictionary, so no need to trim this.  
# If you have a ROM dump with a different filename, either rename the .bin file or change the config here. 
# This is a python script, so make sure whatever changes you make to this file are syntactically correct.

from labels import *

GAME_LIST = { 
        # ATOMISWAVE GAMES
        ATOMISWAVE: {         
            GAMES: {
                ACTION: {
                    "Demolish\nFist":                       "Demolish_Fist.bin",
                    "Dolphin\nBlue":                        "dol222.bin",
                    "Metal Slug\n6":                        "MetalSlug6.bin",
                    "Knights of Valor\nSeven Spirits":      "kov7spirits.bin"
                },
                # Fighting games
                FIGHTING: {
                    "Guilty Gear X\nV1.5":                  "ggx15.bin",
                    "Guilty Gear\nIsuka":                   "Guilty_Gear_Isuka.bin",
                    "Fist of the\nNorth Star":              "FOTNS_Naomi2_Fixed.bin",
                    "Samurai\nShodown VI":                  "SamuraiShowdownVI_SamuraiSpirits_v4.bin",
                    "KOF\nNeowave":                         "KingOfFightersNewWave.bin",
                    "KOF 11":                               "gdrom_KOFXI_controles_JVS_OK_Video_OK_v4.bin",
                    "The Rumble\nFish":                     "The_Rumble_Fish.bin",
                    "The Rumble\nFish 2":                   "gdrom_rumblef2_v4.bin"
                },
                RACING: {
                    "Faster Than\nSpeed":                   "ftspeed.bin"
                },
                SHOOTER: {
                    "Sports\nShooting USA":                 "gdrom_sprtshot.bin"
                },
                SPORT: {
                    "Dirty\nPigskin Football":              "gdrom_dirtypigskin_v3.bin"
                },
                VARIOUS: {
                    "Animal\nBasket":                       "gdrom_anmlbskt.bin",
                    "Salary Man\nKintaro":                  "gdrom_salmankt_JVS_OK_BIOS_OK_Video_OK.bin"
                }
            },
            # All the systems in which you may push the .bin. Must be defined in "ips" list. Each systems need to be separated by
            # a comma except the last one. The first one is the default one.
            SYSTEMS: [
                    "Naomi 1 #1", 
                    "Naomi 2 #2", 
                    "Naomi 2 #3"
            ]
        },
         #NAOMI 1 GAMES
         NAOMI1: {
            GAMES: {
                ACTION: {
                    "Airline Pilot":                        "AirlinePilots.bin",
                    "Cosmic Smash":                         "CosmicSmash.bin",
                    "Dynamite Deka Ex":                     "DynamiteDekaEx.bin",
                    "Gunspike":                             "GunSpike.bin",
                    "Heavy Metal\nGeomatrix":               "HeavyMetalGeomatrix.bin",
                    "Mob Suit Gundam\nFed. Vs Zeon":        "MobileSuitGundam-FederationVsZeon.bin",
                    "Mob Suit Gundam\nFed. Vs Zeon DX":     "MobileSuitGundam-FederationVsZeonDX.bin",
                    "Monkey Ball":                          "MonkeyBall.bin",
                    "Musapeys Choco\nMarker":               "MusapeysChocoMarker.bin",
                    "Power Stone":                          "Powerstone.bin",
                    "Power Stone 2":                        "PowerStone2.bin",
                    "SlashOut":                             "Slashout.bin",
                    "Spawn":                                "spawn.bin",
                    "Spikers Battle":                       "SpikersBattle.bin",
                    "Zombie Revenge":                       "ZombieRevenge.bin"
                },
                FIGHTING: {
                    "Akatsuki Blitz\nkampf Auf Asche":      "Akatsuki_Bk_Ausf_Achse.bin",
                    "Capcom vs. SNK\nM. Fight 2K":          "Capcom_vs_SNK_Millenium_Fight_2000.bin",
                    "Capcom vs. SNK\nM. Fight 2K Pro":      "Capcom_vs_SNK_Millenium_Fight_2000_Pro.bin",
                    "Capcom vs. SNK 2\nM. Fighting 2001":   "Capcom_Vs_SNK_2_Millionaire_Fighting_2001.bin",
                    "Dead or Alive 2":                      "DeadOrAlive2.bin",
                    "Dead or Alive 2\nMillenium":           "DeadOrAlive2Millenium.bin",
                    "Giant Gram Zen.\nPro Wrestle 2":       "Giant_Gram_EPR-21820_PATCHED.bin",
                    "Giant Gram 2K Zn\nPro Wrestle 3":      "Giant_Gram_2000.bin",
                    "Guilty Gear XX":                       "GuiltyGearXX.bin",
                    "Guilty Gear XX\nReload":               "GuiltyGearXXReload.bin",
                    "Guilty Gear XX\nSlash":                "GuiltyGearXXSlash_v6.bin",
                    "Guilty Gear XX\nAccent Core":          "GuiltyGearXXAccentCore_v6.bin",
                    "Jingy Storm\nThe Arcade":              "JingyStormTheArcade.bin",
                    "Marvel vs.\nCapcom 2":                 "MarvelVsCapcom2.bin",
                    "Melty Blood\nActress Again NP":        "MeltyBloodActressAgain.bin",
                    "Melty Blood\nActress Again":           "MeltyBloodActressAgain_v6.bin",
                    "Melty Blood\nAct Cadenza [A]":         "MeltyBloodActCadenza(RevA).bin",
                    "Melty Blood\nAct Cadenza [B]":         "MeltyBloodActCadenzaVerB_v3.bin",
                    "Melty Blood\nAct Cadenza [B2]":        "MeltyBloodActCadenzaVerB2_v3.bin",
                    "Project Justice\nRival School 2":      "RivalSchools2_ProjectJustice.bin",
                    "Street Fighter\nZero 3 Upper":         "StreetFighterZero3Upper.bin",
                    "Toy Fighter":                          "ToyFighter.bin",
                    "WWF Royal Rumble":                     "WWF_Royal_Rumble.bin"
                },
                HORI_SHOOTEMUP: {
                    "Border Down":                          "BorderDown_v3.bin",
                    "Chaos Field":                          "ChaosField_v3.bin",
                    "Gigawing 2":                           "GigaWing2.bin",
                    "Radirgy":                              "Radirgy_v3.bin", 
                    "Radirgy Noa":                          "RadirgyNoa_v6.bin",
                    "Senko no Ronde":                       "senkov3.bin",
                    "Senko no Ronde\nNew Ver":              "senkonewv6.bin",
                    "Senko no Ronde\nSP":                   "SenkoNoRondeSP_v3.bin",
                    "Zero Gunner 2":                        "ZeroGunner2.bin"
                },
                PUZZLE:{
                    "Azumanga Daioh\nPuzzle Bobble":        "AzumangaDaiohPuzzleBobble_v3.bin",
                    "Burning Casino":                       "BurningCasino_v3.bin",
                    "Cleopatra\nFortune Plus":              "CleopatraFortunePlus_v6.bin",
                    "Doki Doki Idol\nStar Seeker":          "DokiDokiIdolStarSeeker.bin",
                    "Kuru Kuru\nChameleon":                 "KuruKuruChameleon_v3.bin",
                    "Nomiso Kone Kone\nPuzzle Takoron":     "NoukonePuzzleTakoron.bin",
                    "Puyo Puyo Da":                         "Puyo_Puyo_Da_EPR-22206_PATCHED.bin",
                    "Puyo Puyo Fever":                      "PuyoPuyoFever_v6.bin",
                    "Sega Tetris":                          "SegaTetris.bin",
                    "Super Shanghai\n2005":                 "SuperShanghai2005_v6.bin",
                    "Super Shanghai\n2005 [A]":             "SuperShanghai2005VerA_v6.bin",
                    "Tetris\nKiwamemichi":                  "TetrisKiwamemichi_v6.bin",
                    "Usagui Yamashiro\nMahjong Hen":        "Usagui_YamashiroMahjongHen_v3.bin"
                },
                RACING: {
                    "18 Wheeler (STD)":                     "18_Wheeler_STD.bin",
                    "18 Wheeler (DLX)":                     "18_Wheeler_DX.bin", 
                    "Crazy Taxi":                           "CrazyTaxi.bin"
                },
                SHOOTER: {
                    "Confidential\nMission":                "ConfidentialMission.bin",
                    "Death Crimson OX":                     "DeathCrimsonOX.bin",
                    "Jambo Safari":                         "Jambo_Safari.bin",
                    "Lupin 3\nThe Shooting":                "Lupin3_TheShooting.bin",
                    "Maze of the King":                     "TheMazeOfTheKings.bin"
                },
                SPORT: {
                    "Sports Jam":                           "SportsJam.bin",
                    "Virtua Athlete":                       "VirtuaAthlete.bin",
                    "Virtua Golf":                          "VirtuaGolf.bin",
                    "Virtua NBA":                           "VirtuaNBA.bin",
                    "Virtua Striker 2\nVer. 2000":          "VirtuaStriker2-2000.bin",
                    "Virtua Tennis":                        "VirtuaTennis.bin",
                    "Virtua Tennis 2":                      "VirtuaTennis2.bin",
                    "Wave Runner GP":                       "WaveRunnerGP.bin",
                    "World Series\nBaseball":               "WorldSeriesBaseball.bin"
                },
                VARIOUS:{
                    "Alien Front":                          "AlienFront.bin",
                    "La Keyboard xyu":                      "LaKeyboardxyu_v3.bin",
                    "Lupin\nThe Typing":                    "Lupin_TheTyping.bin",
                    "Quiz Keitai\nQ Mode":                  "QuizKeitaiQMode.bin",
                    "Samba de Amigo":                       "Samba_De_Amigo_EPR-22966B_Patched.bin",
                    "Sega \nMarine Fishing":                "Sega_Marine_Fishing_EPR-22221.bin",
                    "Sega\nStrike Fighter":                 "SegaStrikeFighter.bin",
                    "Typing of\nthe Dead":                  "TheTypingOfTheDead.bin"
                },
                VERT_SHOOTEMUP: {
                    "Ikaruga":                              "Ikaruga_v3.bin",
                    "Illvelo":                              "Illvelo_v6.bin",
                    "Karous":                               "karous_v3.bin",
                    "Mamoru-kun wa\nNoro. Shimatta!":       "mamonorov6.bin",
                    "Psyvariar 2":                          "Psyvariar2_v6.bin",
                    "Shikigami\nno Shiro II":               "ShikigamiNoShiroII_v6.bin",
                    "Shooting Love\n2007 - Exzeal":         "ShootingLove2007-Exzeal_v6.bin",
                    "Trigger Heart\nExelica":               "TriggerHeartExelica_v6.bin",
                    "Trizeal":                              "Trizeal_v3.bin",
                    "Under Defeat":                         "UnderDefeat_v3.bin"
                }
            },
            # All the systems in which you may push the .bin. Must be defined in "ips" list. Each systems need to be separated by
            # a comma except the last one. The first one is the default one.
            SYSTEMS: [
                    "Naomi 1 #1",
                    "Naomi 2 #1", 
                    "Naomi 2 #2", 
                    "Naomi 2 #3"
            ]
        },
        #NAOMI 2 GAMES
        NAOMI2: {
            GAMES: {
                # Fighting games
                FIGHTING: {
                    "Virtua Fighter 4":                     "VirtuaFighter4.bin", 
                    "Virtua Fighter 4\nVer. B":             "VirtuaFighter4_verb.bin",
                    "Virtua Fighter 4\nVer. C":             "VirtuaFighter4_verc.bin",
                    "Virtua Fighter 4\nEvo":                "VirtuaFighter4Evo.bin",
                    "Virtua Fighter 4\nEvo Ver. B":         "VirtuaFighter4Evo_verb.bin",
                    "Virtua Fighter 4\nFinal Tuned":        "VirtuaFighter4FinalTuned.bin",
                    "Virtua Fighter 4\nFinal Tuned [A]":    "VirtuaFighter4FinalTuned_vera.bin",
                    "Virtua Fighter 4\nFinal Tuned [B]":    "VirtuaFighter4FinalTuned_verb.bin"
                },
                # Racing games
                RACING: {
                    "Club Kart\nEuropean Session":          "ClubKartEuropeanSessionUnlocked.bin",
                    "Initial D\nExport":                    "InitialDexp.bin",
                    "Initial D \nJapanese":                 "InitialDjap.bin",
                    "Initial D 2\nExport":                  "InitialD2exp.bin",
                    "Initial D 2\nJapanese":                "InitialD2jap.bin",
                    "Initial D 2\nJapanese [B]":            "InitialD2jap-revb.bin",
                    "Initial D 3\nExport":                  "Initial_D3_Export.bin",
                    "King Of\nRoute 66":                    "KingOfRoute66.bin"
                },
                # Sport games
                SPORT: {
                    "Beach Spikers":                        "BeachSpikers.bin",
                    "Virtua Striker 3":                     "VirtuaStriker3.bin"
                }  
            },
            # All the systems in which you may push the .bin. Must be defined in "ips" list. Each systems need to be separated by
            # a comma except the last one. The first one is the default one.
            SYSTEMS: [
                    "Naomi 2 #1", 
                    "Naomi 2 #2", 
                    "Naomi 2 #3"
            ]
        },
        #CHIHIRO GAMES
        CHIHIRO: {
            GAMES: {
                # Racing games
                RACING: {
                    "Crazy Taxi\nHigh Roller":            "CrazyTaxiHighRoller.bin",
                    "Out Run 2\n512MB":                   "OR2_512.bin",
                    "Out Run 2\n1GB":                     "OR2_1gb.bin",
                    "Out Run 2\nBETA":                    "OR2BETA.bin",
                    "Out Run 2 SP":                       "or2sp_1gb.bin",
                    "Out Run 2\nSpec Tours 512MB":        "Outrun_2_Special_Tours_512.bin",
                    "Out Run 2\nSpec Tours 1GB":          "Outrun_2_Special_Tours_1GB.bin",
                    "Wangan Midnight\nMax Tune (EXP)":    "Wangan_Midnight_Maximum_Tune_EXPORT_(GDX-0009B).bin",
                    "Wangan Midnight\nMax Tune 512MB":    "Wangan_Midnight_Maximum_Tune_EXP_512.bin",
                    "Wangan Midnight\nMax Tune 1GB":      "Wangan_Midnight_Maximum_Tune_EXP_1GB.bin",
                    "Wangan Midnight\nMax Tune 2 (JAP)":  "Wangan_Midnight_Maximum_Tune_2_JAP_(GDX-0015).bin",
                    "Wangan Midnight\nMax Tune 2 512MB":  "Wangan_Midnight_Maximum_Tune_2_JAP_512.bin",
                    "Wangan Midnight\nMax Tune 2 1GB":    "Wangan_Midnight_Maximum_Tune_2_JAP_1GB.bin",
                    "Wangan Midnight\nMax Tune 2B 512M":  "Wangan_Midnight_Maximum_Tune_2B_EXP_512.bin",
                    "Wangan Midnight\nMax Tune 2B 1GB":   "Wangan_Midnight_Maximum_Tune_2B_EXP_1GB.bin"
                },
                # Shooter games
                SHOOTER: {
                    "Virtua Cop 3\n512MB":                "Virtua_Cop_3_512.bin",
                    "Virtua Cop 3\n1GB":                  "Virtua_Cop_3_1GB.bin",
                    "Ghost Squad\n512M":                  "Ghost_Squad_Ver._A_512.bin",
                    "Ghost Squad \n1GB":                  "Ghost_Squad_Ver._A_1GB.bin",
                    "The House Of\nThe Dead 3":           "The_House_Of_The_Dead_3_GDX-0001.bin",
                },
                # Sport games
                SPORT: {
                    "Sega Golf Club\n2006 NT 512MB":      "Sega_Golf_Club_Version_2006_Next_Tours_Rev.A_512.bin",
                    "Sega Golf Club\n2006 NT 1GB":        "Sega_Golf_Club_Version_2006_Next_Tours_Rev.A_1GB.bin"
                },
                # Action games
                ACTION: {
                    "Gundam Battle\nOperating Sim.":      "Gundam_Battle_Operating_Simulator.bin",
                    "Ollie King\n512MB":                  "Ollie_King_512.bin",
                    "Ollie King\n1GB":                    "Ollie_King_1GB.bin"
                }
            },
            # All the systems in which you may push the .bin. Must be defined in "ips" list. Each systems need to be separated by
            # a comma except the last one. The first one is the default one.
            SYSTEMS: [
                    "Chihiro"
            ]
        },
        #TRIFORCE GAMES
        TRIFORCE: {
            GAMES: {
                RACING: {
                    "F-Zero AX":                          "FZeroAx.bin",
                    "Mario Kart\nArcade GP":              "MarioKartGP.bin",
                    "Mario Kart\nArcade GP 2":            "MarioKartGP2.bin"
                },
                SPORT: {
                    "Virtua Striker\n2002":               "vs2002e.bin",
                    "Virtua Striker 4\nv2006":            "vs406.bin",
                    "Virtua Striker 4\n2006 (Export)":    "Virtua_Striker_4_2006_Exp.bin"
                }
            },
            # All the systems in which you may push the .bin. Must be defined in "ips" list. Each systems need to be separated by
            # a comma except the last one. The first one is the default one.
            SYSTEMS: [
                    "Triforce #1"
            ]
        }
}
Table: Country
Columns:
- id: the unique id for countries
- name: country name
Example Values:
- name: Germany | Portugal | Belgium

Table: Examination
Columns:
- ID: identification of the patient
- Examination Date: Examination Date
- aCL IgG: anti-Cardiolipin antibody (IgG) concentration
- aCL IgM: anti-Cardiolipin antibody (IgM) concentration
- ANA: anti-nucleus antibody concentration
- ANA Pattern: pattern observed in the sheet of ANA examination
- aCL IgA: anti-Cardiolipin antibody (IgA) concentration
- Diagnosis: disease names
- KCT: measure of degree of coagulation
- RVVT: measure of degree of coagulation
- LAC: measure of degree of coagulation
- Symptoms: other symptoms observed
- Thrombosis: degree of thrombosis
Example Values:
- Examination Date: 1995-11-08 | 1996-01-10 | 1996-11-21
- aCL IgG: 1.1 | 2.3 | 1.3
- aCL IgM: 1.7 | 10.7 | 0.7
- ANA: 4096 | 4 | 0
- ANA Pattern: P,S | S,P | P
- aCL IgA: 0 | 19 | 12
- Diagnosis: SLE, SjS, vertigo | APS | SLE, SjS
- KCT: - | +
- RVVT: + | -
- LAC: + | -
- Symptoms: thrombophlebitis | brain infarction | Apo
- Thrombosis: 1 | 3 | 0

Table: Laboratory
Columns:
- ID: identification of the patient
- Date: Date of the laboratory tests (YYMMDD)
- GOT: AST glutamic oxaloacetic transaminase
- GPT: ALT glutamic pyruvic transaminase
- LDH: lactate dehydrogenase
- ALP: alkaliphophatase
- TP: total protein
- ALB: albumin
- UA: uric acid
- UN: urea nitrogen
- CRE: creatinine
- T-BIL: total bilirubin
- T-CHO: total cholesterol
- TG: triglyceride
- CPK: creatinine phosphokinase
- GLU: blood glucose
- WBC: White blood cell
- RBC: Red blood cell
- HGB: Hemoglobin
- HCT: Hematoclit
- PLT: platelet
- PT: prothrombin time
- APTT: activated partial prothrombin time
- FG: fibrinogen
- PIC
- TAT
- TAT2
- U-PRO: proteinuria
- IGG: Ig G
- IGA: Ig A
- IGM: Ig M
- CRP: C-reactive protein
- RA: Rhuematoid Factor
- RF: RAHA
- C3: complement 3
- C4: complement 4
- RNP: anti-ribonuclear protein
- SM: anti-SM
- SC170: anti-scl70
- SSA: anti-SSA
- SSB: anti-SSB
- CENTROMEA: anti-centromere
- DNA: anti-DNA
- DNA-II: anti-DNA
Example Values:
- Date: 1985-11-16 | 1983-12-20 | 1986-01-29
- GOT: 131 | 113 | 47
- GPT: 3 | 80 | 165
- LDH: 172 | 781 | 338
- ALP: 94 | 328 | 429
- TP: 1.8 | 7.1 | 6.5
- ALB: 5.6 | 3.3 | 4.1
- UA: 9.3 | 10.7 | 3.1
- UN: 123 | 98 | 21
- CRE: 0.8 | 5.2 | 13.5
- T-BIL: 0.4 | 0.1 | 0.7
- T-CHO: 240 | 126 | 439
- TG: 93 | 190 | 332
- CPK: 308 | 42 | 143
- GLU: 66 | 119 | 104
- WBC: 21.0 | 8.3 | 21.1
- RBC: 4.7 | 4.4 | 2.2
- HGB: 16.2 | 5.0 | 6.0
- HCT: 51.7 | 28.2 | 41.5
- PLT: 309 | 163 | 223
- PT: 13.3 | 19.4 | 20.0
- APTT: 101 | 90 | 92
- FG: 52.8 | 33.2 | 51.9
- PIC: 529 | 165 | 253
- TAT: 150 | 151 | 170
- TAT2: 86 | 135 | 119
- U-PRO: 0 | 1 | >=300
- IGG: 1462 | 1469 | 1899
- IGA: 119 | 549 | 493
- IGM: 840 | 66 | 44
- CRP: 4.7 | 0.51 | 5
- RA: 7- | - | +-
- RF: 21.8 | 87.3 | 37.1
- C3: 130 | 126 | 145
- C4: 12 | 42 | 44
- RNP: 1 | 0 | 15
- SM: 8 | negative | 1
- SC170: 4 | negative | 1
- SSA: 16 | negative | 4
- SSB: negative | 2 | 32
- CENTROMEA: negative | 0
- DNA: 95.5 | 16.6 | 100

Table: League
Columns:
- id: the unique id for leagues
- country_id: the unique id for countries
- name: league name
Example Values:
- name: Germany 1. Bundesliga | Italy Serie A | Netherlands Eredivisie

Table: Match
Columns:
- id: the unique id for matches
- country_id: country id
- league_id: league id
- season: the season of the match
- stage: the stage of the match
- date: the date of the match
- match_api_id: the id of the match api
- home_team_api_id: the id of the home team api
- away_team_api_id: the id of the away team api
- home_team_goal: the goal of the home team
- away_team_goal: the goal of the away team
- home_player_X1
- home_player_X2
- home_player_X3
- home_player_X4
- home_player_X5
- home_player_X6
- home_player_X7
- home_player_X8
- home_player_X9
- home_player_X10
- home_player_X11
- away_player_X1
- away_player_X2
- away_player_X3
- away_player_X4
- away_player_X5
- away_player_X6
- away_player_X7
- away_player_X8
- away_player_X9
- away_player_X10
- away_player_X11
- home_player_Y1
- home_player_Y2
- home_player_Y3
- home_player_Y4
- home_player_Y5
- home_player_Y6
- home_player_Y7
- home_player_Y8
- home_player_Y9
- home_player_Y10
- home_player_Y11
- away_player_Y1
- away_player_Y2
- away_player_Y3
- away_player_Y4
- away_player_Y5
- away_player_Y6
- away_player_Y7
- away_player_Y8
- away_player_Y9
- away_player_Y10
- away_player_Y11
- home_player_1
- home_player_2
- home_player_3
- home_player_4
- home_player_5
- home_player_6
- home_player_7
- home_player_8
- home_player_9
- home_player_10
- home_player_11
- away_player_1
- away_player_2
- away_player_3
- away_player_4
- away_player_5
- away_player_6
- away_player_7
- away_player_8
- away_player_9
- away_player_10
- away_player_11
- goal: the goal of the match
- shoton: the shot on goal of the match
- shotoff: the shot off goal of the match, which is the opposite of shot on
- foulcommit: the fouls occurred in the match
- card: the cards given in the match
- cross: Balls sent into the opposition team's area from a wide position in the match
- corner: Ball goes out of play for a corner kick in the match
- possession: The duration from a player taking over the ball in the match
- B365H
- B365D
- B365A
- BWH
- BWD
- BWA
- IWH
- IWD
- IWA
- LBH
- LBD
- LBA
- PSH
- PSD
- PSA
- WHH
- WHD
- WHA
- SJH
- SJD
- SJA
- VCH
- VCD
- VCA
- GBH
- GBD
- GBA
- BSH
- BSD
- BSA
Example Values:
- season: 2010/2011 | 2012/2013 | 2008/2009
- stage: 5 | 6 | 27
- date: 2015-04-07 00:00:00 | 2008-08-22 00:00:00 | 2011-10-25 00:00:00
- home_team_goal: 6 | 9 | 3
- away_team_goal: 1 | 7 | 5
- home_player_X1: 2 | 0 | 1
- home_player_X2: 0 | 6 | 1
- home_player_X3: 6 | 8 | 4
- home_player_X4: 5 | 3 | 6
- home_player_X5: 8 | 3 | 6
- home_player_X6: 7 | 4 | 5
- home_player_X7: 5 | 1 | 6
- home_player_X8: 4 | 9 | 6
- home_player_X9: 1 | 4 | 7
- home_player_X10: 7 | 2 | 6
- home_player_X11: 3 | 6 | 7
- away_player_X1: 6 | 1 | 2
- away_player_X2: 3 | 6 | 4
- away_player_X3: 5 | 8 | 3
- away_player_X4: 5 | 4 | 3
- away_player_X5: 5 | 3 | 1
- away_player_X6: 4 | 3 | 5
- away_player_X7: 8 | 6 | 3
- away_player_X8: 4 | 8 | 1
- away_player_X9: 9 | 4 | 7
- away_player_X10: 4 | 7 | 5
- away_player_X11: 7 | 8 | 4
- home_player_Y1: 3 | 1 | 0
- home_player_Y2: 0 | 3
- home_player_Y3: 5 | 3
- home_player_Y4: 5 | 3
- home_player_Y5: 8 | 3 | 7
- home_player_Y6: 3 | 5 | 9
- home_player_Y7: 3 | 5 | 8
- home_player_Y8: 10 | 9 | 6
- home_player_Y9: 6 | 1 | 10
- home_player_Y10: 7 | 6 | 11
- home_player_Y11: 3 | 1 | 11
- away_player_Y1: 1 | 3
- away_player_Y2: 3
- away_player_Y3: 3 | 7
- away_player_Y4: 5 | 3 | 7
- away_player_Y5: 5 | 7 | 3
- away_player_Y6: 5 | 7 | 6
- away_player_Y7: 5 | 7 | 9
- away_player_Y8: 6 | 5 | 10
- away_player_Y9: 7 | 5 | 9
- away_player_Y10: 10 | 8 | 9
- away_player_Y11: 8 | 7 | 11
- home_player_1: 33688 | 38617 | 46531
- home_player_2: 36085 | 36008 | 89185
- home_player_3: 277608 | 93064 | 33408
- home_player_4: 154228 | 49885 | 38956
- home_player_5: 512723 | 209950 | 39621
- home_player_6: 23070 | 12371 | 156097
- home_player_7: 279490 | 37774 | 468931
- home_player_8: 40187 | 24655 | 182765
- home_player_9: 24661 | 31314 | 31325
- home_player_10: 41232 | 119273 | 130027
- home_player_11: 119435 | 95094 | 23724
- away_player_1: 38628 | 500575 | 110154
- away_player_2: 24446 | 131532 | 167648
- away_player_3: 27669 | 277234 | 36322
- away_player_4: 6864 | 42388 | 32833
- away_player_5: 63520 | 421441 | 31014
- away_player_6: 188506 | 68827 | 361757
- away_player_7: 244458 | 71780 | 37471
- away_player_8: 46881 | 560564 | 558136
- away_player_9: 473822 | 33637 | 42263
- away_player_10: 114339 | 32617 | 39045
- away_player_11: 503629 | 238438 | 232253
- goal: <goal><value><comment>n</comment><stats><goals>... | <goal><value><comment>n</comment><stats><goals>... | <goal><value><comment>n</comment><stats><goals>...
- shoton: <shoton><value><stats><shoton>1</shoton></stats... | <shoton><value><stats><shoton>1</shoton></stats... | <shoton><value><stats><shoton>1</shoton></stats...
- shotoff: <shotoff><value><stats><shotoff>1</shotoff></st... | <shotoff><value><stats><shotoff>1</shotoff></st... | <shotoff><value><stats><shotoff>1</shotoff></st...
- foulcommit: <foulcommit><value><stats><foulscommitted>1</fo... | <foulcommit><value><stats><foulscommitted>1</fo... | <foulcommit><value><stats><foulscommitted>1</fo...
- card: <card><value><comment>y</comment><stats><ycards... | <card><value><comment>y</comment><stats><ycards... | <card><value><comment>y</comment><stats><ycards...
- cross: <cross><value><stats><crosses>1</crosses></stat... | <cross><value><stats><crosses>1</crosses></stat... | <cross><value><stats><crosses>1</crosses></stat...
- corner: <corner><value><stats><corners>1</corners></sta... | <corner><value><stats><corners>1</corners></sta... | <corner><value><stats><corners>1</corners></sta...
- possession: <possession><value><comment>35</comment><stats>... | <possession><value><comment>48</comment><stats>... | <possession><value><comment>52</comment><event_...
- B365H: 3.1 | 3.9 | 1.4
- B365D: 1.7 | 4.25 | 2.05
- B365A: 5.0 | 4.2 | 4.5
- BWH: 1.19 | 4.6 | 2.95
- BWD: 3.5 | 2.7 | 3.0
- BWA: 3.55 | 1.95 | 9.4
- IWH: 2.75 | 1.07 | 3.55
- IWD: 5.8 | 2.0 | 6.0
- IWA: 1.12 | 2.9 | 2.95
- LBH: 4.2 | 3.75 | 11.0
- LBD: 4.4 | 3.6 | 8.0
- LBA: 9.5 | 26.0 | 18.0
- PSH: 6.51 | 16.81 | 3.64
- PSD: 5.22 | 3.77 | 16.5
- PSA: 9.25 | 19.44 | 21.4
- WHH: 1.08 | 1.1 | 4.5
- WHD: 7.5 | 1.73 | 1.6
- WHA: 6.5 | 5.6 | 9.5
- SJH: 1.8 | 6.75 | 1.41
- SJD: 3.6 | 6.75 | 2.88
- SJA: 1.615 | 1.44 | 15.0
- VCH: 3.6 | 1.53 | 3.125
- VCD: 26.0 | 3.2 | 3.7
- VCA: 1.833 | 1.3 | 3.25
- GBH: 2.3 | 2.9 | 4.33
- GBD: 2.4 | 1.67 | 7.75
- GBA: 25.0 | 2.2 | 7.75
- BSH: 5.0 | 1.61 | 2.38
- BSD: 10.0 | 2.38 | 12.0
- BSA: 1.17 | 5.5 | 3.4

Table: Patient
Columns:
- ID: identification of the patient
- SEX: Sex
- Birthday: Birthday
- Description: the first date when a patient data was recorded
- First Date: the date when a patient came to the hospital
- Admission: patient was admitted to the hospital (+) or followed at the outpatient clinic (-)
- Diagnosis: disease names
Example Values:
- SEX:  | M | F
- Birthday: 1967-03-18 | 1962-11-28 | 1943-07-03
- Description: 1998-07-01 | 1996-12-12 | 1994-02-01
- First Date: 1996-06-04 | 1994-03-11 | 1985-10-28
- Admission:  | +( | +
- Diagnosis: relapsing polychondritis | PSS/CREST | Vasculitis synd, PN susp

Table: Player
Columns:
- id: the unique id for players
- player_api_id: the id of the player api
- player_name: player name
- player_fifa_api_id: the id of the player fifa api
- birthday: the player's birthday
- height: the player's height
- weight: the player's weight
Example Values:
- player_name: Guus Hupperts | James Tomkins | Nampalys Mendy
- birthday: 1991-12-23 00:00:00 | 1992-12-18 00:00:00 | 1973-03-23 00:00:00
- height: 173 | 198 | 175
- weight: 214 | 130 | 150

Table: Player_Attributes
Columns:
- id: the unique id for players
- player_fifa_api_id: the id of the player fifa api
- player_api_id: the id of the player api
- date: date
- overall_rating: the overall rating of the player
- potential: potential of the player
- preferred_foot: the player's preferred foot when attacking
- attacking_work_rate: the player's attacking work rate
- defensive_work_rate: the player's defensive work rate
- crossing: the player's crossing score
- finishing: the player's finishing rate
- heading_accuracy: the player's heading accuracy
- short_passing: the player's short passing score
- volleys: the player's volley score
- dribbling: the player's dribbling score
- curve: the player's curve score
- free_kick_accuracy: the player's free kick accuracy
- long_passing: the player's long passing score
- ball_control: the player's ball control score
- acceleration: the player's acceleration score
- sprint_speed: the player's sprint speed
- agility: the player's agility
- reactions: the player's reactions score
- balance: the player's balance score
- shot_power: the player's shot power
- jumping: the player's jumping score
- stamina: the player's stamina score
- strength: the player's strength score
- long_shots: the player's long shots score
- aggression: the player's aggression score
- interceptions: the player's interceptions score
- positioning: the player's 
positioning score
- vision: the player's vision score
- penalties: the player's penalties score
- marking: the player's markingscore
- standing_tackle: the player's standing tackle score
- sliding_tackle: the player's sliding tackle score
- gk_diving: the player's goalkeep diving score
- gk_handling: the player's goalkeep diving score
- gk_kicking: the player's goalkeep kicking score
- gk_positioning: the player's goalkeep positioning score
- gk_reflexes: the player's goalkeep reflexes score
Example Values:
- date: 2015-11-06 00:00:00 | 2016-02-04 00:00:00 | 2014-11-07 00:00:00
- overall_rating: 82 | 59 | 41
- potential: 62 | 47 | 88
- preferred_foot: left | right
- attacking_work_rate: norm | None | y
- defensive_work_rate: 6 | 1 | 4
- crossing: 89 | 9 | 42
- finishing: 56 | 8 | 2
- heading_accuracy: 52 | 8 | 55
- short_passing: 80 | 3 | 90
- volleys: 70 | 89 | 14
- dribbling: 71 | 85 | 14
- curve: 85 | 38 | 69
- free_kick_accuracy: 27 | 72 | 40
- long_passing: 54 | 43 | 12
- ball_control: 6 | 7 | 23
- acceleration: 19 | 20 | 62
- sprint_speed: 36 | 79 | 64
- agility: 89 | 81 | 44
- reactions: 72 | 42 | 58
- balance: 26 | 60 | 89
- shot_power: 21 | 5 | 16
- jumping: 88 | 42 | 24
- stamina: 22 | 39 | 27
- strength: 16 | 42 | 79
- long_shots: 91 | 22 | 49
- aggression: 27 | 76 | 22
- interceptions: 14 | 9 | 58
- positioning: 58 | 23 | 10
- vision: 68 | 84 | 66
- penalties: 83 | 12 | 58
- marking: 86 | 22 | 19
- standing_tackle: 82 | 69 | 21
- sliding_tackle: 41 | 67 | 59
- gk_diving: 62 | 3 | 33
- gk_handling: 74 | 84 | 73
- gk_kicking: 50 | 62 | 5
- gk_positioning: 31 | 36 | 83
- gk_reflexes: 53 | 60 | 62

Table: Team
Columns:
- id: the unique id for teams
- team_api_id: the id of the team api
- team_fifa_api_id: the id of the team fifa api
- team_long_name: the team's long name
- team_short_name: the team's short name
Example Values:
- team_long_name: Real Zaragoza | Sassuolo | Fortuna Düsseldorf
- team_short_name: POD | TWE | LUZ

Table: Team_Attributes
Columns:
- id: the unique id for teams
- team_fifa_api_id: the id of the team fifa api
- team_api_id: the id of the team api
- date: Date
- buildUpPlaySpeed: the speed in which attacks are put together
- buildUpPlaySpeedClass: the speed class
- buildUpPlayDribbling: the tendency/ frequency of dribbling
- buildUpPlayDribblingClass: the dribbling class
- buildUpPlayPassing: affects passing distance and support from teammates
- buildUpPlayPassingClass: the passing class
- buildUpPlayPositioningClass: A team's freedom of movement in the 1st two thirds of the pitch
- chanceCreationPassing: Amount of risk in pass decision and run support
- chanceCreationPassingClass: the chance creation passing class
- chanceCreationCrossing: The tendency / frequency of crosses into the box
- chanceCreationCrossingClass: the chance creation crossing class
- chanceCreationShooting: The tendency / frequency of shots taken
- chanceCreationShootingClass: the chance creation shooting class
- chanceCreationPositioningClass: A teams freedom of movement in the final third of the pitch
- defencePressure: Affects how high up the pitch the team will start pressuring
- defencePressureClass: the defence pressure class
- defenceAggression: Affect the teams approach to tackling the ball possessor
- defenceAggressionClass: the defence aggression class
- defenceTeamWidth: Affects how much the team will shift to the ball side
- defenceTeamWidthClass: the defence team width class
- defenceDefenderLineClass: Affects the shape and strategy of the defence
Example Values:
- date: 2012-02-22 00:00:00 | 2011-02-22 00:00:00 | 2013-09-20 00:00:00
- buildUpPlaySpeed: 24 | 80 | 43
- buildUpPlaySpeedClass: Fast | Balanced | Slow
- buildUpPlayDribbling: 51 | 56 | 57
- buildUpPlayDribblingClass: Normal | Little | Lots
- buildUpPlayPassing: 20 | 61 | 64
- buildUpPlayPassingClass: Short | Mixed | Long
- buildUpPlayPositioningClass: Organised | Free Form
- chanceCreationPassing: 50 | 59 | 71
- chanceCreationPassingClass: Safe | Risky | Normal
- chanceCreationCrossing: 47 | 32 | 41
- chanceCreationCrossingClass: Normal | Lots | Little
- chanceCreationShooting: 51 | 37 | 24
- chanceCreationShootingClass: Lots | Normal | Little
- chanceCreationPositioningClass: Free Form | Organised
- defencePressure: 52 | 25 | 33
- defencePressureClass: High | Medium | Deep
- defenceAggression: 63 | 64 | 65
- defenceAggressionClass: Contain | Double | Press
- defenceTeamWidth: 61 | 49 | 42
- defenceTeamWidthClass: Narrow | Wide | Normal
- defenceDefenderLineClass: Offside Trap | Cover

Table: account
Columns:
- account_id: the id of the account
- district_id: location of branch
- frequency: frequency of the acount
- date: the creation date of the account
Example Values:
- frequency: POPLATEK TYDNE | POPLATEK PO OBRATU | POPLATEK MESICNE
- date: 1997-08-02 | 1994-07-04 | 1996-06-08

Table: alignment
Columns:
- id: the unique identifier of the alignment
- alignment: the alignment of the superhero
Example Values:
- alignment: Bad | Neutral | N/A

Table: atom
Columns:
- atom_id: the unique id of atoms
- molecule_id: identifying the molecule to which the atom belongs
- element: the element of the toxicology
Example Values:
- element: i | pb | p

Table: attendance
Columns:
- link_to_event: The unique identifier of the event which was attended
- link_to_member: The unique identifier of the member who attended the event
Example Values:
- link_to_event: rec2N69DMcrqN9PJC | rec5XDvJLyxDsGZWc | recIuIXdbLe5j5vCA
- link_to_member: recP6DJPyi5donvXL | rec2a03QXbFQAUZ7X | recL94zpn6Xh6kQii

Table: attribute
Columns:
- id: the unique identifier of the attribute
- attribute_name: the attribute
Example Values:
- attribute_name: Power | Combat | Durability

Table: badges
Columns:
- Id: the badge id
- UserId: the unique id of the user
- Name: the badge name the user obtained
- Date: the date that the user obtained the badge
Example Values:
- Name: kolmogorov-smirnov | survival | normal-distribution
- Date: 2013-12-13 10:21:18 | 2013-08-09 21:18:26 | 2013-11-19 20:33:23

Table: bond
Columns:
- bond_id: unique id representing bonds
- molecule_id: identifying the molecule in which the bond appears
- bond_type: type of the bond
Example Values:
- bond_type: - | = | #

Table: budget
Columns:
- budget_id: A unique identifier for the budget entry
- category: The area for which the amount is budgeted, such as, advertisement, food, parking
- spent: The total amount spent in the budgeted category for an event.
- remaining: A value calculated as the amount budgeted minus the amount spent
- amount: The amount budgeted for the specified category and event
- event_status: the status of the event
- link_to_event: The unique identifier of the event to which the budget line applies.
Example Values:
- category: Club T-Shirts | Speaker Gifts | Advertisement
- spent: 74.59 | 174.25 | 122.33
- remaining: 20.0 | 0.75 | 10.0
- amount: 350 | 155 | 300
- event_status: Open | Planning | Closed
- link_to_event: rec180D2MI4EpckHy | recWJFyajeK4jCNYz | rec0Si5cQ4rJRVzd6

Table: card
Columns:
- card_id: id number of credit card
- disp_id: disposition id
- type: type of credit card
- issued: the date when the credit card issued
Example Values:
- type: junior | gold | classic
- issued: 1995-03-03 | 1998-10-05 | 1996-08-02

Table: cards
Columns:
- id
- artist: The name of the artist that illustrated the card art.
- asciiName: The ASCII(opens new window) (Basic/128) code formatted card name with no special unicode characters.
- availability: A list of the card's available printing types.
- borderColor: The color of the card border.
- cardKingdomFoilId: card Kingdom Foil Id
- cardKingdomId: card Kingdom Id
- colorIdentity: A list of all the colors found in manaCost, colorIndicator, and text
- colorIndicator: A list of all the colors in the color indicator (The symbol prefixed to a card's types).
- colors: A list of all the colors in manaCost and colorIndicator.
- convertedManaCost: The converted mana cost of the card. Use the manaValue property.
- duelDeck: The indicator for which duel deck the card is in.
- edhrecRank: The card rank on EDHRec
- faceConvertedManaCost: The converted mana cost or mana value for the face for either half or part of the card.
- faceName: The name on the face of the card.
- flavorName: The promotional card name printed above the true card name on special cards that has no game function.
- flavorText: The italicized text found below the rules text that has no game function.
- frameEffects: The visual frame effects.
- frameVersion: The version of the card frame style.
- hand: The starting maximum hand size total modifier.
- hasAlternativeDeckLimit: If the card allows a value other than 4 copies in a deck.
- hasContentWarning: If the card marked by Wizards of the Coast (opens new window) for having sensitive content. See this official article (opens new window) for more information.
- hasFoil: If the card can be found in foil
- hasNonFoil: If the card can be found in non-foil
- isAlternative: If the card is an alternate variation to an original printing
- isFullArt: If the card has full artwork.
- isOnlineOnly: If the card is only available in online game variations.
- isOversized: If the card is oversized.
- isPromo: If the card is a promotional printing.
- isReprint: If the card has been reprinted.
- isReserved: If the card is on the Magic: The Gathering Reserved List (opens new window)
- isStarter: If the card is found in a starter deck such as Planeswalker/Brawl decks.
- isStorySpotlight: If the card is a Story Spotlight card.
- isTextless: If the card does not have a text box.
- isTimeshifted: If the card is time shifted
- keywords: A list of keywords found on the card.
- layout: The type of card layout. For a token card, this will be "token"
- leadershipSkills: A list of formats the card is legal to be a commander in
- life: The starting life total modifier. A plus or minus character precedes an integer.
- loyalty: The starting loyalty value of the card.
- manaCost: The mana cost of the card wrapped in brackets for each value.
- mcmId
- mcmMetaId
- mtgArenaId
- mtgjsonV4Id
- mtgoFoilId
- mtgoId
- multiverseId
- name: The name of the card.
- number: The number of the card
- originalReleaseDate: original Release Date
- originalText: original Text
- originalType: original Type
- otherFaceIds: other Face Ids
- power: The power of the card.
- printings: A list of set printing codes the card was printed in, formatted in uppercase.
- promoTypes: A list of promotional types for a card.
- purchaseUrls: Links that navigate to websites where the card can be purchased.
- rarity: The card printing rarity.
- scryfallId
- scryfallIllustrationId
- scryfallOracleId
- setCode: The set printing code that the card is from.
- side: The identifier of the card side.
- subtypes: A list of card subtypes found after em-dash.
- supertypes: A list of card supertypes found before em-dash.
- tcgplayerProductId
- text: The rules text of the card.
- toughness: The toughness of the card.
- type: The type of the card as visible, including any supertypes and subtypes.
- types: A list of all card types of the card, including Un‑sets and gameplay variants.
- uuid: The universal unique identifier (v5) generated by MTGJSON. Each entry is unique.
- variations
- watermark: The name of the watermark on the card.
Example Values:
- artist: Chris Dien | Brian Durfee | Michael Bruinsma
- asciiName: Seance | Ghazban Ogre | Ifh-Biff Efreet
- availability: dreamcast | arena | mtgo,paper
- borderColor: white | gold | silver
- colorIdentity: B,G,U | B,R,U | R,U,W
- colorIndicator: W | B,G | U
- colors: W,G | R,U,W | G,U,W
- convertedManaCost: 0.0 | 8.0 | 1.0
- duelDeck: a | b
- edhrecRank: 16377 | 9379 | 15129
- faceConvertedManaCost: 7.0 | 4.0 | 1.0
- faceName: Haggle | Shatterskull Smashing | Nissa, Sage Animist
- flavorName: Destoroyah, Perfect Lifeform | Mechagodzilla, Battle Fortress | Biollante, Plant Beast Form
- flavorText: For the Phyrexians, death is not an end, nor a ... | "Xantcha is recovering. The medicine is slow, b... | Orcs are happiest under captains who steer towa...
- frameEffects: showcase,legendary | fullart | legendary,snow
- frameVersion: 1997 | 2003 | 1993
- hand: -3 | -1 | -2
- hasAlternativeDeckLimit: 1 | 0
- hasContentWarning: 0 | 1
- hasFoil: 1 | 0
- hasNonFoil: 1 | 0
- isAlternative: 0 | 1
- isFullArt: 0 | 1
- isOnlineOnly: 1 | 0
- isOversized: 0 | 1
- isPromo: 1 | 0
- isReprint: 0 | 1
- isReserved: 1 | 0
- isStarter: 1 | 0
- isStorySpotlight: 0 | 1
- isTextless: 1 | 0
- isTimeshifted: 0 | 1
- keywords: Afflict,Prowess | Double strike,Indestructible | Double strike,Transform
- layout: transform | normal | scheme
- leadershipSkills: {'brawl': False, 'commander': True, 'oathbreake... | {'brawl': False, 'commander': True, 'oathbreake... | {'brawl': True, 'commander': True, 'oathbreaker...
- life: 2 | 9 | -8
- loyalty: * | 3 | 7
- manaCost: {2}{B}{B} | {4}{G}{G}{G} | {2}{W/B}{W/B}
- name: Dracoplasm | Pyromancer's Swath | Death Bomb
- number: 49b | U7 | 1372
- originalReleaseDate: 2020/3/8 | 2015/8/22 | 2013/6/8
- originalText: All creatures able to block enchanted creature ... | The Fallen Apart comes into play with two arms ... | Destroy target nonblack creature if its toughne...
- originalType: Creature - Orc Shaman | Summon - Enchantress | Creature — Ape Spirit
- otherFaceIds: 90c4d598-dd83-566a-9138-2eb1e255ec8e | 5c445ea7-355b-5ce7-89b4-3f1de4a2fa2a | 1b18ca2b-4e5e-54c1-bf43-1f32afa75f78
- power: 7 | 9 | 2+*
- printings: PRM,PROE,ROE | 5ED,6ED,7ED,8ED,ICE | BFZ,C18,PBFZ,PRM
- promoTypes: duels | promostamped,promopack,planeswalkerstamped | setpromo,prerelease
- purchaseUrls: {'cardKingdom': 'https://mtgjson.com/links/5740... | {'cardKingdom': 'https://mtgjson.com/links/6650... | {'cardKingdom': 'https://mtgjson.com/links/7e37...
- rarity: rare | mythic | common
- setCode: SOI | PCY | JUD
- side: e | c | b
- subtypes: Vampire,Warrior | Illusion,Sliver | Golem,Construct
- supertypes: Legendary | Snow | Host
- text: Flying
Sacrifice Tin-Wing Chimera: Put a +2/+2 ... | If an artifact or creature entering the battlef... | Rally — Whenever Makindi Patrol or another Ally...
- toughness: 3 | 12 | *²
- type: Legendary Creature — Merfolk Artificer | Creature — Elf Druid Warrior | Legendary Creature — Orc Pirate
- types: Artifact,Creature | Summon | Summon,Goblin
- variations: e6c951be-84e3-504a-84ea-39f2c7dcd6e5 | 1ad33093-596e-5e3f-9518-8dc41d9e1547,9a0a1ac2-1... | 09194b12-11d3-5b89-b771-6b87d53a4e89,2426208d-e...
- watermark: goblinexplosioneers | set (M15) | set (P02)

Table: circuits
Columns:
- circuitId: unique identification number of the circuit
- circuitRef: circuit reference name
- name: full name of circuit
- location: location of circuit
- country: country of circuit
- lat: latitude of location of circuit
- lng: longitude of location of circuit
- alt
- url: url
Example Values:
- circuitRef: zolder | tremblant | watkins_glen
- name: Fuji Speedway | Yas Marina Circuit | Zeltweg
- location: Hockenheim | Spa | Pescara
- country: Turkey | Netherlands | Argentina
- lat: 47.5789 | 49.2542 | 33.937
- lng: -1.01694 | -76.9272 | 4.54092
- url: http://en.wikipedia.org/wiki/Adelaide_Street_Ci... | http://en.wikipedia.org/wiki/Hungaroring | http://en.wikipedia.org/wiki/Long_Beach,_Califo...

Table: client
Columns:
- client_id: the unique number
- gender
- birth_date: birth date
- district_id: location of branch
Example Values:
- gender: M | F
- birth_date: 1976-12-31 | 1968-01-30 | 1967-11-07

Table: colour
Columns:
- id: the unique identifier of the color
- colour: the color of the superhero's skin/eye/hair/etc
Example Values:
- colour: Red | Yellow/Red | Black

Table: comments
Columns:
- Id: the comment Id
- PostId: the unique id of the post
- Score: rating score
- Text: the detailed content of the comment
- CreationDate: the creation date of the comment
- UserId: the id of the user who post the comment
- UserDisplayName: user's display name
Example Values:
- Score: 6 | 10 | 29
- Text: In a univariate example perhaps, but if you hav... | A situation where a user wants a simple answer.... | Theorem 14.6, Sigma is singular so density isn'...
- CreationDate: 2011-11-12 21:04:22 | 2012-10-16 00:50:53 | 2011-10-28 02:58:16
- UserDisplayName: user20584 | user28 | user31660

Table: connected
Columns:
- atom_id: id of the first atom
- atom_id2: id of the second atom
- bond_id: bond id representing bond between two atoms
Example Values:
- atom_id2: TR181_17 | TR104_14 | TR153_15

Table: constructorResults
Columns:
- constructorResultsId: constructor Results Id
- raceId: race id
- constructorId: constructor id
- points: points
- status: status
Example Values:
- points: 24.0 | 16.0 | 5.0
- status: D

Table: constructorStandings
Columns:
- constructorStandingsId: unique identification of the constructor standing records
- raceId: id number identifying which races
- constructorId: id number identifying which id
- points: how many points acquired in each race
- position: position or track of circuits
- positionText
- wins: wins
Example Values:
- points: 5.0 | 574.0 | 365.0
- position: 9 | 8 | 12
- positionText: 14 | 11 | 8
- wins: 11 | 17 | 15

Table: constructors
Columns:
- constructorId: the unique identification number identifying constructors
- constructorRef: Constructor Reference name
- name: full name of the constructor
- nationality: nationality of the constructor
- url: the introduction website of the constructor
Example Values:
- constructorRef: zakspeed | moda | brabham
- name: Stevens | Turner | McLaren-Alfa Romeo
- nationality: Japanese | Russian | Hong Kong
- url: http://en.wikipedia.org/wiki/Team_Lotus | http://en.wikipedia.org/wiki/De_Tomaso | http://en.wikipedia.org/wiki/Porsche_in_Formula...

Table: customers
Columns:
- CustomerID: identification of the customer
- Segment: client segment
- Currency: Currency
Example Values:
- Segment: SME | LAM | KAM
- Currency: CZK | EUR

Table: disp
Columns:
- disp_id: unique number of identifying this row of record
- client_id: id number of client
- account_id: id number of account
- type: type of disposition
Example Values:
- type: OWNER | DISPONENT

Table: district
Columns:
- district_id: location of branch
- A2: district_name
- A3: region
- A4
- A5: municipality < district < region
- A6: municipality < district < region
- A7: municipality < district < region
- A8: municipality < district < region
- A9
- A10: ratio of urban inhabitants
- A11: average salary
- A12: unemployment rate 1995
- A13: unemployment rate 1996
- A14: no. of entrepreneurs per 1000 inhabitants
- A15: no. of committed crimes 1995
- A16: no. of committed crimes 1996
Example Values:
- A2: Znojmo | Ostrava - mesto | Decin
- A3: east Bohemia | north Moravia | south Moravia
- A4: 88884 | 78955 | 228848
- A5: 52 | 88 | 11
- A6: 17 | 29 | 25
- A7: 6 | 11 | 12
- A8: 4 | 2 | 3
- A9: 11 | 6 | 10
- A10: 76.3 | 67.0 | 56.9
- A11: 8843 | 8754 | 8254
- A12: 0.2 | 1.7 | 2.2
- A13: 1.25 | 1.86 | 6.55
- A14: 154 | 127 | 87
- A15: 1874 | 2879 | 1563
- A16: 1903 | 1460 | 2813

Table: driverStandings
Columns:
- driverStandingsId: the unique identification number identifying driver standing records
- raceId: id number identifying which races
- driverId: id number identifying which drivers
- points: how many points acquired in each race
- position: position or track of circuits
- positionText
- wins: wins
Example Values:
- points: 272.0 | 87.0 | 30.0
- position: 100 | 51 | 8
- positionText: 81 | 16 | 22
- wins: 7 | 0 | 3

Table: drivers
Columns:
- driverId: the unique identification number identifying each driver
- driverRef: driver reference name
- number: number
- code: abbreviated code for drivers
- forename: forename
- surname: surname
- dob: date of birth
- nationality: nationality of drivers
- url: the introduction website of the drivers
Example Values:
- driverRef: behra | moss | castellotti
- number: 9 | 36 | 55
- code: ALO | CHA | HUL
- forename: Raul | Bernie | Joachim
- surname: Branca | Levegh | Badoer
- dob: 1926-05-15 | 1937-12-02 | 1948-08-31
- nationality: American-Italian | Colombian | Thai
- url: http://en.wikipedia.org/wiki/Giulio_Cabianca | http://en.wikipedia.org/wiki/Corrado_Fabi | http://en.wikipedia.org/wiki/Ralf_Schumacher

Table: event
Columns:
- event_id: A unique identifier for the event
- event_name: event name
- event_date: The date the event took place or is scheduled to take place
- type: The kind of event, such as game, social, election
- notes: A free text field for any notes about the event
- location: Address where the event was held or is to be held or the name of such a location
- status: One of three values indicating if the event is in planning, is opened, or is closed
Example Values:
- event_name: September Meeting | October Meeting | November Meeting
- event_date: 2019-09-07T03:00:00 | 2020-03-24T12:00:00 | 2020-03-19T01:00:00
- type: Registration | Community Service | Social
- notes: Volunteer opportunity to help paint new home. | All active members can vote for new officers be... | Monthly officers meeting
- location: Campus Baseball Stadium | Campus Common | 900 E. Washington St.
- status: Planning | Closed | Open

Table: expense
Columns:
- expense_id: unique id of income
- expense_description: A textual description of what the money was spend for
- expense_date: The date the expense was incurred
- cost: The dollar amount of the expense
- approved: A true or false value indicating if the expense was approved
- link_to_member: The member who incurred the expense
- link_to_budget: The unique identifier of the record in the Budget table that indicates the expected total expenditure for a given category and event.
Example Values:
- expense_description: Parking | Travel Mug | Water, chips, cookies
- expense_date: 2019-10-22 | 2019-10-15 | 2019-11-14
- cost: 28.15 | 13.45 | 16.28
- approved: true
- link_to_member: rec4BLdZHS2Blfp4v | recro8T1MPMwRadVH | recD078PnS3x2doBe
- link_to_budget: recca5tkvdQgoLKZz | recZuCiQzCDAs4zDQ | recTUGXxhTaFZ2qkg

Table: foreign_data
Columns:
- id: unique id number identifying this row of data
- flavorText: The foreign flavor text of the card.
- language: The foreign language of card.
- multiverseid: The foreign multiverse identifier of the card.
- name: The foreign name of the card.
- text: The foreign text ruling of the card.
- type: The foreign type of the card. Includes any supertypes and subtypes.
- uuid
Example Values:
- flavorText: „Ajani reist dorthin, wo er am meisten gebrauch... | 狼人克星并不确知狼人是如何产生的。 所以他们见狼就杀，以防万一。 | 「永遠衆は人の顔を見分けられるが、私のことは青い色のミノタウルスにしか見えないはずだ。」
- language: Italian | Phyrexian | Arabic
- name: エーテル宣誓会の盾魔道士 | Дрейк из Глубинки | Aube de l'espoir
- text: Verursacht Trampelschaden
Immer wenn der Spross... | アーティファクト１つか土地１つを対象とし、それを追放する。構造のひずみはそのパーマネントのコン... | 緑の２/２の狼・クリーチャー・トークンを１体戦場に出す。
陰鬱 ― このターンにクリーチャーが...
- type: Créature : démon et ninja | 生物～鱼 | 生物～虚影／野兽

Table: frpm
Columns:
- CDSCode: CDSCode
- Academic Year: Academic Year
- County Code: County Code
- District Code: District Code
- School Code: School Code
- County Name: County Code
- District Name: District Name
- School Name: School Name
- District Type: District Type
- School Type: School Type
- Educational Option Type: Educational Option Type
- NSLP Provision Status: NSLP Provision Status
- Charter School (Y/N): Charter School (Y/N)
- Charter School Number: Charter School Number
- Charter Funding Type: Charter Funding Type
- IRC
- Low Grade: Low Grade
- High Grade: High Grade
- Enrollment (K-12): Enrollment (K-12)
- Free Meal Count (K-12): Free Meal Count (K-12)
- Percent (%) Eligible Free (K-12)
- FRPM Count (K-12): Free or Reduced Price Meal Count (K-12)
- Percent (%) Eligible FRPM (K-12)
- Enrollment (Ages 5-17): Enrollment (Ages 5-17)
- Free Meal Count (Ages 5-17): Free Meal Count (Ages 5-17)
- Percent (%) Eligible Free (Ages 5-17)
- FRPM Count (Ages 5-17)
- Percent (%) Eligible FRPM (Ages 5-17)
- 2013-14 CALPADS Fall 1 Certification Status: 2013-14 CALPADS Fall 1 Certification Status
Example Values:
- CDSCode: 40687006111058 | 56726036055685 | 19642126071351
- Academic Year: 2014-2015
- County Code: 16 | 03 | 25
- District Code: 61150 | 69583 | 76505
- School Code: 6030183 | 6001945 | 0105940
- County Name: Humboldt | Mariposa | Modoc
- District Name: Sundale Union Elementary | Ballard Elementary | Los Banos Unified
- School Name: Sun Valley Elementary | William Tell Aggeler Opportunity High | Meairs Elementary
- District Type: Elementary School District | Unified School District | Statewide Benefit Charter
- School Type: Alternative Schools of Choice | High Schools (Public) | Special Education Schools (Public)
- Educational Option Type: Youth Authority School | District Special Education Consortia School | Home and Hospital
- NSLP Provision Status: CEP | Provision 1 | Provision 3
- Charter School (Y/N): 0 | 1
- Charter School Number: 1503 | 1082 | 1488
- Charter Funding Type: Directly funded | Locally funded | Not in CS funding model
- IRC: 0 | 1
- Low Grade: 10 | 3 | 5
- High Grade: P | 12 | 2
- Enrollment (K-12): 735.0 | 1255.0 | 1045.0
- Free Meal Count (K-12): 263.0 | 620.0 | 845.0
- Percent (%) Eligible Free (K-12): 0.40546006066734 | 0.25955414012739 | 0.6046511627907
- FRPM Count (K-12): 162.0 | 1297.0 | 930.0
- Percent (%) Eligible FRPM (K-12): 0.81308411214953 | 0.57434514637904 | 0.5045045045045
- Enrollment (Ages 5-17): 1631.0 | 812.0 | 1427.0
- Free Meal Count (Ages 5-17): 785.0 | 873.0 | 239.0
- Percent (%) Eligible Free (Ages 5-17): 0.51508620689655 | 0.20769230769231 | 0.35551763367463
- FRPM Count (Ages 5-17): 160.0 | 687.0 | 707.0
- Percent (%) Eligible FRPM (Ages 5-17): 0.90322580645161 | 0.39655172413793 | 0.84334763948498
- 2013-14 CALPADS Fall 1 Certification Status: 1

Table: gasstations
Columns:
- GasStationID: Gas Station ID
- ChainID: Chain ID
- Country
- Segment: chain segment
Example Values:
- Country: CZE | SVK
- Segment: Discount | Premium | Noname

Table: gender
Columns:
- id: the unique identifier of the gender
- gender: the gender of the superhero
Example Values:
- gender: N/A | Female | Male

Table: hero_attribute
Columns:
- hero_id: the id of the hero
Maps to superhero(id)
- attribute_id: the id of the attribute
Maps to attribute(id)
- attribute_value: the attribute value
Example Values:
- attribute_value: 30 | 95 | 85

Table: hero_power
Columns:
- hero_id: the id of the hero
Maps to superhero(id)
- power_id: the id of the power
Maps to superpower(id)

Table: income
Columns:
- income_id: A unique identifier for each record of income
- date_received: the date that the fund received
- amount: amount of funds
- source: A value indicating where the funds come from such as dues, or the annual university allocation
- notes: A free-text value giving any needed details about the receipt of funds
- link_to_member: link to member
Example Values:
- date_received: 2019-10-17 | 2019-10-14 | 2019-09-25
- amount: 3000 | 1000 | 50
- source: Sponsorship | Fundraising | Dues
- notes: Ad revenue for use on flyers used to advertise ... | Annual funding from Student Government. | Secured donations to help pay for speaker gifts.
- link_to_member: recUdRhbhcEO1Hk5r | recL4aEZBZoPk9NYx | recf4UKTfipCzgcSA

Table: lapTimes
Columns:
- raceId: the identification number identifying race
- driverId: the identification number identifying each driver
- lap: lap number
- position: position or track of circuits
- time: lap time
- milliseconds: milliseconds
Example Values:
- lap: 47 | 16 | 40
- position: 14 | 10 | 5
- time: 1:46.931 | 1:55.897 | 1:47.403
- milliseconds: 71284 | 93764 | 124291

Table: legalities
Columns:
- id: unique id identifying this legality
- format: format of play
- status
- uuid
Example Values:
- format: future | penny | historic
- status: Banned | Restricted | Legal

Table: loan
Columns:
- loan_id: the id number identifying the loan data
- account_id: the id number identifying the account
- date: the date when the loan is approved
- amount: approved amount
- duration: loan duration
- payments: monthly payments
- status: repayment status
Example Values:
- date: 1995-08-01 | 1996-10-16 | 1996-04-18
- amount: 72408 | 135360 | 185544
- duration: 12 | 48 | 24
- payments: 621.0 | 7066.0 | 4192.0
- status: C | B | A

Table: major
Columns:
- major_id: A unique identifier for each major
- major_name: major name
- department: The name of the department that offers the major
- college: The name college that houses the department that offers the major
Example Values:
- major_name: Civil Engineering | Agricultural Education | Sociology
- department: Military Science Program | Journalism and Communication Department | Human Development and Family Studies Department
- college: College of Science | College of the Arts | College of Humanities and Social Sciences

Table: member
Columns:
- member_id: unique id of member
- first_name: member's first name
- last_name: member's last name
- email: member's email
- position: The position the member holds in the club
- t_shirt_size: The size of tee shirt that member wants when shirts are ordered
- phone: The best telephone at which to contact the member
- zip: the zip code of the member's hometown
- link_to_major: The unique identifier of the major of the member. References the Major table
Example Values:
- first_name: Dean | Keith | Sherri
- last_name: Balentine | Allen | Ing
- email: elijah.allen@lpu.edu | annabella.warren@lpu.edu | christof.nielson@lpu.edu
- position: Vice President | Inactive | Secretary
- t_shirt_size: Medium | Small | X-Large
- phone: 894-555-4529 | 727-555-2732 | 840-555-4781
- zip: 21801 | 84003 | 21784
- link_to_major: recuN6taqCVkaZMZS | recf3mPmWq4JXKf4L | recT9LoDnC8ZvdPqM

Table: molecule
Columns:
- molecule_id: unique id of molecule
- label: whether this molecule is carcinogenic or not
Example Values:
- label: + | -

Table: order
Columns:
- order_id: identifying the unique order
- account_id: id number of account
- bank_to: bank of the recipient
- account_to: account of the recipient
- amount: debited amount
- k_symbol: purpose of the payment
Example Values:
- bank_to: QR | EF | IJ
- account_to: 26565379 | 34219330 | 89044069
- amount: 1633.0 | 2592.0 | 1564.9
- k_symbol: SIPO |  | UVER

Table: pitStops
Columns:
- raceId: the identification number identifying race
- driverId: the identification number identifying each driver
- stop: stop number
- lap: lap number
- time: time
- duration: duration time
- milliseconds: milliseconds
Example Values:
- stop: 2 | 4 | 5
- lap: 43 | 6 | 63
- time: 14:36:50 | 20:46:40 | 14:41:05
- duration: 22.048 | 23.130 | 29.370
- milliseconds: 24837 | 22151 | 24269

Table: postHistory
Columns:
- Id: the post history id
- PostHistoryTypeId: the id of the post history type
- PostId: the unique id of the post
- RevisionGUID: the revision globally unique id of the post
- CreationDate: the creation date of the post
- UserId: the user who post the post
- Text: the detailed content of the post
- Comment: comments of the post
- UserDisplayName: user's display name
Example Values:
- CreationDate: 2014-01-16 13:43:26 | 2012-03-06 17:18:16 | 2012-11-21 02:47:13
- Text: You need to specify the purpose of the model be... | <python><dimensionality-reduction><discriminant... | I'm looking for advice/resources/recommendation...
- Comment: tidy up and make concise | added 43 characters in body; edited tags | http://twitter.com/#!/StackStats/status/2511544...
- UserDisplayName: Pierre 303 | Yotam | visnut

Table: postLinks
Columns:
- Id: the post link id
- CreationDate: the creation date of the post link
- PostId: the post id
- RelatedPostId: the id of the related post
- LinkTypeId: the id of the link type
Example Values:
- CreationDate: 2012-12-13 08:22:34 | 2011-05-22 14:21:45 | 2013-10-16 02:48:27

Table: posts
Columns:
- Id: the post id
- PostTypeId: the id of the post type
- AcceptedAnswerId: the accepted answer id of the post
- CreaionDate: the creation date of the post
- Score: the score of the post
- ViewCount: the view count of the post
- Body: the body of the post
- OwnerUserId: the id of the owner user
- LasActivityDate: the last activity date
- Title: the title of the post
- Tags: the tag of the post
- AnswerCount: the total number of answers of the post
- CommentCount: the total number of comments of the post
- FavoriteCount: the total number of favorites of the post
- LastEditorUserId: the id of the last editor
- LastEditDate: the last edit date
- CommunityOwnedDate: the community owned date
- ParentId: the id of the parent post
- ClosedDate: the closed date of the post
- OwnerDisplayName: the display name of the post owner
- LastEditorDisplayName: the display name of the last editor
Example Values:
- CreaionDate: 2010-11-08 16:13:13 | 2010-09-11 20:00:52 | 2010-08-06 05:27:57
- Score: 61 | 95 | 88
- ViewCount: 3257 | 2863 | 3937
- Body: <p>There is a set A having $N$ elements. Based ... | <p>I built a naivebayes model using the Housevo... | <p>I am reading Bishop's Pattern Recognition an...
- LasActivityDate: 2013-11-05 17:28:00 | 2012-06-08 12:28:31 | 2014-05-02 16:10:51
- Title: How to deal with features only available for a ... | Aggregating pooled regression outputs in differ... | What test should be used for detecting team imb...
- Tags: <time-series><bayesian><kalman-filter> | <hypothesis-testing><sampling><sample-size><pow... | <regression><time-series><logarithm>
- AnswerCount: 8 | 3 | 35
- CommentCount: 1 | 6 | 12
- FavoriteCount: 10 | 75 | 55
- LastEditDate: 2012-05-15 04:52:05 | 2011-07-13 14:00:10 | 2014-01-25 18:01:46
- CommunityOwnedDate: 2010-11-30 06:54:37 | 2013-10-11 01:37:35 | 2012-02-29 07:17:57
- ClosedDate: 2013-08-06 10:50:29 | 2013-04-19 03:00:55 | 2014-09-10 16:04:15
- OwnerDisplayName: pbx | Frederik Brinck Jensen | efrem
- LastEditorDisplayName: Sycren | user13261 | DBR

Table: products
Columns:
- ProductID: Product ID
- Description: Description
Example Values:
- Description: **Acquirer Transaction Fee** | Komunikacní poplatek | Kilometer accounting (VAT-free)

Table: publisher
Columns:
- id: the unique identifier of the publisher
- publisher_name: the name of the publisher
Example Values:
- publisher_name: Wildstorm | NBC - Heroes | Universal Studios

Table: qualifying
Columns:
- qualifyId: the unique identification number identifying qualifying
- raceId: the identification number identifying each race
- driverId: the identification number identifying each driver
- constructorId: constructor Id
- number: number
- position: position or track of circuit
- q1: time in qualifying 1
- q2: time in qualifying 2
- q3: time in qualifying 3
Example Values:
- number: 34 | 1 | 55
- position: 24 | 22 | 11
- q1: 1:21.810 | 1:27.555 | 1:15.070
- q2: 1:38.220 | 1:42.082 | 1:14.166
- q3: 1:36.543 | 1:24.021 | 1:28.037

Table: race
Columns:
- id: the unique identifier of the race
- race: the race of the superhero
Example Values:
- race: Spartoi | Inhuman | Asgardian

Table: races
Columns:
- raceId: the unique identification number identifying the race
- year: year
- round: round
- circuitId: circuit Id
- name: name of the race
- date: duration time
- time: time of the location
- url: introduction of races
Example Values:
- year: 1991 | 1982 | 1951
- round: 15 | 17 | 3
- name: Luxembourg Grand Prix | Swiss Grand Prix | Turkish Grand Prix
- date: 2014-03-30 | 2001-06-24 | 1992-05-31
- time: 17:00:00 | 11:30:00 | 08:00:00
- url: http://en.wikipedia.org/wiki/1974_Canadian_Gran... | http://en.wikipedia.org/wiki/1984_French_Grand_... | http://en.wikipedia.org/wiki/1971_Monaco_Grand_...

Table: results
Columns:
- resultId: the unique identification number identifying race result
- raceId: the identification number identifying the race
- driverId: the identification number identifying the driver
- constructorId: the identification number identifying which constructors
- number: number
- grid: the number identifying the area where cars are set into a grid formation in order to start the race.
- position: The finishing position or track of circuits
- positionText
- positionOrder: the finishing order of positions
- points: points
- laps: lap number
- time: finish time
- milliseconds: the actual finishing time of drivers in milliseconds
- fastestLap: fastest lap number
- rank: starting rank positioned by fastest lap speed
- fastestLapTime: fastest Lap Time
- fastestLapSpeed: fastest Lap Speed
- statusId: status ID
Example Values:
- number: 95 | 59 | 109
- position: 17 | 1 | 24
- positionText: N | 21 | 13
- positionOrder: 27 | 18 | 21
- points: 3.5 | 10.0 | 15.0
- laps: 109 | 107 | 56
- time: +24.285 | +41.108 | +1:33.257
- milliseconds: 10855900 | 5182748 | 5463305
- fastestLap: 71 | 67 | 32
- rank: 18 | 24 | 10
- fastestLapTime: 1:18.780 | 1:36.854 | 1:44.101
- fastestLapSpeed: 233.261 | 217.000 | 207.235

Table: rulings
Columns:
- id: unique id identifying this ruling
- date: date
- text: description about this ruling
- uuid
Example Values:
- date: 2019-08-23 | 2020-11-10 | 2016-11-08
- text: Suppression Bonds can enchant any nonland perma... | When Stoneforge Mystic’s second ability resolve... | If Nicol Bolas leaves the battlefield after his...

Table: satscores
Columns:
- cds: California Department Schools
- rtype: rtype
- sname: school name
- dname: district segment
- cname: county name
- enroll12: enrollment (1st-12nd grade)
- NumTstTakr: Number of Test Takers in this school
- AvgScrRead: average scores in Reading
- AvgScrMath: average scores in Math
- AvgScrWrite: average scores in writing
- NumGE1500: Number of Test Takers Whose Total SAT Scores Are Greater or Equal to 1500
Example Values:
- cds: 15638181535905 | 19647330122598 | 38684780119875
- rtype: D | S
- sname: Inderkum High | Alameda Science and Technology Institute | Highland Park Continuation
- dname: Santa Barbara Unified | La Canada Unified | Marin County Office of Education
- cname: Monterey | Siskiyou | Yolo
- enroll12: 721 | 728 | 312
- NumTstTakr: 1432 | 203 | 394
- AvgScrRead: 539 | 411 | 445
- AvgScrMath: 503 | 653 | 568
- AvgScrWrite: 579 | 560 | 468
- NumGE1500: 340 | 157 | 187

Table: schools
Columns:
- CDSCode: CDSCode
- NCESDist: This field represents the 7-digit National Center for Educational Statistics (NCES) school district identification number. The first 2 digits identify the state and the last 5 digits identify the school district. Combined, they make a unique 7-digit ID for each school district.
- NCESSchool: This field represents the 5-digit NCES school identification number. The NCESSchool combined with the NCESDist form a unique 12-digit ID for each school.
- StatusType: This field identifies the status of the district.
- County: County name
- District: District
- School: School
- Street: Street
- StreetAbr: The abbreviated street address of the school, district, or administrative authority’s physical location.
- City: City
- Zip: Zip
- State: State
- MailStreet: MailStreet
- MailStrAbr
- MailCity
- MailZip
- MailState
- Phone: Phone
- Ext: The phone number extension of the school, district, or administrative authority.
- Website: The website address of the school, district, or administrative authority.
- OpenDate: The date the school opened.
- ClosedDate: The date the school closed.
- Charter: This field identifies a charter school.
- CharterNum: The charter school number,
- FundingType: Indicates the charter school funding type
- DOC: District Ownership Code
- DOCType: The District Ownership Code Type is the text description of the DOC category.
- SOC: The School Ownership Code is a numeric code used to identify the type of school.
- SOCType: The School Ownership Code Type is the text description of the type of school.
- EdOpsCode: The Education Option Code is a short text description of the type of education offered.
- EdOpsName: Educational Option Name
- EILCode: The Educational Instruction Level Code is a short text description of the institution's type relative to the grade range served.
- EILName: The Educational Instruction Level Name is the long text description of the institution’s type relative to the grade range served.
- GSoffered: The grade span offered is the lowest grade and the highest grade offered or supported by the school, district, or administrative authority. This field might differ from the grade span served as reported in the most recent certified California Longitudinal Pupil Achievement (CALPADS) Fall 1 data collection.
- GSserved: It is the lowest grade and the highest grade of student enrollment as reported in the most recent certified CALPADS Fall 1 data collection. Only K–12 enrollment is reported through CALPADS. This field may differ from the grade span offered.
- Virtual: This field identifies the type of virtual instruction offered by the school. Virtual instruction is instruction in which students and teachers are separated by time and/or location, and interaction occurs via computers and/or telecommunications technologies.
- Magnet: This field identifies whether a school is a magnet school and/or provides a magnet program.
- Latitude: The angular distance (expressed in degrees) between the location of the school, district, or administrative authority and the equator measured north to south.
- Longitude: The angular distance (expressed in degrees) between the location of the school, district, or administrative authority and the prime meridian (Greenwich, England) measured from west to east.
- AdmFName1: administrator's first name
- AdmLName1: administrator's last name
- AdmEmail1: administrator's email address
- AdmFName2
- AdmLName2
- AdmEmail2
- AdmFName3
- AdmLName3
- AdmEmail3
- LastUpdate
Example Values:
- CDSCode: 37754160132472 | 33670906105837 | 19111976071880
- NCESDist: 0610260 | 0637320 | 0600044
- NCESSchool: 01346 | 02117 | 10602
- StatusType: Merged | Active | Closed
- County: Stanislaus | Trinity | Mendocino
- District: SBE - Long Valley Charter | SBE - Everest Public High | SBE - Prepa Tec Los Angeles High
- School: Hope Street Elementary | Anderson Middle | Dover Academy for International Studies
- Street: 1901 East Shields Avenue, Suite 169 | 49495 Road 427 | 1000 East Florinda Street
- StreetAbr: 411 Larchmont St. | 2410 Janna Ave. | 43900 Mayberry Ave.
- City: Clearlake | Groveland | Atherton
- Zip: 95624-3916 | 95482-4753 | 92201-3392
- State: CA
- MailStreet: 8693 Dearborn Avenue | 37720 Fremont Boulevard | 11900 Campus Drive
- MailStrAbr: 2802 Fourth St. | 300 Sill Rd. | 70 Skyview Terr.
- MailCity: San Bernardino | McFarland | Calexico
- MailZip: 92102-3132 | 95632-1720 | 95652-2439
- MailState: CA
- Phone: (707) 987-4140 | (619) 677-3017 | (650) 991-1252
- Ext: 630100 | 9100 | 236
- Website: http://schools.cvesd.org/schools/harborside/ | www.hesd.k12.ca.us/jfkjh/ | www.csdeagles.com
- OpenDate: 1997-11-01 | 2006-03-20 | 1997-07-28
- ClosedDate: 2001-07-30 | 2014-01-31 | 2013-09-27
- Charter: 1 | 0
- CharterNum: 0597 | 1552 | 1699
- FundingType: Locally funded | Directly funded | Not in CS funding model
- DOC: 52 | 58 | 31
- DOCType: State Board of Education | Administration Only | Statewide Benefit Charter
- SOC: 65 | 13 | 67
- SOCType: High Schools (Public) | Adult Education Centers | State Special Schools
- EdOpsCode: SPEC | ALTSOC | HOMHOS
- EdOpsName: District Special Education Consortia School | ROP | Special Education School
- EILCode: HS | ELEM | PS
- EILName: Elementary | High School | Adult
- GSoffered: 9-11 | 2-3 | 4
- GSserved: 1-10 | 3-12 | 2
- Virtual: P | N | F
- Magnet: 1 | 0
- Latitude: 34.132433 | 34.016239 | 33.599436
- Longitude: -121.47098 | -118.54741 | -117.92108
- AdmFName1: Veroncia | Brandi | Alma
- AdmLName1: Grandinetti | David | Mumper
- AdmEmail1: meltzer_helen@montebello.k12.ca.us | rachel.angel@pvusd.us | bdye@pbvusd.net
- AdmFName2: Julie | Danielle | Stephen
- AdmLName2: Dempsey | West | Avalos
- AdmEmail2: awright@suesd.org | tamara.ripke@dehesasd.net | sshadley@pierce.k12.ca.us
- AdmFName3: Eric | Gerardo | Mary
- AdmLName3: Rojas | Woodruff | Schmidt
- AdmEmail3: andrew.estrada@cvesd.org | tzerpoli@tricitiesrop.org | fournier.michelle@tusd.org
- LastUpdate: 2009-10-22 | 2015-10-09 | 2016-09-10

Table: seasons
Columns:
- year: the unique identification number identifying the race
- url: website link of season race introduction
Example Values:
- year: 1960 | 1982 | 1956
- url: http://en.wikipedia.org/wiki/1977_Formula_One_s... | http://en.wikipedia.org/wiki/2000_Formula_One_s... | http://en.wikipedia.org/wiki/2014_Formula_One_s...

Table: set_translations
Columns:
- id: unique id identifying this set
- language: language of this card
- setCode: the set code for this set
- translation: translation of this card
Example Values:
- language: Korean | Spanish | Japanese
- setCode: FRF | THB | C15
- translation: Mirrodin Sitiada | Перерожденная Алара | 鞑契可汗

Table: sets
Columns:
- id: unique id identifying this set
- baseSetSize: The number of cards in the set.
- block: The block name the set was in.
- booster: A breakdown of possibilities and weights of cards in a booster pack.
- code: The set code for the set.
- isFoilOnly: If the set is only available in foil.
- isForeignOnly: If the set is available only outside the United States of America.
- isNonFoilOnly: If the set is only available in non-foil.
- isOnlineOnly: If the set is only available in online game variations.
- isPartialPreview: If the set is still in preview (spoiled). Preview sets do not have complete data.
- keyruneCode: The matching Keyrune code for set image icons.
- mcmId: The Magic Card Marketset identifier.
- mcmIdExtras: The split Magic Card Market set identifier if a set is printed in two sets. This identifier represents the second set's identifier.
- mcmName
- mtgoCode: The set code for the set as it appears on Magic: The Gathering Online
- name: The name of the set.
- parentCode: The parent set code for set variations like promotions, guild kits, etc.
- releaseDate: The release date in ISO 8601 format for the set.
- tcgplayerGroupId: The group identifier of the set on TCGplayer
- totalSetSize: The total number of cards in the set, including promotional and related supplemental products but excluding Alchemy modifications - however those cards are included in the set itself.
- type: The expansion type of the set.
Example Values:
- baseSetSize: 259 | 133 | 230
- block: Tempest | Zendikar | Commander
- booster: {'default': {'boosters': [{'contents': {'common... | {'default': {'boosters': [{'contents': {'common... | {'default': {'boosters': [{'contents': {'blackA...
- code: PGPX | J19 | DDK
- isFoilOnly: 1 | 0
- isForeignOnly: 0 | 1
- isNonFoilOnly: 1 | 0
- isOnlineOnly: 1 | 0
- isPartialPreview: 1 | 0
- keyruneCode: S99 | PHUK | FUT
- mcmIdExtras: 2451 | 2419 | 2371
- mcmName: Grand Prix Promos | Commander 2015 | Dissension
- mtgoCode: WWK | OHOP | M20
- name: Mirrodin | Guildpact | Salvat 2011
- parentCode: ONS | CMD | C19
- releaseDate: 2015-04-03 | 2013-05-03 | 2017-06-09
- totalSetSize: 12 | 224 | 57
- type: archenemy | token | memorabilia

Table: status
Columns:
- statusId: the unique identification number identifying status
- status: full name of status
Example Values:
- status: +15 Laps | Broken wing | Axle

Table: superhero
Columns:
- id: the unique identifier of the superhero
- superhero_name: the name of the superhero
- full_name: the full name of the superhero
- gender_id: the id of the superhero's gender
- eye_colour_id: the id of the superhero's eye color
- hair_colour_id: the id of the superhero's hair color
- skin_colour_id: the id of the superhero's skin color
- race_id: the id of the superhero's race
- publisher_id: the id of the publisher
- alignment_id: the id of the superhero's alignment
- height_cm: the height of the superhero
- weight_kg: the weight of the superhero
Example Values:
- superhero_name: Darth Vader | Booster Gold | Spider-Woman II
- full_name: Diana of Themyscira | Peyton Westlake | Shirlee Bryant
- height_cm: 188 | 297 | 213
- weight_kg: 135 | 83 | 25

Table: superpower
Columns:
- id: the unique identifier of the superpower
- power_name: the superpower name
Example Values:
- power_name: Energy Beams | Sonar | Phoenix Force

Table: tags
Columns:
- Id: the tag id
- TagName: the name of the tag
- Count: the count of posts that contain this tag
- ExcerptPostId: the excerpt post id of the tag
- WikiPostId: the wiki post id of the tag
Example Values:
- TagName: moving-average | semiparametric | anosim
- Count: 126 | 448 | 165

Table: trans
Columns:
- trans_id: transaction id
- account_id
- date: date of transaction
- type: +/- transaction
- operation: mode of transaction
- amount: amount of money
- balance: balance after transaction
- k_symbol
- bank
- account
Example Values:
- date: 1995-10-13 | 1996-12-12 | 1993-03-19
- type: PRIJEM | VYBER | VYDAJ
- operation: VYBER | PREVOD Z UCTU | PREVOD NA UCET
- amount: 15270 | 25866 | 25488
- balance: 12401 | 14572 | 58440
- k_symbol: DUCHOD | SIPO | UVER
- bank: YZ | OP | AB
- account: 12887466 | 65384101 | 35182595

Table: transactions_1k
Columns:
- TransactionID: Transaction ID
- Date: Date
- Time: Time
- CustomerID: Customer ID
- CardID: Card ID
- GasStationID: Gas Station ID
- ProductID: Product ID
- Amount: Amount
- Price: Price
Example Values:
- Date: 2012-08-25 | 2012-08-26 | 2012-08-23
- Time: 06:01:00 | 13:36:00 | 10:17:00
- Amount: 73 | 61 | 19
- Price: 639.46 | 719.22 | 160.2

Table: users
Columns:
- Id: the user id
- Reputation: the user's reputation
- CreationDate: the creation date of the user account
- DisplayName: the user's display name
- LastAccessDate: the last access date of the user account
- WebsiteUrl: the website url of the user account
- Location: user's location
- AboutMe: the self introduction of the user
- Views: the number of views
- UpVotes: the number of upvotes
- DownVotes: the number of downvotes
- AccountId: the unique id of the account
- Age: user's age
- ProfileImageUrl: the profile image url
Example Values:
- Reputation: 1351 | 2182 | 592
- CreationDate: 2014-06-10 09:47:36 | 2012-01-04 22:17:48 | 2013-12-28 11:27:01
- DisplayName: mcduffee | mathStudent | Thomas Ingalls
- LastAccessDate: 2013-06-29 23:03:49 | 2014-09-13 14:48:02 | 2012-10-22 19:48:57
- WebsiteUrl: http://www.altosresearch.com/ | http://www.digitalquery.com | http://geryit.com
- Location: Korea | South Tyrol, Italy | Nomadic
- AboutMe: <p>I'm a database analyst for a credit union wo... | <p>Junior developer. Golang, Python, Erlang (in... | <p>The economy is in fact over-expanded, partic...
- Views: 257 | 155 | 73
- UpVotes: 201 | 213 | 23
- DownVotes: 82 | 39 | 1
- Age: 41 | 34 | 55
- ProfileImageUrl: https://www.gravatar.com/avatar/f3d69a8f8d4ed81... | https://www.gravatar.com/avatar/c8a8e0f5e962677... | https://www.gravatar.com/avatar/41f9d6eb2281814...

Table: votes
Columns:
- Id: the vote id
- PostId: the id of the post that is voted
- VoteTypeId: the id of the vote type
- CreationDate: the creation date of the vote
- UserId: the id of the voter
- BountyAmount: the amount of bounty
Example Values:
- CreationDate: 2010-08-05 | 2011-04-06 | 2010-09-02
- BountyAmount: 100 | 150 | 200

Table: yearmonth
Columns:
- CustomerID: Customer ID
- Date: Date
- Consumption: consumption
Example Values:
- Date: 201306 | 201205 | 201311
- Consumption: 27162.28 | 6811.27 | 4029.81

Table: zip_code
Columns:
- zip_code: The ZIP code itself. A five-digit number identifying a US post office.
- type: The kind of ZIP code
- city: The city to which the ZIP pertains
- county: The county to which the ZIP pertains
- state: The name of the state to which the ZIP pertains
- short_state: The abbreviation of the state to which the ZIP pertains
Example Values:
- zip_code: 24006 | 84132 | 20814
- type: Standard | PO Box | Unique
- city: Sound Beach | Hopedale | Black Earth
- county: Escambia County | Treasure County | Charles City County
- state: South Dakota | West Virginia | Georgia
- short_state: MT | IL | LA
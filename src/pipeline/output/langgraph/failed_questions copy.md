# 错误问题列表
总数: 234 个

## 按难度分组
| 难度 | 数量 |
|------|------|
| simple | 45 |
| moderate | 133 |
| challenging | 56 |

### CHALLENGING (56题)

#### ID:1481 | debit_card_specializing

**问题**: What is the difference in the annual average consumption of the customers with the least amount of consumption paid in CZK for 2013 between SME and LAM, LAM and KAM, and KAM and SME?

**证据**: annual average consumption of customer with the lowest consumption in each segment = total consumption per year / the number of customer with lowest consumption in each segment; Difference in annual average = SME's annual average - LAM's annual average; Difference in annual average = LAM's annual av...

**生成SQL**:
```sql
SELECT (SELECT annual_avg FROM (SELECT Segment, SUM(total_consumption)/COUNT(*) as annual_avg FROM (SELECT t.CustomerID, t.Segment, t.total_consumption FROM (SELECT c.CustomerID, c.Segment, SUM(y.Consumption) as total_consumption FROM customers c INNER JOIN yearmonth y ON c.CustomerID = y.CustomerID WHERE c.Currency = 'CZK' AND SUBSTRING(y.Date, 1, 4) = '2013' GROUP BY c.CustomerID, c.Segment) as t INNER JOIN (SELECT Segment, MIN(total_consumption) as min_consumption FROM (SELECT c.CustomerID, c.Segment, SUM(y.Consumption) as total_consumption FROM customers c INNER JOIN yearmonth y ON c.Custo
```

**生成结果**:
```json
[
  {
    "diff_SME_LAM": -14009.339999999998,
    "diff_LAM_KAM": 6046.619999999998,
    "diff_KAM_SME": 7962.72
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST(SUM(CASE WHEN `T1`.`Segment` = 'SME' THEN `T2`.`Consumption` ELSE 0 END) AS DOUBLE) / COUNT(`T1`.`CustomerID`) - CAST(SUM(CASE WHEN `T1`.`Segment` = 'LAM' THEN `T2`.`Consumption` ELSE 0 END) AS DOUBLE) / COUNT(`T1`.`CustomerID`),
  CAST(SUM(CASE WHEN `T1`.`Segment` = 'LAM' THEN `T2`.`Consumption` ELSE 0 END) AS DOUBLE) / COUNT(`T1`.`CustomerID`) - CAST(SUM(CASE WHEN `T1`.`Segment` = 'KAM' THEN `T2`.`Consumption` ELSE 0 END) AS DOUBLE) / COUNT(`T1`.`CustomerID`),
  CAST(SUM(CASE WHEN `T1`.`Segment` = 'KAM' THEN `T2`.`Consumption` ELSE 0 END) AS DOUBLE) / COUNT(`T1`.`CustomerID`) -
```

**预期结果**:
```json
[
  {
    "CAST(SUM(CASE WHEN `T1`.`Segment` = 'SME' THEN `T2`.`Consumption` ELSE 0 END) AS DOUBLE) / COUNT(`T1`.`CustomerID`) - CAST(SUM(CASE WHEN `T1`.`Segment` = 'LAM' THEN `T2`.`Consumption` ELSE 0 END) AS DOUBLE) / COUNT(`T1`.`CustomerID`)": 0.0,
    "CAST(SUM(CASE WHEN `T1`.`Segment` = 'LAM' THEN `T2`.`Consumption` ELSE 0 END) AS DOUBLE) / COUNT(`T1`.`CustomerID`) - CAST(SUM(CASE WHEN `T1`.`Segment` = 'KAM' THEN `T2`.`Consumption` ELSE 0 END) AS DOUBLE) / COUNT(`T1`.`CustomerID`)": 582092.86,
    "CAST(SUM(CASE WHEN `T1`.`Segment` = 'KAM' THEN `T2`.`Consumption` ELSE 0 END) AS DOUBLE) / COUNT(`T1`.`CustomerID`) - CAST(SUM(CASE WHEN `T1`.`Segment` = 'SME' THEN `T2`.`Consumption` ELSE 0 END) AS DOUBLE) / COUNT(`T1`.`CustomerID`)": -582092.86
  }
]
```
---

#### ID:1482 | debit_card_specializing

**问题**: Which of the three segments—SME, LAM and KAM—has the biggest and lowest percentage increases in consumption paid in EUR between 2012 and 2013?

**证据**: Increase or Decrease = consumption for 2013 - consumption for 2012; Percentage of Increase = (Increase or Decrease / consumption for 2012) * 100%; The first 4 strings of the Date values in the yearmonth table can represent year

**生成SQL**:
```sql
SELECT 
    Segment,
    PercentageIncrease,
    'Biggest' AS Type
FROM (
    SELECT 
        Segment,
        CAST( (SUM(CASE WHEN Year = '2013' THEN TotalConsumption ELSE 0 END) - 
               SUM(CASE WHEN Year = '2012' THEN TotalConsumption ELSE 0 END)) AS DOUBLE) / 
        CAST( SUM(CASE WHEN Year = '2012' THEN TotalConsumption ELSE 0 END) AS DOUBLE ) * 100 AS PercentageIncrease
    FROM (
        SELECT 
            c.Segment,
            SUBSTRING(y.Date, 1, 4) AS Year,
            SUM(y.Consumption) AS TotalConsumption
        FROM customers c
        INNER JOIN yearmonth y ON c.Cu
```

**生成结果**:
```
❌ 执行失败
```

**预期SQL**:
```sql
SELECT
  CAST((
    SUM(
      CASE
        WHEN `T1`.`Segment` = 'SME' AND `T2`.`Date` LIKE '2013%'
        THEN `T2`.`Consumption`
        ELSE 0
      END
    ) - SUM(
      CASE
        WHEN `T1`.`Segment` = 'SME' AND `T2`.`Date` LIKE '2012%'
        THEN `T2`.`Consumption`
        ELSE 0
      END
    )
  ) AS DOUBLE) * 100 / SUM(
    CASE
      WHEN `T1`.`Segment` = 'SME' AND `T2`.`Date` LIKE '2012%'
      THEN `T2`.`Consumption`
      ELSE 0
    END
  ),
  CAST(SUM(
    CASE
      WHEN `T1`.`Segment` = 'LAM' AND `T2`.`Date` LIKE '2013%'
      THEN `T2`.`Consumption`
      ELSE 0
    END
```

**预期结果**:
```json
[
  {
    "CAST((\n    SUM(\n      CASE\n        WHEN `T1`.`Segment` = 'SME' AND `T2`.`Date` LIKE '2013%'\n        THEN `T2`.`Consumption`\n        ELSE 0\n      END\n    ) - SUM(\n      CASE\n        WHEN `T1`.`Segment` = 'SME' AND `T2`.`Date` LIKE '2012%'\n        THEN `T2`": 545.4018999791232,
    "CAST(SUM(\n    CASE\n      WHEN `T1`.`Segment` = 'LAM' AND `T2`.`Date` LIKE '2013%'\n      THEN `T2`.`Consumption`\n      ELSE 0\n    END\n  ) - SUM(\n    CASE\n      WHEN `T1`.`Segment` = 'LAM' AND `T2`.`Date` LIKE '2012%'\n      THEN `T2`.`Consumption`\n      ELS": 681.5824574939396,
    "CAST(SUM(\n    CASE\n      WHEN `T1`.`Segment` = 'KAM' AND `T2`.`Date` LIKE '2013%'\n      THEN `T2`.`Consumption`\n      ELSE 0\n    END\n  ) - SUM(\n    CASE\n      WHEN `T1`.`Segment` = 'KAM' AND `T2`.`Date` LIKE '2012%'\n      THEN `T2`.`Consumption`\n      ELS": 708.1124062978652
  }
]
```
---

#### ID:1457 | student_club

**问题**: Give the full name and contact number of members who had to spend more than average on each expense.

**证据**: full name refers to first_name, last_name; contact number refers to phone; had spent more than average on each expense refers to cost > AVG(cost)

**生成SQL**:
```sql
SELECT m.first_name, m.last_name, m.phone FROM member m WHERE m.member_id IN (SELECT e.link_to_member FROM expense e GROUP BY e.link_to_member HAVING MIN(e.cost) > (SELECT AVG(cost) FROM expense))
```

**生成结果**:
(空结果)

**预期SQL**:
```sql
SELECT DISTINCT
  `T3`.`first_name`,
  `T3`.`last_name`,
  `T3`.`phone`
FROM `expense` AS `T1`
INNER JOIN `budget` AS `T2`
  ON `T1`.`link_to_budget` = `T2`.`budget_id`
INNER JOIN `member` AS `T3`
  ON `T3`.`member_id` = `T1`.`link_to_member`
WHERE
  `T1`.`cost` > (
    SELECT
      AVG(`T1`.`cost`)
    FROM `expense` AS `T1`
    INNER JOIN `budget` AS `T2`
      ON `T1`.`link_to_budget` = `T2`.`budget_id`
    INNER JOIN `member` AS `T3`
      ON `T3`.`member_id` = `T1`.`link_to_member`
  )
```

**预期结果**:
```json
[
  {
    "first_name": "Sacha",
    "last_name": "Harrison",
    "phone": "840-555-4781"
  },
  {
    "first_name": "Phillip",
    "last_name": "Cullen",
    "phone": "905-555-5035"
  },
  {
    "first_name": "Elijah",
    "last_name": "Allen",
    "phone": "724-555-5721"
  }
]
```
---

#### ID:1464 | student_club

**问题**: Write the full names of students who received funds on the date of 9/9/2019 and include the amount received.

**证据**: full name refers to first_name, last_name, amount of funds received refers to amount, received funds on date refers to date_received

**生成SQL**:
```sql
SELECT m.first_name, m.last_name, i.amount FROM income i INNER JOIN member m ON i.link_to_member = m.member_id WHERE i.date_received = '9/9/2019'
```

**生成结果**:
(空结果)

**预期SQL**:
```sql
SELECT DISTINCT
  `T3`.`first_name`,
  `T3`.`last_name`,
  `T4`.`amount`
FROM `event` AS `T1`
INNER JOIN `attendance` AS `T2`
  ON `T1`.`event_id` = `T2`.`link_to_event`
INNER JOIN `member` AS `T3`
  ON `T3`.`member_id` = `T2`.`link_to_member`
INNER JOIN `income` AS `T4`
  ON `T4`.`link_to_member` = `T3`.`member_id`
WHERE
  `T4`.`date_received` = '2019-09-09'
```

**预期结果**:
```json
[
  {
    "first_name": "Sacha",
    "last_name": "Harrison",
    "amount": 50
  },
  {
    "first_name": "Carlo",
    "last_name": "Jacobs",
    "amount": 50
  }
]
```
---

#### ID:1168 | thrombosis_prediction

**问题**: The oldest SJS patient's medical laboratory work was completed on what date, and what age was the patient when they initially arrived at the hospital?

**证据**: The larger the birthday value, the younger the person is, and vice versa; 'SJS' refers to diagnosis; (SUBTRACT(year(`First Date`)), year(Birthday)); age of the patients when they initially arrived at the hospital refers to year(Birthday)

**生成SQL**:
```sql
SELECT MAX(L.`Date`) AS Lab_Completion_Date, YEAR(P.`First Date`) - YEAR(P.Birthday) AS Age_At_Arrival FROM Patient P INNER JOIN Laboratory L ON P.ID = L.ID WHERE P.Diagnosis = 'SJS' GROUP BY P.ID, P.`First Date`, P.Birthday ORDER BY P.Birthday ASC LIMIT 1
```

**生成结果**:
```json
[
  {
    "Lab_Completion_Date": "1986-01-07",
    "Age_At_Arrival": 69
  }
]
```
**预期SQL**:
```sql
SELECT
  `T1`.`Date`,
  DATE_FORMAT(CAST(`T2`.`First Date` AS DATETIME), '%Y') - DATE_FORMAT(CAST(`T2`.`Birthday` AS DATETIME), '%Y'),
  `T2`.`Birthday`
FROM `Laboratory` AS `T1`
INNER JOIN `Patient` AS `T2`
  ON `T1`.`ID` = `T2`.`ID`
WHERE
  `T2`.`Diagnosis` = 'SJS' AND NOT `T2`.`Birthday` IS NULL
ORDER BY
  `T2`.`Birthday` ASC
LIMIT 1
```

**预期结果**:
```json
[
  {
    "Date": "1981-07-31",
    "DATE_FORMAT(CAST(`T2`.`First Date` AS DATETIME), '%Y') - DATE_FORMAT(CAST(`T2`.`Birthday` AS DATETIME), '%Y')": 69.0,
    "Birthday": "1917-04-18"
  }
]
```
---

#### ID:1169 | thrombosis_prediction

**问题**: What is the ratio of male to female patients among all those with abnormal uric acid counts?

**证据**: male refers to SEX = 'M'; female refers to SEX = 'F'; abnormal uric acid refers to UA < = '8.0' where SEX = 'M', UA < = '6.5' where SEX = 'F'; calculation = DIVIDE(SUM(UA <= '8.0' and SEX = 'M'), SUM(UA <= '6.5 and SEX = 'F'))

**生成SQL**:
```sql
SELECT CAST(COUNT(DISTINCT CASE WHEN P.SEX = 'M' AND L.UA <= 8.0 THEN P.ID END) AS DOUBLE) / COUNT(DISTINCT CASE WHEN P.SEX = 'F' AND L.UA <= 6.5 THEN P.ID END) AS ratio FROM Laboratory L INNER JOIN Patient P ON L.ID = P.ID WHERE (P.SEX = 'M' AND L.UA <= 8.0) OR (P.SEX = 'F' AND L.UA <= 6.5)
```

**生成结果**:
```json
[
  {
    "ratio": 0.184
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST(SUM(CASE WHEN `T2`.`UA` <= 8.0 AND `T1`.`SEX` = 'M' THEN 1 ELSE 0 END) AS DOUBLE) / SUM(CASE WHEN `T2`.`UA` <= 6.5 AND `T1`.`SEX` = 'F' THEN 1 ELSE 0 END)
FROM `Patient` AS `T1`
INNER JOIN `Laboratory` AS `T2`
  ON `T1`.`ID` = `T2`.`ID`
```

**预期结果**:
```json
[
  {
    "CAST(SUM(CASE WHEN `T2`.`UA` <= 8.0 AND `T1`.`SEX` = 'M' THEN 1 ELSE 0 END) AS DOUBLE) / SUM(CASE WHEN `T2`.`UA` <= 6.5 AND `T1`.`SEX` = 'F' THEN 1 ELSE 0 END)": 0.20566810835419985
  }
]
```
---

#### ID:1192 | thrombosis_prediction

**问题**: List all patients who were followed up at the outpatient clinic who underwent a laboratory test in October 1991 and had a total blood bilirubin level within the normal range.

**证据**: followed up at the outpatient clinic refers to Admission = '-'; laboratory test in April 1981 refers to Date like '1991-10%'; blood bilirubin level within the normal range refers to T-BIL < 2.0; 

**生成SQL**:
```sql
SELECT DISTINCT Patient.ID FROM Patient INNER JOIN Laboratory ON Patient.ID = Laboratory.ID WHERE Patient.Admission = '-' AND Laboratory.Date LIKE '1991-10%' AND Laboratory.T-BIL < 2.0
```

**生成结果**:
```
❌ 执行失败
```

**预期SQL**:
```sql
SELECT DISTINCT
  `T1`.`ID`
FROM `Patient` AS `T1`
INNER JOIN `Laboratory` AS `T2`
  ON `T1`.`ID` = `T2`.`ID`
WHERE
  `T1`.`Admission` = '-' AND `T2`.`T-BIL` < 2.0 AND `T2`.`Date` LIKE '1991-10-%'
```

**预期结果**:
```json
[
  {
    "ID": 304157
  },
  {
    "ID": 4466840
  },
  {
    "ID": 4471732
  },
  {
    "ID": 4630092
  },
  {
    "ID": 4632519
  }
]
```
---

#### ID:1241 | thrombosis_prediction

**问题**: For patients with abnormal platelet level, state the number of patients with lower than normal range. How is it compare to the number of patients with higher than normal range?

**证据**: abnormal platelet level refers to PLT <= 100 or PLT >= 400; platelet level lower than normal range refers to PLT < 100; calculation = SUBTRACT(SUM(PLT < 100), SUM(PLT > 400)); platelet level higher than normal range refers to PLT > 400;

**生成SQL**:
```sql
SELECT (SELECT COUNT(DISTINCT ID) FROM Laboratory WHERE PLT < 100) AS LowerCount, (SELECT COUNT(DISTINCT ID) FROM Laboratory WHERE PLT > 400) AS HigherCount, (SELECT COUNT(DISTINCT ID) FROM Laboratory WHERE PLT < 100) - (SELECT COUNT(DISTINCT ID) FROM Laboratory WHERE PLT > 400) AS Difference;
```

**生成结果**:
```json
[
  {
    "LowerCount": 36,
    "HigherCount": 82,
    "Difference": -46
  }
]
```
**预期SQL**:
```sql
SELECT
  SUM(CASE WHEN `T2`.`PLT` <= 100 THEN 1 ELSE 0 END) - SUM(CASE WHEN `T2`.`PLT` >= 400 THEN 1 ELSE 0 END)
FROM `Patient` AS `T1`
INNER JOIN `Laboratory` AS `T2`
  ON `T1`.`ID` = `T2`.`ID`
```

**预期结果**:
```json
[
  {
    "SUM(CASE WHEN `T2`.`PLT` <= 100 THEN 1 ELSE 0 END) - SUM(CASE WHEN `T2`.`PLT` >= 400 THEN 1 ELSE 0 END)": -562.0
  }
]
```
---

#### ID:1242 | thrombosis_prediction

**问题**: For laboratory examinations take in 1984, list all patients below 50 years old with normal platelet level.

**证据**: laboratory examinations take in 1984 refers to YEAR(Date) = '1984'; below 50 years old = SUBTRACT(year(current_timestamp), year(Birthday)) < 50; normal platelet level refers to PLT between 100 and 400; 

**生成SQL**:
```sql
SELECT DISTINCT Patient.ID FROM Laboratory INNER JOIN Patient ON Laboratory.ID = Patient.ID WHERE YEAR(Laboratory.Date) = 1984 AND (YEAR(CURDATE()) - YEAR(Patient.Birthday)) < 50 AND Laboratory.PLT BETWEEN 100 AND 400
```

**生成结果**:
```json
[
  {
    "ID": 102490
  },
  {
    "ID": 460574
  },
  {
    "ID": 1086485
  },
  {
    "ID": 2047892
  },
  {
    "ID": 3173679
  }
]
```
**预期SQL**:
```sql
SELECT DISTINCT
  `T1`.`ID`
FROM `Patient` AS `T1`
INNER JOIN `Laboratory` AS `T2`
  ON `T1`.`ID` = `T2`.`ID`
WHERE
  `T2`.`PLT` BETWEEN 100 AND 400
  AND DATE_FORMAT(CAST(`T2`.`Date` AS DATETIME), '%Y') - DATE_FORMAT(CAST(`T1`.`Birthday` AS DATETIME), '%Y') < 50
  AND DATE_FORMAT(CAST(`T2`.`Date` AS DATETIME), '%Y') = '1984'
```

**预期结果**:
```json
[
  {
    "ID": 30609
  },
  {
    "ID": 48473
  },
  {
    "ID": 52199
  },
  {
    "ID": 58139
  },
  {
    "ID": 81043
  }
]
```
---

#### ID:1243 | thrombosis_prediction

**问题**: For all patients who are older than 55 years old, what is the percentage of female who has abnormal prothrombin time (PT)?

**证据**: older than 55 years old = SUBTRACT(year(current_timestamp), year(Birthday)) > 55; abnormal prothrombin time (PT) refers to PT > = 14; percentage = DIVIDE(SUM(PT > = 14 AND SEX = 'F'), SUM(PT > = 14)) * 100; female refers to sex = 'F'; 

**生成SQL**:
```sql
SELECT (COUNT(DISTINCT CASE WHEN Laboratory.PT >= 14 AND Patient.SEX = 'F' THEN Patient.ID END) / COUNT(DISTINCT CASE WHEN Laboratory.PT >= 14 THEN Patient.ID END)) * 100 AS percentage FROM Patient INNER JOIN Laboratory ON Patient.ID = Laboratory.ID WHERE YEAR(CURDATE()) - YEAR(Birthday) > 55
```

**生成结果**:
```json
[
  {
    "percentage": 72.7273
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST(SUM(CASE WHEN `T2`.`PT` >= 14 AND `T1`.`SEX` = 'F' THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(CASE WHEN `T2`.`PT` >= 14 THEN 1 ELSE 0 END)
FROM `Patient` AS `T1`
INNER JOIN `Laboratory` AS `T2`
  ON `T1`.`ID` = `T2`.`ID`
WHERE
  DATE_FORMAT(CAST(CURRENT_TIMESTAMP() AS DATETIME), '%Y') - DATE_FORMAT(CAST(`T1`.`Birthday` AS DATETIME), '%Y') > 55
```

**预期结果**:
```json
[
  {
    "CAST(SUM(CASE WHEN `T2`.`PT` >= 14 AND `T1`.`SEX` = 'F' THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(CASE WHEN `T2`.`PT` >= 14 THEN 1 ELSE 0 END)": 1.2030885257676422
  }
]
```
---

#### ID:1247 | thrombosis_prediction

**问题**: Among the male patients who have a normal level of white blood cells, how many of them have an abnormal fibrinogen level?

**证据**: male patients refers to Sex = 'M'; normal level of white blood cells refers to WBC > 3.5 and WBC <9.0; abnormal fibrinogen level refers to FG < = 150 or FG > = 450; Don't compute repetitive ones.

**生成SQL**:
```sql
SELECT COUNT(DISTINCT p.ID) FROM Patient p INNER JOIN Laboratory l ON p.ID = l.ID WHERE p.Sex = 'M' AND l.WBC > 3.5 AND l.WBC < 9.0 AND (l.FG <= 150 OR l.FG >= 450)
```

**生成结果**:
```json
[
  {
    "COUNT(DISTINCT p.ID)": 6
  }
]
```
**预期SQL**:
```sql
SELECT
  COUNT(DISTINCT `T1`.`ID`)
FROM `Patient` AS `T1`
INNER JOIN `Laboratory` AS `T2`
  ON `T1`.`ID` = `T2`.`ID`
WHERE
  `T2`.`FG` <= 150
  OR `T2`.`FG` >= 450
  AND `T2`.`WBC` > 3.5
  AND `T2`.`WBC` < 9.0
  AND `T1`.`SEX` = 'M'
```

**预期结果**:
```json
[
  {
    "COUNT(DISTINCT `T1`.`ID`)": 75
  }
]
```
---

#### ID:1302 | thrombosis_prediction

**问题**: For the patients with a normal range of creatinine phosphokinase, how many of them have a positive measure of degree of coagulation?

**证据**: normal range of creatinine phosphokinase refers to CPK < 250; positive measure of degree of coagulation refers to KCT = '+' or RVVT = '+' or LAC = '+' ;

**生成SQL**:
```sql
SELECT COUNT(DISTINCT p.ID) FROM Patient p WHERE EXISTS (SELECT 1 FROM Laboratory l WHERE l.ID = p.ID AND l.CPK < 250) AND EXISTS (SELECT 1 FROM Examination e WHERE e.ID = p.ID AND (e.KCT = '+' OR e.RVVT = '+' OR e.LAC = '+'))
```

**生成结果**:
```json
[
  {
    "COUNT(DISTINCT p.ID)": 1
  }
]
```
**预期SQL**:
```sql
SELECT
  COUNT(`T1`.`ID`)
FROM `Patient` AS `T1`
INNER JOIN `Laboratory` AS `T2`
  ON `T1`.`ID` = `T2`.`ID`
INNER JOIN `Examination` AS `T3`
  ON `T1`.`ID` = `T3`.`ID`
WHERE
  `T2`.`CPK` < 250
  AND (
    `T3`.`KCT` = '+' OR `T3`.`RVVT` = '+' OR `T3`.`LAC` = '+'
  )
```

**预期结果**:
```json
[
  {
    "COUNT(`T1`.`ID`)": 7
  }
]
```
---

#### ID:1028 | european_football_2

**问题**: In Scotland Premier League, which away team won the most during the 2010 season?

**证据**: Final result should return the Team.team_long_name; Scotland Premier League refers to League.name = 'Scotland Premier League'; away team refers to away_team_api_id; away team that won the most refers to MAX(SUBTRACT(away_team_goal, home_team_goal) > 0); 2010 season refers to season = '2009/2010'; wo...

**生成SQL**:
```sql
SELECT T2.team_long_name FROM Team T2 WHERE T2.team_api_id = (SELECT away_team_api_id FROM Match T1 INNER JOIN League T3 ON T1.league_id = T3.id WHERE T3.name = 'Scotland Premier League' AND T1.season = '2009/2010' AND T1.away_team_goal > T1.home_team_goal GROUP BY away_team_api_id ORDER BY COUNT(*) DESC LIMIT 1)
```

**生成结果**:
```
❌ 执行失败
```

**预期SQL**:
```sql
SELECT
  `teamInfo`.`team_long_name`
FROM `League` AS `leagueData`
INNER JOIN `Match` AS `matchData`
  ON `leagueData`.`id` = `matchData`.`league_id`
INNER JOIN `Team` AS `teamInfo`
  ON `matchData`.`away_team_api_id` = `teamInfo`.`team_api_id`
WHERE
  `leagueData`.`name` = 'Scotland Premier League'
  AND `matchData`.`season` = '2009/2010'
  AND `matchData`.`away_team_goal` - `matchData`.`home_team_goal` > 0
GROUP BY
  `matchData`.`away_team_api_id`
ORDER BY
  COUNT(*) DESC
LIMIT 1
```

**预期结果**:
```json
[
  {
    "team_long_name": "Celtic"
  }
]
```
---

#### ID:1031 | european_football_2

**问题**: At present, calculate for the player's age who have a sprint speed of no less than 97 between 2013 to 2015.

**证据**: players age at present = SUBTRACT((DATETIME(), birthday)); sprint speed of no less than 97 refers to sprint_speed > = 97; between 2013 to 2015 refers to YEAR(date) > = '2013' AND YEAR(date) < = '2015'; 

**生成SQL**:
```sql
SELECT TIMESTAMPDIFF(YEAR, Player.birthday, CURDATE()) AS age FROM Player INNER JOIN Player_Attributes ON Player.player_api_id = Player_Attributes.player_api_id WHERE Player_Attributes.sprint_speed >= 97 AND YEAR(Player_Attributes.date) BETWEEN 2013 AND 2015
```

**生成结果**:
```json
[
  {
    "age": 35
  },
  {
    "age": 35
  },
  {
    "age": 35
  },
  {
    "age": 35
  },
  {
    "age": 35
  }
]
```
**预期SQL**:
```sql
SELECT DISTINCT YEAR(CURDATE()) - YEAR(t2.birthday) AS age FROM Player_Attributes AS t1 INNER JOIN Player AS t2 ON t1.player_api_id = t2.player_api_id WHERE YEAR(t1.`date`) BETWEEN 2013 AND 2015 AND t1.sprint_speed >= 97
```

**预期结果**:
```json
[
  {
    "age": 36
  }
]
```
---

#### ID:1037 | european_football_2

**问题**: Calculate the percentage of players who prefer left foot, who were born between 1987 and 1992.

**证据**: players who prefer left foot refers to preferred_foot = 'left'; percentage of players who prefer left foot = DIVIDE(MULTIPLY((SUM(preferred_foot = 'left'), 100)), COUNT(player_fifa_api_id)); born between 1987 and 1992 refers to YEAR(birthday) BETWEEN '1987' AND '1992';

**生成SQL**:
```sql
SELECT (CAST(COUNT(DISTINCT CASE WHEN pa.preferred_foot = 'left' THEN p.id END) AS DOUBLE) * 100) / COUNT(DISTINCT p.id) AS percentage FROM Player p INNER JOIN Player_Attributes pa ON p.player_fifa_api_id = pa.player_fifa_api_id WHERE YEAR(CAST(p.birthday AS DATE)) BETWEEN 1987 AND 1992
```

**生成结果**:
```json
[
  {
    "percentage": 28.868144690781797
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST(COUNT(CASE WHEN `t2`.`preferred_foot` = 'left' THEN `t1`.`id` ELSE NULL END) AS DOUBLE) * 100 / COUNT(`t1`.`id`) AS `percent`
FROM `Player` AS `t1`
INNER JOIN `Player_Attributes` AS `t2`
  ON `t1`.`player_api_id` = `t2`.`player_api_id`
WHERE
  SUBSTR(`t1`.`birthday`, 1, 4) BETWEEN '1987' AND '1992'
```

**预期结果**:
```json
[
  {
    "percent": 24.582259751524273
  }
]
```
---

#### ID:1042 | european_football_2

**问题**: List the name of leagues in which the average goals by the home team is higher than the away team in the 2009/2010 season.

**证据**: name of league refers to League.name; average goals by the home team is higher than the away team = AVG(home_team_goal) > AVG(away_team_goal); AVG(xx_goal) = SUM(xx_goal) / COUNT(DISTINCT Match.id); 2009/2010 season refers to season = '2009/2010'

**生成SQL**:
```sql
SELECT L.name FROM League L INNER JOIN Match M ON L.id = M.league_id WHERE M.season = '2009/2010' GROUP BY L.id, L.name HAVING AVG(M.home_team_goal) > AVG(M.away_team_goal)
```

**生成结果**:
```
❌ 执行失败
```

**预期SQL**:
```sql
SELECT
  `t1`.`name`
FROM `League` AS `t1`
INNER JOIN `Match` AS `t2`
  ON `t1`.`id` = `t2`.`league_id`
WHERE
  `t2`.`season` = '2009/2010'
GROUP BY
  `t1`.`name`
HAVING
  (
    CAST(SUM(`t2`.`home_team_goal`) AS DOUBLE) / COUNT(DISTINCT `t2`.`id`)
  ) - (
    CAST(SUM(`t2`.`away_team_goal`) AS DOUBLE) / COUNT(DISTINCT `t2`.`id`)
  ) > 0
```

**预期结果**:
```json
[
  {
    "name": "Belgium Jupiler League"
  },
  {
    "name": "England Premier League"
  },
  {
    "name": "France Ligue 1"
  },
  {
    "name": "Germany 1. Bundesliga"
  },
  {
    "name": "Italy Serie A"
  }
]
```
---

#### ID:1058 | european_football_2

**问题**: Who has the highest average finishing rate between the highest and shortest football player?

**证据**: finishing rate refers to finishing; highest average finishing rate = MAX(AVG(finishing)); highest football player refers to MAX(height); shortest football player refers to MIN(height);

**生成SQL**:
```sql
SELECT p.player_name FROM Player p JOIN Player_Attributes pa ON p.player_api_id = pa.player_api_id WHERE p.player_api_id IN (SELECT player_api_id FROM Player WHERE height = (SELECT MAX(height) FROM Player) UNION SELECT player_api_id FROM Player WHERE height = (SELECT MIN(height) FROM Player)) GROUP BY p.player_api_id, p.player_name ORDER BY AVG(pa.finishing) DESC LIMIT 1
```

**生成结果**:
```json
[
  {
    "player_name": "Juan Quero"
  }
]
```
**预期SQL**:
```sql
SELECT `A` FROM (SELECT AVG(`finishing`) AS `result`, 'Max' AS `A` FROM `Player` AS `T1` INNER JOIN `Player_Attributes` AS `T2` ON `T1`.`player_api_id` = `T2`.`player_api_id` WHERE `T1`.`height` = (SELECT MAX(`height`) FROM `Player`) UNION SELECT AVG(`finishing`) AS `result`, 'Min' AS `A` FROM `Player` AS `T1` INNER JOIN `Player_Attributes` AS `T2` ON `T1`.`player_api_id` = `T2`.`player_api_id` WHERE `T1`.`height` = (SELECT MIN(`height`) FROM `Player`)) AS `derived` ORDER BY `result` DESC LIMIT 1
```

**预期结果**:
```json
[
  {
    "A": "Min"
  }
]
```
---

#### ID:1094 | european_football_2

**问题**: How much higher in percentage is Ariel Borysiuk's overall rating than that of Paulin Puel?

**证据**: how much higher in percentage = MULTIPLY(DIVIDE(SUBTRACT(overall_rating WHERE player_name = 'Ariel Borysiuk', overall_rating WHERE player_name = 'Paulin Puel'), overall_rating WHERE player_name = 'Paulin Puel'), 100);

**生成SQL**:
```sql
SELECT CAST((ariel_rating - paulin_rating) AS DOUBLE) / CAST(paulin_rating AS DOUBLE) * 100 AS percentage_difference FROM ( SELECT (SELECT overall_rating FROM Player_Attributes WHERE player_api_id = (SELECT player_api_id FROM Player WHERE player_name = 'Ariel Borysiuk') ORDER BY date DESC LIMIT 1) as ariel_rating, (SELECT overall_rating FROM Player_Attributes WHERE player_api_id = (SELECT player_api_id FROM Player WHERE player_name = 'Paulin Puel') ORDER BY date DESC LIMIT 1) as paulin_rating ) as ratings
```

**生成结果**:
```json
[
  {
    "percentage_difference": 15.254237288135593
  }
]
```
**预期SQL**:
```sql
SELECT
  (
    SUM(
      CASE
        WHEN `t1`.`player_name` = 'Ariel Borysiuk'
        THEN `t2`.`overall_rating`
        ELSE 0
      END
    ) * 1.0 - SUM(
      CASE WHEN `t1`.`player_name` = 'Paulin Puel' THEN `t2`.`overall_rating` ELSE 0 END
    )
  ) * 100 / SUM(
    CASE WHEN `t1`.`player_name` = 'Paulin Puel' THEN `t2`.`overall_rating` ELSE 0 END
  )
FROM `Player` AS `t1`
INNER JOIN `Player_Attributes` AS `t2`
  ON `t1`.`player_api_id` = `t2`.`player_api_id`
```

**预期结果**:
```json
[
  {
    "(\n    SUM(\n      CASE\n        WHEN `t1`.`player_name` = 'Ariel Borysiuk'\n        THEN `t2`.`overall_rating`\n        ELSE 0\n      END\n    ) * 1.0 - SUM(\n      CASE WHEN `t1`.`player_name` = 'Paulin Puel' THEN `t2`.`overall_rating` ELSE 0 END\n    )\n  ) * 10": 133.72607
  }
]
```
---

#### ID:1115 | european_football_2

**问题**: What percentage is Landon Donovan's overall rating higher than Jordan Bowery on 2013/7/12?

**证据**: Landon Donovan's refers to player_name = 'Landon Donovan'; Jordan Bowery refers to player_name = 'Jordan Bowery'; percentage refers to DIVIDE(SUBTRACT(player_name = 'Landon Donovan' overall_rating; player_name = 'Jordan Bowery' overall_rating), player_name = 'Landon Donovan' overall_rating)*100

**生成SQL**:
```sql
SELECT (MAX(CASE WHEN p.player_name = 'Landon Donovan' THEN CAST(pa.overall_rating AS DOUBLE) END) - MAX(CASE WHEN p.player_name = 'Jordan Bowery' THEN CAST(pa.overall_rating AS DOUBLE) END)) / MAX(CASE WHEN p.player_name = 'Landon Donovan' THEN CAST(pa.overall_rating AS DOUBLE) END) * 100 AS percentage FROM Player_Attributes pa INNER JOIN Player p ON pa.player_api_id = p.player_api_id WHERE pa.date = '2013/7/12' AND p.player_name IN ('Landon Donovan', 'Jordan Bowery')
```

**生成结果**:
```json
[
  {
    "percentage": null
  }
]
```
**预期SQL**:
```sql
SELECT
  (
    SUM(
      CASE
        WHEN `t1`.`player_name` = 'Landon Donovan'
        THEN `t2`.`overall_rating`
        ELSE 0
      END
    ) * 1.0 - SUM(
      CASE WHEN `t1`.`player_name` = 'Jordan Bowery' THEN `t2`.`overall_rating` ELSE 0 END
    )
  ) * 100 / SUM(
    CASE
      WHEN `t1`.`player_name` = 'Landon Donovan'
      THEN `t2`.`overall_rating`
      ELSE 0
    END
  ) AS `LvsJ_percent`
FROM `Player` AS `t1`
INNER JOIN `Player_Attributes` AS `t2`
  ON `t1`.`player_fifa_api_id` = `t2`.`player_fifa_api_id`
WHERE
  SUBSTR(`t2`.`date`, 1, 10) = '2013-07-12'
```

**预期结果**:
```json
[
  {
    "LvsJ_percent": 25.31646
  }
]
```
---

#### ID:1139 | european_football_2

**问题**: What was the final score for the match on September 24, 2008, in the Belgian Jupiler League between the home team and the away team?

**证据**: September 24, 2008 refers to date like '2008-09-24%'; in the Belgian Jupiler League refers to League.name = 'Belgium Jupiler League'; final score for home team refers to home_team_goal; final score for away team refers to away_team_goal

**生成SQL**:
```sql
SELECT m.home_team_goal, m.away_team_goal FROM Match m INNER JOIN League l ON m.league_id = l.id WHERE l.name = 'Belgium Jupiler League' AND m.date LIKE '2008-09-24%'
```

**生成结果**:
```
❌ 执行失败
```

**预期SQL**:
```sql
SELECT
  `t2`.`home_team_goal`,
  `t2`.`away_team_goal`
FROM `League` AS `t1`
INNER JOIN `Match` AS `t2`
  ON `t1`.`id` = `t2`.`league_id`
WHERE
  `t1`.`name` = 'Belgium Jupiler League' AND `t2`.`date` LIKE '2008-09-24%'
```

**预期结果**:
```json
[
  {
    "home_team_goal": 1,
    "away_team_goal": 1
  }
]
```
---

#### ID:896 | formula_1

**问题**: Calculate the percentage whereby Hamilton was not at the 1st track of the the f1 circuit since 2010.

**证据**: percentage = DIVIDE(COUNT(raceId) where surname = 'Hamilton' and position>1), (COUNT(raceId) where surname = 'Hamilton'); since 2010 refers to year >= 2010

**生成SQL**:
```sql
SELECT CAST(SUM(CASE WHEN r.position > 1 THEN 1 ELSE 0 END) AS DOUBLE) / CAST(COUNT(DISTINCT r.raceId) AS DOUBLE) * 100 AS percentage FROM results r JOIN drivers d ON r.driverId = d.driverId JOIN races ra ON r.raceId = ra.raceId WHERE d.surname = 'Hamilton' AND ra.year >= 2010
```

**生成结果**:
```json
[
  {
    "percentage": 54.22535211267606
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST(COUNT(CASE WHEN `T2`.`position` <> 1 THEN `T2`.`position` END) AS DOUBLE) * 100 / COUNT(`T2`.`driverStandingsId`)
FROM `races` AS `T1`
INNER JOIN `driverStandings` AS `T2`
  ON `T2`.`raceId` = `T1`.`raceId`
INNER JOIN `drivers` AS `T3`
  ON `T3`.`driverId` = `T2`.`driverId`
WHERE
  `T3`.`surname` = 'Hamilton' AND `T1`.`year` >= 2010
```

**预期结果**:
```json
[
  {
    "CAST(COUNT(CASE WHEN `T2`.`position` <> 1 THEN `T2`.`position` END) AS DOUBLE) * 100 / COUNT(`T2`.`driverStandingsId`)": 73.2394366197183
  }
]
```
---

#### ID:944 | formula_1

**问题**: How much faster in percentage is the champion than the driver who finished the race last in the 2008 Australian Grand Prix?

**证据**: how much faster in percentage = divide(subtract(incremental time, champion time), last_driver time) * 100; last driver finished time = incremental time + champion time; only champion's finished time is represented by 'HH:MM:SS.mmm'; finished the game refers to time is not null

**生成SQL**:
```sql
SELECT CAST((last_time - champion_time) AS DOUBLE) / CAST(last_time AS DOUBLE) * 100 AS percentage_faster FROM (SELECT (SELECT milliseconds FROM results WHERE raceId = r.raceId AND positionOrder = 1 AND time IS NOT NULL) AS champion_time, (SELECT milliseconds FROM results WHERE raceId = r.raceId AND positionOrder = (SELECT MAX(positionOrder) FROM results WHERE raceId = r.raceId AND time IS NOT NULL) AND time IS NOT NULL) AS last_time FROM races r WHERE r.year = 2008 AND r.name = 'Australian Grand Prix' LIMIT 1) AS times
```

**生成结果**:
(空结果)

**预期SQL**:
```sql
WITH `time_in_seconds` AS (
  SELECT
    `T1`.`positionOrder`,
    CASE
      WHEN `T1`.`positionOrder` = 1
      THEN (
        CAST(SUBSTR(`T1`.`time`, 1, 1) AS DOUBLE) * 3600
      ) + (
        CAST(SUBSTR(`T1`.`time`, 3, 2) AS DOUBLE) * 60
      ) + CAST(SUBSTR(`T1`.`time`, 6) AS DOUBLE)
      ELSE CAST(SUBSTR(`T1`.`time`, 2) AS DOUBLE)
    END AS `time_seconds`
  FROM `results` AS `T1`
  INNER JOIN `races` AS `T2`
    ON `T1`.`raceId` = `T2`.`raceId`
  WHERE
    `T2`.`name` = 'Australian Grand Prix'
    AND NOT `T1`.`time` IS NULL
    AND `T2`.`year` = 2008
), `champion_time` AS (
  SELE
```

**预期结果**:
```json
[
  {
    "(\n    CAST((\n      SELECT\n        `time_seconds`\n      FROM `last_driver_incremental`\n    ) AS DOUBLE) * 100\n  ) / (\n    SELECT\n      `time_seconds` + (\n        SELECT\n          `time_seconds`\n        FROM `last_driver_incremental`\n      )\n    FROM `champ": null
  }
]
```
---

#### ID:962 | formula_1

**问题**: From 2000 to 2005, what percentage of drivers who were born before 1985 and the lap numbers were over 50?

**证据**: born before 1985 refers to year(dob)<1985; in 2000 to 2005 refers to year between 2000 and 2005; percentage = Divide(COUNT(driverId where year (dob) <1985 and laps >50),COUNT(DriverID where year between 2000 and 2005) *100;

**生成SQL**:
```sql
SELECT (CAST(COUNT(DISTINCT CASE WHEN YEAR(drivers.dob) < 1985 AND results.laps > 50 THEN results.driverId END) AS DOUBLE) * 100.0) / CAST(COUNT(DISTINCT results.driverId) AS DOUBLE) AS percentage FROM results INNER JOIN races ON results.raceId = races.raceId INNER JOIN drivers ON results.driverId = drivers.driverId WHERE races.year BETWEEN 2000 AND 2005
```

**生成结果**:
```json
[
  {
    "percentage": 100.0
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST(SUM(
    CASE
      WHEN DATE_FORMAT(CAST(`T3`.`dob` AS DATETIME), '%Y') < '1985' AND `T1`.`laps` > 50
      THEN 1
      ELSE 0
    END
  ) AS DOUBLE) * 100 / COUNT(*)
FROM `results` AS `T1`
INNER JOIN `races` AS `T2`
  ON `T1`.`raceId` = `T2`.`raceId`
INNER JOIN `drivers` AS `T3`
  ON `T1`.`driverId` = `T3`.`driverId`
WHERE
  `T2`.`year` BETWEEN 2000 AND 2005
```

**预期结果**:
```json
[
  {
    "CAST(SUM(\n    CASE\n      WHEN DATE_FORMAT(CAST(`T3`.`dob` AS DATETIME), '%Y') < '1985' AND `T1`.`laps` > 50\n      THEN 1\n      ELSE 0\n    END\n  ) AS DOUBLE) * 100 / COUNT(*)": 64.88474742520843
  }
]
```
---

#### ID:988 | formula_1

**问题**: List down top 3 German drivers who has the shortest average pit stop duration and were born between 1980-1985.

**证据**: Full name of the driver refers to drivers.forename and drivers.surname; born between 1980-1985 refers to 1980<= year(dob) <=1985; Average pitstop duration refers to Divide(SUM(duration),COUNT(duration)); shortest average refers to Min(avg(duration));

**生成SQL**:
```sql
SELECT drivers.forename, drivers.surname, AVG(pitStops.milliseconds) AS avg_pit_stop_duration FROM drivers INNER JOIN pitStops ON drivers.driverId = pitStops.driverId WHERE drivers.nationality = 'German' AND YEAR(drivers.dob) BETWEEN 1980 AND 1985 GROUP BY drivers.driverId, drivers.forename, drivers.surname ORDER BY avg_pit_stop_duration ASC LIMIT 3
```

**生成结果**:
```json
[
  {
    "forename": "Timo",
    "surname": "Glock",
    "avg_pit_stop_duration": 23689.3889
  },
  {
    "forename": "Adrian",
    "surname": "Sutil",
    "avg_pit_stop_duration": 35102.2155
  },
  {
    "forename": "Nico",
    "surname": "Rosberg",
    "avg_pit_stop_duration": 46321.9125
  }
]
```
**预期SQL**:
```sql
SELECT
  `T2`.`forename`,
  `T2`.`surname`
FROM `pitStops` AS `T1`
INNER JOIN `drivers` AS `T2`
  ON `T1`.`driverId` = `T2`.`driverId`
WHERE
  `T2`.`nationality` = 'German'
  AND DATE_FORMAT(CAST(`T2`.`dob` AS DATETIME), '%Y') BETWEEN '1980' AND '1985'
GROUP BY
  `T2`.`forename`,
  `T2`.`surname`
ORDER BY
  AVG(`T1`.`duration`)
LIMIT 3
```

**预期结果**:
```json
[
  {
    "forename": "Nico",
    "surname": "Rosberg"
  },
  {
    "forename": "Adrian",
    "surname": "Sutil"
  },
  {
    "forename": "Timo",
    "surname": "Glock"
  }
]
```
---

#### ID:1011 | formula_1

**问题**: Which top 20 driver created the shortest lap time ever record in a Formula_1 race? Please give them full names.

**证据**: shortest lap time refers to MIN(time); the time format for the shortest lap time is 'MM:SS.mmm' or 'M:SS.mmm'; full name of the driver refers to forename, surname

**生成SQL**:
```sql
SELECT d.forename, d.surname FROM (SELECT driverId, MIN(milliseconds) as min_milliseconds FROM lapTimes GROUP BY driverId ORDER BY min_milliseconds ASC LIMIT 20) AS lt INNER JOIN drivers d ON lt.driverId = d.driverId ORDER BY lt.min_milliseconds ASC
```

**生成结果**:
```json
[
  {
    "forename": "Lewis",
    "surname": "Hamilton"
  },
  {
    "forename": "Daniel",
    "surname": "Ricciardo"
  },
  {
    "forename": "Kimi",
    "surname": "Räikkönen"
  },
  {
    "forename": "Sebastian",
    "surname": "Vettel"
  },
  {
    "forename": "Valtteri",
    "surname": "Bottas"
  }
]
```
**预期SQL**:
```sql
WITH lap_times_in_seconds AS (SELECT driverId, (CASE WHEN SUBSTR(time, 1, INSTR(time, ':') - 1) <> '' THEN CAST(SUBSTR(time, 1, INSTR(time, ':') - 1) AS FLOAT) * 60 ELSE 0 END + CASE WHEN SUBSTR(time, INSTR(time, ':') + 1, INSTR(time, '.') - INSTR(time, ':') - 1) <> '' THEN CAST(SUBSTR(time, INSTR(time, ':') + 1, INSTR(time, '.') - INSTR(time, ':') - 1) AS FLOAT) ELSE 0 END + CASE WHEN SUBSTR(time, INSTR(time, '.') + 1) <> '' THEN CAST(SUBSTR(time, INSTR(time, '.') + 1) AS FLOAT) / 1000 ELSE 0 END) AS time_in_seconds FROM lapTimes) SELECT T2.forename, T2.surname, T1.driverId FROM (SELECT drive
```

**预期结果**:
```json
[
  {
    "forename": "Nico",
    "surname": "Hülkenberg",
    "driverId": 807
  },
  {
    "forename": "Daniel",
    "surname": "Ricciardo",
    "driverId": 817
  },
  {
    "forename": "Adrian",
    "surname": "Sutil",
    "driverId": 16
  },
  {
    "forename": "Kevin",
    "surname": "Magnussen",
    "driverId": 825
  },
  {
    "forename": "Nico",
    "surname": "Rosberg",
    "driverId": 3
  }
]
```
---

#### ID:1014 | formula_1

**问题**: Please list the lap records for the circuits in Italy.

**证据**: lap record means the fastest time recorded which refers to time

**生成SQL**:
```sql
SELECT circuits.name AS circuit_name, drivers.forename, drivers.surname, results.fastestLapTime AS lap_record FROM circuits INNER JOIN races ON circuits.circuitId = races.circuitId INNER JOIN results ON races.raceId = results.raceId INNER JOIN drivers ON results.driverId = drivers.driverId WHERE circuits.country = 'Italy' AND results.fastestLapTime IS NOT NULL ORDER BY circuits.name, results.fastestLapTime;
```

**生成结果**:
```json
[
  {
    "circuit_name": "Autodromo Enzo e Dino Ferrari",
    "forename": "Michael",
    "surname": "Schumacher",
    "lap_record": "1:20.411"
  },
  {
    "circuit_name": "Autodromo Enzo e Dino Ferrari",
    "forename": "Jenson",
    "surname": "Button",
    "lap_record": "1:21.201"
  },
  {
    "circuit_name": "Autodromo Enzo e Dino Ferrari",
    "forename": "Fernando",
    "surname": "Alonso",
    "lap_record": "1:21.650"
  },
  {
    "circuit_name": "Autodromo Enzo e Dino Ferrari",
    "forename": "Jarno",
    "surname": "Trulli",
    "lap_record": "1:21.666"
  },
  {
    "circuit_name": "Autodromo Enzo e Dino Ferrari",
    "forename": "Ralf",
    "surname": "Schumacher",
    "lap_record": "1:21.689"
  }
]
```
**预期SQL**:
```sql
WITH `fastest_lap_times` AS (
  SELECT
    `T1`.`raceId`,
    `T1`.`FastestLapTime`,
    (
      CAST(SUBSTR(`T1`.`FastestLapTime`, 1, INSTR(`T1`.`FastestLapTime`, ':') - 1) AS DOUBLE) * 60
    ) + (
      CAST(SUBSTR(
        `T1`.`FastestLapTime`,
        INSTR(`T1`.`FastestLapTime`, ':') + 1,
        INSTR(`T1`.`FastestLapTime`, '.') - INSTR(`T1`.`FastestLapTime`, ':') - 1
      ) AS DOUBLE)
    ) + (
      CAST(SUBSTR(`T1`.`FastestLapTime`, INSTR(`T1`.`FastestLapTime`, '.') + 1) AS DOUBLE) / 1000
    ) AS `time_in_seconds`
  FROM `results` AS `T1`
  WHERE
    NOT `T1`.`FastestLapTime` IS N
```

**预期结果**:
```json
[
  {
    "lap_record": "1:20.411"
  }
]
```
---

#### ID:730 | superhero

**问题**: List the superheroes from Marvel Comics who have the super power of 'Super Strength'.

**证据**: the superheroes from Marvel Comics refers to publisher_name = 'Marvel Comics'; super power of "Super Strength" refers to power_name = 'Super Strength';

**生成SQL**:
```sql
SELECT DISTINCT s.superhero_name FROM superhero s INNER JOIN publisher p ON s.publisher_id = p.id INNER JOIN hero_power hp ON s.id = hp.hero_id INNER JOIN superpower sp ON hp.power_id = sp.id WHERE p.publisher_name = 'Marvel Comics' AND sp.power_name = 'Super Strength';
```

**生成结果**:
```json
[
  {
    "superhero_name": "3-D Man"
  },
  {
    "superhero_name": "A-Bomb"
  },
  {
    "superhero_name": "Abomination"
  },
  {
    "superhero_name": "Abraxas"
  },
  {
    "superhero_name": "Absorbing Man"
  }
]
```
**预期SQL**:
```sql
SELECT
  `superhero_name`
FROM `superhero` AS `T1`
WHERE
  EXISTS(
    SELECT
      1
    FROM `hero_power` AS `T2`
    INNER JOIN `superpower` AS `T3`
      ON `T2`.`power_id` = `T3`.`id`
    WHERE
      `T3`.`power_name` = 'Super Strength' AND `T1`.`id` = `T2`.`hero_id`
  )
  AND EXISTS(
    SELECT
      1
    FROM `publisher` AS `T4`
    WHERE
      `T4`.`publisher_name` = 'Marvel Comics' AND `T1`.`publisher_id` = `T4`.`id`
  )
```

**预期结果**:
```json
[
  {
    "superhero_name": "3-D Man"
  },
  {
    "superhero_name": "A-Bomb"
  },
  {
    "superhero_name": "Abomination"
  },
  {
    "superhero_name": "Abraxas"
  },
  {
    "superhero_name": "Absorbing Man"
  }
]
```
---

#### ID:772 | superhero

**问题**: List the eyes, hair and skin colour of all female superheroes published by Dark Horse Comics.

**证据**: eyes refers to eye_colour_id; hair refers to hair_colour_id; skin colour refers to skin_colour_id; female superheroes refers to gender = 'Female'; published by Dark Horse Comics refers to publisher_name = 'Dark Horse Comics';

**生成SQL**:
```sql
SELECT colour_eye.colour AS eye_colour, colour_hair.colour AS hair_colour, colour_skin.colour AS skin_colour FROM superhero INNER JOIN gender ON superhero.gender_id = gender.id AND gender.gender = 'Female' INNER JOIN publisher ON superhero.publisher_id = publisher.id AND publisher.publisher_name = 'Dark Horse Comics' INNER JOIN colour AS colour_eye ON superhero.eye_colour_id = colour_eye.id INNER JOIN colour AS colour_hair ON superhero.hair_colour_id = colour_hair.id INNER JOIN colour AS colour_skin ON superhero.skin_colour_id = colour_skin.id
```

**生成结果**:
```json
[
  {
    "eye_colour": "Green",
    "hair_colour": "Blond",
    "skin_colour": "No Colour"
  },
  {
    "eye_colour": "Brown",
    "hair_colour": "Brown",
    "skin_colour": "No Colour"
  },
  {
    "eye_colour": "No Colour",
    "hair_colour": "No Colour",
    "skin_colour": "No Colour"
  },
  {
    "eye_colour": "No Colour",
    "hair_colour": "No Colour",
    "skin_colour": "Silver"
  },
  {
    "eye_colour": "Violet",
    "hair_colour": "Black",
    "skin_colour": "No Colour"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T1`.`eye_colour_id`,
  `T1`.`hair_colour_id`,
  `T1`.`skin_colour_id`
FROM `superhero` AS `T1`
INNER JOIN `publisher` AS `T2`
  ON `T2`.`id` = `T1`.`publisher_id`
INNER JOIN `gender` AS `T3`
  ON `T3`.`id` = `T1`.`gender_id`
WHERE
  `T2`.`publisher_name` = 'Dark Horse Comics' AND `T3`.`gender` = 'Female'
```

**预期结果**:
```json
[
  {
    "eye_colour_id": 14,
    "hair_colour_id": 6,
    "skin_colour_id": 1
  },
  {
    "eye_colour_id": 9,
    "hair_colour_id": 9,
    "skin_colour_id": 1
  },
  {
    "eye_colour_id": 1,
    "hair_colour_id": 1,
    "skin_colour_id": 1
  },
  {
    "eye_colour_id": 1,
    "hair_colour_id": 1,
    "skin_colour_id": 28
  },
  {
    "eye_colour_id": 30,
    "hair_colour_id": 4,
    "skin_colour_id": 1
  }
]
```
---

#### ID:586 | codebase_community

**问题**: Which user added a bounty amount of 50 to the post title mentioning variance?

**证据**: bounty amount of 50 refers to BountyAmount = 50; user refers to DisplayName; title mentioning variance refers to Title include 'variance'

**生成SQL**:
```sql
SELECT DISTINCT users.DisplayName FROM posts INNER JOIN votes ON posts.Id = votes.PostId INNER JOIN users ON votes.UserId = users.Id WHERE posts.Title LIKE '%variance%' AND votes.BountyAmount = 50
```

**生成结果**:
```json
[
  {
    "DisplayName": "chl"
  },
  {
    "DisplayName": "shabbychef"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T3`.`DisplayName`,
  `T1`.`Title`
FROM `posts` AS `T1`
INNER JOIN `votes` AS `T2`
  ON `T1`.`Id` = `T2`.`PostId`
INNER JOIN `users` AS `T3`
  ON `T3`.`Id` = `T2`.`UserId`
WHERE
  `T2`.`BountyAmount` = 50 AND `T1`.`Title` LIKE '%variance%'
```

**预期结果**:
```json
[
  {
    "DisplayName": "chl",
    "Title": "How to combine confidence intervals for a variance component of a mixed-effects model when using multiple imputation"
  },
  {
    "DisplayName": "shabbychef",
    "Title": "Unbiased estimation of covariance matrix for multiply censored data"
  }
]
```
---

#### ID:634 | codebase_community

**问题**: Among posts by Harvey Motulsky and Noah Snyder, which one has higher popularity?

**证据**: Has higher popularity means the post has higher view count ; calculation = MAX(SUM(ViewCount)) where DisplayName = 'Harvey Motulsky' OR DisplayName = 'Noah Snyder';

**生成SQL**:
```sql
SELECT OwnerDisplayName, SUM(ViewCount) as total_view_count FROM posts WHERE OwnerDisplayName IN ('Harvey Motulsky', 'Noah Snyder') GROUP BY OwnerDisplayName ORDER BY total_view_count DESC
```

**生成结果**:
(空结果)

**预期SQL**:
```sql
SELECT
  `T1`.`DisplayName`
FROM `users` AS `T1`
INNER JOIN `postHistory` AS `T2`
  ON `T1`.`Id` = `T2`.`UserId`
INNER JOIN `posts` AS `T3`
  ON `T2`.`PostId` = `T3`.`Id`
WHERE
  `T1`.`DisplayName` = 'Harvey Motulsky' OR `T1`.`DisplayName` = 'Noah Snyder'
GROUP BY
  `T1`.`DisplayName`
ORDER BY
  SUM(`T3`.`ViewCount`) DESC
LIMIT 1
```

**预期结果**:
```json
[
  {
    "DisplayName": "Harvey Motulsky"
  }
]
```
---

#### ID:639 | codebase_community

**问题**: Based on posts posted by Community, calculate the percentage of posts that use the R language.

**证据**: DIVIDE(COUNT(PostId WHERE TagName = 'r')), (COUNT(PostId WHERE DisplayName = 'Community')) as percentage; R language refers to tagname = 'r'

**生成SQL**:
```sql
SELECT (COUNT(CASE WHEN Tags REGEXP '<r>' THEN 1 END) * 100.0 / COUNT(*)) AS percentage FROM posts WHERE OwnerDisplayName = 'Community'
```

**生成结果**:
```json
[
  {
    "percentage": null
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST(SUM(CASE WHEN `T3`.`TagName` = 'r' THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(`T1`.`Id`)
FROM `users` AS `T1`
INNER JOIN `postHistory` AS `T2`
  ON `T1`.`Id` = `T2`.`UserId`
INNER JOIN `tags` AS `T3`
  ON `T3`.`ExcerptPostId` = `T2`.`PostId`
WHERE
  `T1`.`DisplayName` = 'Community'
```

**预期结果**:
```json
[
  {
    "CAST(SUM(CASE WHEN `T3`.`TagName` = 'r' THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(`T1`.`Id`)": 0.19607843137254902
  }
]
```
---

#### ID:371 | card_games

**问题**: What is the percentage of cards whose language is French among the Story Spotlight cards?

**证据**: Story Spotlight card refers to isStorySpotlight = 1; French is the language; Percentage = Divide(Count(id) where language = 'French' and isStorySpotlight = 1, Count(id) where isStorySpotlight = 1)*100

**生成SQL**:
```sql
SELECT CAST((SELECT COUNT(DISTINCT c.id) FROM cards c INNER JOIN foreign_data fd ON c.uuid = fd.uuid WHERE c.isStorySpotlight = 1 AND fd.language = 'French') AS DOUBLE) / CAST((SELECT COUNT(*) FROM cards WHERE isStorySpotlight = 1) AS DOUBLE) * 100 AS percentage
```

**生成结果**:
```json
[
  {
    "percentage": 83.65384615384616
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST(SUM(CASE WHEN `T2`.`language` = 'French' THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(`T1`.`id`)
FROM `cards` AS `T1`
INNER JOIN `foreign_data` AS `T2`
  ON `T1`.`uuid` = `T2`.`uuid`
WHERE
  `T1`.`isStorySpotlight` = 1
```

**预期结果**:
```json
[
  {
    "CAST(SUM(CASE WHEN `T2`.`language` = 'French' THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(`T1`.`id`)": 10.0
  }
]
```
---

#### ID:416 | card_games

**问题**: What percentage of cards without power are in French?

**证据**: in French refers to language = 'French'; cards without power refers to power IS NULL OR power = '*'; percentage = DIVIDE(COUNT(language = 'French' and power is NULL or power = '*'), COUNT( power is NULL or power = '*'))*100

**生成SQL**:
```sql
SELECT CAST((SELECT COUNT(DISTINCT c.uuid) FROM cards c INNER JOIN foreign_data f ON c.uuid = f.uuid WHERE (c.power IS NULL OR c.power = '*') AND f.language = 'French') AS DOUBLE) * 100 / NULLIF(CAST((SELECT COUNT(*) FROM cards WHERE power IS NULL OR power = '*') AS DOUBLE), 0) AS percentage
```

**生成结果**:
```json
[
  {
    "percentage": 47.95671915756932
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST(SUM(CASE WHEN `T2`.`language` = 'French' THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(`T1`.`id`)
FROM `cards` AS `T1`
INNER JOIN `foreign_data` AS `T2`
  ON `T1`.`uuid` = `T2`.`uuid`
WHERE
  `T1`.`power` IS NULL OR `T1`.`power` = '*'
```

**预期结果**:
```json
[
  {
    "CAST(SUM(CASE WHEN `T2`.`language` = 'French' THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(`T1`.`id`)": 12.975290140452374
  }
]
```
---

#### ID:198 | toxicology

**问题**: On average how many carcinogenic molecules are single bonded?

**证据**: carcinogenic molecules refers to label = '+'; single-bonded refers to bond_type = '-'; average = DIVIDE(SUM(bond_type = '-'), COUNT(atom_id))

**生成SQL**:
```sql
SELECT CAST((SELECT COUNT(*) FROM bond b INNER JOIN molecule m ON b.molecule_id = m.molecule_id WHERE m.label = '+' AND b.bond_type = '-') AS DOUBLE) / (SELECT COUNT(*) FROM atom a INNER JOIN molecule m ON a.molecule_id = m.molecule_id WHERE m.label = '+') AS average_value
```

**生成结果**:
```json
[
  {
    "average_value": 0.8336944745395449
  }
]
```
**预期SQL**:
```sql
SELECT
  AVG(`single_bond_count`)
FROM (
  SELECT
    `T3`.`molecule_id`,
    COUNT(`T1`.`bond_type`) AS `single_bond_count`
  FROM `bond` AS `T1`
  INNER JOIN `atom` AS `T2`
    ON `T1`.`molecule_id` = `T2`.`molecule_id`
  INNER JOIN `molecule` AS `T3`
    ON `T3`.`molecule_id` = `T2`.`molecule_id`
  WHERE
    `T1`.`bond_type` = '-' AND `T3`.`label` = '+'
  GROUP BY
    `T3`.`molecule_id`
) AS `subquery`
```

**预期结果**:
```json
[
  {
    "AVG(`single_bond_count`)": 732.125
  }
]
```
---

#### ID:206 | toxicology

**问题**: What elements are in the TR004_8_9 bond atoms?

**证据**: TR004_8_9 bond atoms refers to bond_id = 'TR004_8_9';

**生成SQL**:
```sql
SELECT a.element FROM (SELECT atom_id FROM connected WHERE bond_id = 'TR004_8_9' UNION ALL SELECT atom_id2 FROM connected WHERE bond_id = 'TR004_8_9') AS atoms INNER JOIN atom a ON atoms.atom_id = a.atom_id
```

**生成结果**:
```json
[
  {
    "element": "c"
  },
  {
    "element": "c"
  },
  {
    "element": "c"
  },
  {
    "element": "c"
  }
]
```
**预期SQL**:
```sql
SELECT DISTINCT
  `T1`.`element`
FROM `atom` AS `T1`
INNER JOIN `connected` AS `T2`
  ON `T1`.`atom_id` = `T2`.`atom_id`
WHERE
  `T2`.`bond_id` = 'TR004_8_9'
```

**预期结果**:
```json
[
  {
    "element": "c"
  }
]
```
---

#### ID:207 | toxicology

**问题**: What elements are in a double type bond?

**证据**: double type bond refers to bond_type = '=';

**生成SQL**:
```sql
SELECT a.element FROM bond b INNER JOIN connected c ON b.bond_id = c.bond_id INNER JOIN atom a ON c.atom_id = a.atom_id WHERE b.bond_type = '=' UNION SELECT a.element FROM bond b INNER JOIN connected c ON b.bond_id = c.bond_id INNER JOIN atom a ON c.atom_id2 = a.atom_id WHERE b.bond_type = '='
```

**生成结果**:
```json
[
  {
    "element": "c"
  },
  {
    "element": "o"
  },
  {
    "element": "n"
  },
  {
    "element": "s"
  },
  {
    "element": "ca"
  }
]
```
**预期SQL**:
```sql
SELECT DISTINCT
  `T1`.`element`
FROM `atom` AS `T1`
INNER JOIN `bond` AS `T2`
  ON `T1`.`molecule_id` = `T2`.`molecule_id`
INNER JOIN `connected` AS `T3`
  ON `T1`.`atom_id` = `T3`.`atom_id`
WHERE
  `T2`.`bond_type` = '='
```

**预期结果**:
```json
[
  {
    "element": "c"
  },
  {
    "element": "o"
  },
  {
    "element": "cl"
  },
  {
    "element": "h"
  },
  {
    "element": "s"
  }
]
```
---

#### ID:212 | toxicology

**问题**: Which element is the least numerous in non-carcinogenic molecules?

**证据**: label = '-' means molecules are non-carcinogenic; least numerous refers to MIN(COUNT(element));

**生成SQL**:
```sql
SELECT element FROM atom INNER JOIN molecule ON atom.molecule_id = molecule.molecule_id WHERE molecule.label = '-' GROUP BY element HAVING COUNT(*) = (SELECT MIN(cnt) FROM (SELECT COUNT(*) AS cnt FROM atom INNER JOIN molecule ON atom.molecule_id = molecule.molecule_id WHERE molecule.label = '-' GROUP BY element) AS sub)
```

**生成结果**:
```json
[
  {
    "element": "pb"
  },
  {
    "element": "ca"
  },
  {
    "element": "k"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T`.`element`
FROM (
  SELECT
    `T1`.`element`,
    COUNT(DISTINCT `T1`.`molecule_id`)
  FROM `atom` AS `T1`
  INNER JOIN `molecule` AS `T2`
    ON `T1`.`molecule_id` = `T2`.`molecule_id`
  WHERE
    `T2`.`label` = '-'
  GROUP BY
    `T1`.`element`
  ORDER BY
    COUNT(DISTINCT `T1`.`molecule_id`) ASC
  LIMIT 1
) AS `t`
```

**预期结果**:
```
❌ 执行失败
```

---

#### ID:215 | toxicology

**问题**: How many atoms with iodine and with sulfur type elements are there in single bond molecules?

**证据**: with iodine element refer to element = 'i'; with sulfur element refers to element = 's'; single type bond refers to bond_type = '-'; Should consider the distinct atoms when counting;

**生成SQL**:
```sql
SELECT COUNT(DISTINCT a.atom_id) FROM atom a INNER JOIN bond b ON a.molecule_id = b.molecule_id WHERE a.element IN ('i', 's') AND b.bond_type = '-'
```

**生成结果**:
```json
[
  {
    "COUNT(DISTINCT a.atom_id)": 97
  }
]
```
**预期SQL**:
```sql
SELECT
  COUNT(DISTINCT CASE WHEN `T1`.`element` = 'i' THEN `T1`.`atom_id` ELSE NULL END) AS `iodine_nums`,
  COUNT(DISTINCT CASE WHEN `T1`.`element` = 's' THEN `T1`.`atom_id` ELSE NULL END) AS `sulfur_nums`
FROM `atom` AS `T1`
INNER JOIN `connected` AS `T2`
  ON `T1`.`atom_id` = `T2`.`atom_id`
INNER JOIN `bond` AS `T3`
  ON `T2`.`bond_id` = `T3`.`bond_id`
WHERE
  `T3`.`bond_type` = '-'
```

**预期结果**:
```json
[
  {
    "iodine_nums": 3,
    "sulfur_nums": 77
  }
]
```
---

#### ID:218 | toxicology

**问题**: What percentage of carcinogenic-type molecules does not contain fluorine?

**证据**: label = '+' mean molecules are carcinogenic; contain fluorine refers to element = 'f'; percentage = DIVIDE(SUM(element = 'f') * 100, COUNT(molecule_id)) where label = '+'; Should consider the distinct atoms when counting;

**生成SQL**:
```sql
SELECT (CAST(SUM(CASE WHEN no_fluorine = 1 THEN 1 ELSE 0 END) AS DOUBLE) / CAST(COUNT(*) AS DOUBLE)) * 100 AS percentage FROM (SELECT m.molecule_id, CASE WHEN NOT EXISTS (SELECT 1 FROM atom a WHERE a.molecule_id = m.molecule_id AND a.element = 'f') THEN 1 ELSE 0 END AS no_fluorine FROM molecule m WHERE m.label = '+') AS subquery
```

**生成结果**:
```json
[
  {
    "percentage": 99.3421052631579
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST(COUNT(DISTINCT CASE WHEN `T1`.`element` <> 'f' THEN `T2`.`molecule_id` ELSE NULL END) AS DOUBLE) * 100 / COUNT(DISTINCT `T2`.`molecule_id`)
FROM `atom` AS `T1`
INNER JOIN `molecule` AS `T2`
  ON `T1`.`molecule_id` = `T2`.`molecule_id`
WHERE
  `T2`.`label` = '+'
```

**预期结果**:
```json
[
  {
    "CAST(COUNT(DISTINCT CASE WHEN `T1`.`element` <> 'f' THEN `T2`.`molecule_id` ELSE NULL END) AS DOUBLE) * 100 / COUNT(DISTINCT `T2`.`molecule_id`)": 100.0
  }
]
```
---

#### ID:219 | toxicology

**问题**: What is the percentage of carcinogenic molecules in triple type bonds?

**证据**: label = '+' mean molecules are carcinogenic; triple bond refers to bond_type = '#'; percentage = DIVIDE(SUM(bond_type = '#') * 100, COUNT(bond_id)) as percent where label = '+'

**生成SQL**:
```sql
SELECT CAST(SUM(CASE WHEN molecule.label = '+' THEN 1 ELSE 0 END) AS DOUBLE) * 100 / CAST(COUNT(*) AS DOUBLE) AS percentage FROM bond INNER JOIN molecule ON bond.molecule_id = molecule.molecule_id WHERE bond.bond_type = '#'
```

**生成结果**:
```json
[
  {
    "percentage": 60.0
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST(COUNT(DISTINCT CASE WHEN `T2`.`label` = '+' THEN `T2`.`molecule_id` ELSE NULL END) AS DOUBLE) * 100 / COUNT(DISTINCT `T2`.`molecule_id`)
FROM `atom` AS `T1`
INNER JOIN `molecule` AS `T2`
  ON `T1`.`molecule_id` = `T2`.`molecule_id`
INNER JOIN `bond` AS `T3`
  ON `T2`.`molecule_id` = `T3`.`molecule_id`
WHERE
  `T3`.`bond_type` = '#'
```

**预期结果**:
```json
[
  {
    "CAST(COUNT(DISTINCT CASE WHEN `T2`.`label` = '+' THEN `T2`.`molecule_id` ELSE NULL END) AS DOUBLE) * 100 / COUNT(DISTINCT `T2`.`molecule_id`)": 66.66666666666667
  }
]
```
---

#### ID:230 | toxicology

**问题**: What are the elements of the toxicology and label of molecule TR060?

**证据**: TR060 is the molecule id; 

**生成SQL**:
```sql
SELECT atom.element, molecule.label FROM atom INNER JOIN molecule ON atom.molecule_id = molecule.molecule_id WHERE molecule.molecule_id = 'TR060'
```

**生成结果**:
```json
[
  {
    "element": "c",
    "label": "-"
  },
  {
    "element": "c",
    "label": "-"
  },
  {
    "element": "h",
    "label": "-"
  },
  {
    "element": "h",
    "label": "-"
  },
  {
    "element": "h",
    "label": "-"
  }
]
```
**预期SQL**:
```sql
SELECT DISTINCT
  `T1`.`element`,
  `T2`.`label`
FROM `atom` AS `T1`
INNER JOIN `molecule` AS `T2`
  ON `T1`.`molecule_id` = `T2`.`molecule_id`
WHERE
  `T2`.`molecule_id` = 'TR060'
```

**预期结果**:
```json
[
  {
    "element": "c",
    "label": "-"
  },
  {
    "element": "h",
    "label": "-"
  },
  {
    "element": "o",
    "label": "-"
  },
  {
    "element": "n",
    "label": "-"
  },
  {
    "element": "cl",
    "label": "-"
  }
]
```
---

#### ID:231 | toxicology

**问题**: Which bond type accounted for the majority of the bonds found in molecule TR010 and state whether or not this molecule is carcinogenic?

**证据**: TR010 is the molecule id; majority of the bond found refers to MAX(COUNT(bond_type)); 

**生成SQL**:
```sql
SELECT b.bond_type, m.label FROM bond b INNER JOIN molecule m ON b.molecule_id = m.molecule_id WHERE b.molecule_id = 'TR010' AND b.bond_type = (SELECT bond_type FROM bond WHERE molecule_id = 'TR010' GROUP BY bond_type ORDER BY COUNT(*) DESC LIMIT 1) LIMIT 1;
```

**生成结果**:
```json
[
  {
    "bond_type": "-",
    "label": "-"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T`.`bond_type`
FROM (
  SELECT
    `T1`.`bond_type`,
    COUNT(`T1`.`molecule_id`)
  FROM `bond` AS `T1`
  WHERE
    `T1`.`molecule_id` = 'TR010'
  GROUP BY
    `T1`.`bond_type`
  ORDER BY
    COUNT(`T1`.`molecule_id`) DESC
  LIMIT 1
) AS `T`
```

**预期结果**:
```json
[
  {
    "bond_type": "-"
  }
]
```
---

#### ID:240 | toxicology

**问题**: List all the elements of the toxicology of the molecule "TR004".

**证据**: TR004 is the molecule id;

**生成SQL**:
```sql
SELECT element FROM atom WHERE molecule_id = 'TR004'
```

**生成结果**:
```json
[
  {
    "element": "s"
  },
  {
    "element": "n"
  },
  {
    "element": "o"
  },
  {
    "element": "c"
  },
  {
    "element": "h"
  }
]
```
**预期SQL**:
```sql
SELECT DISTINCT
  `T`.`element`
FROM `atom` AS `T`
WHERE
  `T`.`molecule_id` = 'TR004'
```

**预期结果**:
```json
[
  {
    "element": "s"
  },
  {
    "element": "n"
  },
  {
    "element": "o"
  },
  {
    "element": "c"
  },
  {
    "element": "h"
  }
]
```
---

#### ID:247 | toxicology

**问题**: List all the elements of atoms that can not bond with any other atoms.

**证据**:  atoms cannot bond with other atoms means atom_id NOT in connected table;

**生成SQL**:
```sql
SELECT element FROM atom WHERE NOT EXISTS (SELECT 1 FROM connected WHERE connected.atom_id = atom.atom_id OR connected.atom_id2 = atom.atom_id)
```

**生成结果**:
```
❌ 执行失败
```

**预期SQL**:
```sql
SELECT DISTINCT
  `T`.`element`
FROM `atom` AS `T`
WHERE
  NOT `T`.`element` IN (
    SELECT DISTINCT
      `T1`.`element`
    FROM `atom` AS `T1`
    INNER JOIN `connected` AS `T2`
      ON `T1`.`atom_id` = `T2`.`atom_id`
  )
```

**预期结果**:
```json
[
  {
    "element": "na"
  },
  {
    "element": "zn"
  },
  {
    "element": "k"
  }
]
```
---

#### ID:263 | toxicology

**问题**: What is the composition of element chlorine in percentage among the single bond molecules?

**证据**: element chlorine refers to element = 'cl'; single bond refers to bond_type = '-'; percentage = DIVIDE(SUM(element = 'cl'), COUNT(atom_id)) as percent where bond_type = '-'

**生成SQL**:
```sql
SELECT CAST(SUM(CASE WHEN a.element = 'cl' THEN 1 ELSE 0 END) AS DOUBLE) / CAST(COUNT(a.atom_id) AS DOUBLE) * 100 AS percentage FROM atom a INNER JOIN ( SELECT atom_id FROM connected WHERE bond_id IN (SELECT bond_id FROM bond WHERE bond_type = '-') UNION ALL SELECT atom_id2 FROM connected WHERE bond_id IN (SELECT bond_id FROM bond WHERE bond_type = '-') ) AS single_bond_atoms ON a.atom_id = single_bond_atoms.atom_id
```

**生成结果**:
```json
[
  {
    "percentage": 2.0276378664600285
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST(COUNT(CASE WHEN `T`.`element` = 'cl' THEN `T`.`atom_id` ELSE NULL END) AS DOUBLE) * 100 / COUNT(`T`.`atom_id`)
FROM (
  SELECT
    `T1`.`atom_id`,
    `T1`.`element`
  FROM `atom` AS `T1`
  INNER JOIN `molecule` AS `T2`
    ON `T1`.`molecule_id` = `T2`.`molecule_id`
  INNER JOIN `bond` AS `T3`
    ON `T2`.`molecule_id` = `T3`.`molecule_id`
  WHERE
    `T3`.`bond_type` = '-'
) AS `T`
```

**预期结果**:
```json
[
  {
    "CAST(COUNT(CASE WHEN `T`.`element` = 'cl' THEN `T`.`atom_id` ELSE NULL END) AS DOUBLE) * 100 / COUNT(`T`.`atom_id`)": 2.6840451814272206
  }
]
```
---

#### ID:281 | toxicology

**问题**: Tally the toxicology element of the 4th atom of each molecule that was carcinogenic.

**证据**: label = '+' means molecules are carcinogenic; 4th atom of each molecule refers to substr(atom_id, 7, 1) = '4'; 

**生成SQL**:
```sql
SELECT atom.element FROM atom INNER JOIN molecule ON atom.molecule_id = molecule.molecule_id WHERE molecule.label = '+' AND SUBSTRING(atom.atom_id, 7, 1) = '4'
```

**生成结果**:
```json
[
  {
    "element": "cl"
  },
  {
    "element": "c"
  },
  {
    "element": "c"
  },
  {
    "element": "h"
  },
  {
    "element": "h"
  }
]
```
**预期SQL**:
```sql
SELECT DISTINCT
  `T1`.`element`
FROM `atom` AS `T1`
INNER JOIN `molecule` AS `T2`
  ON `T1`.`molecule_id` = `T2`.`molecule_id`
WHERE
  `T2`.`label` = '+'
  AND SUBSTR(`T1`.`atom_id`, -1) = '4'
  AND LENGTH(`T1`.`atom_id`) = 7
```

**预期结果**:
```json
[
  {
    "element": "cl"
  },
  {
    "element": "c"
  },
  {
    "element": "br"
  },
  {
    "element": "n"
  },
  {
    "element": "o"
  }
]
```
---

#### ID:28 | california_schools

**问题**: Consider the average difference between K-12 enrollment and 15-17 enrollment of schools that are locally funded, list the names and DOC type of schools which has a difference above this average.

**证据**: Difference between K-12 enrollment and 15-17 enrollment can be computed by `Enrollment (K-12)` - `Enrollment (Ages 5-17)`

**生成SQL**:
```sql
SELECT s.School, s.DOCType FROM frpm f INNER JOIN schools s ON f.CDSCode = s.CDSCode WHERE s.Charter = 0 AND (f.`Enrollment (K-12)` - f.`Enrollment (Ages 5-17)`) > ( SELECT AVG(diff) FROM ( SELECT f2.`Enrollment (K-12)` - f2.`Enrollment (Ages 5-17)` AS diff FROM frpm f2 INNER JOIN schools s2 ON f2.CDSCode = s2.CDSCode WHERE s2.Charter = 0 ) AS t )
```

**生成结果**:
```json
[
  {
    "School": "Alameda County Juvenile Hall/Court",
    "DOCType": "County Office of Education (COE)"
  },
  {
    "School": "Alameda County Community",
    "DOCType": "County Office of Education (COE)"
  },
  {
    "School": "California School for the Blind",
    "DOCType": "State Special Schools"
  },
  {
    "School": "California School for the Deaf-Fremont",
    "DOCType": "State Special Schools"
  },
  {
    "School": "Alameda High",
    "DOCType": "Unified School District"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T2`.`School`,
  `T2`.`DOC`
FROM `frpm` AS `T1`
INNER JOIN `schools` AS `T2`
  ON `T1`.`CDSCode` = `T2`.`CDSCode`
WHERE
  `T2`.`FundingType` = 'Locally funded'
  AND (
    `T1`.`Enrollment (K-12)` - `T1`.`Enrollment (Ages 5-17)`
  ) > (
    SELECT
      AVG(`T3`.`Enrollment (K-12)` - `T3`.`Enrollment (Ages 5-17)`)
    FROM `frpm` AS `T3`
    INNER JOIN `schools` AS `T4`
      ON `T3`.`CDSCode` = `T4`.`CDSCode`
    WHERE
      `T4`.`FundingType` = 'Locally funded'
  )
```

**预期结果**:
```json
[
  {
    "School": "Mountain Oaks",
    "DOC": "00"
  },
  {
    "School": "Castle Rock",
    "DOC": "00"
  },
  {
    "School": "Charter Community School Home Study Academy",
    "DOC": "00"
  },
  {
    "School": "Clovis Online Charter",
    "DOC": "54"
  },
  {
    "School": "Washington Elementary",
    "DOC": "52"
  }
]
```
---

#### ID:36 | california_schools

**问题**: Under whose administration is the school with the highest number of students scoring 1500 or more on the SAT? Indicate their full names.

**证据**: full name means first name, last name; There are at most 3 administrators for each school; SAT Scores are greater or equal to 1500 refers to NumGE1500

**生成SQL**:
```sql
SELECT CONCAT_WS(', ', CASE WHEN s.AdmFName1 IS NOT NULL AND s.AdmLName1 IS NOT NULL THEN CONCAT(s.AdmFName1, ' ', s.AdmLName1) ELSE NULL END, CASE WHEN s.AdmFName2 IS NOT NULL AND s.AdmLName2 IS NOT NULL THEN CONCAT(s.AdmFName2, ' ', s.AdmLName2) ELSE NULL END, CASE WHEN s.AdmFName3 IS NOT NULL AND s.AdmLName3 IS NOT NULL THEN CONCAT(s.AdmFName3, ' ', s.AdmLName3) ELSE NULL END) AS admin_full_names FROM schools s INNER JOIN satscores sat ON s.CDSCode = sat.cds ORDER BY sat.NumGE1500 DESC LIMIT 1
```

**生成结果**:
```json
[
  {
    "admin_full_names": "Michelle King"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T2`.`AdmFName1`,
  `T2`.`AdmLName1`,
  `T2`.`AdmFName2`,
  `T2`.`AdmLName2`,
  `T2`.`AdmFName3`,
  `T2`.`AdmLName3`
FROM `satscores` AS `T1`
INNER JOIN `schools` AS `T2`
  ON `T1`.`cds` = `T2`.`CDSCode`
ORDER BY
  `T1`.`NumGE1500` DESC
LIMIT 1
```

**预期结果**:
```json
[
  {
    "AdmFName1": "Michelle",
    "AdmLName1": "King",
    "AdmFName2": null,
    "AdmLName2": null,
    "AdmFName3": null,
    "AdmLName3": null
  }
]
```
---

#### ID:62 | california_schools

**问题**: What is the total number of non-chartered schools in the county of Los Angeles with a percent (%) of eligible free meals for grades 1 through 12 that is less than 0.18%?

**证据**: non-chartered schools refer to schools whose Charter = 0; K-12 means grades 1 through 12; percent of eligible free rate for K-12 = `Free Meal Count (K-12)` * 100 / `Enrollment (K-12)`

**生成SQL**:
```sql
SELECT COUNT(*) FROM frpm WHERE `County Name` = 'Los Angeles' AND `Charter School (Y/N)` = 0 AND `Percent (%) Eligible Free (K-12)` < 0.18
```

**生成结果**:
```json
[
  {
    "COUNT(*)": 201
  }
]
```
**预期SQL**:
```sql
SELECT
  COUNT(`T2`.`School`)
FROM `frpm` AS `T1`
INNER JOIN `schools` AS `T2`
  ON `T1`.`CDSCode` = `T2`.`CDSCode`
WHERE
  `T2`.`County` = 'Los Angeles'
  AND `T2`.`Charter` = 0
  AND CAST(`T1`.`Free Meal Count (K-12)` AS DOUBLE) * 100 / `T1`.`Enrollment (K-12)` < 0.18
```

**预期结果**:
```json
[
  {
    "COUNT(`T2`.`School`)": 1
  }
]
```
---

#### ID:83 | california_schools

**问题**: Of the schools that offers a magnet program serving a grade span of Kindergarten to 8th grade, how many offers Multiple Provision Types? List the number of cities that offers a Kindergarten to 8th grade span and indicate how many schools are there serving such grade span for each city.

**证据**: Kindergarten to 8th grade refers to K-8; 'Offers a magnet program' means Magnet = 1; Multiple Provision Types refers to `NSLP Provision Status` = 'Multiple Provision Types'

**生成SQL**:
```sql
SELECT 'Multiple Provision Types Count' AS result_type, COUNT(*) AS value FROM schools s INNER JOIN frpm f ON s.CDSCode = f.CDSCode WHERE s.Magnet = 1 AND s.GSserved = 'K-8' AND f.`NSLP Provision Status` = 'Multiple Provision Types' UNION ALL SELECT City AS result_type, COUNT(*) AS value FROM schools WHERE Magnet = 1 AND GSserved = 'K-8' GROUP BY City
```

**生成结果**:
```json
[
  {
    "result_type": "Multiple Provision Types Count",
    "value": 1
  },
  {
    "result_type": "Fresno",
    "value": 2
  },
  {
    "result_type": "El Centro",
    "value": 1
  },
  {
    "result_type": "Bakersfield",
    "value": 1
  },
  {
    "result_type": "Marina Del Rey",
    "value": 1
  }
]
```
**预期SQL**:
```sql
SELECT
  `T2`.`City`,
  COUNT(`T2`.`CDSCode`)
FROM `frpm` AS `T1`
INNER JOIN `schools` AS `T2`
  ON `T1`.`CDSCode` = `T2`.`CDSCode`
WHERE
  `T2`.`Magnet` = 1
  AND `T2`.`GSoffered` = 'K-8'
  AND `T1`.`NSLP Provision Status` = 'Multiple Provision Types'
GROUP BY
  `T2`.`City`
```

**预期结果**:
```json
[
  {
    "City": "Adelanto",
    "COUNT(`T2`.`CDSCode`)": 1
  }
]
```
---

#### ID:87 | california_schools

**问题**: What are the valid e-mail addresses of the administrator of the school located in the San Bernardino county, City of San Bernardino City Unified that opened between 1/1/2009 to 12/31/2010 whose school types are public Intermediate/Middle Schools and Unified Schools?

**证据**: Intermediate/Middle Schools refers to SOC = 62; Unified School refers to DOC = 54; years between 2009 and 2010 can refer to 'between 1/1/2009 to 12/31/2010'

**生成SQL**:
```sql
SELECT GROUP_CONCAT(Email SEPARATOR ', ') AS ValidEmails FROM (SELECT AdmEmail1 AS Email FROM schools WHERE County = 'San Bernardino' AND District = 'San Bernardino City Unified' AND OpenDate BETWEEN '2009-01-01' AND '2010-12-31' AND SOC = 62 AND DOC = 54 AND AdmEmail1 IS NOT NULL AND AdmEmail1 != '' UNION ALL SELECT AdmEmail2 FROM schools WHERE County = 'San Bernardino' AND District = 'San Bernardino City Unified' AND OpenDate BETWEEN '2009-01-01' AND '2010-12-31' AND SOC = 62 AND DOC = 54 AND AdmEmail2 IS NOT NULL AND AdmEmail2 != '' UNION ALL SELECT AdmEmail3 FROM schools WHERE County = 'Sa
```

**生成结果**:
```json
[
  {
    "ValidEmails": "a.lucero@realjourney.org, j.hernandez@realjourney.org"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T2`.`AdmEmail1`,
  `T2`.`AdmEmail2`
FROM `frpm` AS `T1`
INNER JOIN `schools` AS `T2`
  ON `T1`.`CDSCode` = `T2`.`CDSCode`
WHERE
  `T2`.`County` = 'San Bernardino'
  AND `T2`.`City` = 'San Bernardino'
  AND `T2`.`DOC` = 54
  AND DATE_FORMAT(CAST(`T2`.`OpenDate` AS DATETIME), '%Y') BETWEEN '2009' AND '2010'
  AND `T2`.`SOC` = 62
```

**预期结果**:
```json
[
  {
    "AdmEmail1": "a.lucero@realjourney.org",
    "AdmEmail2": "j.hernandez@realjourney.org"
  }
]
```
---

#### ID:94 | financial

**问题**: List out the account numbers of female clients who are oldest and has lowest average salary, calculate the gap between this lowest average salary with the highest average salary?

**证据**: Female means gender = 'F'; A11 refers to average salary; Gap = highest average salary - lowest average salary; If the person A's birthdate > B's birthdate, it means that person B is order than person A.

**生成SQL**:
```sql
SELECT a.account_id, (SELECT MAX(A11) FROM district) - (SELECT MIN(d2.A11) FROM client c2 JOIN district d2 ON c2.district_id = d2.district_id WHERE c2.gender = 'F' AND c2.birth_date = (SELECT MIN(birth_date) FROM client WHERE gender = 'F')) as gap FROM account a JOIN disp ON a.account_id = disp.account_id JOIN client c ON disp.client_id = c.client_id JOIN district d ON c.district_id = d.district_id WHERE c.gender = 'F' AND c.birth_date = (SELECT MIN(birth_date) FROM client WHERE gender = 'F') AND d.A11 = (SELECT MIN(d2.A11) FROM client c2 JOIN district d2 ON c2.district_id = d2.district_id WHE
```

**生成结果**:
```json
[
  {
    "account_id": 1743,
    "gap": 4000
  }
]
```
**预期SQL**:
```sql
SELECT
  `T1`.`account_id`,
  (
    SELECT
      MAX(`A11`) - MIN(`A11`)
    FROM `district`
  )
FROM `account` AS `T1`
INNER JOIN `district` AS `T2`
  ON `T1`.`district_id` = `T2`.`district_id`
INNER JOIN `disp` AS `T3`
  ON `T1`.`account_id` = `T3`.`account_id`
INNER JOIN `client` AS `T4`
  ON `T3`.`client_id` = `T4`.`client_id`
WHERE
  `T2`.`district_id` = (
    SELECT
      `district_id`
    FROM `client`
    WHERE
      `gender` = 'F'
    ORDER BY
      `birth_date` ASC
    LIMIT 1
  )
ORDER BY
  `T2`.`A11` DESC
LIMIT 1
```

**预期结果**:
```json
[
  {
    "account_id": 6,
    "(\n    SELECT\n      MAX(`A11`) - MIN(`A11`)\n    FROM `district`\n  )": 4431
  }
]
```
---

#### ID:125 | financial

**问题**: For loans contracts which are still running where client are in debt, list the district of the and the state the percentage unemployment rate increment from year 1995 to 1996.

**证据**: Unemployment increment rate in percentage = [(unemployment rate 2016 - unemployment rate 2015) / unemployment rate 2015] * 100; unemployment rate 2015 appears in the A12; unemployment rate 2016 appears in the A13; Loan contracts which are still running where client are in debt can be presented as st...

**生成SQL**:
```sql
SELECT district.A2 AS district_name, ((district.A13 - district.A12) / district.A12) * 100 AS unemployment_increment_percentage FROM loan INNER JOIN account ON loan.account_id = account.account_id INNER JOIN district ON account.district_id = district.district_id WHERE loan.status = 'D'
```

**生成结果**:
```json
[
  {
    "district_name": "Strakonice",
    "unemployment_increment_percentage": 40.0
  },
  {
    "district_name": "Chrudim",
    "unemployment_increment_percentage": 39.259259259259245
  },
  {
    "district_name": "Hl.m. Praha",
    "unemployment_increment_percentage": 114.99999999999999
  },
  {
    "district_name": "Brno - mesto",
    "unemployment_increment_percentage": 22.499999999999993
  },
  {
    "district_name": "Mlada Boleslav",
    "unemployment_increment_percentage": 20.0
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST((
    `T3`.`A13` - `T3`.`A12`
  ) AS DOUBLE) * 100 / `T3`.`A12`
FROM `loan` AS `T1`
INNER JOIN `account` AS `T2`
  ON `T1`.`account_id` = `T2`.`account_id`
INNER JOIN `district` AS `T3`
  ON `T2`.`district_id` = `T3`.`district_id`
WHERE
  `T1`.`status` = 'D'
```

**预期结果**:
```json
[
  {
    "CAST((\n    `T3`.`A13` - `T3`.`A12`\n  ) AS DOUBLE) * 100 / `T3`.`A12`": 40.0
  },
  {
    "CAST((\n    `T3`.`A13` - `T3`.`A12`\n  ) AS DOUBLE) * 100 / `T3`.`A12`": 39.25925925925924
  },
  {
    "CAST((\n    `T3`.`A13` - `T3`.`A12`\n  ) AS DOUBLE) * 100 / `T3`.`A12`": 115.0
  },
  {
    "CAST((\n    `T3`.`A13` - `T3`.`A12`\n  ) AS DOUBLE) * 100 / `T3`.`A12`": 22.49999999999999
  },
  {
    "CAST((\n    `T3`.`A13` - `T3`.`A12`\n  ) AS DOUBLE) * 100 / `T3`.`A12`": 20.0
  }
]
```
---

#### ID:149 | financial

**问题**: Please list the account types that are not eligible for loans, and the average income of residents in the district where the account is located exceeds $8000 but is no more than $9000.

**证据**: A11 represents the average salary; Salary and income share the similar meanings; when the account type = 'OWNER', it's eligible for loans

**生成SQL**:
```sql
SELECT DISTINCT d.type FROM disp d INNER JOIN account a ON d.account_id = a.account_id INNER JOIN district di ON a.district_id = di.district_id WHERE d.type != 'OWNER' AND di.A11 > 8000 AND di.A11 <= 9000
```

**生成结果**:
```json
[
  {
    "type": "DISPONENT"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T3`.`type`
FROM `district` AS `T1`
INNER JOIN `account` AS `T2`
  ON `T1`.`district_id` = `T2`.`district_id`
INNER JOIN `disp` AS `T3`
  ON `T2`.`account_id` = `T3`.`account_id`
WHERE
  `T3`.`type` <> 'OWNER' AND `T1`.`A11` BETWEEN 8000 AND 9000
```

**预期结果**:
```json
[
  {
    "type": "DISPONENT"
  },
  {
    "type": "DISPONENT"
  },
  {
    "type": "DISPONENT"
  },
  {
    "type": "DISPONENT"
  },
  {
    "type": "DISPONENT"
  }
]
```
---

#### ID:169 | financial

**问题**: What was the growth rate of the total amount of loans across all accounts for a male client between 1996 and 1997?

**证据**: Growth rate = (sum of amount_1997 - sum of amount_1996) / (sum of amount_1996) * 100%; Male refers to gender = 'M'

**生成SQL**:
```sql
SELECT ( (SUM(CASE WHEN YEAR(loan.date) = 1997 THEN loan.amount ELSE 0 END) - SUM(CASE WHEN YEAR(loan.date) = 1996 THEN loan.amount ELSE 0 END)) / CAST(SUM(CASE WHEN YEAR(loan.date) = 1996 THEN loan.amount ELSE 0 END) AS DOUBLE) ) * 100 AS growth_rate FROM loan WHERE loan.account_id IN (SELECT DISTINCT disp.account_id FROM disp INNER JOIN client ON disp.client_id = client.client_id WHERE client.gender = 'M') AND YEAR(loan.date) IN (1996, 1997)
```

**生成结果**:
```json
[
  {
    "growth_rate": 25.36203967738821
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST((
    SUM(
      CASE
        WHEN DATE_FORMAT(CAST(`T1`.`date` AS DATETIME), '%Y') = '1997'
        THEN `T1`.`amount`
        ELSE 0
      END
    ) - SUM(
      CASE
        WHEN DATE_FORMAT(CAST(`T1`.`date` AS DATETIME), '%Y') = '1996'
        THEN `T1`.`amount`
        ELSE 0
      END
    )
  ) AS DOUBLE) * 100 / SUM(
    CASE
      WHEN DATE_FORMAT(CAST(`T1`.`date` AS DATETIME), '%Y') = '1996'
      THEN `T1`.`amount`
      ELSE 0
    END
  )
FROM `loan` AS `T1`
INNER JOIN `account` AS `T2`
  ON `T1`.`account_id` = `T2`.`account_id`
INNER JOIN `disp` AS `T3`
  ON `T3`.`acc
```

**预期结果**:
```json
[
  {
    "CAST((\n    SUM(\n      CASE\n        WHEN DATE_FORMAT(CAST(`T1`.`date` AS DATETIME), '%Y') = '1997'\n        THEN `T1`.`amount`\n        ELSE 0\n      END\n    ) - SUM(\n      CASE\n        WHEN DATE_FORMAT(CAST(`T1`.`date` AS DATETIME), '%Y') = '1996'\n        TH": 25.300191222790616
  }
]
```
---

#### ID:173 | financial

**问题**: How often does account number 3 request an account statement to be released? What was the aim of debiting 3539 in total?

**证据**: k_symbol refers to the purpose of payments

**生成SQL**:
```sql
SELECT 'frequency' AS question, CAST(COUNT(*) AS CHAR) AS answer FROM trans WHERE account_id = 3 AND operation = 'STATEMENT' UNION ALL SELECT 'aim' AS question, k_symbol AS answer FROM trans WHERE account_id = 3 AND type = '-' GROUP BY k_symbol HAVING SUM(amount) = 3539
```

**生成结果**:
```json
[
  {
    "question": "frequency",
    "answer": "0"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T1`.`frequency`,
  `T2`.`k_symbol`
FROM `account` AS `T1`
INNER JOIN (
  SELECT
    `account_id`,
    `k_symbol`,
    SUM(`amount`) AS `total_amount`
  FROM `order`
  GROUP BY
    `account_id`,
    `k_symbol`
) AS `T2`
  ON `T1`.`account_id` = `T2`.`account_id`
WHERE
  `T1`.`account_id` = 3 AND `T2`.`total_amount` = 3539
```

**预期结果**:
```json
[
  {
    "frequency": "POPLATEK MESICNE",
    "k_symbol": "POJISTNE"
  }
]
```
---


### MODERATE (133题)

#### ID:1490 | debit_card_specializing

**问题**: How many percent of LAM customer consumed more than 46.73?

**证据**: Percentage of LAM customer consumed more than 46.73 = (Total no. of LAM customers who consumed more than 46.73 / Total no. of LAM customers) * 100.

**生成SQL**:
```sql
SELECT CAST((SELECT COUNT(DISTINCT c.CustomerID) FROM customers c INNER JOIN yearmonth y ON c.CustomerID = y.CustomerID WHERE c.Segment = 'LAM' AND y.Consumption > 46.73) AS DOUBLE) / CAST((SELECT COUNT(CustomerID) FROM customers WHERE Segment = 'LAM') AS DOUBLE) * 100 AS percentage
```

**生成结果**:
```json
[
  {
    "percentage": 98.25041006014216
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST(SUM(CASE WHEN `T2`.`Consumption` > 46.73 THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(`T1`.`CustomerID`)
FROM `customers` AS `T1`
INNER JOIN `yearmonth` AS `T2`
  ON `T1`.`CustomerID` = `T2`.`CustomerID`
WHERE
  `T1`.`Segment` = 'LAM'
```

**预期结果**:
```json
[
  {
    "CAST(SUM(CASE WHEN `T2`.`Consumption` > 46.73 THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(`T1`.`CustomerID`)": 98.5267932135058
  }
]
```
---

#### ID:1501 | debit_card_specializing

**问题**: Please list the countries of the gas stations with transactions taken place in June, 2013.

**证据**: June 2013 refers to '201306'; The first 4 strings of the Date values in the yearmonth table can represent year; The 5th and 6th string of the date can refer to month;

**生成SQL**:
```sql
SELECT DISTINCT g.Country FROM transactions_1k t INNER JOIN gasstations g ON t.GasStationID = g.GasStationID WHERE t.Date >= '2013-06-01' AND t.Date <= '2013-06-30'
```

**生成结果**:
(空结果)

**预期SQL**:
```sql
SELECT DISTINCT
  `T2`.`Country`
FROM `transactions_1k` AS `T1`
INNER JOIN `gasstations` AS `T2`
  ON `T1`.`GasStationID` = `T2`.`GasStationID`
INNER JOIN `yearmonth` AS `T3`
  ON `T1`.`CustomerID` = `T3`.`CustomerID`
WHERE
  `T3`.`Date` = '201306'
```

**预期结果**:
```json
[
  {
    "Country": "CZE"
  },
  {
    "Country": "SVK"
  }
]
```
---

#### ID:1529 | debit_card_specializing

**问题**: What is the amount spent by customer "38508" at the gas stations? How much had the customer spent in January 2012?

**证据**: January 2012 refers to the Date value = '201201'

**生成SQL**:
```sql
SELECT (SELECT SUM(CAST(t.Amount AS DOUBLE) * t.Price) FROM transactions_1k t INNER JOIN gasstations g ON t.GasStationID = g.GasStationID WHERE t.CustomerID = 38508) as total_spent, (SELECT SUM(CAST(t.Amount AS DOUBLE) * t.Price) FROM transactions_1k t INNER JOIN gasstations g ON t.GasStationID = g.GasStationID WHERE t.CustomerID = 38508 AND DATE_FORMAT(t.Date, '%Y%m') = '201201') as jan_2012_spent
```

**生成结果**:
```json
[
  {
    "total_spent": 88612.38,
    "jan_2012_spent": null
  }
]
```
**预期SQL**:
```sql
SELECT
  SUM(`T1`.`Price` ),
  SUM(CASE WHEN `T3`.`Date` = '201201' THEN `T1`.`Price` ELSE 0 END)
FROM `transactions_1k` AS `T1`
INNER JOIN `gasstations` AS `T2`
  ON `T1`.`GasStationID` = `T2`.`GasStationID`
INNER JOIN `yearmonth` AS `T3`
  ON `T1`.`CustomerID` = `T3`.`CustomerID`
WHERE
  `T1`.`CustomerID` = '38508'
```

**预期结果**:
```json
[
  {
    "SUM(`T1`.`Price` )": 68740.19999999992,
    "SUM(CASE WHEN `T3`.`Date` = '201201' THEN `T1`.`Price` ELSE 0 END)": 3437.0099999999998
  }
]
```
---

#### ID:1531 | debit_card_specializing

**问题**: Who is the top spending customer and how much is the average price per single item purchased by this customer? What currency was being used?

**证据**: average price per single item = Total(price) / Total(amount)

**生成SQL**:
```sql
SELECT t.CustomerID, CAST(SUM(t.Price * t.Amount) AS DOUBLE) / CAST(SUM(t.Amount) AS DOUBLE) AS avg_price_per_item, c.Currency FROM transactions_1k t INNER JOIN customers c ON t.CustomerID = c.CustomerID WHERE t.CustomerID = (SELECT CustomerID FROM transactions_1k GROUP BY CustomerID ORDER BY SUM(Amount * Price) DESC LIMIT 1) GROUP BY t.CustomerID, c.Currency
```

**生成结果**:
```json
[
  {
    "CustomerID": 13665,
    "avg_price_per_item": 5762.49,
    "Currency": "CZK"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T2`.`CustomerID`,
  SUM(`T2`.`Price` / `T2`.`Amount`),
  `T1`.`Currency`
FROM `customers` AS `T1`
INNER JOIN `transactions_1k` AS `T2`
  ON `T1`.`CustomerID` = `T2`.`CustomerID`
WHERE
  `T2`.`CustomerID` = (
    SELECT
      `CustomerID`
    FROM `yearmonth`
    ORDER BY
      `Consumption` DESC
    LIMIT 1
  )
GROUP BY
  `T2`.`CustomerID`,
  `T1`.`Currency`
```

**预期结果**:
```json
[
  {
    "CustomerID": 12459,
    "SUM(`T2`.`Price` / `T2`.`Amount`)": 203.85607873542577,
    "Currency": "CZK"
  }
]
```
---

#### ID:1533 | debit_card_specializing

**问题**: For all the people who paid more than 29.00 per unit of product id No.5. Give their consumption status in the August of 2012.

**证据**: August of 2012 refers to the Date value = '201208' ; Price per unit of product = Price / Amount;

**生成SQL**:
```sql
SELECT ym.CustomerID, ym.Consumption FROM yearmonth ym WHERE ym.Date = '201208' AND ym.CustomerID IN (SELECT DISTINCT t.CustomerID FROM transactions_1k t WHERE t.ProductID = 5 AND (t.Price / t.Amount) > 29.00)
```

**生成结果**:
```json
[
  {
    "CustomerID": 18831,
    "Consumption": 1903.2
  },
  {
    "CustomerID": 5443,
    "Consumption": 88265.39
  },
  {
    "CustomerID": 46933,
    "Consumption": 1129.2
  },
  {
    "CustomerID": 6768,
    "Consumption": 126157.7
  },
  {
    "CustomerID": 20447,
    "Consumption": 58.19
  }
]
```
**预期SQL**:
```sql
SELECT
  `T2`.`Consumption`
FROM `transactions_1k` AS `T1`
INNER JOIN `yearmonth` AS `T2`
  ON `T1`.`CustomerID` = `T2`.`CustomerID`
WHERE
  `T1`.`Price` / `T1`.`Amount` > 29.00
  AND `T1`.`ProductID` = 5
  AND `T2`.`Date` = '201208'
```

**预期结果**:
```json
[
  {
    "Consumption": 1903.2
  },
  {
    "Consumption": 88265.39
  },
  {
    "Consumption": 1129.2
  },
  {
    "Consumption": 126157.7
  },
  {
    "Consumption": 126157.7
  }
]
```
---

#### ID:1322 | student_club

**问题**: Among the events attended by more than 10 members of the Student_Club, how many of them are meetings?

**证据**: meetings events refers to type = 'Meeting'; attended by more than 10 members refers to COUNT(event_id) > 10

**生成SQL**:
```sql
SELECT COUNT(*) AS meeting_count FROM event WHERE event_id IN (SELECT link_to_event FROM attendance GROUP BY link_to_event HAVING COUNT(link_to_member) > 10) AND type = 'Meeting'
```

**生成结果**:
```json
[
  {
    "meeting_count": 4
  }
]
```
**预期SQL**:
```sql
SELECT COUNT(DISTINCT T1.event_id) FROM event AS T1 INNER JOIN attendance AS T2 ON T1.event_id = T2.link_to_event WHERE T1.type = 'Meeting' GROUP BY T1.event_id HAVING COUNT(T2.link_to_event) > 10
```

**预期结果**:
```json
[
  {
    "COUNT(DISTINCT T1.event_id)": 1
  },
  {
    "COUNT(DISTINCT T1.event_id)": 1
  },
  {
    "COUNT(DISTINCT T1.event_id)": 1
  },
  {
    "COUNT(DISTINCT T1.event_id)": 1
  }
]
```
---

#### ID:1338 | student_club

**问题**: Was each expense in October Meeting on October 8, 2019 approved?

**证据**: event_name = 'October Meeting' where event_date = '2019-10-08'; approved = True means expenses was approved; approved = False means expenses was not approved

**生成SQL**:
```sql
SELECT CASE WHEN NOT EXISTS (SELECT 1 FROM expense exp INNER JOIN budget b ON exp.link_to_budget = b.budget_id INNER JOIN event e ON b.link_to_event = e.event_id WHERE e.event_name = 'October Meeting' AND e.event_date = '2019-10-08' AND exp.approved != 'True') THEN 'Yes' ELSE 'No' END AS result
```

**生成结果**:
```json
[
  {
    "result": "Yes"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T3`.`approved`
FROM `event` AS `T1`
INNER JOIN `budget` AS `T2`
  ON `T1`.`event_id` = `T2`.`link_to_event`
INNER JOIN `expense` AS `T3`
  ON `T2`.`budget_id` = `T3`.`link_to_budget`
WHERE
  `T1`.`event_name` = 'October Meeting' AND `T1`.`event_date` LIKE '2019-10-08%'
```

**预期结果**:
```json
[
  {
    "approved": "true"
  },
  {
    "approved": "true"
  },
  {
    "approved": "true"
  }
]
```
---

#### ID:1340 | student_club

**问题**: Calculate the difference of the total amount spent in all events by the Student_Club in year 2019 and 2020.

**证据**: The first 4 strings of the event_date values in the event table can represent year; The difference of the total amount spent = SUBTRACT(spent where YEAR(event_date) = 2019, spent where YEAR(event_date) = 2020)

**生成SQL**:
```sql
SELECT COALESCE(SUM(CASE WHEN SUBSTRING(e.event_date, 1, 4) = '2019' THEN b.spent ELSE 0 END), 0) - COALESCE(SUM(CASE WHEN SUBSTRING(e.event_date, 1, 4) = '2020' THEN b.spent ELSE 0 END), 0) AS difference FROM budget b INNER JOIN event e ON b.link_to_event = e.event_id WHERE e.event_name = 'Student_Club'
```

**生成结果**:
```json
[
  {
    "difference": 0.0
  }
]
```
**预期SQL**:
```sql
SELECT
  SUM(CASE WHEN SUBSTR(`T1`.`event_date`, 1, 4) = '2019' THEN `T2`.`spent` ELSE 0 END) - SUM(CASE WHEN SUBSTR(`T1`.`event_date`, 1, 4) = '2020' THEN `T2`.`spent` ELSE 0 END) AS `num`
FROM `event` AS `T1`
INNER JOIN `budget` AS `T2`
  ON `T1`.`event_id` = `T2`.`link_to_event`
```

**预期结果**:
```json
[
  {
    "num": 2086.0499999999997
  }
]
```
---

#### ID:1350 | student_club

**问题**: What is the status of the event which bought "Post Cards, Posters" on 2019/8/20?

**证据**: 'Post Cards, Posters' is an expense description; on 2019/8/20 refers to expense_date = '2019-8-20'; status of event refers to event_status

**生成SQL**:
```sql
SELECT b.event_status FROM expense e JOIN budget b ON e.link_to_budget = b.budget_id WHERE e.expense_description = 'Post Cards, Posters' AND e.expense_date = '2019-8-20'
```

**生成结果**:
(空结果)

**预期SQL**:
```sql
SELECT
  `T1`.`event_status`
FROM `budget` AS `T1`
INNER JOIN `expense` AS `T2`
  ON `T1`.`budget_id` = `T2`.`link_to_budget`
WHERE
  `T2`.`expense_description` = 'Post Cards, Posters'
  AND `T2`.`expense_date` = '2019-08-20'
```

**预期结果**:
```json
[
  {
    "event_status": "Closed"
  }
]
```
---

#### ID:1376 | student_club

**问题**: Among all the closed events, which event has the highest spend-to-budget ratio?

**证据**: closed events refers to event_name where status = 'Closed'; highest spend-to budget ratio refers to MAX(DIVIDE(spent, amount))

**生成SQL**:
```sql
SELECT T1.event_name FROM event T1 INNER JOIN budget T2 ON T1.event_id = T2.link_to_event WHERE T1.status = 'Closed' GROUP BY T1.event_id, T1.event_name ORDER BY CAST(SUM(T2.spent) AS DOUBLE) / SUM(T2.amount) DESC LIMIT 1
```

**生成结果**:
```json
[
  {
    "event_name": "Officers meeting - October"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T2`.`event_name`
FROM `budget` AS `T1`
INNER JOIN `event` AS `T2`
  ON `T1`.`link_to_event` = `T2`.`event_id`
WHERE
  `T2`.`status` = 'Closed'
ORDER BY
  `T1`.`spent` / `T1`.`amount` DESC
LIMIT 1
```

**预期结果**:
```json
[
  {
    "event_name": "September Speaker"
  }
]
```
---

#### ID:1387 | student_club

**问题**: Which student has been entrusted to manage the budget for the Yearly Kickoff?

**证据**: name of students means the full name; full name refers to first_name, last_name;'Yearly Kickoff' is an event name;

**生成SQL**:
```sql
SELECT DISTINCT CONCAT(m.first_name, ' ', m.last_name) AS full_name FROM member m INNER JOIN expense e ON m.member_id = e.link_to_member INNER JOIN budget b ON e.link_to_budget = b.budget_id INNER JOIN event ev ON b.link_to_event = ev.event_id WHERE ev.event_name = 'Yearly Kickoff'
```

**生成结果**:
```json
[
  {
    "full_name": "Elijah Allen"
  },
  {
    "full_name": "Sacha Harrison"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T4`.`first_name`,
  `T4`.`last_name`
FROM `event` AS `T1`
INNER JOIN `budget` AS `T2`
  ON `T1`.`event_id` = `T2`.`link_to_event`
INNER JOIN `expense` AS `T3`
  ON `T2`.`budget_id` = `T3`.`link_to_budget`
INNER JOIN `member` AS `T4`
  ON `T3`.`link_to_member` = `T4`.`member_id`
WHERE
  `T1`.`event_name` = 'Yearly Kickoff'
```

**预期结果**:
```json
[
  {
    "first_name": "Elijah",
    "last_name": "Allen"
  },
  {
    "first_name": "Elijah",
    "last_name": "Allen"
  },
  {
    "first_name": "Sacha",
    "last_name": "Harrison"
  },
  {
    "first_name": "Sacha",
    "last_name": "Harrison"
  }
]
```
---

#### ID:1399 | student_club

**问题**: Did Maya Mclean attend the 'Women's Soccer' event?

**证据**: Maya Mclean is the full name; full name refers to first_name, last_name; 'Women's Soccer' is an event_name

**生成SQL**:
```sql
SELECT EXISTS (SELECT 1 FROM attendance a JOIN member m ON a.link_to_member = m.member_id JOIN event e ON a.link_to_event = e.event_id WHERE m.first_name = 'Maya' AND m.last_name = 'Mclean' AND e.event_name = 'Women''s Soccer') AS attended
```

**生成结果**:
```json
[
  {
    "attended": 1
  }
]
```
**预期SQL**:
```sql
SELECT
  CASE WHEN `T3`.`event_name` = 'Women''s Soccer' THEN 'YES' END AS `result`
FROM `member` AS `T1`
INNER JOIN `attendance` AS `T2`
  ON `T1`.`member_id` = `T2`.`link_to_member`
INNER JOIN `event` AS `T3`
  ON `T2`.`link_to_event` = `T3`.`event_id`
WHERE
  `T1`.`first_name` = 'Maya' AND `T1`.`last_name` = 'Mclean'
```

**预期结果**:
```json
[
  {
    "result": "YES"
  },
  {
    "result": null
  },
  {
    "result": null
  },
  {
    "result": null
  },
  {
    "result": null
  }
]
```
---

#### ID:1404 | student_club

**问题**: Identify the type of expenses and their total value approved for 'October Meeting' event.

**证据**: total value refers to SUM(cost); 'October Meeting' is an event name;

**生成SQL**:
```sql
SELECT budget.category, SUM(expense.cost) as total_value FROM event INNER JOIN budget ON event.event_id = budget.link_to_event INNER JOIN expense ON budget.budget_id = expense.link_to_budget WHERE event.event_name = 'October Meeting' AND expense.approved = 'true' GROUP BY budget.category
```

**生成结果**:
```json
[
  {
    "category": "Food",
    "total_value": 121.14
  },
  {
    "category": "Advertisement",
    "total_value": 54.25
  }
]
```
**预期SQL**:
```sql
SELECT `T1`.`type`, SUM(`T3`.`cost`) AS `total_cost` FROM `event` AS `T1` INNER JOIN `budget` AS `T2` ON `T1`.`event_id` = `T2`.`link_to_event` INNER JOIN `expense` AS `T3` ON `T2`.`budget_id` = `T3`.`link_to_budget` WHERE `T1`.`event_name` = 'October Meeting' GROUP BY `T1`.`type`
```

**预期结果**:
```json
[
  {
    "type": "Meeting",
    "total_cost": 175.39
  }
]
```
---

#### ID:1427 | student_club

**问题**: What are the budget category of the events located at MU 215 and a guest speaker type with a 0 budget spent?

**证据**: budget category refers to category; events located at refers to location; type = 'Guest Speaker'; 0 budget spent refers to spent = 0; 

**生成SQL**:
```sql
SELECT budget.category FROM budget INNER JOIN event ON budget.link_to_event = event.event_id WHERE event.location = 'MU 215' AND event.type = 'Guest Speaker' AND budget.spent = 0
```

**生成结果**:
```json
[
  {
    "category": "Speaker Gifts"
  },
  {
    "category": "Parking"
  },
  {
    "category": "Advertisement"
  },
  {
    "category": "Food"
  },
  {
    "category": "Speaker Gifts"
  }
]
```
**预期SQL**:
```sql
SELECT DISTINCT
  `T2`.`category`,
  `T1`.`type`
FROM `event` AS `T1`
INNER JOIN `budget` AS `T2`
  ON `T1`.`event_id` = `T2`.`link_to_event`
WHERE
  `T1`.`location` = 'MU 215' AND `T2`.`spent` = 0 AND `T1`.`type` = 'Guest Speaker'
```

**预期结果**:
```json
[
  {
    "category": "Speaker Gifts",
    "type": "Guest Speaker"
  },
  {
    "category": "Parking",
    "type": "Guest Speaker"
  },
  {
    "category": "Advertisement",
    "type": "Guest Speaker"
  },
  {
    "category": "Food",
    "type": "Guest Speaker"
  }
]
```
---

#### ID:1432 | student_club

**问题**: Among the members with t-shirt size of medium, what is the percentage of the amount 50 received by the Student_Club?

**证据**: t_shirt_size = 'Medium' where position = 'Member'; percentage = DIVIDE(COUNT(amount = 50), COUNT(member_id)) * 100

**生成SQL**:
```sql
SELECT (CAST(COUNT(DISTINCT CASE WHEN income.source = 'Student_Club' AND income.amount = 50 THEN member.member_id END) AS DOUBLE) / CAST(COUNT(DISTINCT member.member_id) AS DOUBLE)) * 100 AS percentage FROM member LEFT JOIN income ON member.member_id = income.link_to_member WHERE member.t_shirt_size = 'Medium'
```

**生成结果**:
```json
[
  {
    "percentage": 0.0
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST(SUM(CASE WHEN `T2`.`amount` = 50 THEN 1.0 ELSE 0 END) AS DOUBLE) * 100 / COUNT(`T2`.`income_id`)
FROM `member` AS `T1`
INNER JOIN `income` AS `T2`
  ON `T1`.`member_id` = `T2`.`link_to_member`
WHERE
  `T1`.`position` = 'Member' AND `T1`.`t_shirt_size` = 'Medium'
```

**预期结果**:
```json
[
  {
    "CAST(SUM(CASE WHEN `T2`.`amount` = 50 THEN 1.0 ELSE 0 END) AS DOUBLE) * 100 / COUNT(`T2`.`income_id`)": 100.0
  }
]
```
---

#### ID:1435 | student_club

**问题**: List the names of closed event as "game" that was closed from 3/15/2019 to 3/20/2020.

**证据**: name of events refers event_name; game event that was closed refers to type = 'Game' where status = 'Closed'; event_date BETWEEN '2019-03-15' and '2020-03-20'; 

**生成SQL**:
```sql
SELECT event_name FROM event WHERE type = 'Game' AND status = 'Closed' AND event_date BETWEEN '2019-03-15' AND '2020-03-20'
```

**生成结果**:
```json
[
  {
    "event_name": "Women's Soccer"
  },
  {
    "event_name": "Football game"
  },
  {
    "event_name": "Football game"
  }
]
```
**预期SQL**:
```sql
SELECT DISTINCT
  `event_name`
FROM `event`
WHERE
  `type` = 'Game'
  AND DATE(SUBSTR(`event_date`, 1, 10)) BETWEEN '2019-03-15' AND '2020-03-20'
  AND `status` = 'Closed'
```

**预期结果**:
```json
[
  {
    "event_name": "Women's Soccer"
  },
  {
    "event_name": "Football game"
  }
]
```
---

#### ID:1149 | thrombosis_prediction

**问题**: Are there more in-patient or outpatient who were male? What is the deviation in percentage?

**证据**: male refers to SEX = 'M'; in-patient refers to Admission = '+'; outpatient refers to Admission = '-'; percentage = DIVIDE(COUNT(ID) where SEX = 'M' and Admission = '+', COUNT(ID) where SEX  = 'M' and Admission = '-')

**生成SQL**:
```sql
SELECT COUNT(CASE WHEN Admission = '+' THEN 1 END) AS in_patient_count, COUNT(CASE WHEN Admission = '-' THEN 1 END) AS out_patient_count, COUNT(CASE WHEN Admission = '+' THEN 1 END) / COUNT(CASE WHEN Admission = '-' THEN 1 END) AS deviation_percentage FROM Patient WHERE SEX = 'M'
```

**生成结果**:
```json
[
  {
    "in_patient_count": 89,
    "out_patient_count": 107,
    "deviation_percentage": 0.8318
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST(SUM(CASE WHEN `Admission` = '+' THEN 1 ELSE 0 END) AS DOUBLE) * 100 / SUM(CASE WHEN `Admission` = '-' THEN 1 ELSE 0 END)
FROM `Patient`
WHERE
  `SEX` = 'M'
```

**预期结果**:
```json
[
  {
    "CAST(SUM(CASE WHEN `Admission` = '+' THEN 1 ELSE 0 END) AS DOUBLE) * 100 / SUM(CASE WHEN `Admission` = '-' THEN 1 ELSE 0 END)": 83.17757009345794
  }
]
```
---

#### ID:1152 | thrombosis_prediction

**问题**: What is the ratio of outpatient to inpatient followed up treatment among all the 'SLE' diagnosed patient?

**证据**: 'SLE' diagnosed patient means Diagnosis = 'SLE'; inpatient refers to Admission = '+'; outpatient refers to Admission = '-'; calculation =  DIVIDE(COUNT(ID) where Diagnosis = 'SLE' and Admission = '+', COUNT(ID) where Diagnosis = 'SLE' and Admission = '-')

**生成SQL**:
```sql
SELECT CAST(COUNT(CASE WHEN Admission = '-' THEN 1 END) AS DOUBLE) / NULLIF(COUNT(CASE WHEN Admission = '+' THEN 1 END), 0) AS outpatient_to_inpatient_ratio FROM Patient WHERE Diagnosis = 'SLE'
```

**生成结果**:
```json
[
  {
    "outpatient_to_inpatient_ratio": 0.7636363636363637
  }
]
```
**预期SQL**:
```sql
SELECT
  SUM(CASE WHEN `Admission` = '+' THEN 1 ELSE 0 END) / SUM(CASE WHEN `Admission` = '-' THEN 1 ELSE 0 END)
FROM `Patient`
WHERE
  `Diagnosis` = 'SLE'
```

**预期结果**:
```json
[
  {
    "SUM(CASE WHEN `Admission` = '+' THEN 1 ELSE 0 END) / SUM(CASE WHEN `Admission` = '-' THEN 1 ELSE 0 END)": 1.3095
  }
]
```
---

#### ID:1175 | thrombosis_prediction

**问题**: How old was the patient who had the highest hemoglobin count at the time of the examination, and what is the doctor's diagnosis?

**证据**: How old the patient refers to SUBTRACT(year(`Examination Date`), year(Birthday)); the highest hemoglobin count refers to MAX(HGB)

**生成SQL**:
```sql
SELECT (YEAR(Examination.`Examination Date`) - YEAR(Patient.Birthday)) AS Age, Examination.Diagnosis FROM Laboratory INNER JOIN Examination ON Laboratory.ID = Examination.ID AND Laboratory.Date = Examination.`Examination Date` INNER JOIN Patient ON Laboratory.ID = Patient.ID WHERE Laboratory.HGB = (SELECT MAX(HGB) FROM Laboratory) ORDER BY Laboratory.HGB DESC LIMIT 1
```

**生成结果**:
(空结果)

**预期SQL**:
```sql
SELECT
  DATE_FORMAT(CAST(`T2`.`Date` AS DATETIME), '%Y') - DATE_FORMAT(CAST(`T1`.`Birthday` AS DATETIME), '%Y'),
  `T1`.`Diagnosis`
FROM `Patient` AS `T1`
INNER JOIN `Laboratory` AS `T2`
  ON `T1`.`ID` = `T2`.`ID`
ORDER BY
  `T2`.`HGB` DESC
LIMIT 1
```

**预期结果**:
```json
[
  {
    "DATE_FORMAT(CAST(`T2`.`Date` AS DATETIME), '%Y') - DATE_FORMAT(CAST(`T1`.`Birthday` AS DATETIME), '%Y')": 28.0,
    "Diagnosis": "SLE"
  }
]
```
---

#### ID:1179 | thrombosis_prediction

**问题**: For the patient who was diagnosed with SLE on 1994/2/19, what was his/her anti-Cardiolipin antibody concentration status on 1993/11/12?

**证据**: diagnosed with SLE refers to Diagnosis = 'SLE'; 1994/2/19 refers to Description = '1994-02-19'; anti-Cardiolipin refers to aCL IgM; 1993/11/12 refers to Examination Date = '1993/11/12'

**生成SQL**:
```sql
SELECT `aCL IgM` FROM Examination WHERE ID = (SELECT ID FROM Patient WHERE Diagnosis = 'SLE' AND Description = '1994-02-19') AND `Examination Date` = '1993-11-12'
```

**生成结果**:
```
❌ 执行失败
```

**预期SQL**:
```sql
SELECT
  `aCL IgA`,
  `aCL IgG`,
  `aCL IgM`
FROM `Examination`
WHERE
  `ID` IN (
    SELECT
      `ID`
    FROM `Patient`
    WHERE
      `Diagnosis` = 'SLE' AND `Description` = '1994-02-19'
  )
  AND `Examination Date` = '1993-11-12'
```

**预期结果**:
```json
[
  {
    "aCL IgA": 3,
    "aCL IgG": 5.1,
    "aCL IgM": 4.1
  }
]
```
---

#### ID:1205 | thrombosis_prediction

**问题**: Was the patient with the number 57266's uric acid within a normal range?

**证据**: uric acid within a normal range refers to UA > 8.0 and SEX = 'M'OR UA > 6.5 and SEX = 'F'

**生成SQL**:
```sql
SELECT CASE WHEN p.SEX = 'M' AND l.UA > 8.0 THEN 'Yes' WHEN p.SEX = 'F' AND l.UA > 6.5 THEN 'Yes' ELSE 'No' END AS is_normal FROM Patient p INNER JOIN Laboratory l ON p.ID = l.ID WHERE p.ID = 57266 AND l.Date = (SELECT MAX(Date) FROM Laboratory WHERE ID = 57266)
```

**生成结果**:
```json
[
  {
    "is_normal": "No"
  }
]
```
**预期SQL**:
```sql
SELECT
  CASE
    WHEN (
      `T1`.`SEX` = 'F' AND `T2`.`UA` > 6.5
    )
    OR (
      `T1`.`SEX` = 'M' AND `T2`.`UA` > 8.0
    )
    THEN TRUE
    ELSE FALSE
  END
FROM `Patient` AS `T1`
INNER JOIN `Laboratory` AS `T2`
  ON `T1`.`ID` = `T2`.`ID`
WHERE
  `T1`.`ID` = 57266
```

**预期结果**:
```json
[
  {
    "CASE\n    WHEN (\n      `T1`.`SEX` = 'F' AND `T2`.`UA` > 6.5\n    )\n    OR (\n      `T1`.`SEX` = 'M' AND `T2`.`UA` > 8.0\n    )\n    THEN TRUE\n    ELSE FALSE\n  END": 0
  },
  {
    "CASE\n    WHEN (\n      `T1`.`SEX` = 'F' AND `T2`.`UA` > 6.5\n    )\n    OR (\n      `T1`.`SEX` = 'M' AND `T2`.`UA` > 8.0\n    )\n    THEN TRUE\n    ELSE FALSE\n  END": 0
  },
  {
    "CASE\n    WHEN (\n      `T1`.`SEX` = 'F' AND `T2`.`UA` > 6.5\n    )\n    OR (\n      `T1`.`SEX` = 'M' AND `T2`.`UA` > 8.0\n    )\n    THEN TRUE\n    ELSE FALSE\n  END": 0
  },
  {
    "CASE\n    WHEN (\n      `T1`.`SEX` = 'F' AND `T2`.`UA` > 6.5\n    )\n    OR (\n      `T1`.`SEX` = 'M' AND `T2`.`UA` > 8.0\n    )\n    THEN TRUE\n    ELSE FALSE\n  END": 0
  },
  {
    "CASE\n    WHEN (\n      `T1`.`SEX` = 'F' AND `T2`.`UA` > 6.5\n    )\n    OR (\n      `T1`.`SEX` = 'M' AND `T2`.`UA` > 8.0\n    )\n    THEN TRUE\n    ELSE FALSE\n  END": 0
  }
]
```
---

#### ID:1209 | thrombosis_prediction

**问题**: Please provide the diagnosis of patients with ALT glutamic pylvic transaminase beyond the normal range by ascending order of their date of birth.

**证据**: ALT glutamic pylvic transaminase beyond the normal range refers to GPT > 60; The larger the birthday value, the younger the person is, and vice versa; 

**生成SQL**:
```sql
SELECT DISTINCT P.Diagnosis FROM Patient P INNER JOIN Laboratory L ON P.ID = L.ID WHERE L.GPT > 60 ORDER BY P.Birthday ASC
```

**生成结果**:
```
❌ 执行失败
```

**预期SQL**:
```sql
SELECT `T1`.`Diagnosis`
FROM `Patient` AS `T1`
INNER JOIN `Laboratory` AS `T2`
  ON `T1`.`ID` = `T2`.`ID`
WHERE
  `T2`.`GPT` > 60
ORDER BY
  `T1`.`Birthday` ASC
```

**预期结果**:
```json
[
  {
    "Diagnosis": "MRA"
  },
  {
    "Diagnosis": "MRA"
  },
  {
    "Diagnosis": "MRA"
  },
  {
    "Diagnosis": "MRA"
  },
  {
    "Diagnosis": "MRA"
  }
]
```
---

#### ID:1225 | thrombosis_prediction

**问题**: List and group all patients by sex for total bilirubin (T-BIL) level not within the normal range.

**证据**: total bilirubin (T-BIL) not within normal range refers to T-BIL > = 2.0

**生成SQL**:
```sql
SELECT p.SEX, GROUP_CONCAT(DISTINCT p.ID) AS patient_ids FROM Patient p INNER JOIN Laboratory l ON p.ID = l.ID WHERE l.`T-BIL` >= 2.0 GROUP BY p.SEX
```

**生成结果**:
```json
[
  {
    "SEX": "F",
    "patient_ids": "250391,1180510,2308236,2931207,4862013"
  },
  {
    "SEX": "M",
    "patient_ids": "43003,444499,1137040,2307640,4618443"
  }
]
```
**预期SQL**:
```sql
SELECT T1.ID, T1.SEX FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.`T-BIL` >= 2.0 GROUP BY T1.SEX, T1.ID
```

**预期结果**:
```json
[
  {
    "ID": 43003,
    "SEX": "M"
  },
  {
    "ID": 250391,
    "SEX": "F"
  },
  {
    "ID": 444499,
    "SEX": "M"
  },
  {
    "ID": 1137040,
    "SEX": "M"
  },
  {
    "ID": 1180510,
    "SEX": "F"
  }
]
```
---

#### ID:1227 | thrombosis_prediction

**问题**: What is the average age of the male patient with high cholesterol?

**证据**: average age = DIVIDE(SUM(SUBTRACT(YEAR(NOW()), YEAR(birthday))), COUNT(ID)); male patient refers to sex = 'M'; high cholesterol refers to `T-CHO` > = 250;

**生成SQL**:
```sql
SELECT CAST(SUM(YEAR(NOW()) - YEAR(Birthday)) AS DOUBLE) / COUNT(ID) AS average_age FROM Patient WHERE SEX = 'M' AND ID IN (SELECT DISTINCT ID FROM Laboratory WHERE `T-CHO` >= 250)
```

**生成结果**:
```json
[
  {
    "average_age": 71.95
  }
]
```
**预期SQL**:
```sql
SELECT AVG(YEAR(CURRENT_DATE) - YEAR(T1.Birthday)) FROM Patient AS T1  INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID  WHERE T2.`T-CHO` >= 250 AND T1.SEX = 'M'
```

**预期结果**:
```json
[
  {
    "AVG(YEAR(CURRENT_DATE) - YEAR(T1.Birthday))": 74.6854
  }
]
```
---

#### ID:1252 | thrombosis_prediction

**问题**: Among the patients with a normal Ig G level, how many of them have symptoms?

**证据**: normal Ig G level refers to IGG > 900 and IGG < 2000; have symptoms refers to Symptoms IS NOT NULL;

**生成SQL**:
```sql
SELECT COUNT(DISTINCT P.ID) FROM Patient P INNER JOIN Laboratory L ON P.ID = L.ID INNER JOIN Examination E ON P.ID = E.ID WHERE L.IGG > 900 AND L.IGG < 2000 AND E.Symptoms IS NOT NULL
```

**生成结果**:
```json
[
  {
    "COUNT(DISTINCT P.ID)": 1
  }
]
```
**预期SQL**:
```sql
SELECT
  COUNT(`T1`.`ID`)
FROM `Patient` AS `T1`
INNER JOIN `Laboratory` AS `T2`
  ON `T1`.`ID` = `T2`.`ID`
INNER JOIN `Examination` AS `T3`
  ON `T3`.`ID` = `T2`.`ID`
WHERE
  `T2`.`IGG` BETWEEN 900 AND 2000 AND NOT `T3`.`Symptoms` IS NULL
```

**预期结果**:
```json
[
  {
    "COUNT(`T1`.`ID`)": 4
  }
]
```
---

#### ID:1254 | thrombosis_prediction

**问题**: How many patients with a normal Ig A level came to the hospital after 1990/1/1?

**证据**: normal Ig A level refers to IGA > 80 AND IGA < 500; came to the hospital after 1990/1/1 refers to YEAR(`First Date`) > = 1990;

**生成SQL**:
```sql
SELECT COUNT(DISTINCT P.ID) FROM Patient P INNER JOIN Laboratory L ON P.ID = L.ID WHERE L.IGA > 80 AND L.IGA < 500 AND YEAR(P.First Date) >= 1990
```

**生成结果**:
```
❌ 执行失败
```

**预期SQL**:
```sql
SELECT
  COUNT(`T1`.`ID`)
FROM `Patient` AS `T1`
INNER JOIN `Laboratory` AS `T2`
  ON `T1`.`ID` = `T2`.`ID`
WHERE
  `T2`.`IGA` BETWEEN 80 AND 500
  AND DATE_FORMAT(CAST(`T1`.`First Date` AS DATETIME), '%Y') > '1990'
```

**预期结果**:
```json
[
  {
    "COUNT(`T1`.`ID`)": 1590
  }
]
```
---

#### ID:1255 | thrombosis_prediction

**问题**: For the patients with an abnormal Ig M level, what is the most common disease they are diagnosed with?

**证据**: abnormal Ig M level refers to IGM <=40 OR IGM >= 400; most common disease refers to MAX(COUNT(Diagnosis));

**生成SQL**:
```sql
SELECT p.Diagnosis, COUNT(*) as disease_count FROM Patient p INNER JOIN (SELECT DISTINCT ID FROM Laboratory WHERE IGM <= 40 OR IGM >= 400) abnormal_patients ON p.ID = abnormal_patients.ID GROUP BY p.Diagnosis ORDER BY disease_count DESC LIMIT 1
```

**生成结果**:
```json
[
  {
    "Diagnosis": "SLE",
    "disease_count": 10
  }
]
```
**预期SQL**:
```sql
SELECT
  `T1`.`Diagnosis`
FROM `Patient` AS `T1`
INNER JOIN `Laboratory` AS `T2`
  ON `T1`.`ID` = `T2`.`ID`
WHERE
  NOT `T2`.`IGM` BETWEEN 40 AND 400
GROUP BY
  `T1`.`Diagnosis`
ORDER BY
  COUNT(`T1`.`Diagnosis`) DESC
LIMIT 1
```

**预期结果**:
```json
[
  {
    "Diagnosis": "RA"
  }
]
```
---

#### ID:1256 | thrombosis_prediction

**问题**: How many patients with a abnormal C-reactive protein don't have their data recorded?

**证据**: abnormal C-reactive protein refers to CRP ='+'; don't have data recorded refers to Description IS NULL;

**生成SQL**:
```sql
SELECT COUNT(DISTINCT Patient.ID) FROM Patient INNER JOIN Laboratory ON Patient.ID = Laboratory.ID WHERE Laboratory.CRP = '+' AND Patient.Description IS NULL
```

**生成结果**:
```json
[
  {
    "COUNT(DISTINCT Patient.ID)": 25
  }
]
```
**预期SQL**:
```sql
SELECT COUNT(T1.ID) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE (T2.CRP = '+' ) AND T1.Description IS NULL;
```

**预期结果**:
```json
[
  {
    "COUNT(T1.ID)": 208
  }
]
```
---

#### ID:1265 | thrombosis_prediction

**问题**: How many patients have a normal level of anti-ribonuclear protein and have been admitted to the hospital?

**证据**: normal level of anti-ribonuclear protein refers to RNP = '-', '+-'; And'-' means 'negative'; '+-' refers to '0'; admitted to the hospital refers to Admission = '+'; Should consider DISTINCT in the final result;

**生成SQL**:
```sql
SELECT COUNT(DISTINCT Patient.ID) AS patient_count FROM Patient INNER JOIN Laboratory ON Patient.ID = Laboratory.ID WHERE Laboratory.RNP IN ('-', '+-') AND Patient.Admission = '+'
```

**生成结果**:
```json
[
  {
    "patient_count": 0
  }
]
```
**预期SQL**:
```sql
SELECT
  COUNT(DISTINCT `T1`.`ID`)
FROM `Patient` AS `T1`
INNER JOIN `Laboratory` AS `T2`
  ON `T1`.`ID` = `T2`.`ID`
WHERE
  `T2`.`RNP` = 'negative' OR `T2`.`RNP` = '0' AND `T1`.`Admission` = '+'
```

**预期结果**:
```json
[
  {
    "COUNT(DISTINCT `T1`.`ID`)": 47
  }
]
```
---

#### ID:1267 | thrombosis_prediction

**问题**: Among the patients with normal anti-SM, how many of them does not have thrombosis?

**证据**: normal anti-SM refers to SM IN('-', '+-'); SM = 'negative' means '-'; SM = '0' means '+-'; SM = '1' means '+'; does not have thrombosis refers to Thrombosis = 0;

**生成SQL**:
```sql
SELECT COUNT(DISTINCT L.ID) FROM Laboratory L WHERE L.SM IN ('negative', '0') AND EXISTS (SELECT 1 FROM Examination E WHERE E.ID = L.ID AND E.Thrombosis = 0)
```

**生成结果**:
```json
[
  {
    "COUNT(DISTINCT L.ID)": 6
  }
]
```
**预期SQL**:
```sql
SELECT
  COUNT(`T1`.`ID`)
FROM `Examination` AS `T1`
INNER JOIN `Laboratory` AS `T2`
  ON `T1`.`ID` = `T2`.`ID`
WHERE
  `T2`.`SM` IN ('negative', '0') AND `T1`.`Thrombosis` = 0
```

**预期结果**:
```json
[
  {
    "COUNT(`T1`.`ID`)": 7
  }
]
```
---

#### ID:1275 | thrombosis_prediction

**问题**: Among the patients who has a normal level of anti-centromere and a normal level of anti-SSB, how many of them are male?

**证据**: normal level of anti-centromere refers to CENTROMEA IN('-', '+-'); normal level of anti-SSB refers to SSB IN('-', '+-'); male refers to Sex = 'M'; Should consider DISTINCT in the final result;

**生成SQL**:
```sql
SELECT COUNT(DISTINCT Patient.ID) FROM Laboratory INNER JOIN Patient ON Laboratory.ID = Patient.ID WHERE Laboratory.CENTROMEA IN ('-', '+-') AND Laboratory.SSB IN ('-', '+-') AND Patient.Sex = 'M'
```

**生成结果**:
```json
[
  {
    "COUNT(DISTINCT Patient.ID)": 0
  }
]
```
**预期SQL**:
```sql
SELECT
  COUNT(DISTINCT `T1`.`ID`)
FROM `Patient` AS `T1`
INNER JOIN `Laboratory` AS `T2`
  ON `T1`.`ID` = `T2`.`ID`
WHERE
  `T2`.`CENTROMEA` IN ('negative', '0')
  AND `T2`.`SSB` IN ('negative', '0')
  AND `T1`.`SEX` = 'M'
```

**预期结果**:
```json
[
  {
    "COUNT(DISTINCT `T1`.`ID`)": 1
  }
]
```
---

#### ID:1025 | european_football_2

**问题**: Give the name of the league had the most goals in the 2016 season?

**证据**: league that had the most goals refers to MAX(SUM(home_team_goal, away_team_goal)); 2016 season refers to season = '2015/2016';

**生成SQL**:
```sql
SELECT l.name FROM Match m JOIN League l ON m.league_id = l.id WHERE m.season = '2015/2016' GROUP BY m.league_id ORDER BY SUM(m.home_team_goal + m.away_team_goal) DESC LIMIT 1
```

**生成结果**:
```
❌ 执行失败
```

**预期SQL**:
```sql
SELECT  `t2`.`name` FROM `Match` AS `t1` INNER JOIN `League` AS `t2`
  ON `t1`.`league_id` = `t2`.`id`
WHERE
  `t1`.`season` = '2015/2016'
GROUP BY
  `t2`.`name`
ORDER BY
  SUM(`t1`.`home_team_goal` + `t1`.`away_team_goal`) DESC
LIMIT 1
```

**预期结果**:
```json
[
  {
    "name": "Spain LIGA BBVA"
  }
]
```
---

#### ID:1029 | european_football_2

**问题**: What are the speed in which attacks are put together of the top 4 teams with the highest build Up Play Speed?

**证据**: speed in which attacks are put together refers to buildUpPlaySpeed;highest build up play speed refers to MAX(buildUpPlaySpeed)

**生成SQL**:
```sql
SELECT T.team_long_name, TA.buildUpPlaySpeed FROM Team_Attributes TA INNER JOIN Team T ON TA.team_api_id = T.team_api_id INNER JOIN (SELECT team_api_id, MAX(date) as latest_date FROM Team_Attributes GROUP BY team_api_id) latest ON TA.team_api_id = latest.team_api_id AND TA.date = latest.latest_date ORDER BY TA.buildUpPlaySpeed DESC LIMIT 4
```

**生成结果**:
```json
[
  {
    "team_long_name": "Carpi",
    "buildUpPlaySpeed": 80
  },
  {
    "team_long_name": "West Ham United",
    "buildUpPlaySpeed": 77
  },
  {
    "team_long_name": "Bayer 04 Leverkusen",
    "buildUpPlaySpeed": 73
  },
  {
    "team_long_name": "Borussia Dortmund",
    "buildUpPlaySpeed": 71
  }
]
```
**预期SQL**:
```sql
SELECT
  `t1`.`buildUpPlaySpeed`
FROM `Team_Attributes` AS `t1`
INNER JOIN `Team` AS `t2`
  ON `t1`.`team_api_id` = `t2`.`team_api_id`
ORDER BY
  `t1`.`buildUpPlaySpeed` ASC
LIMIT 4
```

**预期结果**:
```json
[
  {
    "buildUpPlaySpeed": 20
  },
  {
    "buildUpPlaySpeed": 20
  },
  {
    "buildUpPlaySpeed": 20
  },
  {
    "buildUpPlaySpeed": 23
  }
]
```
---

#### ID:1030 | european_football_2

**问题**: Give the name of the league had the most matches end as draw in the 2016 season?

**证据**: most matches end as draw refers to MAX(SUM(home_team_goal = away_team_goal)); 2016 season refers to season = '2015/2016';

**生成SQL**:
```sql
SELECT l.name FROM League l INNER JOIN ( SELECT league_id, SUM(home_team_goal = away_team_goal) AS draw_count FROM Match WHERE season = '2015/2016' GROUP BY league_id ) t ON l.id = t.league_id ORDER BY t.draw_count DESC LIMIT 1
```

**生成结果**:
```
❌ 执行失败
```

**预期SQL**:
```sql
SELECT
  `t2`.`name`
FROM `Match` AS `t1`
INNER JOIN `League` AS `t2`
  ON `t1`.`league_id` = `t2`.`id`
WHERE
  `t1`.`season` = '2015/2016' AND `t1`.`home_team_goal` = `t1`.`away_team_goal`
GROUP BY
  `t2`.`name`
ORDER BY
  COUNT(`t1`.`id`) DESC
LIMIT 1
```

**预期结果**:
```json
[
  {
    "name": "France Ligue 1"
  }
]
```
---

#### ID:1032 | european_football_2

**问题**: Give the name of the league with the highest matches of all time and how many matches were played in the said league.

**证据**:  league with highest matches of all time refers to MAX(COUNT(league_id));

**生成SQL**:
```sql
SELECT l.name, COUNT(*) as match_count FROM Match m INNER JOIN League l ON m.league_id = l.id GROUP BY l.id, l.name ORDER BY match_count DESC LIMIT 1
```

**生成结果**:
```
❌ 执行失败
```

**预期SQL**:
```sql
SELECT
  `t2`.`name`,
  COUNT(`t1`.`id`)
FROM `Match` AS `t1`
INNER JOIN `League` AS `t2`
  ON `t1`.`league_id` = `t2`.`id`
GROUP BY
  `t2`.`name`
ORDER BY
  COUNT(`t1`.`id`) DESC
LIMIT 1
```

**预期结果**:
```json
[
  {
    "name": "England Premier League",
    "COUNT(`t1`.`id`)": 3040
  }
]
```
---

#### ID:1057 | european_football_2

**问题**: Calculate the average home team goal in the 2010/2011 season in the country of Poland.

**证据**: average home team goal = AVG(home_team_goal)= SUM(home_team_goal) / COUNT(DISTINCT Match.id) WHERE name = 'Poland' and season = '2010/2011';

**生成SQL**:
```sql
SELECT AVG(Match.home_team_goal) AS average_home_team_goal FROM Match INNER JOIN Country ON Match.country_id = Country.id WHERE Country.name = 'Poland' AND Match.season = '2010/2011'
```

**生成结果**:
```
❌ 执行失败
```

**预期SQL**:
```sql
SELECT
  CAST(SUM(`t2`.`home_team_goal`) AS DOUBLE) / COUNT(`t2`.`id`)
FROM `Country` AS `t1`
INNER JOIN `Match` AS `t2`
  ON `t1`.`id` = `t2`.`country_id`
WHERE
  `t1`.`name` = 'Poland' AND `t2`.`season` = '2010/2011'
```

**预期结果**:
```json
[
  {
    "CAST(SUM(`t2`.`home_team_goal`) AS DOUBLE) / COUNT(`t2`.`id`)": 1.5041666666666667
  }
]
```
---

#### ID:1080 | european_football_2

**问题**: Among the players whose preferred foot was the left foot when attacking, how many of them would remain in his position when the team attacked?

**证据**: preferred foot when attacking was the left refers to preferred_foot = 'left'; players who would remain in his position when the team attacked refers to attacking_work_rate = 'low';

**生成SQL**:
```sql
SELECT COUNT(DISTINCT player_api_id) AS player_count FROM Player_Attributes WHERE preferred_foot = 'left' AND attacking_work_rate = 'low'
```

**生成结果**:
```json
[
  {
    "player_count": 189
  }
]
```
**预期SQL**:
```sql
SELECT
  COUNT(`player_api_id`)
FROM `Player_Attributes`
WHERE
  `preferred_foot` = 'left' AND `attacking_work_rate` = 'low'
```

**预期结果**:
```json
[
  {
    "COUNT(`player_api_id`)": 1569
  }
]
```
---

#### ID:1091 | european_football_2

**问题**: How many matches were held in the Belgium Jupiler League in April, 2009?

**证据**: Belgium Jupiler League refers to League.name = 'Belgium Jupiler League'; in April, 2009 refers to SUBSTR(`date`, 1, 7);

**生成SQL**:
```sql
SELECT COUNT(*) AS match_count FROM Match INNER JOIN League ON Match.league_id = League.id WHERE League.name = 'Belgium Jupiler League' AND SUBSTR(Match.date, 1, 7) = '2009-04'
```

**生成结果**:
```
❌ 执行失败
```

**预期SQL**:
```sql
SELECT
  COUNT(`t2`.`id`)
FROM `League` AS `t1`
INNER JOIN `Match` AS `t2`
  ON `t1`.`id` = `t2`.`league_id`
WHERE
  `t1`.`name` = 'Belgium Jupiler League' AND SUBSTR(`t2`.`date`, 1, 7) = '2009-04'
```

**预期结果**:
```json
[
  {
    "COUNT(`t2`.`id`)": 36
  }
]
```
---

#### ID:1107 | european_football_2

**问题**: When was the first time did Kevin Constant have his highest crossing score? Give the date.

**证据**: Kevin Constant refers to player_name = 'Kevin Constant'; highest crossing score refers to MAX(crossing)

**生成SQL**:
```sql
SELECT pa.date FROM Player p JOIN Player_Attributes pa ON p.player_api_id = pa.player_api_id WHERE p.player_name = 'Kevin Constant' AND pa.crossing = (SELECT MAX(pa2.crossing) FROM Player p2 JOIN Player_Attributes pa2 ON p2.player_api_id = pa2.player_api_id WHERE p2.player_name = 'Kevin Constant') ORDER BY pa.date ASC LIMIT 1
```

**生成结果**:
```json
[
  {
    "date": "2013-02-15 00:00:00"
  }
]
```
**预期SQL**:
```sql
SELECT `date` FROM (SELECT `t2`.`crossing`, `t2`.`date` FROM `Player` AS `t1` INNER JOIN `Player_Attributes` AS `t2` ON `t1`.`player_fifa_api_id` = `t2`.`player_fifa_api_id` WHERE `t1`.`player_name` = 'Kevin Constant' ORDER BY `t2`.`crossing` DESC) AS `subquery` ORDER BY `date` DESC LIMIT 1
```

**预期结果**:
```json
[
  {
    "date": "2016-04-21 00:00:00"
  }
]
```
---

#### ID:1113 | european_football_2

**问题**: For the team "Hannover 96", what was its defence aggression class on 2015/9/10?

**证据**: "Hannover 96" refers to team_long_name = 'Hannover 96'; on 2015/9/10 refers to date LIKE '2015-09-10%';

**生成SQL**:
```sql
SELECT TA.defence_aggression_class FROM Team T INNER JOIN Team_Attributes TA ON T.team_api_id = TA.team_api_id WHERE T.team_long_name = 'Hannover 96' AND TA.date LIKE '2015-09-10%'
```

**生成结果**:
```
❌ 执行失败
```

**预期SQL**:
```sql
SELECT
  `t2`.`defenceAggressionClass`
FROM `Team` AS `t1`
INNER JOIN `Team_Attributes` AS `t2`
  ON `t1`.`team_api_id` = `t2`.`team_api_id`
WHERE
  `t1`.`team_long_name` = 'Hannover 96' AND `t2`.`date` LIKE '2015-09-10%'
```

**预期结果**:
```json
[
  {
    "defenceAggressionClass": "Press"
  }
]
```
---

#### ID:1135 | european_football_2

**问题**: Please provide top four football players' IDs who are among the lowest potential players and prefer to use the right foot when attacking.

**证据**: lowest potential players refers to MIN(potential); prefer to use the right foot when attacking refers to preferred_foot = 'right'

**生成SQL**:
```sql
SELECT Player.id FROM Player INNER JOIN Player_Attributes ON Player.player_api_id = Player_Attributes.player_api_id WHERE Player_Attributes.preferred_foot = 'right' ORDER BY Player_Attributes.potential ASC LIMIT 4
```

**生成结果**:
```json
[
  {
    "id": 7909
  },
  {
    "id": 7909
  },
  {
    "id": 3963
  },
  {
    "id": 3963
  }
]
```
**预期SQL**:
```sql
SELECT
  `id`
FROM `Player_Attributes`
WHERE
  `preferred_foot` = 'right'
ORDER BY
  `potential` ASC
LIMIT 4
```

**预期结果**:
```json
[
  {
    "id": 132235
  },
  {
    "id": 132236
  },
  {
    "id": 66214
  },
  {
    "id": 66213
  }
]
```
---

#### ID:1136 | european_football_2

**问题**: How many players had the highest potential score for crossing that preferred to use their left foots while attacking?

**证据**: highest potential score for crossing refers to MAX(crossing); preferred to use their left foots while attacking refers to preferred_foot = 'left'

**生成SQL**:
```sql
SELECT COUNT(DISTINCT player_api_id) FROM Player_Attributes WHERE crossing = (SELECT MAX(crossing) FROM Player_Attributes) AND preferred_foot = 'left'
```

**生成结果**:
```json
[
  {
    "COUNT(DISTINCT player_api_id)": 2
  }
]
```
**预期SQL**:
```sql
SELECT
  COUNT(`t1`.`id`)
FROM `Player_Attributes` AS `t1`
WHERE
  `t1`.`preferred_foot` = 'left'
  AND `t1`.`crossing` = (
    SELECT
      MAX(`crossing`)
    FROM `Player_Attributes`
  )
```

**预期结果**:
```json
[
  {
    "COUNT(`t1`.`id`)": 3
  }
]
```
---

#### ID:1141 | european_football_2

**问题**: Does the KSV Cercle Brugge team have a slow, balanced or fast speed class?

**证据**: KSV Cercle Brugge refers to team_long_name = 'KSV Cercle Brugge'; speed class refers to buildUpPlaySpeedClass

**生成SQL**:
```sql
SELECT ta.buildUpPlaySpeedClass FROM Team t INNER JOIN Team_Attributes ta ON t.team_api_id = ta.team_api_id WHERE t.team_long_name = 'KSV Cercle Brugge' ORDER BY ta.date DESC LIMIT 1
```

**生成结果**:
```json
[
  {
    "buildUpPlaySpeedClass": "Balanced"
  }
]
```
**预期SQL**:
```sql
SELECT DISTINCT
  `t1`.`buildUpPlaySpeedClass`
FROM `Team_Attributes` AS `t1`
INNER JOIN `Team` AS `t2`
  ON `t1`.`team_api_id` = `t2`.`team_api_id`
WHERE
  `t2`.`team_long_name` = 'KSV Cercle Brugge'
```

**预期结果**:
```json
[
  {
    "buildUpPlaySpeedClass": "Balanced"
  },
  {
    "buildUpPlaySpeedClass": "Fast"
  }
]
```
---

#### ID:1146 | european_football_2

**问题**: Please provide the full name of the away team that scored the most goals.

**证据**: full name refers to team_long_name; away team refers to away_team_api_id; scored the most goals refers to MAX(away_team_goal)

**生成SQL**:
```sql
SELECT team_long_name FROM Team WHERE team_api_id = (SELECT away_team_api_id FROM Match ORDER BY away_team_goal DESC LIMIT 1)
```

**生成结果**:
```
❌ 执行失败
```

**预期SQL**:
```sql
SELECT
  `t2`.`team_long_name`
FROM `Match` AS `t1`
INNER JOIN `Team` AS `t2`
  ON `t1`.`away_team_api_id` = `t2`.`team_api_id`
ORDER BY
  `t1`.`away_team_goal` DESC
LIMIT 1
```

**预期结果**:
```json
[
  {
    "team_long_name": "Paris Saint-Germain"
  }
]
```
---

#### ID:1148 | european_football_2

**问题**: What is the percentage of players that are under 180 cm who have an overall strength of more than 70?

**证据**: percentage refers to DIVIDE(COUNT(height < 180 AND overall_rating > 70),COUNT(id)) * 100

**生成SQL**:
```sql
SELECT (CAST(COUNT(DISTINCT CASE WHEN p.height < 180 AND pa.overall_rating > 70 THEN p.id END) AS DOUBLE) / CAST(COUNT(DISTINCT p.id) AS DOUBLE)) * 100 AS percentage FROM Player p LEFT JOIN Player_Attributes pa ON p.player_api_id = pa.player_api_id
```

**生成结果**:
```json
[
  {
    "percentage": 17.585895117540687
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST(COUNT(CASE WHEN `t2`.`overall_rating` > 70 AND `t1`.`height` < 180 THEN `t1`.`id` ELSE NULL END) AS DOUBLE) * 100 / COUNT(`t1`.`id`) AS `percent`
FROM `Player` AS `t1`
INNER JOIN `Player_Attributes` AS `t2`
  ON `t1`.`player_api_id` = `t2`.`player_api_id`
```

**预期结果**:
```json
[
  {
    "percent": 13.944511197255462
  }
]
```
---

#### ID:865 | formula_1

**问题**: For all the drivers who finished the game in race No. 592, who is the oldest?

**证据**: drivers who finished the race refers to time is not empty (i.e. time IS NOT NULL); race number refers to raceId; date of birth refers to drivers.dob; The larger the birthday value, the younger the person is, and vice versa;

**生成SQL**:
```sql
SELECT d.forename, d.surname, d.dob FROM results r INNER JOIN drivers d ON r.driverId = d.driverId WHERE r.raceId = 592 AND r.time IS NOT NULL ORDER BY d.dob ASC LIMIT 1
```

**生成结果**:
```json
[
  {
    "forename": "Jean-Pierre",
    "surname": "Beltoise",
    "dob": "1937-04-26"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T1`.`forename`,
  `T1`.`surname`
FROM `drivers` AS `T1`
INNER JOIN `results` AS `T2`
  ON `T2`.`driverId` = `T1`.`driverId`
WHERE
  `T2`.`raceId` = 592 AND NOT `T2`.`time` IS NULL AND NOT `T1`.`dob` IS NULL
ORDER BY
  `T1`.`dob` ASC
LIMIT 1
```

**预期结果**:
```json
[
  {
    "forename": "Jean-Pierre",
    "surname": "Beltoise"
  }
]
```
---

#### ID:866 | formula_1

**问题**: Who was the player that got the lap time of 0:01:27 in the race No. 161? Show his introduction website.

**证据**: player and driver are synonyms; the lap time of 0:0M:SS refers to lapTime.time LIKE 'M:SS%';race number refers to raceId; introduction website of the drivers refers to url;

**生成SQL**:
```sql
SELECT drivers.url FROM lapTimes INNER JOIN drivers ON lapTimes.driverId = drivers.driverId WHERE lapTimes.raceId = 161 AND lapTimes.time LIKE '0:01:27%'
```

**生成结果**:
(空结果)

**预期SQL**:
```sql
SELECT DISTINCT
  `T2`.`forename`,
  `T2`.`surname`,
  `T2`.`url`
FROM `lapTimes` AS `T1`
INNER JOIN `drivers` AS `T2`
  ON `T2`.`driverId` = `T1`.`driverId`
WHERE
  `T1`.`raceId` = 161 AND `T1`.`time` LIKE '1:27%'
```

**预期结果**:
```json
[
  {
    "forename": "David",
    "surname": "Coulthard",
    "url": "http://en.wikipedia.org/wiki/David_Coulthard"
  },
  {
    "forename": "Jarno",
    "surname": "Trulli",
    "url": "http://en.wikipedia.org/wiki/Jarno_Trulli"
  },
  {
    "forename": "Jenson",
    "surname": "Button",
    "url": "http://en.wikipedia.org/wiki/Jenson_Button"
  },
  {
    "forename": "Rubens",
    "surname": "Barrichello",
    "url": "http://en.wikipedia.org/wiki/Rubens_Barrichello"
  },
  {
    "forename": "Ralf",
    "surname": "Schumacher",
    "url": "http://en.wikipedia.org/wiki/Ralf_Schumacher"
  }
]
```
---

#### ID:877 | formula_1

**问题**: For all the drivers who finished the game in race No. 872, who is the youngest?

**证据**: race number refers to raceId; drivers who finished the race refers to time has value; the youngest is a driver where MAX(dob);

**生成SQL**:
```sql
SELECT d.driverId, d.forename, d.surname FROM results r INNER JOIN drivers d ON r.driverId = d.driverId WHERE r.raceId = 872 AND r.time IS NOT NULL ORDER BY d.dob DESC LIMIT 1
```

**生成结果**:
```json
[
  {
    "driverId": 815,
    "forename": "Sergio",
    "surname": "Pérez"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T1`.`forename`,
  `T1`.`surname`
FROM `drivers` AS `T1`
INNER JOIN `results` AS `T2`
  ON `T2`.`driverId` = `T1`.`driverId`
WHERE
  `T2`.`raceId` = 872 AND NOT `T2`.`time` IS NULL
ORDER BY
  `T1`.`dob` DESC
LIMIT 1
```

**预期结果**:
```json
[
  {
    "forename": "Sergio",
    "surname": "Pérez"
  }
]
```
---

#### ID:881 | formula_1

**问题**: For the drivers who took part in the race in 1983/7/16, what's their race completion rate?

**证据**: DIVIDE(COUNT(driverid when time has value ), (COUNT(driverid )) as percentage; in 1983/7/16 refers to when date = '1983-07-16'

**生成SQL**:
```sql
SELECT CAST(COUNT(DISTINCT CASE WHEN r.time IS NOT NULL THEN r.driverId END) AS DOUBLE) / CAST(COUNT(DISTINCT r.driverId) AS DOUBLE) AS completion_rate FROM results r INNER JOIN races ra ON r.raceId = ra.raceId WHERE ra.date = '1983-07-16'
```

**生成结果**:
```json
[
  {
    "completion_rate": 0.1724137931034483
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST(COUNT(CASE WHEN NOT `T2`.`time` IS NULL THEN `T2`.`driverId` END) AS DOUBLE) * 100 / COUNT(`T2`.`driverId`)
FROM `races` AS `T1`
INNER JOIN `results` AS `T2`
  ON `T2`.`raceId` = `T1`.`raceId`
WHERE
  `T1`.`date` = '1983-07-16'
```

**预期结果**:
```json
[
  {
    "CAST(COUNT(CASE WHEN NOT `T2`.`time` IS NULL THEN `T2`.`driverId` END) AS DOUBLE) * 100 / COUNT(`T2`.`driverId`)": 17.24137931034483
  }
]
```
---

#### ID:894 | formula_1

**问题**: What is the best lap time recorded? List the driver and race with such recorded lap time.

**证据**: the best lap time refers to min(milliseconds); List the driver refers to drivers.forename and drivers.surname; List the race refers to races.name

**生成SQL**:
```sql
SELECT d.forename, d.surname, r.name FROM lapTimes lt INNER JOIN drivers d ON lt.driverId = d.driverId INNER JOIN races r ON lt.raceId = r.raceId WHERE lt.milliseconds = (SELECT MIN(milliseconds) FROM lapTimes);
```

**生成结果**:
```json
[
  {
    "forename": "Lewis",
    "surname": "Hamilton",
    "name": "Austrian Grand Prix"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T2`.`milliseconds`,
  `T1`.`forename`,
  `T1`.`surname`,
  `T3`.`name`
FROM `drivers` AS `T1`
INNER JOIN `lapTimes` AS `T2`
  ON `T1`.`driverId` = `T2`.`driverId`
INNER JOIN `races` AS `T3`
  ON `T2`.`raceId` = `T3`.`raceId`
ORDER BY
  `T2`.`milliseconds` ASC
LIMIT 1
```

**预期结果**:
```json
[
  {
    "milliseconds": 67411,
    "forename": "Lewis",
    "surname": "Hamilton",
    "name": "Austrian Grand Prix"
  }
]
```
---

#### ID:897 | formula_1

**问题**: Name the driver with the most winning. Mention his nationality and what is his maximum point scores.

**证据**: Full name of the driver refers to drivers.forename and drivers.surname; the most winning refers to MAX(COUNT(wins)); average point scores refers to MAX(points);

**生成SQL**:
```sql
SELECT CONCAT(d.forename, ' ', d.surname) AS full_name, d.nationality, top_driver.max_points FROM drivers d INNER JOIN (SELECT driverId, MAX(points) AS max_points FROM driverStandings GROUP BY driverId ORDER BY SUM(wins) DESC LIMIT 1) AS top_driver ON d.driverId = top_driver.driverId
```

**生成结果**:
```json
[
  {
    "full_name": "Michael Schumacher",
    "nationality": "German",
    "max_points": 148.0
  }
]
```
**预期SQL**:
```sql
SELECT
  `T1`.`forename`,
  `T1`.`surname`,
  `T1`.`nationality`,
  MAX(`T2`.`points`)
FROM `drivers` AS `T1`
INNER JOIN `driverStandings` AS `T2`
  ON `T2`.`driverId` = `T1`.`driverId`
WHERE
  `T2`.`wins` >= 1
GROUP BY
  `T1`.`forename`,
  `T1`.`surname`,
  `T1`.`nationality`
ORDER BY
  COUNT(`T2`.`wins`) DESC
LIMIT 1
```

**预期结果**:
```json
[
  {
    "forename": "Michael",
    "surname": "Schumacher",
    "nationality": "German",
    "MAX(`T2`.`points`)": 148.0
  }
]
```
---

#### ID:906 | formula_1

**问题**: Which was Lewis Hamilton first race? What was his points recorded for his first race event?

**证据**: first race refers to min(Year); Lewis Hamiltonrefers to the full name of the driver; Full name of the driver refers to drivers.forename and drivers.surname;

**生成SQL**:
```sql
SELECT r.name, r1.points FROM results r1 JOIN races r ON r1.raceId = r.raceId JOIN drivers d ON r1.driverId = d.driverId WHERE d.forename = 'Lewis' AND d.surname = 'Hamilton' AND r.year = (SELECT MIN(r2.year) FROM results r2 JOIN races r3 ON r2.raceId = r3.raceId JOIN drivers d2 ON r2.driverId = d2.driverId WHERE d2.forename = 'Lewis' AND d2.surname = 'Hamilton') ORDER BY r.date LIMIT 1
```

**生成结果**:
```
❌ 执行失败
```

**预期SQL**:
```sql
SELECT
  `T1`.`name`,
  `T2`.`points`
FROM `races` AS `T1`
INNER JOIN `driverStandings` AS `T2`
  ON `T2`.`raceId` = `T1`.`raceId`
INNER JOIN `drivers` AS `T3`
  ON `T3`.`driverId` = `T2`.`driverId`
WHERE
  `T3`.`forename` = 'Lewis' AND `T3`.`surname` = 'Hamilton'
ORDER BY
  `T1`.`year` ASC
LIMIT 1
```

**预期结果**:
```json
[
  {
    "name": "Malaysian Grand Prix",
    "points": 14.0
  }
]
```
---

#### ID:928 | formula_1

**问题**: Which driver ranked the first in the Canadian Grand Prix in 2007? Please give his reference name.

**证据**: reference name refers to driverRef; Canadian Grand Prix refers to races.name = 'Canadian Grand Prix';

**生成SQL**:
```sql
SELECT d.driverRef FROM results r INNER JOIN races ra ON r.raceId = ra.raceId INNER JOIN drivers d ON r.driverId = d.driverId WHERE ra.year = 2007 AND ra.name = 'Canadian Grand Prix' AND r.position = 1
```

**生成结果**:
```json
[
  {
    "driverRef": "hamilton"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T3`.`forename`,
  `T3`.`surname`,
  `T3`.`driverRef`
FROM `races` AS `T1`
INNER JOIN `results` AS `T2`
  ON `T2`.`raceId` = `T1`.`raceId`
INNER JOIN `drivers` AS `T3`
  ON `T3`.`driverId` = `T2`.`driverId`
WHERE
  `T1`.`name` = 'Canadian Grand Prix' AND `T2`.`rank` = 1 AND `T1`.`year` = 2007
```

**预期结果**:
```json
[
  {
    "forename": "Fernando",
    "surname": "Alonso",
    "driverRef": "alonso"
  }
]
```
---

#### ID:963 | formula_1

**问题**: How many French drivers who obtain the laptime less than 02:00.00?

**证据**: lap time less than 02:00.00 refers to seconds < 120;

**生成SQL**:
```sql
SELECT COUNT(DISTINCT d.driverId) FROM drivers d INNER JOIN lapTimes lt ON d.driverId = lt.driverId WHERE d.nationality = 'French' AND lt.milliseconds < 120000
```

**生成结果**:
```json
[
  {
    "COUNT(DISTINCT d.driverId)": 9
  }
]
```
**预期SQL**:
```sql
SELECT
  COUNT(`T1`.`driverId`)
FROM `drivers` AS `T1`
INNER JOIN `lapTimes` AS `T2`
  ON `T1`.`driverId` = `T2`.`driverId`
WHERE
  `T1`.`nationality` = 'French'
  AND (
    CAST(SUBSTR(`T2`.`time`, 1, 2) AS SIGNED) * 60 + CAST(SUBSTR(`T2`.`time`, 4, 2) AS SIGNED) + CAST(SUBSTR(`T2`.`time`, 7, 2) AS DOUBLE) / 1000
  ) < 120
```

**预期结果**:
```json
[
  {
    "COUNT(`T1`.`driverId`)": 23295
  }
]
```
---

#### ID:972 | formula_1

**问题**: Which drivers who were born in 1971 and has the fastest lap time on the race? Give id and code of these drivers.

**证据**: born in 1971 refers to year(dob) = 1971; has the fastest lap time refers to fastestLapTime has values

**生成SQL**:
```sql
SELECT DISTINCT d.driverId, d.code FROM drivers d INNER JOIN results r ON d.driverId = r.driverId WHERE YEAR(d.dob) = 1971 AND r.fastestLapTime IS NOT NULL
```

**生成结果**:
```json
[
  {
    "driverId": 14,
    "code": "COU"
  },
  {
    "driverId": 35,
    "code": "VIL"
  },
  {
    "driverId": 37,
    "code": "DLR"
  },
  {
    "driverId": 69,
    "code": "BAD"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T2`.`driverId`,
  `T2`.`code`
FROM `results` AS `T1`
INNER JOIN `drivers` AS `T2`
  ON `T1`.`driverId` = `T2`.`driverId`
WHERE
  DATE_FORMAT(CAST(`T2`.`dob` AS DATETIME), '%Y') = '1971'
  AND NOT `T1`.`fastestLapTime` IS NULL
```

**预期结果**:
```json
[
  {
    "driverId": 14,
    "code": "COU"
  },
  {
    "driverId": 14,
    "code": "COU"
  },
  {
    "driverId": 14,
    "code": "COU"
  },
  {
    "driverId": 14,
    "code": "COU"
  },
  {
    "driverId": 14,
    "code": "COU"
  }
]
```
---

#### ID:989 | formula_1

**问题**: Who is the champion of the Canadian Grand Prix in 2008? Indicate his finish time.

**证据**: Only the time of the champion shows in the format of "hour: minutes: seconds.millionsecond";

**生成SQL**:
```sql
SELECT d.forename, d.surname, r.time AS finish_time FROM results r INNER JOIN drivers d ON r.driverId = d.driverId WHERE r.raceId = (SELECT raceId FROM races WHERE year = 2008 AND name = 'Canadian Grand Prix') AND r.position = 1;
```

**生成结果**:
```json
[
  {
    "forename": "Robert",
    "surname": "Kubica",
    "finish_time": "1:36:24.227"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T1`.`time`
FROM `results` AS `T1`
INNER JOIN `races` AS `T2`
  ON `T1`.`raceId` = `T2`.`raceId`
WHERE
  `T2`.`name` = 'Canadian Grand Prix'
  AND `T2`.`year` = 2008
  AND `T1`.`time` LIKE '_:%:__.___'
```

**预期结果**:
```json
[
  {
    "time": "1:36:24.227"
  }
]
```
---

#### ID:1002 | formula_1

**问题**: As of the present, what is the full name of the youngest racer? Indicate her nationality and the name of the race to which he/she first joined.

**证据**: full name refers to forename+surname; Youngest racer = MAX(dob)

**生成SQL**:
```sql
SELECT CONCAT(d.forename, ' ', d.surname) AS full_name, d.nationality, (SELECT r.name FROM results res JOIN races r ON res.raceId = r.raceId WHERE res.driverId = d.driverId ORDER BY r.date ASC LIMIT 1) AS first_race_name FROM drivers d WHERE d.driverId = (SELECT driverId FROM drivers ORDER BY dob DESC LIMIT 1)
```

**生成结果**:
```json
[
  {
    "full_name": "Lance Stroll",
    "nationality": "Canadian",
    "first_race_name": "Chinese Grand Prix"
  }
]
```
**预期SQL**:
```sql
SELECT `T1`.`forename`, `T1`.`surname`, `T1`.`nationality`, `T3`.`name` FROM `drivers` AS `T1` INNER JOIN `driverStandings` AS `T2` ON `T1`.`driverId` = `T2`.`driverId` INNER JOIN `races` AS `T3` ON `T2`.`raceId` = `T3`.`raceId` ORDER BY `T1`.`dob` DESC LIMIT 1
```

**预期结果**:
```json
[
  {
    "forename": "Lance",
    "surname": "Stroll",
    "nationality": "Canadian",
    "name": "Chinese Grand Prix"
  }
]
```
---

#### ID:726 | superhero

**问题**: Rank heroes published by Marvel Comics by their height in descending order.

**证据**: name refers to superhero_name; the tallest hero refers to MAX(height_cm); published by Marvel Comics refers to publisher_name = 'Marvel Comics'

**生成SQL**:
```sql
SELECT superhero.superhero_name, superhero.height_cm FROM superhero INNER JOIN publisher ON superhero.publisher_id = publisher.id WHERE publisher.publisher_name = 'Marvel Comics' ORDER BY superhero.height_cm DESC
```

**生成结果**:
```json
[
  {
    "superhero_name": "Surtur",
    "height_cm": 30480
  },
  {
    "superhero_name": "Ymir",
    "height_cm": 30480
  },
  {
    "superhero_name": "Bloodwraith",
    "height_cm": 3050
  },
  {
    "superhero_name": "Utgard-Loki",
    "height_cm": 1520
  },
  {
    "superhero_name": "Fin Fang Foom",
    "height_cm": 975
  }
]
```
**预期SQL**:
```sql
SELECT
  `superhero_name`,
  `height_cm`,
  RANK() OVER (ORDER BY `height_cm` DESC) AS `HeightRank`
FROM `superhero`
INNER JOIN `publisher`
  ON `superhero`.`publisher_id` = `publisher`.`id`
WHERE
  `publisher`.`publisher_name` = 'Marvel Comics'
```

**预期结果**:
```json
[
  {
    "superhero_name": "Surtur",
    "height_cm": 30480,
    "HeightRank": 1
  },
  {
    "superhero_name": "Ymir",
    "height_cm": 30480,
    "HeightRank": 1
  },
  {
    "superhero_name": "Bloodwraith",
    "height_cm": 3050,
    "HeightRank": 3
  },
  {
    "superhero_name": "Utgard-Loki",
    "height_cm": 1520,
    "HeightRank": 4
  },
  {
    "superhero_name": "Fin Fang Foom",
    "height_cm": 975,
    "HeightRank": 5
  }
]
```
---

#### ID:728 | superhero

**问题**: Rank superheroes from Marvel Comics by their eye color popularity, starting with the most common color.

**证据**: the superheroes from Marvel Comics refers to publisher_name = 'Marvel Comics'; most common color refers to COUNT(superhero.id) DESC;

**生成SQL**:
```sql
SELECT colour.colour, COUNT(superhero.id) as popularity FROM superhero INNER JOIN publisher ON superhero.publisher_id = publisher.id INNER JOIN colour ON superhero.eye_colour_id = colour.id WHERE publisher.publisher_name = 'Marvel Comics' GROUP BY colour.id, colour.colour ORDER BY popularity DESC
```

**生成结果**:
```json
[
  {
    "colour": "Blue",
    "popularity": 126
  },
  {
    "colour": "Brown",
    "popularity": 89
  },
  {
    "colour": "No Colour",
    "popularity": 47
  },
  {
    "colour": "Green",
    "popularity": 40
  },
  {
    "colour": "Red",
    "popularity": 31
  }
]
```
**预期SQL**:
```sql
SELECT
  `colour`.`colour` AS `EyeColor`,
  COUNT(`superhero`.`id`) AS `Count`,
  RANK() OVER (ORDER BY COUNT(`superhero`.`id`) DESC) AS `PopularityRank`
FROM `superhero`
INNER JOIN `colour`
  ON `superhero`.`eye_colour_id` = `colour`.`id`
INNER JOIN `publisher`
  ON `superhero`.`publisher_id` = `publisher`.`id`
WHERE
  `publisher`.`publisher_name` = 'Marvel Comics'
GROUP BY
  `colour`.`colour`
```

**预期结果**:
```json
[
  {
    "EyeColor": "Blue",
    "Count": 126,
    "PopularityRank": 1
  },
  {
    "EyeColor": "Brown",
    "Count": 89,
    "PopularityRank": 2
  },
  {
    "EyeColor": "No Colour",
    "Count": 47,
    "PopularityRank": 3
  },
  {
    "EyeColor": "Green",
    "Count": 40,
    "PopularityRank": 4
  },
  {
    "EyeColor": "Red",
    "Count": 31,
    "PopularityRank": 5
  }
]
```
---

#### ID:732 | superhero

**问题**: Which publisher published the slowest superhero?

**证据**: the slowest superhero refers to attribute_name = 'Speed' where MIN(attribute_value); publisher refers to publisher_name

**生成SQL**:
```sql
SELECT DISTINCT publisher.publisher_name FROM hero_attribute ha INNER JOIN attribute a ON ha.attribute_id = a.id INNER JOIN superhero s ON ha.hero_id = s.id INNER JOIN publisher p ON s.publisher_id = p.id WHERE a.attribute_name = 'Speed' AND ha.attribute_value = (SELECT MIN(ha2.attribute_value) FROM hero_attribute ha2 INNER JOIN attribute a2 ON ha2.attribute_id = a2.id WHERE a2.attribute_name = 'Speed')
```

**生成结果**:
```
❌ 执行失败
```

**预期SQL**:
```sql
SELECT
  `T2`.`publisher_name`
FROM `superhero` AS `T1`
INNER JOIN `publisher` AS `T2`
  ON `T1`.`publisher_id` = `T2`.`id`
INNER JOIN `hero_attribute` AS `T3`
  ON `T1`.`id` = `T3`.`hero_id`
INNER JOIN `attribute` AS `T4`
  ON `T3`.`attribute_id` = `T4`.`id`
WHERE
  `T4`.`attribute_name` = 'Speed'
ORDER BY
  `T3`.`attribute_value`
LIMIT 1
```

**预期结果**:
```json
[
  {
    "publisher_name": "Marvel Comics"
  }
]
```
---

#### ID:736 | superhero

**问题**: Who is the dumbest superhero?

**证据**: the dumbest superhero refers to MIN(attribute_value) where attribute_name = 'Intelligence'

**生成SQL**:
```sql
SELECT s.superhero_name FROM superhero s INNER JOIN hero_attribute ha ON s.id = ha.hero_id INNER JOIN attribute a ON ha.attribute_id = a.id WHERE a.attribute_name = 'Intelligence' AND ha.attribute_value = (SELECT MIN(ha2.attribute_value) FROM hero_attribute ha2 INNER JOIN attribute a2 ON ha2.attribute_id = a2.id WHERE a2.attribute_name = 'Intelligence')
```

**生成结果**:
```json
[
  {
    "superhero_name": "Ammo"
  },
  {
    "superhero_name": "Ando Masahashi"
  },
  {
    "superhero_name": "Jack-Jack"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T1`.`superhero_name`
FROM `superhero` AS `T1`
INNER JOIN `hero_attribute` AS `T2`
  ON `T1`.`id` = `T2`.`hero_id`
INNER JOIN `attribute` AS `T3`
  ON `T2`.`attribute_id` = `T3`.`id`
WHERE
  `T3`.`attribute_name` = 'Intelligence'
ORDER BY
  `T2`.`attribute_value`
LIMIT 1
```

**预期结果**:
```json
[
  {
    "superhero_name": "Ammo"
  }
]
```
---

#### ID:758 | superhero

**问题**: Provide the hair colour of the human superhero who is 185 cm tall.

**证据**: 185 cm tall refers to height_cm = 185; human superhero refers to race = 'human'; hair colour refers to colour where hair_colour_id = colour.id;

**生成SQL**:
```sql
SELECT colour.colour FROM superhero INNER JOIN race ON superhero.race_id = race.id INNER JOIN colour ON superhero.hair_colour_id = colour.id WHERE superhero.height_cm = 185 AND race.race = 'human'
```

**生成结果**:
```json
[
  {
    "colour": "Blond"
  },
  {
    "colour": "Brown"
  },
  {
    "colour": "Brown"
  },
  {
    "colour": "Black"
  },
  {
    "colour": "Black"
  }
]
```
**预期SQL**:
```sql
SELECT DISTINCT
  `T3`.`colour`
FROM `superhero` AS `T1`
INNER JOIN `race` AS `T2`
  ON `T1`.`race_id` = `T2`.`id`
INNER JOIN `colour` AS `T3`
  ON `T1`.`hair_colour_id` = `T3`.`id`
WHERE
  `T1`.`height_cm` = 185 AND `T2`.`race` = 'Human'
```

**预期结果**:
```json
[
  {
    "colour": "Blond"
  },
  {
    "colour": "Brown"
  },
  {
    "colour": "Black"
  },
  {
    "colour": "Brown/White"
  },
  {
    "colour": "No Colour"
  }
]
```
---

#### ID:766 | superhero

**问题**: What is the hero's full name with the highest attribute in strength?

**证据**: highest attribute in strength refers to MAX(attribute_value) WHERE attribute_name = 'strength';

**生成SQL**:
```sql
SELECT s.full_name FROM superhero s INNER JOIN hero_attribute ha ON s.id = ha.hero_id INNER JOIN attribute a ON ha.attribute_id = a.id WHERE a.attribute_name = 'strength' AND ha.attribute_value = (SELECT MAX(ha2.attribute_value) FROM hero_attribute ha2 INNER JOIN attribute a2 ON ha2.attribute_id = a2.id WHERE a2.attribute_name = 'strength')
```

**生成结果**:
```json
[
  {
    "full_name": "Richard Milhouse Jones"
  },
  {
    "full_name": "Abraxas"
  },
  {
    "full_name": "-"
  },
  {
    "full_name": "-"
  },
  {
    "full_name": "En Sabah Nur"
  }
]
```
**预期SQL**:
```sql
SELECT `T1`.`full_name` FROM `superhero` AS `T1` INNER JOIN `hero_attribute` AS `T2` ON `T1`.`id` = `T2`.`hero_id` INNER JOIN `attribute` AS `T3` ON `T2`.`attribute_id` = `T3`.`id` WHERE `T3`.`attribute_name` = 'Strength' ORDER BY `T2`.`attribute_value` DESC LIMIT 1
```

**预期结果**:
```json
[
  {
    "full_name": "Richard Milhouse Jones"
  }
]
```
---

#### ID:794 | superhero

**问题**: Which hero was the fastest?

**证据**: which hero refers to superhero_name; fastest refers to MAX(attribute_value) WHERE attribute_name = 'Speed';

**生成SQL**:
```sql
SELECT s.superhero_name FROM superhero s JOIN hero_attribute ha ON s.id = ha.hero_id JOIN attribute a ON ha.attribute_id = a.id WHERE a.attribute_name = 'Speed' AND ha.attribute_value = (SELECT MAX(ha2.attribute_value) FROM hero_attribute ha2 JOIN attribute a2 ON ha2.attribute_id = a2.id WHERE a2.attribute_name = 'Speed')
```

**生成结果**:
```json
[
  {
    "superhero_name": "Air-Walker"
  },
  {
    "superhero_name": "Angela"
  },
  {
    "superhero_name": "Ardina"
  },
  {
    "superhero_name": "Aurora"
  },
  {
    "superhero_name": "Ben 10"
  }
]
```
**预期SQL**:
```sql
SELECT `T1`.`superhero_name` FROM `superhero` AS `T1` INNER JOIN `hero_attribute` AS `T2` ON `T1`.`id` = `T2`.`hero_id` INNER JOIN `attribute` AS `T3` ON `T2`.`attribute_id` = `T3`.`id`WHERE `T3`.`attribute_name` = 'Speed' AND `T2`.`attribute_value` = (SELECT MAX(`attribute_value`) FROM `hero_attribute` AS `T2b` WHERE `T2b`.`attribute_id` = `T3`.`id` ) LIMIT 1
```

**预期结果**:
```json
[
  {
    "superhero_name": "Air-Walker"
  }
]
```
---

#### ID:798 | superhero

**问题**: What is the publisher for Hawkman, Karate Kid and Speedy?

**证据**: publisher refers to publisher_name; Hawkman refers to superhero_name = 'Hawkman'; Karate Kid refers to superhero_name = 'Karate Kid'; Speedy refers to superhero_name = 'Speedy';

**生成SQL**:
```sql
SELECT s.superhero_name, p.publisher_name FROM superhero s INNER JOIN publisher p ON s.publisher_id = p.id WHERE s.superhero_name IN ('Hawkman', 'Karate Kid', 'Speedy');
```

**生成结果**:
```json
[
  {
    "superhero_name": "Hawkman",
    "publisher_name": "DC Comics"
  },
  {
    "superhero_name": "Karate Kid",
    "publisher_name": "DC Comics"
  },
  {
    "superhero_name": "Speedy",
    "publisher_name": "DC Comics"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T2`.`publisher_name`
FROM `superhero` AS `T1`
INNER JOIN `publisher` AS `T2`
  ON `T1`.`publisher_id` = `T2`.`id`
WHERE
  `T1`.`superhero_name` IN ('Hawkman', 'Karate Kid', 'Speedy')
```

**预期结果**:
```json
[
  {
    "publisher_name": "DC Comics"
  },
  {
    "publisher_name": "DC Comics"
  },
  {
    "publisher_name": "DC Comics"
  }
]
```
---

#### ID:565 | codebase_community

**问题**: User No.23853 gave a comment to a post at 9:08:18 on 2013/7/12, was that post well-finished?

**证据**: user no. 23853 refers to UserId = '23853'; at 9:08:18 on 2013/7/12 refers to CreationDate = '2013-07-12 09:08:18.0'; not well-finished refers to ClosedDate IS NULL and vice versa

**生成SQL**:
```sql
SELECT CASE WHEN p.ClosedDate IS NULL THEN 'Not well-finished' ELSE 'Well-finished' END AS finish_status FROM comments c INNER JOIN posts p ON c.PostId = p.Id WHERE c.UserId = 23853 AND c.CreationDate = '2013-07-12 09:08:18'
```

**生成结果**:
```json
[
  {
    "finish_status": "Well-finished"
  }
]
```
**预期SQL**:
```sql
SELECT
  CASE
    WHEN `T2`.`ClosedDate` IS NULL
    THEN 'NOT well-finished'
    ELSE 'well-finished'
  END AS `resylt`
FROM `comments` AS `T1`
INNER JOIN `posts` AS `T2`
  ON `T1`.`PostId` = `T2`.`Id`
WHERE
  `T1`.`UserId` = 23853 AND `T1`.`CreationDate` = '2013-07-12 09:08:18.0'
```

**预期结果**:
```json
[
  {
    "resylt": "well-finished"
  }
]
```
---

#### ID:581 | codebase_community

**问题**: Who is the owner of the post titled 'Open source tools for visualizing multi-dimensional data?'

**证据**: 'Open source tools for visualizing multi-dimensional data' is the Title of Post; owner refers to DisplayName;

**生成SQL**:
```sql
SELECT OwnerDisplayName FROM posts WHERE Title = 'Open source tools for visualizing multi-dimensional data';
```

**生成结果**:
(空结果)

**预期SQL**:
```sql
SELECT
  `T2`.`DisplayName`
FROM `posts` AS `T1`
INNER JOIN `users` AS `T2`
  ON `T1`.`OwnerUserId` = `T2`.`Id`
WHERE
  `T1`.`Title` = 'Open source tools for visualizing multi-dimensional data?'
```

**预期结果**:
```json
[
  {
    "DisplayName": "Paul"
  }
]
```
---

#### ID:584 | codebase_community

**问题**: Write all the comments left by users who edited the post titled 'Why square the difference instead of taking the absolute value in standard deviation?'

**证据**: "Why square the difference instead of taking the absolute value in standard deviation?" is the Title of post;

**生成SQL**:
```sql
SELECT * FROM comments WHERE UserId IN (SELECT DISTINCT UserId FROM postHistory WHERE PostId = (SELECT Id FROM posts WHERE Title = 'Why square the difference instead of taking the absolute value in standard deviation?'))
```

**生成结果**:
```json
[
  {
    "Id": 71,
    "PostId": 120,
    "Score": 9,
    "Text": "Nice analogy of euclidean space!",
    "CreationDate": "2010-07-19T21:38:48",
    "UserId": 83,
    "UserDisplayName": null
  },
  {
    "Id": 1916,
    "PostId": 1781,
    "Score": 0,
    "Text": "Yes, that is correct: dilution by a factor of D increases all detection limits by a factor of D as well.  (The matrix interference issue is more difficult to quantify and the general situation is extremely complex.  To simplify this, the conventional model is that a suite of tests on one sample yields a vector (x[1], ..., x[k]) where the x[i] are either real numbers or are intervals of reals, typically with left endpoint at -infinity; an interval identifies a set in which the true value is assumed to lie.)",
    "CreationDate": "2010-08-17T18:20:52",
    "UserId": 919,
    "UserDisplayName": null
  },
  {
    "Id": 1952,
    "PostId": 1781,
    "Score": 0,
    "Text": "As an example, suppose an instrument's detection limit is 1 microgram per Liter (ug/L).  A sample is diluted 10:1 (with great precision, so we don't worry about error here) and the instrument reads \"<1\"; that is, nondetectable, for the diluted sample.  The laboratory infers that the concentration in the sample is less than 10*1 = 10 ug/L and reports it as such; that is, as \"<10\".",
    "CreationDate": "2010-08-18T14:06:17",
    "UserId": 919,
    "UserDisplayName": null
  },
  {
    "Id": 1953,
    "PostId": 1804,
    "Score": 0,
    "Text": "That's a good point, but the result might not be so bad.  What one hopes is that the estimate of M*M is close enough to the true value that the perturbation of eigenvalues is reasonably small.  Thus, by projecting to the eigenspace corresponding to the largest eigenvalues, you achieve only a slight perturbation of the correct solution, still achieving the sought-after dimension reduction.  Perhaps the biggest problem may be algorithmic: since you can no longer assume semidefiniteness, you might need to use a more general-purpose algorithm to find the eigensystem.",
    "CreationDate": "2010-08-18T14:09:39",
    "UserId": 919,
    "UserDisplayName": null
  },
  {
    "Id": 1956,
    "PostId": 1836,
    "Score": 2,
    "Text": "Yes it is!  That's why it's well worth studying: challenges to our intuition are exceptionally educational.  I first learned of this from a clear paper on Carlos Rodriguez' (SUNY Albany) Web page but I couldn't find it this morning: it appears the server is down.  Try Googling \"carlos rogriguez statistics\" later.  (His paper is supposed to be at http://omega.albany.edu/8008/confint.html , but this might be an old URL.)",
    "CreationDate": "2010-08-18T14:51:48",
    "UserId": 919,
    "UserDisplayName": null
  }
]
```
**预期SQL**:
```sql
SELECT
  `T2`.`Comment`
FROM `posts` AS `T1`
INNER JOIN `postHistory` AS `T2`
  ON `T1`.`Id` = `T2`.`PostId`
WHERE
  `T1`.`Title` = 'Why square the difference instead of taking the absolute value in standard deviation?'
```

**预期结果**:
```json
[
  {
    "Comment": ""
  },
  {
    "Comment": ""
  },
  {
    "Comment": ""
  },
  {
    "Comment": "edited title"
  },
  {
    "Comment": "TeXified the formulas."
  }
]
```
---

#### ID:587 | codebase_community

**问题**: Calculate the average view count of each post tagged as 'humor' and list the title and the comment of each post.

**证据**: tagged as  'humor' refers to tag = '<humor>'; comment of the post refers to Text; average view count = AVG(ViewCount)

**生成SQL**:
```sql
SELECT p.Title, c.Text AS Comment, AVG(p.ViewCount) OVER () AS AverageViewCount FROM posts p INNER JOIN comments c ON p.Id = c.PostId WHERE p.Tags LIKE '%<humor>%'
```

**生成结果**:
```json
[
  {
    "Title": "So how many staticians *does* it take to screw in a lightbulb?",
    "Comment": "Probably better asked on meta.  People feel like they have to downvote it because it is an off-topic question.  But then the downvotes make it look like staticians have no sense of humor :(",
    "AverageViewCount": 34804.5789
  },
  {
    "Title": "So how many staticians *does* it take to screw in a lightbulb?",
    "Comment": "@Jason Punyon in particular gets a humorless downvote for removing my \"verboten\" tag! ;-)",
    "AverageViewCount": 34804.5789
  },
  {
    "Title": "What is your favorite \"data analysis\" cartoon?",
    "Comment": "I do have to ask though- how come cartoons are in and jokes are out?",
    "AverageViewCount": 34804.5789
  },
  {
    "Title": "What is your favorite \"data analysis\" cartoon?",
    "Comment": "@sharpie: are jokes out?  We obviously don't want the entire site to be humor, but everyone benefits from a little educational humor in small doses.",
    "AverageViewCount": 34804.5789
  },
  {
    "Title": "What is your favorite \"data analysis\" cartoon?",
    "Comment": "@Sharpie, feel free to close or reopen according to your feelings! I agree with Shane, a bit is ok, but not too much. For example, this question already included a funny cartoon. The jokes question not really a funny joke....",
    "AverageViewCount": 34804.5789
  }
]
```
**预期SQL**:
```sql
SELECT AVG(T2.ViewCount) AS average_view_count, T2.Title, T1.Text FROM comments AS T1 INNER JOIN posts AS T2 ON T2.Id = T1.PostId WHERE T2.Tags = '<humor>' GROUP BY T2.Title, T1.Text
```

**预期结果**:
```json
[
  {
    "average_view_count": 288.0,
    "Title": "So how many staticians *does* it take to screw in a lightbulb?",
    "Text": "Probably better asked on meta.  People feel like they have to downvote it because it is an off-topic question.  But then the downvotes make it look like staticians have no sense of humor :("
  },
  {
    "average_view_count": 288.0,
    "Title": "So how many staticians *does* it take to screw in a lightbulb?",
    "Text": "@Jason Punyon in particular gets a humorless downvote for removing my \"verboten\" tag! ;-)"
  },
  {
    "average_view_count": 64481.0,
    "Title": "What is your favorite \"data analysis\" cartoon?",
    "Text": "I do have to ask though- how come cartoons are in and jokes are out?"
  },
  {
    "average_view_count": 64481.0,
    "Title": "What is your favorite \"data analysis\" cartoon?",
    "Text": "@sharpie: are jokes out?  We obviously don't want the entire site to be humor, but everyone benefits from a little educational humor in small doses."
  },
  {
    "average_view_count": 64481.0,
    "Title": "What is your favorite \"data analysis\" cartoon?",
    "Text": "@Sharpie, feel free to close or reopen according to your feelings! I agree with Shane, a bit is ok, but not too much. For example, this question already included a funny cartoon. The jokes question not really a funny joke...."
  }
]
```
---

#### ID:595 | codebase_community

**问题**: Which user have only one post history per post and having at least 1000 views?

**证据**: having at least 1000 view refers to Views > = 1000; user refers to UserId

**生成SQL**:
```sql
SELECT DISTINCT MIN(ph.UserId) as UserId FROM postHistory ph INNER JOIN posts p ON ph.PostId = p.Id WHERE p.ViewCount >= 1000 GROUP BY ph.PostId HAVING COUNT(*) = 1
```

**生成结果**:
(空结果)

**预期SQL**:
```sql
SELECT
  `T2`.`UserId`
FROM `users` AS `T1`
INNER JOIN `postHistory` AS `T2`
  ON `T1`.`Id` = `T2`.`UserId`
INNER JOIN `posts` AS `T3`
  ON `T2`.`PostId` = `T3`.`Id`
WHERE
  `T3`.`ViewCount` >= 1000
GROUP BY
  `T2`.`UserId`
HAVING
  COUNT(DISTINCT `T2`.`PostHistoryTypeId`) = 1
```

**预期结果**:
```json
[
  {
    "UserId": 57
  },
  {
    "UserId": 61
  },
  {
    "UserId": 80
  },
  {
    "UserId": 124
  },
  {
    "UserId": 139
  }
]
```
---

#### ID:637 | codebase_community

**问题**: State all the tags used by Mark Meckes in his posts that doesn't have comments.

**证据**: used by Mark Meckes refers to DisplayName = 'Mark Meckes'; Doen't have comments refers to CommentCount = 0;

**生成SQL**:
```sql
SELECT DISTINCT posts.Tags FROM posts INNER JOIN users ON posts.OwnerUserId = users.Id WHERE users.DisplayName = 'Mark Meckes' AND posts.CommentCount = 0;
```

**生成结果**:
```json
[
  {
    "Tags": "<books>"
  },
  {
    "Tags": null
  }
]
```
**预期SQL**:
```sql
SELECT
  `T3`.`Tags`
FROM `users` AS `T1`
INNER JOIN `postHistory` AS `T2`
  ON `T1`.`Id` = `T2`.`UserId`
INNER JOIN `posts` AS `T3`
  ON `T3`.`Id` = `T2`.`PostId`
WHERE
  `T1`.`DisplayName` = 'Mark Meckes' AND `T3`.`CommentCount` = 0
```

**预期结果**:
```json
[
  {
    "Tags": "<books>"
  },
  {
    "Tags": "<books>"
  },
  {
    "Tags": "<books>"
  },
  {
    "Tags": "<books>"
  },
  {
    "Tags": null
  }
]
```
---

#### ID:640 | codebase_community

**问题**: Calculate the difference in view count from post posted by Mornington and view count from posts posted by Amos.

**证据**: calculation = SUBTRACT(SUM(ViewCount where DisplayName = 'Mornington'), SUM(ViewCount where DisplayName = 'Amos'));

**生成SQL**:
```sql
SELECT COALESCE((SELECT SUM(ViewCount) FROM posts p INNER JOIN users u ON p.OwnerUserId = u.Id WHERE u.DisplayName = 'Mornington'), 0) - COALESCE((SELECT SUM(ViewCount) FROM posts p INNER JOIN users u ON p.OwnerUserId = u.Id WHERE u.DisplayName = 'Amos'), 0) AS difference;
```

**生成结果**:
```json
[
  {
    "difference": -497.0
  }
]
```
**预期SQL**:
```sql
SELECT
  SUM(CASE WHEN `T1`.`DisplayName` = 'Mornington' THEN `T3`.`ViewCount` ELSE 0 END) - SUM(CASE WHEN `T1`.`DisplayName` = 'Amos' THEN `T3`.`ViewCount` ELSE 0 END) AS `diff`
FROM `users` AS `T1`
INNER JOIN `postHistory` AS `T2`
  ON `T1`.`Id` = `T2`.`UserId`
INNER JOIN `posts` AS `T3`
  ON `T3`.`Id` = `T2`.`PostId`
```

**预期结果**:
```json
[
  {
    "diff": -1491.0
  }
]
```
---

#### ID:665 | codebase_community

**问题**: What is the average monthly number of links created in 2010 for posts that have no more than 2 answers?

**证据**: calculation = DIVIDE(COUNT(Id where YEAR(CreationDate) = 2010 and AnswerCount < = 2), 12)

**生成SQL**:
```sql
SELECT CAST(COUNT(DISTINCT pl.Id) AS DOUBLE) / 12 AS average_monthly_links FROM postLinks pl WHERE YEAR(pl.CreationDate) = 2010 AND (EXISTS (SELECT 1 FROM posts p WHERE p.Id = pl.PostId AND p.AnswerCount <= 2) OR EXISTS (SELECT 1 FROM posts p WHERE p.Id = pl.RelatedPostId AND p.AnswerCount <= 2))
```

**生成结果**:
```json
[
  {
    "average_monthly_links": 11.583333333333334
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST(COUNT(`T1`.`Id`) AS DOUBLE) / 12
FROM `postLinks` AS `T1`
INNER JOIN `posts` AS `T2`
  ON `T1`.`PostId` = `T2`.`Id`
WHERE
  `T2`.`AnswerCount` <= 2
  AND DATE_FORMAT(CAST(`T1`.`CreationDate` AS DATETIME), '%Y') = '2010'
```

**预期结果**:
```json
[
  {
    "CAST(COUNT(`T1`.`Id`) AS DOUBLE) / 12": 8.666666666666666
  }
]
```
---

#### ID:672 | codebase_community

**问题**: Among the users located in United Kingdom, how many users whose post have a total favorite amount of 4 or more?

**证据**: favorite amount of 4 or more refers to FavoriteCount > = 4; Location = 'United Kingdom';

**生成SQL**:
```sql
SELECT COUNT(*) FROM (SELECT users.Id FROM users INNER JOIN posts ON users.Id = posts.OwnerUserId WHERE users.Location = 'United Kingdom' GROUP BY users.Id HAVING SUM(posts.FavoriteCount) >= 4) AS user_counts
```

**生成结果**:
```json
[
  {
    "COUNT(*)": 18
  }
]
```
**预期SQL**:
```sql
SELECT
  COUNT(`T1`.`Id`)
FROM `users` AS `T1`
INNER JOIN `posts` AS `T2`
  ON `T1`.`Id` = `T2`.`OwnerUserId`
WHERE
  `T1`.`Location` = 'United Kingdom' AND `T2`.`FavoriteCount` >= 4
```

**预期结果**:
```json
[
  {
    "COUNT(`T1`.`Id`)": 19
  }
]
```
---

#### ID:682 | codebase_community

**问题**: Which is the most valuable post in 2010? Please give its id and the owner's display name.

**证据**: the most valuable post in 2010 refers to MAX(FavoriteCount) where year(CreationDate) = 2010;

**生成SQL**:
```sql
SELECT Id, OwnerDisplayName FROM posts WHERE YEAR(CreationDate) = 2010 ORDER BY FavoriteCount DESC LIMIT 1
```

**生成结果**:
```
❌ 执行失败
```

**预期SQL**:
```sql
SELECT
  `T2`.`OwnerUserId`,
  `T1`.`DisplayName`
FROM `users` AS `T1`
INNER JOIN `posts` AS `T2`
  ON `T1`.`Id` = `T2`.`OwnerUserId`
WHERE
  DATE_FORMAT(CAST(`T1`.`CreationDate` AS DATETIME), '%Y') = '2010'
ORDER BY
  `T2`.`FavoriteCount` DESC
LIMIT 1
```

**预期结果**:
```json
[
  {
    "OwnerUserId": 890,
    "DisplayName": "Fabian Fagerholm"
  }
]
```
---

#### ID:683 | codebase_community

**问题**: What is the percentage of posts whose owners had a reputation of over 1000 in 2011?

**证据**: percentage = DIVIDE(COUNT(Id where YEAR(CreationDate) = 2011 and Reputation > 1000), COUNT(Id) ) * 100;

**生成SQL**:
```sql
SELECT CAST(SUM(CASE WHEN u.Reputation > 1000 THEN 1 ELSE 0 END) AS DECIMAL) / COUNT(p.Id) * 100 AS percentage FROM posts p LEFT JOIN users u ON p.OwnerUserId = u.Id WHERE YEAR(p.CreationDate) = 2011;
```

**生成结果**:
```
❌ 执行失败
```

**预期SQL**:
```sql
SELECT
  CAST(SUM(
    CASE
      WHEN DATE_FORMAT(CAST(`T2`.`CreaionDate` AS DATETIME), '%Y') = '2011'
      AND `T1`.`Reputation` > 1000
      THEN 1
      ELSE 0
    END
  ) AS DOUBLE) * 100 / COUNT(`T1`.`Id`)
FROM `users` AS `T1`
INNER JOIN `posts` AS `T2`
  ON `T1`.`Id` = `T2`.`OwnerUserId`
```

**预期结果**:
```json
[
  {
    "CAST(SUM(\n    CASE\n      WHEN DATE_FORMAT(CAST(`T2`.`CreaionDate` AS DATETIME), '%Y') = '2011'\n      AND `T1`.`Reputation` > 1000\n      THEN 1\n      ELSE 0\n    END\n  ) AS DOUBLE) * 100 / COUNT(`T1`.`Id`)": 7.241992293168744
  }
]
```
---

#### ID:685 | codebase_community

**问题**: Identify the total views on the post 'Computer Game Datasets'. Name the user who posted it last time.

**证据**: total views refer to ViewCount; Name the user refers to DisplayName; post 'Computer Game Datasets' refers to Text = 'Computer Game Datasets';

**生成SQL**:
```sql
SELECT p.ViewCount, u.DisplayName FROM posts p INNER JOIN users u ON p.LastEditorUserId = u.Id WHERE p.Id = (SELECT PostId FROM postHistory WHERE Text = 'Computer Game Datasets' LIMIT 1)
```

**生成结果**:
```json
[
  {
    "ViewCount": 1708,
    "DisplayName": "mbq"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T2`.`ViewCount`,
  `T3`.`DisplayName`
FROM `postHistory` AS `T1`
INNER JOIN `posts` AS `T2`
  ON `T1`.`PostId` = `T2`.`Id`
INNER JOIN `users` AS `T3`
  ON `T2`.`LastEditorUserId` = `T3`.`Id`
WHERE
  `T1`.`Text` = 'Computer Game Datasets'
```

**预期结果**:
```json
[
  {
    "ViewCount": 1708,
    "DisplayName": "mbq"
  },
  {
    "ViewCount": 1708,
    "DisplayName": "mbq"
  }
]
```
---

#### ID:694 | codebase_community

**问题**: Provide the text of the latest 10 comments to the post with the title 'Analysing wind data with R' and the display name of the user who left it.

**证据**: the latest comment refers to MAX(CreationDate);

**生成SQL**:
```sql
SELECT c.Text, c.UserDisplayName FROM comments c WHERE c.PostId = (SELECT Id FROM posts WHERE Title = 'Analysing wind data with R') ORDER BY c.CreationDate DESC LIMIT 10
```

**生成结果**:
```json
[
  {
    "Text": "i thought of integrating seperetly until 4 m/s, between 4 and 15m/s and over 15m/s, and comparing it to a situation of 100% of the time a turbine working in optimal speed",
    "UserDisplayName": null
  },
  {
    "Text": "well untill 4 m/s there is no wind generation and the max is 15 m/s, wind stronger than 15 m/s will make the same amount of energy",
    "UserDisplayName": null
  },
  {
    "Text": "Regarding your question about energy, it's going to be difficult to answer. Do you know anything about your device? Do you know anything of the relationship between wind speed/direction and power? Do you know anything about the layout of the turbines at this particular site since that has a huge impact on the power as you no doubt are aware.",
    "UserDisplayName": null
  },
  {
    "Text": "note that 'lag' is a term used mainly in analysis of data in time, referring to one thing occurring after another. This isn't a lag - it's perhaps more accurately called a shift - or maybe an offset - but shift is probably more common for distributions, they shift and scale.",
    "UserDisplayName": null
  },
  {
    "Text": "i tried ploting it with out zero's but still there is a lag",
    "UserDisplayName": null
  }
]
```
**预期SQL**:
```sql
SELECT
  `T3`.`Text`,
  `T1`.`DisplayName`
FROM `users` AS `T1`
INNER JOIN `posts` AS `T2`
  ON `T1`.`Id` = `T2`.`OwnerUserId`
INNER JOIN `comments` AS `T3`
  ON `T2`.`Id` = `T3`.`PostId`
WHERE
  `T2`.`Title` = 'Analysing wind data with R'
ORDER BY
  `T1`.`CreationDate` DESC
LIMIT 10
```

**预期结果**:
```json
[
  {
    "Text": "About the picture, post to some image hosting and put a link -- I'll convert it into a pasted-in picture.",
    "DisplayName": "eliavs"
  },
  {
    "Text": "+1, interesting question, you might find that soon you will have enough reputation :)",
    "DisplayName": "eliavs"
  },
  {
    "Text": "yup i have thanks to all that helped me!!",
    "DisplayName": "eliavs"
  },
  {
    "Text": "judging from the graph, the problem is not the lag. What you have plotted is roughly goodness of fit. So it seems that Weibull distribution is not apropriate for your data. I see that there is a bunch up near zero, do you have zero values in your data? In that case you will need to model zero values separately. So first suggestion would be to try Weibull for non zero values. Also why Weibull, is there particular reason, some reference from similar work perhaps?",
    "DisplayName": "eliavs"
  },
  {
    "Text": "well yes mainly from literature and other works on wind for the purpose of wind farms",
    "DisplayName": "eliavs"
  }
]
```
---

#### ID:716 | codebase_community

**问题**: Among the comments with scores between 5 to 10, what is the percentage of the users with 0 up votes?

**证据**: percentage = DIVIDE(COUNT(UserId where UpVotes = 0 and Score BETWEEN 5 and 10))*100, (COUNT(UserId where Score BETWEEN 5 and 10));

**生成SQL**:
```sql
SELECT (CAST(COUNT(DISTINCT CASE WHEN u.UpVotes = 0 THEN c.UserId END) AS DOUBLE) * 100) / CAST(COUNT(DISTINCT c.UserId) AS DOUBLE) AS percentage FROM comments c INNER JOIN users u ON c.UserId = u.Id WHERE c.Score BETWEEN 5 AND 10;
```

**生成结果**:
```json
[
  {
    "percentage": 4.87012987012987
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST(SUM(CASE WHEN `T1`.`UpVotes` = 0 THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(`T1`.`Id`) AS `per`
FROM `users` AS `T1`
INNER JOIN `comments` AS `T2`
  ON `T1`.`Id` = `T2`.`UserId`
WHERE
  `T2`.`Score` BETWEEN 5 AND 10
```

**预期结果**:
```json
[
  {
    "per": 1.3264554163596167
  }
]
```
---

#### ID:344 | card_games

**问题**: List all the mythic rarity print cards banned in gladiator format.

**证据**: mythic rarity printing refers to rarity = 'mythic'; card banned refers to status = 'Banned'; in gladiator format refers to format = 'gladiator';

**生成SQL**:
```sql
SELECT cards.* FROM cards INNER JOIN legalities ON cards.uuid = legalities.uuid WHERE cards.rarity = 'mythic' AND legalities.format = 'gladiator' AND legalities.status = 'Banned'
```

**生成结果**:
```json
[
  {
    "id": 17983,
    "artist": "Yongjae Choi",
    "asciiName": null,
    "availability": "arena,mtgo,paper",
    "borderColor": "black",
    "cardKingdomFoilId": "227736",
    "cardKingdomId": "227334",
    "colorIdentity": "G,U",
    "colorIndicator": null,
    "colors": "G,U",
    "convertedManaCost": 3.0,
    "duelDeck": null,
    "edhrecRank": 924,
    "faceConvertedManaCost": null,
    "faceName": null,
    "flavorName": null,
    "flavorText": null,
    "frameEffects": null,
    "frameVersion": "2015",
    "hand": null,
    "hasAlternativeDeckLimit": 0,
    "hasContentWarning": 0,
    "hasFoil": 1,
    "hasNonFoil": 1,
    "isAlternative": 0,
    "isFullArt": 0,
    "isOnlineOnly": 0,
    "isOversized": 0,
    "isPromo": 0,
    "isReprint": 0,
    "isReserved": 0,
    "isStarter": 0,
    "isStorySpotlight": 0,
    "isTextless": 0,
    "isTimeshifted": 0,
    "keywords": null,
    "layout": "normal",
    "leadershipSkills": "{'brawl': True, 'commander': False, 'oathbreaker': True}",
    "life": null,
    "loyalty": "4",
    "manaCost": "{1}{G}{U}",
    "mcmId": "398659",
    "mcmMetaId": "280814",
    "mtgArenaId": "70344",
    "mtgjsonV4Id": "7998ef11-85d3-5280-b880-bd8b3a896e66",
    "mtgoFoilId": null,
    "mtgoId": "78538",
    "multiverseId": "473159",
    "name": "Oko, Thief of Crowns",
    "number": "197",
    "originalReleaseDate": null,
    "originalText": "+2: Create a Food token.\n+1: Target artifact or creature loses all abilities and becomes a green Elk creature with base power and toughness 3/3.\n−5: Exchange control of target artifact or creature you control and target creature an opponent controls with ",
    "originalType": "Legendary Planeswalker — Oko",
    "otherFaceIds": null,
    "power": null,
    "printings": "ELD,PELD,PRM",
    "promoTypes": null,
    "purchaseUrls": "{'cardKingdom': 'https://mtgjson.com/links/b554341a1e2e4bc6', 'cardKingdomFoil': 'https://mtgjson.com/links/3a4f0694bc7ec67d', 'cardmarket': 'https://mtgjson.com/links/47fc0c7a1fd8b8c1', 'tcgplayer': 'https://mtgjson.com/links/c87de898ceca3008'}",
    "rarity": "mythic",
    "scryfallId": "3462a3d0-5552-49fa-9eb7-100960c55891",
    "scryfallIllustrationId": "a7e6d58e-e8da-445c-8375-1f1dac564eed",
    "scryfallOracleId": "60c60923-ff1b-43f7-8768-731499fcffc9",
    "setCode": "ELD",
    "side": null,
    "subtypes": "Oko",
    "supertypes": "Legendary",
    "tcgplayerProductId": "198356",
    "text": "[+2]: Create a Food token. (It's an artifact with \"{2}, {T}, Sacrifice this artifact: You gain 3 life.\")\n[+1]: Target artifact or creature loses all abilities and becomes a green Elk creature with base power and toughness 3/3.\n[−5]: Exchange control of ta",
    "toughness": null,
    "type": "Legendary Planeswalker — Oko",
    "types": "Planeswalker",
    "uuid": "46153afe-5e05-5082-852a-648c03924bcf",
    "variations": "f203bad8-9c07-507c-9699-fc8fec69e2d2",
    "watermark": null
  },
  {
    "id": 18058,
    "artist": "Wesley Burt",
    "asciiName": null,
    "availability": "mtgo,paper",
    "borderColor": "borderless",
    "cardKingdomFoilId": "228008",
    "cardKingdomId": "227483",
    "colorIdentity": "G,U",
    "colorIndicator": null,
    "colors": "G,U",
    "convertedManaCost": 3.0,
    "duelDeck": null,
    "edhrecRank": 924,
    "faceConvertedManaCost": null,
    "faceName": null,
    "flavorName": null,
    "flavorText": null,
    "frameEffects": null,
    "frameVersion": "2015",
    "hand": null,
    "hasAlternativeDeckLimit": 0,
    "hasContentWarning": 0,
    "hasFoil": 1,
    "hasNonFoil": 1,
    "isAlternative": 0,
    "isFullArt": 0,
    "isOnlineOnly": 0,
    "isOversized": 0,
    "isPromo": 0,
    "isReprint": 0,
    "isReserved": 0,
    "isStarter": 1,
    "isStorySpotlight": 0,
    "isTextless": 0,
    "isTimeshifted": 0,
    "keywords": null,
    "layout": "normal",
    "leadershipSkills": "{'brawl': True, 'commander': False, 'oathbreaker': True}",
    "life": null,
    "loyalty": "4",
    "manaCost": "{1}{G}{U}",
    "mcmId": "398664",
    "mcmMetaId": "280814",
    "mtgArenaId": null,
    "mtgjsonV4Id": "202c6f3d-2094-516d-bd3e-1c3e7d16be3e",
    "mtgoFoilId": null,
    "mtgoId": null,
    "multiverseId": null,
    "name": "Oko, Thief of Crowns",
    "number": "271",
    "originalReleaseDate": null,
    "originalText": null,
    "originalType": null,
    "otherFaceIds": null,
    "power": null,
    "printings": "ELD,PELD,PRM",
    "promoTypes": "boosterfun",
    "purchaseUrls": "{'cardKingdom': 'https://mtgjson.com/links/986800d453ba65c9', 'cardKingdomFoil': 'https://mtgjson.com/links/4244006031661d34', 'cardmarket': 'https://mtgjson.com/links/e219b4d426be1474', 'tcgplayer': 'https://mtgjson.com/links/6c32958f96c8fa2c'}",
    "rarity": "mythic",
    "scryfallId": "95da027e-34c1-4098-827d-1647693ad8f4",
    "scryfallIllustrationId": "4c64f0e1-8d5d-449f-afe8-333f7b41789d",
    "scryfallOracleId": "60c60923-ff1b-43f7-8768-731499fcffc9",
    "setCode": "ELD",
    "side": null,
    "subtypes": "Oko",
    "supertypes": "Legendary",
    "tcgplayerProductId": "198357",
    "text": "[+2]: Create a Food token. (It's an artifact with \"{2}, {T}, Sacrifice this artifact: You gain 3 life.\")\n[+1]: Target artifact or creature loses all abilities and becomes a green Elk creature with base power and toughness 3/3.\n[−5]: Exchange control of ta",
    "toughness": null,
    "type": "Legendary Planeswalker — Oko",
    "types": "Planeswalker",
    "uuid": "f203bad8-9c07-507c-9699-fc8fec69e2d2",
    "variations": "46153afe-5e05-5082-852a-648c03924bcf",
    "watermark": null
  },
  {
    "id": 29523,
    "artist": "Mike Bierek",
    "asciiName": null,
    "availability": "arena,mtgo,paper",
    "borderColor": "black",
    "cardKingdomFoilId": "219702",
    "cardKingdomId": null,
    "colorIdentity": "U",
    "colorIndicator": null,
    "colors": "U",
    "convertedManaCost": 7.0,
    "duelDeck": null,
    "edhrecRank": 789,
    "faceConvertedManaCost": null,
    "faceName": null,
    "flavorName": null,
    "flavorText": "Sarkhan wandered into a tomb and back in time.",
    "frameEffects": null,
    "frameVersion": "2015",
    "hand": null,
    "hasAlternativeDeckLimit": 0,
    "hasContentWarning": 0,
    "hasFoil": 1,
    "hasNonFoil": 0,
    "isAlternative": 0,
    "isFullArt": 0,
    "isOnlineOnly": 0,
    "isOversized": 0,
    "isPromo": 1,
    "isReprint": 0,
    "isReserved": 0,
    "isStarter": 1,
    "isStorySpotlight": 0,
    "isTextless": 0,
    "isTimeshifted": 0,
    "keywords": null,
    "layout": "normal",
    "leadershipSkills": null,
    "life": null,
    "loyalty": null,
    "manaCost": "{5}{U}{U}",
    "mcmId": "359678",
    "mcmMetaId": null,
    "mtgArenaId": "68294",
    "mtgjsonV4Id": "ab6d408f-63db-57b6-9382-586cbceade42",
    "mtgoFoilId": null,
    "mtgoId": "68145",
    "multiverseId": "450253",
    "name": "Nexus of Fate",
    "number": "306",
    "originalReleaseDate": null,
    "originalText": "Take an extra turn after this one.\nIf Nexus of Fate would be put into a graveyard from anywhere, reveal Nexus of Fate and shuffle it into its owner's library instead.",
    "originalType": "Instant",
    "otherFaceIds": null,
    "power": null,
    "printings": "M19",
    "promoTypes": "buyabox",
    "purchaseUrls": "{'cardKingdomFoil': 'https://mtgjson.com/links/be89268a4f20f2cd', 'tcgplayer': 'https://mtgjson.com/links/f5678eecae1ae542'}",
    "rarity": "mythic",
    "scryfallId": "f163cfbf-6df6-4af5-9fe4-23b0d511586a",
    "scryfallIllustrationId": "bd8f0d5b-9045-4156-90da-f60b3b8e2d7a",
    "scryfallOracleId": "6c1d22d4-f28e-4041-a9b6-1575e8929b61",
    "setCode": "M19",
    "side": null,
    "subtypes": null,
    "supertypes": null,
    "tcgplayerProductId": "169146",
    "text": "Take an extra turn after this one.\nIf Nexus of Fate would be put into a graveyard from anywhere, reveal Nexus of Fate and shuffle it into its owner's library instead.",
    "toughness": null,
    "type": "Instant",
    "types": "Instant",
    "uuid": "f2b2679f-0d84-5602-8014-241725c94023",
    "variations": null,
    "watermark": null
  },
  {
    "id": 38736,
    "artist": "Yongjae Choi",
    "asciiName": null,
    "availability": "paper",
    "borderColor": "black",
    "cardKingdomFoilId": "228295",
    "cardKingdomId": "228222",
    "colorIdentity": "G,U",
    "colorIndicator": null,
    "colors": "G,U",
    "convertedManaCost": 3.0,
    "duelDeck": null,
    "edhrecRank": 924,
    "faceConvertedManaCost": null,
    "faceName": null,
    "flavorName": null,
    "flavorText": null,
    "frameEffects": null,
    "frameVersion": "2015",
    "hand": null,
    "hasAlternativeDeckLimit": 0,
    "hasContentWarning": 0,
    "hasFoil": 1,
    "hasNonFoil": 1,
    "isAlternative": 0,
    "isFullArt": 0,
    "isOnlineOnly": 0,
    "isOversized": 0,
    "isPromo": 1,
    "isReprint": 1,
    "isReserved": 0,
    "isStarter": 1,
    "isStorySpotlight": 0,
    "isTextless": 0,
    "isTimeshifted": 0,
    "keywords": null,
    "layout": "normal",
    "leadershipSkills": "{'brawl': False, 'commander': False, 'oathbreaker': True}",
    "life": null,
    "loyalty": "4",
    "manaCost": "{1}{G}{U}",
    "mcmId": "404004",
    "mcmMetaId": null,
    "mtgArenaId": null,
    "mtgjsonV4Id": "18eb3cf0-af1e-5dba-bf97-b6dbdc4db86a",
    "mtgoFoilId": null,
    "mtgoId": null,
    "multiverseId": null,
    "name": "Oko, Thief of Crowns",
    "number": "197p",
    "originalReleaseDate": null,
    "originalText": null,
    "originalType": null,
    "otherFaceIds": null,
    "power": null,
    "printings": "ELD,PELD,PRM",
    "promoTypes": "promostamped,promopack,planeswalkerstamped",
    "purchaseUrls": "{'cardKingdom': 'https://mtgjson.com/links/3f415645c2342160', 'cardKingdomFoil': 'https://mtgjson.com/links/aa7db5e0334549ab', 'tcgplayer': 'https://mtgjson.com/links/bfbcaa3f22bdbfd8'}",
    "rarity": "mythic",
    "scryfallId": "058c60d2-25d1-42bf-9747-715e9ff56e0b",
    "scryfallIllustrationId": "a7e6d58e-e8da-445c-8375-1f1dac564eed",
    "scryfallOracleId": "60c60923-ff1b-43f7-8768-731499fcffc9",
    "setCode": "PELD",
    "side": null,
    "subtypes": "Oko",
    "supertypes": "Legendary",
    "tcgplayerProductId": "200395",
    "text": "[+2]: Create a Food token. (It's an artifact with \"{2}, {T}, Sacrifice this artifact: You gain 3 life.\")\n[+1]: Target artifact or creature loses all abilities and becomes a green Elk creature with base power and toughness 3/3.\n[−5]: Exchange control of ta",
    "toughness": null,
    "type": "Legendary Planeswalker — Oko",
    "types": "Planeswalker",
    "uuid": "3d8884e6-75a2-5422-98e0-44b155f71db7",
    "variations": "8c48df5c-6e6f-5602-8312-523435d88a9b",
    "watermark": null
  },
  {
    "id": 38737,
    "artist": "Yongjae Choi",
    "asciiName": null,
    "availability": "paper",
    "borderColor": "black",
    "cardKingdomFoilId": "228154",
    "cardKingdomId": null,
    "colorIdentity": "G,U",
    "colorIndicator": null,
    "colors": "G,U",
    "convertedManaCost": 3.0,
    "duelDeck": null,
    "edhrecRank": 924,
    "faceConvertedManaCost": null,
    "faceName": null,
    "flavorName": null,
    "flavorText": null,
    "frameEffects": null,
    "frameVersion": "2015",
    "hand": null,
    "hasAlternativeDeckLimit": 0,
    "hasContentWarning": 0,
    "hasFoil": 1,
    "hasNonFoil": 0,
    "isAlternative": 0,
    "isFullArt": 0,
    "isOnlineOnly": 0,
    "isOversized": 0,
    "isPromo": 1,
    "isReprint": 1,
    "isReserved": 0,
    "isStarter": 1,
    "isStorySpotlight": 0,
    "isTextless": 0,
    "isTimeshifted": 0,
    "keywords": null,
    "layout": "normal",
    "leadershipSkills": "{'brawl': False, 'commander': False, 'oathbreaker': True}",
    "life": null,
    "loyalty": "4",
    "manaCost": "{1}{G}{U}",
    "mcmId": "403664",
    "mcmMetaId": null,
    "mtgArenaId": null,
    "mtgjsonV4Id": "13f4b43c-5110-591c-9466-f9196ea80c84",
    "mtgoFoilId": null,
    "mtgoId": null,
    "multiverseId": null,
    "name": "Oko, Thief of Crowns",
    "number": "197s",
    "originalReleaseDate": null,
    "originalText": null,
    "originalType": null,
    "otherFaceIds": null,
    "power": null,
    "printings": "ELD,PELD,PRM",
    "promoTypes": "prerelease,datestamped",
    "purchaseUrls": "{'cardKingdomFoil': 'https://mtgjson.com/links/922ea76334566e8c', 'tcgplayer': 'https://mtgjson.com/links/c343fdbb863ee371'}",
    "rarity": "mythic",
    "scryfallId": "acbb9670-5e79-4f19-b4bc-afbbe130d122",
    "scryfallIllustrationId": "a7e6d58e-e8da-445c-8375-1f1dac564eed",
    "scryfallOracleId": "60c60923-ff1b-43f7-8768-731499fcffc9",
    "setCode": "PELD",
    "side": null,
    "subtypes": "Oko",
    "supertypes": "Legendary",
    "tcgplayerProductId": "199928",
    "text": "[+2]: Create a Food token. (It's an artifact with \"{2}, {T}, Sacrifice this artifact: You gain 3 life.\")\n[+1]: Target artifact or creature loses all abilities and becomes a green Elk creature with base power and toughness 3/3.\n[−5]: Exchange control of ta",
    "toughness": null,
    "type": "Legendary Planeswalker — Oko",
    "types": "Planeswalker",
    "uuid": "8c48df5c-6e6f-5602-8312-523435d88a9b",
    "variations": "3d8884e6-75a2-5422-98e0-44b155f71db7",
    "watermark": null
  }
]
```
**预期SQL**:
```sql
SELECT DISTINCT
  `T1`.`id`
FROM `cards` AS `T1`
INNER JOIN `legalities` AS `T2`
  ON `T1`.`uuid` = `T2`.`uuid`
WHERE
  `T2`.`format` = 'gladiator'
  AND `T2`.`status` = 'Banned'
  AND `T1`.`rarity` = 'mythic'
```

**预期结果**:
```json
[
  {
    "id": 17983
  },
  {
    "id": 18058
  },
  {
    "id": 29523
  },
  {
    "id": 38736
  },
  {
    "id": 38737
  }
]
```
---

#### ID:345 | card_games

**问题**: For artifact type of cards that do not have multiple faces on the same card, state its legalities status for vintage play format.

**证据**: Artifact type of cards refers to types = 'Artifact'; card does not have multiple faces on the same card refers to side is NULL'; vintage play format refers to format = 'vintage';

**生成SQL**:
```sql
SELECT cards.name, legalities.status FROM cards INNER JOIN legalities ON cards.uuid = legalities.uuid WHERE cards.types = 'Artifact' AND cards.side IS NULL AND legalities.format = 'vintage'
```

**生成结果**:
```json
[
  {
    "name": "Angel's Feather",
    "status": "Legal"
  },
  {
    "name": "Chimeric Staff",
    "status": "Legal"
  },
  {
    "name": "Chromatic Star",
    "status": "Legal"
  },
  {
    "name": "Citanul Flute",
    "status": "Legal"
  },
  {
    "name": "Coat of Arms",
    "status": "Legal"
  }
]
```
**预期SQL**:
```sql
SELECT DISTINCT
  `T2`.`status`
FROM `cards` AS `T1`
INNER JOIN `legalities` AS `T2`
  ON `T1`.`uuid` = `T2`.`uuid`
WHERE
  `T1`.`type` = 'Artifact' AND `T2`.`format` = 'vintage' AND `T1`.`side` IS NULL
```

**预期结果**:
```json
[
  {
    "status": "Legal"
  },
  {
    "status": "Restricted"
  },
  {
    "status": "Banned"
  }
]
```
---

#### ID:347 | card_games

**问题**: Find all cards illustrated by Stephen Daniel and describe the text of the ruling of these cards. State if these cards have missing or degraded properties and values.

**证据**: cards have missing or degraded properties and value refers to hasContentWarning = 1; 'Stephen Daniele' is artist; Find all cards refers to return card id

**生成SQL**:
```sql
SELECT c.id AS card_id, r.text AS ruling_text, CASE WHEN c.hasContentWarning = 1 THEN 'Yes' ELSE 'No' END AS has_missing_or_degraded FROM cards c INNER JOIN rulings r ON c.uuid = r.uuid WHERE c.artist = 'Stephen Daniele'
```

**生成结果**:
```json
[
  {
    "card_id": 29,
    "ruling_text": "You can’t put an Aura card from your hand onto the battlefield this way if that Aura can’t legally enchant Academy Researchers. For example, you can’t put an Aura with “enchant land” or “enchant green creature” onto the battlefield attached to Academy Res",
    "has_missing_or_degraded": "No"
  },
  {
    "card_id": 3872,
    "ruling_text": "This card now has Enchant Swamp, which works exactly like any other Enchant ability. This means it can only be cast targeting a Swamp, and it will be put into its owner’s graveyard if the permanent it’s attached to ever stops being a Swamp.",
    "has_missing_or_degraded": "No"
  },
  {
    "card_id": 6651,
    "ruling_text": "Cycling is an activated ability. Effects that interact with activated abilities (such as Stifle or Rings of Brighthearth) will interact with cycling. Effects that interact with spells (such as Remove Soul or Faerie Tauntings) will not.",
    "has_missing_or_degraded": "No"
  },
  {
    "card_id": 6652,
    "ruling_text": "Cycling is an activated ability. Effects that interact with activated abilities (such as Stifle or Rings of Brighthearth) will interact with cycling. Effects that interact with spells (such as Remove Soul or Faerie Tauntings) will not.",
    "has_missing_or_degraded": "No"
  },
  {
    "card_id": 7950,
    "ruling_text": "Cycling is an activated ability. Effects that interact with activated abilities (such as Stifle or Rings of Brighthearth) will interact with cycling. Effects that interact with spells (such as Remove Soul or Faerie Tauntings) will not.",
    "has_missing_or_degraded": "No"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T1`.`id`,
  `T2`.`text`,
  `T1`.`hasContentWarning`
FROM `cards` AS `T1`
INNER JOIN `rulings` AS `T2`
  ON `T1`.`uuid` = `T2`.`uuid`
WHERE
  `T1`.`artist` = 'Stephen Daniele'
```

**预期结果**:
```json
[
  {
    "id": 29,
    "text": "You can’t put an Aura card from your hand onto the battlefield this way if that Aura can’t legally enchant Academy Researchers. For example, you can’t put an Aura with “enchant land” or “enchant green creature” onto the battlefield attached to Academy Res",
    "hasContentWarning": 0
  },
  {
    "id": 3872,
    "text": "This card now has Enchant Swamp, which works exactly like any other Enchant ability. This means it can only be cast targeting a Swamp, and it will be put into its owner’s graveyard if the permanent it’s attached to ever stops being a Swamp.",
    "hasContentWarning": 0
  },
  {
    "id": 6651,
    "text": "Cycling is an activated ability. Effects that interact with activated abilities (such as Stifle or Rings of Brighthearth) will interact with cycling. Effects that interact with spells (such as Remove Soul or Faerie Tauntings) will not.",
    "hasContentWarning": 0
  },
  {
    "id": 6652,
    "text": "Cycling is an activated ability. Effects that interact with activated abilities (such as Stifle or Rings of Brighthearth) will interact with cycling. Effects that interact with spells (such as Remove Soul or Faerie Tauntings) will not.",
    "hasContentWarning": 0
  },
  {
    "id": 7950,
    "text": "Cycling is an activated ability. Effects that interact with activated abilities (such as Stifle or Rings of Brighthearth) will interact with cycling. Effects that interact with spells (such as Remove Soul or Faerie Tauntings) will not.",
    "hasContentWarning": 0
  }
]
```
---

#### ID:349 | card_games

**问题**: Name the card and artist with the most ruling information. Also state if the card is a promotional printing.

**证据**: with the most ruling information refers to Max(count(rulings.uuid)); the card is the promotional printing refers to isPromo = 1;

**生成SQL**:
```sql
SELECT c.name, c.artist, c.isPromo FROM cards c INNER JOIN rulings r ON c.uuid = r.uuid GROUP BY c.uuid, c.name, c.artist, c.isPromo HAVING COUNT(r.uuid) = (SELECT MAX(ruling_count) FROM (SELECT COUNT(*) as ruling_count FROM rulings GROUP BY uuid) as sub)
```

**生成结果**:
```json
[
  {
    "name": "Teferi's Protection",
    "artist": "Chase Stone",
    "isPromo": 0
  },
  {
    "name": "Teferi's Protection",
    "artist": "Chase Stone",
    "isPromo": 1
  },
  {
    "name": "Teferi's Protection",
    "artist": "Chase Stone",
    "isPromo": 0
  },
  {
    "name": "Teferi's Protection",
    "artist": "Chase Stone",
    "isPromo": 0
  }
]
```
**预期SQL**:
```sql
SELECT `T1`.`name`, `T1`.`artist`, `T1`.`isPromo` FROM `cards` AS `T1` INNER JOIN `rulings` AS `T2` ON `T1`.`uuid` = `T2`.`uuid` WHERE `T1`.`isPromo` = 1 AND `T1`.`artist` = ( SELECT `artist` FROM `cards` WHERE `isPromo` = 1 GROUP BY `artist` HAVING COUNT(DISTINCT `uuid`) = (SELECT MAX(card_counts.max_count) FROM (SELECT COUNT(DISTINCT `uuid`) AS max_count FROM `cards` WHERE `isPromo` = 1 GROUP BY `artist`) AS card_counts))LIMIT 1
```

**预期结果**:
```json
[
  {
    "name": "Serrated Arrows",
    "artist": "John Avon",
    "isPromo": 1
  }
]
```
---

#### ID:352 | card_games

**问题**: Calculate the percentage of the cards availabe in Chinese Simplified.

**证据**: Chinese Simplified' is the language; percentage = Divide(Sum(id where language = 'Chinese Simplified'), Count(id)) *100

**生成SQL**:
```sql
SELECT CAST((SELECT COUNT(DISTINCT uuid) FROM foreign_data WHERE language = 'Chinese Simplified') AS DOUBLE) / CAST((SELECT COUNT(*) FROM cards) AS DOUBLE) * 100 AS percentage
```

**生成结果**:
```json
[
  {
    "percentage": 35.38418218295731
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST(SUM(CASE WHEN `T2`.`language` = 'Chinese Simplified' THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(`T1`.`id`)
FROM `cards` AS `T1`
INNER JOIN `foreign_data` AS `T2`
  ON `T1`.`uuid` = `T2`.`uuid`
```

**预期结果**:
```json
[
  {
    "CAST(SUM(CASE WHEN `T2`.`language` = 'Chinese Simplified' THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(`T1`.`id`)": 8.773399659641314
  }
]
```
---

#### ID:391 | card_games

**问题**: Among the Artifact cards, which are black color and comes with foreign languague translation?

**证据**: Artifact card refers to originalType = 'Artifact'; black color refers to colors = 'B'; foreign language refers to language in foreign_data

**生成SQL**:
```sql
SELECT name FROM cards WHERE originalType = 'Artifact' AND colors = 'B' AND EXISTS (SELECT 1 FROM foreign_data WHERE foreign_data.uuid = cards.uuid AND foreign_data.language IS NOT NULL)
```

**生成结果**:
```json
[
  {
    "name": "Executioner's Capsule"
  },
  {
    "name": "Executioner's Capsule"
  },
  {
    "name": "Immortal Coil"
  },
  {
    "name": "Onyx Goblet"
  },
  {
    "name": "Executioner's Capsule"
  }
]
```
**预期SQL**:
```sql
SELECT DISTINCT
  `T1`.`name`
FROM `cards` AS `T1`
INNER JOIN `foreign_data` AS `T2`
  ON `T1`.`uuid` = `T2`.`uuid`
WHERE
  `T1`.`originalType` = 'Artifact' AND `T1`.`colors` = 'B'
```

**预期结果**:
```json
[
  {
    "name": "Executioner's Capsule"
  },
  {
    "name": "Immortal Coil"
  },
  {
    "name": "Onyx Goblet"
  },
  {
    "name": "Netherborn Altar"
  },
  {
    "name": "Scepter of Fugue"
  }
]
```
---

#### ID:402 | card_games

**问题**: What is the percentage of Story Spotlight cards that do not have a text box? List them by their ID.

**证据**: Story Spotlight cards that do not have a text box refers to isStorySpotlight = 1 and isTextless = 0; Percentage = DIVIDE(SUM(count(id) where isStorylight = 1 AND isTextless = 0 ), SUM(count(id))) * 100

**生成SQL**:
```sql
SELECT id, (SELECT CAST(COUNT(CASE WHEN isStorySpotlight = 1 AND isTextless = 1 THEN 1 END) AS DOUBLE) * 100 / COUNT(*) FROM cards) AS percentage FROM cards WHERE isStorySpotlight = 1 AND isTextless = 1
```

**生成结果**:
(空结果)

**预期SQL**:
```sql
SELECT
  CAST(SUM(CASE WHEN `isTextless` = 0  AND `isStorySpotlight` = 1 THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(`id`)
FROM `cards`
```

**预期结果**:
```json
[
  {
    "CAST(SUM(CASE WHEN `isTextless` = 0  AND `isStorySpotlight` = 1 THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(`id`)": 0.18302770053852382
  }
]
```
---

#### ID:405 | card_games

**问题**: How many Brazilian Portuguese translated sets are inside the Commander block?

**证据**: Commander block refer to block = 'Commander'; sets refer to code = setCode; Portuguese refer to language = 'Portuguese (Brasil)'

**生成SQL**:
```sql
SELECT COUNT(DISTINCT sets.id) AS brazilian_portuguese_sets_count FROM sets INNER JOIN set_translations ON sets.code = set_translations.setCode WHERE sets.block = 'Commander' AND set_translations.language = 'Portuguese (Brasil)'
```

**生成结果**:
```json
[
  {
    "brazilian_portuguese_sets_count": 0
  }
]
```
**预期SQL**:
```sql
SELECT
  COUNT(`T1`.`id`)
FROM `sets` AS `T1`
INNER JOIN `set_translations` AS `T2`
  ON `T1`.`code` = `T2`.`setCode`
WHERE
  `T2`.`language` = 'Portuguese (Brazil)' AND `T1`.`block` = 'Commander'
```

**预期结果**:
```json
[
  {
    "COUNT(`T1`.`id`)": 7
  }
]
```
---

#### ID:407 | card_games

**问题**: Lists all types of cards in German.

**证据**: German refer to language; all types refer to the subtypes, supertypes; subtypes is not null AND supertypes is not null

**生成SQL**:
```sql
SELECT DISTINCT cards.subtypes, cards.supertypes FROM foreign_data INNER JOIN cards ON foreign_data.uuid = cards.uuid WHERE foreign_data.language = 'German' AND cards.subtypes IS NOT NULL AND cards.supertypes IS NOT NULL
```

**生成结果**:
```json
[
  {
    "subtypes": "Human,Rebel",
    "supertypes": "Legendary"
  },
  {
    "subtypes": "Angel",
    "supertypes": "Legendary"
  },
  {
    "subtypes": "Merfolk,Wizard",
    "supertypes": "Legendary"
  },
  {
    "subtypes": "Vampire,Noble",
    "supertypes": "Legendary"
  },
  {
    "subtypes": "Avatar,Minion",
    "supertypes": "Legendary"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T1`.`subtypes`,
  `T1`.`supertypes`
FROM `cards` AS `T1`
INNER JOIN `foreign_data` AS `T2`
  ON `T1`.`uuid` = `T2`.`uuid`
WHERE
  `T2`.`language` = 'German'
  AND NOT `T1`.`subtypes` IS NULL
  AND NOT `T1`.`supertypes` IS NULL
```

**预期结果**:
```json
[
  {
    "subtypes": "Human,Rebel",
    "supertypes": "Legendary"
  },
  {
    "subtypes": "Angel",
    "supertypes": "Legendary"
  },
  {
    "subtypes": "Merfolk,Wizard",
    "supertypes": "Legendary"
  },
  {
    "subtypes": "Vampire,Noble",
    "supertypes": "Legendary"
  },
  {
    "subtypes": "Avatar,Minion",
    "supertypes": "Legendary"
  }
]
```
---

#### ID:408 | card_games

**问题**: How many unknown power cards contain info about the triggered ability

**证据**: unknown power cards refers to power is null or power = '*';contain info about the triggered ability refers to text contains 'triggered ability'

**生成SQL**:
```sql
SELECT COUNT(*) FROM cards WHERE (power IS NULL OR power = '*') AND text LIKE '%triggered ability%'
```

**生成结果**:
```json
[
  {
    "COUNT(*)": 35
  }
]
```
**预期SQL**:
```sql
SELECT
  Count(DISTINCT `T1`.`id`) 
FROM `cards` AS `T1`
INNER JOIN `rulings` AS `T2`
  ON `T1`.`uuid` = `T2`.`uuid`
WHERE
  (
    `T1`.`power` IS NULL OR `T1`.`power` = '*'
  )
  AND `T2`.`text` LIKE '%triggered ability%'
```

**预期结果**:
```json
[
  {
    "Count(DISTINCT `T1`.`id`)": 1382
  }
]
```
---

#### ID:412 | card_games

**问题**: What is the foreign name of the card in French of type Creature, normal layout and black border color, by artist Matthew D. Wilson?

**证据**: in French refers to language = 'French'; black border color refers to borderColor = 'black'

**生成SQL**:
```sql
SELECT foreign_data.name FROM foreign_data INNER JOIN cards ON foreign_data.uuid = cards.uuid WHERE foreign_data.language = 'French' AND cards.type = 'Creature' AND cards.layout = 'normal' AND cards.borderColor = 'black' AND cards.artist = 'Matthew D. Wilson'
```

**生成结果**:
(空结果)

**预期SQL**:
```sql
SELECT
  `name`
FROM `foreign_data`
WHERE
  `uuid` IN (
    SELECT
      `uuid`
    FROM `cards`
    WHERE
      `types` = 'Creature'
      AND `layout` = 'normal'
      AND `borderColor` = 'black'
      AND `artist` = 'Matthew D. Wilson'
  )
  AND `language` = 'French'
```

**预期结果**:
```json
[
  {
    "name": "Escouade de balistes"
  },
  {
    "name": "Reya Aubevenant"
  },
  {
    "name": "Tisseuse d'esprit"
  },
  {
    "name": "Étrangleur mou"
  },
  {
    "name": "Vampire de Mephidross"
  }
]
```
---

#### ID:459 | card_games

**问题**: Which card costs more converted mana, "Serra Angel" or "Shrine Keeper"?

**证据**: "Serra Angel" refers to name = 'Serra Angel'; "Shrine Keeper" refers to name = 'Shrine Keeper'; card costs more converted mana when the value of convertedManaCost is greater

**生成SQL**:
```sql
SELECT name, convertedManaCost FROM cards WHERE name IN ('Serra Angel', 'Shrine Keeper') ORDER BY convertedManaCost DESC
```

**生成结果**:
```json
[
  {
    "name": "Serra Angel",
    "convertedManaCost": 5.0
  },
  {
    "name": "Serra Angel",
    "convertedManaCost": 5.0
  },
  {
    "name": "Serra Angel",
    "convertedManaCost": 5.0
  },
  {
    "name": "Serra Angel",
    "convertedManaCost": 5.0
  },
  {
    "name": "Serra Angel",
    "convertedManaCost": 5.0
  }
]
```
**预期SQL**:
```sql
SELECT
  `name`
FROM `cards`
WHERE
  `name` IN ('Serra Angel', 'Shrine Keeper')
ORDER BY
  `convertedManaCost` DESC
LIMIT 1
```

**预期结果**:
```json
[
  {
    "name": "Serra Angel"
  }
]
```
---

#### ID:462 | card_games

**问题**: What's the Italian name of the set of cards with "Ancestor's Chosen" is in?

**证据**: Italian is a language which refers to language = 'Italian'; with "Ancestor's Chosen" in the card set refers to name = 'Ancestor''s Chosen'

**生成SQL**:
```sql
SELECT st.translation FROM cards c INNER JOIN set_translations st ON c.setCode = st.setCode WHERE c.name = 'Ancestor''s Chosen' AND st.language = 'Italian'
```

**生成结果**:
```json
[
  {
    "translation": "Set Base Decima Edizione"
  },
  {
    "translation": "Set Base Decima Edizione"
  },
  {
    "translation": "Sentenza"
  }
]
```
**预期SQL**:
```sql
SELECT
  `translation`
FROM `set_translations`
WHERE
  `setCode` IN (
    SELECT
      `setCode`
    FROM `cards`
    WHERE
      `name` = 'Ancestor''s Chosen'
  )
  AND `language` = 'Italian'
```

**预期结果**:
```json
[
  {
    "translation": "Set Base Decima Edizione"
  },
  {
    "translation": "Sentenza"
  }
]
```
---

#### ID:465 | card_games

**问题**: For the set of cards with "Ancestor's Chosen" in it, is there a Korean version of it?

**证据**: set of cards with "Ancestor''s Chosen" in it refers to name = 'Ancestor''s Chosen'; Korean version refers to language = 'Korean'

**生成SQL**:
```sql
SELECT EXISTS (SELECT 1 FROM foreign_data WHERE uuid IN (SELECT uuid FROM cards WHERE name = 'Ancestor''s Chosen') AND language = 'Korean') AS has_korean_version
```

**生成结果**:
```json
[
  {
    "has_korean_version": 0
  }
]
```
**预期SQL**:
```sql
SELECT
  CASE
    WHEN SUM(
      CASE
        WHEN `T2`.`language` = 'Korean' AND NOT `T2`.`translation` IS NULL
        THEN 1
        ELSE 0
      END
    ) > 0
    THEN 'YES'
    ELSE 'NO'
  END
FROM `cards` AS `T1`
INNER JOIN `set_translations` AS `T2`
  ON `T2`.`setCode` = `T1`.`setCode`
WHERE
  `T1`.`name` = 'Ancestor''s Chosen'
```

**预期结果**:
```json
[
  {
    "CASE\n    WHEN SUM(\n      CASE\n        WHEN `T2`.`language` = 'Korean' AND NOT `T2`.`translation` IS NULL\n        THEN 1\n        ELSE 0\n      END\n    ) > 0\n    THEN 'YES'\n    ELSE 'NO'\n  END": "YES"
  }
]
```
---

#### ID:469 | card_games

**问题**: Did the set of cards with "Angel of Mercy" appear on Magic: The Gathering Online?

**证据**: card set "Angel of Mercy" refers to name = 'Angel of Mercy'; appear on Magic: The Gathering Online refers to mtgoCode is NOT NULL and vice versa

**生成SQL**:
```sql
SELECT EXISTS (SELECT 1 FROM cards c INNER JOIN sets s ON c.setCode = s.code WHERE c.name = 'Angel of Mercy' AND s.mtgoCode IS NOT NULL) AS appears_on_mtgo;
```

**生成结果**:
```json
[
  {
    "appears_on_mtgo": 1
  }
]
```
**预期SQL**:
```sql
SELECT
  CASE WHEN NOT `T2`.`mtgoCode` IS NULL THEN 'YES' ELSE 'NO' END
FROM `cards` AS `T1`
INNER JOIN `sets` AS `T2`
  ON `T2`.`code` = `T1`.`setCode`
WHERE
  `T1`.`name` = 'Angel of Mercy'
```

**预期结果**:
```json
[
  {
    "CASE WHEN NOT `T2`.`mtgoCode` IS NULL THEN 'YES' ELSE 'NO' END": "YES"
  },
  {
    "CASE WHEN NOT `T2`.`mtgoCode` IS NULL THEN 'YES' ELSE 'NO' END": "YES"
  },
  {
    "CASE WHEN NOT `T2`.`mtgoCode` IS NULL THEN 'YES' ELSE 'NO' END": "YES"
  },
  {
    "CASE WHEN NOT `T2`.`mtgoCode` IS NULL THEN 'YES' ELSE 'NO' END": "YES"
  },
  {
    "CASE WHEN NOT `T2`.`mtgoCode` IS NULL THEN 'YES' ELSE 'NO' END": "YES"
  }
]
```
---

#### ID:473 | card_games

**问题**: Is the set of cards with Adarkar Valkyrie only available outside the United States?

**证据**: card set Adarkar Valkyrie refers to name = 'Adarkar Valkyrie'; isForeignOnly = 1 means only available outside the United States;

**生成SQL**:
```sql
SELECT isForeignOnly FROM sets WHERE code IN (SELECT setCode FROM cards WHERE name = 'Adarkar Valkyrie')
```

**生成结果**:
```json
[
  {
    "isForeignOnly": 0
  },
  {
    "isForeignOnly": 0
  },
  {
    "isForeignOnly": 0
  },
  {
    "isForeignOnly": 0
  },
  {
    "isForeignOnly": 0
  }
]
```
**预期SQL**:
```sql
SELECT
  CASE WHEN `isForeignOnly` = 1 THEN 'YES' ELSE 'NO' END
FROM `cards` AS `T1`
INNER JOIN `sets` AS `T2`
  ON `T2`.`code` = `T1`.`setCode`
WHERE
  `T1`.`name` = 'Adarkar Valkyrie'
```

**预期结果**:
```json
[
  {
    "CASE WHEN `isForeignOnly` = 1 THEN 'YES' ELSE 'NO' END": "NO"
  },
  {
    "CASE WHEN `isForeignOnly` = 1 THEN 'YES' ELSE 'NO' END": "NO"
  },
  {
    "CASE WHEN `isForeignOnly` = 1 THEN 'YES' ELSE 'NO' END": "NO"
  },
  {
    "CASE WHEN `isForeignOnly` = 1 THEN 'YES' ELSE 'NO' END": "NO"
  },
  {
    "CASE WHEN `isForeignOnly` = 1 THEN 'YES' ELSE 'NO' END": "NO"
  }
]
```
---

#### ID:474 | card_games

**问题**: Among the sets of cards that have an Italian translation, how many of them have a base set number of under 100?

**证据**: Italian translation refers to language = 'Italian'; have a translation means translation is not null; base set number of under 100 refers to baseSetSize < 10

**生成SQL**:
```sql
SELECT COUNT(*) AS count FROM sets INNER JOIN set_translations ON sets.code = set_translations.setCode WHERE set_translations.language = 'Italian' AND set_translations.translation IS NOT NULL AND sets.baseSetSize < 10
```

**生成结果**:
```json
[
  {
    "count": 0
  }
]
```
**预期SQL**:
```sql
SELECT
  COUNT(`T1`.`id`)
FROM `sets` AS `T1`
INNER JOIN `set_translations` AS `T2`
  ON `T2`.`setCode` = `T1`.`code`
WHERE
  NOT `T2`.`translation` IS NULL
  AND `T1`.`baseSetSize` < 100
  AND `T2`.`language` = 'Italian'
```

**预期结果**:
```json
[
  {
    "COUNT(`T1`.`id`)": 30
  }
]
```
---

#### ID:483 | card_games

**问题**: Please list the Italian text ruling of all the cards in the set Coldsnap.

**证据**: card set Coldsnap refers to name = 'Coldsnap'; Italian refers to language = 'Italian'

**生成SQL**:
```sql
SELECT cards.name, foreign_data.text FROM sets INNER JOIN cards ON sets.code = cards.setCode INNER JOIN foreign_data ON cards.uuid = foreign_data.uuid WHERE sets.name = 'Coldsnap' AND foreign_data.language = 'Italian'
```

**生成结果**:
```json
[
  {
    "name": "Adarkar Valkyrie",
    "text": "Volare, cautela\n{T}: Quando una creatura bersaglio diversa dalla Valchiria dell'Adarkar viene messa in un cimitero in questo turno, rimetti in gioco quella carta sotto il tuo controllo."
  },
  {
    "name": "Boreal Griffin",
    "text": "Volare\n{S}: Il Grifone di Borealia guadagna attacco improvviso fino alla fine del turno. ({S} può essere pagato con un mana da un permanente neve.)"
  },
  {
    "name": "Cover of Winter",
    "text": "Mantenimento cumulativo {S} ({S} può essere pagato con un mana da un permanente neve.)\nSe una creatura sta per infliggere danno da combattimento a te e/o a una o più creature che controlli, previeni X di quei danni, dove X è pari al numero di segnalini ep"
  },
  {
    "name": "Darien, King of Kjeldor",
    "text": "Ogniqualvolta ti viene inflitto danno, puoi mettere in gioco altrettante pedine creatura Soldato 1/1 bianche."
  },
  {
    "name": "Field Marshal",
    "text": "Gli altri Soldati prendono +1/+1 e hanno attacco improvviso."
  }
]
```
**预期SQL**:
```sql
SELECT DISTINCT
  `T1`.`text`
FROM `foreign_data` AS `T1`
INNER JOIN `cards` AS `T2`
  ON `T2`.`uuid` = `T1`.`uuid`
INNER JOIN `sets` AS `T3`
  ON `T3`.`code` = `T2`.`setCode`
WHERE
  `T3`.`name` = 'Coldsnap' AND `T1`.`language` = 'Italian'
```

**预期结果**:
```json
[
  {
    "text": "Volare, cautela\n{T}: Quando una creatura bersaglio diversa dalla Valchiria dell'Adarkar viene messa in un cimitero in questo turno, rimetti in gioco quella carta sotto il tuo controllo."
  },
  {
    "text": "Volare\n{S}: Il Grifone di Borealia guadagna attacco improvviso fino alla fine del turno. ({S} può essere pagato con un mana da un permanente neve.)"
  },
  {
    "text": "Mantenimento cumulativo {S} ({S} può essere pagato con un mana da un permanente neve.)\nSe una creatura sta per infliggere danno da combattimento a te e/o a una o più creature che controlli, previeni X di quei danni, dove X è pari al numero di segnalini ep"
  },
  {
    "text": "Ogniqualvolta ti viene inflitto danno, puoi mettere in gioco altrettante pedine creatura Soldato 1/1 bianche."
  },
  {
    "text": "Gli altri Soldati prendono +1/+1 e hanno attacco improvviso."
  }
]
```
---

#### ID:484 | card_games

**问题**: Please list the Italian names of the cards in the set Coldsnap with the highest converted mana cost.

**证据**: card set Coldsnap refers to name = 'Coldsnap'; Italian refers to language = 'Italian'; highest converted mana cost refers to MAX(convertedManaCost)

**生成SQL**:
```sql
SELECT fd.name FROM foreign_data fd INNER JOIN cards c ON fd.uuid = c.uuid WHERE c.setCode = (SELECT code FROM sets WHERE name = 'Coldsnap') AND fd.language = 'Italian' AND c.convertedManaCost = (SELECT MAX(convertedManaCost) FROM cards WHERE setCode = (SELECT code FROM sets WHERE name = 'Coldsnap'))
```

**生成结果**:
```json
[
  {
    "name": "Devastazione Solare"
  },
  {
    "name": "Requisire"
  },
  {
    "name": "Jokulmorder"
  },
  {
    "name": "Gufo Gelopiuma"
  },
  {
    "name": "Araldo di Leshrac"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T2`.`name`
FROM `foreign_data` AS `T1`
INNER JOIN `cards` AS `T2`
  ON `T2`.`uuid` = `T1`.`uuid`
INNER JOIN `sets` AS `T3`
  ON `T3`.`code` = `T2`.`setCode`
WHERE
  `T3`.`name` = 'Coldsnap' AND `T1`.`language` = 'Italian'
ORDER BY
  `T2`.`convertedManaCost` DESC
```

**预期结果**:
```json
[
  {
    "name": "Sunscour"
  },
  {
    "name": "Commandeer"
  },
  {
    "name": "Jokulmorder"
  },
  {
    "name": "Rimefeather Owl"
  },
  {
    "name": "Herald of Leshrac"
  }
]
```
---

#### ID:518 | card_games

**问题**: Which of the play format has the highest number of banned status? Indicate the play format and the names of all the card meet the condition.

**证据**: play format refers to format; banned status refers to status = 'Banned'; the highest number of banned status refers to MAX(COUNT(status = 'Banned'))

**生成SQL**:
```sql
SELECT l.format, c.name FROM legalities l INNER JOIN cards c ON l.uuid = c.uuid WHERE l.status = 'Banned' AND l.format IN (SELECT format FROM legalities WHERE status = 'Banned' GROUP BY format HAVING COUNT(*) = (SELECT MAX(banned_count) FROM (SELECT COUNT(*) as banned_count FROM legalities WHERE status = 'Banned' GROUP BY format) as sub))
```

**生成结果**:
```
❌ 执行失败
```

**预期SQL**:
```sql
SELECT T2.format, T1.name FROM cards AS T1 INNER JOIN legalities AS T2 ON T2.uuid = T1.uuid INNER JOIN ( SELECT format FROM legalities WHERE status = 'Banned' GROUP BY format ORDER BY COUNT(*) DESC LIMIT 1 ) AS MaxBanned ON MaxBanned.format = T2.format WHERE T2.status = 'Banned'
```

**预期结果**:
```json
[
  {
    "format": "legacy",
    "name": "Balance"
  },
  {
    "format": "legacy",
    "name": "Crusade"
  },
  {
    "format": "legacy",
    "name": "Ancestral Recall"
  },
  {
    "format": "legacy",
    "name": "Time Walk"
  },
  {
    "format": "legacy",
    "name": "Timetwister"
  }
]
```
---

#### ID:522 | card_games

**问题**: Which cards are ranked 1st on EDHRec? List all of the cards name and its banned play format.

**证据**: ranked 1st on EDHRec refers to edhrecRank = 1; banned refers to status = 'Banned'; play format refers to format; cards name refers to name

**生成SQL**:
```sql
SELECT c.name, l.format FROM cards c INNER JOIN legalities l ON c.uuid = l.uuid WHERE c.edhrecRank = 1 AND l.status = 'Banned'
```

**生成结果**:
```json
[
  {
    "name": "Sol Ring",
    "format": "duel"
  },
  {
    "name": "Sol Ring",
    "format": "legacy"
  },
  {
    "name": "Sol Ring",
    "format": "duel"
  },
  {
    "name": "Sol Ring",
    "format": "legacy"
  },
  {
    "name": "Sol Ring",
    "format": "duel"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T1`.`name`,
  `T2`.`format`
FROM `cards` AS `T1`
INNER JOIN `legalities` AS `T2`
  ON `T2`.`uuid` = `T1`.`uuid`
WHERE
  `T1`.`edhrecRank` = 1 AND `T2`.`status` = 'Banned'
GROUP BY
  `T1`.`name`,
  `T2`.`format`
```

**预期结果**:
```json
[
  {
    "name": "Sol Ring",
    "format": "duel"
  },
  {
    "name": "Sol Ring",
    "format": "legacy"
  }
]
```
---

#### ID:529 | card_games

**问题**: Find and list the names of sets which doesn't have Japanese translation but have Korean translation.

**证据**: names of sets refers to name; doesn't have Japanese translation refers to language not like '%Japanese%'; have Korean translation refers to language = 'Korean'

**生成SQL**:
```sql
SELECT DISTINCT s.name FROM sets s WHERE EXISTS (SELECT 1 FROM set_translations st WHERE st.setCode = s.code AND st.language = 'Korean') AND NOT EXISTS (SELECT 1 FROM set_translations st WHERE st.setCode = s.code AND st.language LIKE '%Japanese%')
```

**生成结果**:
(空结果)

**预期SQL**:
```sql
SELECT
  `name`
FROM `sets`
WHERE
  `code` IN (
    SELECT
      `setCode`
    FROM `set_translations`
    WHERE
      `language` = 'Korean' AND NOT `language` LIKE '%Japanese%'
  )
```

**预期结果**:
```json
[
  {
    "name": "Tenth Edition"
  },
  {
    "name": "Fourth Edition"
  },
  {
    "name": "Fifth Dawn"
  },
  {
    "name": "Fifth Edition"
  },
  {
    "name": "Classic Sixth Edition"
  }
]
```
---

#### ID:530 | card_games

**问题**: List all the frame styles and cards Allen Williams worked on and find any banned cards if there are any.

**证据**: frame styles refers to frameVersion; cards Allen Williams worked on refers to artist = 'Allen Williams'; banned cards refers to status = 'Banned'

**生成SQL**:
```sql
SELECT 'frameStyle' AS type, frameVersion AS value FROM cards GROUP BY frameVersion UNION ALL SELECT 'card' AS type, name AS value FROM cards WHERE artist = 'Allen Williams' UNION ALL SELECT 'banned' AS type, c.name AS value FROM cards c INNER JOIN legalities l ON c.uuid = l.uuid WHERE l.status = 'Banned'
```

**生成结果**:
```json
[
  {
    "type": "frameStyle",
    "value": "2003"
  },
  {
    "type": "frameStyle",
    "value": "1993"
  },
  {
    "type": "frameStyle",
    "value": "2015"
  },
  {
    "type": "frameStyle",
    "value": "1997"
  },
  {
    "type": "frameStyle",
    "value": "future"
  }
]
```
**预期SQL**:
```sql
SELECT DISTINCT
  `T1`.`frameVersion`,
  `T1`.`name`,
  CASE WHEN `T2`.`status` = 'Banned' THEN `T1`.`name` ELSE 'NO' END
FROM `cards` AS `T1`
INNER JOIN `legalities` AS `T2`
  ON `T1`.`uuid` = `T2`.`uuid`
WHERE
  `T1`.`artist` = 'Allen Williams'
```

**预期结果**:
```json
[
  {
    "frameVersion": "1997",
    "name": "Blinking Spirit",
    "CASE WHEN `T2`.`status` = 'Banned' THEN `T1`.`name` ELSE 'NO' END": "NO"
  },
  {
    "frameVersion": "1997",
    "name": "Kjeldoran Royal Guard",
    "CASE WHEN `T2`.`status` = 'Banned' THEN `T1`.`name` ELSE 'NO' END": "NO"
  },
  {
    "frameVersion": "1997",
    "name": "Enervate",
    "CASE WHEN `T2`.`status` = 'Banned' THEN `T1`.`name` ELSE 'NO' END": "NO"
  },
  {
    "frameVersion": "1997",
    "name": "Diminishing Returns",
    "CASE WHEN `T2`.`status` = 'Banned' THEN `T1`.`name` ELSE 'NO' END": "NO"
  },
  {
    "frameVersion": "2003",
    "name": "Blinking Spirit",
    "CASE WHEN `T2`.`status` = 'Banned' THEN `T1`.`name` ELSE 'NO' END": "NO"
  }
]
```
---

#### ID:197 | toxicology

**问题**: Calculate the average number of oxygen atoms in single-bonded molecules.

**证据**: single-bonded molecules refers to bond_type = '-' ; average number of oxygen atom = AVG(element = 'o')

**生成SQL**:
```sql
SELECT AVG(oxygen_count) FROM (SELECT molecule_id, COUNT(*) as oxygen_count FROM atom WHERE element = 'o' AND molecule_id IN (SELECT DISTINCT molecule_id FROM bond WHERE bond_type = '-') GROUP BY molecule_id) AS subquery
```

**生成结果**:
```json
[
  {
    "AVG(oxygen_count)": 3.1097
  }
]
```
**预期SQL**:
```sql
SELECT
  AVG(`oxygen_count`)
FROM (
  SELECT
    `T1`.`molecule_id`,
    COUNT(`T1`.`element`) AS `oxygen_count`
  FROM `atom` AS `T1`
  INNER JOIN `bond` AS `T2`
    ON `T1`.`molecule_id` = `T2`.`molecule_id`
  WHERE
    `T2`.`bond_type` = '-' AND `T1`.`element` = 'o'
  GROUP BY
    `T1`.`molecule_id`
) AS `oxygen_counts`
```

**预期结果**:
```json
[
  {
    "AVG(`oxygen_count`)": 99.6835
  }
]
```
---

#### ID:208 | toxicology

**问题**: Which type of label is the most numerous in atoms with hydrogen?

**证据**: with hydrogen refers to element = 'h'; label most numerous in atoms refers to MAX(COUNT(label)); 

**生成SQL**:
```sql
SELECT m.label FROM atom a INNER JOIN molecule m ON a.molecule_id = m.molecule_id WHERE a.element = 'h' GROUP BY m.label ORDER BY COUNT(a.atom_id) DESC LIMIT 1
```

**生成结果**:
```json
[
  {
    "label": "-"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T`.`label`
FROM (
  SELECT
    `T2`.`label`,
    COUNT(`T2`.`molecule_id`)
  FROM `atom` AS `T1`
  INNER JOIN `molecule` AS `T2`
    ON `T1`.`molecule_id` = `T2`.`molecule_id`
  WHERE
    `T1`.`element` = 'h'
  GROUP BY
    `T2`.`label`
  ORDER BY
    COUNT(`T2`.`molecule_id`) DESC
  LIMIT 1
) AS `t`
```

**预期结果**:
```
❌ 执行失败
```

---

#### ID:234 | toxicology

**问题**: How many bonds which involved atom 12 does molecule TR009 have?

**证据**: TR009 is the molecule id;  involved atom 12 refers to atom_id = 'TR009_12' or atom_id2 = 'TR009_12'

**生成SQL**:
```sql
SELECT COUNT(DISTINCT c.bond_id) FROM connected c INNER JOIN bond b ON c.bond_id = b.bond_id WHERE (c.atom_id = 'TR009_12' OR c.atom_id2 = 'TR009_12') AND b.molecule_id = 'TR009'
```

**生成结果**:
```json
[
  {
    "COUNT(DISTINCT c.bond_id)": 3
  }
]
```
**预期SQL**:
```sql
SELECT
  COUNT(`T2`.`bond_id`)
FROM `bond` AS `T1`
INNER JOIN `connected` AS `T2`
  ON `T1`.`bond_id` = `T2`.`bond_id`
WHERE
  `T1`.`molecule_id` = 'TR009'
  AND `T2`.`atom_id` = CONCAT(`T1`.`molecule_id`, '_1')
  OR `T2`.`atom_id2` = CONCAT(`T1`.`molecule_id`, '_2')
```

**预期结果**:
```json
[
  {
    "COUNT(`T2`.`bond_id`)": 1041
  }
]
```
---

#### ID:244 | toxicology

**问题**: Is the molecule with the most double bonds carcinogenic?

**证据**: double bond refers to bond_type = ' = '; label = '+' mean molecules are carcinogenic

**生成SQL**:
```sql
SELECT m.label FROM molecule m WHERE m.molecule_id = (SELECT b.molecule_id FROM bond b WHERE b.bond_type = ' = ' GROUP BY b.molecule_id ORDER BY COUNT(*) DESC LIMIT 1)
```

**生成结果**:
(空结果)

**预期SQL**:
```sql
SELECT
  `T1`.`label`
FROM `molecule` AS `T1`
INNER JOIN (
  SELECT
    `T`.`molecule_id`,
    COUNT(`T`.`bond_type`)
  FROM `bond` AS `T`
  WHERE
    `T`.`bond_type` = '='
  GROUP BY
    `T`.`molecule_id`
  ORDER BY
    COUNT(`T`.`bond_type`) DESC
  LIMIT 1
) AS `T2`
  ON `T1`.`molecule_id` = `T2`.`molecule_id`
```

**预期结果**:
```json
[
  {
    "label": "+"
  }
]
```
---

#### ID:245 | toxicology

**问题**: What is the average number of bonds the atoms with the element iodine have?

**证据**: atoms with the element iodine refers to element = 'i'; average = DIVIDE(COUND(bond_id), COUNT(atom_id)) where element = 'i'

**生成SQL**:
```sql
SELECT AVG(bond_count) AS avg_bonds_per_iodine_atom FROM (SELECT a.atom_id, COUNT(c.bond_id) AS bond_count FROM atom a LEFT JOIN connected c ON a.atom_id = c.atom_id OR a.atom_id = c.atom_id2 WHERE a.element = 'i' GROUP BY a.atom_id) AS sub
```

**生成结果**:
```json
[
  {
    "avg_bonds_per_iodine_atom": 2.0
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST(COUNT(`T2`.`bond_id`) AS DOUBLE) / COUNT(`T1`.`atom_id`)
FROM `atom` AS `T1`
INNER JOIN `connected` AS `T2`
  ON `T1`.`atom_id` = `T2`.`atom_id`
WHERE
  `T1`.`element` = 'i'
```

**预期结果**:
```json
[
  {
    "CAST(COUNT(`T2`.`bond_id`) AS DOUBLE) / COUNT(`T1`.`atom_id`)": 1.0
  }
]
```
---

#### ID:273 | toxicology

**问题**: What is the percentage of element chlorine in carcinogenic molecules?

**证据**: chlorine refers to element = 'cl'; label = '+' mean molecules are carcinogenic; percentage = DIVIDE(SUM(element = 'pb'); COUNT(molecule_id)) as percentage where label = '+'

**生成SQL**:
```sql
SELECT CAST(SUM(atom.element = 'cl') AS DOUBLE) / COUNT(DISTINCT molecule.molecule_id) AS percentage FROM molecule INNER JOIN atom ON molecule.molecule_id = atom.molecule_id WHERE molecule.label = '+'
```

**生成结果**:
```json
[
  {
    "percentage": 0.7631578947368421
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST(COUNT(CASE WHEN `T1`.`element` = 'cl' THEN `T1`.`element` ELSE NULL END) AS DOUBLE) * 100 / COUNT(`T1`.`element`)
FROM `atom` AS `T1`
INNER JOIN `molecule` AS `T2`
  ON `T1`.`molecule_id` = `T2`.`molecule_id`
WHERE
  `T2`.`label` = '+'
```

**预期结果**:
```json
[
  {
    "CAST(COUNT(CASE WHEN `T1`.`element` = 'cl' THEN `T1`.`element` ELSE NULL END) AS DOUBLE) * 100 / COUNT(`T1`.`element`)": 3.1419284940411703
  }
]
```
---

#### ID:327 | toxicology

**问题**: Which non-carcinogenic molecules consisted more than 5 atoms?

**证据**: label = '-' means molecules are non-carcinogenic; molecules consisted more than 5 atoms refers to COUNT(molecule_id) > 5

**生成SQL**:
```sql
SELECT molecule.molecule_id FROM molecule INNER JOIN atom ON molecule.molecule_id = atom.molecule_id WHERE molecule.label = '-' GROUP BY molecule.molecule_id HAVING COUNT(atom.atom_id) > 5
```

**生成结果**:
```json
[
  {
    "molecule_id": "TR002"
  },
  {
    "molecule_id": "TR004"
  },
  {
    "molecule_id": "TR007"
  },
  {
    "molecule_id": "TR008"
  },
  {
    "molecule_id": "TR009"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T`.`molecule_id`
FROM (
  SELECT
    `T1`.`molecule_id`,
    COUNT(`T2`.`atom_id`)
  FROM `molecule` AS `T1`
  INNER JOIN `atom` AS `T2`
    ON `T1`.`molecule_id` = `T2`.`molecule_id`
  WHERE
    `T1`.`label` = '-'
  GROUP BY
    `T1`.`molecule_id`
  HAVING
    COUNT(`T2`.`atom_id`) > 5
) AS `t`
```

**预期结果**:
```
❌ 执行失败
```

---

#### ID:23 | california_schools

**问题**: List the names of schools with more than 30 difference in enrollements between K-12 and ages 5-17? Please also give the full street adress of the schools.

**证据**: Diffrence in enrollement = `Enrollment (K-12)` - `Enrollment (Ages 5-17)`

**生成SQL**:
```sql
SELECT frpm.`School Name` AS school_name, CONCAT(schools.Street, ', ', schools.City, ', ', schools.Zip) AS full_address FROM frpm INNER JOIN schools ON frpm.CDSCode = schools.CDSCode WHERE (frpm.`Enrollment (K-12)` - frpm.`Enrollment (Ages 5-17)`) > 30;
```

**生成结果**:
```json
[
  {
    "school_name": "Alameda County Community",
    "full_address": "313 West Winton Avenue, Hayward, 94544-1136"
  },
  {
    "school_name": "California School for the Deaf-Fremont",
    "full_address": "39350 Gallaudet Drive, Fremont, 94538-2308"
  },
  {
    "school_name": "Alameda High",
    "full_address": "2201 Encinal Avenue, Alameda, 94501-4406"
  },
  {
    "school_name": "Encinal High",
    "full_address": "210 Central Avenue, Alameda, 94501-3278"
  },
  {
    "school_name": "Island High (Continuation)",
    "full_address": "1900 Third Street, Alameda, 94501-1851"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T1`.`School`,
  `T1`.`Street`
FROM `schools` AS `T1`
INNER JOIN `frpm` AS `T2`
  ON `T1`.`CDSCode` = `T2`.`CDSCode`
WHERE
  `T2`.`Enrollment (K-12)` - `T2`.`Enrollment (Ages 5-17)` > 30
```

**预期结果**:
```json
[
  {
    "School": "Alameda County Community",
    "Street": "313 West Winton Avenue"
  },
  {
    "School": "California School for the Deaf-Fremont",
    "Street": "39350 Gallaudet Drive"
  },
  {
    "School": "Alameda High",
    "Street": "2201 Encinal Avenue"
  },
  {
    "School": "Encinal High",
    "Street": "210 Central Avenue"
  },
  {
    "School": "Island High (Continuation)",
    "Street": "1900 Third Street"
  }
]
```
---

#### ID:25 | california_schools

**问题**: Name schools in Riverside which the average of average math score for SAT is grater than 400, what is the funding type of these schools?

**证据**: Average of average math = sum(average math scores) / count(schools).

**生成SQL**:
```sql
SELECT s.sname, sc.FundingType FROM satscores s INNER JOIN schools sc ON s.cds = sc.CDSCode WHERE s.cname = 'Riverside' AND (SELECT AVG(AvgScrMath) FROM satscores WHERE cname = 'Riverside') > 400
```

**生成结果**:
```json
[
  {
    "sname": null,
    "FundingType": null
  },
  {
    "sname": "River Springs Charter",
    "FundingType": "Directly funded"
  },
  {
    "sname": "Riverside County Education Academy",
    "FundingType": "Locally funded"
  },
  {
    "sname": "Come Back Kids",
    "FundingType": "Locally funded"
  },
  {
    "sname": "Gateway College and Career Academy",
    "FundingType": "Directly funded"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T1`.`sname`,
  `T2`.`Charter Funding Type`
FROM `satscores` AS `T1`
INNER JOIN `frpm` AS `T2`
  ON `T1`.`cds` = `T2`.`CDSCode`
WHERE
  `T2`.`District Name` LIKE 'Riverside%'
GROUP BY
  `T1`.`sname`,
  `T2`.`Charter Funding Type`
HAVING
  CAST(SUM(`T1`.`AvgScrMath`) AS DOUBLE) / COUNT(`T1`.`cds`) > 400
```

**预期结果**:
```json
[
  {
    "sname": "River Springs Charter",
    "Charter Funding Type": "Directly funded"
  },
  {
    "sname": "Arlington High",
    "Charter Funding Type": null
  },
  {
    "sname": "Martin Luther King Jr. High",
    "Charter Funding Type": null
  },
  {
    "sname": "John W. North High",
    "Charter Funding Type": null
  },
  {
    "sname": "Polytechnic High",
    "Charter Funding Type": null
  }
]
```
---

#### ID:26 | california_schools

**问题**: State the names and full communication address of high schools in Monterey which has more than 800 free or reduced price meals for ages 15-17?

**证据**: Full communication address should include Street, City, State and zip code if any.

**生成SQL**:
```sql
SELECT schools.School AS SchoolName, schools.Street, schools.City, schools.State, schools.Zip FROM schools INNER JOIN frpm ON schools.CDSCode = frpm.CDSCode WHERE frpm.`County Name` = 'Monterey' AND frpm.`School Type` LIKE '%High%' AND frpm.`FRPM Count (Ages 5-17)` > 800
```

**生成结果**:
```json
[
  {
    "SchoolName": "Alisal High",
    "Street": "777 Williams Road",
    "City": "Salinas",
    "State": "CA",
    "Zip": "93905-1907"
  },
  {
    "SchoolName": "Everett Alvarez High",
    "Street": "1900 Independence Boulevard",
    "City": "Salinas",
    "State": "CA",
    "Zip": "93906-5300"
  },
  {
    "SchoolName": "North Salinas High",
    "Street": "55 Kip Drive",
    "City": "Salinas",
    "State": "CA",
    "Zip": "93906-2908"
  },
  {
    "SchoolName": "Salinas High",
    "Street": "726 South Main Street",
    "City": "Salinas",
    "State": "CA",
    "Zip": "93901-3243"
  },
  {
    "SchoolName": "North Monterey County High",
    "Street": "13990 Castroville Boulevard",
    "City": "Castroville",
    "State": "CA",
    "Zip": "95012-9749"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T1`.`School Name`,
  `T2`.`Street`,
  `T2`.`City`,
  `T2`.`State`,
  `T2`.`Zip`
FROM `frpm` AS `T1`
INNER JOIN `schools` AS `T2`
  ON `T1`.`CDSCode` = `T2`.`CDSCode`
WHERE
  `T2`.`County` = 'Monterey'
  AND `T1`.`Free Meal Count (Ages 5-17)` > 800
  AND `T1`.`School Type` = 'High Schools (Public)'
```

**预期结果**:
```json
[
  {
    "School Name": "Alisal High",
    "Street": "777 Williams Road",
    "City": "Salinas",
    "State": "CA",
    "Zip": "93905-1907"
  },
  {
    "School Name": "Everett Alvarez High",
    "Street": "1900 Independence Boulevard",
    "City": "Salinas",
    "State": "CA",
    "Zip": "93906-5300"
  },
  {
    "School Name": "North Salinas High",
    "Street": "55 Kip Drive",
    "City": "Salinas",
    "State": "CA",
    "Zip": "93906-2908"
  },
  {
    "School Name": "Salinas High",
    "Street": "726 South Main Street",
    "City": "Salinas",
    "State": "CA",
    "Zip": "93901-3243"
  },
  {
    "School Name": "Soledad High",
    "Street": "425 Gabilan Drive",
    "City": "Soledad",
    "State": "CA",
    "Zip": "93960-3207"
  }
]
```
---

#### ID:27 | california_schools

**问题**: What is the average score in writing for the schools that were opened after 1991 or closed before 2000? List the school names along with the score. Also, list the communication number of the schools if there is any.

**证据**: Communication number refers to phone number.

**生成SQL**:
```sql
SELECT schools.School, satscores.AvgScrWrite, schools.Phone FROM satscores INNER JOIN schools ON satscores.cds = schools.CDSCode WHERE schools.OpenDate > '1991-12-31' OR schools.ClosedDate < '2000-01-01'
```

**生成结果**:
```json
[
  {
    "School": "FAME Public Charter",
    "AvgScrWrite": 505,
    "Phone": null
  },
  {
    "School": "Envision Academy for Arts & Technology",
    "AvgScrWrite": 395,
    "Phone": "(510) 596-8901"
  },
  {
    "School": "Aspire California College Preparatory Academy",
    "AvgScrWrite": null,
    "Phone": null
  },
  {
    "School": "Alameda Science and Technology Institute",
    "AvgScrWrite": 555,
    "Phone": "(510) 748-4021"
  },
  {
    "School": "Nea Community Learning Center",
    "AvgScrWrite": null,
    "Phone": "(510) 748-4008"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T2`.`School`,
  `T1`.`AvgScrWrite`,
  `T2`.`Phone`
FROM `schools` AS `T2`
LEFT JOIN `satscores` AS `T1`
  ON `T2`.`CDSCode` = `T1`.`cds`
WHERE
  DATE_FORMAT(CAST(`T2`.`OpenDate` AS DATETIME), '%Y') > '1991'
  OR DATE_FORMAT(CAST(`T2`.`ClosedDate` AS DATETIME), '%Y') < '2000'
```

**预期结果**:
```json
[
  {
    "School": "FAME Public Charter",
    "AvgScrWrite": 505,
    "Phone": null
  },
  {
    "School": "Envision Academy for Arts & Technology",
    "AvgScrWrite": 395,
    "Phone": "(510) 596-8901"
  },
  {
    "School": "Aspire California College Preparatory Academy",
    "AvgScrWrite": null,
    "Phone": null
  },
  {
    "School": "Community School for Creative Education",
    "AvgScrWrite": null,
    "Phone": "(510) 686-4131"
  },
  {
    "School": "Yu Ming Charter",
    "AvgScrWrite": null,
    "Phone": "(510) 452-2063"
  }
]
```
---

#### ID:31 | california_schools

**问题**: What is the eligible free rate of the 10th and 11th schools with the highest enrolment for students in grades 1 through 12?

**证据**: K-12 refers to students in grades 1 through 12; Eligible free rate for K-12 = `Free Meal Count (K-12)` / `Enrollment (K-12)`

**生成SQL**:
```sql
SELECT `School Name`, CAST(`Free Meal Count (K-12)` AS DOUBLE) / CAST(`Enrollment (K-12)` AS DOUBLE) AS eligible_free_rate FROM frpm ORDER BY `Enrollment (K-12)` DESC, CDSCode ASC LIMIT 9, 2;
```

**生成结果**:
```json
[
  {
    "School Name": "El Camino Real Charter High",
    "eligible_free_rate": 0.1344364012409514
  },
  {
    "School Name": "Eleanor Roosevelt High",
    "eligible_free_rate": 0.2905894519131334
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST(`Free Meal Count (K-12)` AS DOUBLE) / `Enrollment (K-12)`
FROM `frpm`
ORDER BY
  `Enrollment (K-12)` DESC
LIMIT 2
OFFSET 9
```

**预期结果**:
```json
[
  {
    "CAST(`Free Meal Count (K-12)` AS DOUBLE) / `Enrollment (K-12)`": 0.1344364012409514
  },
  {
    "CAST(`Free Meal Count (K-12)` AS DOUBLE) / `Enrollment (K-12)`": 0.2905894519131334
  }
]
```
---

#### ID:32 | california_schools

**问题**: What is the eligible free or reduced price meal rate for the top 5 schools in grades 1-12 with the highest free or reduced price meal count of the schools with the ownership code 66?

**证据**: grades 1-12 means K-12; Eligible free or reduced price meal rate for K-12 = `FRPM Count (K-12)` / `Enrollment (K-12)`

**生成SQL**:
```sql
SELECT schools.`School Name` AS school_name, CAST(frpm.`FRPM Count (K-12)` AS DOUBLE) / CAST(frpm.`Enrollment (K-12)` AS DOUBLE) AS eligible_free_or_reduced_price_meal_rate FROM schools INNER JOIN frpm ON schools.CDSCode = frpm.CDSCode WHERE schools.SOC = '66' ORDER BY frpm.`FRPM Count (K-12)` DESC LIMIT 5
```

**生成结果**:
```
❌ 执行失败
```

**预期SQL**:
```sql
SELECT
  CAST(`T1`.`FRPM Count (K-12)` AS DOUBLE) / `T1`.`Enrollment (K-12)`
FROM `frpm` AS `T1`
INNER JOIN `schools` AS `T2`
  ON `T1`.`CDSCode` = `T2`.`CDSCode`
WHERE
  `T2`.`SOC` = 66
ORDER BY
  `T1`.`FRPM Count (K-12)` DESC
LIMIT 5
```

**预期结果**:
```json
[
  {
    "CAST(`T1`.`FRPM Count (K-12)` AS DOUBLE) / `T1`.`Enrollment (K-12)`": 0.9179476526796843
  },
  {
    "CAST(`T1`.`FRPM Count (K-12)` AS DOUBLE) / `T1`.`Enrollment (K-12)`": 0.9993290841999329
  },
  {
    "CAST(`T1`.`FRPM Count (K-12)` AS DOUBLE) / `T1`.`Enrollment (K-12)`": 0.8964987714987716
  },
  {
    "CAST(`T1`.`FRPM Count (K-12)` AS DOUBLE) / `T1`.`Enrollment (K-12)`": 0.8958203368683718
  },
  {
    "CAST(`T1`.`FRPM Count (K-12)` AS DOUBLE) / `T1`.`Enrollment (K-12)`": 0.9141803553469662
  }
]
```
---

#### ID:37 | california_schools

**问题**: What is the complete address of the school with the lowest excellence rate? Indicate the Street, City, Zip and State.

**证据**: Execellence Rate = NumGE1500 / NumTstTakr; complete address has Street, City, State, Zip code

**生成SQL**:
```sql
SELECT s.Street, s.City, s.Zip, s.State FROM satscores sc INNER JOIN schools s ON sc.cds = s.CDSCode WHERE sc.NumTstTakr > 0 ORDER BY (sc.NumGE1500 / sc.NumTstTakr) ASC LIMIT 1
```

**生成结果**:
```json
[
  {
    "Street": "1900 Third Street",
    "City": "Alameda",
    "Zip": "94501-1851",
    "State": "CA"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T2`.`Street`,
  `T2`.`City`,
  `T2`.`State`,
  `T2`.`Zip`
FROM `satscores` AS `T1`
INNER JOIN `schools` AS `T2`
  ON `T1`.`cds` = `T2`.`CDSCode`
ORDER BY
  CAST(`T1`.`NumGE1500` AS DOUBLE) / `T1`.`NumTstTakr` ASC
LIMIT 1
```

**预期结果**:
```json
[
  {
    "Street": "2125 Jefferson Avenue",
    "City": "Berkeley",
    "State": "CA",
    "Zip": "94703-1414"
  }
]
```
---

#### ID:40 | california_schools

**问题**: What is the telephone number for the school with the lowest average score in reading in Fresno Unified?

**证据**: Fresno Unified is a name of district;

**生成SQL**:
```sql
SELECT s.Phone FROM satscores sat INNER JOIN schools s ON sat.cds = s.CDSCode WHERE s.District = 'Fresno Unified' ORDER BY sat.AvgScrRead ASC LIMIT 1;
```

**生成结果**:
```json
[
  {
    "Phone": "(559) 490-4290"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T2`.`Phone`
FROM `satscores` AS `T1`
INNER JOIN `schools` AS `T2`
  ON `T1`.`cds` = `T2`.`CDSCode`
WHERE
  `T2`.`District` = 'Fresno Unified' AND NOT `T1`.`AvgScrRead` IS NULL
ORDER BY
  `T1`.`AvgScrRead` ASC
LIMIT 1
```

**预期结果**:
```json
[
  {
    "Phone": "(559) 248-5100"
  }
]
```
---

#### ID:47 | california_schools

**问题**: What is the monthly average number of schools that opened in Alameda County under the jurisdiction of the Elementary School District in 1980?

**证据**: Elementary School District refers to DOC = 52; Monthly average number of schools that opened in 1980 = count(schools that opened in 1980) / 12

**生成SQL**:
```sql
SELECT CAST(COUNT(*) AS DOUBLE) / 12 AS monthly_average FROM schools WHERE County = 'Alameda County' AND DOC = '52' AND YEAR(OpenDate) = 1980
```

**生成结果**:
```json
[
  {
    "monthly_average": 0.0
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST(COUNT(`School`) AS DOUBLE) / 12
FROM `schools`
WHERE
  `DOC` = 52
  AND `County` = 'Alameda'
  AND DATE_FORMAT(CAST(`OpenDate` AS DATETIME), '%Y') = '1980'
```

**预期结果**:
```json
[
  {
    "CAST(COUNT(`School`) AS DOUBLE) / 12": 1.4166666666666667
  }
]
```
---

#### ID:48 | california_schools

**问题**: What is the ratio of merged Unified School District schools in Orange County to merged Elementary School District schools?

**证据**: Elementary School District refers to DOC = 52; Unified School District refers to DOC = 54.

**生成SQL**:
```sql
SELECT CAST((SELECT COUNT(*) FROM schools WHERE County = 'Orange County' AND DOC = '54') AS DOUBLE) / CAST((SELECT COUNT(*) FROM schools WHERE DOC = '52') AS DOUBLE) AS ratio
```

**生成结果**:
```json
[
  {
    "ratio": 0.0
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST(SUM(CASE WHEN `DOC` = 54 THEN 1 ELSE 0 END) AS DOUBLE) / SUM(CASE WHEN `DOC` = 52 THEN 1 ELSE 0 END)
FROM `schools`
WHERE
  `StatusType` = 'Merged' AND `County` = 'Orange'
```

**预期结果**:
```json
[
  {
    "CAST(SUM(CASE WHEN `DOC` = 54 THEN 1 ELSE 0 END) AS DOUBLE) / SUM(CASE WHEN `DOC` = 52 THEN 1 ELSE 0 END)": 0.5714285714285714
  }
]
```
---

#### ID:77 | california_schools

**问题**: Which schools served a grade span of Kindergarten to 9th grade in the county of Los Angeles and what is its Percent (%) Eligible FRPM (Ages 5-17)?

**证据**: Percent (%) Eligible FRPM (Ages 5-17) can be acquired by `FRPM Count (Ages 5-17)` / `Enrollment (Ages 5-17)` * 100

**生成SQL**:
```sql
SELECT `School Name`, CASE WHEN CAST(`Enrollment (Ages 5-17)` AS DOUBLE) = 0 THEN NULL ELSE CAST(`FRPM Count (Ages 5-17)` AS DOUBLE) / CAST(`Enrollment (Ages 5-17)` AS DOUBLE) * 100 END AS `Percent (%) Eligible FRPM (Ages 5-17)` FROM `frpm` WHERE `County Name` = 'Los Angeles' AND `Low Grade` = 'K' AND `High Grade` = '9'
```

**生成结果**:
(空结果)

**预期SQL**:
```sql
SELECT
  `T2`.`School`,
  `T1`.`FRPM Count (Ages 5-17)` * 100 / `T1`.`Enrollment (Ages 5-17)`
FROM `frpm` AS `T1`
INNER JOIN `schools` AS `T2`
  ON `T1`.`CDSCode` = `T2`.`CDSCode`
WHERE
  `T2`.`County` = 'Los Angeles' AND `T2`.`GSserved` = 'K-9'
```

**预期结果**:
```json
[
  {
    "School": "White Oak Elementary",
    "`T1`.`FRPM Count (Ages 5-17)` * 100 / `T1`.`Enrollment (Ages 5-17)`": 3.755868544600939
  },
  {
    "School": "The Accelerated",
    "`T1`.`FRPM Count (Ages 5-17)` * 100 / `T1`.`Enrollment (Ages 5-17)`": 97.63888888888889
  }
]
```
---

#### ID:79 | california_schools

**问题**: Between San Diego and Santa Barbara, which county offers the most number of schools that does not offer physical building? Indicate the amount.

**证据**: 'Does not offer physical building' means Virtual = F in the database.

**生成SQL**:
```sql
SELECT County, COUNT(*) AS school_count FROM schools WHERE County IN ('San Diego', 'Santa Barbara') AND Virtual = 'F' GROUP BY County ORDER BY school_count DESC LIMIT 1
```

**生成结果**:
```
❌ 执行失败
```

**预期SQL**:
```sql
SELECT
  `County`,
  COUNT(`Virtual`)
FROM `schools`
WHERE
  (
    `County` = 'San Diego' OR `County` = 'Santa Barbara'
  ) AND `Virtual` = 'F'
GROUP BY
  `County`
ORDER BY
  COUNT(`Virtual`) DESC
LIMIT 1
```

**预期结果**:
```json
[
  {
    "County": "San Diego",
    "COUNT(`Virtual`)": 8
  }
]
```
---

#### ID:85 | california_schools

**问题**: What is the Percent (%) Eligible Free (K-12) in the school administered by an administrator whose first name is Alusine. List the district code of the school.

**证据**: Percent (%) Eligible Free (K-12) = `Free Meal Count (K-12)` / `Enrollment (K-12)` * 100%

**生成SQL**:
```sql
SELECT frpm.`Percent (%) Eligible Free (K-12)`, frpm.`District Code` FROM schools INNER JOIN frpm ON schools.CDSCode = frpm.CDSCode WHERE schools.AdmFName1 = 'Alusine';
```

**生成结果**:
```json
[
  {
    "Percent (%) Eligible Free (K-12)": 0.70151133501259,
    "District Code": 64857
  }
]
```
**预期SQL**:
```sql
SELECT
  `T1`.`Free Meal Count (K-12)` * 100 / `T1`.`Enrollment (K-12)`,
  `T1`.`District Code`
FROM `frpm` AS `T1`
INNER JOIN `schools` AS `T2`
  ON `T1`.`CDSCode` = `T2`.`CDSCode`
WHERE
  `T2`.`AdmFName1` = 'Alusine'
```

**预期结果**:
```json
[
  {
    "`T1`.`Free Meal Count (K-12)` * 100 / `T1`.`Enrollment (K-12)`": 70.15113350125945,
    "District Code": 64857
  }
]
```
---

#### ID:95 | financial

**问题**: List out the account numbers of clients who are youngest and have highest average salary?

**证据**: If the person A's birthdate < B's birthdate, it means that person B is younger than person A; A11 refers to average salary

**生成SQL**:
```sql
SELECT DISTINCT account.account_id FROM account INNER JOIN disp ON account.account_id = disp.account_id INNER JOIN client ON disp.client_id = client.client_id INNER JOIN district ON account.district_id = district.district_id WHERE client.birth_date = (SELECT MAX(birth_date) FROM client) AND district.A11 = (SELECT MAX(A11) FROM district)
```

**生成结果**:
(空结果)

**预期SQL**:
```sql
SELECT
  `T1`.`account_id`
FROM `account` AS `T1`
INNER JOIN `disp` AS `T2`
  ON `T1`.`account_id` = `T2`.`account_id`
INNER JOIN `client` AS `T3`
  ON `T2`.`client_id` = `T3`.`client_id`
INNER JOIN `district` AS `T4`
  ON `T4`.`district_id` = `T1`.`district_id`
WHERE
  `T2`.`client_id` = (
    SELECT
      `client_id`
    FROM `client`
    ORDER BY
      `birth_date` DESC
    LIMIT 1
  )
GROUP BY
  `T4`.`A11`,
  `T1`.`account_id`
```

**预期结果**:
```json
[
  {
    "account_id": 2836
  }
]
```
---

#### ID:99 | financial

**问题**: Among the accounts who have loan validity more than 12 months, list out the accounts that have the highest approved amount and have account opening date in 1993.

**证据**: Loan validity more than 12 months refers to duration > 12

**生成SQL**:
```sql
SELECT a.account_id, MAX(l.amount) as max_approved_amount FROM loan l INNER JOIN account a ON l.account_id = a.account_id WHERE l.duration > 12 AND YEAR(a.date) = 1993 GROUP BY a.account_id HAVING MAX(l.amount) = (SELECT MAX(l2.amount) FROM loan l2 INNER JOIN account a2 ON l2.account_id = a2.account_id WHERE l2.duration > 12 AND YEAR(a2.date) = 1993))
```

**生成结果**:
```
❌ 执行失败
```

**预期SQL**:
```sql
SELECT
  `T1`.`account_id`
FROM `loan` AS `T1`
INNER JOIN `account` AS `T2`
  ON `T1`.`account_id` = `T2`.`account_id`
WHERE
  DATE_FORMAT(CAST(`T2`.`date` AS DATETIME), '%Y') = '1993'
  AND `T1`.`duration` > 12
ORDER BY
  `T1`.`amount` DESC
LIMIT 1
```

**预期结果**:
```json
[
  {
    "account_id": 10451
  }
]
```
---

#### ID:118 | financial

**问题**: For loan amount less than USD100,000, what is the percentage of accounts that is still running with no issue.

**证据**: Status = 'C' stands for running contract, ok so far; Percentage of accounts by condition = [(total(amount) & condition) / (total amount)] * 100.

**生成SQL**:
```sql
SELECT CAST((SELECT COUNT(DISTINCT account_id) FROM loan WHERE amount < 100000 AND status = 'C') AS DOUBLE) / CAST((SELECT COUNT(DISTINCT account_id) FROM loan) AS DOUBLE) * 100 AS percentage
```

**生成结果**:
```json
[
  {
    "percentage": 20.967741935483872
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST(SUM(`status` = 'C') AS DOUBLE) * 100 / COUNT(`account_id`)
FROM `loan`
WHERE
  `amount` < 100000
```

**预期结果**:
```json
[
  {
    "CAST(SUM(`status` = 'C') AS DOUBLE) * 100 / COUNT(`account_id`)": 46.885245901639344
  }
]
```
---

#### ID:128 | financial

**问题**: List the top nine districts, by descending order, from the highest to the lowest, the number of female account holders.

**证据**: A2 refers to districts; Female refers to gender = 'F'

**生成SQL**:
```sql
SELECT district.A2 AS district_name, COUNT(DISTINCT client.client_id) AS female_account_holders FROM client INNER JOIN disp ON client.client_id = disp.client_id INNER JOIN account ON disp.account_id = account.account_id INNER JOIN district ON account.district_id = district.district_id WHERE client.gender = 'F' GROUP BY district.district_id, district.A2 ORDER BY female_account_holders DESC LIMIT 9
```

**生成结果**:
```json
[
  {
    "district_name": "Hl.m. Praha",
    "female_account_holders": 334
  },
  {
    "district_name": "Karvina",
    "female_account_holders": 94
  },
  {
    "district_name": "Ostrava - mesto",
    "female_account_holders": 77
  },
  {
    "district_name": "Brno - mesto",
    "female_account_holders": 71
  },
  {
    "district_name": "Zlin",
    "female_account_holders": 57
  }
]
```
**预期SQL**:
```sql
SELECT
  `T2`.`A2`,
  COUNT(`T1`.`client_id`)
FROM `client` AS `T1`
INNER JOIN `district` AS `T2`
  ON `T1`.`district_id` = `T2`.`district_id`
WHERE
  `T1`.`gender` = 'F'
GROUP BY
  `T2`.`district_id`,
  `T2`.`A2`
ORDER BY
  COUNT(`T1`.`client_id`) DESC
LIMIT 9
```

**预期结果**:
```json
[
  {
    "A2": "Hl.m. Praha",
    "COUNT(`T1`.`client_id`)": 324
  },
  {
    "A2": "Karvina",
    "COUNT(`T1`.`client_id`)": 88
  },
  {
    "A2": "Ostrava - mesto",
    "COUNT(`T1`.`client_id`)": 84
  },
  {
    "A2": "Brno - mesto",
    "COUNT(`T1`.`client_id`)": 75
  },
  {
    "A2": "Zlin",
    "COUNT(`T1`.`client_id`)": 57
  }
]
```
---

#### ID:129 | financial

**问题**: Which are the top ten withdrawals (non-credit card) by district names for the month of January 1996?

**证据**: Non-credit card withdraws refers to type = 'VYDAJ'; January 1996 can be found by date LIKE '1996-01%' in the database; A2 means district names

**生成SQL**:
```sql
SELECT district.A2 AS district_name, SUM(trans.amount) AS total_withdrawal FROM trans INNER JOIN account ON trans.account_id = account.account_id INNER JOIN district ON account.district_id = district.district_id WHERE trans.type = 'VYDAJ' AND trans.date LIKE '1996-01%' GROUP BY district.A2 ORDER BY total_withdrawal DESC LIMIT 10
```

**生成结果**:
```json
[
  {
    "district_name": "Hl.m. Praha",
    "total_withdrawal": 6757078.0
  },
  {
    "district_name": "Karvina",
    "total_withdrawal": 1777590.0
  },
  {
    "district_name": "Ostrava - mesto",
    "total_withdrawal": 1712383.0
  },
  {
    "district_name": "Zlin",
    "total_withdrawal": 1622293.0
  },
  {
    "district_name": "Olomouc",
    "total_withdrawal": 1502053.0
  }
]
```
**预期SQL**:
```sql
SELECT DISTINCT
  `T1`.`A2`
FROM `district` AS `T1`
INNER JOIN `account` AS `T2`
  ON `T1`.`district_id` = `T2`.`district_id`
INNER JOIN `trans` AS `T3`
  ON `T2`.`account_id` = `T3`.`account_id`
WHERE
  `T3`.`type` = 'VYDAJ' AND `T3`.`date` LIKE '1996-01%'
ORDER BY
  `A2` ASC
LIMIT 10
```

**预期结果**:
```json
[
  {
    "A2": "Benesov"
  },
  {
    "A2": "Beroun"
  },
  {
    "A2": "Blansko"
  },
  {
    "A2": "Breclav"
  },
  {
    "A2": "Brno - mesto"
  }
]
```
---

#### ID:145 | financial

**问题**: Who are the account holder identification numbers whose who have transactions on the credit card with the amount is less than the average, in 1998?

**证据**: Operation = 'VYBER KARTOU' refers to credit card withdrawal

**生成SQL**:
```sql
SELECT DISTINCT T3.client_id FROM trans T1 INNER JOIN disp T2 ON T1.account_id = T2.account_id INNER JOIN client T3 ON T2.client_id = T3.client_id WHERE YEAR(T1.date) = 1998 AND T1.operation = 'VYBER KARTOU' AND T1.amount < (SELECT AVG(amount) FROM trans WHERE YEAR(date) = 1998 AND operation = 'VYBER KARTOU')
```

**生成结果**:
```json
[
  {
    "client_id": 19
  },
  {
    "client_id": 41
  },
  {
    "client_id": 51
  },
  {
    "client_id": 56
  },
  {
    "client_id": 57
  }
]
```
**预期SQL**:
```sql
SELECT
  `T1`.`account_id`
FROM `trans` AS `T1`
INNER JOIN `account` AS `T2`
  ON `T1`.`account_id` = `T2`.`account_id`
WHERE
  DATE_FORMAT(CAST(`T1`.`date` AS DATETIME), '%Y') = '1998'
  AND `T1`.`operation` = 'VYBER KARTOU'
  AND `T1`.`amount` < (
    SELECT
      AVG(`amount`)
    FROM `trans`
    WHERE
      DATE_FORMAT(CAST(`date` AS DATETIME), '%Y') = '1998'
  )
```

**预期结果**:
```json
[
  {
    "account_id": 14
  },
  {
    "account_id": 14
  },
  {
    "account_id": 14
  },
  {
    "account_id": 14
  },
  {
    "account_id": 14
  }
]
```
---

#### ID:152 | financial

**问题**: What is the average number of crimes committed in 1995 in regions where the number exceeds 4000 and the region has accounts that are opened starting from the year 1997?

**证据**: A3 refers to region names; A15 stands for the average number of crimes commited in 1995.

**生成SQL**:
```sql
SELECT AVG(A15) AS average_crimes_1995 FROM district WHERE A15 > 4000 AND district_id IN (SELECT district_id FROM account WHERE YEAR(date) >= 1997)
```

**生成结果**:
```json
[
  {
    "average_crimes_1995": 9675.0385
  }
]
```
**预期SQL**:
```sql
SELECT
  AVG(`T1`.`A15`)
FROM `district` AS `T1`
INNER JOIN `account` AS `T2`
  ON `T1`.`district_id` = `T2`.`district_id`
WHERE
  DATE_FORMAT(CAST(`T2`.`date` AS DATETIME), '%Y') >= '1997' AND `T1`.`A15` > 4000
```

**预期结果**:
```json
[
  {
    "AVG(`T1`.`A15`)": 29670.4495
  }
]
```
---

#### ID:168 | financial

**问题**: What percentage of clients who opened their accounts in the district with an average salary of over 10000 are women?

**证据**: Female refers to gender = 'F'; Woman and female are closed; Average salary can be found in A11

**生成SQL**:
```sql
SELECT (CAST(COUNT(CASE WHEN c.gender = 'F' THEN 1 END) AS DOUBLE) * 100.0 / CAST(COUNT(*) AS DOUBLE)) AS percentage FROM client c WHERE c.client_id IN (SELECT DISTINCT d.client_id FROM disp d WHERE d.account_id IN (SELECT a.account_id FROM account a WHERE a.district_id IN (SELECT di.district_id FROM district di WHERE di.A11 > 10000)))
```

**生成结果**:
```json
[
  {
    "percentage": 50.38819875776397
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST(SUM(`T2`.`gender` = 'F') AS DOUBLE) * 100 / COUNT(`T2`.`client_id`)
FROM `district` AS `T1`
INNER JOIN `client` AS `T2`
  ON `T1`.`district_id` = `T2`.`district_id`
WHERE
  `T1`.`A11` > 10000
```

**预期结果**:
```json
[
  {
    "CAST(SUM(`T2`.`gender` = 'F') AS DOUBLE) * 100 / COUNT(`T2`.`client_id`)": 49.609984399375975
  }
]
```
---

#### ID:186 | financial

**问题**: What percentage of male clients request for weekly statements to be issued?

**证据**: Percentage of male clients = [count(male clients who requested weekly statements / count(clients who requested weekly statements)] * 100%; Male means gender = 'M'; 'POPLATEK TYDNE' stands for weekly issuance

**生成SQL**:
```sql
SELECT CAST(COUNT(DISTINCT CASE WHEN C.gender = 'M' THEN C.client_id END) AS DOUBLE) / CAST(COUNT(DISTINCT C.client_id) AS DOUBLE) * 100 AS percentage FROM client C INNER JOIN disp D ON C.client_id = D.client_id INNER JOIN account A ON D.account_id = A.account_id WHERE A.frequency = 'POPLATEK TYDNE'
```

**生成结果**:
```json
[
  {
    "percentage": 52.12765957446809
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST(SUM(`T1`.`gender` = 'M') AS DOUBLE) * 100 / COUNT(`T1`.`client_id`)
FROM `client` AS `T1`
INNER JOIN `district` AS `T3`
  ON `T1`.`district_id` = `T3`.`district_id`
INNER JOIN `account` AS `T2`
  ON `T2`.`district_id` = `T3`.`district_id`
INNER JOIN `disp` AS `T4`
  ON `T1`.`client_id` = `T4`.`client_id` AND `T2`.`account_id` = `T4`.`account_id`
WHERE
  `T2`.`frequency` = 'POPLATEK TYDNE'
```

**预期结果**:
```json
[
  {
    "CAST(SUM(`T1`.`gender` = 'M') AS DOUBLE) * 100 / COUNT(`T1`.`client_id`)": 52.63157894736842
  }
]
```
---

#### ID:192 | financial

**问题**: What is the average amount of loan which are still on running contract with statement issuance after each transaction?

**证据**: status = 'C' stands for running contract, OK so far; status = 'D' stands for running contract, client in debt. 'POPLATEK PO OBRATU' stands for issuance after transaction

**生成SQL**:
```sql
SELECT AVG(CAST(loan.amount AS DOUBLE)) AS average_amount FROM loan WHERE loan.status IN ('C', 'D') AND EXISTS (SELECT 1 FROM trans WHERE trans.account_id = loan.account_id AND trans.k_symbol = 'POPLATEK PO OBRATU')
```

**生成结果**:
```json
[
  {
    "average_amount": null
  }
]
```
**预期SQL**:
```sql
SELECT
  AVG(`T2`.`amount`)
FROM `account` AS `T1`
INNER JOIN `loan` AS `T2`
  ON `T1`.`account_id` = `T2`.`account_id`
WHERE
  `T2`.`status` IN ('C', 'D') AND `T1`.`frequency` = 'POPLATEK PO OBRATU'
```

**预期结果**:
```json
[
  {
    "AVG(`T2`.`amount`)": 192836.5714
  }
]
```
---

#### ID:194 | financial

**问题**: Provide the IDs and age of the client with high level credit card, which is eligible for loans.

**证据**: the credit card is high-level refers to card.type = 'gold'; eligible for loans refers to disp.type = 'OWNER'

**生成SQL**:
```sql
SELECT c.client_id, TIMESTAMPDIFF(YEAR, c.birth_date, CURDATE()) AS age FROM client c INNER JOIN disp d ON c.client_id = d.client_id INNER JOIN card ca ON d.disp_id = ca.disp_id WHERE d.type = 'OWNER' AND ca.type = 'gold'
```

**生成结果**:
```json
[
  {
    "client_id": 9,
    "age": 90
  },
  {
    "client_id": 41,
    "age": 57
  },
  {
    "client_id": 79,
    "age": 56
  },
  {
    "client_id": 326,
    "age": 58
  },
  {
    "client_id": 548,
    "age": 88
  }
]
```
**预期SQL**:
```sql
SELECT
  `T1`.`client_id`,
  DATE_FORMAT(CAST(CURRENT_TIMESTAMP() AS DATETIME), '%Y') - DATE_FORMAT(CAST(`T3`.`birth_date` AS DATETIME), '%Y')
FROM `disp` AS `T1`
INNER JOIN `card` AS `T2`
  ON `T2`.`disp_id` = `T1`.`disp_id`
INNER JOIN `client` AS `T3`
  ON `T1`.`client_id` = `T3`.`client_id`
WHERE
  `T2`.`type` = 'gold' AND `T1`.`type` = 'OWNER'
```

**预期结果**:
```json
[
  {
    "client_id": 9,
    "DATE_FORMAT(CAST(CURRENT_TIMESTAMP() AS DATETIME), '%Y') - DATE_FORMAT(CAST(`T3`.`birth_date` AS DATETIME), '%Y')": 91.0
  },
  {
    "client_id": 41,
    "DATE_FORMAT(CAST(CURRENT_TIMESTAMP() AS DATETIME), '%Y') - DATE_FORMAT(CAST(`T3`.`birth_date` AS DATETIME), '%Y')": 58.0
  },
  {
    "client_id": 79,
    "DATE_FORMAT(CAST(CURRENT_TIMESTAMP() AS DATETIME), '%Y') - DATE_FORMAT(CAST(`T3`.`birth_date` AS DATETIME), '%Y')": 57.0
  },
  {
    "client_id": 326,
    "DATE_FORMAT(CAST(CURRENT_TIMESTAMP() AS DATETIME), '%Y') - DATE_FORMAT(CAST(`T3`.`birth_date` AS DATETIME), '%Y')": 59.0
  },
  {
    "client_id": 548,
    "DATE_FORMAT(CAST(CURRENT_TIMESTAMP() AS DATETIME), '%Y') - DATE_FORMAT(CAST(`T3`.`birth_date` AS DATETIME), '%Y')": 89.0
  }
]
```
---


### SIMPLE (45题)

#### ID:1500 | debit_card_specializing

**问题**: Please list the product description of the products consumed in September, 2013.

**证据**: September 2013 refers to 201309; The first 4 strings of the Date values in the yearmonth table can represent year; The 5th and 6th string of the date can refer to month.

**生成SQL**:
```sql
SELECT DISTINCT p.Description FROM transactions_1k t INNER JOIN products p ON t.ProductID = p.ProductID WHERE DATE_FORMAT(t.Date, '%Y%m') = '201309';
```

**生成结果**:
(空结果)

**预期SQL**:
```sql
SELECT
  `T3`.`Description`
FROM `transactions_1k` AS `T1`
INNER JOIN `yearmonth` AS `T2`
  ON `T1`.`CustomerID` = `T2`.`CustomerID`
INNER JOIN `products` AS `T3`
  ON `T1`.`ProductID` = `T3`.`ProductID`
WHERE
  `T2`.`Date` = '201309'
```

**预期结果**:
```json
[
  {
    "Description": "Nafta"
  },
  {
    "Description": "Nafta"
  },
  {
    "Description": "Provoz.nápl."
  },
  {
    "Description": "Natural"
  },
  {
    "Description": "Nafta"
  }
]
```
---

#### ID:1505 | debit_card_specializing

**问题**: Among the customers who paid in euro, how many of them have a monthly consumption of over 1000?

**证据**: Pays in euro = Currency = 'EUR'.

**生成SQL**:
```sql
SELECT COUNT(DISTINCT c.CustomerID) FROM customers c INNER JOIN yearmonth y ON c.CustomerID = y.CustomerID WHERE c.Currency = 'EUR' AND y.Consumption > 1000
```

**生成结果**:
```json
[
  {
    "COUNT(DISTINCT c.CustomerID)": 391
  }
]
```
**预期SQL**:
```sql
SELECT
  COUNT(*)
FROM `yearmonth` AS `T1`
INNER JOIN `customers` AS `T2`
  ON `T1`.`CustomerID` = `T2`.`CustomerID`
WHERE
  `T2`.`Currency` = 'EUR' AND `T1`.`Consumption` > 1000.00
```

**预期结果**:
```json
[
  {
    "COUNT(*)": 2730
  }
]
```
---

#### ID:1524 | debit_card_specializing

**问题**: What's the nationality of the customer who spent 548.4 in 2012/8/24?

**证据**: '2012/8/24' can be represented by '2012-08-24'

**生成SQL**:
```sql
SELECT c.Currency AS nationality FROM transactions_1k t INNER JOIN customers c ON t.CustomerID = c.CustomerID WHERE t.Date = '2012-08-24' AND t.Price = 548.4
```

**生成结果**:
```json
[
  {
    "nationality": "CZK"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T2`.`Country`
FROM `transactions_1k` AS `T1`
INNER JOIN `gasstations` AS `T2`
  ON `T1`.`GasStationID` = `T2`.`GasStationID`
WHERE
  `T1`.`Date` = '2012-08-24' AND  `T1`.`Price` = 548.4
```

**预期结果**:
```json
[
  {
    "Country": "CZE"
  }
]
```
---

#### ID:1525 | debit_card_specializing

**问题**: What is the percentage of the customers who used EUR in 2012/8/25?

**证据**: '2012/8/25' can be represented by '2012-08-25'

**生成SQL**:
```sql
SELECT (CAST(COUNT(DISTINCT CASE WHEN c.Currency = 'EUR' AND t.CustomerID IS NOT NULL THEN c.CustomerID END) AS DOUBLE) * 100) / CAST(COUNT(DISTINCT c.CustomerID) AS DOUBLE) AS percentage FROM customers c LEFT JOIN (SELECT DISTINCT CustomerID FROM transactions_1k WHERE Date = '2012-08-25') t ON c.CustomerID = t.CustomerID
```

**生成结果**:
```json
[
  {
    "percentage": 0.021564338744955485
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST(SUM(CASE WHEN `T2`.`Currency` = 'EUR' THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(`T1`.`CustomerID`)
FROM `transactions_1k` AS `T1`
INNER JOIN `customers` AS `T2`
  ON `T1`.`CustomerID` = `T2`.`CustomerID`
WHERE
  `T1`.`Date` = '2012-08-25'
```

**预期结果**:
```json
[
  {
    "CAST(SUM(CASE WHEN `T2`.`Currency` = 'EUR' THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(`T1`.`CustomerID`)": 1.6470588235294117
  }
]
```
---

#### ID:1422 | student_club

**问题**: State the category of events were held at MU 215.

**证据**: 'MU 215' is the location of event; 

**生成SQL**:
```sql
SELECT DISTINCT type FROM event WHERE location = 'MU 215'
```

**生成结果**:
```json
[
  {
    "type": "Election"
  },
  {
    "type": "Meeting"
  },
  {
    "type": "Guest Speaker"
  }
]
```
**预期SQL**:
```sql
SELECT DISTINCT
  `T2`.`category`
FROM `event` AS `T1`
INNER JOIN `budget` AS `T2`
  ON `T1`.`event_id` = `T2`.`link_to_event`
WHERE
  `T1`.`location` = 'MU 215'
```

**预期结果**:
```json
[
  {
    "category": "Advertisement"
  },
  {
    "category": "Food"
  },
  {
    "category": "Speaker Gifts"
  },
  {
    "category": "Parking"
  }
]
```
---

#### ID:1166 | thrombosis_prediction

**问题**: What are the symptoms observed by the youngest patient to ever did a medical examination? Identify their diagnosis.

**证据**: The larger the birthday value, the younger the person is, and vice versa; symptoms observed refers to the symptoms is not NULL

**生成SQL**:
```sql
SELECT e.Symptoms, p.Diagnosis FROM Examination e INNER JOIN Patient p ON e.ID = p.ID WHERE e.ID = (SELECT p2.ID FROM Patient p2 WHERE EXISTS (SELECT 1 FROM Examination e2 WHERE e2.ID = p2.ID) ORDER BY p2.Birthday DESC LIMIT 1) AND e.Symptoms IS NOT NULL
```

**生成结果**:
(空结果)

**预期SQL**:
```sql
SELECT
  `T2`.`Symptoms`,
  `T1`.`Diagnosis`
FROM `Patient` AS `T1`
INNER JOIN `Examination` AS `T2`
  ON `T1`.`ID` = `T2`.`ID`
WHERE
  NOT `T2`.`Symptoms` IS NULL
ORDER BY
  `T1`.`Birthday` DESC
LIMIT 1
```

**预期结果**:
```json
[
  {
    "Symptoms": "CNS susp",
    "Diagnosis": "SLE"
  }
]
```
---

#### ID:1251 | thrombosis_prediction

**问题**: How many patients with an Ig G higher than normal?

**证据**: Ig G higher than normal refers to IGG >= 2000; Should consider DISTINCT in the final result;

**生成SQL**:
```sql
SELECT COUNT(DISTINCT ID) FROM Laboratory WHERE IGG >= 2000
```

**生成结果**:
```json
[
  {
    "COUNT(DISTINCT ID)": 136
  }
]
```
**预期SQL**:
```sql
SELECT
  COUNT(DISTINCT `T1`.`ID`)
FROM `Patient` AS `T1`
INNER JOIN `Laboratory` AS `T2`
  ON `T1`.`ID` = `T2`.`ID`
INNER JOIN `Examination` AS `T3`
  ON `T3`.`ID` = `T2`.`ID`
WHERE
  `T2`.`IGG` >= 2000
```

**预期结果**:
```json
[
  {
    "COUNT(DISTINCT `T1`.`ID`)": 9
  }
]
```
---

#### ID:1035 | european_football_2

**问题**: Give the team_fifa_api_id of teams with more than 50 but less than 60 build-up play speed.

**证据**: teams with more than 50 but less than 60 build-up play speed refers to buildUpPlaySpeed >50 AND buildUpPlaySpeed <60; 

**生成SQL**:
```sql
SELECT T.team_fifa_api_id FROM Team T INNER JOIN Team_Attributes TA ON T.team_fifa_api_id = TA.team_fifa_api_id WHERE TA.buildUpPlaySpeed > 50 AND TA.buildUpPlaySpeed < 60
```

**生成结果**:
```json
[
  {
    "team_fifa_api_id": 434
  },
  {
    "team_fifa_api_id": 77
  },
  {
    "team_fifa_api_id": 77
  },
  {
    "team_fifa_api_id": 77
  },
  {
    "team_fifa_api_id": 614
  }
]
```
**预期SQL**:
```sql
SELECT DISTINCT
  `team_fifa_api_id`
FROM `Team_Attributes`
WHERE
  `buildUpPlaySpeed` > 50 AND `buildUpPlaySpeed` < 60
```

**预期结果**:
```json
[
  {
    "team_fifa_api_id": 1
  },
  {
    "team_fifa_api_id": 3
  },
  {
    "team_fifa_api_id": 4
  },
  {
    "team_fifa_api_id": 7
  },
  {
    "team_fifa_api_id": 10
  }
]
```
---

#### ID:1078 | european_football_2

**问题**: Which player is older, Aaron Lennon or Abdelaziz Barrada?

**证据**: The larger the birthday value, the younger the person is, and vice versa;

**生成SQL**:
```sql
SELECT player_name, birthday FROM Player WHERE player_name IN ('Aaron Lennon', 'Abdelaziz Barrada') ORDER BY birthday ASC;
```

**生成结果**:
```json
[
  {
    "player_name": "Aaron Lennon",
    "birthday": "1987-04-16 00:00:00"
  },
  {
    "player_name": "Abdelaziz Barrada",
    "birthday": "1989-06-19 00:00:00"
  }
]
```
**预期SQL**:
```sql
SELECT
  `player_name`
FROM `Player`
WHERE
  `player_name` IN ('Aaron Lennon', 'Abdelaziz Barrada')
ORDER BY
  `birthday` ASC
LIMIT 1
```

**预期结果**:
```json
[
  {
    "player_name": "Aaron Lennon"
  }
]
```
---

#### ID:1092 | european_football_2

**问题**: Give the name of the league had the most matches in the 2008/2009 season?

**证据**: league that had the most matches in the 2008/2009 season refers to MAX(league_name WHERE season = '2008/2009');

**生成SQL**:
```sql
SELECT l.name FROM League l WHERE l.id = (SELECT league_id FROM Match WHERE season = '2008/2009' GROUP BY league_id ORDER BY COUNT(*) DESC LIMIT 1)
```

**生成结果**:
```
❌ 执行失败
```

**预期SQL**:
```sql
SELECT `t1`.`name` FROM `League` AS `t1`JOIN `Match` AS `t2` ON `t1`.`id` = `t2`.`league_id` WHERE  `t2`.`season` = '2008/2009' GROUP BY  `t1`.`name` HAVING COUNT(`t2`.`id`) = (SELECT MAX(match_count) FROM (SELECT COUNT(`t2`.`id`) AS match_count FROM `Match` AS `t2` WHERE `t2`.`season` = '2008/2009' GROUP BY  `t2`.`league_id`) AS subquery)
```

**预期结果**:
```json
[
  {
    "name": "England Premier League"
  },
  {
    "name": "France Ligue 1"
  },
  {
    "name": "Italy Serie A"
  },
  {
    "name": "Spain LIGA BBVA"
  }
]
```
---

#### ID:1122 | european_football_2

**问题**: State the name of the most strongest player.

**证据**: strongest players refers to player has MAX(overall_rating)

**生成SQL**:
```sql
SELECT p.player_name FROM Player p INNER JOIN Player_Attributes pa ON p.player_api_id = pa.player_api_id WHERE pa.overall_rating = (SELECT MAX(overall_rating) FROM Player_Attributes)
```

**生成结果**:
```json
[
  {
    "player_name": "Lionel Messi"
  },
  {
    "player_name": "Lionel Messi"
  },
  {
    "player_name": "Lionel Messi"
  },
  {
    "player_name": "Lionel Messi"
  },
  {
    "player_name": "Lionel Messi"
  }
]
```
**预期SQL**:
```sql
SELECT DISTINCT t1.player_name FROM Player AS t1 INNER JOIN Player_Attributes AS t2 ON t1.player_api_id = t2.player_api_id WHERE t2.overall_rating = (SELECT MAX(overall_rating) FROM Player_Attributes)
```

**预期结果**:
```json
[
  {
    "player_name": "Lionel Messi"
  }
]
```
---

#### ID:1144 | european_football_2

**问题**: Please state the finishing rate and curve score of the player who has the heaviest weight.

**证据**: finishing rate refer to finishing; curve score refer to curve; heaviest weight refers to MAX(weight)

**生成SQL**:
```sql
SELECT pa.finishing, pa.curve FROM Player p INNER JOIN Player_Attributes pa ON p.player_api_id = pa.player_api_id WHERE p.weight = (SELECT MAX(weight) FROM Player)
```

**生成结果**:
```json
[
  {
    "finishing": 13,
    "curve": 13
  },
  {
    "finishing": 13,
    "curve": 13
  },
  {
    "finishing": 13,
    "curve": 13
  },
  {
    "finishing": 13,
    "curve": 13
  },
  {
    "finishing": 12,
    "curve": 12
  }
]
```
**预期SQL**:
```sql
SELECT
  `id`,
  `finishing`,
  `curve`
FROM `Player_Attributes`
WHERE
  `player_api_id` = (
    SELECT
      `player_api_id`
    FROM `Player`
    ORDER BY
      `weight` DESC
    LIMIT 1
  )
LIMIT 1
```

**预期结果**:
```json
[
  {
    "id": 98022,
    "finishing": 13,
    "curve": 13
  }
]
```
---

#### ID:1145 | european_football_2

**问题**: Which top 4 leagues had the most games in the 2015-2016 season?

**证据**: in the 2015-2016 season refers to season = '2015/2016'; league with most games refers to League.name where MAX(COUNT(id)); 

**生成SQL**:
```sql
SELECT League.name, COUNT(Match.id) as game_count FROM Match INNER JOIN League ON Match.league_id = League.id WHERE Match.season = '2015/2016' GROUP BY League.id, League.name ORDER BY game_count DESC LIMIT 4
```

**生成结果**:
```
❌ 执行失败
```

**预期SQL**:
```sql
SELECT
  `t1`.`name`
FROM `League` AS `t1`
INNER JOIN `Match` AS `t2`
  ON `t1`.`id` = `t2`.`league_id`
WHERE
  `t2`.`season` = '2015/2016'
GROUP BY
  `t1`.`name`
ORDER BY
  COUNT(`t2`.`id`) DESC
LIMIT 4
```

**预期结果**:
```json
[
  {
    "name": "Spain LIGA BBVA"
  },
  {
    "name": "England Premier League"
  },
  {
    "name": "France Ligue 1"
  },
  {
    "name": "Italy Serie A"
  }
]
```
---

#### ID:847 | formula_1

**问题**: What is the surname of the driver with the best lap time in race number 19 in the second qualifying period?

**证据**: race number refers to raceId; second qualifying period refers to q2; best lap time refers to MIN(q2);

**生成SQL**:
```sql
SELECT d.surname FROM drivers d WHERE d.driverId = (SELECT driverId FROM qualifying WHERE raceId = 19 ORDER BY q2 ASC LIMIT 1)
```

**生成结果**:
```json
[
  {
    "surname": "Nakajima"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T2`.`surname`
FROM `qualifying` AS `T1`
INNER JOIN `drivers` AS `T2`
  ON `T2`.`driverId` = `T1`.`driverId`
WHERE
  `T1`.`raceId` = 19
ORDER BY
  `T1`.`q2` ASC
LIMIT 1
```

**预期结果**:
```json
[
  {
    "surname": "Davidson"
  }
]
```
---

#### ID:850 | formula_1

**问题**: Please give the name of the race held on the circuits in Germany.

**证据**: Germany is a name of country;

**生成SQL**:
```sql
SELECT races.name FROM races INNER JOIN circuits ON races.circuitId = circuits.circuitId WHERE circuits.country = 'Germany'
```

**生成结果**:
```json
[
  {
    "name": "German Grand Prix"
  },
  {
    "name": "German Grand Prix"
  },
  {
    "name": "German Grand Prix"
  },
  {
    "name": "German Grand Prix"
  },
  {
    "name": "German Grand Prix"
  }
]
```
**预期SQL**:
```sql
SELECT DISTINCT
  `T2`.`name`
FROM `circuits` AS `T1`
INNER JOIN `races` AS `T2`
  ON `T2`.`circuitID` = `T1`.`circuitId`
WHERE
  `T1`.`country` = 'Germany'
```

**预期结果**:
```json
[
  {
    "name": "German Grand Prix"
  },
  {
    "name": "European Grand Prix"
  },
  {
    "name": "Luxembourg Grand Prix"
  }
]
```
---

#### ID:861 | formula_1

**问题**: What is his number of the driver who finished 0:01:54 in the Q3 of qualifying race No.903?

**证据**: race number refers to raceId; finished 0:0M:SS in the Q3 refers to q3 LIKE 'M:SS%'

**生成SQL**:
```sql
SELECT number FROM qualifying WHERE raceId = 903 AND q3 LIKE '0:01:54%'
```

**生成结果**:
(空结果)

**预期SQL**:
```sql
SELECT
  `T2`.`number`
FROM `qualifying` AS `T1`
INNER JOIN `drivers` AS `T2`
  ON `T2`.`driverId` = `T1`.`driverId`
WHERE
  `T1`.`raceId` = 903 AND `T1`.`q3` LIKE '1:54%'
```

**预期结果**:
```json
[
  {
    "number": 3
  },
  {
    "number": 5
  }
]
```
---

#### ID:868 | formula_1

**问题**: Where is Malaysian Grand Prix held? Give the location coordinates.

**证据**: location coordinates refers to (lat, lng); Malaysian Grand Prix refers to races.name = 'Malaysian Grand Prix'

**生成SQL**:
```sql
SELECT circuits.lat, circuits.lng FROM races INNER JOIN circuits ON races.circuitId = circuits.circuitId WHERE races.name = 'Malaysian Grand Prix'
```

**生成结果**:
```json
[
  {
    "lat": 2.76083,
    "lng": 101.738
  },
  {
    "lat": 2.76083,
    "lng": 101.738
  },
  {
    "lat": 2.76083,
    "lng": 101.738
  },
  {
    "lat": 2.76083,
    "lng": 101.738
  },
  {
    "lat": 2.76083,
    "lng": 101.738
  }
]
```
**预期SQL**:
```sql
SELECT DISTINCT
  `T1`.`lat`,
  `T1`.`lng`
FROM `circuits` AS `T1`
INNER JOIN `races` AS `T2`
  ON `T2`.`circuitID` = `T1`.`circuitId`
WHERE
  `T2`.`name` = 'Malaysian Grand Prix'
```

**预期结果**:
```json
[
  {
    "lat": 2.76083,
    "lng": 101.738
  }
]
```
---

#### ID:872 | formula_1

**问题**: In the race No. 45, for the driver who had the Q3 time as 0:01:33, what is his abbreviated code?

**证据**: race number refers to raceId; had the Q3 time as 0:0M:SS refers to q3 LIKE 'M:SS%'

**生成SQL**:
```sql
SELECT d.code FROM qualifying q INNER JOIN drivers d ON q.driverId = d.driverId WHERE q.raceId = 45 AND q.q3 = '0:01:33'
```

**生成结果**:
(空结果)

**预期SQL**:
```sql
SELECT
  `T2`.`code`
FROM `qualifying` AS `T1`
INNER JOIN `drivers` AS `T2`
  ON `T2`.`driverId` = `T1`.`driverId`
WHERE
  `T1`.`raceId` = 45 AND `T1`.`q3` LIKE '1:33%'
```

**预期结果**:
```json
[
  {
    "code": "HAM"
  }
]
```
---

#### ID:902 | formula_1

**问题**: Which race was Alex Yoong in when he was in track number less than 20?

**证据**: Alex Yoong refers to the full name of the driver; Full name of the driver refers to drivers.forename and drivers.surname;track number less than 10 refers to position < 20

**生成SQL**:
```sql
SELECT r.name, r.year FROM drivers d INNER JOIN results res ON d.driverId = res.driverId INNER JOIN races r ON res.raceId = r.raceId WHERE d.forename = 'Alex' AND d.surname = 'Yoong' AND res.position < 20
```

**生成结果**:
```json
[
  {
    "name": "Brazilian Grand Prix",
    "year": 2002
  },
  {
    "name": "Canadian Grand Prix",
    "year": 2002
  },
  {
    "name": "French Grand Prix",
    "year": 2002
  },
  {
    "name": "Italian Grand Prix",
    "year": 2002
  },
  {
    "name": "Japanese Grand Prix",
    "year": 2001
  }
]
```
**预期SQL**:
```sql
SELECT
  `T1`.`name`
FROM `races` AS `T1`
INNER JOIN `driverStandings` AS `T2`
  ON `T2`.`raceId` = `T1`.`raceId`
INNER JOIN `drivers` AS `T3`
  ON `T3`.`driverId` = `T2`.`driverId`
WHERE
  `T3`.`forename` = 'Alex' AND `T3`.`surname` = 'Yoong' AND `T2`.`position` < 20
```

**预期结果**:
```json
[
  {
    "name": "Malaysian Grand Prix"
  },
  {
    "name": "Brazilian Grand Prix"
  },
  {
    "name": "San Marino Grand Prix"
  },
  {
    "name": "Spanish Grand Prix"
  },
  {
    "name": "Austrian Grand Prix"
  }
]
```
---

#### ID:915 | formula_1

**问题**: Which country is the oldest driver from?

**证据**: date of birth refers to drivers.dob; The larger the birthday value, the younger the person is, and vice versa;

**生成SQL**:
```sql
SELECT nationality FROM drivers ORDER BY dob ASC LIMIT 1;
```

**生成结果**:
```json
[
  {
    "nationality": "South African"
  }
]
```
**预期SQL**:
```sql
SELECT
  `nationality`
FROM `drivers`
WHERE
  NOT `dob` IS NULL
ORDER BY
  `dob` ASC
LIMIT 1
```

**预期结果**:
```json
[
  {
    "nationality": "French"
  }
]
```
---

#### ID:930 | formula_1

**问题**: In which Formula_1 race did Lewis Hamilton rank the highest?

**证据**: rank the highest refers to min(rank); Lewis Hamilton refers to the full name of the driver; Full name of the driver refers to drivers.forename and drivers.surname;

**生成SQL**:
```sql
SELECT r.name FROM races r INNER JOIN results res ON r.raceId = res.raceId WHERE res.driverId = (SELECT driverId FROM drivers WHERE forename = 'Lewis' AND surname = 'Hamilton') AND res.rank IS NOT NULL ORDER BY res.rank ASC LIMIT 1
```

**生成结果**:
```json
[
  {
    "name": "Chinese Grand Prix"
  }
]
```
**预期SQL**:
```sql
SELECT
  `name`
FROM `races`
WHERE
  `raceId` IN (
    SELECT
      `raceId`
    FROM `results`
    WHERE
      `rank` = 1
      AND `driverId` = (
        SELECT
          `driverId`
        FROM `drivers`
        WHERE
          `forename` = 'Lewis' AND `surname` = 'Hamilton'
      )
  )
```

**预期结果**:
```json
[
  {
    "name": "Chinese Grand Prix"
  },
  {
    "name": "Malaysian Grand Prix"
  },
  {
    "name": "Japanese Grand Prix"
  },
  {
    "name": "Chinese Grand Prix"
  },
  {
    "name": "Spanish Grand Prix"
  }
]
```
---

#### ID:937 | formula_1

**问题**: What's the finish time for the driver who ranked second in 2008's Chinese Grand Prix?

**证据**: finish time refers to time; Chinese Grand Prix refers to races.name = 'Chinese Grand Prix';

**生成SQL**:
```sql
SELECT time FROM results WHERE raceId = (SELECT raceId FROM races WHERE year = 2008 AND name = 'Chinese Grand Prix') AND position = 2
```

**生成结果**:
```json
[
  {
    "time": "+14.925"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T1`.`time`
FROM `results` AS `T1`
INNER JOIN `races` AS `T2`
  ON `T1`.`raceId` = `T2`.`raceId`
WHERE
  `T1`.`rank` = 2 AND `T2`.`name` = 'Chinese Grand Prix' AND `T2`.`year` = 2008
```

**预期结果**:
```json
[
  {
    "time": "+16.445"
  }
]
```
---

#### ID:959 | formula_1

**问题**: What is the fastest lap number of the champion in 2009?

**证据**: in 2009 refers to year = 2009; Only the time of the champion shows in the format of "hour: minutes: seconds.millionsecond"

**生成SQL**:
```sql
SELECT fastestLap FROM results WHERE driverId = (SELECT driverId FROM driverStandings WHERE raceId IN (SELECT raceId FROM races WHERE year = 2009) GROUP BY driverId ORDER BY SUM(points) DESC LIMIT 1) AND raceId IN (SELECT raceId FROM races WHERE year = 2009) AND fastestLapTime IS NOT NULL ORDER BY STR_TO_DATE(fastestLapTime, '%k:%i:%s.%f') ASC LIMIT 1
```

**生成结果**:
```json
[
  {
    "fastestLap": 18
  }
]
```
**预期SQL**:
```sql
SELECT
  `T1`.`fastestLap`
FROM `results` AS `T1`
INNER JOIN `races` AS `T2`
  ON `T1`.`raceId` = `T2`.`raceId`
WHERE
  `T2`.`year` = 2009 AND `T1`.`time` LIKE '_:%:__.___'
```

**预期结果**:
```json
[
  {
    "fastestLap": 18
  },
  {
    "fastestLap": 42
  },
  {
    "fastestLap": 11
  },
  {
    "fastestLap": 17
  },
  {
    "fastestLap": 49
  }
]
```
---

#### ID:967 | formula_1

**问题**: State code numbers of top 3 yougest drivers. How many Netherlandic drivers among them?

**证据**: youngest driver refers to Max (year(dob)); Netherlandic and Dutch refer to the same country

**生成SQL**:
```sql
SELECT GROUP_CONCAT(code ORDER BY dob DESC) AS top_3_codes, SUM(CASE WHEN nationality = 'Dutch' THEN 1 ELSE 0 END) AS dutch_count FROM drivers WHERE driverId IN (SELECT driverId FROM drivers ORDER BY dob DESC LIMIT 3)
```

**生成结果**:
```
❌ 执行失败
```

**预期SQL**:
```sql
SELECT COUNT(*) FROM (SELECT `T1`.`nationality` FROM `drivers` AS `T1` ORDER BY `T1`.`dob` DESC LIMIT 3) AS `T3` WHERE `T3`.`nationality` = 'Dutch'
```

**预期结果**:
```json
[
  {
    "COUNT(*)": 1
  }
]
```
---

#### ID:978 | formula_1

**问题**: How many times the circuits were held in Austria? Please give their location and coordinates.

**证据**: location coordinates refers to (lat,lng); Austria refers to country = 'Austria';

**生成SQL**:
```sql
SELECT c.name AS circuit_name, c.location, c.lat, c.lng, COUNT(r.raceId) AS times_held FROM circuits c INNER JOIN races r ON c.circuitId = r.circuitId WHERE c.country = 'Austria' GROUP BY c.circuitId, c.name, c.location, c.lat, c.lng ORDER BY times_held DESC
```

**生成结果**:
```json
[
  {
    "circuit_name": "A1-Ring",
    "location": "Spielburg",
    "lat": 47.2197,
    "lng": 14.7647,
    "times_held": 25
  },
  {
    "circuit_name": "Red Bull Ring",
    "location": "Spielburg",
    "lat": 47.2197,
    "lng": 14.7647,
    "times_held": 4
  },
  {
    "circuit_name": "Zeltweg",
    "location": "Styria",
    "lat": 47.2039,
    "lng": 14.7478,
    "times_held": 1
  }
]
```
**预期SQL**:
```sql
SELECT DISTINCT
  `location`,
  `lat`,
  `lng`
FROM `circuits`
WHERE
  `country` = 'Austria'
```

**预期结果**:
```json
[
  {
    "location": "Spielburg",
    "lat": 47.2197,
    "lng": 14.7647
  },
  {
    "location": "Styria",
    "lat": 47.2039,
    "lng": 14.7478
  }
]
```
---

#### ID:533 | codebase_community

**问题**: How many users last accessed the website after 2014/9/1?

**证据**: last accessed after 2014/9/1 refers to LastAccessDate > '2014-09-01'

**生成SQL**:
```sql
SELECT COUNT(*) FROM users WHERE LastAccessDate > '2014-09-01'
```

**生成结果**:
```json
[
  {
    "COUNT(*)": 5146
  }
]
```
**预期SQL**:
```sql
SELECT
  COUNT(`Id`)
FROM `users`
WHERE
  DATE(`LastAccessDate`) > '2014-09-01'
```

**预期结果**:
```json
[
  {
    "COUNT(`Id`)": 4941
  }
]
```
---

#### ID:539 | codebase_community

**问题**: Who is the owner of the post "Eliciting priors from experts"?

**证据**: "Eliciting priors from experts" is the Title of post; owner refers to DisplayName

**生成SQL**:
```sql
SELECT OwnerDisplayName FROM posts WHERE Title = 'Eliciting priors from experts'
```

**生成结果**:
```json
[
  {
    "OwnerDisplayName": null
  }
]
```
**预期SQL**:
```sql
SELECT
  `T2`.`DisplayName`
FROM `posts` AS `T1`
INNER JOIN `users` AS `T2`
  ON `T1`.`OwnerUserId` = `T2`.`Id`
WHERE
  `T1`.`Title` = 'Eliciting priors from experts'
```

**预期结果**:
```json
[
  {
    "DisplayName": "csgillespie"
  }
]
```
---

#### ID:576 | codebase_community

**问题**: Name the user that commented 'thank you user93!'

**证据**: "thank you user93" is the Text of comment; user refers to DisplayName

**生成SQL**:
```sql
SELECT UserDisplayName FROM comments WHERE Text = 'thank you user93!';
```

**生成结果**:
```json
[
  {
    "UserDisplayName": null
  }
]
```
**预期SQL**:
```sql
SELECT
  `T1`.`DisplayName`
FROM `users` AS `T1`
INNER JOIN `comments` AS `T2`
  ON `T1`.`Id` = `T2`.`UserId`
WHERE
  `T2`.`Text` = 'thank you user93!'
```

**预期结果**:
```json
[
  {
    "DisplayName": "Preets"
  }
]
```
---

#### ID:671 | codebase_community

**问题**: What is the display name of the user who acquired the first Autobiographer badge?

**证据**: Autobiographer is the name of the badge; acquired the first refers to MIN(Date);

**生成SQL**:
```sql
SELECT u.DisplayName FROM badges b INNER JOIN users u ON b.UserId = u.Id WHERE b.Name = 'Autobiographer' AND b.Date = (SELECT MIN(Date) FROM badges WHERE Name = 'Autobiographer')
```

**生成结果**:
```json
[
  {
    "DisplayName": "Geoff Dalgas"
  },
  {
    "DisplayName": "Jarrod Dixon"
  },
  {
    "DisplayName": "Vince"
  },
  {
    "DisplayName": "csgillespie"
  },
  {
    "DisplayName": "Pierre"
  }
]
```
**预期SQL**:
```sql
SELECT
  `T1`.`DisplayName`
FROM `users` AS `T1`
INNER JOIN `badges` AS `T2`
  ON `T1`.`Id` = `T2`.`UserId`
WHERE
  `T2`.`Name` = 'Autobiographer'
ORDER BY
  `T2`.`Date`
LIMIT 1
```

**预期结果**:
```json
[
  {
    "DisplayName": "Jin"
  }
]
```
---

#### ID:710 | codebase_community

**问题**: In posts with 1 comment, how many of the comments have 0 score?

**证据**: in posts with 1 comment refers to CommentCount = 1;

**生成SQL**:
```sql
SELECT COUNT(*) FROM comments c INNER JOIN posts p ON c.PostId = p.Id WHERE p.CommentCount = 1 AND c.Score = 0
```

**生成结果**:
```json
[
  {
    "COUNT(*)": 10997
  }
]
```
**预期SQL**:
```sql
SELECT
  COUNT(`T1`.`id`)
FROM `comments` AS `T1`
INNER JOIN `posts` AS `T2`
  ON `T1`.`PostId` = `T2`.`Id`
WHERE
  `T2`.`CommentCount` = 1 AND `T2`.`Score` = 0
```

**预期结果**:
```json
[
  {
    "COUNT(`T1`.`id`)": 2888
  }
]
```
---

#### ID:340 | card_games

**问题**: Which are the cards that have incredibly powerful foils.

**证据**: incredibly poweful foils refers to cardKingdomFoilId is not null AND cardKingdomId is not null

**生成SQL**:
```sql
SELECT name FROM cards WHERE cardKingdomFoilId IS NOT NULL AND cardKingdomId IS NOT NULL
```

**生成结果**:
```json
[
  {
    "name": "Ballista Squad"
  },
  {
    "name": "Bandage"
  },
  {
    "name": "Beacon of Immortality"
  },
  {
    "name": "Cho-Manno, Revolutionary"
  },
  {
    "name": "Condemn"
  }
]
```
**预期SQL**:
```sql
SELECT
  `id`
FROM `cards`
WHERE
  NOT `cardKingdomFoilId` IS NULL AND NOT `cardKingdomId` IS NULL
```

**预期结果**:
```json
[
  {
    "id": 4
  },
  {
    "id": 5
  },
  {
    "id": 6
  },
  {
    "id": 9
  },
  {
    "id": 10
  }
]
```
---

#### ID:341 | card_games

**问题**: What are the borderless cards available without powerful foils?

**证据**: borderless' refers to borderColor; poweful foils refers to cardKingdomFoilId paired with cardKingdomId AND cardKingdomId is not null

**生成SQL**:
```sql
SELECT id, name, uuid, borderColor, cardKingdomId, cardKingdomFoilId FROM cards WHERE borderColor = 'borderless' AND (cardKingdomId IS NULL OR cardKingdomFoilId IS NULL)
```

**生成结果**:
```json
[
  {
    "id": 23004,
    "name": "Void Beckoner",
    "uuid": "5b62d7ac-440b-58f9-8086-a002d074cfd0",
    "borderColor": "borderless",
    "cardKingdomId": null,
    "cardKingdomFoilId": null
  },
  {
    "id": 25350,
    "name": "Valki, God of Lies // Tibalt, Cosmic Impostor",
    "uuid": "88be86ce-90b6-5d9d-b132-044c41baf7f1",
    "borderColor": "borderless",
    "cardKingdomId": null,
    "cardKingdomFoilId": null
  },
  {
    "id": 25355,
    "name": "Barkchannel Pathway // Tidechannel Pathway",
    "uuid": "1bd0076a-80ad-59f7-bb8d-9dc5e3cc92ef",
    "borderColor": "borderless",
    "cardKingdomId": null,
    "cardKingdomFoilId": null
  },
  {
    "id": 25357,
    "name": "Blightstep Pathway // Searstep Pathway",
    "uuid": "1da37e87-57bf-5a70-aaf2-aad976848548",
    "borderColor": "borderless",
    "cardKingdomId": null,
    "cardKingdomFoilId": null
  },
  {
    "id": 25359,
    "name": "Darkbore Pathway // Slitherbore Pathway",
    "uuid": "8dbc37a4-d21a-5539-8e45-ef2955a0456d",
    "borderColor": "borderless",
    "cardKingdomId": null,
    "cardKingdomFoilId": null
  }
]
```
**预期SQL**:
```sql
SELECT
  `id`
FROM `cards`
WHERE
  `borderColor` = 'borderless'
  AND (
    `cardKingdomId` IS NULL OR `cardKingdomId` IS NULL
  )
```

**预期结果**:
```json
[
  {
    "id": 23004
  },
  {
    "id": 25350
  },
  {
    "id": 25355
  },
  {
    "id": 25357
  },
  {
    "id": 25359
  }
]
```
---

#### ID:358 | card_games

**问题**: What is the border color of card "Ancestor's Chosen"?

**证据**: name of card  = 'Ancestor''s Chosen' ;

**生成SQL**:
```sql
SELECT borderColor FROM cards WHERE name = 'Ancestor''s Chosen'
```

**生成结果**:
```json
[
  {
    "borderColor": "black"
  },
  {
    "borderColor": "black"
  },
  {
    "borderColor": "black"
  },
  {
    "borderColor": "black"
  }
]
```
**预期SQL**:
```sql
SELECT DISTINCT
  `borderColor`
FROM `cards`
WHERE
  `name` = 'Ancestor''s Chosen'
```

**预期结果**:
```json
[
  {
    "borderColor": "black"
  }
]
```
---

#### ID:366 | card_games

**问题**: What is the rule of playing card "Benalish Knight"?

**证据**: Benalish Knight' is the name of card; rule of playing card refers to format;

**生成SQL**:
```sql
SELECT l.format, l.status FROM legalities l WHERE l.uuid = (SELECT uuid FROM cards WHERE name = 'Benalish Knight')
```

**生成结果**:
```
❌ 执行失败
```

**预期SQL**:
```sql
SELECT
  `T2`.`format`
FROM `cards` AS `T1`
INNER JOIN `legalities` AS `T2`
  ON `T1`.`uuid` = `T2`.`uuid`
WHERE
  `T1`.`name` = 'Benalish Knight'
```

**预期结果**:
```json
[
  {
    "format": "commander"
  },
  {
    "format": "duel"
  },
  {
    "format": "legacy"
  },
  {
    "format": "modern"
  },
  {
    "format": "pauper"
  }
]
```
---

#### ID:377 | card_games

**问题**: How many cards with original type of "Summon - Angel" have subtype other than "Angel"?

**证据**: subtype other than Angel refers to subtypes is not 'Angel';

**生成SQL**:
```sql
SELECT COUNT(*) FROM cards WHERE originalType = 'Summon - Angel' AND (subtypes IS NULL OR subtypes NOT LIKE '%Angel%');
```

**生成结果**:
```json
[
  {
    "COUNT(*)": 0
  }
]
```
**预期SQL**:
```sql
SELECT
  COUNT(`id`)
FROM `cards`
WHERE
  `originalType` = 'Summon - Angel' AND `subtypes` <> 'Angel'
```

**预期结果**:
```json
[
  {
    "COUNT(`id`)": 3
  }
]
```
---

#### ID:383 | card_games

**问题**: How many of the banned cards are white border?

**证据**: banned card refers to status = 'Banned'; white border refers to borderColor = 'white';

**生成SQL**:
```sql
SELECT COUNT(DISTINCT c.uuid) FROM cards c INNER JOIN legalities l ON c.uuid = l.uuid WHERE l.status = 'Banned' AND c.borderColor = 'white'
```

**生成结果**:
```json
[
  {
    "COUNT(DISTINCT c.uuid)": 89
  }
]
```
**预期SQL**:
```sql
SELECT
  COUNT(`T1`.`id`)
FROM `cards` AS `T1`
INNER JOIN `legalities` AS `T2`
  ON `T1`.`uuid` = `T2`.`uuid`
WHERE
  `T2`.`status` = 'Banned' AND `T1`.`borderColor` = 'white'
```

**预期结果**:
```json
[
  {
    "COUNT(`T1`.`id`)": 258
  }
]
```
---

#### ID:424 | card_games

**问题**: What proportion of cards do not have a text box with a normal layout?

**证据**: do not have a text box refers to isTextless = 1; proportion refers to DIVIDE(COUNT(Textless = 1 and layout = 'normal'),COUNT(Textless))*100

**生成SQL**:
```sql
SELECT (SUM(layout = 'normal') / CAST(COUNT(*) AS DOUBLE)) * 100 AS proportion FROM cards WHERE isTextless = 1
```

**生成结果**:
```json
[
  {
    "proportion": 100.0
  }
]
```
**预期SQL**:
```sql
SELECT
  CAST(SUM(CASE WHEN `isTextless` = 1 AND `layout` = 'normal' THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(*)
FROM `cards`
```

**预期结果**:
```json
[
  {
    "CAST(SUM(CASE WHEN `isTextless` = 1 AND `layout` = 'normal' THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(*)": 0.20238639963394459
  }
]
```
---

#### ID:440 | card_games

**问题**: Which foreign language used by "A Pedra Fellwar"?

**证据**: "A Pedra Fellwar" refers to name = 'A Pedra Fellwar'

**生成SQL**:
```sql
SELECT DISTINCT fd.language FROM cards c INNER JOIN foreign_data fd ON c.uuid = fd.uuid WHERE c.name = 'A Pedra Fellwar'
```

**生成结果**:
(空结果)

**预期SQL**:
```sql
SELECT DISTINCT
  `language`
FROM `foreign_data`
WHERE
  `name` = 'A Pedra Fellwar'
```

**预期结果**:
```json
[
  {
    "language": "Portuguese (Brazil)"
  }
]
```
---

#### ID:227 | toxicology

**问题**: What is the percentage of molecules that are carcinogenic? Please provide your answer as a percentage with three decimal places.

**证据**: label = '+' mean molecules are carcinogenic; percentage = DIVIDE(SUM(label = '+'), COUNT(molecule_id)) as percent

**生成SQL**:
```sql
SELECT ROUND((CAST(SUM(label = '+') AS DOUBLE) / COUNT(*)) * 100, 3) AS percentage FROM molecule
```

**生成结果**:
```json
[
  {
    "percentage": 44.315
  }
]
```
**预期SQL**:
```sql
SELECT
  ROUND(
    CAST(COUNT(CASE WHEN `T`.`label` = '+' THEN `T`.`molecule_id` ELSE NULL END) AS DOUBLE) * 100 / COUNT(`T`.`molecule_id`),
    3
  )
FROM `molecule` AS `t`
```

**预期结果**:
```
❌ 执行失败
```

---

#### ID:239 | toxicology

**问题**: How many connections does the atom 19 have?

**证据**: connections refers to bond_id; atom 19 refers to atom_id like 'TR%_19';

**生成SQL**:
```sql
SELECT COUNT(*) AS connection_count FROM connected WHERE atom_id LIKE 'TR%_19' OR atom_id2 LIKE 'TR%_19'
```

**生成结果**:
```json
[
  {
    "connection_count": 754
  }
]
```
**预期SQL**:
```sql
SELECT
  COUNT(`T`.`bond_id`)
FROM `connected` AS `T`
WHERE
  SUBSTR(`T`.`atom_id`, -2) = '19'
```

**预期结果**:
```json
[
  {
    "COUNT(`T`.`bond_id`)": 377
  }
]
```
---

#### ID:17 | california_schools

**问题**: Rank schools by their average score in Writing where the score is greater than 499, showing their charter numbers.

**证据**: Valid charter number means the number is not null

**生成SQL**:
```sql
SELECT s.sname, s.AvgScrWrite, sch.CharterNum FROM satscores s INNER JOIN schools sch ON s.cds = sch.CDSCode WHERE s.AvgScrWrite > 499 AND sch.CharterNum IS NOT NULL ORDER BY s.AvgScrWrite DESC
```

**生成结果**:
```json
[
  {
    "sname": "Pacific Collegiate Charter",
    "AvgScrWrite": 630,
    "CharterNum": "0210"
  },
  {
    "sname": "University High",
    "AvgScrWrite": 593,
    "CharterNum": "0890"
  },
  {
    "sname": "OCSA",
    "AvgScrWrite": 582,
    "CharterNum": "0290"
  },
  {
    "sname": "Alameda Community Learning Center",
    "AvgScrWrite": 581,
    "CharterNum": "0352"
  },
  {
    "sname": "Northcoast Preparatory and Performing Arts Academy",
    "AvgScrWrite": 579,
    "CharterNum": "0930"
  }
]
```
**预期SQL**:
```sql
SELECT
  `CharterNum`,
  `AvgScrWrite`,
  RANK() OVER (ORDER BY `AvgScrWrite` DESC) AS `WritingScoreRank`
FROM `schools` AS `T1`
INNER JOIN `satscores` AS `T2`
  ON `T1`.`CDSCode` = `T2`.`cds`
WHERE
  `T2`.`AvgScrWrite` > 499 AND NOT `CharterNum` IS NULL
```

**预期结果**:
```json
[
  {
    "CharterNum": "0210",
    "AvgScrWrite": 630,
    "WritingScoreRank": 1
  },
  {
    "CharterNum": "0890",
    "AvgScrWrite": 593,
    "WritingScoreRank": 2
  },
  {
    "CharterNum": "0290",
    "AvgScrWrite": 582,
    "WritingScoreRank": 3
  },
  {
    "CharterNum": "0352",
    "AvgScrWrite": 581,
    "WritingScoreRank": 4
  },
  {
    "CharterNum": "0930",
    "AvgScrWrite": 579,
    "WritingScoreRank": 5
  }
]
```
---

#### ID:41 | california_schools

**问题**: List the names of virtual schools that are among the top 5 in their respective counties based on average reading scores.

**证据**: Exclusively virtual refers to Virtual = 'F'; respective counties means PARTITION BY County

**生成SQL**:
```sql
SELECT School FROM ( SELECT s.School, s.County, sat.AvgScrRead, ROW_NUMBER() OVER (PARTITION BY s.County ORDER BY sat.AvgScrRead DESC) as rank FROM schools s INNER JOIN satscores sat ON s.CDSCode = sat.cds WHERE s.Virtual = 'F' ) ranked_schools WHERE rank <= 5 ORDER BY County, rank
```

**生成结果**:
```
❌ 执行失败
```

**预期SQL**:
```sql
SELECT  School FROM ( SELECT T2.School, T1.AvgScrRead, RANK() OVER (PARTITION BY T2.County ORDER BY T1.AvgScrRead DESC) AS rnk FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode WHERE T2.Virtual = 'F') ranked_schools WHERE rnk <= 5
```

**预期结果**:
```json
[
  {
    "School": "Academy of Arts and Sciences: Fresno"
  },
  {
    "School": "Dunlap Leadership Academy"
  },
  {
    "School": "Insight School of California"
  },
  {
    "School": "California Virtual Academy @ Kings"
  },
  {
    "School": "National University Academy, Armona"
  }
]
```
---

#### ID:46 | california_schools

**问题**: Which state special schools have the highest number of enrollees from grades 1 through 12?

**证据**: State Special Schools refers to DOC = 31; Grades 1 through 12 means K-12

**生成SQL**:
```sql
SELECT s.School, MAX(f.`Enrollment (K-12)`) AS max_enrollment FROM schools s INNER JOIN frpm f ON s.CDSCode = f.CDSCode WHERE s.DOC = '31' GROUP BY s.CDSCode, s.School ORDER BY max_enrollment DESC
```

**生成结果**:
```json
[
  {
    "School": "California School for the Deaf-Fremont",
    "max_enrollment": 410.0
  },
  {
    "School": "California School for the Deaf-Riverside",
    "max_enrollment": 355.0
  },
  {
    "School": "California School for the Blind",
    "max_enrollment": 60.0
  }
]
```
**预期SQL**:
```sql
SELECT
  `T2`.`School`
FROM `frpm` AS `T1`
INNER JOIN `schools` AS `T2`
  ON `T1`.`CDSCode` = `T2`.`CDSCode`
WHERE
  `T2`.`DOC` = 31
ORDER BY
  `T1`.`Enrollment (K-12)` DESC
LIMIT 1
```

**预期结果**:
```json
[
  {
    "School": "California School for the Deaf-Fremont"
  }
]
```
---

#### ID:82 | california_schools

**问题**: What is the grade span offered in the school with the highest longitude?

**证据**: the highest longitude refers to the school with the maximum absolute longitude value.

**生成SQL**:
```sql
SELECT GSoffered FROM schools WHERE ABS(Longitude) = (SELECT MAX(ABS(Longitude)) FROM schools)
```

**生成结果**:
```json
[
  {
    "GSoffered": "K-8"
  },
  {
    "GSoffered": null
  }
]
```
**预期SQL**:
```sql
SELECT
  `GSoffered`
FROM `schools`
ORDER BY
  ABS(`longitude`) DESC
LIMIT 1
```

**预期结果**:
```json
[
  {
    "GSoffered": "K-8"
  }
]
```
---

#### ID:159 | financial

**问题**: List all the withdrawals in cash transactions that the client with the id 3356 makes.

**证据**: operation = 'VYBER' refers to withdrawal in cash

**生成SQL**:
```sql
SELECT trans.* FROM client INNER JOIN disp ON client.client_id = disp.client_id INNER JOIN trans ON disp.account_id = trans.account_id WHERE client.client_id = 3356 AND trans.operation = 'VYBER'
```

**生成结果**:
```json
[
  {
    "trans_id": 816173,
    "account_id": 2779,
    "date": "1993-12-02",
    "type": "VYDAJ",
    "operation": "VYBER",
    "amount": 800,
    "balance": 42072,
    "k_symbol": null,
    "bank": null,
    "account": null
  },
  {
    "trans_id": 816174,
    "account_id": 2779,
    "date": "1994-12-29",
    "type": "VYDAJ",
    "operation": "VYBER",
    "amount": 2400,
    "balance": 59207,
    "k_symbol": null,
    "bank": null,
    "account": null
  },
  {
    "trans_id": 816175,
    "account_id": 2779,
    "date": "1995-12-05",
    "type": "VYDAJ",
    "operation": "VYBER",
    "amount": 4320,
    "balance": 45682,
    "k_symbol": null,
    "bank": null,
    "account": null
  },
  {
    "trans_id": 816181,
    "account_id": 2779,
    "date": "1993-11-20",
    "type": "VYDAJ",
    "operation": "VYBER",
    "amount": 600,
    "balance": 42711,
    "k_symbol": null,
    "bank": null,
    "account": null
  },
  {
    "trans_id": 816185,
    "account_id": 2779,
    "date": "1994-02-24",
    "type": "VYDAJ",
    "operation": "VYBER",
    "amount": 3480,
    "balance": 40506,
    "k_symbol": null,
    "bank": null,
    "account": null
  }
]
```
**预期SQL**:
```sql
SELECT
  `T4`.`trans_id`
FROM `client` AS `T1`
INNER JOIN `disp` AS `T2`
  ON `T1`.`client_id` = `T2`.`client_id`
INNER JOIN `account` AS `T3`
  ON `T2`.`account_id` = `T3`.`account_id`
INNER JOIN `trans` AS `T4`
  ON `T3`.`account_id` = `T4`.`account_id`
WHERE
  `T1`.`client_id` = 3356 AND `T4`.`operation` = 'VYBER'
```

**预期结果**:
```json
[
  {
    "trans_id": 816173
  },
  {
    "trans_id": 816174
  },
  {
    "trans_id": 816175
  },
  {
    "trans_id": 816181
  },
  {
    "trans_id": 816185
  }
]
```
---


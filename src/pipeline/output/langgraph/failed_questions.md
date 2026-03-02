# SQL 生成失败案例分析报告

生成时间: 2026-01-19 01:48:37

## 整体统计

| 指标 | 数值 |
|------|------|
| 总问题数 | 500 |
| 有效评估 | 500 |
| 执行失败 | 0 |
| 执行准确率 | 50.60% |

## 按难度统计

| 难度 | 准确率 | 失败数 | 总数 |
|------|--------|--------|------|
| simple | 56.76% | 64 | 148 |
| moderate | 49.20% | 127 | 250 |
| challenging | 45.10% | 56 | 102 |

---

# Simple 难度失败案例 (64个)

## 1. [ID:1498]

**问题**: What is the highest monthly consumption in the year 2012?

**证据**: (无)

**生成SQL**:
```sql
SELECT MAX(Consumption) AS highest_monthly_consumption FROM yearmonth WHERE SUBSTRING(Date, 1, 4) = '2012'
```

**预期SQL**:
```sql
SELECT
  SUM(`Consumption`)
FROM `yearmonth`
WHERE
  SUBSTR(`Date`, 1, 4) = '2012'
GROUP BY
  SUBSTR(`Date`, 5, 2)
ORDER BY
  SUM(`Consumption`) DESC
LIMIT 1
```

**生成结果**: [{'highest_monthly_consumption': 445279.69}]

**预期结果**: [{'SUM(`Consumption`)': 51787161.73999976}]

---

## 2. [ID:1500]

**问题**: Please list the product description of the products consumed in September, 2013.

**证据**: (无)

**生成SQL**:
```sql
SELECT DISTINCT p.Description FROM products p INNER JOIN transactions_1k t ON p.ProductID = t.ProductID WHERE t.Date >= '2013-09-01' AND t.Date <= '2013-09-30'
```

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

**生成结果**: []

**预期结果**: [{'Description': 'Nafta'}, {'Description': 'Nafta'}, {'Description': 'Provoz.nápl.'}] ... (+973行)

---

## 3. [ID:1505]

**问题**: Among the customers who paid in euro, how many of them have a monthly consumption of over 1000?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(DISTINCT c.CustomerID) FROM customers c INNER JOIN yearmonth y ON c.CustomerID = y.CustomerID WHERE c.Currency = 'EUR' AND y.Consumption > 1000
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

**生成结果**: [{'COUNT(DISTINCT c.CustomerID)': 391}]

**预期结果**: [{'COUNT(*)': 2730}]

---

## 4. [ID:1524]

**问题**: What's the nationality of the customer who spent 548.4 in 2012/8/24?

**证据**: (无)

**生成SQL**:
```sql
SELECT c.Currency FROM transactions_1k t INNER JOIN customers c ON t.CustomerID = c.CustomerID WHERE t.Date = '2012-08-24' AND t.Amount = 548.4
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

**生成结果**: []

**预期结果**: [{'Country': 'CZE'}]

---

## 5. [ID:1525]

**问题**: What is the percentage of the customers who used EUR in 2012/8/25?

**证据**: (无)

**生成SQL**:
```sql
SELECT (COUNT(DISTINCT t.CustomerID) * 100.0 / (SELECT COUNT(DISTINCT CustomerID) FROM transactions_1k WHERE Date = '2012-08-25')) AS percentage FROM transactions_1k t INNER JOIN customers c ON t.CustomerID = c.CustomerID WHERE t.Date = '2012-08-25' AND c.Currency = 'EUR'
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

**生成结果**: [{'percentage': 2.7027}]

**预期结果**: [{"CAST(SUM(CASE WHEN `T2`.`Currency` = 'EUR' THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(`T1`.`CustomerID`)": 1.6470588235294117}]

---

## 6. [ID:1334]

**问题**: List the full name of the Student_Club members that grew up in Illinois state.

**证据**: (无)

**生成SQL**:
```sql
SELECT CONCAT(m.first_name, ' ', m.last_name) AS full_name FROM member m INNER JOIN zip_code z ON m.zip = z.zip_code WHERE z.state = 'Illinois'
```

**预期SQL**:
```sql
SELECT
  `T1`.`first_name`,
  `T1`.`last_name`
FROM `member` AS `T1`
INNER JOIN `zip_code` AS `T2`
  ON `T1`.`zip` = `T2`.`zip_code`
WHERE
  `T2`.`state` = 'Illinois'
```

**生成结果**: [{'full_name': 'Annabella Warren'}, {'full_name': 'Tyler Hewitt'}, {'full_name': 'Trent Smith'}]

**预期结果**: [{'first_name': 'Annabella', 'last_name': 'Warren'}, {'first_name': 'Tyler', 'last_name': 'Hewitt'}, {'first_name': 'Trent', 'last_name': 'Smith'}]

---

## 7. [ID:1371]

**问题**: How many members attended the "Women's Soccer" event?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(*) FROM attendance WHERE link_to_event IN (SELECT event_id FROM event WHERE event_name = 'Women's Soccer')
```

**预期SQL**:
```sql
SELECT
  COUNT(`T2`.`link_to_member`)
FROM `event` AS `T1`
INNER JOIN `attendance` AS `T2`
  ON `T1`.`event_id` = `T2`.`link_to_event`
WHERE
  `T1`.`event_name` = 'Women''s Soccer'
```

**生成结果**: []

**预期结果**: [{'COUNT(`T2`.`link_to_member`)': 17}]

---

## 8. [ID:1389]

**问题**: Which event has the lowest cost?

**证据**: (无)

**生成SQL**:
```sql
SELECT event_name FROM event WHERE event_id IN (SELECT link_to_event FROM budget ORDER BY spent ASC LIMIT 1)
```

**预期SQL**:
```sql
SELECT
  `T1`.`event_name`
FROM `event` AS `T1`
INNER JOIN `budget` AS `T2`
  ON `T1`.`event_id` = `T2`.`link_to_event`
INNER JOIN `expense` AS `T3`
  ON `T2`.`budget_id` = `T3`.`link_to_budget`
ORDER BY
  `T3`.`cost`
LIMIT 1
```

**生成结果**: []

**预期结果**: [{'event_name': 'September Speaker'}]

---

## 9. [ID:1410]

**问题**: List out the full name and total cost that member id "rec4BLdZHS2Blfp4v" incurred?

**证据**: (无)

**生成SQL**:
```sql
SELECT CONCAT(m.first_name, ' ', m.last_name) AS full_name, SUM(e.cost) AS total_cost FROM member m INNER JOIN expense e ON m.member_id = e.link_to_member WHERE m.member_id = 'rec4BLdZHS2Blfp4v' GROUP BY m.member_id, m.first_name, m.last_name
```

**预期SQL**:
```sql
SELECT
  `T1`.`first_name`,
  `T1`.`last_name`,
  SUM(`T2`.`cost`)
FROM `member` AS `T1`
INNER JOIN `expense` AS `T2`
  ON `T1`.`member_id` = `T2`.`link_to_member`
WHERE
  `T1`.`member_id` = 'rec4BLdZHS2Blfp4v'
```

**生成结果**: [{'full_name': 'Sacha Harrison', 'total_cost': 866.25}]

**预期结果**: [{'first_name': 'Sacha', 'last_name': 'Harrison', 'SUM(`T2`.`cost`)': 866.25}]

---

## 10. [ID:1422]

**问题**: State the category of events were held at MU 215.

**证据**: (无)

**生成SQL**:
```sql
SELECT DISTINCT type FROM event WHERE location = 'MU 215'
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

**生成结果**: [{'type': 'Election'}, {'type': 'Meeting'}, {'type': 'Guest Speaker'}]

**预期结果**: [{'category': 'Advertisement'}, {'category': 'Food'}, {'category': 'Speaker Gifts'}] ... (+1行)

---

## 11. [ID:1153]

**问题**: What is the disease patient '30609' diagnosed with. List all the date of laboratory tests done for this patient.

**证据**: (无)

**生成SQL**:
```sql
SELECT Diagnosis FROM Patient WHERE ID = 30609; SELECT Date FROM Laboratory WHERE ID = 30609 ORDER BY Date;
```

**预期SQL**:
```sql
SELECT
  `T1`.`Diagnosis`,
  `T2`.`Date`
FROM `Patient` AS `T1`
INNER JOIN `Laboratory` AS `T2`
  ON `T1`.`ID` = `T2`.`ID`
WHERE
  `T1`.`ID` = 30609
```

**生成结果**: []

**预期结果**: [{'Diagnosis': 'SLE, MCTD', 'Date': '1984-07-12'}, {'Diagnosis': 'SLE, MCTD', 'Date': '1984-08-02'}, {'Diagnosis': 'SLE, MCTD', 'Date': '1984-09-03'}] ... (+57行)

---

## 12. [ID:1166]

**问题**: What are the symptoms observed by the youngest patient to ever did a medical examination? Identify their diagnosis.

**证据**: (无)

**生成SQL**:
```sql
SELECT T2.Symptoms, T2.Diagnosis FROM Patient T1 INNER JOIN Examination T2 ON T1.ID = T2.ID WHERE T1.Birthday = (SELECT MAX(Birthday) FROM Patient) AND T2.Symptoms IS NOT NULL
```

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

**生成结果**: []

**预期结果**: [{'Symptoms': 'CNS susp', 'Diagnosis': 'SLE'}]

---

## 13. [ID:1198]

**问题**: How many female patients were given an APS diagnosis?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(*) FROM Patient WHERE SEX = 'F' AND Diagnosis LIKE '%APS%'
```

**预期SQL**:
```sql
SELECT
  COUNT(`ID`)
FROM `Patient`
WHERE
  `SEX` = 'F' AND `Diagnosis` = 'APS'
```

**生成结果**: [{'COUNT(*)': 51}]

**预期结果**: [{'COUNT(`ID`)': 16}]

---

## 14. [ID:1251]

**问题**: How many patients with an Ig G higher than normal?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(DISTINCT ID) FROM Laboratory WHERE IGG >= 2000
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

**生成结果**: [{'COUNT(DISTINCT ID)': 136}]

**预期结果**: [{'COUNT(DISTINCT `T1`.`ID`)': 9}]

---

## 15. [ID:1035]

**问题**: Give the team_fifa_api_id of teams with more than 50 but less than 60 build-up play speed.

**证据**: (无)

**生成SQL**:
```sql
SELECT team_fifa_api_id FROM Team_Attributes WHERE buildUpPlaySpeed > 50 AND buildUpPlaySpeed < 60
```

**预期SQL**:
```sql
SELECT DISTINCT
  `team_fifa_api_id`
FROM `Team_Attributes`
WHERE
  `buildUpPlaySpeed` > 50 AND `buildUpPlaySpeed` < 60
```

**生成结果**: [{'team_fifa_api_id': 434}, {'team_fifa_api_id': 77}, {'team_fifa_api_id': 77}] ... (+353行)

**预期结果**: [{'team_fifa_api_id': 1}, {'team_fifa_api_id': 3}, {'team_fifa_api_id': 4}] ... (+158行)

---

## 16. [ID:1048]

**问题**: What is the overall rating of the football player Gabriel Tamas in year 2011?

**证据**: (无)

**生成SQL**:
```sql
SELECT overall_rating FROM Player_Attributes WHERE player_api_id = (SELECT player_api_id FROM Player WHERE player_name = 'Gabriel Tamas') AND strftime('%Y', date) = '2011'
```

**预期SQL**:
```sql
SELECT  `t2`.`overall_rating` FROM `Player` AS `t1`
INNER JOIN `Player_Attributes` AS `t2`
  ON `t1`.`player_api_id` = `t2`.`player_api_id` WHERE  `t1`.`player_name` = 'Gabriel Tamas'  AND DATE_FORMAT(CAST(`t2`.`date` AS DATETIME), '%Y') = '2011'
```

**生成结果**: []

**预期结果**: [{'overall_rating': 75}]

---

## 17. [ID:1078]

**问题**: Which player is older, Aaron Lennon or Abdelaziz Barrada?

**证据**: (无)

**生成SQL**:
```sql
SELECT player_name FROM Player WHERE player_name IN ('Aaron Lennon', 'Abdelaziz Barrada') ORDER BY birthday DESC LIMIT 1
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

**生成结果**: [{'player_name': 'Abdelaziz Barrada'}]

**预期结果**: [{'player_name': 'Aaron Lennon'}]

---

## 18. [ID:1092]

**问题**: Give the name of the league had the most matches in the 2008/2009 season?

**证据**: (无)

**生成SQL**:
```sql
SELECT L.name FROM League L INNER JOIN Match M ON L.id = M.league_id WHERE M.season = '2008/2009' GROUP BY L.name ORDER BY COUNT(M.id) DESC LIMIT 1
```

**预期SQL**:
```sql
SELECT `t1`.`name` FROM `League` AS `t1`JOIN `Match` AS `t2` ON `t1`.`id` = `t2`.`league_id` WHERE  `t2`.`season` = '2008/2009' GROUP BY  `t1`.`name` HAVING COUNT(`t2`.`id`) = (SELECT MAX(match_count) FROM (SELECT COUNT(`t2`.`id`) AS match_count FROM `Match` AS `t2` WHERE `t2`.`season` = '2008/2009' GROUP BY  `t2`.`league_id`) AS subquery)
```

**生成结果**: []

**预期结果**: [{'name': 'England Premier League'}, {'name': 'France Ligue 1'}, {'name': 'Italy Serie A'}] ... (+1行)

---

## 19. [ID:1122]

**问题**: State the name of the most strongest player.

**证据**: (无)

**生成SQL**:
```sql
SELECT player_name FROM Player WHERE id = (SELECT player_id FROM Player_Attributes ORDER BY overall_rating DESC LIMIT 1)
```

**预期SQL**:
```sql
SELECT DISTINCT t1.player_name FROM Player AS t1 INNER JOIN Player_Attributes AS t2 ON t1.player_api_id = t2.player_api_id WHERE t2.overall_rating = (SELECT MAX(overall_rating) FROM Player_Attributes)
```

**生成结果**: []

**预期结果**: [{'player_name': 'Lionel Messi'}]

---

## 20. [ID:1144]

**问题**: Please state the finishing rate and curve score of the player who has the heaviest weight.

**证据**: (无)

**生成SQL**:
```sql
SELECT pa.finishing, pa.curve FROM Player_Attributes pa INNER JOIN Player p ON pa.player_api_id = p.player_api_id WHERE p.weight = (SELECT MAX(weight) FROM Player)
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

**生成结果**: [{'finishing': 13, 'curve': 13}, {'finishing': 13, 'curve': 13}, {'finishing': 13, 'curve': 13}] ... (+35行)

**预期结果**: [{'id': 98022, 'finishing': 13, 'curve': 13}]

---

## 21. [ID:1145]

**问题**: Which top 4 leagues had the most games in the 2015-2016 season?

**证据**: (无)

**生成SQL**:
```sql
SELECT L.name FROM League L INNER JOIN Match M ON L.id = M.league_id WHERE M.season = '2015/2016' GROUP BY L.name ORDER BY COUNT(M.id) DESC LIMIT 4
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

**生成结果**: []

**预期结果**: [{'name': 'Spain LIGA BBVA'}, {'name': 'England Premier League'}, {'name': 'France Ligue 1'}] ... (+1行)

---

## 22. [ID:847]

**问题**: What is the surname of the driver with the best lap time in race number 19 in the second qualifying period?

**证据**: (无)

**生成SQL**:
```sql
SELECT d.surname FROM drivers d JOIN qualifying q ON d.driverId = q.driverId WHERE q.raceId = 19 AND q.q2 IS NOT NULL ORDER BY q.q2 ASC LIMIT 1
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

**生成结果**: [{'surname': 'Räikkönen'}]

**预期结果**: [{'surname': 'Davidson'}]

---

## 23. [ID:850]

**问题**: Please give the name of the race held on the circuits in Germany.

**证据**: (无)

**生成SQL**:
```sql
SELECT r.name FROM races r INNER JOIN circuits c ON r.circuitId = c.circuitId WHERE c.country = 'Germany'
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

**生成结果**: [{'name': 'German Grand Prix'}, {'name': 'German Grand Prix'}, {'name': 'German Grand Prix'}] ... (+73行)

**预期结果**: [{'name': 'German Grand Prix'}, {'name': 'European Grand Prix'}, {'name': 'Luxembourg Grand Prix'}]

---

## 24. [ID:854]

**问题**: What is the coordinates location of the circuits for Australian grand prix?

**证据**: (无)

**生成SQL**:
```sql
SELECT c.lat, c.lng FROM circuits c INNER JOIN races r ON c.circuitId = r.circuitId WHERE r.name = 'Australian Grand Prix'
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
  `T2`.`name` = 'Australian Grand Prix'
```

**生成结果**: [{'lat': -34.9272, 'lng': 138.617}, {'lat': -34.9272, 'lng': 138.617}, {'lat': -34.9272, 'lng': 138.617}] ... (+8行)

**预期结果**: [{'lat': -34.9272, 'lng': 138.617}]

---

## 25. [ID:857]

**问题**: Give the coordinate position for Abu Dhabi Grand Prix.

**证据**: (无)

**生成SQL**:
```sql
SELECT c.lat, c.lng FROM races r INNER JOIN circuits c ON r.circuitId = c.circuitId WHERE r.name = 'Abu Dhabi Grand Prix'
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
  `T2`.`name` = 'Abu Dhabi Grand Prix'
```

**生成结果**: [{'lat': 24.4672, 'lng': 54.6031}, {'lat': 24.4672, 'lng': 54.6031}, {'lat': 24.4672, 'lng': 54.6031}] ... (+6行)

**预期结果**: [{'lat': 24.4672, 'lng': 54.6031}]

---

## 26. [ID:861]

**问题**: What is his number of the driver who finished 0:01:54 in the Q3 of qualifying race No.903?

**证据**: (无)

**生成SQL**:
```sql
SELECT d.number FROM drivers d JOIN qualifying q ON d.driverId = q.driverId WHERE q.raceId = 903 AND q.q3 LIKE '0:01:54%'
```

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

**生成结果**: []

**预期结果**: [{'number': 3}, {'number': 5}]

---

## 27. [ID:868]

**问题**: Where is Malaysian Grand Prix held? Give the location coordinates.

**证据**: (无)

**生成SQL**:
```sql
SELECT c.lat, c.lng FROM races r INNER JOIN circuits c ON r.circuitId = c.circuitId WHERE r.name = 'Malaysian Grand Prix'
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

**生成结果**: [{'lat': 2.76083, 'lng': 101.738}, {'lat': 2.76083, 'lng': 101.738}, {'lat': 2.76083, 'lng': 101.738}] ... (+16行)

**预期结果**: [{'lat': 2.76083, 'lng': 101.738}]

---

## 28. [ID:872]

**问题**: In the race No. 45, for the driver who had the Q3 time as 0:01:33, what is his abbreviated code?

**证据**: (无)

**生成SQL**:
```sql
SELECT d.code FROM qualifying q JOIN drivers d ON q.driverId = d.driverId WHERE q.raceId = 45 AND q.q3 LIKE '0:01:33%'
```

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

**生成结果**: []

**预期结果**: [{'code': 'HAM'}]

---

## 29. [ID:898]

**问题**: How old is the youngest Japanese driver? What is his name?

**证据**: (无)

**生成SQL**:
```sql
SELECT forename, surname, dob FROM drivers WHERE nationality = 'Japanese' ORDER BY dob DESC LIMIT 1
```

**预期SQL**:
```sql
SELECT
  DATE_FORMAT(CAST(CURRENT_TIMESTAMP() AS DATETIME), '%Y') - DATE_FORMAT(CAST(`dob` AS DATETIME), '%Y'),
  `forename`,
  `surname`
FROM `drivers`
WHERE
  `nationality` = 'Japanese'
ORDER BY
  `dob` DESC
LIMIT 1
```

**生成结果**: [{'forename': 'Kamui', 'surname': 'Kobayashi', 'dob': '1986-09-13'}]

**预期结果**: [{"DATE_FORMAT(CAST(CURRENT_TIMESTAMP() AS DATETIME), '%Y') - DATE_FORMAT(CAST(`dob` AS DATETIME), '%Y')": 40.0, 'forename': 'Kamui', 'surname': 'Kobayashi'}]

---

## 30. [ID:902]

**问题**: Which race was Alex Yoong in when he was in track number less than 20?

**证据**: (无)

**生成SQL**:
```sql
SELECT r.name FROM results res INNER JOIN drivers d ON res.driverId = d.driverId INNER JOIN races r ON res.raceId = r.raceId WHERE d.forename = 'Alex' AND d.surname = 'Yoong' AND res.position < 20
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

**生成结果**: [{'name': 'Brazilian Grand Prix'}, {'name': 'Canadian Grand Prix'}, {'name': 'French Grand Prix'}] ... (+2行)

**预期结果**: [{'name': 'Malaysian Grand Prix'}, {'name': 'Brazilian Grand Prix'}, {'name': 'San Marino Grand Prix'}] ... (+12行)

---

## 31. [ID:915]

**问题**: Which country is the oldest driver from?

**证据**: (无)

**生成SQL**:
```sql
SELECT nationality FROM drivers ORDER BY dob ASC LIMIT 1
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

**生成结果**: [{'nationality': 'South African'}]

**预期结果**: [{'nationality': 'French'}]

---

## 32. [ID:930]

**问题**: In which Formula_1 race did Lewis Hamilton rank the highest?

**证据**: (无)

**生成SQL**:
```sql
SELECT r.name FROM results res INNER JOIN races r ON res.raceId = r.raceId INNER JOIN drivers d ON res.driverId = d.driverId WHERE d.forename = 'Lewis' AND d.surname = 'Hamilton' AND res.rank IS NOT NULL ORDER BY res.rank ASC LIMIT 1
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

**生成结果**: [{'name': 'Chinese Grand Prix'}]

**预期结果**: [{'name': 'Chinese Grand Prix'}, {'name': 'Malaysian Grand Prix'}, {'name': 'Japanese Grand Prix'}] ... (+34行)

---

## 33. [ID:937]

**问题**: What's the finish time for the driver who ranked second in 2008's Chinese Grand Prix?

**证据**: (无)

**生成SQL**:
```sql
SELECT r.time FROM results r JOIN races ra ON r.raceId = ra.raceId WHERE ra.year = 2008 AND ra.name = 'Chinese Grand Prix' AND r.position = 2
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

**生成结果**: [{'time': '+14.925'}]

**预期结果**: [{'time': '+16.445'}]

---

## 34. [ID:950]

**问题**: Please list the constructor names with 0 points at race 291.

**证据**: (无)

**生成SQL**:
```sql
SELECT DISTINCT c.name FROM constructorResults cr INNER JOIN constructors c ON cr.constructorId = c.constructorId WHERE cr.raceId = 291 AND cr.points = 0
```

**预期SQL**:
```sql
SELECT
  `T2`.`name`
FROM `constructorStandings` AS `T1`
INNER JOIN `constructors` AS `T2`
  ON `T1`.`constructorId` = `T2`.`constructorId`
WHERE
  `T1`.`points` = 0 AND `T1`.`raceId` = 291
```

**生成结果**: [{'name': 'Minardi'}, {'name': 'Dallara'}, {'name': 'Larrousse'}] ... (+8行)

**预期结果**: [{'name': 'Ligier'}, {'name': 'Jordan'}, {'name': 'Larrousse'}] ... (+3行)

---

## 35. [ID:951]

**问题**: How many Japanese constructors have 0 points in 2 races?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(*) FROM (SELECT constructorId FROM constructorStandings WHERE points = 0 GROUP BY constructorId HAVING COUNT(DISTINCT raceId) = 2) AS zero_points_constructors INNER JOIN constructors ON zero_points_constructors.constructorId = constructors.constructorId WHERE constructors.nationality = 'Japanese'
```

**预期SQL**:
```sql
SELECT
  COUNT(`T1`.`raceId`)
FROM `constructorStandings` AS `T1`
INNER JOIN `constructors` AS `T2`
  ON `T1`.`constructorId` = `T2`.`constructorId`
WHERE
  `T1`.`points` = 0 AND `T2`.`nationality` = 'Japanese'
GROUP BY
  `T1`.`constructorId`
HAVING
  COUNT(`raceId`) = 2
```

**生成结果**: [{'COUNT(*)': 1}]

**预期结果**: [{'COUNT(`T1`.`raceId`)': 2}]

---

## 36. [ID:959]

**问题**: What is the fastest lap number of the champion in 2009?

**证据**: (无)

**生成SQL**:
```sql
SELECT r.fastestLap FROM results r JOIN races ra ON r.raceId = ra.raceId JOIN driverStandings ds ON r.raceId = ds.raceId AND r.driverId = ds.driverId WHERE ra.year = 2009 AND ds.position = 1
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

**生成结果**: [{'fastestLap': 18}, {'fastestLap': 44}, {'fastestLap': 11}] ... (+13行)

**预期结果**: [{'fastestLap': 18}, {'fastestLap': 42}, {'fastestLap': 11}] ... (+13行)

---

## 37. [ID:967]

**问题**: State code numbers of top 3 yougest drivers. How many Netherlandic drivers among them?

**证据**: (无)

**生成SQL**:
```sql
SELECT code FROM drivers WHERE nationality = 'Dutch' ORDER BY dob DESC LIMIT 3
```

**预期SQL**:
```sql
SELECT COUNT(*) FROM (SELECT `T1`.`nationality` FROM `drivers` AS `T1` ORDER BY `T1`.`dob` DESC LIMIT 3) AS `T3` WHERE `T3`.`nationality` = 'Dutch'
```

**生成结果**: [{'code': 'VER'}, {'code': 'VDG'}, {'code': 'DOO'}]

**预期结果**: [{'COUNT(*)': 1}]

---

## 38. [ID:978]

**问题**: How many times the circuits were held in Austria? Please give their location and coordinates.

**证据**: (无)

**生成SQL**:
```sql
SELECT circuits.name, circuits.location, circuits.lat, circuits.lng FROM circuits WHERE circuits.country = 'Austria'
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

**生成结果**: [{'name': 'A1-Ring', 'location': 'Spielburg', 'lat': 47.2197, 'lng': 14.7647}, {'name': 'Zeltweg', 'location': 'Styria', 'lat': 47.2039, 'lng': 14.7478}, {'name': 'Red Bull Ring', 'location': 'Spielburg', 'lat': 47.2197, 'lng': 14.7647}]

**预期结果**: [{'location': 'Spielburg', 'lat': 47.2197, 'lng': 14.7647}, {'location': 'Styria', 'lat': 47.2039, 'lng': 14.7478}]

---

## 39. [ID:791]

**问题**: Calculate the average height for all superhero.

**证据**: (无)

**生成SQL**:
```sql
SELECT AVG(height_cm) FROM superhero
```

**预期SQL**:
```sql
SELECT
  CAST(SUM(`height_cm`) AS DOUBLE) / COUNT(`id`)
FROM `superhero`
```

**生成结果**: [{'AVG(height_cm)': 267.7514}]

**预期结果**: [{'CAST(SUM(`height_cm`) AS DOUBLE) / COUNT(`id`)': 247.04533333333333}]

---

## 40. [ID:532]

**问题**: Please list the display names of all the users whose accounts were created in the year 2011.

**证据**: (无)

**生成SQL**:
```sql
SELECT DISTINCT users.DisplayName FROM users WHERE YEAR(users.CreationDate) = 2011
```

**预期SQL**:
```sql
SELECT
  `DisplayName`
FROM `users`
WHERE
  DATE_FORMAT(CAST(`CreationDate` AS DATETIME), '%Y') = '2011'
```

**生成结果**: [{'DisplayName': 'Rob'}, {'DisplayName': 'Anubhav'}, {'DisplayName': 'Betamoo'}] ... (+997行)

**预期结果**: [{'DisplayName': 'Rob'}, {'DisplayName': 'Anubhav'}, {'DisplayName': 'Betamoo'}] ... (+997行)

---

## 41. [ID:533]

**问题**: How many users last accessed the website after 2014/9/1?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(*) FROM users WHERE LastAccessDate > '2014-09-01'
```

**预期SQL**:
```sql
SELECT
  COUNT(`Id`)
FROM `users`
WHERE
  DATE(`LastAccessDate`) > '2014-09-01'
```

**生成结果**: [{'COUNT(*)': 5146}]

**预期结果**: [{'COUNT(`Id`)': 4941}]

---

## 42. [ID:539]

**问题**: Who is the owner of the post "Eliciting priors from experts"?

**证据**: (无)

**生成SQL**:
```sql
SELECT p.OwnerDisplayName FROM posts p WHERE p.Title = 'Eliciting priors from experts'
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

**生成结果**: [{'OwnerDisplayName': None}]

**预期结果**: [{'DisplayName': 'csgillespie'}]

---

## 43. [ID:537]

**问题**: How many posts does the user csgillespie own?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(*) FROM posts WHERE OwnerDisplayName = 'csgillespie'
```

**预期SQL**:
```sql
SELECT
  COUNT(`T1`.`id`)
FROM `posts` AS `T1`
INNER JOIN `users` AS `T2`
  ON `T1`.`OwnerUserId` = `T2`.`Id`
WHERE
  `T2`.`DisplayName` = 'csgillespie'
```

**生成结果**: [{'COUNT(*)': 0}]

**预期结果**: [{'COUNT(`T1`.`id`)': 121}]

---

## 44. [ID:567]

**问题**: For the user with the display name of "Tiago Pasqualini", how many posts did he/she own?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(*) FROM posts WHERE OwnerDisplayName = 'Tiago Pasqualini'
```

**预期SQL**:
```sql
SELECT
  COUNT(`T1`.`Id`)
FROM `users` AS `T1`
INNER JOIN `posts` AS `T2`
  ON `T1`.`Id` = `T2`.`OwnerUserId`
WHERE
  `T1`.`DisplayName` = 'Tiago Pasqualini'
```

**生成结果**: [{'COUNT(*)': 0}]

**预期结果**: [{'COUNT(`T1`.`Id`)': 2}]

---

## 45. [ID:576]

**问题**: Name the user that commented 'thank you user93!'

**证据**: (无)

**生成SQL**:
```sql
SELECT DISTINCT UserDisplayName FROM comments WHERE Text LIKE '%thank you user93!%'
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

**生成结果**: [{'UserDisplayName': None}]

**预期结果**: [{'DisplayName': 'Preets'}]

---

## 46. [ID:710]

**问题**: In posts with 1 comment, how many of the comments have 0 score?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(*) FROM comments WHERE PostId IN (SELECT Id FROM posts WHERE CommentCount = 1) AND Score = 0
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

**生成结果**: [{'COUNT(*)': 10997}]

**预期结果**: [{'COUNT(`T1`.`id`)': 2888}]

---

## 47. [ID:340]

**问题**: Which are the cards that have incredibly powerful foils.

**证据**: (无)

**生成SQL**:
```sql
SELECT name FROM cards WHERE cardKingdomFoilId IS NOT NULL AND cardKingdomId IS NOT NULL
```

**预期SQL**:
```sql
SELECT
  `id`
FROM `cards`
WHERE
  NOT `cardKingdomFoilId` IS NULL AND NOT `cardKingdomId` IS NULL
```

**生成结果**: [{'name': 'Ballista Squad'}, {'name': 'Bandage'}, {'name': 'Beacon of Immortality'}] ... (+997行)

**预期结果**: [{'id': 4}, {'id': 5}, {'id': 6}] ... (+997行)

---

## 48. [ID:341]

**问题**: What are the borderless cards available without powerful foils?

**证据**: (无)

**生成SQL**:
```sql
SELECT name FROM cards WHERE borderColor = 'borderless' AND cardKingdomFoilId IS NOT NULL AND cardKingdomId IS NOT NULL
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

**生成结果**: [{'name': 'Karn Liberated'}, {'name': 'Jace, the Mind Sculptor'}, {'name': 'Avacyn, Angel of Hope'}] ... (+166行)

**预期结果**: [{'id': 23004}, {'id': 25350}, {'id': 25355}] ... (+64行)

---

## 49. [ID:358]

**问题**: What is the border color of card "Ancestor's Chosen"?

**证据**: (无)

**生成SQL**:
```sql
SELECT borderColor FROM cards WHERE name = 'Ancestor''s Chosen'
```

**预期SQL**:
```sql
SELECT DISTINCT
  `borderColor`
FROM `cards`
WHERE
  `name` = 'Ancestor''s Chosen'
```

**生成结果**: [{'borderColor': 'black'}, {'borderColor': 'black'}, {'borderColor': 'black'}] ... (+1行)

**预期结果**: [{'borderColor': 'black'}]

---

## 50. [ID:366]

**问题**: What is the rule of playing card "Benalish Knight"?

**证据**: (无)

**生成SQL**:
```sql
SELECT text FROM cards WHERE name = 'Benalish Knight'
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

**生成结果**: [{'text': 'Flash (You may cast this spell any time you could cast an instant.)\nFirst strike (This creature deals combat damage before creatures without first strike.)'}, {'text': 'Flash (You may cast this spell any time you could cast an instant.)\nFirst strike (This creature deals combat damage before creatures without first strike.)'}, {'text': 'Flash (You may cast this spell any time you could cast an instant.)\nFirst strike (This creature deals combat damage before creatures without first strike.)'}] ... (+1行)

**预期结果**: [{'format': 'commander'}, {'format': 'duel'}, {'format': 'legacy'}] ... (+29行)

---

## 51. [ID:377]

**问题**: How many cards with original type of "Summon - Angel" have subtype other than "Angel"?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(*) FROM cards WHERE originalType = 'Summon - Angel' AND subtypes NOT LIKE '%Angel%'
```

**预期SQL**:
```sql
SELECT
  COUNT(`id`)
FROM `cards`
WHERE
  `originalType` = 'Summon - Angel' AND `subtypes` <> 'Angel'
```

**生成结果**: [{'COUNT(*)': 0}]

**预期结果**: [{'COUNT(`id`)': 3}]

---

## 52. [ID:383]

**问题**: How many of the banned cards are white border?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(*) FROM cards WHERE borderColor = 'white' AND id IN (SELECT uuid FROM legalities WHERE status = 'Banned')
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

**生成结果**: [{'COUNT(*)': 57}]

**预期结果**: [{'COUNT(`T1`.`id`)': 258}]

---

## 53. [ID:414]

**问题**: What language is the set of 180 cards that belongs to the Ravnica block translated into?

**证据**: (无)

**生成SQL**:
```sql
SELECT st.translation FROM set_translations st JOIN sets s ON st.setCode = s.code WHERE s.baseSetSize = 180 AND s.block = 'Ravnica'
```

**预期SQL**:
```sql
SELECT
  `T2`.`language`
FROM `sets` AS `T1`
INNER JOIN `set_translations` AS `T2`
  ON `T1`.`code` = `T2`.`setCode`
WHERE
  `T1`.`block` = 'Ravnica' AND `T1`.`baseSetSize` = 180
```

**生成结果**: [{'translation': '纷争'}, {'translation': '紛爭'}, {'translation': 'Discorde'}] ... (+7行)

**预期结果**: [{'language': 'Chinese Simplified'}, {'language': 'Chinese Traditional'}, {'language': 'French'}] ... (+7行)

---

## 54. [ID:440]

**问题**: Which foreign language used by "A Pedra Fellwar"?

**证据**: (无)

**生成SQL**:
```sql
SELECT language FROM foreign_data WHERE name = 'A Pedra Fellwar'
```

**预期SQL**:
```sql
SELECT DISTINCT
  `language`
FROM `foreign_data`
WHERE
  `name` = 'A Pedra Fellwar'
```

**生成结果**: [{'language': 'Portuguese (Brazil)'}, {'language': 'Portuguese (Brazil)'}, {'language': 'Portuguese (Brazil)'}] ... (+3行)

**预期结果**: [{'language': 'Portuguese (Brazil)'}]

---

## 55. [ID:227]

**问题**: What is the percentage of molecules that are carcinogenic? Please provide your answer as a percentage with three decimal places.

**证据**: (无)

**生成SQL**:
```sql
SELECT ROUND(COUNT(CASE WHEN label = '+' THEN 1 END) * 100.0 / COUNT(molecule_id), 3) AS percentage FROM molecule
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

**生成结果**: [{'percentage': 44.315}]

**预期结果**: []

---

## 56. [ID:239]

**问题**: How many connections does the atom 19 have?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(*) FROM connected WHERE atom_id LIKE 'TR%_19' OR atom_id2 LIKE 'TR%_19'
```

**预期SQL**:
```sql
SELECT
  COUNT(`T`.`bond_id`)
FROM `connected` AS `T`
WHERE
  SUBSTR(`T`.`atom_id`, -2) = '19'
```

**生成结果**: [{'COUNT(*)': 754}]

**预期结果**: [{'COUNT(`T`.`bond_id`)': 377}]

---

## 57. [ID:248]

**问题**: What are the atoms of the triple bond with the molecule "TR041"?

**证据**: (无)

**生成SQL**:
```sql
SELECT atom_id FROM atom WHERE molecule_id = 'TR041' AND atom_id IN (SELECT atom_id FROM connected WHERE bond_id IN (SELECT bond_id FROM bond WHERE molecule_id = 'TR041' AND bond_type = '#'))
```

**预期SQL**:
```sql
SELECT
  `T2`.`atom_id`,
  `T2`.`atom_id2`
FROM `atom` AS `T1`
INNER JOIN `connected` AS `T2`
  ON `T1`.`atom_id` = `T2`.`atom_id`
INNER JOIN `bond` AS `T3`
  ON `T2`.`bond_id` = `T3`.`bond_id`
WHERE
  `T3`.`bond_type` = '#' AND `T3`.`molecule_id` = 'TR041'
```

**生成结果**: [{'atom_id': 'TR041_10'}, {'atom_id': 'TR041_7'}, {'atom_id': 'TR041_8'}] ... (+1行)

**预期结果**: [{'atom_id': 'TR041_10', 'atom_id2': 'TR041_7'}, {'atom_id': 'TR041_7', 'atom_id2': 'TR041_10'}, {'atom_id': 'TR041_8', 'atom_id2': 'TR041_9'}] ... (+1行)

---

## 58. [ID:5]

**问题**: How many schools with an average score in Math greater than 400 in the SAT test are exclusively virtual?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(*) FROM satscores WHERE AvgScrMath > 400 AND cds IN (SELECT CDSCode FROM schools WHERE Virtual = 'F')
```

**预期SQL**:
```sql
SELECT  COUNT(DISTINCT `T2`.`School`) FROM `satscores` AS `T1` INNER JOIN `schools` AS `T2`  ON `T1`.`cds` = `T2`.`CDSCode` WHERE  `T2`.`Virtual` = 'F' AND `T1`.`AvgScrMath` > 400
```

**生成结果**: []

**预期结果**: [{'COUNT(DISTINCT `T2`.`School`)': 4}]

---

## 59. [ID:17]

**问题**: Rank schools by their average score in Writing where the score is greater than 499, showing their charter numbers.

**证据**: (无)

**生成SQL**:
```sql
SELECT sname, CharterNum FROM satscores WHERE AvgScrWrite > 499 AND CharterNum IS NOT NULL ORDER BY AvgScrWrite DESC
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

**生成结果**: []

**预期结果**: [{'CharterNum': '0210', 'AvgScrWrite': 630, 'WritingScoreRank': 1}, {'CharterNum': '0890', 'AvgScrWrite': 593, 'WritingScoreRank': 2}, {'CharterNum': '0290', 'AvgScrWrite': 582, 'WritingScoreRank': 3}] ... (+55行)

---

## 60. [ID:41]

**问题**: List the names of virtual schools that are among the top 5 in their respective counties based on average reading scores.

**证据**: (无)

**生成SQL**:
```sql
SELECT s.School FROM schools s INNER JOIN satscores sc ON s.CDSCode = sc.cds WHERE s.Virtual = 'F' AND sc.rtype = 'S' AND sc.AvgScrRead IN (SELECT AvgScrRead FROM satscores sc2 WHERE sc2.cname = s.County AND sc2.rtype = 'S' ORDER BY AvgScrRead DESC LIMIT 5) GROUP BY s.School, s.County ORDER BY s.County, s.School
```

**预期SQL**:
```sql
SELECT  School FROM ( SELECT T2.School, T1.AvgScrRead, RANK() OVER (PARTITION BY T2.County ORDER BY T1.AvgScrRead DESC) AS rnk FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode WHERE T2.Virtual = 'F') ranked_schools WHERE rnk <= 5
```

**生成结果**: []

**预期结果**: [{'School': 'Academy of Arts and Sciences: Fresno'}, {'School': 'Dunlap Leadership Academy'}, {'School': 'Insight School of California'}] ... (+31行)

---

## 61. [ID:46]

**问题**: Which state special schools have the highest number of enrollees from grades 1 through 12?

**证据**: (无)

**生成SQL**:
```sql
SELECT s.School, s.District, s.County, f.`Enrollment (K-12)` FROM schools s INNER JOIN frpm f ON s.CDSCode = f.CDSCode WHERE s.DOC = '31' ORDER BY f.`Enrollment (K-12)` DESC LIMIT 1
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

**生成结果**: [{'School': 'California School for the Deaf-Fremont', 'District': 'California School for the Deaf-Fremont (State Special Schl)', 'County': 'Alameda', 'Enrollment (K-12)': 410.0}]

**预期结果**: [{'School': 'California School for the Deaf-Fremont'}]

---

## 62. [ID:82]

**问题**: What is the grade span offered in the school with the highest longitude?

**证据**: (无)

**生成SQL**:
```sql
SELECT GSoffered FROM schools WHERE Longitude = (SELECT MAX(ABS(Longitude)) FROM schools)
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

**生成结果**: []

**预期结果**: [{'GSoffered': 'K-8'}]

---

## 63. [ID:112]

**问题**: For the female client who was born in 1976/1/29, which district did she opened her account?

**证据**: (无)

**生成SQL**:
```sql
SELECT d.A2 FROM client c INNER JOIN account a ON c.district_id = a.district_id INNER JOIN district d ON a.district_id = d.district_id WHERE c.gender = 'F' AND c.birth_date = '1976-01-29'
```

**预期SQL**:
```sql
SELECT
  `T1`.`A2`
FROM `district` AS `T1`
INNER JOIN `client` AS `T2`
  ON `T1`.`district_id` = `T2`.`district_id`
WHERE
  `T2`.`birth_date` = '1976-01-29' AND `T2`.`gender` = 'F'
```

**生成结果**: [{'A2': 'Tachov'}, {'A2': 'Tachov'}, {'A2': 'Tachov'}] ... (+47行)

**预期结果**: [{'A2': 'Tachov'}]

---

## 64. [ID:159]

**问题**: List all the withdrawals in cash transactions that the client with the id 3356 makes.

**证据**: (无)

**生成SQL**:
```sql
SELECT trans.trans_id, trans.account_id, trans.date, trans.type, trans.operation, trans.amount, trans.balance, trans.k_symbol, trans.bank, trans.account FROM trans INNER JOIN disp ON trans.account_id = disp.account_id WHERE disp.client_id = 3356 AND trans.operation = 'VYBER'
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

**生成结果**: [{'trans_id': 816173, 'account_id': 2779, 'date': '1993-12-02', 'type': 'VYDAJ', 'operation': 'VYBER', 'amount': 800, 'balance': 42072, 'k_symbol': None, 'bank': None, 'account': None}, {'trans_id': 816174, 'account_id': 2779, 'date': '1994-12-29', 'type': 'VYDAJ', 'operation': 'VYBER', 'amount': 2400, 'balance': 59207, 'k_symbol': None, 'bank': None, 'account': None}, {'trans_id': 816175, 'account_id': 2779, 'date': '1995-12-05', 'type': 'VYDAJ', 'operation': 'VYBER', 'amount': 4320, 'balance': 45682, 'k_symbol': None, 'bank': None, 'account': None}] ... (+137行)

**预期结果**: [{'trans_id': 816173}, {'trans_id': 816174}, {'trans_id': 816175}] ... (+137行)

---

---

# Moderate 难度失败案例 (127个)

## 1. [ID:1479]

**问题**: Which year recorded the most consumption of gas paid in CZK?

**证据**: (无)

**生成SQL**:
```sql
SELECT SUBSTRING(Date, 1, 4) AS Year FROM yearmonth WHERE Currency = 'CZK' GROUP BY SUBSTRING(Date, 1, 4) ORDER BY SUM(Consumption) DESC LIMIT 1
```

**预期SQL**:
```sql
SELECT
  SUBSTR(`T2`.`Date`, 1, 4)
FROM `customers` AS `T1`
INNER JOIN `yearmonth` AS `T2`
  ON `T1`.`CustomerID` = `T2`.`CustomerID`
WHERE
  `T1`.`Currency` = 'CZK'
GROUP BY
  SUBSTR(`T2`.`Date`, 1, 4)
ORDER BY
  SUM(`T2`.`Consumption`) DESC
LIMIT 1
```

**生成结果**: []

**预期结果**: [{'SUBSTR(`T2`.`Date`, 1, 4)': '2013'}]

---

## 2. [ID:1490]

**问题**: How many percent of LAM customer consumed more than 46.73?

**证据**: (无)

**生成SQL**:
```sql
SELECT (COUNT(DISTINCT CASE WHEN ym.Consumption > 46.73 THEN c.CustomerID END) * 100.0 / COUNT(DISTINCT c.CustomerID)) AS percentage FROM customers c INNER JOIN yearmonth ym ON c.CustomerID = ym.CustomerID WHERE c.Segment = 'LAM'
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

**生成结果**: [{'percentage': 99.52922}]

**预期结果**: [{'CAST(SUM(CASE WHEN `T2`.`Consumption` > 46.73 THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(`T1`.`CustomerID`)': 98.5267932135058}]

---

## 3. [ID:1501]

**问题**: Please list the countries of the gas stations with transactions taken place in June, 2013.

**证据**: (无)

**生成SQL**:
```sql
SELECT DISTINCT Country FROM gasstations WHERE GasStationID IN (SELECT GasStationID FROM transactions_1k WHERE Date >= '2013-06-01' AND Date <= '2013-06-30')
```

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

**生成结果**: []

**预期结果**: [{'Country': 'CZE'}, {'Country': 'SVK'}]

---

## 4. [ID:1529]

**问题**: What is the amount spent by customer "38508" at the gas stations? How much had the customer spent in January 2012?

**证据**: (无)

**生成SQL**:
```sql
SELECT SUM(Amount) FROM transactions_1k WHERE CustomerID = 38508 AND Date >= '2012-01-01' AND Date <= '2012-01-31'
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

**生成结果**: [{'SUM(Amount)': None}]

**预期结果**: [{'SUM(`T1`.`Price` )': 68740.19999999992, "SUM(CASE WHEN `T3`.`Date` = '201201' THEN `T1`.`Price` ELSE 0 END)": 3437.0099999999998}]

---

## 5. [ID:1531]

**问题**: Who is the top spending customer and how much is the average price per single item purchased by this customer? What currency was being used?

**证据**: (无)

**生成SQL**:
```sql
SELECT c.CustomerID, AVG(t.Price) AS avg_price_per_item, c.Currency FROM transactions_1k t INNER JOIN customers c ON t.CustomerID = c.CustomerID GROUP BY c.CustomerID, c.Currency ORDER BY SUM(t.Amount) DESC LIMIT 1
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

**生成结果**: [{'CustomerID': 16358, 'avg_price_per_item': 1680.188, 'Currency': 'CZK'}]

**预期结果**: [{'CustomerID': 12459, 'SUM(`T2`.`Price` / `T2`.`Amount`)': 203.85607873542577, 'Currency': 'CZK'}]

---

## 6. [ID:1533]

**问题**: For all the people who paid more than 29.00 per unit of product id No.5. Give their consumption status in the August of 2012.

**证据**: (无)

**生成SQL**:
```sql
SELECT c.Segment FROM transactions_1k t INNER JOIN customers c ON t.CustomerID = c.CustomerID WHERE t.ProductID = 5 AND t.Price / t.Amount > 29.00 AND t.Date >= '2012-08-01' AND t.Date <= '2012-08-31' GROUP BY c.Segment
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

**生成结果**: [{'Segment': 'SME'}, {'Segment': 'KAM'}, {'Segment': 'LAM'}]

**预期结果**: [{'Consumption': 1903.2}, {'Consumption': 88265.39}, {'Consumption': 1129.2}] ... (+7行)

---

## 7. [ID:1322]

**问题**: Among the events attended by more than 10 members of the Student_Club, how many of them are meetings?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(*) FROM (SELECT event_id FROM event WHERE type = 'Meeting' AND event_id IN (SELECT link_to_event FROM attendance GROUP BY link_to_event HAVING COUNT(link_to_member) > 10)) AS meeting_events
```

**预期SQL**:
```sql
SELECT COUNT(DISTINCT T1.event_id) FROM event AS T1 INNER JOIN attendance AS T2 ON T1.event_id = T2.link_to_event WHERE T1.type = 'Meeting' GROUP BY T1.event_id HAVING COUNT(T2.link_to_event) > 10
```

**生成结果**: [{'COUNT(*)': 4}]

**预期结果**: [{'COUNT(DISTINCT T1.event_id)': 1}, {'COUNT(DISTINCT T1.event_id)': 1}, {'COUNT(DISTINCT T1.event_id)': 1}] ... (+1行)

---

## 8. [ID:1338]

**问题**: Was each expense in October Meeting on October 8, 2019 approved?

**证据**: (无)

**生成SQL**:
```sql
SELECT e.expense_id, e.approved FROM expense e INNER JOIN budget b ON e.link_to_budget = b.budget_id INNER JOIN event ev ON b.link_to_event = ev.event_id WHERE ev.event_name = 'October Meeting' AND ev.event_date = '2019-10-08'
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

**生成结果**: []

**预期结果**: [{'approved': 'true'}, {'approved': 'true'}, {'approved': 'true'}]

---

## 9. [ID:1350]

**问题**: What is the status of the event which bought "Post Cards, Posters" on 2019/8/20?

**证据**: (无)

**生成SQL**:
```sql
SELECT e.status FROM event e INNER JOIN budget b ON e.event_id = b.link_to_event INNER JOIN expense exp ON b.budget_id = exp.link_to_budget WHERE exp.expense_description = 'Post Cards, Posters' AND exp.expense_date = '2019-8-20'
```

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

**生成结果**: []

**预期结果**: [{'event_status': 'Closed'}]

---

## 10. [ID:1387]

**问题**: Which student has been entrusted to manage the budget for the Yearly Kickoff?

**证据**: (无)

**生成SQL**:
```sql
SELECT m.first_name, m.last_name FROM member m INNER JOIN budget b ON m.member_id = b.link_to_event INNER JOIN event e ON b.link_to_event = e.event_id WHERE e.event_name = 'Yearly Kickoff'
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

**生成结果**: []

**预期结果**: [{'first_name': 'Elijah', 'last_name': 'Allen'}, {'first_name': 'Elijah', 'last_name': 'Allen'}, {'first_name': 'Sacha', 'last_name': 'Harrison'}] ... (+1行)

---

## 11. [ID:1399]

**问题**: Did Maya Mclean attend the 'Women's Soccer' event?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(*) > 0 AS attended FROM attendance WHERE link_to_event IN (SELECT event_id FROM event WHERE event_name = 'Women\'s Soccer') AND link_to_member IN (SELECT member_id FROM member WHERE CONCAT(first_name, ' ', last_name) = 'Maya Mclean')
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

**生成结果**: [{'attended': 1}]

**预期结果**: [{'result': 'YES'}, {'result': None}, {'result': None}] ... (+11行)

---

## 12. [ID:1404]

**问题**: Identify the type of expenses and their total value approved for 'October Meeting' event.

**证据**: (无)

**生成SQL**:
```sql
SELECT b.category, SUM(e.cost) AS total_value FROM expense e INNER JOIN budget b ON e.link_to_budget = b.budget_id INNER JOIN event ev ON b.link_to_event = ev.event_id WHERE ev.event_name = 'October Meeting' AND e.approved = 'true' GROUP BY b.category
```

**预期SQL**:
```sql
SELECT `T1`.`type`, SUM(`T3`.`cost`) AS `total_cost` FROM `event` AS `T1` INNER JOIN `budget` AS `T2` ON `T1`.`event_id` = `T2`.`link_to_event` INNER JOIN `expense` AS `T3` ON `T2`.`budget_id` = `T3`.`link_to_budget` WHERE `T1`.`event_name` = 'October Meeting' GROUP BY `T1`.`type`
```

**生成结果**: [{'category': 'Food', 'total_value': 121.14}, {'category': 'Advertisement', 'total_value': 54.25}]

**预期结果**: [{'type': 'Meeting', 'total_cost': 175.39}]

---

## 13. [ID:1427]

**问题**: What are the budget category of the events located at MU 215 and a guest speaker type with a 0 budget spent?

**证据**: (无)

**生成SQL**:
```sql
SELECT b.category FROM budget b INNER JOIN event e ON b.link_to_event = e.event_id WHERE e.location = 'MU 215' AND e.type = 'Guest Speaker' AND b.spent = 0
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

**生成结果**: [{'category': 'Speaker Gifts'}, {'category': 'Parking'}, {'category': 'Advertisement'}] ... (+13行)

**预期结果**: [{'category': 'Speaker Gifts', 'type': 'Guest Speaker'}, {'category': 'Parking', 'type': 'Guest Speaker'}, {'category': 'Advertisement', 'type': 'Guest Speaker'}] ... (+1行)

---

## 14. [ID:1435]

**问题**: List the names of closed event as "game" that was closed from 3/15/2019 to 3/20/2020.

**证据**: (无)

**生成SQL**:
```sql
SELECT event_name FROM event WHERE type = 'Game' AND status = 'Closed' AND event_date BETWEEN '2019-03-15' AND '2020-03-20'
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

**生成结果**: [{'event_name': "Women's Soccer"}, {'event_name': 'Football game'}, {'event_name': 'Football game'}]

**预期结果**: [{'event_name': "Women's Soccer"}, {'event_name': 'Football game'}]

---

## 15. [ID:1149]

**问题**: Are there more in-patient or outpatient who were male? What is the deviation in percentage?

**证据**: (无)

**生成SQL**:
```sql
SELECT (SELECT COUNT(ID) FROM Patient WHERE SEX = 'M' AND Admission = '+') AS in_patient_count, (SELECT COUNT(ID) FROM Patient WHERE SEX = 'M' AND Admission = '-') AS out_patient_count, CAST((SELECT COUNT(ID) FROM Patient WHERE SEX = 'M' AND Admission = '+') AS DOUBLE) / CAST((SELECT COUNT(ID) FROM Patient WHERE SEX = 'M' AND Admission = '-') AS DOUBLE) AS deviation_percentage
```

**预期SQL**:
```sql
SELECT
  CAST(SUM(CASE WHEN `Admission` = '+' THEN 1 ELSE 0 END) AS DOUBLE) * 100 / SUM(CASE WHEN `Admission` = '-' THEN 1 ELSE 0 END)
FROM `Patient`
WHERE
  `SEX` = 'M'
```

**生成结果**: [{'in_patient_count': 89, 'out_patient_count': 107, 'deviation_percentage': 0.8317757009345794}]

**预期结果**: [{"CAST(SUM(CASE WHEN `Admission` = '+' THEN 1 ELSE 0 END) AS DOUBLE) * 100 / SUM(CASE WHEN `Admission` = '-' THEN 1 ELSE 0 END)": 83.17757009345794}]

---

## 16. [ID:1152]

**问题**: What is the ratio of outpatient to inpatient followed up treatment among all the 'SLE' diagnosed patient?

**证据**: (无)

**生成SQL**:
```sql
SELECT CAST(SUM(CASE WHEN Admission = '+' THEN 1 ELSE 0 END) AS DOUBLE) / CAST(SUM(CASE WHEN Admission = '-' THEN 1 ELSE 0 END) AS DOUBLE) AS outpatient_inpatient_ratio FROM Patient WHERE Diagnosis LIKE '%SLE%'
```

**预期SQL**:
```sql
SELECT
  SUM(CASE WHEN `Admission` = '+' THEN 1 ELSE 0 END) / SUM(CASE WHEN `Admission` = '-' THEN 1 ELSE 0 END)
FROM `Patient`
WHERE
  `Diagnosis` = 'SLE'
```

**生成结果**: [{'outpatient_inpatient_ratio': 1.2857142857142858}]

**预期结果**: [{"SUM(CASE WHEN `Admission` = '+' THEN 1 ELSE 0 END) / SUM(CASE WHEN `Admission` = '-' THEN 1 ELSE 0 END)": 1.3095}]

---

## 17. [ID:1164]

**问题**: How many of the patients with the most serious thrombosis cases examined in 1997 are women?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(DISTINCT e.ID) FROM Examination e INNER JOIN Patient p ON e.ID = p.ID WHERE e.Thrombosis = 1 AND YEAR(e."Examination Date") = 1997 AND p.SEX = 'F'
```

**预期SQL**:
```sql
SELECT
  COUNT(*)
FROM `Patient` AS `T1`
INNER JOIN `Examination` AS `T2`
  ON `T1`.`ID` = `T2`.`ID`
WHERE
  `T1`.`SEX` = 'F'
  AND DATE_FORMAT(CAST(`T2`.`Examination Date` AS DATETIME), '%Y') = '1997'
  AND `T2`.`Thrombosis` = 1
```

**生成结果**: []

**预期结果**: [{'COUNT(*)': 1}]

---

## 18. [ID:1175]

**问题**: How old was the patient who had the highest hemoglobin count at the time of the examination, and what is the doctor's diagnosis?

**证据**: (无)

**生成SQL**:
```sql
SELECT (YEAR(T2.`Examination Date`) - YEAR(T1.Birthday)) AS Age, T2.Diagnosis FROM Patient T1 INNER JOIN Examination T2 ON T1.ID = T2.ID WHERE T2.`Examination Date` = (SELECT MAX(T3.`Examination Date`) FROM Examination T3 WHERE T3.ID = T2.ID) ORDER BY T2.`Examination Date` DESC LIMIT 1
```

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

**生成结果**: [{'Age': 37, 'Diagnosis': 'SLE, SjS, vertigo'}]

**预期结果**: [{"DATE_FORMAT(CAST(`T2`.`Date` AS DATETIME), '%Y') - DATE_FORMAT(CAST(`T1`.`Birthday` AS DATETIME), '%Y')": 28.0, 'Diagnosis': 'SLE'}]

---

## 19. [ID:1179]

**问题**: For the patient who was diagnosed with SLE on 1994/2/19, what was his/her anti-Cardiolipin antibody concentration status on 1993/11/12?

**证据**: (无)

**生成SQL**:
```sql
SELECT aCL IgM FROM Examination WHERE ID = (SELECT ID FROM Patient WHERE Diagnosis LIKE '%SLE%' AND Description = '1994-02-19') AND Examination Date = '1993-11-12'
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

**生成结果**: []

**预期结果**: [{'aCL IgA': 3, 'aCL IgG': 5.1, 'aCL IgM': 4.1}]

---

## 20. [ID:1187]

**问题**: How many patients who were examined between 1987/7/6 and 1996/1/31 had a GPT level greater than 30 and an ALB level less than 4? List them by their ID.

**证据**: (无)

**生成SQL**:
```sql
SELECT ID FROM Laboratory WHERE Date BETWEEN '1987-07-06' AND '1996-01-31' AND GPT > 30 AND ALB < 4
```

**预期SQL**:
```sql
SELECT DISTINCT
  `ID`
FROM `Laboratory`
WHERE
  `Date` BETWEEN '1987-07-06' AND '1996-01-31' AND `GPT` > 30 AND `ALB` < 4
```

**生成结果**: [{'ID': 27654}, {'ID': 27654}, {'ID': 27654}] ... (+462行)

**预期结果**: [{'ID': 27654}, {'ID': 71417}, {'ID': 912147}] ... (+60行)

---

## 21. [ID:1205]

**问题**: Was the patient with the number 57266's uric acid within a normal range?

**证据**: (无)

**生成SQL**:
```sql
SELECT CASE WHEN p.SEX = 'M' AND l.UA > 8.0 THEN 'Abnormal' WHEN p.SEX = 'F' AND l.UA > 6.5 THEN 'Abnormal' ELSE 'Normal' END AS uric_acid_status FROM Laboratory l INNER JOIN Patient p ON l.ID = p.ID WHERE p.ID = 57266 ORDER BY l.Date DESC LIMIT 1
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

**生成结果**: [{'uric_acid_status': 'Normal'}]

**预期结果**: [{"CASE\n    WHEN (\n      `T1`.`SEX` = 'F' AND `T2`.`UA` > 6.5\n    )\n    OR (\n      `T1`.`SEX` = 'M' AND `T2`.`UA` > 8.0\n    )\n    THEN TRUE\n    ELSE FALSE\n  END": 0}, {"CASE\n    WHEN (\n      `T1`.`SEX` = 'F' AND `T2`.`UA` > 6.5\n    )\n    OR (\n      `T1`.`SEX` = 'M' AND `T2`.`UA` > 8.0\n    )\n    THEN TRUE\n    ELSE FALSE\n  END": 0}, {"CASE\n    WHEN (\n      `T1`.`SEX` = 'F' AND `T2`.`UA` > 6.5\n    )\n    OR (\n      `T1`.`SEX` = 'M' AND `T2`.`UA` > 8.0\n    )\n    THEN TRUE\n    ELSE FALSE\n  END": 0}] ... (+64行)

---

## 22. [ID:1209]

**问题**: Please provide the diagnosis of patients with ALT glutamic pylvic transaminase beyond the normal range by ascending order of their date of birth.

**证据**: (无)

**生成SQL**:
```sql
SELECT DISTINCT P.ID, P.Diagnosis FROM Patient P INNER JOIN Laboratory L ON P.ID = L.ID WHERE L.GPT > 60 ORDER BY P.Birthday ASC
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

**生成结果**: []

**预期结果**: [{'Diagnosis': 'MRA'}, {'Diagnosis': 'MRA'}, {'Diagnosis': 'MRA'}] ... (+868行)

---

## 23. [ID:1225]

**问题**: List and group all patients by sex for total bilirubin (T-BIL) level not within the normal range.

**证据**: (无)

**生成SQL**:
```sql
SELECT p.ID, p.SEX, l.`T-BIL` FROM Patient p INNER JOIN Laboratory l ON p.ID = l.ID WHERE l.`T-BIL` >= 2.0 ORDER BY p.SEX, p.ID
```

**预期SQL**:
```sql
SELECT T1.ID, T1.SEX FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.`T-BIL` >= 2.0 GROUP BY T1.SEX, T1.ID
```

**生成结果**: [{'ID': 250391, 'SEX': 'F', 'T-BIL': 2.8}, {'ID': 1180510, 'SEX': 'F', 'T-BIL': 2.6}, {'ID': 1180510, 'SEX': 'F', 'T-BIL': 2.5}] ... (+63行)

**预期结果**: [{'ID': 43003, 'SEX': 'M'}, {'ID': 250391, 'SEX': 'F'}, {'ID': 444499, 'SEX': 'M'}] ... (+7行)

---

## 24. [ID:1227]

**问题**: What is the average age of the male patient with high cholesterol?

**证据**: (无)

**生成SQL**:
```sql
SELECT AVG(DATEDIFF(CURDATE(), p.Birthday) / 365.25) AS average_age FROM Patient p INNER JOIN Laboratory l ON p.ID = l.ID WHERE p.SEX = 'M' AND l.`T-CHO` >= 250
```

**预期SQL**:
```sql
SELECT AVG(YEAR(CURRENT_DATE) - YEAR(T1.Birthday)) FROM Patient AS T1  INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID  WHERE T2.`T-CHO` >= 250 AND T1.SEX = 'M'
```

**生成结果**: [{'average_age': 74.22226487}]

**预期结果**: [{'AVG(YEAR(CURRENT_DATE) - YEAR(T1.Birthday))': 74.6854}]

---

## 25. [ID:1235]

**问题**: What are the patient's diagnosis for those who has lower red blood blood cell? State their ID and age.

**证据**: (无)

**生成SQL**:
```sql
SELECT p.ID, (YEAR(CURDATE()) - YEAR(p.Birthday)) AS age, p.Diagnosis FROM Patient p INNER JOIN Laboratory l ON p.ID = l.ID WHERE l.RBC < 3.5
```

**预期SQL**:
```sql
SELECT DISTINCT
  `T1`.`Diagnosis`,
  `T1`.`ID`,
  DATE_FORMAT(CAST(CURRENT_TIMESTAMP() AS DATETIME), '%Y') - DATE_FORMAT(CAST(`T1`.`Birthday` AS DATETIME), '%Y')
FROM `Patient` AS `T1`
INNER JOIN `Laboratory` AS `T2`
  ON `T1`.`ID` = `T2`.`ID`
WHERE
  `T2`.`RBC` < 3.5
```

**生成结果**: [{'ID': 27654, 'age': 90, 'Diagnosis': 'RA, SLE susp'}, {'ID': 27654, 'age': 90, 'Diagnosis': 'RA, SLE susp'}, {'ID': 27654, 'age': 90, 'Diagnosis': 'RA, SLE susp'}] ... (+756行)

**预期结果**: [{'Diagnosis': 'RA, SLE susp', 'ID': 27654, "DATE_FORMAT(CAST(CURRENT_TIMESTAMP() AS DATETIME), '%Y') - DATE_FORMAT(CAST(`T1`.`Birthday` AS DATETIME), '%Y')": 90.0}, {'Diagnosis': 'SLE, MCTD', 'ID': 30609, "DATE_FORMAT(CAST(CURRENT_TIMESTAMP() AS DATETIME), '%Y') - DATE_FORMAT(CAST(`T1`.`Birthday` AS DATETIME), '%Y')": 82.0}, {'Diagnosis': 'SJS', 'ID': 58139, "DATE_FORMAT(CAST(CURRENT_TIMESTAMP() AS DATETIME), '%Y') - DATE_FORMAT(CAST(`T1`.`Birthday` AS DATETIME), '%Y')": 54.0}] ... (+70行)

---

## 26. [ID:1252]

**问题**: Among the patients with a normal Ig G level, how many of them have symptoms?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(DISTINCT Laboratory.ID) FROM Laboratory WHERE Laboratory.IGG > 900 AND Laboratory.IGG < 2000 AND EXISTS (SELECT 1 FROM Examination WHERE Examination.ID = Laboratory.ID AND Examination.Symptoms IS NOT NULL)
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

**生成结果**: [{'COUNT(DISTINCT Laboratory.ID)': 1}]

**预期结果**: [{'COUNT(`T1`.`ID`)': 4}]

---

## 27. [ID:1254]

**问题**: How many patients with a normal Ig A level came to the hospital after 1990/1/1?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(DISTINCT Patient.ID) FROM Patient INNER JOIN Laboratory ON Patient.ID = Laboratory.ID WHERE Laboratory.IGA > 80 AND Laboratory.IGA < 500 AND YEAR(Patient.`First Date`) >= 1990
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

**生成结果**: [{'COUNT(DISTINCT Patient.ID)': 140}]

**预期结果**: [{'COUNT(`T1`.`ID`)': 1590}]

---

## 28. [ID:1255]

**问题**: For the patients with an abnormal Ig M level, what is the most common disease they are diagnosed with?

**证据**: (无)

**生成SQL**:
```sql
SELECT Diagnosis FROM Laboratory WHERE IGM <= 40 OR IGM >= 400 GROUP BY Diagnosis ORDER BY COUNT(*) DESC LIMIT 1
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

**生成结果**: []

**预期结果**: [{'Diagnosis': 'RA'}]

---

## 29. [ID:1256]

**问题**: How many patients with a abnormal C-reactive protein don't have their data recorded?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(*) FROM Patient WHERE ID NOT IN (SELECT DISTINCT ID FROM Laboratory WHERE CRP = '+') AND Description IS NULL
```

**预期SQL**:
```sql
SELECT COUNT(T1.ID) FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE (T2.CRP = '+' ) AND T1.Description IS NULL;
```

**生成结果**: [{'COUNT(*)': 191}]

**预期结果**: [{'COUNT(T1.ID)': 208}]

---

## 30. [ID:1265]

**问题**: How many patients have a normal level of anti-ribonuclear protein and have been admitted to the hospital?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(DISTINCT Laboratory.ID) FROM Laboratory INNER JOIN Patient ON Laboratory.ID = Patient.ID WHERE Laboratory.RNP IN ('-', '+-') AND Patient.Admission = '+'
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

**生成结果**: [{'COUNT(DISTINCT Laboratory.ID)': 0}]

**预期结果**: [{'COUNT(DISTINCT `T1`.`ID`)': 47}]

---

## 31. [ID:1267]

**问题**: Among the patients with normal anti-SM, how many of them does not have thrombosis?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(DISTINCT T1.ID) FROM Patient T1 INNER JOIN Laboratory T2 ON T1.ID = T2.ID INNER JOIN Examination T3 ON T1.ID = T3.ID WHERE T2.SM IN ('-', '+-') AND T3.Thrombosis = 0
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

**生成结果**: [{'COUNT(DISTINCT T1.ID)': 0}]

**预期结果**: [{'COUNT(`T1`.`ID`)': 7}]

---

## 32. [ID:1275]

**问题**: Among the patients who has a normal level of anti-centromere and a normal level of anti-SSB, how many of them are male?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(DISTINCT T1.ID) FROM Patient T1 INNER JOIN Laboratory T2 ON T1.ID = T2.ID WHERE T1.SEX = 'M' AND T2.CENTROMEA IN ('-', '+-') AND T2.SSB IN ('-', '+-')
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

**生成结果**: [{'COUNT(DISTINCT T1.ID)': 0}]

**预期结果**: [{'COUNT(DISTINCT `T1`.`ID`)': 1}]

---

## 33. [ID:1281]

**问题**: Among the patients who have an abnormal level of glutamic oxaloacetic transaminase, when was the youngest of them born?

**证据**: (无)

**生成SQL**:
```sql
SELECT MIN(P.Birthday) FROM Patient P INNER JOIN Laboratory L ON P.ID = L.ID WHERE L.GOT >= 60
```

**预期SQL**:
```sql
SELECT
  `T1`.`Birthday`
FROM `Patient` AS `T1`
INNER JOIN `Laboratory` AS `T2`
  ON `T1`.`ID` = `T2`.`ID`
WHERE
  `T2`.`GOT` >= 60
ORDER BY
  `T1`.`Birthday` DESC
LIMIT 1
```

**生成结果**: [{'MIN(P.Birthday)': '1922-12-01'}]

**预期结果**: [{'Birthday': '1987-12-05'}]

---

## 34. [ID:1025]

**问题**: Give the name of the league had the most goals in the 2016 season?

**证据**: (无)

**生成SQL**:
```sql
SELECT l.name FROM League l JOIN Match m ON l.id = m.league_id WHERE m.season = '2015/2016' GROUP BY l.name ORDER BY SUM(m.home_team_goal + m.away_team_goal) DESC LIMIT 1
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

**生成结果**: []

**预期结果**: [{'name': 'Spain LIGA BBVA'}]

---

## 35. [ID:1029]

**问题**: What are the speed in which attacks are put together of the top 4 teams with the highest build Up Play Speed?

**证据**: (无)

**生成SQL**:
```sql
SELECT T1.buildUpPlaySpeed FROM Team_Attributes T1 INNER JOIN Team T2 ON T1.team_api_id = T2.team_api_id ORDER BY T1.buildUpPlaySpeed DESC LIMIT 4
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

**生成结果**: [{'buildUpPlaySpeed': 80}, {'buildUpPlaySpeed': 78}, {'buildUpPlaySpeed': 78}] ... (+1行)

**预期结果**: [{'buildUpPlaySpeed': 20}, {'buildUpPlaySpeed': 20}, {'buildUpPlaySpeed': 20}] ... (+1行)

---

## 36. [ID:1030]

**问题**: Give the name of the league had the most matches end as draw in the 2016 season?

**证据**: (无)

**生成SQL**:
```sql
SELECT L.name FROM League L INNER JOIN Match M ON L.id = M.league_id WHERE M.season = '2015/2016' AND M.home_team_goal = M.away_team_goal GROUP BY L.name ORDER BY COUNT(*) DESC LIMIT 1
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

**生成结果**: []

**预期结果**: [{'name': 'France Ligue 1'}]

---

## 37. [ID:1032]

**问题**: Give the name of the league with the highest matches of all time and how many matches were played in the said league.

**证据**: (无)

**生成SQL**:
```sql
SELECT L.name, COUNT(M.id) AS match_count FROM Match M INNER JOIN League L ON M.league_id = L.id GROUP BY L.id, L.name ORDER BY match_count DESC LIMIT 1
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

**生成结果**: []

**预期结果**: [{'name': 'England Premier League', 'COUNT(`t1`.`id`)': 3040}]

---

## 38. [ID:1057]

**问题**: Calculate the average home team goal in the 2010/2011 season in the country of Poland.

**证据**: (无)

**生成SQL**:
```sql
SELECT AVG(home_team_goal) FROM Match WHERE season = '2010/2011' AND country_id = (SELECT id FROM Country WHERE name = 'Poland')
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

**生成结果**: []

**预期结果**: [{'CAST(SUM(`t2`.`home_team_goal`) AS DOUBLE) / COUNT(`t2`.`id`)': 1.5041666666666667}]

---

## 39. [ID:1068]

**问题**: From 2010 to 2015, what was the average overall rating of players who are higher than 170?

**证据**: (无)

**生成SQL**:
```sql
SELECT AVG(t2.overall_rating) FROM Player_Attributes t2 INNER JOIN Player t1 ON t2.player_api_id = t1.player_api_id WHERE t1.height > 170 AND strftime('%Y', t2.date) >= '2010' AND strftime('%Y', t2.date) <= '2015'
```

**预期SQL**:
```sql
SELECT
  CAST(SUM(`t2`.`overall_rating`) AS DOUBLE) / COUNT(`t2`.`id`)
FROM `Player` AS `t1`
INNER JOIN `Player_Attributes` AS `t2`
  ON `t1`.`player_api_id` = `t2`.`player_api_id`
WHERE
  `t1`.`height` > 170
  AND DATE_FORMAT(CAST(`t2`.`date` AS DATETIME), '%Y') >= '2010'
  AND DATE_FORMAT(CAST(`t2`.`date` AS DATETIME), '%Y') <= '2015'
```

**生成结果**: []

**预期结果**: [{'CAST(SUM(`t2`.`overall_rating`) AS DOUBLE) / COUNT(`t2`.`id`)': 68.87610612712349}]

---

## 40. [ID:1091]

**问题**: How many matches were held in the Belgium Jupiler League in April, 2009?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(*) FROM Match WHERE league_id = (SELECT id FROM League WHERE name = 'Belgium Jupiler League') AND SUBSTR(date, 1, 7) = '2009-04'
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

**生成结果**: []

**预期结果**: [{'COUNT(`t2`.`id`)': 36}]

---

## 41. [ID:1107]

**问题**: When was the first time did Kevin Constant have his highest crossing score? Give the date.

**证据**: (无)

**生成SQL**:
```sql
SELECT date FROM Player_Attributes WHERE player_api_id = (SELECT player_api_id FROM Player WHERE player_name = 'Kevin Constant') AND crossing = (SELECT MAX(crossing) FROM Player_Attributes WHERE player_api_id = (SELECT player_api_id FROM Player WHERE player_name = 'Kevin Constant')) ORDER BY date ASC LIMIT 1
```

**预期SQL**:
```sql
SELECT `date` FROM (SELECT `t2`.`crossing`, `t2`.`date` FROM `Player` AS `t1` INNER JOIN `Player_Attributes` AS `t2` ON `t1`.`player_fifa_api_id` = `t2`.`player_fifa_api_id` WHERE `t1`.`player_name` = 'Kevin Constant' ORDER BY `t2`.`crossing` DESC) AS `subquery` ORDER BY `date` DESC LIMIT 1
```

**生成结果**: [{'date': '2013-02-15 00:00:00'}]

**预期结果**: [{'date': '2016-04-21 00:00:00'}]

---

## 42. [ID:1124]

**问题**: Who are the players that tend to be attacking when their mates were doing attack moves? List down their name.

**证据**: (无)

**生成SQL**:
```sql
SELECT DISTINCT p.player_name FROM Player p INNER JOIN Player_Attributes pa ON p.player_api_id = pa.player_api_id OR p.player_fifa_api_id = pa.player_fifa_api_id WHERE pa.attacking_work_rate = 'high'
```

**预期SQL**:
```sql
SELECT DISTINCT
  `t1`.`player_name`
FROM `Player` AS `t1`
INNER JOIN `Player_Attributes` AS `t2`
  ON `t1`.`player_api_id` = `t2`.`player_api_id`
WHERE
  `t2`.`attacking_work_rate` = 'high'
```

**生成结果**: [{'player_name': 'Aaron Cresswell'}, {'player_name': 'Aaron Lennon'}, {'player_name': 'Aaron Meijers'}] ... (+997行)

**预期结果**: [{'player_name': 'Aaron Cresswell'}, {'player_name': 'Aaron Lennon'}, {'player_name': 'Aaron Meijers'}] ... (+997行)

---

## 43. [ID:1141]

**问题**: Does the KSV Cercle Brugge team have a slow, balanced or fast speed class?

**证据**: (无)

**生成SQL**:
```sql
SELECT buildUpPlaySpeedClass FROM Team_Attributes WHERE team_api_id = (SELECT team_api_id FROM Team WHERE team_long_name = 'KSV Cercle Brugge') ORDER BY date DESC LIMIT 1
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

**生成结果**: [{'buildUpPlaySpeedClass': 'Balanced'}]

**预期结果**: [{'buildUpPlaySpeedClass': 'Balanced'}, {'buildUpPlaySpeedClass': 'Fast'}]

---

## 44. [ID:1146]

**问题**: Please provide the full name of the away team that scored the most goals.

**证据**: (无)

**生成SQL**:
```sql
SELECT T2.team_long_name FROM Match T1 INNER JOIN Team T2 ON T1.away_team_api_id = T2.team_api_id GROUP BY T2.team_long_name ORDER BY SUM(T1.away_team_goal) DESC LIMIT 1
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

**生成结果**: []

**预期结果**: [{'team_long_name': 'Paris Saint-Germain'}]

---

## 45. [ID:846]

**问题**: Please list the reference names of the drivers who are eliminated in the first period in race number 20.

**证据**: (无)

**生成SQL**:
```sql
SELECT DISTINCT d.driverRef FROM drivers d INNER JOIN qualifying q ON d.driverId = q.driverId WHERE q.raceId = 20 AND q.position > 5
```

**预期SQL**:
```sql
SELECT
  `T2`.`driverRef`
FROM `qualifying` AS `T1`
INNER JOIN `drivers` AS `T2`
  ON `T2`.`driverId` = `T1`.`driverId`
WHERE
  `T1`.`raceId` = 20
ORDER BY
  `T1`.`q1` DESC
LIMIT 5
```

**生成结果**: [{'driverRef': 'heidfeld'}, {'driverRef': 'trulli'}, {'driverRef': 'rosberg'}] ... (+14行)

**预期结果**: [{'driverRef': 'sato'}, {'driverRef': 'davidson'}, {'driverRef': 'vettel'}] ... (+2行)

---

## 46. [ID:866]

**问题**: Who was the player that got the lap time of 0:01:27 in the race No. 161? Show his introduction website.

**证据**: (无)

**生成SQL**:
```sql
SELECT d.url FROM lapTimes l JOIN drivers d ON l.driverId = d.driverId WHERE l.raceId = 161 AND l.time LIKE '0:01:27%'
```

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

**生成结果**: []

**预期结果**: [{'forename': 'David', 'surname': 'Coulthard', 'url': 'http://en.wikipedia.org/wiki/David_Coulthard'}, {'forename': 'Jarno', 'surname': 'Trulli', 'url': 'http://en.wikipedia.org/wiki/Jarno_Trulli'}, {'forename': 'Jenson', 'surname': 'Button', 'url': 'http://en.wikipedia.org/wiki/Jenson_Button'}] ... (+6行)

---

## 47. [ID:877]

**问题**: For all the drivers who finished the game in race No. 872, who is the youngest?

**证据**: (无)

**生成SQL**:
```sql
SELECT d.driverId, d.forename, d.surname FROM drivers d INNER JOIN results r ON d.driverId = r.driverId WHERE r.raceId = 872 AND r.time IS NOT NULL ORDER BY d.dob DESC LIMIT 1
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

**生成结果**: [{'driverId': 815, 'forename': 'Sergio', 'surname': 'Pérez'}]

**预期结果**: [{'forename': 'Sergio', 'surname': 'Pérez'}]

---

## 48. [ID:892]

**问题**: State the driver with the most points scored. Find his full name with that points.

**证据**: (无)

**生成SQL**:
```sql
SELECT CONCAT(d.forename, ' ', d.surname) AS full_name, SUM(ds.points) AS total_points FROM drivers d JOIN driverStandings ds ON d.driverId = ds.driverId GROUP BY d.driverId, d.forename, d.surname ORDER BY total_points DESC LIMIT 1
```

**预期SQL**:
```sql
SELECT
  `T3`.`forename`,
  `T3`.`surname`,
  `T2`.`points`
FROM `races` AS `T1`
INNER JOIN `driverStandings` AS `T2`
  ON `T2`.`raceId` = `T1`.`raceId`
INNER JOIN `drivers` AS `T3`
  ON `T3`.`driverId` = `T2`.`driverId`
ORDER BY
  `T2`.`points` DESC
LIMIT 1
```

**生成结果**: [{'full_name': 'Lewis Hamilton', 'total_points': 24366.0}]

**预期结果**: [{'forename': 'Sebastian', 'surname': 'Vettel', 'points': 397.0}]

---

## 49. [ID:894]

**问题**: What is the best lap time recorded? List the driver and race with such recorded lap time.

**证据**: (无)

**生成SQL**:
```sql
SELECT d.forename, d.surname, r.name FROM lapTimes l JOIN drivers d ON l.driverId = d.driverId JOIN races r ON l.raceId = r.raceId WHERE l.milliseconds = (SELECT MIN(milliseconds) FROM lapTimes)
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

**生成结果**: [{'forename': 'Lewis', 'surname': 'Hamilton', 'name': 'Austrian Grand Prix'}]

**预期结果**: [{'milliseconds': 67411, 'forename': 'Lewis', 'surname': 'Hamilton', 'name': 'Austrian Grand Prix'}]

---

## 50. [ID:904]

**问题**: State the race and year of race in which Michael Schumacher had his fastest lap.

**证据**: (无)

**生成SQL**:
```sql
SELECT r.name, r.year FROM results res INNER JOIN races r ON res.raceId = r.raceId INNER JOIN drivers d ON res.driverId = d.driverId WHERE d.forename = 'Michael' AND d.surname = 'Schumacher' AND res.fastestLap = (SELECT MIN(fastestLap) FROM results res2 WHERE res2.driverId = d.driverId) ORDER BY r.year DESC LIMIT 1
```

**预期SQL**:
```sql
SELECT
  `T1`.`name`,
  `T1`.`year`
FROM `races` AS `T1`
INNER JOIN `lapTimes` AS `T2`
  ON `T2`.`raceId` = `T1`.`raceId`
INNER JOIN `drivers` AS `T3`
  ON `T3`.`driverId` = `T2`.`driverId`
WHERE
  `T3`.`forename` = 'Michael' AND `T3`.`surname` = 'Schumacher'
ORDER BY
  `T2`.`milliseconds` ASC
LIMIT 1
```

**生成结果**: [{'name': 'Spanish Grand Prix', 'year': 2012}]

**预期结果**: [{'name': 'Austrian Grand Prix', 'year': 2003}]

---

## 51. [ID:906]

**问题**: Which was Lewis Hamilton first race? What was his points recorded for his first race event?

**证据**: (无)

**生成SQL**:
```sql
SELECT r.name, r.year, r.date, rs.points FROM results rs INNER JOIN races r ON rs.raceId = r.raceId INNER JOIN drivers d ON rs.driverId = d.driverId WHERE d.forename = 'Lewis' AND d.surname = 'Hamilton' ORDER BY r.year ASC, r.round ASC LIMIT 1
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

**生成结果**: [{'name': 'Malaysian Grand Prix', 'year': 2007, 'date': '2007-04-08', 'points': 8.0}]

**预期结果**: [{'name': 'Malaysian Grand Prix', 'points': 14.0}]

---

## 52. [ID:928]

**问题**: Which driver ranked the first in the Canadian Grand Prix in 2007? Please give his reference name.

**证据**: (无)

**生成SQL**:
```sql
SELECT d.driverRef FROM results r JOIN races ra ON r.raceId = ra.raceId JOIN drivers d ON r.driverId = d.driverId WHERE ra.name = 'Canadian Grand Prix' AND ra.year = 2007 AND r.positionOrder = 1
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

**生成结果**: [{'driverRef': 'hamilton'}]

**预期结果**: [{'forename': 'Fernando', 'surname': 'Alonso', 'driverRef': 'alonso'}]

---

## 53. [ID:931]

**问题**: What was the fastest lap speed among all drivers in the 2009 Spanish Grand Prix?

**证据**: (无)

**生成SQL**:
```sql
SELECT MAX(CAST(fastestLapSpeed AS DOUBLE)) FROM results WHERE raceId = (SELECT raceId FROM races WHERE name = 'Spanish Grand Prix' AND year = 2009)
```

**预期SQL**:
```sql
SELECT
  `T2`.`fastestLapSpeed`
FROM `races` AS `T1`
INNER JOIN `results` AS `T2`
  ON `T2`.`raceId` = `T1`.`raceId`
WHERE
  `T1`.`name` = 'Spanish Grand Prix'
  AND `T1`.`year` = 2009
  AND NOT `T2`.`fastestLapSpeed` IS NULL
ORDER BY
  `T2`.`fastestLapSpeed` DESC
LIMIT 1
```

**生成结果**: [{'MAX(CAST(fastestLapSpeed AS DOUBLE))': 202.484}]

**预期结果**: [{'fastestLapSpeed': '202.484'}]

---

## 54. [ID:963]

**问题**: How many French drivers who obtain the laptime less than 02:00.00?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(DISTINCT d.driverId) FROM drivers d INNER JOIN lapTimes lt ON d.driverId = lt.driverId WHERE d.nationality = 'French' AND lt.milliseconds < 120000
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

**生成结果**: [{'COUNT(DISTINCT d.driverId)': 9}]

**预期结果**: [{'COUNT(`T1`.`driverId`)': 23295}]

---

## 55. [ID:972]

**问题**: Which drivers who were born in 1971 and has the fastest lap time on the race? Give id and code of these drivers.

**证据**: (无)

**生成SQL**:
```sql
SELECT DISTINCT d.driverId, d.code FROM drivers d INNER JOIN results r ON d.driverId = r.driverId WHERE YEAR(d.dob) = 1971 AND r.fastestLapTime IS NOT NULL
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

**生成结果**: [{'driverId': 14, 'code': 'COU'}, {'driverId': 35, 'code': 'VIL'}, {'driverId': 37, 'code': 'DLR'}] ... (+1行)

**预期结果**: [{'driverId': 14, 'code': 'COU'}, {'driverId': 14, 'code': 'COU'}, {'driverId': 14, 'code': 'COU'}] ... (+147行)

---

## 56. [ID:981]

**问题**: On what year did the youngest driver had his first qualifying race? Also state the name, date and time of the race.

**证据**: (无)

**生成SQL**:
```sql
SELECT d.forename, d.surname, MIN(r.date) AS first_qualifying_date, r.name AS race_name, r.time AS race_time FROM drivers d JOIN qualifying q ON d.driverId = q.driverId JOIN races r ON q.raceId = r.raceId WHERE d.dob = (SELECT MAX(dob) FROM drivers) GROUP BY d.driverId, d.forename, d.surname, r.name, r.time ORDER BY first_qualifying_date LIMIT 1
```

**预期SQL**:
```sql
SELECT
  `T3`.`year`,
  `T3`.`name`,
  `T3`.`date`,
  `T3`.`time`
FROM `qualifying` AS `T1`
INNER JOIN `drivers` AS `T2`
  ON `T1`.`driverId` = `T2`.`driverId`
INNER JOIN `races` AS `T3`
  ON `T1`.`raceId` = `T3`.`raceId`
WHERE
  `T1`.`driverId` = (
    SELECT
      `driverId`
    FROM `drivers`
    ORDER BY
      `dob` DESC
    LIMIT 1
  )
ORDER BY
  `T3`.`date` ASC
LIMIT 1
```

**生成结果**: [{'forename': 'Lance', 'surname': 'Stroll', 'first_qualifying_date': '2017-04-09', 'race_name': 'Chinese Grand Prix', 'race_time': '06:00:00'}]

**预期结果**: [{'year': 2017, 'name': 'Chinese Grand Prix', 'date': '2017-04-09', 'time': '06:00:00'}]

---

## 57. [ID:989]

**问题**: Who is the champion of the Canadian Grand Prix in 2008? Indicate his finish time.

**证据**: (无)

**生成SQL**:
```sql
SELECT d.forename, d.surname, r.time FROM results r JOIN races ra ON r.raceId = ra.raceId JOIN drivers d ON r.driverId = d.driverId WHERE ra.name = 'Canadian Grand Prix' AND ra.year = 2008 AND r.positionOrder = 1
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

**生成结果**: [{'forename': 'Robert', 'surname': 'Kubica', 'time': '1:36:24.227'}]

**预期结果**: [{'time': '1:36:24.227'}]

---

## 58. [ID:1002]

**问题**: As of the present, what is the full name of the youngest racer? Indicate her nationality and the name of the race to which he/she first joined.

**证据**: (无)

**生成SQL**:
```sql
SELECT CONCAT(d.forename, ' ', d.surname) AS full_name, d.nationality, r.name AS first_race_name FROM drivers d JOIN results res ON d.driverId = res.driverId JOIN races r ON res.raceId = r.raceId WHERE d.dob = (SELECT MAX(dob) FROM drivers) ORDER BY r.date ASC LIMIT 1
```

**预期SQL**:
```sql
SELECT `T1`.`forename`, `T1`.`surname`, `T1`.`nationality`, `T3`.`name` FROM `drivers` AS `T1` INNER JOIN `driverStandings` AS `T2` ON `T1`.`driverId` = `T2`.`driverId` INNER JOIN `races` AS `T3` ON `T2`.`raceId` = `T3`.`raceId` ORDER BY `T1`.`dob` DESC LIMIT 1
```

**生成结果**: [{'full_name': 'Lance Stroll', 'nationality': 'Canadian', 'first_race_name': 'Chinese Grand Prix'}]

**预期结果**: [{'forename': 'Lance', 'surname': 'Stroll', 'nationality': 'Canadian', 'name': 'Chinese Grand Prix'}]

---

## 59. [ID:726]

**问题**: Rank heroes published by Marvel Comics by their height in descending order.

**证据**: (无)

**生成SQL**:
```sql
SELECT s.superhero_name FROM superhero s INNER JOIN publisher p ON s.publisher_id = p.id WHERE p.publisher_name = 'Marvel Comics' ORDER BY s.height_cm DESC
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

**生成结果**: [{'superhero_name': 'Surtur'}, {'superhero_name': 'Ymir'}, {'superhero_name': 'Bloodwraith'}] ... (+384行)

**预期结果**: [{'superhero_name': 'Surtur', 'height_cm': 30480, 'HeightRank': 1}, {'superhero_name': 'Ymir', 'height_cm': 30480, 'HeightRank': 1}, {'superhero_name': 'Bloodwraith', 'height_cm': 3050, 'HeightRank': 3}] ... (+384行)

---

## 60. [ID:728]

**问题**: Rank superheroes from Marvel Comics by their eye color popularity, starting with the most common color.

**证据**: (无)

**生成SQL**:
```sql
SELECT c.colour FROM superhero s INNER JOIN publisher p ON s.publisher_id = p.id INNER JOIN colour c ON s.eye_colour_id = c.id WHERE p.publisher_name = 'Marvel Comics' GROUP BY c.colour ORDER BY COUNT(s.id) DESC
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

**生成结果**: [{'colour': 'Blue'}, {'colour': 'Brown'}, {'colour': 'No Colour'}] ... (+16行)

**预期结果**: [{'EyeColor': 'Blue', 'Count': 126, 'PopularityRank': 1}, {'EyeColor': 'Brown', 'Count': 89, 'PopularityRank': 2}, {'EyeColor': 'No Colour', 'Count': 47, 'PopularityRank': 3}] ... (+16行)

---

## 61. [ID:758]

**问题**: Provide the hair colour of the human superhero who is 185 cm tall.

**证据**: (无)

**生成SQL**:
```sql
SELECT c.colour FROM superhero s JOIN race r ON s.race_id = r.id JOIN colour c ON s.hair_colour_id = c.id WHERE s.height_cm = 185 AND r.race = 'human'
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

**生成结果**: [{'colour': 'Blond'}, {'colour': 'Brown'}, {'colour': 'Brown'}] ... (+8行)

**预期结果**: [{'colour': 'Blond'}, {'colour': 'Brown'}, {'colour': 'Black'}] ... (+2行)

---

## 62. [ID:794]

**问题**: Which hero was the fastest?

**证据**: (无)

**生成SQL**:
```sql
SELECT s.superhero_name FROM superhero s INNER JOIN hero_attribute ha ON s.id = ha.hero_id INNER JOIN attribute a ON ha.attribute_id = a.id WHERE a.attribute_name = 'Speed' ORDER BY ha.attribute_value DESC LIMIT 1
```

**预期SQL**:
```sql
SELECT `T1`.`superhero_name` FROM `superhero` AS `T1` INNER JOIN `hero_attribute` AS `T2` ON `T1`.`id` = `T2`.`hero_id` INNER JOIN `attribute` AS `T3` ON `T2`.`attribute_id` = `T3`.`id`WHERE `T3`.`attribute_name` = 'Speed' AND `T2`.`attribute_value` = (SELECT MAX(`attribute_value`) FROM `hero_attribute` AS `T2b` WHERE `T2b`.`attribute_id` = `T3`.`id` ) LIMIT 1
```

**生成结果**: [{'superhero_name': 'Zoom'}]

**预期结果**: [{'superhero_name': 'Air-Walker'}]

---

## 63. [ID:800]

**问题**: Calculate the percentage of superheroes with blue eyes.

**证据**: (无)

**生成SQL**:
```sql
SELECT (SUM(CASE WHEN c.colour = 'Blue' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS percentage FROM superhero s INNER JOIN colour c ON s.eye_colour_id = c.id WHERE c.colour = 'Blue'
```

**预期SQL**:
```sql
SELECT
  CAST(COUNT(CASE WHEN `T2`.`colour` = 'Blue' THEN 1 ELSE NULL END) AS DOUBLE) * 100 / COUNT(`T1`.`id`)
FROM `superhero` AS `T1`
INNER JOIN `colour` AS `T2`
  ON `T1`.`eye_colour_id` = `T2`.`id`
```

**生成结果**: [{'percentage': 100.0}]

**预期结果**: [{"CAST(COUNT(CASE WHEN `T2`.`colour` = 'Blue' THEN 1 ELSE NULL END) AS DOUBLE) * 100 / COUNT(`T1`.`id`)": 31.2}]

---

## 64. [ID:565]

**问题**: User No.23853 gave a comment to a post at 9:08:18 on 2013/7/12, was that post well-finished?

**证据**: (无)

**生成SQL**:
```sql
SELECT CASE WHEN p.ClosedDate IS NULL THEN 'well-finished' ELSE 'not well-finished' END AS finish_status FROM comments c INNER JOIN posts p ON c.PostId = p.Id WHERE c.UserId = 23853 AND c.CreationDate = '2013-07-12 09:08:18'
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

**生成结果**: [{'finish_status': 'not well-finished'}]

**预期结果**: [{'resylt': 'well-finished'}]

---

## 65. [ID:571]

**问题**: For the user No.24, how many times is the number of his/her posts compared to his/her votes?

**证据**: (无)

**生成SQL**:
```sql
SELECT CAST(COUNT(p.Id) AS DOUBLE) / CAST(COUNT(v.Id) AS DOUBLE) AS post_to_vote_ratio FROM posts p LEFT JOIN votes v ON p.OwnerUserId = v.UserId WHERE p.OwnerUserId = 24
```

**预期SQL**:
```sql
SELECT
  CAST(COUNT(DISTINCT `T2`.`Id`) AS DOUBLE) / COUNT(DISTINCT `T1`.`Id`)
FROM `votes` AS `T1`
INNER JOIN `posts` AS `T2`
  ON `T1`.`UserId` = `T2`.`OwnerUserId`
WHERE
  `T1`.`UserId` = 24
```

**生成结果**: [{'post_to_vote_ratio': 1.0}]

**预期结果**: [{'CAST(COUNT(DISTINCT `T2`.`Id`) AS DOUBLE) / COUNT(DISTINCT `T1`.`Id`)': 0.375}]

---

## 66. [ID:581]

**问题**: Who is the owner of the post titled 'Open source tools for visualizing multi-dimensional data?'

**证据**: (无)

**生成SQL**:
```sql
SELECT p.OwnerDisplayName FROM posts p WHERE p.Title = 'Open source tools for visualizing multi-dimensional data?'
```

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

**生成结果**: [{'OwnerDisplayName': None}]

**预期结果**: [{'DisplayName': 'Paul'}]

---

## 67. [ID:584]

**问题**: Write all the comments left by users who edited the post titled 'Why square the difference instead of taking the absolute value in standard deviation?'

**证据**: (无)

**生成SQL**:
```sql
SELECT c.* FROM comments c INNER JOIN posts p ON c.PostId = p.Id WHERE p.Title = 'Why square the difference instead of taking the absolute value in standard deviation?'
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

**生成结果**: [{'Id': 64, 'PostId': 118, 'Score': 11, 'Text': 'In a way, the measurement you proposed is widely used in case of error (model quality) analysis -- then it is called MAE, "mean absolute error".', 'CreationDate': '2010-07-19T21:30:23', 'UserId': 88, 'UserDisplayName': None}, {'Id': 128, 'PostId': 118, 'Score': 2, 'Text': "In accepting an answer it seems important to me that we pay attention to whether the answer is circular.  The normal distribution is based on these measurements of variance from squared error terms, but that isn't in and of itself a justification for using (X-M)^2 over |X-M|.", 'CreationDate': '2010-07-20T07:59:54', 'UserId': 196, 'UserDisplayName': None}, {'Id': 414, 'PostId': 118, 'Score': 1, 'Text': 'Do you think the term standard means this is THE standard today ? Isn\'t it like asking why principal component are "principal" and not secondary ?', 'CreationDate': '2010-07-23T21:44:37', 'UserId': 223, 'UserDisplayName': None}] ... (+8行)

**预期结果**: [{'Comment': ''}, {'Comment': ''}, {'Comment': ''}] ... (+5行)

---

## 68. [ID:587]

**问题**: Calculate the average view count of each post tagged as 'humor' and list the title and the comment of each post.

**证据**: (无)

**生成SQL**:
```sql
SELECT p.Title, c.Text, AVG(p.ViewCount) AS AverageViewCount FROM posts p INNER JOIN comments c ON p.Id = c.PostId WHERE p.Tags LIKE '%<humor>%' GROUP BY p.Id, p.Title, c.Text
```

**预期SQL**:
```sql
SELECT AVG(T2.ViewCount) AS average_view_count, T2.Title, T1.Text FROM comments AS T1 INNER JOIN posts AS T2 ON T2.Id = T1.PostId WHERE T2.Tags = '<humor>' GROUP BY T2.Title, T1.Text
```

**生成结果**: [{'Title': 'So how many staticians *does* it take to screw in a lightbulb?', 'Text': 'Probably better asked on meta.  People feel like they have to downvote it because it is an off-topic question.  But then the downvotes make it look like staticians have no sense of humor :(', 'AverageViewCount': 288.0}, {'Title': 'So how many staticians *does* it take to screw in a lightbulb?', 'Text': '@Jason Punyon in particular gets a humorless downvote for removing my "verboten" tag! ;-)', 'AverageViewCount': 288.0}, {'Title': 'What is your favorite "data analysis" cartoon?', 'Text': 'I do have to ask though- how come cartoons are in and jokes are out?', 'AverageViewCount': 64481.0}] ... (+16行)

**预期结果**: [{'average_view_count': 288.0, 'Title': 'So how many staticians *does* it take to screw in a lightbulb?', 'Text': 'Probably better asked on meta.  People feel like they have to downvote it because it is an off-topic question.  But then the downvotes make it look like staticians have no sense of humor :('}, {'average_view_count': 288.0, 'Title': 'So how many staticians *does* it take to screw in a lightbulb?', 'Text': '@Jason Punyon in particular gets a humorless downvote for removing my "verboten" tag! ;-)'}, {'average_view_count': 64481.0, 'Title': 'What is your favorite "data analysis" cartoon?', 'Text': 'I do have to ask though- how come cartoons are in and jokes are out?'}] ... (+6行)

---

## 69. [ID:595]

**问题**: Which user have only one post history per post and having at least 1000 views?

**证据**: (无)

**生成SQL**:
```sql
SELECT DISTINCT T1.UserId FROM postHistory T1 INNER JOIN posts T2 ON T1.PostId = T2.Id WHERE T2.ViewCount >= 1000 GROUP BY T1.UserId, T1.PostId HAVING COUNT(T1.Id) = 1
```

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

**生成结果**: [{'UserId': None}, {'UserId': -1}, {'UserId': 5}] ... (+268行)

**预期结果**: [{'UserId': 57}, {'UserId': 61}, {'UserId': 80}] ... (+91行)

---

## 70. [ID:604]

**问题**: What is the average of the up votes and the average user age for users creating more than 10 posts?

**证据**: (无)

**生成SQL**:
```sql
SELECT AVG(u.UpVotes) AS avg_up_votes, AVG(u.Age) AS avg_user_age FROM users u WHERE u.Id IN (SELECT OwnerUserId FROM posts GROUP BY OwnerUserId HAVING COUNT(*) > 10)
```

**预期SQL**:
```sql
SELECT
  AVG(`T1`.`UpVotes`),
  AVG(`T1`.`Age`)
FROM `users` AS `T1`
INNER JOIN (
  SELECT
    `OwnerUserId`,
    COUNT(*) AS `post_count`
  FROM `posts`
  GROUP BY
    `OwnerUserId`
  HAVING
    `post_count` > 10
) AS `T2`
  ON `T1`.`Id` = `T2`.`OwnerUserId`
```

**生成结果**: []

**预期结果**: [{'AVG(`T1`.`UpVotes`)': 182.2833, 'AVG(`T1`.`Age`)': 34.0833}]

---

## 71. [ID:633]

**问题**: Which post by slashnick has the most answers count? State the post ID.

**证据**: (无)

**生成SQL**:
```sql
SELECT Id FROM posts WHERE OwnerDisplayName = 'slashnick' ORDER BY AnswerCount DESC LIMIT 1
```

**预期SQL**:
```sql
SELECT
  `T2`.`PostId`
FROM `users` AS `T1`
INNER JOIN `postHistory` AS `T2`
  ON `T1`.`Id` = `T2`.`UserId`
INNER JOIN `posts` AS `T3`
  ON `T2`.`PostId` = `T3`.`Id`
WHERE
  `T1`.`DisplayName` = 'slashnick'
ORDER BY
  `T3`.`AnswerCount` DESC
LIMIT 1
```

**生成结果**: []

**预期结果**: [{'PostId': 351}]

---

## 72. [ID:637]

**问题**: State all the tags used by Mark Meckes in his posts that doesn't have comments.

**证据**: (无)

**生成SQL**:
```sql
SELECT DISTINCT T1.Tags FROM posts T1 INNER JOIN users T2 ON T1.OwnerUserId = T2.Id WHERE T2.DisplayName = 'Mark Meckes' AND T1.CommentCount = 0 AND T1.Tags IS NOT NULL
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

**生成结果**: [{'Tags': '<books>'}]

**预期结果**: [{'Tags': '<books>'}, {'Tags': '<books>'}, {'Tags': '<books>'}] ... (+2行)

---

## 73. [ID:640]

**问题**: Calculate the difference in view count from post posted by Mornington and view count from posts posted by Amos.

**证据**: (无)

**生成SQL**:
```sql
SELECT (SELECT SUM(ViewCount) FROM posts WHERE OwnerDisplayName = 'Mornington') - (SELECT SUM(ViewCount) FROM posts WHERE OwnerDisplayName = 'Amos') AS view_count_difference
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

**生成结果**: [{'view_count_difference': None}]

**预期结果**: [{'diff': -1491.0}]

---

## 74. [ID:665]

**问题**: What is the average monthly number of links created in 2010 for posts that have no more than 2 answers?

**证据**: (无)

**生成SQL**:
```sql
SELECT AVG(monthly_count) AS average_monthly_links FROM (SELECT MONTH(CreationDate) AS month, COUNT(Id) AS monthly_count FROM postLinks WHERE YEAR(CreationDate) = 2010 AND PostId IN (SELECT Id FROM posts WHERE AnswerCount <= 2) GROUP BY MONTH(CreationDate)) AS monthly_counts
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

**生成结果**: [{'average_monthly_links': 17.3333}]

**预期结果**: [{'CAST(COUNT(`T1`.`Id`) AS DOUBLE) / 12': 8.666666666666666}]

---

## 75. [ID:672]

**问题**: Among the users located in United Kingdom, how many users whose post have a total favorite amount of 4 or more?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(DISTINCT u.Id) FROM users u INNER JOIN posts p ON u.Id = p.OwnerUserId WHERE u.Location = 'United Kingdom' AND p.FavoriteCount >= 4
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

**生成结果**: [{'COUNT(DISTINCT u.Id)': 14}]

**预期结果**: [{'COUNT(`T1`.`Id`)': 19}]

---

## 76. [ID:682]

**问题**: Which is the most valuable post in 2010? Please give its id and the owner's display name.

**证据**: (无)

**生成SQL**:
```sql
SELECT p.Id, p.OwnerDisplayName FROM posts p WHERE YEAR(p.CreaionDate) = 2010 ORDER BY p.FavoriteCount DESC LIMIT 1
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

**生成结果**: [{'Id': 1595, 'OwnerDisplayName': None}]

**预期结果**: [{'OwnerUserId': 890, 'DisplayName': 'Fabian Fagerholm'}]

---

## 77. [ID:683]

**问题**: What is the percentage of posts whose owners had a reputation of over 1000 in 2011?

**证据**: (无)

**生成SQL**:
```sql
SELECT (COUNT(CASE WHEN u.Reputation > 1000 THEN p.Id END) * 100.0 / COUNT(p.Id)) AS percentage FROM posts p INNER JOIN users u ON p.OwnerUserId = u.Id WHERE YEAR(p.CreaionDate) = 2011
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

**生成结果**: [{'percentage': 51.16624}]

**预期结果**: [{"CAST(SUM(\n    CASE\n      WHEN DATE_FORMAT(CAST(`T2`.`CreaionDate` AS DATETIME), '%Y') = '2011'\n      AND `T1`.`Reputation` > 1000\n      THEN 1\n      ELSE 0\n    END\n  ) AS DOUBLE) * 100 / COUNT(`T1`.`Id`)": 7.241992293168744}]

---

## 78. [ID:685]

**问题**: Identify the total views on the post 'Computer Game Datasets'. Name the user who posted it last time.

**证据**: (无)

**生成SQL**:
```sql
SELECT p.ViewCount, u.DisplayName FROM posts p INNER JOIN users u ON p.OwnerUserId = u.Id WHERE p.Title = 'Computer Game Datasets' ORDER BY p.CreaionDate DESC LIMIT 1
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

**生成结果**: [{'ViewCount': 1708, 'DisplayName': 'Menno'}]

**预期结果**: [{'ViewCount': 1708, 'DisplayName': 'mbq'}, {'ViewCount': 1708, 'DisplayName': 'mbq'}]

---

## 79. [ID:694]

**问题**: Provide the text of the latest 10 comments to the post with the title 'Analysing wind data with R' and the display name of the user who left it.

**证据**: (无)

**生成SQL**:
```sql
SELECT c.Text, c.UserDisplayName FROM comments c INNER JOIN posts p ON c.PostId = p.Id WHERE p.Title = 'Analysing wind data with R' ORDER BY c.CreationDate DESC LIMIT 10
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

**生成结果**: [{'Text': 'i thought of integrating seperetly until 4 m/s, between 4 and 15m/s and over 15m/s, and comparing it to a situation of 100% of the time a turbine working in optimal speed', 'UserDisplayName': None}, {'Text': 'well untill 4 m/s there is no wind generation and the max is 15 m/s, wind stronger than 15 m/s will make the same amount of energy', 'UserDisplayName': None}, {'Text': "Regarding your question about energy, it's going to be difficult to answer. Do you know anything about your device? Do you know anything of the relationship between wind speed/direction and power? Do you know anything about the layout of the turbines at this particular site since that has a huge impact on the power as you no doubt are aware.", 'UserDisplayName': None}] ... (+7行)

**预期结果**: [{'Text': "About the picture, post to some image hosting and put a link -- I'll convert it into a pasted-in picture.", 'DisplayName': 'eliavs'}, {'Text': '+1, interesting question, you might find that soon you will have enough reputation :)', 'DisplayName': 'eliavs'}, {'Text': 'yup i have thanks to all that helped me!!', 'DisplayName': 'eliavs'}] ... (+7行)

---

## 80. [ID:716]

**问题**: Among the comments with scores between 5 to 10, what is the percentage of the users with 0 up votes?

**证据**: (无)

**生成SQL**:
```sql
SELECT (COUNT(DISTINCT c.UserId) * 100.0) / (SELECT COUNT(DISTINCT c2.UserId) FROM comments c2 WHERE c2.Score BETWEEN 5 AND 10) AS percentage FROM comments c INNER JOIN users u ON c.UserId = u.Id WHERE c.Score BETWEEN 5 AND 10 AND u.UpVotes = 0
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

**生成结果**: [{'percentage': 4.87013}]

**预期结果**: [{'per': 1.3264554163596167}]

---

## 81. [ID:344]

**问题**: List all the mythic rarity print cards banned in gladiator format.

**证据**: (无)

**生成SQL**:
```sql
SELECT c.name, c.setCode, c.rarity FROM cards c INNER JOIN legalities l ON c.uuid = l.uuid WHERE l.format = 'gladiator' AND l.status = 'Banned' AND c.rarity = 'mythic'
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

**生成结果**: [{'name': 'Oko, Thief of Crowns', 'setCode': 'ELD', 'rarity': 'mythic'}, {'name': 'Oko, Thief of Crowns', 'setCode': 'ELD', 'rarity': 'mythic'}, {'name': 'Nexus of Fate', 'setCode': 'M19', 'rarity': 'mythic'}] ... (+2行)

**预期结果**: [{'id': 17983}, {'id': 18058}, {'id': 29523}] ... (+2行)

---

## 82. [ID:345]

**问题**: For artifact type of cards that do not have multiple faces on the same card, state its legalities status for vintage play format.

**证据**: (无)

**生成SQL**:
```sql
SELECT l.status FROM cards c INNER JOIN legalities l ON c.uuid = l.uuid WHERE c.types LIKE '%Artifact%' AND c.side IS NULL AND l.format = 'vintage'
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

**生成结果**: [{'status': 'Legal'}, {'status': 'Legal'}, {'status': 'Legal'}] ... (+997行)

**预期结果**: [{'status': 'Legal'}, {'status': 'Restricted'}, {'status': 'Banned'}]

---

## 83. [ID:347]

**问题**: Find all cards illustrated by Stephen Daniel and describe the text of the ruling of these cards. State if these cards have missing or degraded properties and values.

**证据**: (无)

**生成SQL**:
```sql
SELECT c.id, c.name, c.text, r.text AS ruling_text, c.hasContentWarning FROM cards c LEFT JOIN rulings r ON c.uuid = r.uuid WHERE c.artist = 'Stephen Daniele' AND c.hasContentWarning = 1
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

**生成结果**: []

**预期结果**: [{'id': 29, 'text': 'You can’t put an Aura card from your hand onto the battlefield this way if that Aura can’t legally enchant Academy Researchers. For example, you can’t put an Aura with “enchant land” or “enchant green creature” onto the battlefield attached to Academy Res', 'hasContentWarning': 0}, {'id': 3872, 'text': 'This card now has Enchant Swamp, which works exactly like any other Enchant ability. This means it can only be cast targeting a Swamp, and it will be put into its owner’s graveyard if the permanent it’s attached to ever stops being a Swamp.', 'hasContentWarning': 0}, {'id': 6651, 'text': 'Cycling is an activated ability. Effects that interact with activated abilities (such as Stifle or Rings of Brighthearth) will interact with cycling. Effects that interact with spells (such as Remove Soul or Faerie Tauntings) will not.', 'hasContentWarning': 0}] ... (+20行)

---

## 84. [ID:349]

**问题**: Name the card and artist with the most ruling information. Also state if the card is a promotional printing.

**证据**: (无)

**生成SQL**:
```sql
SELECT c.name, c.artist, c.isPromo FROM cards c INNER JOIN (SELECT uuid, COUNT(*) as ruling_count FROM rulings GROUP BY uuid ORDER BY ruling_count DESC LIMIT 1) r ON c.uuid = r.uuid
```

**预期SQL**:
```sql
SELECT `T1`.`name`, `T1`.`artist`, `T1`.`isPromo` FROM `cards` AS `T1` INNER JOIN `rulings` AS `T2` ON `T1`.`uuid` = `T2`.`uuid` WHERE `T1`.`isPromo` = 1 AND `T1`.`artist` = ( SELECT `artist` FROM `cards` WHERE `isPromo` = 1 GROUP BY `artist` HAVING COUNT(DISTINCT `uuid`) = (SELECT MAX(card_counts.max_count) FROM (SELECT COUNT(DISTINCT `uuid`) AS max_count FROM `cards` WHERE `isPromo` = 1 GROUP BY `artist`) AS card_counts))LIMIT 1
```

**生成结果**: [{'name': "Teferi's Protection", 'artist': 'Chase Stone', 'isPromo': 0}]

**预期结果**: [{'name': 'Serrated Arrows', 'artist': 'John Avon', 'isPromo': 1}]

---

## 85. [ID:391]

**问题**: Among the Artifact cards, which are black color and comes with foreign languague translation?

**证据**: (无)

**生成SQL**:
```sql
SELECT c.name, c.asciiName, c.setCode, c.rarity, c.manaCost, c.convertedManaCost, c.text, c.type, c.originalType, c.colors, c.colorIdentity, c.keywords, c.power, c.toughness, c.loyalty, c.flavorText, c.flavorName, c.artist, c.number, c.printings, c.promoTypes, c.purchaseUrls, c.scryfallId, c.scryfallIllustrationId, c.scryfallOracleId, c.variations, c.watermark, c.layout, c.hand, c.life, c.leadershipSkills, c.hasAlternativeDeckLimit, c.hasContentWarning, c.hasFoil, c.hasNonFoil, c.isAlternative, c.isFullArt, c.isOnlineOnly, c.isOversized, c.isPromo, c.isReprint, c.isReserved, c.isStarter, c.isStorySpotlight, c.isTextless, c.isTimeshifted, c.duelDeck, c.edhrecRank, c.faceConvertedManaCost, c.faceName, c.frameEffects, c.frameVersion, c.isReprint, c.mcmId, c.mcmMetaId, c.mtgArenaId, c.mtgjsonV4Id, c.mtgoFoilId, c.mtgoId, c.multiverseId, c.originalReleaseDate, c.originalText, c.originalType, c.otherFaceIds, c.side, c.subtypes, c.supertypes, c.tcgplayerProductId, c.uuid, c.artist, c.asciiName, c.availability, c.borderColor, c.cardKingdomFoilId, c.cardKingdomId, c.colorIdentity, c.colorIndicator, c.colors, c.convertedManaCost, c.duelDeck, c.edhrecRank, c.faceConvertedManaCost, c.faceName, c.flavorName, c.flavorText, c.frameEffects, c.frameVersion, c.hand, c.hasAlternativeDeckLimit, c.hasContentWarning, c.hasFoil, c.hasNonFoil, c.isAlternative, c.isFullArt, c.isOnlineOnly, c.isOversized, c.isPromo, c.isReprint, c.isReserved, c.isStarter, c.isStorySpotlight, c.isTextless, c.isTimeshifted, c.keywords, c.layout, c.leadershipSkills, c.life, c.loyalty, c.manaCost, c.mcmId, c.mcmMetaId, c.mtgArenaId, c.mtgjsonV4Id, c.mtgoFoilId, c.mtgoId, c.multiverseId, c.name, c.number, c.originalReleaseDate, c.originalText, c.originalType, c.otherFaceIds, c.power, c.printings, c.promoTypes, c.purchaseUrls, c.rarity, c.scryfallId, c.scryfallIllustrationId, c.scryfallOracleId, c.setCode, c.side, c.subtypes, c.supertypes, c.tcgplayerProductId, c.text, c.toughness, c.type, c.types, c.uuid, c.variations, c.watermark, f.name AS foreign_name, f.text AS foreign_text, f.type AS foreign_type, f.flavorText AS foreign_flavorText, f.language, f.multiverseid FROM cards c INNER JOIN foreign_data f ON c.uuid = f.uuid WHERE c.originalType = 'Artifact' AND c.colors = 'B' AND f.language IS NOT NULL
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

**生成结果**: [{'name': "Executioner's Capsule", 'asciiName': None, 'setCode': '2XM', 'rarity': 'common', 'manaCost': '{B}', 'convertedManaCost': 1.0, 'text': "{1}{B}, {T}, Sacrifice Executioner's Capsule: Destroy target nonblack creature.", 'type': 'Artifact', 'originalType': 'Artifact', 'colors': 'B', 'colorIdentity': 'B', 'keywords': None, 'power': None, 'toughness': None, 'loyalty': None, 'flavorText': 'There is always a moment of trepidation before opening a message capsule, for fear of the judgment that might be contained within.', 'flavorName': None, 'artist': 'Warren Mahy', 'number': '92', 'printings': '2XM,ALA,C16,MB1,MMA', 'promoTypes': None, 'purchaseUrls': "{'cardKingdom': 'https://mtgjson.com/links/f3de9034ad549e4d', 'cardKingdomFoil': 'https://mtgjson.com/links/3ed0ff791d97efff', 'cardmarket': 'https://mtgjson.com/links/53d76c48986a6528', 'tcgplayer': 'https://mtgjson.com/links/34b15dadf8e5b88f'}", 'scryfallId': '032ea333-96e1-4ad8-8947-21d6bc3a9f91', 'scryfallIllustrationId': '63406ef2-21e0-4113-94cf-69bbe55047cb', 'scryfallOracleId': 'c9cd266c-7ecf-4beb-b9da-69b88f33abd3', 'variations': None, 'watermark': None, 'layout': 'normal', 'hand': None, 'life': None, 'leadershipSkills': None, 'hasAlternativeDeckLimit': 0, 'hasContentWarning': 0, 'hasFoil': 1, 'hasNonFoil': 1, 'isAlternative': 0, 'isFullArt': 0, 'isOnlineOnly': 0, 'isOversized': 0, 'isPromo': 0, 'isReprint': 1, 'isReserved': 0, 'isStarter': 0, 'isStorySpotlight': 0, 'isTextless': 0, 'isTimeshifted': 0, 'duelDeck': None, 'edhrecRank': 2492, 'faceConvertedManaCost': None, 'faceName': None, 'frameEffects': None, 'frameVersion': '2015', 'c.isReprint': 1, 'mcmId': '486434', 'mcmMetaId': '10047', 'mtgArenaId': None, 'mtgjsonV4Id': 'f68f4a6f-d1c6-5b92-a5a4-dc7762d079ae', 'mtgoFoilId': None, 'mtgoId': '82218', 'multiverseId': '489765', 'originalReleaseDate': None, 'originalText': "{1}{B}, {T}, Sacrifice Executioner's Capsule: Destroy target nonblack creature.", 'c.originalType': 'Artifact', 'otherFaceIds': None, 'side': None, 'subtypes': None, 'supertypes': None, 'tcgplayerProductId': '219528', 'uuid': 'be690a68-9c47-5750-ba05-0ce332bf962a', 'c.artist': 'Warren Mahy', 'c.asciiName': None, 'availability': 'mtgo,paper', 'borderColor': 'black', 'cardKingdomFoilId': '236738', 'cardKingdomId': '236325', 'c.colorIdentity': 'B', 'colorIndicator': None, 'c.colors': 'B', 'c.convertedManaCost': 1.0, 'c.duelDeck': None, 'c.edhrecRank': 2492, 'c.faceConvertedManaCost': None, 'c.faceName': None, 'c.flavorName': None, 'c.flavorText': 'There is always a moment of trepidation before opening a message capsule, for fear of the judgment that might be contained within.', 'c.frameEffects': None, 'c.frameVersion': '2015', 'c.hand': None, 'c.hasAlternativeDeckLimit': 0, 'c.hasContentWarning': 0, 'c.hasFoil': 1, 'c.hasNonFoil': 1, 'c.isAlternative': 0, 'c.isFullArt': 0, 'c.isOnlineOnly': 0, 'c.isOversized': 0, 'c.isPromo': 0, 'c.isReserved': 0, 'c.isStarter': 0, 'c.isStorySpotlight': 0, 'c.isTextless': 0, 'c.isTimeshifted': 0, 'c.keywords': None, 'c.layout': 'normal', 'c.leadershipSkills': None, 'c.life': None, 'c.loyalty': None, 'c.manaCost': '{B}', 'c.mcmId': '486434', 'c.mcmMetaId': '10047', 'c.mtgArenaId': None, 'c.mtgjsonV4Id': 'f68f4a6f-d1c6-5b92-a5a4-dc7762d079ae', 'c.mtgoFoilId': None, 'c.mtgoId': '82218', 'c.multiverseId': '489765', 'c.name': "Executioner's Capsule", 'c.number': '92', 'c.originalReleaseDate': None, 'c.originalText': "{1}{B}, {T}, Sacrifice Executioner's Capsule: Destroy target nonblack creature.", 'c.otherFaceIds': None, 'c.power': None, 'c.printings': '2XM,ALA,C16,MB1,MMA', 'c.promoTypes': None, 'c.purchaseUrls': "{'cardKingdom': 'https://mtgjson.com/links/f3de9034ad549e4d', 'cardKingdomFoil': 'https://mtgjson.com/links/3ed0ff791d97efff', 'cardmarket': 'https://mtgjson.com/links/53d76c48986a6528', 'tcgplayer': 'https://mtgjson.com/links/34b15dadf8e5b88f'}", 'c.rarity': 'common', 'c.scryfallId': '032ea333-96e1-4ad8-8947-21d6bc3a9f91', 'c.scryfallIllustrationId': '63406ef2-21e0-4113-94cf-69bbe55047cb', 'c.scryfallOracleId': 'c9cd266c-7ecf-4beb-b9da-69b88f33abd3', 'c.setCode': '2XM', 'c.side': None, 'c.subtypes': None, 'c.supertypes': None, 'c.tcgplayerProductId': '219528', 'c.text': "{1}{B}, {T}, Sacrifice Executioner's Capsule: Destroy target nonblack creature.", 'c.toughness': None, 'c.type': 'Artifact', 'types': 'Artifact', 'c.uuid': 'be690a68-9c47-5750-ba05-0ce332bf962a', 'c.variations': None, 'c.watermark': None, 'foreign_name': 'Kapsel des Henkers', 'foreign_text': '{1}{B}, {T}, opfere die Kapsel des Henkers: Zerstöre eine nichtschwarze Kreatur deiner Wahl.', 'foreign_type': 'Artefakt', 'foreign_flavorText': 'Es gibt immer einen kleinen Moment der Beklemmung, bevor die Kapsel mit der Nachricht geöffnet wird, da niemand das Urteil vorher kennt.', 'language': 'German', 'multiverseid': 490097}, {'name': "Executioner's Capsule", 'asciiName': None, 'setCode': '2XM', 'rarity': 'common', 'manaCost': '{B}', 'convertedManaCost': 1.0, 'text': "{1}{B}, {T}, Sacrifice Executioner's Capsule: Destroy target nonblack creature.", 'type': 'Artifact', 'originalType': 'Artifact', 'colors': 'B', 'colorIdentity': 'B', 'keywords': None, 'power': None, 'toughness': None, 'loyalty': None, 'flavorText': 'There is always a moment of trepidation before opening a message capsule, for fear of the judgment that might be contained within.', 'flavorName': None, 'artist': 'Warren Mahy', 'number': '92', 'printings': '2XM,ALA,C16,MB1,MMA', 'promoTypes': None, 'purchaseUrls': "{'cardKingdom': 'https://mtgjson.com/links/f3de9034ad549e4d', 'cardKingdomFoil': 'https://mtgjson.com/links/3ed0ff791d97efff', 'cardmarket': 'https://mtgjson.com/links/53d76c48986a6528', 'tcgplayer': 'https://mtgjson.com/links/34b15dadf8e5b88f'}", 'scryfallId': '032ea333-96e1-4ad8-8947-21d6bc3a9f91', 'scryfallIllustrationId': '63406ef2-21e0-4113-94cf-69bbe55047cb', 'scryfallOracleId': 'c9cd266c-7ecf-4beb-b9da-69b88f33abd3', 'variations': None, 'watermark': None, 'layout': 'normal', 'hand': None, 'life': None, 'leadershipSkills': None, 'hasAlternativeDeckLimit': 0, 'hasContentWarning': 0, 'hasFoil': 1, 'hasNonFoil': 1, 'isAlternative': 0, 'isFullArt': 0, 'isOnlineOnly': 0, 'isOversized': 0, 'isPromo': 0, 'isReprint': 1, 'isReserved': 0, 'isStarter': 0, 'isStorySpotlight': 0, 'isTextless': 0, 'isTimeshifted': 0, 'duelDeck': None, 'edhrecRank': 2492, 'faceConvertedManaCost': None, 'faceName': None, 'frameEffects': None, 'frameVersion': '2015', 'c.isReprint': 1, 'mcmId': '486434', 'mcmMetaId': '10047', 'mtgArenaId': None, 'mtgjsonV4Id': 'f68f4a6f-d1c6-5b92-a5a4-dc7762d079ae', 'mtgoFoilId': None, 'mtgoId': '82218', 'multiverseId': '489765', 'originalReleaseDate': None, 'originalText': "{1}{B}, {T}, Sacrifice Executioner's Capsule: Destroy target nonblack creature.", 'c.originalType': 'Artifact', 'otherFaceIds': None, 'side': None, 'subtypes': None, 'supertypes': None, 'tcgplayerProductId': '219528', 'uuid': 'be690a68-9c47-5750-ba05-0ce332bf962a', 'c.artist': 'Warren Mahy', 'c.asciiName': None, 'availability': 'mtgo,paper', 'borderColor': 'black', 'cardKingdomFoilId': '236738', 'cardKingdomId': '236325', 'c.colorIdentity': 'B', 'colorIndicator': None, 'c.colors': 'B', 'c.convertedManaCost': 1.0, 'c.duelDeck': None, 'c.edhrecRank': 2492, 'c.faceConvertedManaCost': None, 'c.faceName': None, 'c.flavorName': None, 'c.flavorText': 'There is always a moment of trepidation before opening a message capsule, for fear of the judgment that might be contained within.', 'c.frameEffects': None, 'c.frameVersion': '2015', 'c.hand': None, 'c.hasAlternativeDeckLimit': 0, 'c.hasContentWarning': 0, 'c.hasFoil': 1, 'c.hasNonFoil': 1, 'c.isAlternative': 0, 'c.isFullArt': 0, 'c.isOnlineOnly': 0, 'c.isOversized': 0, 'c.isPromo': 0, 'c.isReserved': 0, 'c.isStarter': 0, 'c.isStorySpotlight': 0, 'c.isTextless': 0, 'c.isTimeshifted': 0, 'c.keywords': None, 'c.layout': 'normal', 'c.leadershipSkills': None, 'c.life': None, 'c.loyalty': None, 'c.manaCost': '{B}', 'c.mcmId': '486434', 'c.mcmMetaId': '10047', 'c.mtgArenaId': None, 'c.mtgjsonV4Id': 'f68f4a6f-d1c6-5b92-a5a4-dc7762d079ae', 'c.mtgoFoilId': None, 'c.mtgoId': '82218', 'c.multiverseId': '489765', 'c.name': "Executioner's Capsule", 'c.number': '92', 'c.originalReleaseDate': None, 'c.originalText': "{1}{B}, {T}, Sacrifice Executioner's Capsule: Destroy target nonblack creature.", 'c.otherFaceIds': None, 'c.power': None, 'c.printings': '2XM,ALA,C16,MB1,MMA', 'c.promoTypes': None, 'c.purchaseUrls': "{'cardKingdom': 'https://mtgjson.com/links/f3de9034ad549e4d', 'cardKingdomFoil': 'https://mtgjson.com/links/3ed0ff791d97efff', 'cardmarket': 'https://mtgjson.com/links/53d76c48986a6528', 'tcgplayer': 'https://mtgjson.com/links/34b15dadf8e5b88f'}", 'c.rarity': 'common', 'c.scryfallId': '032ea333-96e1-4ad8-8947-21d6bc3a9f91', 'c.scryfallIllustrationId': '63406ef2-21e0-4113-94cf-69bbe55047cb', 'c.scryfallOracleId': 'c9cd266c-7ecf-4beb-b9da-69b88f33abd3', 'c.setCode': '2XM', 'c.side': None, 'c.subtypes': None, 'c.supertypes': None, 'c.tcgplayerProductId': '219528', 'c.text': "{1}{B}, {T}, Sacrifice Executioner's Capsule: Destroy target nonblack creature.", 'c.toughness': None, 'c.type': 'Artifact', 'types': 'Artifact', 'c.uuid': 'be690a68-9c47-5750-ba05-0ce332bf962a', 'c.variations': None, 'c.watermark': None, 'foreign_name': "Capsule de l'exécuteur", 'foreign_text': "{1}{B}, {T}, sacrifiez la Capsule de l'exécuteur : Détruisez la créature non-noire ciblée.", 'foreign_type': 'Artefact', 'foreign_flavorText': "L'ouverture d'une capsule est toujours précédée d'un instant de trépidation, de crainte du jugement qu'elle pourrait contenir.", 'language': 'French', 'multiverseid': 490429}, {'name': "Executioner's Capsule", 'asciiName': None, 'setCode': '2XM', 'rarity': 'common', 'manaCost': '{B}', 'convertedManaCost': 1.0, 'text': "{1}{B}, {T}, Sacrifice Executioner's Capsule: Destroy target nonblack creature.", 'type': 'Artifact', 'originalType': 'Artifact', 'colors': 'B', 'colorIdentity': 'B', 'keywords': None, 'power': None, 'toughness': None, 'loyalty': None, 'flavorText': 'There is always a moment of trepidation before opening a message capsule, for fear of the judgment that might be contained within.', 'flavorName': None, 'artist': 'Warren Mahy', 'number': '92', 'printings': '2XM,ALA,C16,MB1,MMA', 'promoTypes': None, 'purchaseUrls': "{'cardKingdom': 'https://mtgjson.com/links/f3de9034ad549e4d', 'cardKingdomFoil': 'https://mtgjson.com/links/3ed0ff791d97efff', 'cardmarket': 'https://mtgjson.com/links/53d76c48986a6528', 'tcgplayer': 'https://mtgjson.com/links/34b15dadf8e5b88f'}", 'scryfallId': '032ea333-96e1-4ad8-8947-21d6bc3a9f91', 'scryfallIllustrationId': '63406ef2-21e0-4113-94cf-69bbe55047cb', 'scryfallOracleId': 'c9cd266c-7ecf-4beb-b9da-69b88f33abd3', 'variations': None, 'watermark': None, 'layout': 'normal', 'hand': None, 'life': None, 'leadershipSkills': None, 'hasAlternativeDeckLimit': 0, 'hasContentWarning': 0, 'hasFoil': 1, 'hasNonFoil': 1, 'isAlternative': 0, 'isFullArt': 0, 'isOnlineOnly': 0, 'isOversized': 0, 'isPromo': 0, 'isReprint': 1, 'isReserved': 0, 'isStarter': 0, 'isStorySpotlight': 0, 'isTextless': 0, 'isTimeshifted': 0, 'duelDeck': None, 'edhrecRank': 2492, 'faceConvertedManaCost': None, 'faceName': None, 'frameEffects': None, 'frameVersion': '2015', 'c.isReprint': 1, 'mcmId': '486434', 'mcmMetaId': '10047', 'mtgArenaId': None, 'mtgjsonV4Id': 'f68f4a6f-d1c6-5b92-a5a4-dc7762d079ae', 'mtgoFoilId': None, 'mtgoId': '82218', 'multiverseId': '489765', 'originalReleaseDate': None, 'originalText': "{1}{B}, {T}, Sacrifice Executioner's Capsule: Destroy target nonblack creature.", 'c.originalType': 'Artifact', 'otherFaceIds': None, 'side': None, 'subtypes': None, 'supertypes': None, 'tcgplayerProductId': '219528', 'uuid': 'be690a68-9c47-5750-ba05-0ce332bf962a', 'c.artist': 'Warren Mahy', 'c.asciiName': None, 'availability': 'mtgo,paper', 'borderColor': 'black', 'cardKingdomFoilId': '236738', 'cardKingdomId': '236325', 'c.colorIdentity': 'B', 'colorIndicator': None, 'c.colors': 'B', 'c.convertedManaCost': 1.0, 'c.duelDeck': None, 'c.edhrecRank': 2492, 'c.faceConvertedManaCost': None, 'c.faceName': None, 'c.flavorName': None, 'c.flavorText': 'There is always a moment of trepidation before opening a message capsule, for fear of the judgment that might be contained within.', 'c.frameEffects': None, 'c.frameVersion': '2015', 'c.hand': None, 'c.hasAlternativeDeckLimit': 0, 'c.hasContentWarning': 0, 'c.hasFoil': 1, 'c.hasNonFoil': 1, 'c.isAlternative': 0, 'c.isFullArt': 0, 'c.isOnlineOnly': 0, 'c.isOversized': 0, 'c.isPromo': 0, 'c.isReserved': 0, 'c.isStarter': 0, 'c.isStorySpotlight': 0, 'c.isTextless': 0, 'c.isTimeshifted': 0, 'c.keywords': None, 'c.layout': 'normal', 'c.leadershipSkills': None, 'c.life': None, 'c.loyalty': None, 'c.manaCost': '{B}', 'c.mcmId': '486434', 'c.mcmMetaId': '10047', 'c.mtgArenaId': None, 'c.mtgjsonV4Id': 'f68f4a6f-d1c6-5b92-a5a4-dc7762d079ae', 'c.mtgoFoilId': None, 'c.mtgoId': '82218', 'c.multiverseId': '489765', 'c.name': "Executioner's Capsule", 'c.number': '92', 'c.originalReleaseDate': None, 'c.originalText': "{1}{B}, {T}, Sacrifice Executioner's Capsule: Destroy target nonblack creature.", 'c.otherFaceIds': None, 'c.power': None, 'c.printings': '2XM,ALA,C16,MB1,MMA', 'c.promoTypes': None, 'c.purchaseUrls': "{'cardKingdom': 'https://mtgjson.com/links/f3de9034ad549e4d', 'cardKingdomFoil': 'https://mtgjson.com/links/3ed0ff791d97efff', 'cardmarket': 'https://mtgjson.com/links/53d76c48986a6528', 'tcgplayer': 'https://mtgjson.com/links/34b15dadf8e5b88f'}", 'c.rarity': 'common', 'c.scryfallId': '032ea333-96e1-4ad8-8947-21d6bc3a9f91', 'c.scryfallIllustrationId': '63406ef2-21e0-4113-94cf-69bbe55047cb', 'c.scryfallOracleId': 'c9cd266c-7ecf-4beb-b9da-69b88f33abd3', 'c.setCode': '2XM', 'c.side': None, 'c.subtypes': None, 'c.supertypes': None, 'c.tcgplayerProductId': '219528', 'c.text': "{1}{B}, {T}, Sacrifice Executioner's Capsule: Destroy target nonblack creature.", 'c.toughness': None, 'c.type': 'Artifact', 'types': 'Artifact', 'c.uuid': 'be690a68-9c47-5750-ba05-0ce332bf962a', 'c.variations': None, 'c.watermark': None, 'foreign_name': '処刑人の薬包', 'foreign_text': '{1}{B}, {T}, 処刑人の薬包を生け贄に捧げる：黒でないクリーチャー１体を対象とする。それを破壊する。', 'foreign_type': 'アーティファクト', 'foreign_flavorText': '書簡を開封する前には、いつも恐ろしい瞬間がある。その中にあるかもしれない決定に対する恐怖だ。', 'language': 'Japanese', 'multiverseid': 490761}] ... (+77行)

**预期结果**: [{'name': "Executioner's Capsule"}, {'name': 'Immortal Coil'}, {'name': 'Onyx Goblet'}] ... (+5行)

---

## 86. [ID:407]

**问题**: Lists all types of cards in German.

**证据**: (无)

**生成SQL**:
```sql
SELECT DISTINCT type FROM cards WHERE type IS NOT NULL AND type != ''
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

**生成结果**: [{'type': 'Creature — Human Cleric'}, {'type': 'Creature — Angel'}, {'type': 'Creature — Bird Soldier'}] ... (+997行)

**预期结果**: [{'subtypes': 'Human,Rebel', 'supertypes': 'Legendary'}, {'subtypes': 'Angel', 'supertypes': 'Legendary'}, {'subtypes': 'Merfolk,Wizard', 'supertypes': 'Legendary'}] ... (+997行)

---

## 87. [ID:408]

**问题**: How many unknown power cards contain info about the triggered ability

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(*) FROM cards WHERE (power IS NULL OR power = '*') AND text LIKE '%triggered ability%'
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

**生成结果**: [{'COUNT(*)': 35}]

**预期结果**: [{'Count(DISTINCT `T1`.`id`)': 1382}]

---

## 88. [ID:412]

**问题**: What is the foreign name of the card in French of type Creature, normal layout and black border color, by artist Matthew D. Wilson?

**证据**: (无)

**生成SQL**:
```sql
SELECT f.name FROM cards c INNER JOIN foreign_data f ON c.uuid = f.uuid WHERE f.language = 'French' AND c.type LIKE '%Creature%' AND c.layout = 'normal' AND c.borderColor = 'black' AND c.artist = 'Matthew D. Wilson'
```

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

**生成结果**: [{'name': 'Escouade de balistes'}, {'name': 'Reya Aubevenant'}, {'name': "Tisseuse d'esprit"}] ... (+48行)

**预期结果**: [{'name': 'Escouade de balistes'}, {'name': 'Reya Aubevenant'}, {'name': "Tisseuse d'esprit"}] ... (+47行)

---

## 89. [ID:459]

**问题**: Which card costs more converted mana, "Serra Angel" or "Shrine Keeper"?

**证据**: (无)

**生成SQL**:
```sql
SELECT name, convertedManaCost FROM cards WHERE name IN ('Serra Angel', 'Shrine Keeper') ORDER BY convertedManaCost DESC LIMIT 1
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

**生成结果**: [{'name': 'Serra Angel', 'convertedManaCost': 5.0}]

**预期结果**: [{'name': 'Serra Angel'}]

---

## 90. [ID:462]

**问题**: What's the Italian name of the set of cards with "Ancestor's Chosen" is in?

**证据**: (无)

**生成SQL**:
```sql
SELECT st.translation FROM set_translations st JOIN cards c ON st.setCode = c.setCode WHERE c.name = 'Ancestor''s Chosen' AND st.language = 'Italian'
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

**生成结果**: [{'translation': 'Set Base Decima Edizione'}, {'translation': 'Set Base Decima Edizione'}, {'translation': 'Sentenza'}]

**预期结果**: [{'translation': 'Set Base Decima Edizione'}, {'translation': 'Sentenza'}]

---

## 91. [ID:465]

**问题**: For the set of cards with "Ancestor's Chosen" in it, is there a Korean version of it?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(*) > 0 AS has_korean_version FROM foreign_data WHERE name = 'Ancestor''s Chosen' AND language = 'Korean'
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

**生成结果**: [{'has_korean_version': 0}]

**预期结果**: [{"CASE\n    WHEN SUM(\n      CASE\n        WHEN `T2`.`language` = 'Korean' AND NOT `T2`.`translation` IS NULL\n        THEN 1\n        ELSE 0\n      END\n    ) > 0\n    THEN 'YES'\n    ELSE 'NO'\n  END": 'YES'}]

---

## 92. [ID:466]

**问题**: Among the cards in the set "Hauptset Zehnte Edition", how many of them are designed by Adam Rex?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(*) FROM cards WHERE artist = 'Adam Rex' AND setCode = (SELECT code FROM set_translations WHERE translation = 'Hauptset Zehnte Edition')
```

**预期SQL**:
```sql
SELECT
  COUNT(`T1`.`id`)
FROM `cards` AS `T1`
INNER JOIN `set_translations` AS `T2`
  ON `T2`.`setCode` = `T1`.`setCode`
WHERE
  `T2`.`translation` = 'Hauptset Zehnte Edition' AND `T1`.`artist` = 'Adam Rex'
```

**生成结果**: []

**预期结果**: [{'COUNT(`T1`.`id`)': 12}]

---

## 93. [ID:469]

**问题**: Did the set of cards with "Angel of Mercy" appear on Magic: The Gathering Online?

**证据**: (无)

**生成SQL**:
```sql
SELECT EXISTS (SELECT 1 FROM cards c INNER JOIN sets s ON c.setCode = s.code WHERE c.name = 'Angel of Mercy' AND s.mtgoCode IS NOT NULL) AS appears_on_mtgo
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

**生成结果**: [{'appears_on_mtgo': 1}]

**预期结果**: [{"CASE WHEN NOT `T2`.`mtgoCode` IS NULL THEN 'YES' ELSE 'NO' END": 'YES'}, {"CASE WHEN NOT `T2`.`mtgoCode` IS NULL THEN 'YES' ELSE 'NO' END": 'YES'}, {"CASE WHEN NOT `T2`.`mtgoCode` IS NULL THEN 'YES' ELSE 'NO' END": 'YES'}] ... (+12行)

---

## 94. [ID:473]

**问题**: Is the set of cards with Adarkar Valkyrie only available outside the United States?

**证据**: (无)

**生成SQL**:
```sql
SELECT s.isForeignOnly FROM sets s INNER JOIN cards c ON s.code = c.setCode WHERE c.name = 'Adarkar Valkyrie'
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

**生成结果**: [{'isForeignOnly': 0}, {'isForeignOnly': 0}, {'isForeignOnly': 0}] ... (+2行)

**预期结果**: [{"CASE WHEN `isForeignOnly` = 1 THEN 'YES' ELSE 'NO' END": 'NO'}, {"CASE WHEN `isForeignOnly` = 1 THEN 'YES' ELSE 'NO' END": 'NO'}, {"CASE WHEN `isForeignOnly` = 1 THEN 'YES' ELSE 'NO' END": 'NO'}] ... (+2行)

---

## 95. [ID:479]

**问题**: Among the cards with converted mana cost higher than 5 in the set Coldsnap, how many of them have unknown power?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(*) FROM cards WHERE setCode = 'CDS' AND convertedManaCost > 5 AND (power = '*' OR power IS NULL)
```

**预期SQL**:
```sql
SELECT
  SUM(CASE WHEN `T1`.`power` = '*' OR `T1`.`power` IS NULL THEN 1 ELSE 0 END)
FROM `cards` AS `T1`
INNER JOIN `sets` AS `T2`
  ON `T2`.`code` = `T1`.`setCode`
WHERE
  `T2`.`name` = 'Coldsnap' AND `T1`.`convertedManaCost` > 5
```

**生成结果**: [{'COUNT(*)': 0}]

**预期结果**: [{"SUM(CASE WHEN `T1`.`power` = '*' OR `T1`.`power` IS NULL THEN 1 ELSE 0 END)": 6.0}]

---

## 96. [ID:480]

**问题**: What is the Italian flavor text of the card "Ancestor's Chosen"?

**证据**: (无)

**生成SQL**:
```sql
SELECT flavorText FROM foreign_data WHERE language = 'Italian' AND name = 'Ancestor''s Chosen'
```

**预期SQL**:
```sql
SELECT
  `T2`.`flavorText`
FROM `cards` AS `T1`
INNER JOIN `foreign_data` AS `T2`
  ON `T2`.`uuid` = `T1`.`uuid`
WHERE
  `T1`.`name` = 'Ancestor''s Chosen' AND `T2`.`language` = 'Italian'
```

**生成结果**: []

**预期结果**: [{'flavorText': '"La volontà di tutti, eseguita per mano mia."'}, {'flavorText': 'Sancito da generazioni di forza.'}]

---

## 97. [ID:483]

**问题**: Please list the Italian text ruling of all the cards in the set Coldsnap.

**证据**: (无)

**生成SQL**:
```sql
SELECT f.text FROM foreign_data f INNER JOIN cards c ON f.uuid = c.uuid WHERE f.language = 'Italian' AND c.setCode = 'CSP'
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

**生成结果**: [{'text': "Volare, cautela\n{T}: Quando una creatura bersaglio diversa dalla Valchiria dell'Adarkar viene messa in un cimitero in questo turno, rimetti in gioco quella carta sotto il tuo controllo."}, {'text': 'Volare\n{S}: Il Grifone di Borealia guadagna attacco improvviso fino alla fine del turno. ({S} può essere pagato con un mana da un permanente neve.)'}, {'text': 'Mantenimento cumulativo {S} ({S} può essere pagato con un mana da un permanente neve.)\nSe una creatura sta per infliggere danno da combattimento a te e/o a una o più creature che controlli, previeni X di quei danni, dove X è pari al numero di segnalini ep'}] ... (+152行)

**预期结果**: [{'text': "Volare, cautela\n{T}: Quando una creatura bersaglio diversa dalla Valchiria dell'Adarkar viene messa in un cimitero in questo turno, rimetti in gioco quella carta sotto il tuo controllo."}, {'text': 'Volare\n{S}: Il Grifone di Borealia guadagna attacco improvviso fino alla fine del turno. ({S} può essere pagato con un mana da un permanente neve.)'}, {'text': 'Mantenimento cumulativo {S} ({S} può essere pagato con un mana da un permanente neve.)\nSe una creatura sta per infliggere danno da combattimento a te e/o a una o più creature che controlli, previeni X di quei danni, dove X è pari al numero di segnalini ep'}] ... (+146行)

---

## 98. [ID:484]

**问题**: Please list the Italian names of the cards in the set Coldsnap with the highest converted mana cost.

**证据**: (无)

**生成SQL**:
```sql
SELECT f.name FROM foreign_data f INNER JOIN cards c ON f.uuid = c.uuid WHERE f.language = 'Italian' AND c.setCode = 'CSP' AND c.convertedManaCost = (SELECT MAX(convertedManaCost) FROM cards WHERE setCode = 'CSP')
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

**生成结果**: [{'name': 'Devastazione Solare'}, {'name': 'Requisire'}, {'name': 'Jokulmorder'}] ... (+9行)

**预期结果**: [{'name': 'Sunscour'}, {'name': 'Commandeer'}, {'name': 'Jokulmorder'}] ... (+152行)

---

## 99. [ID:518]

**问题**: Which of the play format has the highest number of banned status? Indicate the play format and the names of all the card meet the condition.

**证据**: (无)

**生成SQL**:
```sql
SELECT format, name FROM cards WHERE uuid IN (SELECT uuid FROM legalities WHERE status = 'Banned') GROUP BY format ORDER BY COUNT(*) DESC LIMIT 1
```

**预期SQL**:
```sql
SELECT T2.format, T1.name FROM cards AS T1 INNER JOIN legalities AS T2 ON T2.uuid = T1.uuid INNER JOIN ( SELECT format FROM legalities WHERE status = 'Banned' GROUP BY format ORDER BY COUNT(*) DESC LIMIT 1 ) AS MaxBanned ON MaxBanned.format = T2.format WHERE T2.status = 'Banned'
```

**生成结果**: []

**预期结果**: [{'format': 'legacy', 'name': 'Balance'}, {'format': 'legacy', 'name': 'Crusade'}, {'format': 'legacy', 'name': 'Ancestral Recall'}] ... (+543行)

---

## 100. [ID:522]

**问题**: Which cards are ranked 1st on EDHRec? List all of the cards name and its banned play format.

**证据**: (无)

**生成SQL**:
```sql
SELECT c.name, l.format FROM cards c INNER JOIN legalities l ON c.uuid = l.uuid WHERE c.edhrecRank = 1 AND l.status = 'Banned'
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

**生成结果**: [{'name': 'Sol Ring', 'format': 'duel'}, {'name': 'Sol Ring', 'format': 'legacy'}, {'name': 'Sol Ring', 'format': 'duel'}] ... (+63行)

**预期结果**: [{'name': 'Sol Ring', 'format': 'duel'}, {'name': 'Sol Ring', 'format': 'legacy'}]

---

## 101. [ID:529]

**问题**: Find and list the names of sets which doesn't have Japanese translation but have Korean translation.

**证据**: (无)

**生成SQL**:
```sql
SELECT s.name FROM sets s WHERE s.code IN (SELECT setCode FROM set_translations WHERE language = 'Korean') AND s.code NOT IN (SELECT setCode FROM set_translations WHERE language = 'Japanese')
```

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

**生成结果**: []

**预期结果**: [{'name': 'Tenth Edition'}, {'name': 'Fourth Edition'}, {'name': 'Fifth Dawn'}] ... (+118行)

---

## 102. [ID:530]

**问题**: List all the frame styles and cards Allen Williams worked on and find any banned cards if there are any.

**证据**: (无)

**生成SQL**:
```sql
SELECT DISTINCT c.frameVersion, c.name FROM cards c WHERE c.artist = 'Allen Williams' UNION SELECT DISTINCT c.frameVersion, c.name FROM cards c INNER JOIN legalities l ON c.uuid = l.uuid WHERE l.status = 'Banned' AND c.artist = 'Allen Williams'
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

**生成结果**: [{'frameVersion': '1997', 'name': 'Blinking Spirit'}, {'frameVersion': '1997', 'name': 'Kjeldoran Royal Guard'}, {'frameVersion': '1997', 'name': 'Enervate'}] ... (+80行)

**预期结果**: [{'frameVersion': '1997', 'name': 'Blinking Spirit', "CASE WHEN `T2`.`status` = 'Banned' THEN `T1`.`name` ELSE 'NO' END": 'NO'}, {'frameVersion': '1997', 'name': 'Kjeldoran Royal Guard', "CASE WHEN `T2`.`status` = 'Banned' THEN `T1`.`name` ELSE 'NO' END": 'NO'}, {'frameVersion': '1997', 'name': 'Enervate', "CASE WHEN `T2`.`status` = 'Banned' THEN `T1`.`name` ELSE 'NO' END": 'NO'}] ... (+80行)

---

## 103. [ID:201]

**问题**: What is the percentage of carbon in double-bond molecules?

**证据**: (无)

**生成SQL**:
```sql
SELECT (SUM(CASE WHEN a.element = 'c' THEN 1 ELSE 0 END) * 100.0 / COUNT(a.atom_id)) AS carbon_percentage FROM atom a INNER JOIN bond b ON a.molecule_id = b.molecule_id WHERE b.bond_type = '='
```

**预期SQL**:
```sql
SELECT
  CAST(COUNT(DISTINCT CASE WHEN `T1`.`element` = 'c' THEN `T1`.`atom_id` ELSE NULL END) AS DOUBLE) * 100 / COUNT(DISTINCT `T1`.`atom_id`)
FROM `atom` AS `T1`
INNER JOIN `bond` AS `T2`
  ON `T1`.`molecule_id` = `T2`.`molecule_id`
WHERE
  `T2`.`bond_type` = '='
```

**生成结果**: [{'carbon_percentage': 41.19624}]

**预期结果**: [{"CAST(COUNT(DISTINCT CASE WHEN `T1`.`element` = 'c' THEN `T1`.`atom_id` ELSE NULL END) AS DOUBLE) * 100 / COUNT(DISTINCT `T1`.`atom_id`)": 38.80961092816197}]

---

## 104. [ID:208]

**问题**: Which type of label is the most numerous in atoms with hydrogen?

**证据**: (无)

**生成SQL**:
```sql
SELECT label FROM molecule WHERE molecule_id IN (SELECT molecule_id FROM atom WHERE element = 'h') GROUP BY label ORDER BY COUNT(*) DESC LIMIT 1
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

**生成结果**: [{'label': '-'}]

**预期结果**: []

---

## 105. [ID:213]

**问题**: What type of bond is there between the atoms TR004_8 and TR004_20?

**证据**: (无)

**生成SQL**:
```sql
SELECT bond_type FROM bond WHERE bond_id = (SELECT bond_id FROM connected WHERE (atom_id = 'TR004_8' AND atom_id2 = 'TR004_20') OR (atom_id = 'TR004_20' AND atom_id2 = 'TR004_8'))
```

**预期SQL**:
```sql
SELECT
  `T1`.`bond_type`
FROM `bond` AS `T1`
INNER JOIN `connected` AS `T2`
  ON `T1`.`bond_id` = `T2`.`bond_id`
WHERE
  `T2`.`atom_id` = 'TR004_8'
  AND `T2`.`atom_id2` = 'TR004_20'
  OR `T2`.`atom_id2` = 'TR004_8'
  AND `T2`.`atom_id` = 'TR004_20'
```

**生成结果**: []

**预期结果**: [{'bond_type': '-'}, {'bond_type': '-'}]

---

## 106. [ID:234]

**问题**: How many bonds which involved atom 12 does molecule TR009 have?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(*) FROM bond WHERE molecule_id = 'TR009' AND (bond_id IN (SELECT bond_id FROM connected WHERE atom_id = 'TR009_12' OR atom_id2 = 'TR009_12'))
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

**生成结果**: [{'COUNT(*)': 3}]

**预期结果**: [{'COUNT(`T2`.`bond_id`)': 1041}]

---

## 107. [ID:273]

**问题**: What is the percentage of element chlorine in carcinogenic molecules?

**证据**: (无)

**生成SQL**:
```sql
SELECT (SUM(CASE WHEN element = 'cl' THEN 1 ELSE 0 END) * 100.0 / COUNT(DISTINCT molecule_id)) AS percentage FROM molecule m INNER JOIN atom a ON m.molecule_id = a.molecule_id WHERE m.label = '+'
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

**生成结果**: []

**预期结果**: [{"CAST(COUNT(CASE WHEN `T1`.`element` = 'cl' THEN `T1`.`element` ELSE NULL END) AS DOUBLE) * 100 / COUNT(`T1`.`element`)": 3.1419284940411703}]

---

## 108. [ID:327]

**问题**: Which non-carcinogenic molecules consisted more than 5 atoms?

**证据**: (无)

**生成SQL**:
```sql
SELECT m.molecule_id FROM molecule m WHERE m.label = '-' AND (SELECT COUNT(*) FROM atom a WHERE a.molecule_id = m.molecule_id) > 5
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

**生成结果**: [{'molecule_id': 'TR002'}, {'molecule_id': 'TR004'}, {'molecule_id': 'TR007'}] ... (+183行)

**预期结果**: []

---

## 109. [ID:23]

**问题**: List the names of schools with more than 30 difference in enrollements between K-12 and ages 5-17? Please also give the full street adress of the schools.

**证据**: (无)

**生成SQL**:
```sql
SELECT s.School, s.Street, s.StreetAbr, s.City, s.Zip FROM frpm f INNER JOIN schools s ON f.CDSCode = s.CDSCode WHERE ABS(f.`Enrollment (K-12)` - f.`Enrollment (Ages 5-17)`) > 30
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

**生成结果**: [{'School': 'Alameda County Community', 'Street': '313 West Winton Avenue', 'StreetAbr': '313 West Winton Ave.', 'City': 'Hayward', 'Zip': '94544-1136'}, {'School': 'California School for the Deaf-Fremont', 'Street': '39350 Gallaudet Drive', 'StreetAbr': '39350 Gallaudet Dr.', 'City': 'Fremont', 'Zip': '94538-2308'}, {'School': 'Alameda High', 'Street': '2201 Encinal Avenue', 'StreetAbr': '2201 Encinal Ave.', 'City': 'Alameda', 'Zip': '94501-4406'}] ... (+997行)

**预期结果**: [{'School': 'Alameda County Community', 'Street': '313 West Winton Avenue'}, {'School': 'California School for the Deaf-Fremont', 'Street': '39350 Gallaudet Drive'}, {'School': 'Alameda High', 'Street': '2201 Encinal Avenue'}] ... (+997行)

---

## 110. [ID:24]

**问题**: Give the names of the schools with the percent eligible for free meals in K-12 is more than 0.1 and test takers whose test score is greater than or equal to 1500?

**证据**: (无)

**生成SQL**:
```sql
SELECT T1.School Name FROM frpm T1 INNER JOIN satscores T2 ON T1.CDSCode = T2.cds WHERE (T1."Free Meal Count (K-12)" / T1."Enrollment (K-12)") > 0.1 AND T2.NumGE1500 > 0
```

**预期SQL**:
```sql
SELECT
  `T2`.`School Name`
FROM `satscores` AS `T1`
INNER JOIN `frpm` AS `T2`
  ON `T1`.`cds` = `T2`.`CDSCode`
WHERE
  CAST(`T2`.`Free Meal Count (K-12)` AS DOUBLE) / `T2`.`Enrollment (K-12)` > 0.1
  AND `T1`.`NumGE1500` > 0
```

**生成结果**: []

**预期结果**: [{'School Name': 'FAME Public Charter'}, {'School Name': 'Envision Academy for Arts & Technology'}, {'School Name': 'Alameda Science and Technology Institute'}] ... (+997行)

---

## 111. [ID:25]

**问题**: Name schools in Riverside which the average of average math score for SAT is grater than 400, what is the funding type of these schools?

**证据**: (无)

**生成SQL**:
```sql
SELECT s.School, s.FundingType FROM schools s INNER JOIN satscores sc ON s.CDSCode = sc.cds WHERE s.County = 'Riverside' GROUP BY s.CDSCode, s.School, s.FundingType HAVING AVG(sc.AvgScrMath) > 400
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

**生成结果**: [{'School': None, 'FundingType': None}, {'School': 'River Springs Charter', 'FundingType': 'Directly funded'}, {'School': None, 'FundingType': None}] ... (+77行)

**预期结果**: [{'sname': 'River Springs Charter', 'Charter Funding Type': 'Directly funded'}, {'sname': 'Arlington High', 'Charter Funding Type': None}, {'sname': 'Martin Luther King Jr. High', 'Charter Funding Type': None}] ... (+3行)

---

## 112. [ID:26]

**问题**: State the names and full communication address of high schools in Monterey which has more than 800 free or reduced price meals for ages 15-17?

**证据**: (无)

**生成SQL**:
```sql
SELECT s.School, s.Street, s.City, s.State, s.Zip FROM schools s INNER JOIN frpm f ON s.CDSCode = f.CDSCode WHERE s.County = 'Monterey' AND s.GSoffered LIKE '%15%' AND s.GSoffered LIKE '%17%' AND f."FRPM Count (Ages 5-17)" > 800
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

**生成结果**: []

**预期结果**: [{'School Name': 'Alisal High', 'Street': '777 Williams Road', 'City': 'Salinas', 'State': 'CA', 'Zip': '93905-1907'}, {'School Name': 'Everett Alvarez High', 'Street': '1900 Independence Boulevard', 'City': 'Salinas', 'State': 'CA', 'Zip': '93906-5300'}, {'School Name': 'North Salinas High', 'Street': '55 Kip Drive', 'City': 'Salinas', 'State': 'CA', 'Zip': '93906-2908'}] ... (+2行)

---

## 113. [ID:27]

**问题**: What is the average score in writing for the schools that were opened after 1991 or closed before 2000? List the school names along with the score. Also, list the communication number of the schools if there is any.

**证据**: (无)

**生成SQL**:
```sql
SELECT s.School, satscores.AvgScrWrite, s.Phone FROM satscores INNER JOIN schools ON satscores.cds = schools.CDSCode WHERE (schools.OpenDate > '1991-12-31' OR schools.ClosedDate < '2000-01-01')
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

**生成结果**: []

**预期结果**: [{'School': 'FAME Public Charter', 'AvgScrWrite': 505, 'Phone': None}, {'School': 'Envision Academy for Arts & Technology', 'AvgScrWrite': 395, 'Phone': '(510) 596-8901'}, {'School': 'Aspire California College Preparatory Academy', 'AvgScrWrite': None, 'Phone': None}] ... (+997行)

---

## 114. [ID:31]

**问题**: What is the eligible free rate of the 10th and 11th schools with the highest enrolment for students in grades 1 through 12?

**证据**: (无)

**生成SQL**:
```sql
SELECT `Percent (%) Eligible Free (K-12)` FROM frpm WHERE `Enrollment (K-12)` IS NOT NULL ORDER BY `Enrollment (K-12)` DESC LIMIT 10 OFFSET 9
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

**生成结果**: [{'Percent (%) Eligible Free (K-12)': 0.13443640124095}, {'Percent (%) Eligible Free (K-12)': 0.29058945191313}, {'Percent (%) Eligible Free (K-12)': 0.42917103882476}] ... (+7行)

**预期结果**: [{'CAST(`Free Meal Count (K-12)` AS DOUBLE) / `Enrollment (K-12)`': 0.1344364012409514}, {'CAST(`Free Meal Count (K-12)` AS DOUBLE) / `Enrollment (K-12)`': 0.2905894519131334}]

---

## 115. [ID:32]

**问题**: What is the eligible free or reduced price meal rate for the top 5 schools in grades 1-12 with the highest free or reduced price meal count of the schools with the ownership code 66?

**证据**: (无)

**生成SQL**:
```sql
SELECT T1.`School Name`, T1.`Percent (%) Eligible FRPM (K-12)` FROM frpm T1 INNER JOIN schools T2 ON T1.`CDSCode` = T2.`CDSCode` WHERE T2.`SOC` = '66' AND T1.`Academic Year` = (SELECT MAX(`Academic Year`) FROM frpm) ORDER BY T1.`FRPM Count (K-12)` DESC LIMIT 5
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

**生成结果**: [{'School Name': 'Paramount High', 'Percent (%) Eligible FRPM (K-12)': 0.91794765267968}, {'School Name': 'Calexico High', 'Percent (%) Eligible FRPM (K-12)': 0.99932908419993}, {'School Name': 'Bell Senior High', 'Percent (%) Eligible FRPM (K-12)': 0.89649877149877}] ... (+2行)

**预期结果**: [{'CAST(`T1`.`FRPM Count (K-12)` AS DOUBLE) / `T1`.`Enrollment (K-12)`': 0.9179476526796843}, {'CAST(`T1`.`FRPM Count (K-12)` AS DOUBLE) / `T1`.`Enrollment (K-12)`': 0.9993290841999329}, {'CAST(`T1`.`FRPM Count (K-12)` AS DOUBLE) / `T1`.`Enrollment (K-12)`': 0.8964987714987716}] ... (+2行)

---

## 116. [ID:37]

**问题**: What is the complete address of the school with the lowest excellence rate? Indicate the Street, City, Zip and State.

**证据**: (无)

**生成SQL**:
```sql
SELECT s.Street, s.City, s.Zip, s.State FROM schools s INNER JOIN satscores sc ON s.CDSCode = sc.cds WHERE sc.NumTstTakr > 0 ORDER BY (sc.NumGE1500 / sc.NumTstTakr) ASC LIMIT 1
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

**生成结果**: [{'Street': '1900 Third Street', 'City': 'Alameda', 'Zip': '94501-1851', 'State': 'CA'}]

**预期结果**: [{'Street': '2125 Jefferson Avenue', 'City': 'Berkeley', 'State': 'CA', 'Zip': '94703-1414'}]

---

## 117. [ID:40]

**问题**: What is the telephone number for the school with the lowest average score in reading in Fresno Unified?

**证据**: (无)

**生成SQL**:
```sql
SELECT s.Phone FROM schools s INNER JOIN satscores sc ON s.CDSCode = sc.cds WHERE sc.cname = 'Fresno' AND s.District = 'Fresno Unified' ORDER BY sc.AvgScrRead ASC LIMIT 1
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

**生成结果**: [{'Phone': '(559) 498-8543'}]

**预期结果**: [{'Phone': '(559) 248-5100'}]

---

## 118. [ID:72]

**问题**: How many students from the ages of 5 to 17 are enrolled at the State Special School school in Fremont for the 2014-2015 academic year?

**证据**: (无)

**生成SQL**:
```sql
SELECT SUM(`Enrollment (Ages 5-17)`) FROM frpm WHERE `Academic Year` = '2014-2015' AND `School Type` = 'State Special Schools' AND `School Name` LIKE '%Fremont%'
```

**预期SQL**:
```sql
SELECT
  `T1`.`Enrollment (Ages 5-17)`
FROM `frpm` AS `T1`
INNER JOIN `schools` AS `T2`
  ON `T1`.`CDSCode` = `T2`.`CDSCode`
WHERE
  `T2`.`EdOpsCode` = 'SSS'
  AND `T2`.`City` = 'Fremont'
  AND `T1`.`Academic Year` BETWEEN 2014 AND 2015
```

**生成结果**: [{'SUM(`Enrollment (Ages 5-17)`)': 335.0}]

**预期结果**: [{'Enrollment (Ages 5-17)': 40.0}, {'Enrollment (Ages 5-17)': 335.0}]

---

## 119. [ID:77]

**问题**: Which schools served a grade span of Kindergarten to 9th grade in the county of Los Angeles and what is its Percent (%) Eligible FRPM (Ages 5-17)?

**证据**: (无)

**生成SQL**:
```sql
SELECT f.`School Name`, f.`Percent (%) Eligible FRPM (Ages 5-17)` FROM frpm f INNER JOIN schools s ON f.`CDSCode` = s.`CDSCode` WHERE s.`County` = 'Los Angeles' AND f.`Low Grade` = 'K' AND f.`High Grade` = '9'
```

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

**生成结果**: []

**预期结果**: [{'School': 'White Oak Elementary', '`T1`.`FRPM Count (Ages 5-17)` * 100 / `T1`.`Enrollment (Ages 5-17)`': 3.755868544600939}, {'School': 'The Accelerated', '`T1`.`FRPM Count (Ages 5-17)` * 100 / `T1`.`Enrollment (Ages 5-17)`': 97.63888888888889}]

---

## 120. [ID:85]

**问题**: What is the Percent (%) Eligible Free (K-12) in the school administered by an administrator whose first name is Alusine. List the district code of the school.

**证据**: (无)

**生成SQL**:
```sql
SELECT frpm."District Code" FROM frpm INNER JOIN schools ON frpm."CDSCode" = schools."CDSCode" WHERE schools."AdmFName1" = 'Alusine'
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

**生成结果**: []

**预期结果**: [{'`T1`.`Free Meal Count (K-12)` * 100 / `T1`.`Enrollment (K-12)`': 70.15113350125945, 'District Code': 64857}]

---

## 121. [ID:95]

**问题**: List out the account numbers of clients who are youngest and have highest average salary?

**证据**: (无)

**生成SQL**:
```sql
SELECT DISTINCT a.account_id FROM account a JOIN disp d ON a.account_id = d.account_id JOIN client c ON d.client_id = c.client_id JOIN district di ON a.district_id = di.district_id WHERE c.birth_date = (SELECT MIN(birth_date) FROM client) AND di.A11 = (SELECT MAX(A11) FROM district)
```

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

**生成结果**: []

**预期结果**: [{'account_id': 2836}]

---

## 122. [ID:98]

**问题**: Among the accounts who have approved loan date in 1997, list out the accounts that have the lowest approved amount and choose weekly issuance statement.

**证据**: (无)

**生成SQL**:
```sql
SELECT DISTINCT T1.account_id FROM account T1 INNER JOIN loan T2 ON T1.account_id = T2.account_id WHERE T2.date >= '1997-01-01' AND T2.date <= '1997-12-31' AND T1.frequency = 'POPLATEK TYDNE' AND T2.amount = (SELECT MIN(amount) FROM loan WHERE date >= '1997-01-01' AND date <= '1997-12-31')
```

**预期SQL**:
```sql
SELECT
  `T2`.`account_id`
FROM `loan` AS `T1`
INNER JOIN `account` AS `T2`
  ON `T1`.`account_id` = `T2`.`account_id`
WHERE
  DATE_FORMAT(CAST(`T1`.`date` AS DATETIME), '%Y') = '1997'
  AND `T2`.`frequency` = 'POPLATEK TYDNE'
ORDER BY
  `T1`.`amount`
LIMIT 1
```

**生成结果**: []

**预期结果**: [{'account_id': 176}]

---

## 123. [ID:129]

**问题**: Which are the top ten withdrawals (non-credit card) by district names for the month of January 1996?

**证据**: (无)

**生成SQL**:
```sql
SELECT d.A2 AS district_name, SUM(t.amount) AS total_withdrawals FROM trans t INNER JOIN account a ON t.account_id = a.account_id INNER JOIN district d ON a.district_id = d.district_id WHERE t.type = 'VYDAJ' AND t.date LIKE '1996-01%' GROUP BY d.A2 ORDER BY total_withdrawals DESC LIMIT 10
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

**生成结果**: [{'district_name': 'Hl.m. Praha', 'total_withdrawals': 6757078.0}, {'district_name': 'Karvina', 'total_withdrawals': 1777590.0}, {'district_name': 'Ostrava - mesto', 'total_withdrawals': 1712383.0}] ... (+7行)

**预期结果**: [{'A2': 'Benesov'}, {'A2': 'Beroun'}, {'A2': 'Blansko'}] ... (+7行)

---

## 124. [ID:145]

**问题**: Who are the account holder identification numbers whose who have transactions on the credit card with the amount is less than the average, in 1998?

**证据**: (无)

**生成SQL**:
```sql
SELECT DISTINCT T1.account_id FROM trans T1 WHERE T1.operation = 'VYBER KARTOU' AND T1.date >= '1998-01-01' AND T1.date <= '1998-12-31' AND T1.amount < (SELECT AVG(amount) FROM trans WHERE operation = 'VYBER KARTOU' AND date >= '1998-01-01' AND date <= '1998-12-31')
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

**生成结果**: [{'account_id': 14}, {'account_id': 33}, {'account_id': 43}] ... (+657行)

**预期结果**: [{'account_id': 14}, {'account_id': 14}, {'account_id': 14}] ... (+997行)

---

## 125. [ID:152]

**问题**: What is the average number of crimes committed in 1995 in regions where the number exceeds 4000 and the region has accounts that are opened starting from the year 1997?

**证据**: (无)

**生成SQL**:
```sql
SELECT AVG(A15) FROM district WHERE A15 > 4000 AND district_id IN (SELECT district_id FROM account WHERE YEAR(date) >= 1997)
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

**生成结果**: [{'AVG(A15)': 9675.0385}]

**预期结果**: [{'AVG(`T1`.`A15`)': 29670.4495}]

---

## 126. [ID:186]

**问题**: What percentage of male clients request for weekly statements to be issued?

**证据**: (无)

**生成SQL**:
```sql
SELECT (COUNT(CASE WHEN c.gender = 'M' THEN 1 END) * 100.0 / COUNT(*)) AS percentage FROM client c INNER JOIN disp d ON c.client_id = d.client_id INNER JOIN account a ON d.account_id = a.account_id WHERE a.frequency = 'POPLATEK TYDNE' AND d.type = 'OWNER'
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

**生成结果**: [{'percentage': 54.16667}]

**预期结果**: [{"CAST(SUM(`T1`.`gender` = 'M') AS DOUBLE) * 100 / COUNT(`T1`.`client_id`)": 52.63157894736842}]

---

## 127. [ID:194]

**问题**: Provide the IDs and age of the client with high level credit card, which is eligible for loans.

**证据**: (无)

**生成SQL**:
```sql
SELECT DISTINCT c.client_id, TIMESTAMPDIFF(YEAR, c.birth_date, CURDATE()) AS age FROM client c INNER JOIN disp d ON c.client_id = d.client_id INNER JOIN card ca ON d.disp_id = ca.disp_id WHERE ca.type = 'gold' AND d.type = 'OWNER'
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

**生成结果**: [{'client_id': 9, 'age': 90}, {'client_id': 41, 'age': 57}, {'client_id': 79, 'age': 56}] ... (+85行)

**预期结果**: [{'client_id': 9, "DATE_FORMAT(CAST(CURRENT_TIMESTAMP() AS DATETIME), '%Y') - DATE_FORMAT(CAST(`T3`.`birth_date` AS DATETIME), '%Y')": 91.0}, {'client_id': 41, "DATE_FORMAT(CAST(CURRENT_TIMESTAMP() AS DATETIME), '%Y') - DATE_FORMAT(CAST(`T3`.`birth_date` AS DATETIME), '%Y')": 58.0}, {'client_id': 79, "DATE_FORMAT(CAST(CURRENT_TIMESTAMP() AS DATETIME), '%Y') - DATE_FORMAT(CAST(`T3`.`birth_date` AS DATETIME), '%Y')": 57.0}] ... (+85行)

---

---

# Challenging 难度失败案例 (56个)

## 1. [ID:1481]

**问题**: What is the difference in the annual average consumption of the customers with the least amount of consumption paid in CZK for 2013 between SME and LAM, LAM and KAM, and KAM and SME?

**证据**: (无)

**生成SQL**:
```sql
SELECT (SELECT AVG(consumption) FROM (SELECT CustomerID, SUM(Consumption) AS consumption FROM yearmonth WHERE Date BETWEEN '201301' AND '201312' AND CustomerID IN (SELECT CustomerID FROM customers WHERE Currency = 'CZK' AND Segment = 'SME' GROUP BY CustomerID HAVING SUM(Consumption) = (SELECT MIN(total_consumption) FROM (SELECT CustomerID, SUM(Consumption) AS total_consumption FROM yearmonth WHERE Date BETWEEN '201301' AND '201312' AND CustomerID IN (SELECT CustomerID FROM customers WHERE Currency = 'CZK' AND Segment = 'SME') GROUP BY CustomerID) t)) GROUP BY CustomerID) t) - (SELECT AVG(consumption) FROM (SELECT CustomerID, SUM(Consumption) AS consumption FROM yearmonth WHERE Date BETWEEN '201301' AND '201312' AND CustomerID IN (SELECT CustomerID FROM customers WHERE Currency = 'CZK' AND Segment = 'LAM' GROUP BY CustomerID HAVING SUM(Consumption) = (SELECT MIN(total_consumption) FROM (SELECT CustomerID, SUM(Consumption) AS total_consumption FROM yearmonth WHERE Date BETWEEN '201301' AND '201312' AND CustomerID IN (SELECT CustomerID FROM customers WHERE Currency = 'CZK' AND Segment = 'LAM') GROUP BY CustomerID) t)) GROUP BY CustomerID) t) AS SME_LAM, (SELECT AVG(consumption) FROM (SELECT CustomerID, SUM(Consumption) AS consumption FROM yearmonth WHERE Date BETWEEN '201301' AND '201312' AND CustomerID IN (SELECT CustomerID FROM customers WHERE Currency = 'CZK' AND Segment = 'LAM' GROUP BY CustomerID HAVING SUM(Consumption) = (SELECT MIN(total_consumption) FROM (SELECT CustomerID, SUM(Consumption) AS total_consumption FROM yearmonth WHERE Date BETWEEN '201301' AND '201312' AND CustomerID IN (SELECT CustomerID FROM customers WHERE Currency = 'CZK' AND Segment = 'LAM') GROUP BY CustomerID) t)) GROUP BY CustomerID) t) - (SELECT AVG(consumption) FROM (SELECT CustomerID, SUM(Consumption) AS consumption FROM yearmonth WHERE Date BETWEEN '201301' AND '201312' AND CustomerID IN (SELECT CustomerID FROM customers WHERE Currency = 'CZK' AND Segment = 'KAM' GROUP BY CustomerID HAVING SUM(Consumption) = (SELECT MIN(total_consumption) FROM (SELECT CustomerID, SUM(Consumption) AS total_consumption FROM yearmonth WHERE Date BETWEEN '201301' AND '201312' AND CustomerID IN (SELECT CustomerID FROM customers WHERE Currency = 'CZK' AND Segment = 'KAM') GROUP BY CustomerID) t)) GROUP BY CustomerID) t) AS LAM_KAM, (SELECT AVG(consumption) FROM (SELECT CustomerID, SUM(Consumption) AS consumption FROM yearmonth WHERE Date BETWEEN '201301' AND '201312' AND CustomerID IN (SELECT CustomerID FROM customers WHERE Currency = 'CZK' AND Segment = 'KAM' GROUP BY CustomerID HAVING SUM(Consumption) = (SELECT MIN(total_consumption) FROM (SELECT CustomerID, SUM(Consumption) AS total_consumption FROM yearmonth WHERE Date BETWEEN '201301' AND '201312' AND CustomerID IN (SELECT CustomerID FROM customers WHERE Currency = 'CZK' AND Segment = 'KAM') GROUP BY CustomerID) t)) GROUP BY CustomerID) t) - (SELECT AVG(consumption) FROM (SELECT CustomerID, SUM(Consumption) AS consumption FROM yearmonth WHERE Date BETWEEN '201301' AND '201312' AND CustomerID IN (SELECT CustomerID FROM customers WHERE Currency = 'CZK' AND Segment = 'SME' GROUP BY CustomerID HAVING SUM(Consumption) = (SELECT MIN(total_consumption) FROM (SELECT CustomerID, SUM(Consumption) AS total_consumption FROM yearmonth WHERE Date BETWEEN '201301' AND '201312' AND CustomerID IN (SELECT CustomerID FROM customers WHERE Currency = 'CZK' AND Segment = 'SME') GROUP BY CustomerID) t)) GROUP BY CustomerID) t) AS KAM_SME
```

**预期SQL**:
```sql
SELECT
  CAST(SUM(CASE WHEN `T1`.`Segment` = 'SME' THEN `T2`.`Consumption` ELSE 0 END) AS DOUBLE) / COUNT(`T1`.`CustomerID`) - CAST(SUM(CASE WHEN `T1`.`Segment` = 'LAM' THEN `T2`.`Consumption` ELSE 0 END) AS DOUBLE) / COUNT(`T1`.`CustomerID`),
  CAST(SUM(CASE WHEN `T1`.`Segment` = 'LAM' THEN `T2`.`Consumption` ELSE 0 END) AS DOUBLE) / COUNT(`T1`.`CustomerID`) - CAST(SUM(CASE WHEN `T1`.`Segment` = 'KAM' THEN `T2`.`Consumption` ELSE 0 END) AS DOUBLE) / COUNT(`T1`.`CustomerID`),
  CAST(SUM(CASE WHEN `T1`.`Segment` = 'KAM' THEN `T2`.`Consumption` ELSE 0 END) AS DOUBLE) / COUNT(`T1`.`CustomerID`) - CAST(SUM(CASE WHEN `T1`.`Segment` = 'SME' THEN `T2`.`Consumption` ELSE 0 END) AS DOUBLE) / COUNT(`T1`.`CustomerID`)
FROM `customers` AS `T1`
INNER JOIN `yearmonth` AS `T2`
  ON `T1`.`CustomerID` = `T2`.`CustomerID`
WHERE
  `T1`.`Currency` = 'CZK'
  AND `T2`.`Consumption` = (
    SELECT
      MIN(`Consumption`)
    FROM `yearmonth`
  )
  AND `T2`.`Date` BETWEEN 201301 AND 201312
```

**生成结果**: []

**预期结果**: [{"CAST(SUM(CASE WHEN `T1`.`Segment` = 'SME' THEN `T2`.`Consumption` ELSE 0 END) AS DOUBLE) / COUNT(`T1`.`CustomerID`) - CAST(SUM(CASE WHEN `T1`.`Segment` = 'LAM' THEN `T2`.`Consumption` ELSE 0 END) AS DOUBLE) / COUNT(`T1`.`CustomerID`)": 0.0, "CAST(SUM(CASE WHEN `T1`.`Segment` = 'LAM' THEN `T2`.`Consumption` ELSE 0 END) AS DOUBLE) / COUNT(`T1`.`CustomerID`) - CAST(SUM(CASE WHEN `T1`.`Segment` = 'KAM' THEN `T2`.`Consumption` ELSE 0 END) AS DOUBLE) / COUNT(`T1`.`CustomerID`)": 582092.86, "CAST(SUM(CASE WHEN `T1`.`Segment` = 'KAM' THEN `T2`.`Consumption` ELSE 0 END) AS DOUBLE) / COUNT(`T1`.`CustomerID`) - CAST(SUM(CASE WHEN `T1`.`Segment` = 'SME' THEN `T2`.`Consumption` ELSE 0 END) AS DOUBLE) / COUNT(`T1`.`CustomerID`)": -582092.86}]

---

## 2. [ID:1482]

**问题**: Which of the three segments—SME, LAM and KAM—has the biggest and lowest percentage increases in consumption paid in EUR between 2012 and 2013?

**证据**: (无)

**生成SQL**:
```sql
SELECT T1.Segment, CAST((SUM(CASE WHEN SUBSTRING(T2.Date, 1, 4) = '2013' THEN T2.Consumption ELSE 0 END) - SUM(CASE WHEN SUBSTRING(T2.Date, 1, 4) = '2012' THEN T2.Consumption ELSE 0 END)) / SUM(CASE WHEN SUBSTRING(T2.Date, 1, 4) = '2012' THEN T2.Consumption ELSE 0 END) * 100 AS DOUBLE) AS PercentageIncrease FROM customers T1 INNER JOIN yearmonth T2 ON T1.CustomerID = T2.CustomerID WHERE T1.Currency = 'EUR' AND (SUBSTRING(T2.Date, 1, 4) = '2012' OR SUBSTRING(T2.Date, 1, 4) = '2013') GROUP BY T1.Segment ORDER BY PercentageIncrease DESC LIMIT 1 UNION ALL SELECT T1.Segment, CAST((SUM(CASE WHEN SUBSTRING(T2.Date, 1, 4) = '2013' THEN T2.Consumption ELSE 0 END) - SUM(CASE WHEN SUBSTRING(T2.Date, 1, 4) = '2012' THEN T2.Consumption ELSE 0 END)) / SUM(CASE WHEN SUBSTRING(T2.Date, 1, 4) = '2012' THEN T2.Consumption ELSE 0 END) * 100 AS DOUBLE) AS PercentageIncrease FROM customers T1 INNER JOIN yearmonth T2 ON T1.CustomerID = T2.CustomerID WHERE T1.Currency = 'EUR' AND (SUBSTRING(T2.Date, 1, 4) = '2012' OR SUBSTRING(T2.Date, 1, 4) = '2013') GROUP BY T1.Segment ORDER BY PercentageIncrease ASC LIMIT 1
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
  ) - SUM(
    CASE
      WHEN `T1`.`Segment` = 'LAM' AND `T2`.`Date` LIKE '2012%'
      THEN `T2`.`Consumption`
      ELSE 0
    END
  ) AS DOUBLE) * 100 / SUM(
    CASE
      WHEN `T1`.`Segment` = 'LAM' AND `T2`.`Date` LIKE '2012%'
      THEN `T2`.`Consumption`
      ELSE 0
    END
  ),
  CAST(SUM(
    CASE
      WHEN `T1`.`Segment` = 'KAM' AND `T2`.`Date` LIKE '2013%'
      THEN `T2`.`Consumption`
      ELSE 0
    END
  ) - SUM(
    CASE
      WHEN `T1`.`Segment` = 'KAM' AND `T2`.`Date` LIKE '2012%'
      THEN `T2`.`Consumption`
      ELSE 0
    END
  ) AS DOUBLE) * 100 / SUM(
    CASE
      WHEN `T1`.`Segment` = 'KAM' AND `T2`.`Date` LIKE '2012%'
      THEN `T2`.`Consumption`
      ELSE 0
    END
  )
FROM `customers` AS `T1`
INNER JOIN `yearmonth` AS `T2`
  ON `T1`.`CustomerID` = `T2`.`CustomerID`
```

**生成结果**: []

**预期结果**: [{"CAST((\n    SUM(\n      CASE\n        WHEN `T1`.`Segment` = 'SME' AND `T2`.`Date` LIKE '2013%'\n        THEN `T2`.`Consumption`\n        ELSE 0\n      END\n    ) - SUM(\n      CASE\n        WHEN `T1`.`Segment` = 'SME' AND `T2`.`Date` LIKE '2012%'\n        THEN `T2`": 545.4018999791232, "CAST(SUM(\n    CASE\n      WHEN `T1`.`Segment` = 'LAM' AND `T2`.`Date` LIKE '2013%'\n      THEN `T2`.`Consumption`\n      ELSE 0\n    END\n  ) - SUM(\n    CASE\n      WHEN `T1`.`Segment` = 'LAM' AND `T2`.`Date` LIKE '2012%'\n      THEN `T2`.`Consumption`\n      ELS": 681.5824574939396, "CAST(SUM(\n    CASE\n      WHEN `T1`.`Segment` = 'KAM' AND `T2`.`Date` LIKE '2013%'\n      THEN `T2`.`Consumption`\n      ELSE 0\n    END\n  ) - SUM(\n    CASE\n      WHEN `T1`.`Segment` = 'KAM' AND `T2`.`Date` LIKE '2012%'\n      THEN `T2`.`Consumption`\n      ELS": 708.1124062978652}]

---

## 3. [ID:1457]

**问题**: Give the full name and contact number of members who had to spend more than average on each expense.

**证据**: (无)

**生成SQL**:
```sql
SELECT m.first_name, m.last_name, m.phone FROM member m INNER JOIN expense e ON m.member_id = e.link_to_member WHERE e.cost > (SELECT AVG(cost) FROM expense)
```

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

**生成结果**: [{'first_name': 'Sacha', 'last_name': 'Harrison', 'phone': '840-555-4781'}, {'first_name': 'Sacha', 'last_name': 'Harrison', 'phone': '840-555-4781'}, {'first_name': 'Sacha', 'last_name': 'Harrison', 'phone': '840-555-4781'}] ... (+8行)

**预期结果**: [{'first_name': 'Sacha', 'last_name': 'Harrison', 'phone': '840-555-4781'}, {'first_name': 'Phillip', 'last_name': 'Cullen', 'phone': '905-555-5035'}, {'first_name': 'Elijah', 'last_name': 'Allen', 'phone': '724-555-5721'}]

---

## 4. [ID:1168]

**问题**: The oldest SJS patient's medical laboratory work was completed on what date, and what age was the patient when they initially arrived at the hospital?

**证据**: (无)

**生成SQL**:
```sql
SELECT T1.Date, (YEAR(T1.`First Date`) - YEAR(T2.Birthday)) AS age FROM Patient T2 INNER JOIN Laboratory T1 ON T2.ID = T1.ID WHERE T2.Diagnosis LIKE '%SJS%' ORDER BY T2.Birthday ASC LIMIT 1
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

**生成结果**: []

**预期结果**: [{'Date': '1981-07-31', "DATE_FORMAT(CAST(`T2`.`First Date` AS DATETIME), '%Y') - DATE_FORMAT(CAST(`T2`.`Birthday` AS DATETIME), '%Y')": 69.0, 'Birthday': '1917-04-18'}]

---

## 5. [ID:1169]

**问题**: What is the ratio of male to female patients among all those with abnormal uric acid counts?

**证据**: (无)

**生成SQL**:
```sql
SELECT (SELECT COUNT(DISTINCT p.ID) FROM Patient p JOIN Laboratory l ON p.ID = l.ID WHERE p.SEX = 'M' AND l.UA <= 8.0) / (SELECT COUNT(DISTINCT p.ID) FROM Patient p JOIN Laboratory l ON p.ID = l.ID WHERE p.SEX = 'F' AND l.UA <= 6.5) AS male_to_female_ratio
```

**预期SQL**:
```sql
SELECT
  CAST(SUM(CASE WHEN `T2`.`UA` <= 8.0 AND `T1`.`SEX` = 'M' THEN 1 ELSE 0 END) AS DOUBLE) / SUM(CASE WHEN `T2`.`UA` <= 6.5 AND `T1`.`SEX` = 'F' THEN 1 ELSE 0 END)
FROM `Patient` AS `T1`
INNER JOIN `Laboratory` AS `T2`
  ON `T1`.`ID` = `T2`.`ID`
```

**生成结果**: [{'male_to_female_ratio': 0.184}]

**预期结果**: [{"CAST(SUM(CASE WHEN `T2`.`UA` <= 8.0 AND `T1`.`SEX` = 'M' THEN 1 ELSE 0 END) AS DOUBLE) / SUM(CASE WHEN `T2`.`UA` <= 6.5 AND `T1`.`SEX` = 'F' THEN 1 ELSE 0 END)": 0.20566810835419985}]

---

## 6. [ID:1171]

**问题**: How many underage patients were examined during the course of the three-year period from 1990 to 1993?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(DISTINCT Patient.ID) FROM Patient INNER JOIN Examination ON Patient.ID = Examination.ID WHERE YEAR(Patient.Birthday) < 18 AND YEAR(Examination.`Examination Date`) BETWEEN 1990 AND 1993
```

**预期SQL**:
```sql
SELECT
  COUNT(`T1`.`ID`)
FROM `Patient` AS `T1`
INNER JOIN `Examination` AS `T2`
  ON `T1`.`ID` = `T2`.`ID`
WHERE
  DATE_FORMAT(CAST(`T2`.`Examination Date` AS DATETIME), '%Y') BETWEEN '1990' AND '1993'
  AND DATE_FORMAT(CAST(`T2`.`Examination Date` AS DATETIME), '%Y') - DATE_FORMAT(CAST(`T1`.`Birthday` AS DATETIME), '%Y') < '18'
```

**生成结果**: [{'COUNT(DISTINCT Patient.ID)': 0}]

**预期结果**: [{'COUNT(`T1`.`ID`)': 1}]

---

## 7. [ID:1192]

**问题**: List all patients who were followed up at the outpatient clinic who underwent a laboratory test in October 1991 and had a total blood bilirubin level within the normal range.

**证据**: (无)

**生成SQL**:
```sql
SELECT DISTINCT p.ID FROM Patient p INNER JOIN Laboratory l ON p.ID = l.ID WHERE p.Admission = '-' AND l.Date LIKE '1991-10%' AND l.T-BIL < 2.0
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

**生成结果**: []

**预期结果**: [{'ID': 304157}, {'ID': 4466840}, {'ID': 4471732}] ... (+3行)

---

## 8. [ID:1232]

**问题**: Provide ID, sex and age of patient who has blood glucose (GLU) not within normal range but with total cholesterol(T-CHO) within normal range.

**证据**: (无)

**生成SQL**:
```sql
SELECT DISTINCT p.ID, p.SEX, TIMESTAMPDIFF(YEAR, p.Birthday, CURDATE()) AS age FROM Patient p INNER JOIN Laboratory l ON p.ID = l.ID WHERE l.GLU >= 180 AND l.T_CHO < 250
```

**预期SQL**:
```sql
SELECT DISTINCT
  `T1`.`ID`,
  `T1`.`SEX`,
  DATE_FORMAT(CAST(CURRENT_TIMESTAMP() AS DATETIME), '%Y') - DATE_FORMAT(CAST(`T1`.`Birthday` AS DATETIME), '%Y')
FROM `Patient` AS `T1`
INNER JOIN `Laboratory` AS `T2`
  ON `T1`.`ID` = `T2`.`ID`
WHERE
  `T2`.`GLU` >= 180 AND `T2`.`T-CHO` < 250
```

**生成结果**: []

**预期结果**: [{'ID': 57266, 'SEX': 'M', "DATE_FORMAT(CAST(CURRENT_TIMESTAMP() AS DATETIME), '%Y') - DATE_FORMAT(CAST(`T1`.`Birthday` AS DATETIME), '%Y')": 103.0}, {'ID': 2371753, 'SEX': 'F', "DATE_FORMAT(CAST(CURRENT_TIMESTAMP() AS DATETIME), '%Y') - DATE_FORMAT(CAST(`T1`.`Birthday` AS DATETIME), '%Y')": 94.0}, {'ID': 3354706, 'SEX': 'F', "DATE_FORMAT(CAST(CURRENT_TIMESTAMP() AS DATETIME), '%Y') - DATE_FORMAT(CAST(`T1`.`Birthday` AS DATETIME), '%Y')": 90.0}] ... (+10行)

---

## 9. [ID:1241]

**问题**: For patients with abnormal platelet level, state the number of patients with lower than normal range. How is it compare to the number of patients with higher than normal range?

**证据**: (无)

**生成SQL**:
```sql
SELECT (SELECT COUNT(DISTINCT ID) FROM Laboratory WHERE PLT < 100) AS lower_than_normal, (SELECT COUNT(DISTINCT ID) FROM Laboratory WHERE PLT > 400) AS higher_than_normal, (SELECT (SELECT COUNT(DISTINCT ID) FROM Laboratory WHERE PLT < 100) - (SELECT COUNT(DISTINCT ID) FROM Laboratory WHERE PLT > 400)) AS difference
```

**预期SQL**:
```sql
SELECT
  SUM(CASE WHEN `T2`.`PLT` <= 100 THEN 1 ELSE 0 END) - SUM(CASE WHEN `T2`.`PLT` >= 400 THEN 1 ELSE 0 END)
FROM `Patient` AS `T1`
INNER JOIN `Laboratory` AS `T2`
  ON `T1`.`ID` = `T2`.`ID`
```

**生成结果**: [{'lower_than_normal': 36, 'higher_than_normal': 82, 'difference': -46}]

**预期结果**: [{'SUM(CASE WHEN `T2`.`PLT` <= 100 THEN 1 ELSE 0 END) - SUM(CASE WHEN `T2`.`PLT` >= 400 THEN 1 ELSE 0 END)': -562.0}]

---

## 10. [ID:1242]

**问题**: For laboratory examinations take in 1984, list all patients below 50 years old with normal platelet level.

**证据**: (无)

**生成SQL**:
```sql
SELECT DISTINCT L.ID FROM Laboratory L INNER JOIN Patient P ON L.ID = P.ID WHERE YEAR(L.Date) = '1984' AND (YEAR(CURDATE()) - YEAR(P.Birthday)) < 50 AND L.PLT BETWEEN 100 AND 400
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

**生成结果**: [{'ID': 102490}, {'ID': 460574}, {'ID': 1086485}] ... (+2行)

**预期结果**: [{'ID': 30609}, {'ID': 48473}, {'ID': 52199}] ... (+73行)

---

## 11. [ID:1243]

**问题**: For all patients who are older than 55 years old, what is the percentage of female who has abnormal prothrombin time (PT)?

**证据**: (无)

**生成SQL**:
```sql
SELECT (SUM(CASE WHEN T2.SEX = 'F' AND T1.PT >= 14 THEN 1 ELSE 0 END) / SUM(CASE WHEN T1.PT >= 14 THEN 1 ELSE 0 END)) * 100 AS percentage FROM Laboratory T1 INNER JOIN Patient T2 ON T1.ID = T2.ID WHERE (YEAR(CURDATE()) - YEAR(T2.Birthday)) > 55
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

**生成结果**: [{'percentage': 78.3626}]

**预期结果**: [{"CAST(SUM(CASE WHEN `T2`.`PT` >= 14 AND `T1`.`SEX` = 'F' THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(CASE WHEN `T2`.`PT` >= 14 THEN 1 ELSE 0 END)": 1.2030885257676422}]

---

## 12. [ID:1247]

**问题**: Among the male patients who have a normal level of white blood cells, how many of them have an abnormal fibrinogen level?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(DISTINCT T1.ID) FROM Patient T1 INNER JOIN Laboratory T2 ON T1.ID = T2.ID WHERE T1.SEX = 'M' AND T2.WBC > 3.5 AND T2.WBC < 9.0 AND (T2.FG <= 150 OR T2.FG >= 450)
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

**生成结果**: [{'COUNT(DISTINCT T1.ID)': 6}]

**预期结果**: [{'COUNT(DISTINCT `T1`.`ID`)': 75}]

---

## 13. [ID:1270]

**问题**: Among the patients who has a normal anti-scl70, how many of them are female and does not have any symptom?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(DISTINCT P.ID) FROM Patient P WHERE P.SEX = 'F' AND P.ID NOT IN (SELECT DISTINCT ID FROM Examination WHERE Symptoms IS NOT NULL) AND P.ID IN (SELECT DISTINCT ID FROM Laboratory WHERE SC170 IN ('negative', '0'))
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
  (
    `T2`.`SC170` = 'negative' OR `T2`.`SC170` = '0'
  )
  AND `T1`.`SEX` = 'F'
  AND `T3`.`Symptoms` IS NULL
```

**生成结果**: [{'COUNT(DISTINCT P.ID)': 0}]

**预期结果**: [{'COUNT(DISTINCT `T1`.`ID`)': 2}]

---

## 14. [ID:1302]

**问题**: For the patients with a normal range of creatinine phosphokinase, how many of them have a positive measure of degree of coagulation?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(DISTINCT T1.ID) FROM Laboratory T1 INNER JOIN Examination T2 ON T1.ID = T2.ID WHERE T1.CPK < 250 AND (T2.KCT = '+' OR T2.RVVT = '+' OR T2.LAC = '+')
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

**生成结果**: [{'COUNT(DISTINCT T1.ID)': 1}]

**预期结果**: [{'COUNT(`T1`.`ID`)': 7}]

---

## 15. [ID:1028]

**问题**: In Scotland Premier League, which away team won the most during the 2010 season?

**证据**: (无)

**生成SQL**:
```sql
SELECT T2.team_long_name FROM Match T1 INNER JOIN League T3 ON T1.league_id = T3.id INNER JOIN Team T2 ON T1.away_team_api_id = T2.team_api_id WHERE T3.name = 'Scotland Premier League' AND T1.season = '2009/2010' AND T1.away_team_goal > T1.home_team_goal GROUP BY T2.team_long_name ORDER BY COUNT(*) DESC LIMIT 1
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

**生成结果**: []

**预期结果**: [{'team_long_name': 'Celtic'}]

---

## 16. [ID:1031]

**问题**: At present, calculate for the player's age who have a sprint speed of no less than 97 between 2013 to 2015.

**证据**: (无)

**生成SQL**:
```sql
SELECT DISTINCT p.id, p.player_name, TIMESTAMPDIFF(YEAR, p.birthday, CURDATE()) AS age FROM Player p INNER JOIN Player_Attributes pa ON p.player_api_id = pa.player_api_id WHERE pa.sprint_speed >= 97 AND YEAR(pa.date) BETWEEN 2013 AND 2015
```

**预期SQL**:
```sql
SELECT DISTINCT YEAR(CURDATE()) - YEAR(t2.birthday) AS age FROM Player_Attributes AS t1 INNER JOIN Player AS t2 ON t1.player_api_id = t2.player_api_id WHERE YEAR(t1.`date`) BETWEEN 2013 AND 2015 AND t1.sprint_speed >= 97
```

**生成结果**: [{'id': 7112, 'player_name': 'Mathis Bolly', 'age': 35}]

**预期结果**: [{'age': 36}]

---

## 17. [ID:1036]

**问题**: List the long name of teams with above-average build-up play passing in 2012.

**证据**: (无)

**生成SQL**:
```sql
SELECT DISTINCT T1.team_long_name FROM Team T1 INNER JOIN Team_Attributes T2 ON T1.team_api_id = T2.team_api_id WHERE strftime('%Y', T2.date) = '2012' AND T2.buildUpPlayPassing > (SELECT AVG(buildUpPlayPassing) FROM Team_Attributes WHERE strftime('%Y', date) = '2012' AND buildUpPlayPassing IS NOT NULL)
```

**预期SQL**:
```sql
SELECT DISTINCT
  `t4`.`team_long_name`
FROM `Team_Attributes` AS `t3`
INNER JOIN `Team` AS `t4`
  ON `t3`.`team_api_id` = `t4`.`team_api_id`
WHERE
  SUBSTR(`t3`.`date`, 1, 4) = '2012'
  AND `t3`.`buildUpPlayPassing` > (
    SELECT
      CAST(SUM(`t2`.`buildUpPlayPassing`) AS DOUBLE) / COUNT(`t1`.`id`)
    FROM `Team` AS `t1`
    INNER JOIN `Team_Attributes` AS `t2`
      ON `t1`.`team_api_id` = `t2`.`team_api_id`
    WHERE
      DATE_FORMAT(CAST(`t2`.`date` AS DATETIME), '%Y') = '2012'
  )
```

**生成结果**: []

**预期结果**: [{'team_long_name': 'Aberdeen'}, {'team_long_name': 'AC Ajaccio'}, {'team_long_name': 'Milan'}] ... (+125行)

---

## 18. [ID:1042]

**问题**: List the name of leagues in which the average goals by the home team is higher than the away team in the 2009/2010 season.

**证据**: (无)

**生成SQL**:
```sql
SELECT L.name FROM League L INNER JOIN Match M ON L.id = M.league_id WHERE M.season = '2009/2010' GROUP BY L.id, L.name HAVING AVG(M.home_team_goal) > AVG(M.away_team_goal)
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

**生成结果**: []

**预期结果**: [{'name': 'Belgium Jupiler League'}, {'name': 'England Premier League'}, {'name': 'France Ligue 1'}] ... (+8行)

---

## 19. [ID:1058]

**问题**: Who has the highest average finishing rate between the highest and shortest football player?

**证据**: (无)

**生成SQL**:
```sql
SELECT T1.player_name FROM Player T1 INNER JOIN Player_Attributes T2 ON T1.player_api_id = T2.player_api_id WHERE T1.height = (SELECT MAX(height) FROM Player) OR T1.height = (SELECT MIN(height) FROM Player) GROUP BY T1.player_name ORDER BY AVG(T2.finishing) DESC LIMIT 1
```

**预期SQL**:
```sql
SELECT `A` FROM (SELECT AVG(`finishing`) AS `result`, 'Max' AS `A` FROM `Player` AS `T1` INNER JOIN `Player_Attributes` AS `T2` ON `T1`.`player_api_id` = `T2`.`player_api_id` WHERE `T1`.`height` = (SELECT MAX(`height`) FROM `Player`) UNION SELECT AVG(`finishing`) AS `result`, 'Min' AS `A` FROM `Player` AS `T1` INNER JOIN `Player_Attributes` AS `T2` ON `T1`.`player_api_id` = `T2`.`player_api_id` WHERE `T1`.`height` = (SELECT MIN(`height`) FROM `Player`)) AS `derived` ORDER BY `result` DESC LIMIT 1
```

**生成结果**: [{'player_name': 'Juan Quero'}]

**预期结果**: [{'A': 'Min'}]

---

## 20. [ID:1084]

**问题**: Among the players born before the year 1986, how many of them would remain in his position and defense while the team attacked?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(DISTINCT p.id) FROM Player p INNER JOIN Player_Attributes pa ON p.player_api_id = pa.player_api_id WHERE strftime('%Y', p.birthday) < '1986' AND pa.defensive_work_rate = 'high'
```

**预期SQL**:
```sql
SELECT
  COUNT(DISTINCT `t1`.`player_name`)
FROM `Player` AS `t1`
INNER JOIN `Player_Attributes` AS `t2`
  ON `t1`.`player_api_id` = `t2`.`player_api_id`
WHERE
  DATE_FORMAT(CAST(`t1`.`birthday` AS DATETIME), '%Y') < '1986'
  AND `t2`.`defensive_work_rate` = 'high'
```

**生成结果**: []

**预期结果**: [{'COUNT(DISTINCT `t1`.`player_name`)': 892}]

---

## 21. [ID:1094]

**问题**: How much higher in percentage is Ariel Borysiuk's overall rating than that of Paulin Puel?

**证据**: (无)

**生成SQL**:
```sql
SELECT ((a.overall_rating - b.overall_rating) / b.overall_rating) * 100 AS percentage_difference FROM (SELECT overall_rating FROM Player_Attributes WHERE player_api_id = (SELECT player_api_id FROM Player WHERE player_name = 'Ariel Borysiuk') ORDER BY date DESC LIMIT 1) a, (SELECT overall_rating FROM Player_Attributes WHERE player_api_id = (SELECT player_api_id FROM Player WHERE player_name = 'Paulin Puel') ORDER BY date DESC LIMIT 1) b
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

**生成结果**: [{'percentage_difference': 15.2542}]

**预期结果**: [{"(\n    SUM(\n      CASE\n        WHEN `t1`.`player_name` = 'Ariel Borysiuk'\n        THEN `t2`.`overall_rating`\n        ELSE 0\n      END\n    ) * 1.0 - SUM(\n      CASE WHEN `t1`.`player_name` = 'Paulin Puel' THEN `t2`.`overall_rating` ELSE 0 END\n    )\n  ) * 10": 133.72607}]

---

## 22. [ID:1114]

**问题**: What was the average overall rating for Marko Arnautovic from 2007/2/22 to 2016/4/21?

**证据**: (无)

**生成SQL**:
```sql
SELECT AVG(overall_rating) FROM Player_Attributes WHERE player_api_id IN (SELECT player_api_id FROM Player WHERE player_name = 'Marko Arnautovic') AND date BETWEEN '2007-02-22' AND '2016-04-21'
```

**预期SQL**:
```sql
SELECT
  CAST(SUM(`t2`.`overall_rating`) AS DOUBLE) / COUNT(`t2`.`id`)
FROM `Player` AS `t1`
INNER JOIN `Player_Attributes` AS `t2`
  ON `t1`.`player_fifa_api_id` = `t2`.`player_fifa_api_id`
WHERE
  `t1`.`player_name` = 'Marko Arnautovic'
  AND SUBSTR(`t2`.`date`, 1, 10) BETWEEN '2007-02-22' AND '2016-04-21'
```

**生成结果**: [{'AVG(overall_rating)': 75.2813}]

**预期结果**: [{'CAST(SUM(`t2`.`overall_rating`) AS DOUBLE) / COUNT(`t2`.`id`)': 75.39393939393939}]

---

## 23. [ID:1139]

**问题**: What was the final score for the match on September 24, 2008, in the Belgian Jupiler League between the home team and the away team?

**证据**: (无)

**生成SQL**:
```sql
SELECT home_team_goal, away_team_goal FROM Match WHERE date LIKE '2008-09-24%' AND league_id = (SELECT id FROM League WHERE name = 'Belgium Jupiler League')
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

**生成结果**: []

**预期结果**: [{'home_team_goal': 1, 'away_team_goal': 1}]

---

## 24. [ID:896]

**问题**: Calculate the percentage whereby Hamilton was not at the 1st track of the the f1 circuit since 2010.

**证据**: (无)

**生成SQL**:
```sql
SELECT (COUNT(CASE WHEN r.position > 1 THEN 1 END) * 100.0 / COUNT(*)) AS percentage FROM results AS r INNER JOIN drivers AS d ON r.driverId = d.driverId INNER JOIN races AS ra ON r.raceId = ra.raceId WHERE d.surname = 'Hamilton' AND ra.year >= 2010
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

**生成结果**: [{'percentage': 54.22535}]

**预期结果**: [{'CAST(COUNT(CASE WHEN `T2`.`position` <> 1 THEN `T2`.`position` END) AS DOUBLE) * 100 / COUNT(`T2`.`driverStandingsId`)': 73.2394366197183}]

---

## 25. [ID:962]

**问题**: From 2000 to 2005, what percentage of drivers who were born before 1985 and the lap numbers were over 50?

**证据**: (无)

**生成SQL**:
```sql
SELECT (COUNT(DISTINCT d.driverId) * 100.0 / (SELECT COUNT(DISTINCT d.driverId) FROM drivers d INNER JOIN results r ON d.driverId = r.driverId INNER JOIN races ra ON r.raceId = ra.raceId WHERE ra.year BETWEEN 2000 AND 2005)) AS percentage FROM drivers d INNER JOIN results r ON d.driverId = r.driverId INNER JOIN races ra ON r.raceId = ra.raceId WHERE ra.year BETWEEN 2000 AND 2005 AND YEAR(d.dob) < 1985 AND r.laps > 50
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

**生成结果**: [{'percentage': 100.0}]

**预期结果**: [{"CAST(SUM(\n    CASE\n      WHEN DATE_FORMAT(CAST(`T3`.`dob` AS DATETIME), '%Y') < '1985' AND `T1`.`laps` > 50\n      THEN 1\n      ELSE 0\n    END\n  ) AS DOUBLE) * 100 / COUNT(*)": 64.88474742520843}]

---

## 26. [ID:994]

**问题**: Which constructor scored most points from Monaco Grand Prix between 1980 and 2010? List the score, name and nationality of this team.

**证据**: (无)

**生成SQL**:
```sql
SELECT c.name, c.nationality, SUM(cs.points) AS total_points FROM constructorStandings cs JOIN constructors c ON cs.constructorId = c.constructorId JOIN races r ON cs.raceId = r.raceId WHERE r.name = 'Monaco Grand Prix' AND r.year BETWEEN 1980 AND 2010 GROUP BY c.constructorId, c.name, c.nationality ORDER BY total_points DESC LIMIT 1
```

**预期SQL**:
```sql
SELECT
  SUM(`T1`.`points`),
  `T2`.`name`,
  `T2`.`nationality`
FROM `constructorResults` AS `T1`
INNER JOIN `constructors` AS `T2`
  ON `T1`.`constructorId` = `T2`.`constructorId`
INNER JOIN `races` AS `T3`
  ON `T3`.`raceid` = `T1`.`raceid`
WHERE
  `T3`.`name` = 'Monaco Grand Prix' AND `T3`.`year` BETWEEN 1980 AND 2010
GROUP BY
  `T2`.`name`
ORDER BY
  SUM(`T1`.`points`) DESC
LIMIT 1
```

**生成结果**: [{'name': 'McLaren', 'nationality': 'British', 'total_points': 1145.5}]

**预期结果**: [{'SUM(`T1`.`points`)': 218.5, 'name': 'McLaren', 'nationality': 'British'}]

---

## 27. [ID:1011]

**问题**: Which top 20 driver created the shortest lap time ever record in a Formula_1 race? Please give them full names.

**证据**: (无)

**生成SQL**:
```sql
SELECT d.forename, d.surname FROM lapTimes l INNER JOIN drivers d ON l.driverId = d.driverId GROUP BY l.driverId, d.forename, d.surname ORDER BY MIN(l.time) ASC LIMIT 20
```

**预期SQL**:
```sql
WITH lap_times_in_seconds AS (SELECT driverId, (CASE WHEN SUBSTR(time, 1, INSTR(time, ':') - 1) <> '' THEN CAST(SUBSTR(time, 1, INSTR(time, ':') - 1) AS FLOAT) * 60 ELSE 0 END + CASE WHEN SUBSTR(time, INSTR(time, ':') + 1, INSTR(time, '.') - INSTR(time, ':') - 1) <> '' THEN CAST(SUBSTR(time, INSTR(time, ':') + 1, INSTR(time, '.') - INSTR(time, ':') - 1) AS FLOAT) ELSE 0 END + CASE WHEN SUBSTR(time, INSTR(time, '.') + 1) <> '' THEN CAST(SUBSTR(time, INSTR(time, '.') + 1) AS FLOAT) / 1000 ELSE 0 END) AS time_in_seconds FROM lapTimes) SELECT T2.forename, T2.surname, T1.driverId FROM (SELECT driverId, MIN(time_in_seconds) AS min_time_in_seconds FROM lap_times_in_seconds GROUP BY driverId) AS T1 INNER JOIN drivers AS T2 ON T1.driverId = T2.driverId ORDER BY T1.min_time_in_seconds ASC LIMIT 20
```

**生成结果**: [{'forename': 'Jean-Éric', 'surname': 'Vergne'}, {'forename': 'Romain', 'surname': 'Grosjean'}, {'forename': 'Marcus', 'surname': 'Ericsson'}] ... (+17行)

**预期结果**: [{'forename': 'Nico', 'surname': 'Hülkenberg', 'driverId': 807}, {'forename': 'Daniel', 'surname': 'Ricciardo', 'driverId': 817}, {'forename': 'Adrian', 'surname': 'Sutil', 'driverId': 16}] ... (+17行)

---

## 28. [ID:1014]

**问题**: Please list the lap records for the circuits in Italy.

**证据**: (无)

**生成SQL**:
```sql
SELECT l.raceId, l.driverId, l.lap, l.time, l.milliseconds FROM lapTimes l INNER JOIN races r ON l.raceId = r.raceId INNER JOIN circuits c ON r.circuitId = c.circuitId WHERE c.country = 'Italy' AND l.time = (SELECT MIN(l2.time) FROM lapTimes l2 WHERE l2.raceId = l.raceId AND l2.lap = l.lap) ORDER BY l.raceId, l.lap
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
    NOT `T1`.`FastestLapTime` IS NULL
)
SELECT
  `T1`.`FastestLapTime` AS `lap_record`
FROM `results` AS `T1`
INNER JOIN `races` AS `T2`
  ON `T1`.`raceId` = `T2`.`raceId`
INNER JOIN `circuits` AS `T3`
  ON `T2`.`circuitId` = `T3`.`circuitId`
INNER JOIN (
  SELECT
    MIN(`fastest_lap_times`.`time_in_seconds`) AS `min_time_in_seconds`
  FROM `fastest_lap_times`
  INNER JOIN `races` AS `T2`
    ON `fastest_lap_times`.`raceId` = `T2`.`raceId`
  INNER JOIN `circuits` AS `T3`
    ON `T2`.`circuitId` = `T3`.`circuitId`
  WHERE
    `T3`.`country` = 'Italy'
) AS `T4`
  ON (
    CAST(SUBSTR(`T1`.`FastestLapTime`, 1, INSTR(`T1`.`FastestLapTime`, ':') - 1) AS DOUBLE) * 60
  ) + (
    CAST(SUBSTR(
      `T1`.`FastestLapTime`,
      INSTR(`T1`.`FastestLapTime`, ':') + 1,
      INSTR(`T1`.`FastestLapTime`, '.') - INSTR(`T1`.`FastestLapTime`, ':') - 1
    ) AS DOUBLE)
  ) + (
    CAST(SUBSTR(`T1`.`FastestLapTime`, INSTR(`T1`.`FastestLapTime`, '.') + 1) AS DOUBLE) / 1000
  ) = `T4`.`min_time_in_seconds`
LIMIT 1
```

**生成结果**: []

**预期结果**: [{'lap_record': '1:20.411'}]

---

## 29. [ID:743]

**问题**: What is the percentage of superheroes who act in their own self-interest or make decisions based on their own moral code? Indicate how many of the said superheroes were published by Marvel Comics.

**证据**: (无)

**生成SQL**:
```sql
SELECT (COUNT(CASE WHEN a.alignment = 'Bad' THEN 1 END) * 100.0 / COUNT(s.id)) AS percentage, COUNT(CASE WHEN a.alignment = 'Bad' AND p.publisher_name = 'Marvel Comics' THEN 1 END) AS marvel_count FROM superhero s INNER JOIN alignment a ON s.alignment_id = a.id LEFT JOIN publisher p ON s.publisher_id = p.id
```

**预期SQL**:
```sql
SELECT
  (
    CAST(COUNT(*) AS DOUBLE) * 100 / (
      SELECT
        COUNT(*)
      FROM `superhero`
    )
  ),
  CAST(SUM(CASE WHEN `T2`.`publisher_name` = 'Marvel Comics' THEN 1 ELSE 0 END) AS DOUBLE)
FROM `superhero` AS `T1`
INNER JOIN `publisher` AS `T2`
  ON `T1`.`publisher_id` = `T2`.`id`
INNER JOIN `alignment` AS `T3`
  ON `T3`.`id` = `T1`.`alignment_id`
WHERE
  `T3`.`alignment` = 'Bad'
```

**生成结果**: [{'percentage': 28.49462, 'marvel_count': 118}]

**预期结果**: [{'(\n    CAST(COUNT(*) AS DOUBLE) * 100 / (\n      SELECT\n        COUNT(*)\n      FROM `superhero`\n    )\n  )': 28.266666666666666, "CAST(SUM(CASE WHEN `T2`.`publisher_name` = 'Marvel Comics' THEN 1 ELSE 0 END) AS DOUBLE)": 118.0}]

---

## 30. [ID:772]

**问题**: List the eyes, hair and skin colour of all female superheroes published by Dark Horse Comics.

**证据**: (无)

**生成SQL**:
```sql
SELECT c1.colour AS eye_colour, c2.colour AS hair_colour, c3.colour AS skin_colour FROM superhero s INNER JOIN gender g ON s.gender_id = g.id INNER JOIN publisher p ON s.publisher_id = p.id INNER JOIN colour c1 ON s.eye_colour_id = c1.id INNER JOIN colour c2 ON s.hair_colour_id = c2.id INNER JOIN colour c3 ON s.skin_colour_id = c3.id WHERE g.gender = 'Female' AND p.publisher_name = 'Dark Horse Comics'
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

**生成结果**: [{'eye_colour': 'Green', 'hair_colour': 'Blond', 'skin_colour': 'No Colour'}, {'eye_colour': 'Brown', 'hair_colour': 'Brown', 'skin_colour': 'No Colour'}, {'eye_colour': 'No Colour', 'hair_colour': 'No Colour', 'skin_colour': 'No Colour'}] ... (+2行)

**预期结果**: [{'eye_colour_id': 14, 'hair_colour_id': 6, 'skin_colour_id': 1}, {'eye_colour_id': 9, 'hair_colour_id': 9, 'skin_colour_id': 1}, {'eye_colour_id': 1, 'hair_colour_id': 1, 'skin_colour_id': 1}] ... (+2行)

---

## 31. [ID:586]

**问题**: Which user added a bounty amount of 50 to the post title mentioning variance?

**证据**: (无)

**生成SQL**:
```sql
SELECT DISTINCT u.DisplayName FROM votes v INNER JOIN posts p ON v.PostId = p.Id INNER JOIN users u ON v.UserId = u.Id WHERE v.BountyAmount = 50 AND p.Title LIKE '%variance%'
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

**生成结果**: [{'DisplayName': 'chl'}, {'DisplayName': 'shabbychef'}]

**预期结果**: [{'DisplayName': 'chl', 'Title': 'How to combine confidence intervals for a variance component of a mixed-effects model when using multiple imputation'}, {'DisplayName': 'shabbychef', 'Title': 'Unbiased estimation of covariance matrix for multiply censored data'}]

---

## 32. [ID:634]

**问题**: Among posts by Harvey Motulsky and Noah Snyder, which one has higher popularity?

**证据**: (无)

**生成SQL**:
```sql
SELECT p.Id, p.Title, p.ViewCount FROM posts p INNER JOIN users u ON p.OwnerUserId = u.Id WHERE u.DisplayName IN ('Harvey Motulsky', 'Noah Snyder') ORDER BY p.ViewCount DESC LIMIT 1
```

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

**生成结果**: [{'Id': 109, 'Title': "Power of Holm's multiple comparison testing compared to others", 'ViewCount': 3980}]

**预期结果**: [{'DisplayName': 'Harvey Motulsky'}]

---

## 33. [ID:639]

**问题**: Based on posts posted by Community, calculate the percentage of posts that use the R language.

**证据**: (无)

**生成SQL**:
```sql
SELECT (COUNT(CASE WHEN t.TagName = 'r' THEN p.Id END) * 100.0 / COUNT(p.Id)) AS percentage FROM posts p INNER JOIN tags t ON p.Id = t.Id WHERE p.OwnerDisplayName = 'Community'
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

**生成结果**: [{'percentage': None}]

**预期结果**: [{"CAST(SUM(CASE WHEN `T3`.`TagName` = 'r' THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(`T1`.`Id`)": 0.19607843137254902}]

---

## 34. [ID:371]

**问题**: What is the percentage of cards whose language is French among the Story Spotlight cards?

**证据**: (无)

**生成SQL**:
```sql
SELECT (COUNT(CASE WHEN f.language = 'French' THEN 1 END) * 100.0 / COUNT(c.id)) AS percentage FROM cards c LEFT JOIN foreign_data f ON c.uuid = f.uuid WHERE c.isStorySpotlight = 1
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

**生成结果**: [{'percentage': 9.80834}]

**预期结果**: [{"CAST(SUM(CASE WHEN `T2`.`language` = 'French' THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(`T1`.`id`)": 10.0}]

---

## 35. [ID:416]

**问题**: What percentage of cards without power are in French?

**证据**: (无)

**生成SQL**:
```sql
SELECT (COUNT(CASE WHEN f.language = 'French' AND (c.power IS NULL OR c.power = '*') THEN 1 END) * 100.0 / COUNT(CASE WHEN c.power IS NULL OR c.power = '*' THEN 1 END)) AS percentage FROM cards c LEFT JOIN foreign_data f ON c.uuid = f.uuid
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

**生成结果**: [{'percentage': 11.58289}]

**预期结果**: [{"CAST(SUM(CASE WHEN `T2`.`language` = 'French' THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(`T1`.`id`)": 12.975290140452374}]

---

## 36. [ID:487]

**问题**: What is the percentage of incredibly powerful cards in the set Coldsnap?

**证据**: (无)

**生成SQL**:
```sql
SELECT (SUM(CASE WHEN cardKingdomFoilId IS NOT NULL AND cardKingdomId IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*)) * 100 AS percentage FROM cards WHERE setCode = 'Coldsnap'
```

**预期SQL**:
```sql
SELECT
  CAST(SUM(
    CASE
      WHEN NOT `T1`.`cardKingdomFoilId` IS NULL AND NOT `T1`.`cardKingdomId` IS NULL
      THEN 1
      ELSE 0
    END
  ) AS DOUBLE) * 100 / COUNT(`T1`.`id`)
FROM `cards` AS `T1`
INNER JOIN `sets` AS `T2`
  ON `T2`.`code` = `T1`.`setCode`
WHERE
  `T2`.`name` = 'Coldsnap'
```

**生成结果**: [{'percentage': None}]

**预期结果**: [{'CAST(SUM(\n    CASE\n      WHEN NOT `T1`.`cardKingdomFoilId` IS NULL AND NOT `T1`.`cardKingdomId` IS NULL\n      THEN 1\n      ELSE 0\n    END\n  ) AS DOUBLE) * 100 / COUNT(`T1`.`id`)': 100.0}]

---

## 37. [ID:198]

**问题**: On average how many carcinogenic molecules are single bonded?

**证据**: (无)

**生成SQL**:
```sql
SELECT AVG(bond_count) FROM (SELECT COUNT(*) AS bond_count FROM molecule m JOIN bond b ON m.molecule_id = b.molecule_id WHERE m.label = '+' AND b.bond_type = '-' GROUP BY m.molecule_id) AS subquery
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

**生成结果**: [{'AVG(bond_count)': 20.25}]

**预期结果**: [{'AVG(`single_bond_count`)': 732.125}]

---

## 38. [ID:207]

**问题**: What elements are in a double type bond?

**证据**: (无)

**生成SQL**:
```sql
SELECT DISTINCT atom.element FROM atom INNER JOIN bond ON atom.molecule_id = bond.molecule_id WHERE bond.bond_type = '='
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

**生成结果**: [{'element': 'c'}, {'element': 'o'}, {'element': 'cl'}] ... (+13行)

**预期结果**: [{'element': 'c'}, {'element': 'o'}, {'element': 'cl'}] ... (+10行)

---

## 39. [ID:212]

**问题**: Which element is the least numerous in non-carcinogenic molecules?

**证据**: (无)

**生成SQL**:
```sql
SELECT element FROM atom WHERE molecule_id IN (SELECT molecule_id FROM molecule WHERE label = '-') GROUP BY element ORDER BY COUNT(*) ASC LIMIT 1
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

**生成结果**: [{'element': 'k'}]

**预期结果**: []

---

## 40. [ID:215]

**问题**: How many atoms with iodine and with sulfur type elements are there in single bond molecules?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(DISTINCT atom_id) FROM atom WHERE element IN ('i', 's') AND molecule_id IN (SELECT DISTINCT molecule_id FROM bond WHERE bond_type = '-')
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

**生成结果**: [{'COUNT(DISTINCT atom_id)': 97}]

**预期结果**: [{'iodine_nums': 3, 'sulfur_nums': 77}]

---

## 41. [ID:218]

**问题**: What percentage of carcinogenic-type molecules does not contain fluorine?

**证据**: (无)

**生成SQL**:
```sql
SELECT (SUM(CASE WHEN a.element = 'f' THEN 1 ELSE 0 END) * 100.0 / COUNT(DISTINCT m.molecule_id)) AS percentage FROM molecule m LEFT JOIN atom a ON m.molecule_id = a.molecule_id WHERE m.label = '+'
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

**生成结果**: [{'percentage': 2.63158}]

**预期结果**: [{"CAST(COUNT(DISTINCT CASE WHEN `T1`.`element` <> 'f' THEN `T2`.`molecule_id` ELSE NULL END) AS DOUBLE) * 100 / COUNT(DISTINCT `T2`.`molecule_id`)": 100.0}]

---

## 42. [ID:219]

**问题**: What is the percentage of carcinogenic molecules in triple type bonds?

**证据**: (无)

**生成SQL**:
```sql
SELECT (SUM(CASE WHEN b.bond_type = '#' THEN 1 ELSE 0 END) * 100.0 / COUNT(b.bond_id)) AS percentage FROM bond b INNER JOIN molecule m ON b.molecule_id = m.molecule_id WHERE m.label = '+'
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

**生成结果**: [{'percentage': 0.08075}]

**预期结果**: [{"CAST(COUNT(DISTINCT CASE WHEN `T2`.`label` = '+' THEN `T2`.`molecule_id` ELSE NULL END) AS DOUBLE) * 100 / COUNT(DISTINCT `T2`.`molecule_id`)": 66.66666666666667}]

---

## 43. [ID:230]

**问题**: What are the elements of the toxicology and label of molecule TR060?

**证据**: (无)

**生成SQL**:
```sql
SELECT a.element, m.label FROM atom a JOIN molecule m ON a.molecule_id = m.molecule_id WHERE m.molecule_id = 'TR060'
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

**生成结果**: [{'element': 'c', 'label': '-'}, {'element': 'c', 'label': '-'}, {'element': 'h', 'label': '-'}] ... (+100行)

**预期结果**: [{'element': 'c', 'label': '-'}, {'element': 'h', 'label': '-'}, {'element': 'o', 'label': '-'}] ... (+2行)

---

## 44. [ID:231]

**问题**: Which bond type accounted for the majority of the bonds found in molecule TR010 and state whether or not this molecule is carcinogenic?

**证据**: (无)

**生成SQL**:
```sql
SELECT b.bond_type, m.label FROM bond b INNER JOIN molecule m ON b.molecule_id = m.molecule_id WHERE b.molecule_id = 'TR010' GROUP BY b.bond_type, m.label ORDER BY COUNT(*) DESC LIMIT 1
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

**生成结果**: [{'bond_type': '-', 'label': '-'}]

**预期结果**: [{'bond_type': '-'}]

---

## 45. [ID:240]

**问题**: List all the elements of the toxicology of the molecule "TR004".

**证据**: (无)

**生成SQL**:
```sql
SELECT element FROM atom WHERE molecule_id = 'TR004'
```

**预期SQL**:
```sql
SELECT DISTINCT
  `T`.`element`
FROM `atom` AS `T`
WHERE
  `T`.`molecule_id` = 'TR004'
```

**生成结果**: [{'element': 's'}, {'element': 'n'}, {'element': 'o'}] ... (+21行)

**预期结果**: [{'element': 's'}, {'element': 'n'}, {'element': 'o'}] ... (+3行)

---

## 46. [ID:247]

**问题**: List all the elements of atoms that can not bond with any other atoms.

**证据**: (无)

**生成SQL**:
```sql
SELECT DISTINCT atom.element FROM atom WHERE atom.atom_id NOT IN (SELECT atom_id FROM connected) AND atom.atom_id NOT IN (SELECT atom_id2 FROM connected)
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

**生成结果**: [{'element': 'na'}, {'element': 'cl'}, {'element': 'h'}] ... (+2行)

**预期结果**: [{'element': 'na'}, {'element': 'zn'}, {'element': 'k'}]

---

## 47. [ID:281]

**问题**: Tally the toxicology element of the 4th atom of each molecule that was carcinogenic.

**证据**: (无)

**生成SQL**:
```sql
SELECT atom.element FROM atom INNER JOIN molecule ON atom.molecule_id = molecule.molecule_id WHERE molecule.label = '+' AND SUBSTRING(atom.atom_id, 7, 1) = '4'
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

**生成结果**: [{'element': 'cl'}, {'element': 'c'}, {'element': 'c'}] ... (+266行)

**预期结果**: [{'element': 'cl'}, {'element': 'c'}, {'element': 'br'}] ... (+5行)

---

## 48. [ID:28]

**问题**: Consider the average difference between K-12 enrollment and 15-17 enrollment of schools that are locally funded, list the names and DOC type of schools which has a difference above this average.

**证据**: (无)

**生成SQL**:
```sql
SELECT T1.School Name, T1.DOCType FROM frpm T1 INNER JOIN schools T2 ON T1.CDSCode = T2.CDSCode WHERE T2.FundingType = 'Locally funded' AND (T1.`Enrollment (K-12)` - T1.`Enrollment (Ages 5-17)`) > (SELECT AVG(T3.`Enrollment (K-12)` - T3.`Enrollment (Ages 5-17)`) FROM frpm T3 INNER JOIN schools T4 ON T3.CDSCode = T4.CDSCode WHERE T4.FundingType = 'Locally funded')
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

**生成结果**: []

**预期结果**: [{'School': 'Mountain Oaks', 'DOC': '00'}, {'School': 'Castle Rock', 'DOC': '00'}, {'School': 'Charter Community School Home Study Academy', 'DOC': '00'}] ... (+54行)

---

## 49. [ID:36]

**问题**: Under whose administration is the school with the highest number of students scoring 1500 or more on the SAT? Indicate their full names.

**证据**: (无)

**生成SQL**:
```sql
SELECT s.AdmFName1, s.AdmLName1 FROM satscores t1 INNER JOIN schools s ON t1.cds = s.CDSCode WHERE t1.NumGE1500 = (SELECT MAX(NumGE1500) FROM satscores)
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

**生成结果**: [{'AdmFName1': 'Michelle', 'AdmLName1': 'King'}]

**预期结果**: [{'AdmFName1': 'Michelle', 'AdmLName1': 'King', 'AdmFName2': None, 'AdmLName2': None, 'AdmFName3': None, 'AdmLName3': None}]

---

## 50. [ID:83]

**问题**: Of the schools that offers a magnet program serving a grade span of Kindergarten to 8th grade, how many offers Multiple Provision Types? List the number of cities that offers a Kindergarten to 8th grade span and indicate how many schools are there serving such grade span for each city.

**证据**: (无)

**生成SQL**:
```sql
SELECT s.City, COUNT(s.CDSCode) AS school_count FROM schools s INNER JOIN frpm f ON s.CDSCode = f.CDSCode WHERE s.Magnet = 1 AND f.GSserved = 'K-8' AND f.`NSLP Provision Status` = 'Multiple Provision Types' GROUP BY s.City
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

**生成结果**: []

**预期结果**: [{'City': 'Adelanto', 'COUNT(`T2`.`CDSCode`)': 1}]

---

## 51. [ID:87]

**问题**: What are the valid e-mail addresses of the administrator of the school located in the San Bernardino county, City of San Bernardino City Unified that opened between 1/1/2009 to 12/31/2010 whose school types are public Intermediate/Middle Schools and Unified Schools?

**证据**: (无)

**生成SQL**:
```sql
SELECT DISTINCT AdmEmail1, AdmEmail2, AdmEmail3 FROM schools WHERE County = 'San Bernardino' AND District = 'San Bernardino City Unified' AND OpenDate BETWEEN '2009-01-01' AND '2010-12-31' AND (SOC = '62' OR DOC = '54') AND AdmEmail1 IS NOT NULL
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

**生成结果**: [{'AdmEmail1': 'a.lucero@realjourney.org', 'AdmEmail2': 'j.hernandez@realjourney.org', 'AdmEmail3': None}, {'AdmEmail1': 'jfranco@ofy.org', 'AdmEmail2': 'bgillespie@ofy.org', 'AdmEmail3': None}, {'AdmEmail1': 'a.lucero@realjourney.org', 'AdmEmail2': 'a.ramirez@realjourney.org', 'AdmEmail3': None}] ... (+1行)

**预期结果**: [{'AdmEmail1': 'a.lucero@realjourney.org', 'AdmEmail2': 'j.hernandez@realjourney.org'}]

---

## 52. [ID:94]

**问题**: List out the account numbers of female clients who are oldest and has lowest average salary, calculate the gap between this lowest average salary with the highest average salary?

**证据**: (无)

**生成SQL**:
```sql
SELECT account.account_id FROM client INNER JOIN disp ON client.client_id = disp.client_id INNER JOIN account ON disp.account_id = account.account_id INNER JOIN district ON account.district_id = district.district_id WHERE client.gender = 'F' AND client.birth_date = (SELECT MIN(birth_date) FROM client WHERE gender = 'F') AND district.A11 = (SELECT MIN(A11) FROM district) ORDER BY account.account_id
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

**生成结果**: []

**预期结果**: [{'account_id': 6, '(\n    SELECT\n      MAX(`A11`) - MIN(`A11`)\n    FROM `district`\n  )': 4431}]

---

## 53. [ID:125]

**问题**: For loans contracts which are still running where client are in debt, list the district of the and the state the percentage unemployment rate increment from year 1995 to 1996.

**证据**: (无)

**生成SQL**:
```sql
SELECT d.A2 AS district, d.A3 AS state, ((d.A13 - d.A12) / d.A12) * 100 AS unemployment_increment_percentage FROM district d INNER JOIN account a ON d.district_id = a.district_id INNER JOIN loan l ON a.account_id = l.account_id WHERE l.status = 'D'
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

**生成结果**: [{'district': 'Strakonice', 'state': 'south Bohemia', 'unemployment_increment_percentage': 40.0}, {'district': 'Chrudim', 'state': 'east Bohemia', 'unemployment_increment_percentage': 39.259259259259245}, {'district': 'Hl.m. Praha', 'state': 'Prague', 'unemployment_increment_percentage': 114.99999999999999}] ... (+42行)

**预期结果**: [{'CAST((\n    `T3`.`A13` - `T3`.`A12`\n  ) AS DOUBLE) * 100 / `T3`.`A12`': 40.0}, {'CAST((\n    `T3`.`A13` - `T3`.`A12`\n  ) AS DOUBLE) * 100 / `T3`.`A12`': 39.25925925925924}, {'CAST((\n    `T3`.`A13` - `T3`.`A12`\n  ) AS DOUBLE) * 100 / `T3`.`A12`': 115.0}] ... (+42行)

---

## 54. [ID:149]

**问题**: Please list the account types that are not eligible for loans, and the average income of residents in the district where the account is located exceeds $8000 but is no more than $9000.

**证据**: (无)

**生成SQL**:
```sql
SELECT DISTINCT account.frequency FROM account INNER JOIN district ON account.district_id = district.district_id WHERE account.frequency NOT IN (SELECT DISTINCT account.frequency FROM account INNER JOIN loan ON account.account_id = loan.account_id WHERE account.frequency = 'OWNER') AND district.A11 > 8000 AND district.A11 <= 9000
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

**生成结果**: [{'frequency': 'POPLATEK MESICNE'}, {'frequency': 'POPLATEK PO OBRATU'}, {'frequency': 'POPLATEK TYDNE'}]

**预期结果**: [{'type': 'DISPONENT'}, {'type': 'DISPONENT'}, {'type': 'DISPONENT'}] ... (+458行)

---

## 55. [ID:169]

**问题**: What was the growth rate of the total amount of loans across all accounts for a male client between 1996 and 1997?

**证据**: (无)

**生成SQL**:
```sql
SELECT ((SUM(CASE WHEN YEAR(l.date) = 1997 THEN l.amount ELSE 0 END) - SUM(CASE WHEN YEAR(l.date) = 1996 THEN l.amount ELSE 0 END)) / SUM(CASE WHEN YEAR(l.date) = 1996 THEN l.amount ELSE 0 END)) * 100 AS growth_rate FROM loan l INNER JOIN disp d ON l.account_id = d.account_id INNER JOIN client c ON d.client_id = c.client_id WHERE c.gender = 'M' AND l.date BETWEEN '1996-01-01' AND '1997-12-31'
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
  ON `T3`.`account_id` = `T2`.`account_id`
INNER JOIN `client` AS `T4`
  ON `T4`.`client_id` = `T3`.`client_id`
WHERE
  `T4`.`gender` = 'M' AND `T3`.`type` = 'OWNER'
```

**生成结果**: [{'growth_rate': 25.362}]

**预期结果**: [{"CAST((\n    SUM(\n      CASE\n        WHEN DATE_FORMAT(CAST(`T1`.`date` AS DATETIME), '%Y') = '1997'\n        THEN `T1`.`amount`\n        ELSE 0\n      END\n    ) - SUM(\n      CASE\n        WHEN DATE_FORMAT(CAST(`T1`.`date` AS DATETIME), '%Y') = '1996'\n        TH": 25.300191222790616}]

---

## 56. [ID:173]

**问题**: How often does account number 3 request an account statement to be released? What was the aim of debiting 3539 in total?

**证据**: (无)

**生成SQL**:
```sql
SELECT COUNT(*) AS statement_requests FROM `order` WHERE account_id = 3 AND k_symbol = 'UROK'; SELECT SUM(amount) AS total_debit FROM `order` WHERE account_id = 3 AND k_symbol = 'UROK';
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

**生成结果**: []

**预期结果**: [{'frequency': 'POPLATEK MESICNE', 'k_symbol': 'POJISTNE'}]

---


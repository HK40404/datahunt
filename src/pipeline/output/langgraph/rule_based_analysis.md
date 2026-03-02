# SQL 生成错误分析报告
**生成时间**: 2026-01-19T01:25:59.291109
**总失败数**: 64

## 按难度统计

| 难度 | 失败数 |
|------|--------|
| simple | 64 |
| moderate | 0 |
| challenging | 0 |

## 错误类型统计

| 错误类型 | 数量 | 占比 |
|----------|------|------|
| JOIN漏表 | 19 | 29.7% |
| 其他 | 19 | 29.7% |
| DISTINCT缺失 | 6 | 9.4% |
| 聚合函数差异 | 5 | 7.8% |
| JOIN多表 | 4 | 6.2% |
| LIKE误用 | 3 | 4.7% |
| GROUP BY多余 | 2 | 3.1% |
| 等号误用 | 2 | 3.1% |
| GROUP BY缺失 | 1 | 1.6% |
| 排序方向错误 | 1 | 1.6% |
| WHERE条件缺失 | 1 | 1.6% |
| LIMIT缺失 | 1 | 1.6% |

## 典型案例

### JOIN漏表

**问题 #1500** (simple)
- Please list the product description of the products consumed in September, 2013.

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

---

### 其他

**问题 #1505** (simple)
- Among the customers who paid in euro, how many of them have a monthly consumption of over 1000?

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

---

### DISTINCT缺失

**问题 #1035** (simple)
- Give the team_fifa_api_id of teams with more than 50 but less than 60 build-up play speed.

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

---

### 聚合函数差异

**问题 #1525** (simple)
- What is the percentage of the customers who used EUR in 2012/8/25?

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

---

### JOIN多表

**问题 #1144** (simple)
- Please state the finishing rate and curve score of the player who has the heaviest weight.

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

---

### LIKE误用

**问题 #1198** (simple)
- How many female patients were given an APS diagnosis?

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

---

### GROUP BY多余

**问题 #1410** (simple)
- List out the full name and total cost that member id "rec4BLdZHS2Blfp4v" incurred?

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

---

### 等号误用

**问题 #861** (simple)
- What is his number of the driver who finished 0:01:54 in the Q3 of qualifying race No.903?

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

---

### GROUP BY缺失

**问题 #1498** (simple)
- What is the highest monthly consumption in the year 2012?

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

---

### 排序方向错误

**问题 #1078** (simple)
- Which player is older, Aaron Lennon or Abdelaziz Barrada?

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

---

### WHERE条件缺失

**问题 #915** (simple)
- Which country is the oldest driver from?

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

---

### LIMIT缺失

**问题 #82** (simple)
- What is the grade span offered in the school with the highest longitude?

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

---

## 改进建议

### 高优先级
1. **JOIN漏表**: 增强Schema Linking的多表关联推理
2. **WHERE条件**: 确保WHERE子句覆盖所有筛选条件
3. **数值计算**: 百分比/比率问题需明确分母

### 中优先级
4. **DISTINCT**: 列表查询添加去重
5. **GROUP BY**: 聚合查询必须包含GROUP BY
6. **LIMIT**: TOP N查询必须包含LIMIT


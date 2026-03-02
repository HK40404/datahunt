# datahunt

```text
[START]
   |
   v
[Query Rewrite] -> [Schema Link] -> [SQL Generate] -> [SQL Validate] -> [SQL Execute] -> [END]
                                                            |                 |
                                                            v                 v
                                                        [SQL Fix] <-----------+
                                                            |
                                                            +-> [END]
                                                            |
                                                            +-> [SQL Validate]

```

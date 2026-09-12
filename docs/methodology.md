# Methodology

The application analyzes the included player-level CSV. Cleaning imputes selected demographic fields and splits records by positive versus zero/missing purchase amount. Missing amounts are grouped with non-paying records by the current implementation; this is an assumption, not confirmed behavior.

Revenue share is segment revenue divided by total observed revenue. Revenue per user depends on the dataframe supplied: all observed users for ARPU, paying users for ARPPU. The dataset observation period must be established before comparing these metrics across time.

`FirstPurchaseDaysAfterInstall` is a conversion-latency measure. No activity-event table is used, so D1/D7/D30 cohort retention is not calculated. Numeric correlations are associations only. Churn prediction and causal uplift estimation are not implemented.

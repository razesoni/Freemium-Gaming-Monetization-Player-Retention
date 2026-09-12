# Data dictionary

Fields consumed by the current Python modules:

| Field | Use |
| --- | --- |
| UserID | Distinct-user denominator |
| InAppPurchaseAmount | Observed spending; currency and observation window require source verification |
| SpendingSegment | Existing segment label used for aggregation |
| FirstPurchaseDaysAfterInstall | Days to first purchase, used for descriptive statistics |
| SessionCount | Engagement feature |
| AverageSessionLength | Engagement feature; unit requires source verification |
| GameGenre | Genre filter and pivot |
| Device, Country | Dashboard filters |
| Age, Gender | Descriptive demographics |
| LastPurchaseDate | Parsed purchase date |

Source provenance, sampling method, units, and data collection dates are not independently established in this repository. Do not infer representative population behavior from this sample.

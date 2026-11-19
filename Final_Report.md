# FreshFlow Juice Company - Final Report

## 1. Executive summary
This project analyses a synthetic dataset of 500 transactions across 30 days. It examines data quality, outlet and product performance, daily revenue, discount bands and alternative discount scenarios.

## 2. Dataset profile
The CSV contains 500 data rows and 12 numeric columns. Each row represents one transaction. Numeric codes represent outlets, products, categories and payment methods. The data is generated reproducibly using a fixed random seed.

## 3. Data quality and cleaning
The program counts missing values and checks duplicate IDs, invalid days, unknown codes, category mismatches, invalid quantities, prices, costs, discounts and ratings. The original array is preserved. A separate cleaned array is used for financial calculations. Missing customer ratings are allowed because ratings are not required for sales calculations.

## 4. Metric definitions
- Gross sales = quantity × unit price
- Discount amount = gross sales × discount rate
- Net revenue = gross sales − discount amount
- Cost of goods sold = quantity × unit cost
- Gross profit = net revenue − cost of goods sold
- Gross margin (%) = gross profit ÷ net revenue × 100
- Average transaction value = mean net revenue per valid transaction

## 5. Sales performance
Use Task E output in `analysis_output.txt` to compare outlet and product revenue, gross profit and units. The highest-volume product may differ from the highest-profit product.

## 6. Trend analysis
Task G reports daily revenue, day-to-day absolute and percentage changes, a three-day moving average and cumulative revenue. A 30-day period cannot establish annual seasonality.

## 7. Discount investigation
Task H compares transaction counts, quantity, revenue and gross margin across discount bands. The results show association, not proof of cause and effect.

## 8. Anomaly register
Task I creates `anomaly_register.csv`. It flags high prices using the IQR rule, discounts above 30%, zero stock and unusual revenue using a z-score. These are review flags, not automatic errors.

## 9. Scenario analysis
Task J models alternative discount rates while holding quantity and unit cost constant. These scenarios are not forecasts and do not estimate customer demand response.

## 10. Limitations
The dataset is synthetic and covers only 30 days. Operating expenses are not included, so gross profit is not net profit. Transaction data alone cannot establish inventory waste or stock flow. Correlation or group differences do not prove causation.

## 11. Recommendations
Use Task L findings to compare outlet profitability, product demand with product profit, and discounts with gross margin. Monitor the recommended measures over a longer period before making business decisions.

## 12. Appendix
The Python script includes data loading, audit masks, cleaning, metric calculations, group comparisons, descriptive statistics, daily trends, anomaly flags, scenario analysis and validation tests.

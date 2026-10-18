# Retail Sales Performance & Inventory Optimization

## 1. Project Overview

This project analyzes the UCI Online Retail transaction dataset to understand sales performance, product demand, country-wise revenue, and monthly sales trends.

The objective is to provide data-driven recommendations that help a retail business improve sales planning and make better inventory decisions.

## 2. Key Business Findings

### Finding 1: Overall Sales Performance

- Total sales value: 10,642,110.80 dataset currency units.
- Total units sold: 5,572,420.
- Average order value: approximately 533.17 dataset currency units.
- The cleaned dataset contains 19,960 unique invoices according to the KPI analysis. An earlier analysis reported 19,962, so this difference requires reconciliation.

### Finding 2: Monthly Sales Trends

November 2011 recorded the highest monthly sales value in the analyzed data, at approximately 1,503,866.78.

December 2011 recorded approximately 637,790.33, but the dataset only covers December through December 9. Therefore, December should not be compared directly with complete months.

### Finding 3: Country-wise Sales

The United Kingdom contributed approximately 9,001,744.09 in sales value, making it the largest market in the dataset.

The Netherlands, EIRE, Germany, and France were among the other leading markets.

### Finding 4: Product Performance

The top-products analysis identifies items that generated higher sales value. These products can be investigated further to understand demand and prioritize inventory planning.

Postage-related entries, such as DOTCOM POSTAGE, should be reviewed separately from physical merchandise before making inventory assortment decisions.

## 3. Business Recommendations

### Recommendation 1: Prioritize High-Performing Products

Review high-sales products regularly and compare their sales patterns over time. Use this information alongside actual stock-on-hand data before deciding which products need priority replenishment.

### Recommendation 2: Improve Monthly Demand Planning

Use historical monthly sales trends to support purchasing and staffing plans. Consider seasonal demand patterns, but exclude incomplete periods from direct month-to-month comparisons.

### Recommendation 3: Focus on the Main Market

The United Kingdom is the largest market in this dataset. Monitor its sales trends and product demand while continuing to evaluate opportunities in other countries.

### Recommendation 4: Monitor Returns and Cancellations

Review negative-quantity transactions and cancellation invoices to identify possible return and cancellation patterns. Confirm the business meaning of these records before treating them as verified returns.

### Recommendation 5: Collect Inventory and Supplier Data

To calculate real stockout rates, reorder points, and supplier reliability, collect additional information such as:

- Daily inventory on-hand quantities.
- Stockout events and their duration.
- Supplier lead times.
- Purchase orders and delivery dates.
- Product costs and inventory holding costs.

Transaction data alone cannot establish whether a product was out of stock.

## 4. Project Limitations

- The dataset contains retail transactions, not historical inventory balances.
- Actual stockout rates and optimal reorder quantities cannot be calculated from the available fields alone.
- Supplier reliability and lead-time performance cannot be measured without supplier and delivery records.
- The unique invoice count differs between earlier EDA and later KPI analysis and should be reconciled.
- December 2011 is incomplete in the dataset.
- The sales figures are presented in dataset currency units, not converted into Indian rupees.

## 5. Conclusion

The project demonstrates how Python, SQL, and Power BI can be used to clean retail transaction data, analyze business performance, calculate KPIs, and communicate findings through a dashboard.

The analysis provides a foundation for inventory optimization. Adding real inventory, stockout, and supplier data would enable a more complete inventory management solution.

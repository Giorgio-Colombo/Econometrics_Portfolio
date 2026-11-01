# Boston Housing: determinants of house prices

A full write-up of a multiple linear regression on the Boston Housing dataset, carried out in **IBM SPSS**.

**Read the report:**
- [English version (PDF)](boston_housing_regression_EN.pdf)
- [Versione italiana (PDF)](boston_housing_regression_IT.pdf)

## Question
Which tract-level characteristics explain the median value of owner-occupied homes (`MEDV`, in $1,000s), and what is the best parsimonious model?

## Data
506 observations from the U.S. Census Bureau on Boston-area tracts, 13 explanatory variables (crime rate, nitric oxides, rooms per dwelling, distance to employment centres, pupil-teacher ratio, % lower-status population, and others). Originally used in Harrison & Rubinfeld (1978), *Hedonic prices and the demand for clean air*. No missing values.

## Approach
1. **Descriptives:** mean price about 22.5 thousand dollars, positive skew (1.108) and leptokurtosis (1.495). Prices above $50,000 are censored at $50,000, which explains the departure from normality.
2. **Collinearity:** `TAX` and `RAD` are almost perfectly correlated (r = 0.91); `TAX` has the highest VIF (about 9) and is dropped from the full model.
3. **Full model:** R² about 73.5%, F = 113.931, statistically significant at the 5% level.
4. **Restricted model:** `INDUS` and `AGE` are not significant and are removed.
5. **Model choice:** a nested-model F-test gives F = 0.74, below the critical value of 3.014 (α = 0.05, df = 2 and 494). We fail to reject the restriction, so the **restricted model is preferred**.
6. **Interpretation:** `LSTAT`, `CRIM`, `NOX`, `DIS` and `PTRATIO` have negative effects on price, while `RM` and `RAD` are positive. `RM` (rooms per dwelling) has by far the largest effect.
7. **Residuals:** mean zero with positive skew; the Shapiro-Wilk test (W of about 0.908) rejects normality, which is consistent with the censoring of the dependent variable.

## Limitations
The normality of residuals is rejected, and the censored price variable suggests a censored or log-linear specification as a natural next step.

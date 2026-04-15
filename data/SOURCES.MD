# Data Sources

All datasets in this folder are from verified UK government sources. They are
small, lightweight JSON files suitable for use in the Cabinet Secretary
objectives dashboard.

Curated from: https://github.com/i-dot-ai/awesome-gov-datasets

---

## ONS (Office for National Statistics)

| File | Description | Coverage | Source URL |
|------|-------------|----------|------------|
| `ons_gdp_quarterly_growth.json` | UK GDP quarter-on-quarter growth rate (%) | Last 10 years | [ONS IHYQ/PGDP](https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/ihyq/pgdp) |
| `ons_cpi_inflation.json` | UK CPI annual rate of inflation (%) | Last 5 years | [ONS L55O/MM23](https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/l55o/mm23) |
| `ons_unemployment_rate.json` | UK unemployment rate, age 16+ (%) | Last 5 years | [ONS MGSX/LMS](https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/unemployment/timeseries/mgsx/lms) |
| `ons_public_borrowing.json` | UK public sector net borrowing (GBP millions) | Last 5 years | [ONS DZLT/PUSF](https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/timeseries/dzlt/pusf) |
| `ons_uk_population.json` | UK population estimate (thousands) | Last 20 years | [ONS UKPOP/POP](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/timeseries/ukpop/pop) |

## GOV.UK Content API

| File | Description | Items | Source URL |
|------|-------------|-------|------------|
| `govuk_civil_service_policy_papers.json` | Policy papers on Civil Service reform | 15 | [GOV.UK Search API](https://www.gov.uk/api/search.json) |
| `govuk_ai_government_speeches.json` | Speeches on AI in government | 15 | [GOV.UK Search API](https://www.gov.uk/api/search.json) |
| `govuk_efficiency_papers.json` | Policy papers on government efficiency & productivity | 10 | [GOV.UK Search API](https://www.gov.uk/api/search.json) |
| `govuk_people_survey.json` | Civil Service People Survey results references | 10 | [GOV.UK Search API](https://www.gov.uk/api/search.json) |
| `govuk_civil_service_stats.json` | Civil Service statistics dataset references | 10 | [GOV.UK Search API](https://www.gov.uk/api/search.json) |

## Hansard (UK Parliament)

| File | Description | Source URL |
|------|-------------|------------|
| `hansard_civil_service_reform.json` | Parliamentary contributions mentioning civil service reform (summary + 20 sample contributions) | [Hansard API](https://hansard-api.parliament.uk) |

## Police Open Data

| File | Description | Source URL |
|------|-------------|------------|
| `police_crime_categories.json` | Crime category definitions used in UK policing data | [Police Data API](https://data.police.uk/api/crime-categories) |

---

## How these map to Cabinet Secretary objectives

- **Objective 1 (Delivery of Government priorities):** GDP growth, unemployment, inflation, public borrowing, efficiency papers
- **Objective 2 (Policy advice):** Policy papers, speeches, Hansard debates
- **Objective 3 (Cabinet Government):** Hansard debates, policy papers
- **Objective 4 (Civil Service reform):** Civil Service statistics, People Survey, efficiency papers, AI speeches
- **Objective 5 (Culture and engagement):** People Survey, Civil Service statistics, crime categories (public services context)

## Data freshness

Downloaded: 2026-04-15. All ONS time series are automatically updated by ONS.
GOV.UK and Hansard data reflects what was published at time of download.

# Apartment Rent Analysis – Zlín (Web Scraping Project)

This project focuses on the collection and analysis of apartment rental data in the city of **Zlín**, Czech Republic. The data was gathered using **web scraping** techniques with the `BeautifulSoup` library and subsequently analyzed using Python and pandas.

---

## Project Overview

The goal of this project was to:

- Scrape real estate listings from a housing website
- Extract relevant information: location, area, price, etc.
- Clean and process the data for statistical analysis
- Visualize patterns in rental pricing
- Provide a final report summarizing the findings

---

## Repository Structure

- `web_scraper_apartment_zlin.py` – converted Python script from original notebook
- `Web-scraping-data.csv` – dataset collected using BeautifulSoup
- `Final Report of the Project_Analysis of Apartments for Rent in Zlín.pdf` – final analytical report with visuals and summary
- `README.md` – this documentation

---

## How to Run the Script

1. Make sure you have Python 3.8+ installed
2. Install required libraries:

```bash
pip install pandas requests beautifulsoup4
```

3. Run the script:

```bash
python web_scraper_apartment_zlin.py
```

4. The dataset will be read from `Web-scraping-data.csv` and analyzed accordingly.

---

## Data Source

Data was collected via web scraping using the `BeautifulSoup` library from the Czech real estate website [www.sreality.cz](https://www.sreality.cz) from a public real estate listing site in the Czech Republic during a specific period.

---

## Output

The output includes descriptive statistics, price comparisons, location-based insights, and visual charts. All findings are summarized in the included PDF report.

---

## Notes

- This project was part of a data analysis and web scraping practice assignment.
- The data may no longer reflect the current state of the rental market.


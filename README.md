# wuzzuf_scraping
**Python project with Jupyter notebook**

The site will be scraped for some info found in the search result page, this info are simple and can be extracted using beautiful soup.

Then for each search result, using the link extracted from the previous step, other data will be scraped from inside each post page (like salary), this data can't be extracted using beautiful soup only because it's filled in using JavaScript, so selenium will be used to run a bot browser and load the site then scrap the data.

All the extracted data will be grouped in a table and saved in a local CSV file.

- Extracted info from the search result pages:
  - Job title
  - Company
  - Post link
  - Job location
  - Contract type
  - Skills required
- Extracted info from inside each post page:
  - Salary

Note: To run selenium, an exe for the firefox driver <a href=https://github.com/mozilla/geckodriver/releases>(GeckoDriver)</a> is needed

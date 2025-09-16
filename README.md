# HiringCafe Job Scraper

## What it does
This script pulls job listings from HiringCafe for **“Marketing Director”** in New York (last 14 days) and saves them to a CSV file.

## Files
- `hiringcafe_scraper.py` → the Python script  
- `hiringcafe_jobs.csv` → the output with all jobs  

## What’s in the CSV
Each row has:
- url  
- job title  
- company  
- salary (min and max if available)  
- remote (yes/no)  
- workplace type (remote, hybrid, onsite)  
- location  
- seniority level  
- commitment (full-time, part-time, contract, etc.)  
- apply source (where the job came from, like LinkedIn or company site)  

## How to run
1. Install the needed libraries:
   ```bash
   pip install requests pandas
2. Run the script:
   ```bash
   python hiringcafe_scraper.py
3. The jobs will be saved in:
   ```bash
   The jobs will be saved in:

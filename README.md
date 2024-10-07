# Dutch Employers Scraper

## Overview
This project is a Python-based web scraper designed to extract information about Dutch employers that are registered to provide relocation and visa sponsorships for knowledge migrants in the Netherlands. The data is sourced from the official Dutch immigration website and includes company names in Dutch, English, and Spanish.

### Features
- **Scrapes data from a specific table**: Extracts data starting from the "Empleo regular de inmigrantes del conocimiento" table, including all rows but excluding the table's title.
- **Handles timeouts and errors**: Implements retry logic for handling timeouts or connection errors, retrying up to 3 times with random delays between 1 and 3 seconds.
- **Translation using Google Translate**: Translates the company names from Dutch to English and Spanish.
- **Partial data saving**: Updates the Excel file every 100 rows to provide real-time progress monitoring, allowing you to open the file and see the scraped data before the entire process completes.
- **Error logging**: Captures any errors encountered during the scraping or translation process and logs them in an "Error" column in the resulting Excel file.

### Output
The script saves the extracted data into an Excel file named `NED Registered Employers.xlsx`. Each row in the file contains:
- **Row Number**: The position of the entry in the table.
- **Company Name (Dutch)**: The original company name as listed in the Dutch table.
- **Company Name (English)**: The translated company name.
- **Company Name (Spanish)**: The company name translated into Spanish.
- **Error**: Any error messages encountered during scraping or translation. If no errors occurred, this field will contain "None".

### Prerequisites
- Python 3.8 or higher
- An internet connection for accessing the Dutch immigration website and using Google Translate API.

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-github-username/DutchScrape.git
   cd DutchScrape

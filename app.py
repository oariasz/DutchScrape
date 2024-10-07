import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import pandas as pd
import time
import random


class Scraper:
    def __init__(self, url, max_retries=3, update_interval=100):
        self.url = url
        self.translator = Translator()
        self.data = []
        self.start_time = time.time()
        self.max_retries = max_retries
        self.update_interval = update_interval

    def fetch_content(self):
        retries = 0
        while retries < self.max_retries:
            try:
                response = requests.get(self.url, timeout=10)
                if response.status_code == 200:
                    return response.content
                else:
                    raise Exception(f"Failed to retrieve content. Status code: {response.status_code}")
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                retries += 1
                wait_time = random.uniform(1, 3)  # Wait between 1 and 3 seconds
                print(f"Timeout or connection error encountered. Retrying {retries}/{self.max_retries} after {wait_time:.2f} seconds...")
                time.sleep(wait_time)
        raise Exception("Failed to retrieve content after multiple retries due to timeouts.")

    def parse_html(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        # Find the specific table titled "Empleo regular de inmigrantes del conocimiento"
        table = soup.find('table')
        if not table:
            raise Exception("No table found on the page.")
        return table

    def extract_data(self, table):
        rows = table.find_all('tr')
        row_count = 0  # Counter for table rows
        for row in rows[1:]:  # Skip the first row if it contains column titles
            cells = row.find_all('td')
            if cells:
                try:
                    company_name_nl = cells[0].get_text(strip=True)  # Company name in Dutch
                    company_name_en = self.retry_translation(company_name_nl, 'en')
                    company_name_es = self.retry_translation(company_name_nl, 'es')

                    # Store the data
                    self.data.append({
                        "Row Number": row_count + 1,
                        "Company Name (Dutch)": company_name_nl,
                        "Company Name (English)": company_name_en,
                        "Company Name (Spanish)": company_name_es,
                        "Error": "None"
                    })

                    row_count += 1

                    # Print the row details to the console
                    print(f"Row {row_count} scraped:")
                    print(f"  Dutch: {company_name_nl}")
                    print(f"  English: {company_name_en}")
                    print(f"  Spanish: {company_name_es}\n")

                    # Update the Excel file every 100 rows
                    if row_count % self.update_interval == 0:
                        self.save_to_excel(partial=True)
                        print(f"Progress saved after {row_count} rows.")

                except Exception as e:
                    # Store the error in the data
                    self.data.append({
                        "Row Number": row_count + 1,
                        "Company Name (Dutch)": company_name_nl if 'company_name_nl' in locals() else "N/A",
                        "Company Name (English)": "N/A",
                        "Company Name (Spanish)": "N/A",
                        "Error": str(e)
                    })
                    print(f"Skipping row {row_count + 1} due to error: {e}")

    def retry_translation(self, text, dest_lang):
        retries = 0
        while retries < self.max_retries:
            try:
                translated_text = self.translator.translate(text, src='nl', dest=dest_lang).text
                return translated_text
            except Exception as e:
                retries += 1
                wait_time = random.uniform(1, 3)
                print(f"Translation error for '{text}' to '{dest_lang}'. Retrying {retries}/{self.max_retries} after {wait_time:.2f} seconds...")
                time.sleep(wait_time)
        raise Exception(f"Failed to translate '{text}' to '{dest_lang}' after {self.max_retries} retries.")

    def save_to_excel(self, partial=False):
        df = pd.DataFrame(self.data)
        df.to_excel("NED Registered Employers.xlsx", index=False)
        if partial:
            print("Partial data successfully saved to NED Registered Employers.xlsx")
        else:
            print("Final data successfully saved to NED Registered Employers.xlsx")

    def print_summary(self):
        elapsed_time = time.time() - self.start_time
        total_rows = len(self.data)
        print("\nSUMMARY:")
        print(f"Total rows scraped: {total_rows}")
        print(f"Time elapsed: {elapsed_time:.2f} seconds")


class TranslatorScraper:
    def __init__(self, url):
        self.scraper = Scraper(url)

    def run(self):
        try:
            html_content = self.scraper.fetch_content()
            table = self.scraper.parse_html(html_content)
            self.scraper.extract_data(table)
            self.scraper.save_to_excel()  # Save final data
            self.scraper.print_summary()
        except Exception as e:
            print(f"An error occurred: {e}")


# URL of the Dutch website
url = "https://ind.nl/nl/openbaar-register-erkende-referenten/openbaar-register-arbeid-regulier-kennismigranten"

# Create an instance of TranslatorScraper and run it
scraper = TranslatorScraper(url)
scraper.run()

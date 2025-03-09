from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from apppython import process_song_name

def get_current_trending_songs():
    # Define the target URL
    url = 'https://trending-songs.com/'
    trending_songs = []

    try:
        # Set up Chrome options for headless browsing
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        
        # Initialize Chrome driver with headless options
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        # Wait 5 seconds for dynamic content to load
        time.sleep(5)
        
        # Get the page source after JavaScript execution
        page_source = driver.page_source
        
        # Parse the HTML content
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Find and process table content
        table_elements = soup.find_all('table')
        for table in table_elements:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all(['td', 'th'])
                row_text = [col.get_text(strip=True) for col in cols]
                if any(row_text):  # Only process if row contains any text
                    # Process the entire row text
                    processed_text = process_song_name(' | '.join(row_text))
                    trending_songs.append(processed_text)

        driver.quit()
        return trending_songs

    except Exception as e:
        print(f"An error occurred: {e}")
        if 'driver' in locals():
            driver.quit()
        return []
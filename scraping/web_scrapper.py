from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
import os
import csv
from selenium.common.exceptions import NoSuchElementException
import json

# Setup WebDriver for Firefox
def get_web_driver(headless=False):
    options = webdriver.FirefoxOptions()
    if headless:
        options.add_argument('--headless')
    return webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

# Scrape and save genre links
def scrape_and_save_genre_links(driver, file_path="data/raw/genre_links.csv"):
    anime_url = 'https://myanimelist.net/anime.php'
    manga_url = 'https://myanimelist.net/manga.php'
    urls = [anime_url, manga_url]
    genre_data = []
    for url in urls:
        driver.get(url)
        # Locate the div that contains "Genres"
        # Find the div that contains the text "Genres"
        genre_header = driver.find_element(By.XPATH, "//div[contains(@class, 'normal_header') and contains(text(), 'Genres')]")
        # Find the next sibling div with class "genre-link"
        genre_section = genre_header.find_element(By.XPATH, "./following-sibling::div[@class='genre-link']")
        # Find the actual genre list within this section
        genre_rows = genre_section.find_elements(By.CLASS_NAME, 'genre-name-link')

        for genre_tag in genre_rows:
            genre_name = genre_tag.text.strip()
            genre_url = genre_tag.get_attribute('href')
            genre_data.append([genre_name, genre_url])

    # Ensure directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    file_exists = os.path.isfile(file_path)

    # Save to CSV
    with open(file_path, mode='a', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Genre", "URL"])
        writer.writerows(genre_data)

    print(f"Genre data saved to {file_path}")

# Load last accessed genre and page number from JSON
def load_last_accessed_url(file_path="data/raw/last_accessed_url.json"):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {"genre": None, "page": 1}  # Default start from start

# Save last accessed genre and page number to JSON
def save_last_accessed_url(genre, page_num, file_path="data/raw/last_accessed_url.json"):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump({"genre": genre, "page": page_num}, file)


# Scrape and save anime details
def scrape_anime_details(driver, file_path="data/raw/raw_scraped_anime_data.csv"):
    anime_blocks = driver.find_elements(By.CLASS_NAME, "js-anime-category-producer.seasonal-anime")
    if not anime_blocks:
        print("No anime data found on this page. Skipping...")
        return  1 # Skip processing if no anime blocks are found
    scraped_data = []

    for anime in anime_blocks:
        try:
            # Extract Title & Subtitle
            title_element = anime.find_element(By.CSS_SELECTOR, ".title-text .h2_anime_title a")
            title = title_element.text.strip()
            title_url = title_element.get_attribute("href")

            try:
                subtitle = anime.find_element(By.CSS_SELECTOR, ".title-text .h3_anime_subtitle").text.strip()
            except:
                subtitle = "" 

            # Extract Synopsis
            try:
                synopsis = anime.find_element(By.CSS_SELECTOR, ".synopsis.js-synopsis p").text.strip()
            except:
                synopsis = "" 

            # Extract Genres (Tags)
            genre_elements = anime.find_elements(By.CSS_SELECTOR, ".genres-inner .genre a")
            genres = [genre.text.strip() for genre in genre_elements]

            # Append extracted data
            scraped_data.append([title, subtitle, title_url, ", ".join(genres), synopsis, "Anime"])

        except Exception as e:
            print(f"Error scraping anime: {e}")
            continue  # Skip to the next anime if an error occurs

    # Save to CSV
    os.makedirs("data/raw", exist_ok=True)
    file_exists = os.path.isfile(file_path)

    with open(file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Title", "Subtitle", "URL", "Genres", "Synopsis", "Type"])  # Header
        writer.writerows(scraped_data)

    print(f"Scraped {len(scraped_data)} anime entries from the page.")


# Scrape and save manga details
def scrape_manga_details(driver, file_path="data/raw/raw_scraped_manga_data.csv"):
    manga_blocks = driver.find_elements(By.CLASS_NAME, "js-seasonal-anime") 
    scraped_data = []
    if not manga_blocks:
        print("No anime data found on this page. Skipping...")
        return 1 # Skip processing if no manga blocks are found

    for manga in manga_blocks:
        try:
            # Extract Title & Subtitle
            title_element = manga.find_element(By.CSS_SELECTOR, ".title-text .h2_manga_title a")
            title = title_element.text.strip()
            title_url = title_element.get_attribute("href")
            
            # Extract Subtitle 
            try:
                subtitle = manga.find_element(By.CSS_SELECTOR, ".title-text .h3_manga_subtitle").text.strip()
            except:
                subtitle = ""  
            # Extract Synopsis
            try:
                synopsis = manga.find_element(By.CSS_SELECTOR, ".synopsis.js-synopsis p").text.strip()
            except:
                synopsis = ""  
            # Extract Genres (Tags)
            genre_elements = manga.find_elements(By.CSS_SELECTOR, ".genres-inner .genre a")
            genres = [genre.text.strip() for genre in genre_elements]

            # Append extracted data
            scraped_data.append([title, subtitle, title_url, ", ".join(genres), synopsis, "Manga"])

        except Exception as e:
            print(f"Error scraping manga: {e}")
            continue  # Skip to the next manga if an error occurs

    # Save to CSV
    os.makedirs("data/raw", exist_ok=True)
    file_exists = os.path.isfile(file_path)

    with open(file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Title", "Subtitle", "URL", "Genres", "Synopsis", "Type"])  # Header
        writer.writerows(scraped_data)

    print(f"Scraped {len(scraped_data)} manga entries from the page.")



# Open genre links and paginate through them
def open_genre_links(driver, file_path="data/raw/genre_links.csv"):
    last_accessed = load_last_accessed_url()  # Load last genre and page number
    last_accessed_genre = last_accessed['genre']
    last_accessecd_page = last_accessed['page']
    
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        start_processing = False  # Flag to start processing after the last accessed genre

        for row in reader:
            current_genre_name = row[0]
            current_genre_url = row[1]

            # Start processing after reaching the last accessed genre
            if last_accessed_genre and current_genre_name != last_accessed_genre and not start_processing:
                continue  # Skip to the last accessed genre

            start_processing = True  # Start processing from this genre onward

            print(f"Opening {current_genre_name} page: {current_genre_url}")

            # Loop through pages starting from the saved last page
            for page_num in range(last_accessecd_page, 51):
                try:
                    page_url = f"{current_genre_url}?page={page_num}"
                    driver.get(page_url)
                    print(f"Opened {current_genre_name} page {page_num}")
                    if "manga" in current_genre_url:  # Check if the genre is for manga
                        flag = scrape_manga_details(driver)
                        # Save last accessed page number after successful scraping
                        if flag == 0:
                            save_last_accessed_url(current_genre_name, page_num + 1)
                        if flag == 1:
                            break  # Break out of the page loop for manga genre
                    else:  # Otherwise, scrape anime details
                        flag = scrape_anime_details(driver)
                        # Save last accessed page number after successful scraping
                        if flag == 0:
                            save_last_accessed_url(current_genre_name, page_num + 1)
                        if flag == 1:
                            break  # Break out of the page loop for anime genre


                except NoSuchElementException:
                    print(f"Page {page_num} not found for {current_genre_name}. Moving to next genre.")
                    
                    # Reset to start next genre from page 1
                    save_last_accessed_url(None, 1)
                    break  # Exit the loop and go to the next genre
# Main function
def main():
    driver = get_web_driver()
    try:
        # Uncomment the function you want to run
        print("Scraping Genres...")
        #scrape_and_save_genre_links(driver)
        print("Scraping Details...")
        #open_genre_links(driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
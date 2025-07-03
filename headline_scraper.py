# headline_scraper.py

# Imports
import datetime
from bs4 import BeautifulSoup
import requests

# Helper Function for NYT
def get_text(html_element):
    """
    Extracts the title and summary text from a given HTML element.

    Parameters:
        html_element (bs4.element.Tag): A BeautifulSoup HTML element containing the article information.

    Returns:
        str or None: The combined title and summary text if available, or None if no text is found.
    """
    title_and_summary_tag = html_element.find_all('p')

    if len(title_and_summary_tag) == 0:
        return None

    if len(title_and_summary_tag) < 2:
        return title_and_summary_tag[0].text

    title = title_and_summary_tag[0].text
    summary = title_and_summary_tag[1].text

    return title + ". " + summary

# Main Function
def main():
    """
    Runs the news headline scraper based on user-selected source.

    The user is prompted to enter one of the following sources: 'chicagotribune', 'nyt', or 'latimes'.
    The program sends a request to the selected news website, extracts headlines using BeautifulSoup,
    and saves the results in a text file named 'headlines_<source>_<YYYY-MM-DD>.txt'.

    Prints the number of headlines scraped and the output filename.

    If the source is invalid, a friendly error message is displayed.
    """
    # Get user input
    source = input("Enter the news source to scrape (chicagotribune, nyt, latimes): ").lower()

    if source == 'chicagotribune':
        print("Scraping Chicago Tribune...")
        response = requests.get('https://www.chicagotribune.com/', timeout=10)
        html = BeautifulSoup(response.text, 'html.parser')
        headlines = [headline['title'] for headline in html.find_all(class_="article-title")]

    elif source == 'nyt':
        print("Scraping New York Times...")
        response = requests.get('https://www.nytimes.com/', timeout=10)
        html = BeautifulSoup(response.text, 'html.parser')
        headlines = [get_text(headline) for headline in html.find_all(class_="story-wrapper")]

    elif source == 'latimes':
        print("Scraping Los Angeles Times...")
        response = requests.get('https://www.latimes.com/', timeout=10)
        html = BeautifulSoup(response.text, 'html.parser')
        headlines = [
            headline['aria-label'].strip()
            for headline in html.find_all('a', class_='link promo-placeholder')
            if 'aria-label' in headline.attrs
        ]

    else:
        print("\nInvalid source. Please enter one of the following: chicagotribune, nyt, latimes.\n")
        return

    # Clean out None values
    headlines = [headline for headline in headlines if headline is not None]

    # Save to file
    TODAY = datetime.datetime.today().strftime('%Y-%m-%d')
    filename = f"headlines_{source}_{TODAY}.txt"

    with open(filename, 'w', encoding='utf-8') as output_file:
        for headline in headlines:
            output_file.write(headline.strip() + '\n')

    print(f"Scraped {len(headlines)} headlines and saved to {filename}")

# Run the main function
if __name__ == "__main__":
    main()
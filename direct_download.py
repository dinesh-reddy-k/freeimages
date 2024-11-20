from utils import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor, as_completed
from downloader import download_image

def init_browser() -> webdriver.Chrome:
    try:
        options = chromeBrowserOptions()
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    except Exception as e:
        raise RuntimeError(f"Failed to initialize browser: {str(e)}")

def get_search_link():
    # Base URL
    base_url = "https://www.freepik.com/search?"

    # Function to get input and return value or None
    def get_input(prompt, default=None):
        value = input(prompt).strip()
        return value if value else default

    # Getting inputs for parameters
    ai = get_input("Exclude AI-generated content? (yes/no or leave blank): ")
    if ai:
        ai_param = "excluded" if ai.lower() == "yes" else "included"
    else:
        ai_param = None

    orientation = get_input("Enter orientation (muiltiple with space separated) (landscape, panoramic, portrait, square, or leave blank): ")
    people = get_input("Include people? (yes/no or leave blank): ")
    if people:
        people_param = "include" if people.lower() == "yes" else "exclude"
    else:
        people_param = None

    premium = get_input("Premium only? (yes/no or leave blank): ")
    if premium:
        premium_param = "1" if premium.lower() == "yes" else "0"
    else:
        premium_param = None

    query = get_input("Enter search query (e.g., Happy Man or leave blank): ")
    content_type = get_input("Enter content type (vector, icon, video, psd, , photo, template, mockup or leave blank): ")

    # Constructing the URL
    params = {
        "ai": ai_param,
        "format": 'search',
        "orientation": orientation.replace(' ', '%2C') if orientation else '',
        "people": people_param,
        "premium": premium_param,
        "query": query.replace(' ','+'),
        "type": content_type,
    }

    # Filter out None values from parameters
    filtered_params = {key: value for key, value in params.items() if value is not None}

    # Join parameters into the URL
    final_url = base_url + "&".join([f"{key}={value}" for key, value in filtered_params.items()])
    return final_url
    print(final_url)

def download_images(urls):

    MAX_CONCURRENT = 10
    with ThreadPoolExecutor(max_workers=MAX_CONCURRENT) as executor:
        # Submit all tasks
        {executor.submit(download_image, a): a for a in urls}

def main():
    link = get_search_link()
    browser = init_browser()
    browser.get(link)
    elements = browser.find_elements(By.XPATH, '//*[@id="__next"]/div[4]/div[3]/div/div[3]/div/figure/a/img')
    print(len(elements))
    image_urls = []
    for element in elements:
        image_urls.append(element.get_attribute("src"))
    download_images(image_urls)
    
if __name__ == '__main__':
    main()

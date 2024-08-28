import requests
from bs4 import BeautifulSoup

# Function to scrape webpage content
def scrape_webpage(url):
    try:
        # Fetch HTML content from the webpage
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for unsuccessful responses
    except requests.exceptions.RequestException as e:
        print("Failed to fetch webpage:", e)
        return None
    
    # Parse HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract CSS links
    css_links = [link.get('href') for link in soup.find_all('link', rel='stylesheet')]
    
    # Extract JS links
    js_links = [script.get('src') for script in soup.find_all('script', src=True)]
    
    # Extract all other links
    other_links = [link.get('href') for link in soup.find_all('a', href=True)]
    
    # Extract text content
    text_content = soup.get_text()
    
    # Extract all HTML content
    html_content = str(soup)
    
    return {
        'css_links': css_links,
        'js_links': js_links,
        'other_links': other_links,
        'text_content': text_content,
        'html_content': html_content
    }

# Function to scrape image links
def scrape_image_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Failed to fetch image links:", e)
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    image_links = [img.get('src') for img in soup.find_all('img', src=True)]
    return image_links

# Function to scrape video links
def scrape_video_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Failed to fetch video links:", e)
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    video_links = [video.get('src') for video in soup.find_all('video', src=True)]
    return video_links

# Function to prompt user for choices
def get_user_choices():
    choices = []
    print("Select the data you want to extract:")
    print("1. HTML")
    print("2. CSS")
    print("3. JavaScript")
    print("4. Text Content")
    print("5. Links")
    print("6. Images")
    print("7. Videos")
    
    user_input = input("Enter the numbers separated by commas (e.g., 1,2,3): ").strip()
    for choice in user_input.split(','):
        choices.append(int(choice))
    return choices

# Function to ask the user if they want to perform another task
def perform_another_task():
    while True:
        choice = input("\nDo you want to perform another task? (yes/no): ").strip().lower()
        if choice == 'yes':
            return True
        elif choice == 'no':
            return False
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")

# Example usage
url = input("Enter the URL of the webpage: ")  # Prompt user for URL
while True:
    data = scrape_webpage(url)
    if data:
        user_choices = get_user_choices()
        for choice in user_choices:
            if choice == 1:
                print("\nHTML Content:")
                print(data['html_content'])
            elif choice == 2:
                print("\nCSS Links:")
                print(data['css_links'])
            elif choice == 3:
                print("\nJS Links:")
                print(data['js_links'])
            elif choice == 4:
                print("\nText Content:")
                print(data['text_content'])
            elif choice == 5:
                print("\nOther Links:")
                print(data['other_links'])
            elif choice == 6:
                print("\nImage Links:")
                image_links = scrape_image_links(url)
                if image_links:
                    print(image_links)
            elif choice == 7:
                print("\nVideo Links:")
                video_links = scrape_video_links(url)
                if video_links:
                    print(video_links)
            
        if not perform_another_task():
            break
    else:
        print("Failed to scrape webpage. Exiting program...")
        break
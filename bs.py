from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import csv


# Create a new instance of the Chrome driver
driver = webdriver.Chrome(
    executable_path="C:/Users/Rudhi/Downloads/sy_scraper/chromedriver.exe"
)

# Navigate to the webpage
driver.get("https://www.glassdoor.sg/Reviews/ASUS-Reviews-E40093.htm")

# chrome options
options = webdriver.ChromeOptions()
# options.add_argument("--start-maximized")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")
options.add_experimental_option("excludeSwitches", ["enable-logging"])

# Wait for the page to load (you might need to adjust this time depending on the website)

url = "https://www.glassdoor.sg/Overview/Working-at-ASUS-EI_IE40093.11,15.htm"
driver.get(url)

time.sleep(5)

element = driver.find_element(
    By.XPATH, '//*[@id="EmpLinksWrapper"]/div[2]/div/div[1]/a[1]'
)
element.click()

time.sleep(15)

Enter_email = driver.find_element(By.ID, "hardsellUserEmail")
Enter_email.send_keys("yagat53495@artgulin.com")
time.sleep(5)
Enter_email.send_keys(Keys.ENTER)
time.sleep(5)
Enter_pw = driver.find_element(By.ID, "hardsellUserPassword")
Enter_pw.send_keys("man12345")
time.sleep(5)
Enter_pw.send_keys(Keys.ENTER)
time.sleep(25)


def collect_ratings_and_dates():
    # Find all rating elements
    ratings = driver.find_elements(
        By.CLASS_NAME, "review-details__review-details-module__overallRating"
    )
    dates = driver.find_elements(
        By.CLASS_NAME, "review-details__review-details-module__reviewDate"
    )

    # Create a list to store the data
    data = []

    # Add each rating and date to the list
    for rating, date in zip(ratings, dates):
        data.append([rating.text, date.text])

    return data


# Find all rating elements
ratings = driver.find_elements(
    By.CLASS_NAME, "review-details__review-details-module__overallRating"
)

dates = driver.find_elements(
    By.CLASS_NAME, "review-details__review-details-module__reviewDate"
)

current_page = 1
all_data = []
while current_page <= 3:
    # Collect ratings and dates on the current page
    current_data = collect_ratings_and_dates()
    all_data.extend(current_data)

    # Determine the correct page number link based on the current page number
    page_link_xpath = (
        '//*[@id="Container"]/div/div[1]/div[2]/main/div[{}]/div/div[1]/ul/li[{}]/a'
    )
    if current_page <= 3:
        div_index = 6 if current_page == 1 else 5
        page_number = current_page + 1
    else:
        div_index = 5
        page_number = 4

    # Find the next page link
    next_page_link = driver.find_element(
        By.XPATH, page_link_xpath.format(div_index, page_number)
    )

    # Click the next page link
    next_page_link.click()

    # Wait for the page to load
    time.sleep(2)  # Adjust the sleep time according to your page load time

    # Increment the current page number
    current_page += 1

with open("ratings_and_dates.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Rating", "Date"])
    writer.writerows(all_data)

# Close the browser
driver.quit()

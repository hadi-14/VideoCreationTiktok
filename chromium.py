# Import necessary modules
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
import chrome_version

from GoogleSheetHandler import GoogleSheetHandler
from VideoProcessor import VideoProcessor
import time
import pyperclip
import random
import string
import os

# Instantiate GoogleSheetHandler
handler = GoogleSheetHandler()
df = handler.get_sheet_data('TiktokBot')
df["Status"].replace("", "Remaining", inplace=True)
handler.overwrite_sheet_with_data(df, "TiktokBot")

# Function to generate a random password
def generate_password(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# Set up undetected Chrome options
co = uc.ChromeOptions()

# Add arguments to Chrome options
co.add_argument(r"--user-data-dir=C:\Users\Dell\AppData\Local\Google\Chrome\User Data")
co.add_argument(r'--profile-directory=Profile 15')
co.add_argument("--start-maximized")
co.add_argument('--disable-gpu')
co.add_argument('--disable-infobars')
co.add_argument('--no-sandbox')
co.add_argument("--disable-popup-blocking")
co.add_argument("--disable-dev-shm-usage")
co.add_argument("--disable-notifications")
co.add_experimental_option("prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False})
# co.add_argument('--headless')

# Function to get window handles
def getWindowHandles():
    return driver.window_handles

# Instantiate undetected Chrome driver with options
driver = uc.Chrome(options=co, use_subprocess=True, version_main=int(chrome_version.get_chrome_version().split(".")[0]))

# Instantiate ActionChains
actions = ActionChains(driver)
driver.maximize_window()

# Visit URL
driver.get("https://chat.openai.com/c/dfd3b1e4-2b78-402a-a48e-a327542261b0")
time.sleep(5)
driver.implicitly_wait(10)
driver.execute_script(f'''window.open("https://app.simplified.com/signup");''')
time.sleep(5)
driver.switch_to.window(getWindowHandles()[1])
driver.implicitly_wait(10)

time.sleep(0.5)

def signup():
    actions.click(WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Sign Up with Google')]/../..")))).perform()
    time.sleep(5)

    driver.switch_to.window(getWindowHandles()[-1])
    actions.click(WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@data-identifier='asjaisimplified@gmail.com']")))).perform()

    time.sleep(10)

    driver.switch_to.window(getWindowHandles()[1])
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Hint: Name of your company']"))).send_keys(random.choice(["Tiktok", "Test", "Magic", "IDK", "Youtube", "Facebook", "HomeWork", "Experiment", "Student"]))
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(1)

def logout():
    driver.get("https://app.simplified.com/settings")

    time.sleep(1)
    actions.move_to_element(WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Danger Zone')]")))).click().perform()
    
    time.sleep(0.5)
    actions.move_to_element(WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Delete Account')]")))).click().perform()
    actions.move_to_element(WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Yes, delete')]")))).click().perform()

    time.sleep(5)

try:
    signup()
except:

    logout()
    driver.get("https://app.simplified.com/signup")
    time.sleep(1)

    signup()

# Loop through dataframe
DoneCnt = 0
for cnt, topic in enumerate(df["Topic"]):
    if df["Status"].values.tolist()[cnt] != "Remaining":
        continue

    driver.switch_to.window(getWindowHandles()[0])

    # Define prompts
    prompts = [
        f'Write a 75 second viral educational showcase Tik Tok script about Do you know about "{topic}" Make sure the script is engaging with a good, quick hook. Keep the script relatively serious and educational. The script should ONLY include the voice, NOT the editing direction or stage direction! Start with a " and end with a ". Have paragraph breaks that stay within the". Do not do a countdown. Do not include an outro or summary. DO NOT USE EMOJIS! The script should portray the info in interactive way. Describe and make it educational. Start with "Do you know!"',
        "give me short caption for this too with suitable hashtags for tiktok with #DidYouKnow included"
    ]

    # Send first prompt
    actions.send_keys_to_element(driver.find_element(By.XPATH, "//textarea[@placeholder='Message ChatGPT…']"), prompts[0]).perform()
    driver.find_element(By.XPATH, "//button[@data-testid='send-button']").click()
    time.sleep(1)

    # Click on message box to get script
    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid='send-button']")))
    actions.click(driver.find_elements(By.XPATH, "//*[@class='flex items-center gap-1.5 rounded-md p-1 text-xs text-token-text-tertiary hover:text-token-text-primary md:invisible md:group-hover:visible md:group-[.final-completion]:visible']")[-1]).perform()
    script = pyperclip.paste().strip()
    print("Script: ", script)

    # Send second prompt
    actions.send_keys_to_element(driver.find_element(By.XPATH, "//textarea[@placeholder='Message ChatGPT…']"), prompts[1]).perform()
    driver.find_element(By.XPATH, "//button[@data-testid='send-button']").click()
    time.sleep(1)

    # Click on message box to get title
    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid='send-button']")))
    actions.click(driver.find_elements(By.XPATH, "//*[@class='flex items-center gap-1.5 rounded-md p-1 text-xs text-token-text-tertiary hover:text-token-text-primary md:invisible md:group-hover:visible md:group-[.final-completion]:visible']")[-1]).perform()
    title = pyperclip.paste().strip().removeprefix('"').removesuffix('"')
    print("Title: ", title)

    # Switch to second window
    driver.switch_to.window(getWindowHandles()[1])
    driver.get("https://app.simplified.com/video/generate-ai/script-to-video")
    driver.implicitly_wait(10)
    time.sleep(5)

    actions.click(driver.find_element(By.XPATH, "//*[contains(text(), 'Select AI Speaker')]/..")).perform()
    time.sleep(0.5)

    # Select AI Speaker
    actions.click(WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'AI Speakers')]")))).perform()
    time.sleep(0.5)
    actions.click(WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Matthew')]/../../../..")))).perform()
    time.sleep(1)

    # Enter title
    actions.click(driver.find_element(By.XPATH, "//textarea[@name='title']")).perform()
    pyperclip.copy(title)
    actions.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
    time.sleep(1)

    # Enter script
    actions.click(driver.find_element(By.XPATH, "//textarea[@name='description']")).perform()
    pyperclip.copy(script)
    actions.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
    time.sleep(1)

    # Generate video
    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Generate')]"))).click()

    # Wait for export button
    WebDriverWait(driver, 600).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Export')]/..")))
    time.sleep(15)

    # Click on export
    actions.move_to_element(WebDriverWait(driver, 600).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Export')]/..")))).click().perform()
    time.sleep(1.2)

    # Click on download
    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Download')]"))).click()

    # Get most recent .fdmdownload file
    recent_fdmdownload = VideoProcessor.get_most_recent_fdmdownload()
    recent_mp4 = VideoProcessor.convert_fdmdownload_to_mp4(recent_fdmdownload)
    current_directory = os.path.join(os.getcwd(), "media")

    # Crop video
    path = os.path.join(current_directory, title + ".mp4")
    VideoProcessor.cropVideo(recent_mp4, path, 69, 244, 1676, 942)
    os.remove(recent_mp4)

    # Update dataframe status
    df.at[cnt, "Status"] = "Done"
    handler.overwrite_sheet_with_data(df, "TiktokBot")

    DoneCnt += 1
    if DoneCnt >= 10 or ((cnt+1) == len(df["Topic"])):
        logout()

driver.close()
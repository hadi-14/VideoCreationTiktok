# Import necessary modules
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
import chrome_version

from __utils__.GoogleSheetHandler import GoogleSheetHandler
from __utils__.VideoProcessor import processVideo
from __utils__.helpers import BrowserHelpers
import time
import random
import string

VIDEOS_PER_ACCOUNT_CYCLE = 10

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
co.add_argument("--no-first-run")
co.add_argument("--no-defualt-browser-check")
co.add_argument("--start-maximized")
co.add_argument('--disable-gpu')
co.add_argument('--disable-infobars')
co.add_argument('--no-sandbox')
co.add_argument("--disable-popup-blocking")
co.add_argument("--disable-dev-shm-usage")
co.add_argument("--disable-notifications")
co.add_experimental_option("prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False})
# co.add_argument('--headless')

# Instantiate undetected Chrome driver with options
driver = uc.Chrome(options=co, use_subprocess=True, version_main=int(chrome_version.get_chrome_version().split(".")[0]))

# Instantiate ActionChains
actions = ActionChains(driver)
driver.maximize_window()

helper = BrowserHelpers(driver, actions)

# Visit URL
driver.get("https://chat.openai.com/c/dfd3b1e4-2b78-402a-a48e-a327542261b0")
time.sleep(5)
driver.implicitly_wait(10)

while "Remaining" in df["status"].values.tolist():
    driver.execute_script(f'''window.open("https://app.simplified.com/signup");''')
    time.sleep(5)
    driver.switch_to.window(helper.getWindowHandles()[1])
    driver.implicitly_wait(10)

    time.sleep(0.5)

    try:
        helper.signup()
    except:

        helper.logout()
        driver.get("https://app.simplified.com/signup")
        time.sleep(1)

        helper.signup()
        
    driver.close()

    with open("titles.txt", "w") as f:
        f.write("")

    # Loop through dataframe
    DoneCnt = 0
    titlesDone = {}
    for cnt, topic in enumerate(df["Topic"]):
        if df["Status"].values.tolist()[cnt] != "Remaining":
            continue

        driver.switch_to.window(helper.getWindowHandles()[0])
        title, script = helper.askGPT(topic)

        # Switch to second window
        driver.execute_script(f'''window.open("https://app.simplified.com/video/generate-ai/text-to-video");''')
        driver.switch_to.window(helper.getWindowHandles()[DoneCnt + 1])
        helper.GenerateVideo(topic, script)
        titlesDone[title] = cnt
        
        with open("titles.txt", "a") as f:
            f.write(f"{title}\n")

        DoneCnt += 1
        if DoneCnt >= VIDEOS_PER_ACCOUNT_CYCLE or ((cnt+1) == len(df["Topic"])):
            break
            
    DoneCnt = 0
    for title in list(titlesDone.keys()):
        cnt = titlesDone[title]
        
        driver.switch_to.window(helper.getWindowHandles()[DoneCnt + 1])

        # Wait for export button
        WebDriverWait(driver, 1000).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Export')]/..")))
        time.sleep(5)

        helper.exportVideo()

        # TODO: to study the file name scheme and then make this step faster by able to download multiple exports
        processVideo(title)
        driver.close()

        # Update dataframe status
        df.at[cnt, "Status"] = "Done"
        handler.overwrite_sheet_with_data(df, "TiktokBot")

        DoneCnt += 1
        if DoneCnt >= VIDEOS_PER_ACCOUNT_CYCLE:
            helper.logout()
            break

driver.close()
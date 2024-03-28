# %%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome import service
from oauth2client.service_account import ServiceAccountCredentials
from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import crop
import time
import pyperclip
import random
import string
import pandas as pd
import gspread
import os
import shutil
import cv2
import getpass
# %%
class GoogleSheetHandler:
    def __init__(self, credentials_file='credentials.json'):
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.credentials_file = credentials_file
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_file, self.scope)
        self.gc = gspread.authorize(self.credentials)

    def get_sheet_data(self, spreadsheet_name, worksheet_index=0):
        spreadsheet = self.gc.open(spreadsheet_name)
        worksheet = spreadsheet.get_worksheet(worksheet_index)
        data = worksheet.get_all_values()
        df = pd.DataFrame(data[1:], columns=data[0])
        return df

    def overwrite_sheet_with_data(self, dataframe, spreadsheet_name, worksheet_index=0):
        spreadsheet = self.gc.open(spreadsheet_name)
        worksheet = spreadsheet.get_worksheet(worksheet_index)
        data = dataframe.values.tolist()
        worksheet.clear()
        # worksheet.resize(len(data), len(data[0]))
        worksheet.append_row(dataframe.columns.tolist())
        worksheet.append_rows(data)

def cropVideo(src, dest, x,y,h,w):
    clip = VideoFileClip(src)
    cropped_clip = crop(clip, x1=x, y1=y, width=w, height=h)
    cropped_clip.write_videofile(dest)
# %%
handler = GoogleSheetHandler()
df = handler.get_sheet_data('TiktokBot')
df["Status"].replace("", "Remaining", inplace=True)
handler.overwrite_sheet_with_data(df, "TiktokBot")
df

# %%
def generate_password(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# %%
co = webdriver.ChromeOptions()

co.add_argument("--start-maximized")
co.add_argument('--disable-gpu')
co.add_argument('--disable-infobars')
co.add_argument('--no-sandbox')
# co.add_argument('--headless')
co.add_argument("--disable-popup-blocking")
co.add_argument(fr"--user-data-dir=C:\Users\{getpass.getuser()}\AppData\Roaming\Opera Software\Opera Stable")
co.add_argument(r'--profile-directory=Default') #e.g. Profile 3
co.binary_location = fr"C:\Users\{getpass.getuser()}\AppData\Local\Programs\Opera\opera.exe"
co.add_experimental_option('w3c', True)

def getWindowHandles():
    handles = driver.window_handles[1:].copy()
    del handles[1]
    return handles

# driver = webdriver.Chrome(options=co, use_subprocess=True)

webdriver_service = service.Service("operadriver.exe")
webdriver_service.start()
driver = webdriver.Remote(webdriver_service.service_url, options=co)

actions = ActionChains(driver)
driver.maximize_window()
# URLs to visit
driver.get("https://chat.openai.com/c/202a469b-f42f-4bea-a736-ae4bfc7ebed3")
time.sleep(5)
driver.implicitly_wait(10)
driver.execute_script(f'''window.open("https://www.capcut.com/my-cloud/7341722566995918853");''')
time.sleep(5)
driver.switch_to.window(getWindowHandles()[1])
driver.implicitly_wait(10)
driver.execute_script(f'''window.open("https://app.simplified.com/signup");''')
time.sleep(5)
driver.switch_to.window(getWindowHandles()[2])
driver.implicitly_wait(10)

# %%
time.sleep(0.5)
# actions.send_keys_to_element(driver.find_element(By.XPATH, "//input[@type='email']"), email).perform()
# password = generate_password()
# actions.send_keys_to_element(driver.find_element(By.XPATH, "(//input[@type='password'])"), password).perform()
actions.click(WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Sign Up with Google')]/../..")))).perform()
time.sleep(2)
try:
    driver.switch_to.window(getWindowHandles()[-1])
    actions.click(WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@data-identifier='asjaisimplified@gmail.com']")))).perform()
except:
    driver.switch_to.window(getWindowHandles()[-2])
    actions.click(WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@data-identifier='asjaisimplified@gmail.com']")))).perform()

time.sleep(10)

driver.switch_to.window(getWindowHandles()[2])
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Hint: Name of your company']"))).send_keys(random.choice(["Tiktok", "Test", "Magic", "IDK", "Youtube", "Facebook", "HomeWork", "Experiment", "Student"]))
driver.find_element(By.XPATH, "//button[@type='submit']").click()
time.sleep(1)

# %%
driver.get("https://app.simplified.com/activate/video")

driver.get("https://app.simplified.com/video/generate-ai/script-to-video")

# %%
DoneCnt = 0
for cnt, topic in  enumerate(df["Topic"]):
    if df["Status"].values.tolist()[cnt] != "Remaining":continue
    driver.switch_to.window(getWindowHandles()[0])

    prompts = [f'Write a 90 second viral educational showcase Tik Tok script about Do you know about "{topic}" Make sure the script is engaging with a good, quick hook. Keep the script relatively serious and educational. The script should ONLY include the voice, NOT the editing direction or stage direction! Start with a " and end with a ". Have paragraph breaks that stay within the". Do not do a countdown. Do not include an outro or summary. DO NOT USE EMOJIS! The script should portray the info in interactive way. Describe and make it educational. Start with "Do you know!"', "give me short caption for this too with suitable hashtags for tiktok with #DidYouKnow included"]

    driver.find_element(By.XPATH, "//textarea[@placeholder='Message ChatGPT…']").send_keys(prompts[0])
    driver.find_element(By.XPATH, "//button[@data-testid='send-button']").click()

    time.sleep(1)
    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid='send-button']")))
    driver.find_elements(By.XPATH, "//*[@class='flex items-center gap-1.5 rounded-md p-1 text-xs text-token-text-tertiary hover:text-token-text-primary md:invisible md:group-hover:visible md:group-[.final-completion]:visible']")[-1].click()
    script = pyperclip.paste()
    print("Script: ", script)

    driver.find_element(By.XPATH, "//textarea[@placeholder='Message ChatGPT…']").send_keys(prompts[1])
    driver.find_element(By.XPATH, "//button[@data-testid='send-button']").click()

    time.sleep(1)
    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid='send-button']")))
    driver.find_elements(By.XPATH, "//*[@class='flex items-center gap-1.5 rounded-md p-1 text-xs text-token-text-tertiary hover:text-token-text-primary md:invisible md:group-hover:visible md:group-[.final-completion]:visible']")[-1].click()
    title = pyperclip.paste().removeprefix('"').removesuffix('"')
    print("Title: ", title)

    driver.switch_to.window(getWindowHandles()[2])
    driver.get("https://app.simplified.com/video/generate-ai/script-to-video")
    driver.implicitly_wait(10)
    time.sleep(5)
    actions.click(driver.find_element(By.XPATH, "//*[@id='popover-trigger-17']")).perform()
    time.sleep(0.5)

    actions.click(WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Video Captions language')]/../div")))).perform()
    time.sleep(0.5)
    actions.send_keys("English").perform()
    time.sleep(0.5)
    actions.send_keys(Keys.ENTER).perform()
    time.sleep(0.5)
    # actions.click(WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Video Captions language')]/../div")))).perform()
    # time.sleep(0.5)
    
    actions.click(WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Select AI speaker')]/../button")))).perform()
    time.sleep(0.5)
    actions.click(WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Matthew')]/../../../..")))).perform()
    time.sleep(1)

    actions.click(driver.find_element(By.XPATH, "//textarea[@name='title']")).perform()
    pyperclip.copy(title)
    actions.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
    time.sleep(1)

    actions.click(driver.find_element(By.XPATH, "//textarea[@name='description']")).perform()
    pyperclip.copy(script)
    actions.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
    time.sleep(1)

    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Generate')]"))).click()

    # %%
    WebDriverWait(driver, 600).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Export')]/..")))
    time.sleep(5)
    WebDriverWait(driver, 600).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Export')]/.."))).click()
    time.sleep(1.2)
    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Download')]"))).click()

    # %%
    def get_most_recent_fdmdownload():
        downloads_folder = os.path.expanduser("~/Downloads")  # Path to the Downloads folder

        while True:
            files = os.listdir(downloads_folder)
            for file in files:
                if file.endswith(".mp4.fdmdownload"):
                    return os.path.join(downloads_folder, file)
            time.sleep(1)  # Wait for 1 second

    # Function to convert .fdmdownload file to its corresponding MP4 file
    def convert_fdmdownload_to_mp4(fdmdownload_path):
        mp4_path = fdmdownload_path.replace(".fdmdownload", "")
        while not os.path.exists(mp4_path):
            time.sleep(1)  # Wait for 1 second
        # os.rename(fdmdownload_path, mp4_path)
        return mp4_path


    # %%
    # Get the path of the most recent .fdmdownload file
    recent_fdmdownload = get_most_recent_fdmdownload()
    recent_mp4 = convert_fdmdownload_to_mp4(recent_fdmdownload)
    current_directory = os.path.join(os.getcwd(), "media")
    # shutil.move(recent_mp4, os.path.join(current_directory,"temp.mp4"))

    # %%
    path = os.path.join(current_directory, title + ".mp4")
    cropVideo(recent_mp4, path, 69,244,1676,942)
    os.remove(recent_mp4)

    # %%
    # driver.switch_to.window(getWindowHandles()[1])
    # driver.find_element(By.XPATH, "//*[contains(text(),'Materials')]/../../..").click()
    # time.sleep(1)
    # driver.find_element(By.XPATH, "//input[@type='file']").send_keys(path)

    # time.sleep(10)
    # os.remove(path)

    # %% 
    df.at[cnt, "Status"] = "Done"
    handler.overwrite_sheet_with_data(df, "TiktokBot")

    DoneCnt += 1
    if DoneCnt >= 10:break
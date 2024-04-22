import random
import time
import pyperclip
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class BrowserHelpers():
    
    def __init__(self, driver, actions) -> None:
        self.driver = driver
        self.actions = actions

    def signup(self):
        self.actions.click(WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Sign Up with Google')]/../..")))).perform()
        time.sleep(5)

        self.driver.switch_to.window(self.getWindowHandles()[-1])
        self.actions.click(WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@data-identifier='asjaisimplified@gmail.com']")))).perform()

        time.sleep(10)

        self.driver.switch_to.window(self.getWindowHandles()[1])
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Hint: Name of your company']"))).send_keys(random.choice(["Tiktok", "Test", "Magic", "IDK", "Youtube", "Facebook", "HomeWork", "Experiment", "Student"]))
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(1)

    def logout(self):
        self.driver.get("https://app.simplified.com/settings")

        time.sleep(3)
        self.actions.move_to_element(WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Danger Zone')]")))).perform()
        self.actions.click(WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Danger Zone')]")))).perform()
        
        time.sleep(1)
        self.actions.move_to_element(WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Delete Account')]")))).click().perform()
        self.actions.move_to_element(WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Yes, delete')]")))).click().perform()

        time.sleep(5)
        
    def askGPT(self, topic):
        # Define prompts
        prompts = [
            f'Write a 75 second viral educational showcase TikTok script about Do you know about "{topic}" Make sure the script is engaging with a good, quick hook. Keep the script relatively serious and educational. The script should ONLY include the voice, NOT the editing direction or stage direction! Start with a " and end with a ". Have paragraph breaks that stay within the". Do not do a countdown. Do not include an outro or summary. DO NOT USE EMOJIS! The script should portray the info in an interactive way. Describe and make it educational. Start with "Do you know!" and keep within 250 words',
            "give me short caption for this too with suitable hashtags for tiktok with #DidYouKnow included and keep it withn 20 words"
        ]

        # Send first prompt
        self.actions.send_keys_to_element(self.driver.find_element(By.XPATH, "//textarea[@placeholder='Message ChatGPT…']"), prompts[0]).perform()
        self.driver.find_element(By.XPATH, "//button[@data-testid='send-button']").click()
        time.sleep(1)
    
        # Click on message box to get script
        WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid='send-button']")))
        self.actions.move_to_element(self.driver.find_elements(By.XPATH, "//div[@data-message-author-role='assistant']")[-1]).perform()
        time.sleep(0.8)
        self.actions.click(self.driver.find_elements(By.XPATH, "//*[@class='flex items-center gap-1.5 rounded-md p-1 text-xs text-token-text-tertiary hover:text-token-text-primary']")[-1]).perform()
        script = pyperclip.paste().strip()
        print("Script: ", script)

        # Send second prompt
        self.actions.send_keys_to_element(self.driver.find_element(By.XPATH, "//textarea[@placeholder='Message ChatGPT…']"), prompts[1]).perform()
        self.driver.find_element(By.XPATH, "//button[@data-testid='send-button']").click()
        time.sleep(1)

        # Click on message box to get title
        WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid='send-button']")))
        self.actions.click(self.driver.find_elements(By.XPATH, "//*[@class='flex items-center gap-1.5 rounded-md p-1 text-xs text-token-text-tertiary hover:text-token-text-primary']")[-1]).perform()
        title = pyperclip.paste().strip().removeprefix('"').removesuffix('"').replace(": ", " ").replace("?", "")
        print("Title: ", title)
        
        return title, script

    def GenerateVideo(self, title, script):
        time.sleep(10)

        self.actions.click(self.driver.find_element(By.XPATH, "//*[contains(text(), 'Provide a Script')]/..")).perform()
        time.sleep(0.5)
        
        self.actions.click(self.driver.find_element(By.XPATH, "//*[contains(text(), 'Select AI Speaker')]/..")).perform()
        time.sleep(0.5)

        # Select AI Speaker
        self.actions.click(WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'AI Speakers')]")))).perform()
        time.sleep(0.5)
        self.actions.click(WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Matthew')]/../../../..")))).perform()
        time.sleep(1)

        # Enter title
        self.actions.click(self.driver.find_element(By.XPATH, "//textarea[@name='title']")).perform()
        pyperclip.copy(title)
        self.actions.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
        time.sleep(1)

        # Enter script
        self.actions.click(self.driver.find_element(By.XPATH, "//textarea[@name='description']")).perform()
        pyperclip.copy(script)
        self.actions.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
        time.sleep(1)

        # Generate video
        WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Generate')]"))).click()

    def exportVideo(self):
        # Click on export
        self.actions.move_to_element(WebDriverWait(self.driver, 600).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Export')]/..")))).click().perform()
        time.sleep(1.2)

        # Click on download
        WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Download')]"))).click()

    # Function to get window handles
    def getWindowHandles(self):
        return self.driver.window_handles
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.touch_actions import TouchActions
from time import gmtime, strftime
import time
import json
import os

def scrape():
	mode = raw_input("[m]anual or [a]utomatic? ")

	if (mode == "m" or mode == "manual"):
		ingredients = []
		name = raw_input("Enter the title of the recipe: ")
		preptime = raw_input("Enter the prep time for the recipe: ")
		cooktime = raw_input("Enter the cook time for the recipe: ")
		totaltime = raw_input("Enter the total time for the recipe: ")
		servings = raw_input("Enter the number of servings: ")
		ingredient = raw_input("Enter an ingredient ('q', 'quit', 'e', or 'exit' to stop): ")
		ingredients.append(ingredient)
		while ingredient.lower() not in {'q', 'quit', 'e', 'exit'}:
			ingredient = raw_input("Enter the next ingredient: ")
			if ingredient.lower() not in {'q', 'quit', 'e', 'exit'}:
				ingredients.append(ingredient)
		invalid_input = False
	elif (mode == "a" or mode == "automatic"):
		URL = raw_input("Enter the URL to the recipe: ")
		while (URL.find("https://www.allrecipes.com/recipe/") != 0):
			print("Recipe sites supported:\nallrecipes.com\nPlease enter a valid recipe URL.\n")
			URL = raw_input("Enter the URL to the recipe: ")
		driver = webdriver.Chrome('/usr/bin/chromedriver')
		driver.get(URL)
		delay = 3
		html1 = driver.page_source
		html2 = driver.execute_script("return document.documentElement.innerHTML;")
		try:
			WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'headline-wrapper')]/h1")))
		except TimeoutException:
			print("page took too long to load")
		name = driver.find_element(By.XPATH, "//div[contains(@class, 'headline-wrapper')]/h1").text
		#first is prep, second is cook, third is additional, fourth is total, fifth is servings, sixth is yield
		nums = driver.find_elements(By.XPATH, "//div[contains(@class, 'recipe-meta-item-body')]")
		ingredients = driver.find_elements(By.XPATH, "//span[contains(@class, 'ingredients-item-name')]")
		driver.quit()
	elif mode.lower() in {'q', 'quit', 'e', 'exit'}:
		print("Goodbye")
		return
	else:
		print("Invalid input, mode must be:\nm\nmanual\na\nautomatic\n")

	while (invalid_input):
		scrape()

	file = open("Test.json", "w+")

	file.write("{\n  \"name\": \"")
	file.write(name)
	file.write("\",\n  \"prep_time\": \"")
	if (mode == "a" or mode == "automatic"):
		file.write(nums[0].text)
	else:
		file.write(preptime)
	file.write("\",\n  \"cook_time\": \"")
	if (mode == "a" or mode == "automatic"):
		file.write(nums[1].text)
	else:
		file.write(cooktime)
	file.write("\",\n  \"total_time\": \"")
	if (mode == "a" or mode == "automatic"):
		file.write(nums[3].text)
	else:
		file.write(totaltime)
	file.write("\",\n  \"servings\": \"")
	if (mode == "a" or mode == "automatic"):
		file.write(nums[4].text)
	else:
		file.write(servings)
	file.write("\",\n  \"ingredients\":{\n")

	i = 1
	for ingredient in ingredients:
		file.write("    \"")
		file.write(str(i))
		file.write("\": { \"item\": \"")
		if (mode == "a" or mode == "automatic"):
			file.write(ingredient.text.encode('utf-8'))
		else:
			file.write(ingredient)
		file.write("\"}")
		if i != len(ingredients):
			file.write(",\n")
		i = i + 1

	file.write("\n  }\n}")
	file.close()

	esurl = "http://localhost:9200/recipes3/_doc/" + strftime("%Y%m%d%H%M%S", gmtime())
	cmd = './esJson POST Test.json ' + esurl
	os.system(cmd)
	return

invalid_input = True
scrape()
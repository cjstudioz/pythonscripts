from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
driver = webdriver.Firefox()
driver.implicitly_wait(30 )
base_url = "http://www.gumtree.com/"

driver.get(base_url + "/london")
driver.find_element_by_link_text("Post an ad").click()
driver.find_element_by_id("login-username").send_keys("tongwaisin@gmail.com")
driver.find_element_by_id("login-password").send_keys("123456")
driver.find_element_by_link_text("Post an ad").click()
driver.find_element_by_css_selector("li.l1-flats-houses. > a > span").click()
driver.find_element_by_link_text("To Share").click()
driver.find_element_by_link_text("Offered").click()
driver.find_element_by_link_text("Double Room").click()
driver.find_element_by_id("category-select_submit-category").click()
driver.find_element_by_id("post-ad_postcode").clear()
driver.find_element_by_id("post-ad_postcode").send_keys("SE1 7XT")
driver.find_element_by_css_selector("em.placeholder.pseudo-p laceholder").click()
driver.find_element_by_id("location_local_area").clear()
driver.find_element_by_id("location_local_area").send_keys("Elephant Castle")
driver.find_element_by_id("post-ad_set_postcode").click()
driver.find_element_by_id("post-ad_title").click()
driver.find_element_by_id("post-ad_title").clear()
driver.find_element_by_id("post-ad_title").send_keys("top floor flat, London Eye, near city SE1 waterloo Southbank, lambeth north, london bridge")
driver.find_element_by_id("post-ad_available_date").click()
driver.find_element_by_css_selector("span.ui-icon.ui-icon-ci rcle-triangle-e").click()
driver.find_element_by_link_text("1").click()
driver.find_element_by_id("post-ad_price").clear()
driver.find_element_by_id("post-ad_price").send_keys("185")
driver.find_element_by_id("post-ad_price_frequency_2").click ()
driver.find_element_by_id("post-ad_property_type_2").click()
Select(driver.find_element_by_id("post-ad_property_room_type")).select_by_visible_text("Double")
driver.find_element_by_id("post-ad_property_couples_1").click()
driver.find_element_by_id("post-ad_seller_type_2").click()
driver.find_element_by_id("post-ad_youtubeLink").clear()
driver.find_element_by_id("post-ad_youtubeLink").send_keys("http://www.youtube.com/watch?v=MFB_tb48lyk")
driver.find_element_by_id("post-ad_description").clear()
driver.find_element_by_id("post-ad_description").send_keys("Lambeth North Tube Station at your doorstep\n** PLEASE WATCH THE VIDEO ***\n\nDouble Room is in a 2 bedroom South East Facing corner unit.\n\n3 min walk to Waterloo station\n5 min walk to South Bank\n\n\npostcode: SE1 7XT\n\nprice does not include bills\nnote: no common living room as it is being used a another room")
driver.find_element_by_id("post-ad_useEmail").click()
driver.find_element_by_id("post-ad_useEmail").click()
driver.find_element_by_id("post-ad_submit-new-advert-data").click()
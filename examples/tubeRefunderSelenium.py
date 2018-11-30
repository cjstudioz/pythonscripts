from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Firefox()
driver.implicitly_wait(30)
base_url = "https://www.tfl.gov.uk/"
verificationErrors = []
accept_next_alert = True

driver = driver
driver.get(base_url + "/tfl/tickets/refunds/tuberefund/refund.aspx?mode=oyster")
Select(driver.find_element_by_id("cphMain_ddl_Title")).select_by_visible_text("Mr")
driver.find_element_by_id("cphMain_txt_surname").clear()
driver.find_element_by_id("cphMain_txt_surname").send_keys("Chew")
driver.find_element_by_id("cphMain_txt_firstname").clear()
driver.find_element_by_id("cphMain_txt_firstname").send_keys("Kian Kiat")
driver.find_element_by_id("t_searchpostcode").clear()
driver.find_element_by_id("t_searchpostcode").send_keys("SE1 6DX")
driver.find_element_by_id("cphMain_txt_postcode").clear()
driver.find_element_by_id("cphMain_txt_postcode").send_keys("SE1 6DX")
driver.find_element_by_id("cphMain_txt_address1").clear()
driver.find_element_by_id("cphMain_txt_address1").send_keys("Apartment 384 Metro Central Heights")
driver.find_element_by_id("cphMain_txt_address3").clear()
driver.find_element_by_id("cphMain_txt_address3").send_keys("London")
driver.find_element_by_id("cphMain_txt_telephone").clear()
driver.find_element_by_id("cphMain_txt_telephone").send_keys("07778123111")
driver.find_element_by_id("cphMain_txt_email").clear()
driver.find_element_by_id("cphMain_txt_email").send_keys("tongwaisin@gmail.com")
Select(driver.find_element_by_id("cphMain_ddl_TicketType")).select_by_visible_text("Pre pay")
driver.find_element_by_id("cphMain_txt_oyster_number").clear()
driver.find_element_by_id("cphMain_txt_oyster_number").send_keys("057013249590")
driver.find_element_by_id("cphMain_rbl_oyster_cardtype_0").click()
Select(driver.find_element_by_id("cphMain_lb_lineofdelay")).select_by_visible_text("Northern")
Select(driver.find_element_by_id("cphMain_lb_startstation")).select_by_visible_text("Elephant & Castle")
Select(driver.find_element_by_id("cphMain_lb_endstation")).select_by_visible_text("St. Paul's")
Select(driver.find_element_by_id("cphMain_lb_stationofdelay")).select_by_visible_text("Elephant & Castle")
Select(driver.find_element_by_id("cphMain_calJourneyDate_ddl_day")).select_by_visible_text("6")
Select(driver.find_element_by_id("cphMain_calJourneyDate_ddl_month")).select_by_visible_text("February")
Select(driver.find_element_by_id("cphMain_calJourneyDate_ddl_year")).select_by_visible_text("2014")
Select(driver.find_element_by_id("cphMain_lb_starttime_hour")).select_by_visible_text("9")
Select(driver.find_element_by_id("cphMain_lb_starttime_minute")).select_by_visible_text("0")
Select(driver.find_element_by_id("cphMain_calDelayDate_ddl_day")).select_by_visible_text("6")
Select(driver.find_element_by_id("cphMain_calDelayDate_ddl_month")).select_by_visible_text("February")
Select(driver.find_element_by_id("cphMain_calDelayDate_ddl_year")).select_by_visible_text("2014")
Select(driver.find_element_by_id("cphMain_lb_delay_hour")).select_by_visible_text("9")
Select(driver.find_element_by_id("cphMain_lb_delay_minute")).select_by_visible_text("0")
Select(driver.find_element_by_id("cphMain_lb_delay_length_hour")).select_by_visible_text("0")
Select(driver.find_element_by_id("cphMain_lb_delay_length_minute")).select_by_visible_text("45")
driver.find_element_by_id("cphMain_chk_confirmation").click()
driver.find_element_by_id("cphMain_btn_submit").click()
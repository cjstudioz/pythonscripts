from urllib2 import urlopen
import urllib

params = {
'__EVENTARGUMENT': None,
'__EVENTTARGET': None,
'__LASTFOCUS': None,
'ctl00$cphMain$btn_submit': 'Submit',
'ctl00$cphMain$calDelayDate$ddl_day': 05,
'ctl00$cphMain$calDelayDate$ddl_month': 02,
'ctl00$cphMain$calDelayDate$ddl_year': 2014,
'ctl00$cphMain$calJourneyDate$ddl_day': 31,
'ctl00$cphMain$calJourneyDate$ddl_month': 01,
'ctl00$cphMain$calJourneyDate$ddl_year': 2014,
'ctl00$cphMain$chk_confirmation': 'on',
'ctl00$cphMain$ddl_TicketType': 'Annual',
'ctl00$cphMain$ddl_Title': 'Mr',
'ctl00$cphMain$dll_oyster_refundpaymentmethod': 'Credit voucher',
'ctl00$cphMain$lb_delay_hour': 9,
'ctl00$cphMain$lb_delay_length_hour': 0,
'ctl00$cphMain$lb_delay_length_minute': 16,
'ctl00$cphMain$lb_delay_minute': 0,
'ctl00$cphMain$lb_endstation': "St. Paul's",
'ctl00$cphMain$lb_lineofdelay': 'Central',
'ctl00$cphMain$lb_startstation': 'Elephant & Castle',
'ctl00$cphMain$lb_starttime_hour': 9,
'ctl00$cphMain$lb_starttime_minute': 0,
'ctl00$cphMain$lb_stationofdelay': 'Bank',
'ctl00$cphMain$lb_stationofdelay1': None,
'ctl00$cphMain$lb_stationofdelay2': None,
'ctl00$cphMain$rbl_oyster_cardtype': 'Adult',
'ctl00$cphMain$txt_address1': 'Apartment 384 Metro Central Heights',
'ctl00$cphMain$txt_address2': None,
'ctl00$cphMain$txt_address3': 'London',
'ctl00$cphMain$txt_email': None,
'ctl00$cphMain$txt_firstname': 'Lee',
'ctl00$cphMain$txt_oyster_number': '057460741101',
'ctl00$cphMain$txt_photocard': None,
'ctl00$cphMain$txt_postcode': 'Se1 6dx',
'ctl00$cphMain$txt_surname': 'Cj',
'ctl00$cphMain$txt_telephone': '07986187124',
}


url = 'https://www.tfl.gov.uk/tfl/tickets/refunds/tuberefund/refund.aspx?mode=oyster' #HTTP/1.1

header = {
'Host': 'www.tfl.gov.uk',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language': 'en-US,en;q=0.5',
'Accept-Encoding': 'gzip, deflate',
'Referer': 'https://www.tfl.gov.uk/tfl/tickets/refunds/tuberefund/refund.aspx?mode=oyster',
}

data = urllib.urlencode(params)
pagehandle = urlopen(url, data=data)
res = pagehandle.read()
f = open("c:/temp/tubeREfund.HTML", 'w') 
f.write(res)

GENDER = [
	('m', 'Male'),
	('f', 'Female'),
	('o', 'Other')
]

RACE = [
	('white', 'White'),
	('black', 'Black / African American'),
	('indian', 'American Indian / Alaskan Native'),
	('asian', 'Asian'),
	('islander', 'Native Hawaiian / Pacific Islander'),
	('other','Other')
]

EDUCATION = [
	('none', 'No Highschool'),
	('hsdiploma', 'Highschool Diploma'),
	('ged', 'GED'),
	('associates', 'Associate Degree'),
	('bachelors', 'Bachelors Degree'),
	('masters', 'Masters Degree'),
	('phd', 'PhD / Doctorates Degree')
]

EMPLOYMENT_STATUS = [
	('unemployable', 'Unemployable'),
	('unemployed', 'Unemployed'),
	('part', 'Part-time'),
	('full','Full-time'),
	('retired','Retired')]

INDUSTRY = [
	('accounting','Accounting/Finance'),
	('administrative','Administrative'),
	('advertising','Advertising'),
	('airlines','Airlines/Avionics/Aerospace'),
	('architectural','Architectural'),
	('banking','Banking/Finance'),
	('biotechnology','Biotechnology'),
	('construction','Civil/Construction'),
	('engineering','Engineering'),
	('communication','Communications'),
	('computer','Computer/IT'),
	('software','Software Development'),
	('contract','Consultant/Contractual'),
	('csrservice','Customer Service'),
	('defense','Defense'),
	('design','Design'),
	('education','Education'),
	('ee','Electrical Engineering'),
	('electronics','Electronics Engineering'),
	('energy','Energy'),
	('environment','Environmental/Safety'),
	('fundraising','Fundraising'),
	('medicine','Health/Medicine/Medical'),
	('hr','Human Resources'),
	('insurance','Insurance'),
	('legal','Legal'),
	('transportation','Logistics/Transportation'),
	('maintenance','Maintenance'),
	('management','Management'),
	('student','Student'),
	('warehouse','Manufacturing/Warehouse'),
	('marketing','Marketing')
]

MARITAL_STATUS = [
	('single','Single'),
	('relationship','In a relationship'),
	('married','Married'),
	('complicated','Complicated'),
	('widowed','Widowed')
]

ORIENTATION = [
	('straight','Straight'),
	('bi','Bisexual'),
	('gay','Homosexual')
]

MBTI = [
	('ISTJ','ISTJ'),
	('ISFJ','ISFJ'),
	('INFJ','INFJ'),
	('INTJ','INTJ'),
	('ISTP','ISTP'),
	('ISFP','ISFP'),
	('INFP','INFP'),
	('INTP','INTP'),
	('ESTP','ESTP'),
	('ESFP','ESFP'),
	('ENFP','ESFP'),
	('ENTP','ENTP'),
	('ESTJ','ESTJ'),
	('ESFJ','ESFJ'),
	('ENFJ','ENFJ'),
	('ENTJ','ENTJ')
]

INCOME_LEVEL = [
	('1','0 - 10,000'),
	('2','10,000 - 20,000'),
	('3','20,000 - 30,000'),
	('4','30,000 - 40,000'),
	('5','40,000 - 50,000'),
	('6','50,000 - 60,000'),
	('7','60,000 - 70,000'),
	('8','70,000 - 80,000'),
	('9','80,000 - 90,000'),
	('10','100,000 - 200,000'),
	('11','200,000+')
]

METRICS = [
	('US', 'US Metric (lbs,ft,in)'),
	('SI', 'SI metric (kg,m)')
]

TIMEZONES = [
		('-12', '(GMT -12:00 hours) Eniwetok, Kwajalein'), 
		('-11', '(GMT -11:00 hours) Midway Island, Samoa'), 
		('-10', '(GMT -10:00 hours) Hawaii'), 
		('-9', '(GMT -9:00 hours) Alaska'), 
		('-8', '(GMT -8:00 hours) Pacific Time (US & Canada)'), 
		('-7', '(GMT -7:00 hours) Mountain Time (US & Canada)'), 
		('-6', '(GMT -6:00 hours) Central Time (US & Canada), Mexico City'), 
		('-5', '(GMT -5:00 hours) Eastern Time (US & Canada), Bogota, Lima, Quito'), 
		('-4', '(GMT -4:00 hours) Atlantic Time (Canada), Caracas, La Paz'), 
		('-3.5', '(GMT -3:30 hours) Newfoundland'), 
		('-3', '(GMT -3:00 hours) Brazil, Buenos Aires, Georgetown'), 
		('-2', '(GMT -2:00 hours) Mid-Atlantic'), 
		('-1', '(GMT -1:00 hours) Azores, Cape Verde Islands'), 
		('0', '(GMT) Western Europe Time, London, Lisbon, Casablanca, Monrovia'), 
		('+1', '(GMT +1:00 hours) CET(Central Europe Time), Brussels, Copenhagen, Madrid, Paris'), 
		('+2', '(GMT +2:00 hours) EET(Eastern Europe Time), Kaliningrad, South Africa'), 
		('+3', '(GMT +3:00 hours) Baghdad, Kuwait, Riyadh, Moscow, St. Petersburg, Volgograd, Nairobi'), 
		('+3.5', '(GMT +3:30 hours) Tehran'), 
		('+4', '(GMT +4:00 hours) Abu Dhabi, Muscat, Baku, Tbilisi'), 
		('+4.5', '(GMT +4:30 hours) Kabul'), 
		('+5', '(GMT +5:00 hours) Ekaterinburg, Islamabad, Karachi, Tashkent'), 
		('+5.5', '(GMT +5:30 hours) Bombay, Calcutta, Madras, New Delhi'), 
		('+6', '(GMT +6:00 hours) Almaty, Dhaka, Colombo'), 
		('+7', '(GMT +7:00 hours) Bangkok, Hanoi, Jakarta'), 
		('+8', '(GMT +8:00 hours) Beijing, Perth, Singapore, Hong Kong, Chongqing, Urumqi, Taipei'), 
		('+9', '(GMT +9:00 hours) Tokyo, Seoul, Osaka, Sapporo, Yakutsk'), 
		('+9.5', '(GMT +9:30 hours) Adelaide, Darwin'), 
		('+10', '(GMT +10:00 hours) EAST(East Australian Standard), Guam, Papua New Guinea, Vladivostok'), 
		('+11', '(GMT +11:00 hours) Magadan, Solomon Islands, New Caledonia'), 
		('+12', '(GMT +12:00 hours) Auckland, Wellington, Fiji, Kamchatka, Marshall Island')
]

DATEDISPLAY = [
	('mm/dd/yyyy','05/24/1985'),
	('mm.dd.yyyy','05.24.1985'),
	('mm-dd-yyyy','05-24-1985'),
	('yyyy/mm/dd','1985/05/24'),
	('yyyy.mm.dd','1985.05.24'),
	('yyyy-mm-dd','1985-05-24'),
	('dd/mm/yyyy','24/05/1985'),
	('dd-mm-yyyy','24-05-1985'),
	('dd.mm.yyyy','24.05.1985'),
]

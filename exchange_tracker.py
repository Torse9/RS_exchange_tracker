#http://services.runescape.com/m=itemdb_rs/Rune_platebody/viewitem?obj=1127
# import webpage to txtfile. Search for "average180.push([new Date('YYYY/MM/DD'), DAILYVALUE, AVERAGEVALUE]);" 
# Apply to variable, save to txt file.(html?)

# REMEMBER TO PUT FORLOOP ON EVERYTHING,
# Make sure date is good in catch_in_file func also check if for line can be replacedf with forloop func.


#V1.0
#1.0 Completed the Exchange_Table and worked out the known bugs. I'd like to call this V1.0 as this is what I initially wanted. But more are gonna be added all the time.
#0.9.1 Created forloop func to shorten the code as the for loop was appearing several times and could easily be replaced. Some bugfixes.
#0.9 Implemented a common area where all the prices for the day is. TO COME: Last weeks prices and percentage based rise/decrease
#0.8.55 Changed the logs to be one line so we can find values based on date easier.
#0.8.5 Added proper error handling in check to see if todays date are not yet in tmp file to avoid program crash.
#0.8 Added tons of variables so that you can run several items.
#0.7 added price increase or decrease per day.

import os
from os import system
import urllib2
import re
import datetime


exc = "Items\exchange_table.txt"
tmp = "tmp.txt"
urlist = ["Items\Rune_platebody.txt", "http://services.runescape.com/m=itemdb_rs/Rune_platebody/viewitem?obj=1127", #0,1
		  "Items\Rune_platelegs.txt", "http://services.runescape.com/m=itemdb_rs/Rune_platelegs/viewitem?obj=1079", #2,3
		  "Items\Rune_helm.txt"     , "http://services.runescape.com/m=itemdb_rs/Rune_helm/viewitem?obj=1147"	  , #4,5
		  "Items\Rune_full_helm.txt", "http://services.runescape.com/m=itemdb_rs/Rune_full_helm/viewitem?obj=1163", #6,7
		  "Items\Rune_chainbody.txt", "http://services.runescape.com/m=itemdb_rs/Rune_chainbody/viewitem?obj=1113", #8,9
		  "Items\Nature_rune.txt"   , "http://services.runescape.com/m=itemdb_rs/Nature_rune/viewitem?obj=561"	  , #10,11
		  "Items\Fire_rune.txt"     , "http://services.runescape.com/m=itemdb_rs/Fire_rune/viewitem?obj=554"      ] #12,13
#Need to catch urlist from outside function, drag the parametres through the process.

def forloop(objective, date, path):
	for line in openfile(path, 3):
		if objective in line:
			fished = map(int, re.findall(r'\d+', line))
			return fished
		elif date in line:
			fished = map(int, re.findall(r'\d+', line))
			return fished

def catch_in_file(path):
	today = datetime.date.today().strftime("%Y/%m/%d")
	ydayv = datetime.date.today()-datetime.timedelta(days=1)
	ydays = ydayv.strftime("%Y/%m/%d")	

	for line in openfile(path,3):
		
		if today in line:
			caught = map(int, re.findall(r'\d+', line))
			del caught[0:3]
			oldprice = anytime(path, datetime.date.today())
			dperc = pincdec(caught[0], oldprice[0])
			wperc = pincdec(caught[0], oldprice[1])
			mperc = pincdec(caught[0], oldprice[2])
			three_mperc = pincdec(caught[0], oldprice[3])
			if oldprice[4] != 0:
				six_mperc = pincdec(caught[0], oldprice[4])
			else:
				# It seems that any new item added to the list will not be able to show 180 days percentage.
				six_mperc = "ERROR"
			return (caught[0], oldprice[0], dperc, oldprice[1],
			wperc, oldprice[2], mperc, oldprice[3],
			three_mperc, oldprice[4], six_mperc)

	caught = forloop("#", ydays, path)
	del caught[0:3]
	print("{0} is not yet in tmp").format(today)
	oldprice = anytime(path, ydayv)
	dperc = pincdec(caught[0], oldprice[0])
	wperc = pincdec(caught[0], oldprice[1])
	mperc = pincdec(caught[0], oldprice[2])
	three_mperc = pincdec(caught[0], oldprice[3])
	if oldprice[4] != 0:
		six_mperc = pincdec(caught[0], oldprice[4])
	else:
		# It seems that any new item added to the list will not be able to show 180 days percentage.
		six_mperc = "ERROR"
	return (caught[0], oldprice[0], dperc, oldprice[1],
			wperc, oldprice[2], mperc, oldprice[3],
			three_mperc, oldprice[4], six_mperc)

def anytime(path, date):
	ddato = date - datetime.timedelta(days=1)
	wdato = date - datetime.timedelta(days=7)
	mdato = date - datetime.timedelta(days=30)
	three_mdato = date - datetime.timedelta(days=90)
	six_mdato = date - datetime.timedelta(days=180)
	dprice = forloop("#", ddato.strftime("%Y/%m/%d"), path)
	wprice = forloop("#", wdato.strftime("%Y/%m/%d"), path)
	mprice = forloop("#", mdato.strftime("%Y/%m/%d"), path)
	three_mprice = forloop("#", three_mdato.strftime("%Y/%m/%d"), path)
	six_mprice = forloop("#", six_mdato.strftime("%Y/%m/%d"), path)
	if six_mprice == None:
		six_mprice = [0, 0, 0, 0, 0]
	del dprice[0:3], wprice[0:3], mprice[0:3], three_mprice[0:3], six_mprice[0:3]
	return dprice[0], wprice[0], mprice[0], three_mprice[0], six_mprice[0]

# filname: 0 == tmp, 1 == Rune_platebody
def openfile(filname, value):
	if value == 0: #Read only
		with open(filname, "r") as file:
			file = file.read()
	elif value == 1:		#if value == 1, Append
		file = open(filname, "a")
	elif value == 2:		# if value == 2, Write
		file = open(filname, "w")
	elif value == 3:		# if value == 3, Read while open
		file = open(filname, "r")
		
	return file


#Checks if the current date is already in file or if it is not in tmp.txt. If not it will append template with current values.
def check(this_date, file):	
	if this_date in openfile(file, 0):
			print("{0} is already in txt").format(this_date)
			return 0
	
	elif this_date not in openfile(tmp, 0):
		print ("{0} is not yet in {1}").format(this_date, tmp)
		return 0
	
	else:
		return 1

def catch_date(filedate, file):
	msg = ("{0}").format(filedate)
	gotcha = forloop(msg, "#", file)
	del gotcha[0:4]
	return gotcha
# Maps the digits into a tuple and removes text. Also removes digits in index range 0-4.

def request(site):
	req = urllib2.Request (site)
	response = urllib2.urlopen(req)
	the_page = response.read()
	return the_page

#To calculate the percentage increase: First: work out the difference (increase) 
#between the two numbers you are comparing. Then: divide the increase by the original
#number and multiply the answer by 100. If your answer is a negative number then this is
#a percentage decrease.
def pincdec(nprice, oprice):
	perc = float(nprice) - float(oprice)
	perc = perc / oprice
	perc = perc * 100 
	return int(perc)

#Search the tmp file for todays date and catches the line in a variable.

def process(item, path):
	# Get the html from specified page
	answer = request(path)

	#Open a tmp file and writes the html from the page

	txt = openfile(tmp,2).write(answer)

	date = datetime.date.today() - datetime.timedelta(days=180)
	for i in range(180): 
		date += datetime.timedelta(days=1)
		date_prn = date.strftime("%Y/%m/%d")
		if check(date_prn, item) == 1:
			if catch_date(date_prn, tmp) == 1:
				print("Date is not in the file yet.")
				pass
			else:
				catched = catch_date(date_prn, tmp)
				
				ndate = date - datetime.timedelta(days=1)
				ndate = ndate.strftime("%Y/%m/%d")
				
				subdate = catch_date(ndate, tmp)
				if subdate == []:
					subdate = [0,0] # Deliver Default value in case there is no date to subtract from to avoid program crash
			#Template for each value to be written in a text file

				template ="""{0}	Current Value: {1}	Incr or Decr: {2}
__________________________________________________________________

	""".format(date_prn, catched[0], catched[0] - subdate[0])
				
				openfile(item, 1).write(template)
				
		#Search the respective file for the date. If the date exists continue, if not paste in

#DD/MM/YYYY
# Current Value:
# ??????
# Incr or Decr:
# +- ??
# ______________

process(urlist[0], urlist[1])
process(urlist[12], urlist[13])
process(urlist[2], urlist[3])
process(urlist[4], urlist[5])
process(urlist[6], urlist[7])
process(urlist[8], urlist[9])
process(urlist[10],urlist[11])



#[0]TODAY, [1]YESTERDAY, [2]PERCENTAGE
#[3]LAST WEEK, [4]LASTWEEK_PERCENTAGE
#[5]LAST MONTH, [6]LASTMONTH_PERCENTAGE
#[7]THREE MONTH, [8]LAST3MONTH_PERCENTAGE
#[9]SIX MONTH, , [10]LAST6MONTH_PERCENTAGE

nat_run = catch_in_file(urlist[10])
fir_run = catch_in_file(urlist[12])
run_plat = catch_in_file(urlist[0])
run_chain = catch_in_file(urlist[8])
run_fhelm = catch_in_file(urlist[6])
run_plegs = catch_in_file(urlist[2])
run_helm = catch_in_file(urlist[4])


def exchange_table(table_item, Name):
	table = """
|------------------------------|
|   ________________
|   |Name0|
|   ----------------
|      TODAY
|   {Name1}: {N0}gp
|
|     IC/DC: {N1}gp [{N2}%]
|
|       WEEK
|   {Name2}: {N3}gp
|
|     IC/DC: {N4}gp [{N5}%]
|
|       MONTH
|   {Name3}: {N6}gp
|
|     IC/DC: {N7}gp [{N8}%]
|
|       THREE MONTHS
|   {Name4}: {N9}gp
|
|     IC/DC: {N10}gp [{N11}%]
|
|       SIX MONTHS
|   {Name5}: {N12}gp
|
|     IC/DC: {N13}gp [{N14}%]""".format(Name0=Name, Name1=Name, Name2=Name, Name3=Name, Name4=Name, Name5=Name,

										N0=table_item[0], N1=table_item[0] - table_item[1], N2=table_item[2],
										N3=table_item[3], N4=table_item[0] - table_item[3], N5=table_item[4],
										N6=table_item[5], N7=table_item[0] - table_item[5], N8=table_item[6],
										N9=table_item[7], N10=table_item[0] - table_item[7], N11=table_item[8],
										N12=table_item[9], N13=table_item[0] - table_item[9], N14=table_item[10])









exchange_table ="""
|------------------------------|
|   _____________
|   |NATURE RUNE|
|   -------------
|      TODAY
|   Nature Rune: {N0}gp
|
|     IC/DC: {N1}gp [{N2}%]
|
|       WEEK
|   Nature Rune: {N3}gp
|
|     IC/DC: {N4}gp [{N5}%]
|
|       MONTH
|   Nature Rune: {N6}gp
|
|     IC/DC: {N7}gp [{N8}%]
|
|       THREE MONTHS
|   Nature Rune: {N9}gp
|
|     IC/DC: {N10}gp [{N11}%]
|
|       SIX MONTHS
|   Nature Rune: {N12}gp
|
|     IC/DC: {N13}gp [{N14}%]
|------------------------------|
|   _____________
|   |FIRE RUNE  |
|   -------------
|      TODAY
|   Fire Rune: {F0}gp
|
|     IC/DC: {F1}gp [{F2}%]
|
|       WEEK
|   Fire Rune: {F3}gp
|
|     IC/DC: {F4}gp [{F5}%]
|
|       MONTH
|   Fire Rune: {F6}gp
|
|     IC/DC: {F7}gp [{F8}%]
|
|       THREE MONTHS
|   Fire Rune: {F9}gp
|
|     IC/DC: {F10}gp [{F11}%]
|
|       SIX MONTHS
|   Fire Rune: {F12}gp
|
|     IC/DC: {F13}gp [{F14}%]
|------------------------------|
|   ________________
|   |RUNE PLATEBODY|
|   ----------------
|      TODAY
|   Rune Platebody:{PB0}gp
|
|     IC/DC: {PB1}gp [{PB2}%]
|
|       WEEK
|   Rune Platebody:{PB3}gp
|
|     IC/DC: {PB4}gp [{PB5}%]
|
|       MONTH
|   Rune Platebody:{PB6}gp
|
|     IC/DC: {PB7}gp [{PB8}%]
|
|       THREE MONTHS
|   Rune Platebody:{PB9}gp
|
|     IC/DC: {PB10}gp [{PB11}%]
|
|       SIX MONTHS
|   Rune Platebody: {PB12}gp
|
|     IC/DC: {PB13}gp [{PB14}%]
|------------------------------|
|   ________________
|   |RUNE CHAINBODY|
|   ----------------
|      TODAY
| Rune Chainbody:{RC0}gp
|
|     IC/DC: {RC1}gp [{RC2}%]
|
|       WEEK
| Rune Chainbody:{RC3}gp
|
|     IC/DC: {RC4}gp [{RC5}%]
|
|       MONTH
| Rune Chainbody:{RC6}gp
|
|     IC/DC: {RC7}gp [{RC8}%]
|
|       THREE MONTHS
| Rune Chainbody: {RC9}gp
|
|     IC/DC: {RC10}gp [{RC11}%]
|
|       SIX MONTHS
| Rune Chainbody: {RC12}gp
|
|     IC/DC: {RC13}gp [{RC14}%]
|------------------------------|
|   ________________
|   |RUNE FULL HELM|
|   ----------------
|      TODAY
| Rune full helm:{FH0}gp
|
|     IC/DC: {FH1}gp [{FH2}%]
|
|       WEEK
| Rune full helm:{FH3}gp
|
|     IC/DC: {FH4}gp [{FH5}%]
|
|       MONTH
| Rune full helm:{FH6}gp
|
|     IC/DC: {FH7}gp [{FH8}%] 
|
|       THREE MONTHS
| Rune full helm: {FH9}gp
|
|     IC/DC: {FH10}gp [{FH11}%]
|
|       SIX MONTHS
| Rune full helm: {FH12}gp
|
|     IC/DC: {FH13}gp [{FH14}%]
|------------------------------|
|   ________________
|   |RUNE PLATELEGS|
|   ----------------
|      TODAY
| Rune Platelegs:{PL0}gp
|
|     IC/DC: {PL1}gp [{PL2}%]
|
|       WEEK
| Rune Platelegs:{PL3}gp
|
|     IC/DC: {PL4}gp [{PL5}%]
|
|       MONTH
| Rune Platelegs:{PL6}gp
|
|     IC/DC: {PL7}gp [{PL8}%]
|
|       THREE MONTHS
| Rune Platelegs: {PL9}gp
|
|     IC/DC: {PL10}gp [{PL11}%]
|
|       SIX MONTHS
| Rune Platelegs: {PL12}gp
|
|     IC/DC: {PL13}gp [{PL14}%]
|------------------------------|
|   ___________
|   |RUNE HELM|
|   -----------
|      TODAY
|   Rune helm: 	 {RH0}gp
|
|     IC/DC: {RH1}gp [{RH2}%]
|
|       WEEK
|   Rune helm: 	 {RH3}gp
|
|     IC/DC: {RH4}gp [{RH5}%]
|
|       MONTH
|   Rune helm: 	 {RH6}gp
|
|     IC/DC: {RH7}gp [{RH8}%]
|
|       THREE MONTHS
|   Rune helm: {RH9}gp
|
|     IC/DC: {RH10}gp [{RH11}%]
|
|       SIX MONTHS
|   Rune helm: {RH12}gp
|
|     IC/DC: {RH13}gp [{RH14}%]
|------------------------------|""".format(
	N0=nat_run[0], N1=nat_run[0] - nat_run[1], N2=nat_run[2], #TODAY, TODAY - YESTERDAY, PERCENTAGE
	N3=nat_run[3], N4=nat_run[0] - nat_run[3], N5=nat_run[4], #LAST WEEK, TODAY - LAST WEEK, PERCENTAGE
	N6=nat_run[5], N7=nat_run[0] - nat_run[5], N8=nat_run[6], #LAST MONTH, TODAY - LAST MONTH, PERCENTAGE
	N9=nat_run[7], N10=nat_run[0] - nat_run[7], N11=nat_run[8], # THREE MONTH, TODAY - THREE MONTH, PERCENTAGE
	N12=nat_run[9], N13=nat_run[0] - nat_run[9], N14=nat_run[10], #SIX MONTH, TODAY - SIX MONTH, PERCENTAGE 

	F0=fir_run[0], F1=fir_run[0] - fir_run[1], F2=fir_run[2],
	F3=fir_run[3], F4=fir_run[0] - fir_run[3], F5=fir_run[4],
	F6=fir_run[5], F7=fir_run[0] - fir_run[5], F8=fir_run[6],
	F9=fir_run[7], F10=fir_run[0] - fir_run[7], F11=fir_run[8],
	F12=fir_run[9], F13=fir_run[0] -fir_run[9], F14=fir_run[10],

	PB0=run_plat[0], PB1=run_plat[0] - run_plat[1], PB2=run_plat[2],
	PB3=run_plat[3], PB4=run_plat[0] - run_plat[3], PB5=run_plat[4],
	PB6=run_plat[5], PB7=run_plat[0] - run_plat[5], PB8=run_plat[6],
	PB9=run_plat[7], PB10=run_plat[0] - run_plat[7], PB11=run_plat[8],
	PB12=run_plat[9], PB13=run_plat[0] - run_plat[9], PB14=run_plat[10],

	RC0=run_chain[0], RC1=run_chain[0] - run_chain[1], RC2=run_chain[2],
	RC3=run_chain[3], RC4=run_chain[0] - run_chain[3], RC5=run_chain[4],
	RC6=run_chain[5], RC7=run_chain[0] - run_chain[5], RC8=run_chain[6],
	RC9=run_chain[7], RC10=run_chain[0] - run_chain[7], RC11=run_chain[8],
	RC12=run_chain[9], RC13=run_chain[0] - run_chain[9], RC14=run_chain[10],

	FH0=run_fhelm[0], FH1=run_fhelm[0] - run_fhelm[1], FH2=run_fhelm[2],
	FH3=run_fhelm[3], FH4=run_fhelm[0] - run_fhelm[3], FH5=run_fhelm[4],
	FH6=run_fhelm[5], FH7=run_fhelm[0] - run_fhelm[5], FH8=run_fhelm[6],
	FH9=run_fhelm[7], FH10=run_fhelm[0] - run_fhelm[7], FH11=run_fhelm[8],
	FH12=run_fhelm[9], FH13=run_fhelm[0] - run_fhelm[9], FH14=run_fhelm[10],

	PL0=run_plegs[0], PL1=run_plegs[0] - run_plegs[1], PL2=run_plegs[2],
	PL3=run_plegs[3], PL4=run_plegs[0] - run_plegs[3], PL5=run_plegs[4],
	PL6=run_plegs[5], PL7=run_plegs[0] - run_plegs[5], PL8=run_plegs[6],
	PL9=run_plegs[7], PL10=run_plegs[0] - run_plegs[7], PL11=run_plegs[8],
	PL12=run_plegs[9], PL13=run_plegs[0] - run_plegs[9], PL14=run_plegs[10],

	RH0=run_helm[0], RH1=run_helm[0] - run_helm[1], RH2=run_helm[2],
	RH3=run_helm[3], RH4=run_helm[0] - run_helm[3], RH5=run_helm[4],
	RH6=run_helm[5], RH7=run_helm[0] - run_helm[5], RH8=run_helm[6],
	RH9=run_helm[7], RH10=run_helm[0] - run_helm[7], RH11=run_helm[8],
	RH12=run_helm[9], RH13=run_helm[0] - run_helm[9], RH14=run_helm[10])

openfile(exc, 2).write(exchange_table)
os.system("start " + exc)
exit(0)
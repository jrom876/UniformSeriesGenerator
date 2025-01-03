#!/usr/bin/python3

# PROJECT		intCalc
# FILE			top_gui.py
# DESIGNER		Jacob Romero 
#			Creative Engineering Solutions, LLC

#### This Project has four parts:

# 	0.	To provide methods for iterating through the interest calculator
#		equations defined below and generate raw data suitable for csv files.

# 	1.	To generate various csv files from the raw data.

# 	2.	To provide a tkinter GUI for easy UI and UX with this class.

# 	3.	To provide unittest methods for development and maintenance.

#### Input Parameters:

# 	F		Future Value
#	P		Present Value
#	A		Payment, end-of-period cash receipt, or disbursement
# 	i		Interest rate per period
# 	n		Number of years 
#	per		Number of interest periods per year

#### Equations:

# Series Future Value, find F given A:	
# Series Future Value is the total amount which will be accrued or repaid (F)
# given a uniform series of disbursements (A) over n periods.
#		F = A*((((1+i)**n)-1)/i)

# Series Present Worth, find P given A:		
# Series Present Worth is the present value (P) of an annuity given
# a uniform series of disbursements (A) over n periods.	
#		P = A*((((1+i)**n)-1)/(i*((1+i)**n)))

# Sinking Fund, find A given F:
# A Sinking Fund is when you deposit a uniform series of amounts (A) 
# to accumulate a desired future amount (F) by the end of period n.		
#		A = F*(i/(((1+i)**n)-1))

# Capital Recovery, find A given P:
# Capital Recovery is how big an annual return (A) has to be in order to
# recover the initial investment amount (P) by the end of period n.		
#		P = A*((i*((1+i)**n))/(((1+i)**n)-1))

#### References:
## https://www.activestate.com/resources/quick-reads/how-to-display-data-in-a-table-using-tkinter/
## https://www.python-course.eu/tkinter_entry_widgets.php     
#################################
####### IMPORT STATEMENTS #######
import os
import csv
import sys
import time
import math
import struct
import numpy as np
import pandas as pd
from csv import reader
from csv import writer
from csv import DictReader
import tkinter as tk
# import tkinter as tki
from tkinter import *
import datetime as datetime
try:
    import tkMessageBox
except ImportError:  # Python 3
    import tkinter.messagebox as tkMessageBox

from sinkingFund import *
#from messagebox2 import *
from interestCalc import *
from capitalRecovery import*
#############################################
############### TKINTER SETUP ###############
root = tk.Tk()
root.title("Interest Calculator GUI Version 0.0.1")
#root.geometry("1200x750")
root.geometry("1000x500")
#root.geometry("1200x900")
column_size = 60
row_size = 25
#rootmsg = Tk() 
#rootmsg.geometry("300x200") 
#############################################
################## GLOBALS ##################
GLOBAL_F = 0.0
GLOBAL_P = 0
GLOBAL_A  = 0.0
GLOBAL_int = 0.0001
GLOBAL_num = 1
GLOBAL_per = 1
GLOBAL_TUPLE = (0,0,0,0,0,0)
GLOBAL_LIST = [0,0,0,0]
#################################
####### CLASS DECLARATION #######
class CSV_Writer:
	def __init__(self, fv=0, pw=0, pmt=0, i=0.001, n=1, per=1):
		self.F	 	= fv 	if fv>=0 else 0
		self.P	 	= pw 	if pw>=0 else 0
		self.A	 	= pmt 	if pmt>=0 else 0
		self.int 	= i 	if i>0 else 0.001
		self.num 	= n 	if n>=1 else 1
		self.per	= per	if per>=1 else 1
		
		self.tuple 	= (fv,pw,pmt,i,n,per)
		self.list 	= [fv,pw,pmt,i,n,per]
		self.olist	= [fv,pw,n]
		self.printlist 	= [round(fv,2),round(pw,2),round(pmt,2),round(i,6),n,per]
		
		self.compound = fv*((1+(i/per))**(n*per))
		self.pworth = pw*((1+(i/per))**(n*per*(-1)))
		self.futvalue = pmt*((((1+(i/per))**(n*per))-1)/(i/per))		
		self.presentWorth = pmt*(((math.pow((1+(i/per)),(n*per)))-1)/((i/per)*(math.pow((1+(i/per)),(n*per)))))		
		self.sinkFund = fv*((i/per)/(((1+(i/per))**(n*per))-1))
		self.capRecovery = pw*(((i/per)*(math.pow((1+(i/per)),(n*per))))/((math.pow((1+(i/per)),(n*per))-1)))
		
		# print('CSV Writer list = {0}'.format(self.printlist))	
		# print('compound = {0:.2f}'.format(self.compound))	
		# print('pworth = {0:.2f}'.format(self.pworth))
		# print('futvalue = \t{0:.2f}'.format(self.futvalue))	
		# print('presentWorth = \t{0:.2f}'.format(self.presentWorth))	
		# print('sinkingFund = \t{0:.2f}'.format(self.sinkFund))	
		# print('capRecovery = \t{0:.2f}'.format(self.capRecovery))		

        # def __del__(self):
            # print("Destructor called")	
	
####################################
##<<<<<<<<< WE ARE NOW >>>>>>>>>>>##
##<<<<< OUTSIDE OF THE CLASS >>>>>##
####################################
########## Create Labels ##########
F_in_label   = tk.Label(root, text="FV")
P_in_label   = tk.Label(root, text="PW")
A_in_label   = tk.Label(root, text="PMT")
int_in_label = tk.Label(root, text="INT")
num_in_label = tk.Label(root, text="NUM")
per_in_label = tk.Label(root, text="PER")

######### Output Labels ##########
fv_out_label = tk.StringVar()
fv_out_label_text = tk.StringVar()
fv_out_label_text.set("set input")
fv_out_label = tk.Label(root, textvariable=fv_out_label_text, width=8)
fv_out_label.grid(row=0, column=1)

####################################################
############### Button Declarations ################
gen_csv_button = tk.Button(text="Gen CSV",
		command=lambda: gen_csv_cmd(), width=13)
                    
gen_off_button = tk.Button(text="Show CSV", 
		# ~ command=lambda: gen_test_cmd(), width=13)
		command=lambda: gen_test_cmd2(), width=13)                     

gen_csv_button.grid(row=0,  column=0)
gen_off_button.grid(row=1,  column=0)

####################################################
################ Entry Declarations ################

Fset = 		tk.StringVar()
Pset = 		tk.StringVar()
Aset = 		tk.StringVar()
intset = 	tk.StringVar()
numset = 	tk.StringVar()
perset = 	tk.StringVar()

Fset_entry = 	tk.Entry(root, textvariable=Fset, width=10)
Pset_entry = 	tk.Entry(root, textvariable=Pset,  width=10)
Aset_entry = 	tk.Entry(root, textvariable=Aset, width=10)
intset_entry = 	tk.Entry(root, textvariable=intset, width=10)
numset_entry = 	tk.Entry(root, textvariable=numset, width=10)
perset_entry = 	tk.Entry(root, textvariable=perset, width=10)

Fset.set(0.0)
Pset.set(250000)
Aset.set(0.0)
intset.set(0.03)
numset.set(10)
perset.set(1)

Fset_entry.grid		(row=1,  column=1)
Pset_entry.grid		(row=2,  column=1)
Aset_entry.grid		(row=3,  column=1)
intset_entry.grid   	(row=4,  column=1)
numset_entry.grid 	(row=5,  column=1)
perset_entry.grid 	(row=6,  column=1)

###########
F_val		 = tk.StringVar()
P_val		= tk.StringVar()
A_va		= tk.StringVar()
int_val 	= tk.StringVar()
num_val		= tk.StringVar()
per_val		= tk.StringVar()

F_val_label_text = tk.StringVar()
F_val_label_text.set("0")
F_val_label = tk.Label(root, textvariable=F_val_label_text, width=10)
F_val_label.grid(row=1, column=4)

P_val_label_text = tk.StringVar()
P_val_label_text.set("0")
P_val_label = tk.Label(root, textvariable=P_val_label_text, width=10)
P_val_label.grid(row=1, column=5)

A_val_label_text = tk.StringVar()
A_val_label_text.set("0")
A_val_label = tk.Label(root, textvariable=A_val_label_text, width=10)
A_val_label.grid(row=1, column=6)

int_val_label_text = tk.StringVar()
int_val_label_text.set("0.0001")
int_val_label = tk.Label(root, textvariable=int_val_label_text, width=10)
int_val_label.grid(row=1, column=7)

num_val_label_text = tk.StringVar()
num_val_label_text.set("1")
num_val_label = tk.Label(root, textvariable=num_val_label_text, width=10)
num_val_label.grid(row=1, column=8)

per_val_label_text = tk.StringVar()
per_val_label_text.set("1")
per_val_label = tk.Label(root, textvariable=per_val_label_text, width=10)
per_val_label.grid(row=1, column=9)

################### Functions and Commands ################### 

################### Button Commands ####################
def gen_csv_cmd():
	#cw1 = CSV_Writer(0,25000,0,0.03,10,12)
	cw1 = CSV_Writer(float(Fset.get()),
		float(Pset.get()),
		float(Aset.get()),
		float(intset.get()),
		int(numset.get()),
		int(perset.get()))
	print('then\t',cw1.printlist)
	cw1 = cloneFromList(extrap(cw1))
	print('now\t',cw1.printlist)
	var_matrix = [[rows]for rows in range(cw1.num*cw1.per)]
	for i in range(30):
		root.grid_columnconfigure(i,  minsize=column_size)
		root.grid_rowconfigure(i,  minsize=row_size)
		F_val_label.grid(   row=1, column=4)
		P_val_label.grid(   row=1, column=5)
		A_val_label.grid(   row=1, column=6)
		int_val_label.grid( row=1, column=7)
		num_val_label.grid( row=1, column=8)
		per_val_label.grid( row=1, column=9)	
		F_val_label_text.set("{0}".format(cw1.F))
		P_val_label_text.set("{0}".format(cw1.P))
		A_val_label_text.set("{0}".format(cw1.A))
		int_val_label_text.set("{0}".format(cw1.int))
		num_val_label_text.set("{0}".format(cw1.num))
		per_val_label_text.set("{0}".format(cw1.per))
	#lchan_xcoord_label_text.set("{0}".format(int(movelsrX.get())))

def gen_test_cmd():
	## setting up tk entry widget
	rooter=tki.Tk()   
	# setting the windows size 
	rooter.geometry("900x450")	
	rooter.title("CSV TEST OUTPUT 0.0.1")
	column_size = 30
	row_size = 15
	
	cw1 = CSV_Writer(
		float(Fset.get()),
		float(Pset.get()),
		float(Aset.get()),
		float(intset.get()),
		int(numset.get()),
		int(perset.get()))
	#print('then\t',cw1.printlist)
	cw1 = cloneFromList(extrap(cw1))
	#print('now\t',cw1.printlist)
	print("Test Button")
		  
	# w = Label(root, text ='CES LLC', font = "50")  
	# w.pack() 		
	# msg = Message( root, text = "Contract Engineering")   		
	# msg.pack()   
	  
	#root.mainloop()
    #return csv1
	rows = []
	for i in range(cw1.num*cw1.per):
		cols = []
		for j in range(6):
			e = tki.Entry(rooter)
			e.grid(row=i, column=j, sticky=NSEW)
			e.insert(END, '{0}'.format(cw1.list[j]))
			cols.append(e)
		rows.append(cols)
	#rooter.loop()
	
	###################################
def gen_test_cmd2():	
	## Initializing csv object with our input values
	cw1 = CSV_Writer(
		float(Fset.get()),
		float(Pset.get()),
		float(Aset.get()),
		float(intset.get()),
		int(numset.get()),
		int(perset.get()))
	print('then\t',cw1.printlist)	 ## DBPRINT
	cw1 = cloneFromList(extrap(cw1))
	print('now\t',cw1.printlist)	 ## DBPRINT
	
	print("Testing Show CSV Button") ## DBPRINT
	
	## Create csv file in main directory	
	tgf1_header =['count','FV','PW','SF','CR','Atot','FV-PV','Owed']
	outlist2 = [cw1.num*cw1.per,cw1.F,cw1.P,round(cw1.sinkFund,2),round(cw1.capRecovery,2),round(cw1.A*((cw1.num*cw1.per)+1),2),round((cw1.F-cw1.P),2),0] ## has 8 items
	print("cw1.A = ",cw1.A) 
	print("k = ",cw1.num*cw1.per) 
	print("cw1.A * k = ",cw1.A*(cw1.num*cw1.per))  	 		
	with open('top_gui_1.csv', mode='w') as tgf1file:
		tgf1_writer = csv.writer(tgf1file)
		tgf1_writer.writerow(tgf1_header)
		tgf1_writer.writerow(outlist2)
	tgf1file.close()
	with open('top_gui_1.csv', mode='a+') as tgf1file:
		tgf1_writer = csv.writer(tgf1file)
		for k in range(1,(cw1.num*cw1.per)+1):
			
			## Counter for this iteration
			outlist2[0] = k			
			
			## Future Value for this iteration
			var1 = round(cw1.F - cw1.A*((((1+(cw1.int/cw1.per))**k)-1)/(cw1.int/cw1.per)),2)
			outlist2[1] = var1 if var1 >=0 else 0 ## FGA	
			
			## Present Worth for this iteration
			## self.presentWorth = pmt*(((math.pow((1+(i/per)),(n*per)))-1)/((i/per)*(math.pow((1+(i/per)),(n*per)))))
			var2 = round(cw1.P - cw1.A*(((math.pow((1+(cw1.int/cw1.per)),k))-1)/((cw1.int/cw1.per)*
							(math.pow((1+(cw1.int/cw1.per)),k)))),2)
			outlist2[2] = var2 if var2 >= 0 else 0 ## PGA	
			
			## Sinking Fund
			# ~ ##self.sinkFund = fv*((i/per)/(((1+(i/per))**(n*per))-1))
			var3 = round(cw1.F*((cw1.int/cw1.per)/(((1+(cw1.int/cw1.per))**k)-1)),2)		
			outlist2[3] = var3 if var3 >= 0 else 0
			
			## Capital Recovery
			# ~ ## self.capRecovery = pw*(((i/per)*(math.pow((1+(i/per)),(n*per))))/((math.pow((1+(i/per)),(n*per))-1)))
			var4 = round(cw1.P*(((cw1.int/cw1.per)*((1+(cw1.int/cw1.per))**k))/(((1+(cw1.int/cw1.per))**k)-1)),2)		
			outlist2[4] = var4 if var4 >= 0 else 0
			
			## Sum of Payments for this iteration
			var5 = round(cw1.A*k,2)
			outlist2[5] = var5 #if var5 >= 0 else 0
			
			## TEST:	PW - (present worth for this iteration)
			var6 = round((cw1.P - var2),2)
			outlist2[6] = var6 #if var6 >= 0 else 0
			
			## TEST:	PW -  (sum of payments for this iteration)
			var7 = round((cw1.P - var5),2)
			outlist2[7] = var7 #if var7 >= 0 else 0
			
			tgf1_writer.writerow(outlist2)
			# ~ #print(outlist2)						
		tgf1file.close()
	print('cw1\t{0}\n'.format(cw1.list)) ## DBPRINT
	print('outlist2\t{0}\n'.format(outlist2)) ## DBPRINT
##########################################################
	
	
#######################
####### CLONERS #######		
def cloneCSV_Writer(cw):
	cw1 = CSV_Writer(cw.F,cw.P,cw.A,cw.int,cw.num,cw.per)
	#print('{0:.2f}'.format(cw1.futvalue)) ## DBPRINT
	return cw1	
			
def cloneFromList(c=[0,0,0,0.0001,1,1]):
	cw1 = CSV_Writer(c[0],c[1],c[2],c[3],c[4],c[5])
	#print('{0:.2f}'.format(cw1.futvalue)) ## DBPRINT
	return cw1		
      
def create_csv(f,p,a,i,n,per):
	cw1 = CSV_Writer(f,p,a,i,n,per)
	return cw1 
 	
#######################
## extrap(cw): This function extrapolates uninitialized object values
## from incomplete object definitions, and returns them in a list for 
## later iteration.

## 1.	It isolates the input object by cloning it; 
## 2.	copies the clone's self.list;
## 3.	modifies the list with extrapolated values; and
## 4.	returns the modified list.

def extrap(cw):
	cw1 = CSV_Writer(cw.F,cw.P,cw.A,cw.int,cw.num,cw.per)
	outlist = cw1.list
	#print('inlist = ',outlist) ## DBPRINT
	
	## Switch Block ##
	if (cw1.list[0]==0)and(cw1.list[1]==0)and(cw1.list[2]==0):
		print('Nothing to do here. Try again.')
		
	elif cw1.list[2]>0:		
		outlist[0] = round(outlist[2]*((((1+(cw1.int/cw1.per))**(cw1.num*cw1.per))-1)/(cw1.int/cw1.per)),2)	
		outlist[1] = round(outlist[2]*(((math.pow((1+(cw1.int/cw1.per)),(cw1.num*cw1.per)))-1)
			/((cw1.int/cw1.per)*(math.pow((1+(cw1.int/cw1.per)),(cw1.num*cw1.per))))),2)				

	elif cw1.list[1]>0 and cw1.list[2]<=0:	
		outlist[2] = round(outlist[1]*(((cw1.int/cw1.per)*(math.pow((1+(cw1.int/cw1.per)),
			(cw1.num*cw1.per))))/((math.pow((1+(cw1.int/cw1.per)),(cw1.num*cw1.per))-1))),2)	
		outlist[0] = round(outlist[2]*((((1+(cw1.int/cw1.per))**(cw1.num*cw1.per))-1)/(cw1.int/cw1.per)),2)	
			
	elif cw1.list[0]>0 and cw1.list[1]<=0 and cw1.list[2]<=0:	
		outlist[2] = round(outlist[0]*((cw1.int/cw1.per)/(((1+(cw1.int/cw1.per))**(cw1.num*cw1.per))-1)),2)		
		outlist[1] = round(outlist[2]*(((math.pow((1+(cw1.int/cw1.per)),(cw1.num*cw1.per)))-1)
			/((cw1.int/cw1.per)*(math.pow((1+(cw1.int/cw1.per)),(cw1.num*cw1.per))))),2)
			
	#print('outlist = ',outlist,'\n') ## DBPRINT
	return outlist

###################	
## csvgen_1(): This function accepts a CSV_Writer object as the input arg
## and generates a csv file from its attributes.
def csvgen_1(cw1):
	agf_header =['F','P','A','profit','n','test']
	inlist = extrap(cw1)
	cw = cloneFromList(inlist)
	#outlist = cw.list
	outlist1 = [cw.F,cw.P,cw.A,0,cw.num*cw.per,0,0,0]
	#print(outlist1)

	############################################################
	##			outlist1[0:8]
	##  [0]	 [1]  	[2]	[3]	[4]	[5]	[6]	[7]
	##  fv	 pw	 pmts	profit	count	test1	test2	test3

	for k in range(1,(cw.num*cw.per)+1):
		## Future Value
		var0 = round(inlist[0]-cw.A*((((1+(cw.int/cw.per))**k)-1)/(cw.int/cw.per)),2)
		outlist1[0] = var0 if var0 >=0 else 0 ## FGA	
		
		## Present Worth	
		var1 = round(inlist[1]-cw.A*(((math.pow((1+(cw.int/cw.per)),k))-1)/((cw.int/cw.per)*
						(math.pow((1+(cw.int/cw.per)),k)))),2)
		outlist1[1] = var1 if var1 >= 0 else 0 ## PGA	
		
		## Sum of Payments
		outlist1[2] = round(cw.A*k,2)
		
		## Total Profit earned during this iteration
		var3 = round((cw.A*((((1+(cw.int/cw.per))**k)-1)/(cw.int/cw.per)) - 
						cw.A*(((math.pow((1+(cw.int/cw.per)),k))-1)/((cw.int/cw.per)*
						(math.pow((1+(cw.int/cw.per)),k))))),2)
		outlist1[3] = var3
		
		## Counter
		outlist1[4] = k
		
		## Test1 Output
		outlist1[5] = round(inlist[0] - outlist1[2],2)
		
		## Test2 Output
		outlist1[6] = round(outlist1[5] + outlist1[2],2)
		
		agf1_writer.writerow(outlist1)
		#print(outlist1)

###################	
## csvgen_2(): This function accepts a CSV_Writer object as input arg, and
## generates a csv file from it.
def csvgen_2(cw1):
	profit_header =['F','P','n','i','test1','test2','test3','test4']
	inlist = extrap(cw1)
	cw = cloneFromList(inlist)
	#outlist = cw.list

	#############################################################
	##			outlist2[0:8]
	##  [0]	 [1]  	[2]	[3]	[4]	[5]	[6]	[7]
	##  fv	 pw	pmt	int	num	test1	test2	test3	
	outlist2 = [cw.F,cw.P,cw.A,cw.int,cw.num*cw.per,0,round(cw.F-cw.P,2),0]
	print(outlist2)
	
	for k in range(1,(cw.num*cw.per)+1):
		
		var0 = round(inlist[0]-cw.A*((((1+(cw.int/cw.per))**k)-1)/(cw.int/cw.per)),2)
		outlist2[0] = var0 if var0 > 0 else 0.00001 ## FGA
			
		var1 = round(inlist[1]-cw.A*(((math.pow((1+(cw.int/cw.per)),
				k))-1)/((cw.int/cw.per)*(math.pow((1+(cw.int/cw.per)),k)))),2)
		outlist2[1] = var1 if var1 > 0 else 0.00001 ## PGA	
		
		## sinkFund == cw.A			
		var2 = round(inlist[0]*((cw.int/cw.per)/(((1+(cw.int/cw.per))**k)-1)),2)
		## capRecovery == cw.A
		#var2 = round(inlist[1]*(((cw.int/cw.per)*(math.pow((1+(cw.int/cw.per)),
		#					k)))/((math.pow((1+(cw.int/cw.per)),k)-1))),2)
		outlist2[2] = var2
		
		## Interest paid this period
		outlist2[3] = round(((outlist2[0]/outlist2[1])**(1/k))-1,2)
		
		outlist2[4] = k
		
		outlist2[5] = round(cw.A*k,2)
		
		outlist2[6] = round(cw.P - outlist2[1],2) 
		
		outlist2[7] = round(cw.F - outlist2[0],2) 
		
		
		agf2_writer.writerow(outlist2)
		print(outlist2)

###################
## getIntRate(): olist needs to be [fv,pw,n]
def getIntRate(olist=[0,0,0]):
	outI = 0.0
	if ((olist[0]==0)and(olist[1]==0))or(olist[2]==0):
		print('Nothing to do here. Try again.')		
	else: 	
		outI = ((olist[0]/olist[1])**(1/olist[2]))-1	
	print('interest rate = {0:.5f}'.format(outI)) ## DBPRINT
	return outI

###################		

#####################################################
################ The Label Generator ################
for a in range(30):
	root.grid_columnconfigure(a,  minsize=column_size)
	root.grid_rowconfigure(a,  minsize=row_size)
	F_in_label.grid(   row=0, column=4)
	P_in_label.grid(   row=0, column=5)
	A_in_label.grid(   row=0, column=6)
	int_in_label.grid( row=0, column=7)
	num_in_label.grid( row=0, column=8)
	per_in_label.grid( row=0, column=9)
 
root.update()
root.mainloop()

#### Construction Zone Pylon ####
#### End of Construction Zone Pylon ####


#!/usr/bin/python3

# PROJECT		intCalc
# FILE			csvgen.py
# AUTHOR		Jacob Romero 
#				Creative Engineering Solutions, LLC

#### This Project has several parts:

# 	1.	To provide methods for iterating through the interest calculator
#		equations defined below and generate raw data suitable for csv files.

# 	3.	To generate various csv files from the raw data.

# 	4.	To provide a tkinter GUI for easy UI and UX with this class.

# 	5.	To provide unittest methods for development and maintenance.

# This file, csvgen.py, accomplishes parts 1 and 2 above.
# For part 3, use top_gui.py.
# For part 4, use test_csv.py.

#### Input Parameters:

# 			F	Future Value
#			P	Present Value
#			A	Payment, end-of-period cash receipt, or disbursement
# 			i	Interest rate per interst period
# 			n	Number of interest periods

#### Equations:

# Series Future Value, find F given A:	
# Series Future Value is the total amount which will be accrued or repaid (F)
# given a uniform series of disbursements (A) over n periods.
#			F = A*((((1+i)**n)-1)/i)

# Series Present Worth, find P given A:		
# Series Present Worth is the present value (P) of an annuity given
# a uniform series of disbursements (A) over n periods.	
#			P = A*((((1+i)**n)-1)/(i*((1+i)**n)))

# Sinking Fund, find A given F:
# A Sinking Fund is when you deposit a uniform series of amounts (A) 
# to accumulate a desired future amount (F) by the end of period n.		
#			A = F*(i/(((1+i)**n)-1))

# Capital Recovery, find A given P:
# Capital Recovery is how big an annual return (A) has to be in order to
# recover the initial investment amount (P) by the end of period n.		
#			P = A*((i*((1+i)**n))/(((1+i)**n)-1))

import os
import csv
import sys
import time
import math
import numpy as np
import pandas as pd
from csv import reader
from csv import writer
from csv import DictReader
import tkinter as tk
from tkinter import ttk
from sinkingFund import *
from interestCalc import *
from capitalRecovery import*

fields = ['F','P','A','i','n','p']
outvals = [0,0,0,0.001,0,0]

# name of csv file
#filename = "wtf_testOutput.csv"
td1_csv = "testdata_1.csv"

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
		
		self.compound = self.P*((1+(i/per))**(n*per))
		self.pworth = self.F*((1+(i/per))**(n*per*(-1)))
		self.futvalue = self.A*((((1+(i/per))**(n*per))-1)/(i/per))		
		self.presentWorth = self.A*(((math.pow((1+(i/per)),(n*per)))-1)/((i/per)*(math.pow((1+(i/per)),(n*per)))))		
		self.sinkFund = self.F*((i/per)/(((1+(i/per))**(n*per))-1))
		self.capRecovery = self.P*(((i/per)*(math.pow((1+(i/per)),(n*per))))/((math.pow((1+(i/per)),(n*per))-1)))
		self.profit = round(self.compound - self.pworth,2)
		
		# print('CSV Writer list = {0}'.format(self.printlist))	
		# print('compound = {0:.2f}'.format(self.compound))	
		# print('pworth = {0:.2f}'.format(self.pworth))
		# print('futvalue = \t{0:.2f}'.format(self.futvalue))	
		# print('presentWorth = \t{0:.2f}'.format(self.presentWorth))	
		# print('sinkingFund = \t{0:.2f}'.format(self.sinkFund))	
		# print('capRecovery = \t{0:.2f}'.format(self.capRecovery))			
	
#######################
####### GETTERS #######
	def gtFGA(self):
		self.futvalue = self.A*((((1+(self.int/self.per))**(self.num*self.per))-1)/(self.int/self.per))
		print('futvalue = \t{0:.2f}'.format(self.futvalue)) ## DBPRINT
		
	def gtAGF(self):
		self.sinkFund = self.F*((self.int/self.per)/(((1+(self.int/self.per))**(self.num*self.per))-1))
		print('sinkingFund = \t{0:.2f}'.format(self.sinkFund)) ## DBPRINT
		
	def gtAGP(self):
		self.capRecovery = self.P*(((self.int/self.per)*(math.pow((1+(self.int/self.per)),
		(self.num*self.per))))/((math.pow((1+(self.int/self.per)),(self.num*self.per))-1)))
		print('capRecovery = \t{0:.2f}'.format(self.capRecovery)) ## DBPRINT

	def gtPGA(self):
		self.presentWorth = self.A*(((math.pow((1+(self.int/self.per)),
		(self.num*self.per)))-1)/((self.int/self.per)*(math.pow((1+(self.int/self.per)),(self.num*self.per)))))
		print('presentWorth = \t{0:.2f}'.format(self.presentWorth)) ## DBPRINT

		
#################################
####### SERIES GENERATORS #######		
	def genFGA(self):
		for j in range(1,self.num+1):
			self.futvalue = self.A*((((1+(self.int/self.per))**(j*self.per))-1)/(self.int/self.per))
			print('fv = \t{0:.2f}'.format(self.futvalue)) ## DBPRINT		
			#return self.futvalue	
	def genPGA(self):
		for j in range(1,self.num+1):
			self.presentWorth = self.A*(((math.pow((1+(self.int/self.per)),
			(j*self.per)))-1)/((self.int/self.per)*(math.pow((1+(self.int/self.per)),(j*self.per)))))
			print('pw = \t{0:.2f}'.format(self.presentWorth)) ## DBPRINT
			#print(self.profit)
			#return self.presentWorth	
				
	def genAGF(self):
		for j in range(1,self.num+1):
			self.sinkFund = self.F*((self.int/self.per)/(((1+(self.int/self.per))**(j*self.per))-1))
			print('sinkingFund = \t{0:.2f}'.format(self.sinkFund)) ## DBPRINT	
			#return self.sinkFund						
	def genAGP(self):
		for j in range(1,self.num+1):
			self.capRecovery = self.P*(((self.int/self.per)*(math.pow((1+(self.int/self.per)),
			(j*self.per))))/((math.pow((1+(self.int/self.per)),(j*self.per))-1)))
			print('capRecovery = \t{0:.2f}'.format(self.capRecovery)) ## DBPRINT
			#return self.capRecovery		
		
####################################
##<<<<<<<<< WE ARE NOW >>>>>>>>>>>##
##<<<<< OUTSIDE OF THE CLASS >>>>>##

#######################
####### CLONERS #######		
def cloneCSV_Writer(cw):
	cw1 = CSV_Writer(cw.F,cw.P,cw.A,cw.int,cw.num,cw.per)
	#print('{0:.2f}'.format(cw1.futvalue)) ## DBPRINT
	return cw1	
			
def cloneFromList(c=[0,0,0,0.001,1,1]):
	cw1 = CSV_Writer(c[0],c[1],c[2],c[3],c[4],c[5])
	#print('{0:.2f}'.format(cw1.futvalue)) ## DBPRINT
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
	print('inlist = ',outlist) ## DBPRINT
	
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
			
	print('outlist = ',outlist,'\n') ## DBPRINT
	return outlist

###################	
agf_header =['F','P','A','profit','n','test']
def csvgen(cw1):
	inlist = extrap(cw1)
	cw = cloneFromList(inlist)
	#outlist = cw.list
	outlist1 = [cw.F,cw.P,cw.A,0,cw.num*cw.per,0,0,0]
	#print(outlist1)
	
	with open('agf_1.csv', mode='w') as agf1file:
		agf1_writer = csv.writer(agf1file)
		agf1_writer.writerow(agf_header)
		agf1_writer.writerow(outlist1)
	agf1file.close()
	############################################################
	##					outlist1[0:8]
	##	[0]	 [1]  [2]	[3]		[4]		[5]		[6]		[7]
	##  fv	 pw	  pmts	profit	count	test1	test2	test3

	with open('agf_1.csv', mode='a+') as agf1file:
		agf1_writer = csv.writer(agf1file)
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
	agf1file.close()

	###########################
	##		outlist2[0:5]
	##	[0]	 [1]  [2]	[3]		[4]		[5]		[6]		[7]
	##  fv	 pw	  pmt	int		num		test1	test2	test3
	outlist2 = [cw.F,cw.P,cw.A,cw.int,cw.num*cw.per,0,round(cw.F-cw.P,2),0]
	profit_header =['F','P','n','i','test1','test2','test3','test4']
	print(outlist2)
	
	with open('bgf_2.csv', mode='w') as agf2file:
		agf2_writer = csv.writer(agf2file)
		agf2_writer.writerow(profit_header)
		agf2_writer.writerow(outlist2)
	agf2file.close()
				
	with open('bgf_2.csv', mode='a+') as agf2file:
		agf2_writer = csv.writer(agf2file)
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
	agf2file.close()
###################
def gtProfit(cw):
	for j in range(1,cw.num+1):
		cw.futvalue = cw.A*((((1+(cw.int/cw.per))**(j*cw.per))-1)/(cw.int/cw.per))		
		cw.presentWorth = cw.A*(((math.pow((1+(cw.int/cw.per)),
			(j*cw.per)))-1)/((cw.int/cw.per)*(math.pow((1+(cw.int/cw.per)),(j*cw.per)))))
		diff = round(cw.futvalue-cw.presentWorth,2)
		print('profit = {0:.2f} - {1:.2f} \t= {2:.2f}'.format(cw.futvalue,cw.presentWorth,diff))
	#return cw.futvalue-cw.presentWorth

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
# Driver program
if __name__ == "__main__":
	#cr0 = CSV_Writer(614210.50,250000,1054.01,0.03,30,12)
	cr0 = CSV_Writer(0,250000,0,0.03,10,12)
	cr2 = cloneFromList(extrap(cr0))
	csvgen(cr0)
	#gtProfit(cr2)
	#getIntRate(cr2.olist)
	print('\n')
	# cr0.gtAGF()
	# cr0.gtAGP()
	# cr0.gtFGA()
	# cr0.gtPGA()
	
	#cr2.genAGF()
	#cr2.genAGP()
	# cr2.genFGA()
	# cr2.genPGA()
		
	# cr1 = cr0.cloneCSV_Writer(cr0)
	# cr2 = cloneFromList(cr1.list)
	# #print('cr0.tuple = {0}'.format(cr0.tuple))
	# print('cr1.futvalue = {0:.2f}'.format(cr1.futvalue))
	# print('cr2.futvalue = {0:.2f}'.format(cr2.futvalue))
	# print('\n')
	# #cr1 = CSV_Writer(614210.50,250000,1054.01,0.03/12,30*12,1)
	# cr1.gtAGF()
	# cr1.gtAGP()
	# cr1.gtFGA()
	# cr1.gtPGA()
	# # print('\n')
	
	# cr0.genAGF()
	# cr0.genAGP()
	# cr0.genFGA()
	# cr0.genPGA()

##########################################################

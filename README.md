 PROJECT:	
 UniformSeriesGenerator
 
 AUTHOR:	
 Jacob Romero, 
 Creative Engineering Solutions, LLC

 This project will simplify certain investment calculations (The Uniform Series Equations), and facilitate the creation of spreadsheets for loans and investments.
  
 This Project has four parts:

 	0.	To iterate through the financial equations defined below and generate raw data suitable for csv files.

 	1.	To generate various csv files from the raw data.

 	2.	To provide a tkinter GUI for easy UI with this class.

 	3.	To provide unittest methods for development and maintenance.

 csvgen.py, accomplishes parts 0 and 1 right now.
 
 top_gui.py accomplishes parts 0, 1 and 2 for now.
 
 For part 3, Still working on it...

 Input/Output Parameters:

 			F	Future Value
			P	Present Value
			A	Payment, end-of-period cash receipt, or disbursement
 			i	Interest rate per interst period
 			n	Number of interest periods

 Equations:

 Series Future Value, find F given A:
 
 Series Future Value is the total amount which will be accrued or repaid (F)
 given a uniform series of disbursements (A) over n periods.
			
			F = A*((((1+i)**n)-1)/i)

 Series Present Worth, find P given A:
 
 Series Present Worth is the present value (P) of an annuity given
 a uniform series of disbursements (A) over n periods.	
			
			P = A*((((1+i)**n)-1)/(i*((1+i)**n)))

 Sinking Fund, find A given F:
 
 A Sinking Fund is when you deposit a uniform series of amounts (A) 
 to accumulate a desired future amount (F) by the end of period n. 
 This is the one you use to calculate a monthly loan payback amount.
			
			A = F*(i/(((1+i)**n)-1))

 Capital Recovery, find A given P:
 
 Capital Recovery is how big an annual return (A) has to be in order to
 recover the initial investment amount (P) by the end of period n.		
			
			P = A*((i*((1+i)**n))/(((1+i)**n)-1))

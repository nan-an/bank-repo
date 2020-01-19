import decimal
import datetime
from tabulate import tabulate

#\033[34m - Blue
#\033[0m - Black
#\033[31m - Red

def inputf(a):
	w=input('\033[34m'+a+'\033[0m')
	print('\033[31m',end="")
	return w

class Bank:
	def __init__(self,accounts={},customers={},branches={},transactions=[],nextAcc=1,nextBranch=2,date=datetime.datetime.date(datetime.datetime.now())):
		self.Acc=accounts
		self.Cust=customers
		self.Branch=branches
		self.Trans=transactions
		self.nextAcc=nextAcc
		self.nextBranch=nextBranch
		self.date=date

	class Accounts:
		def __init__(self,accno,customer,balance,branch,dwl,withdrawn=0):
			self.accno=accno
			self.customer=customer
			self.balance=balance
			self.branch=branch
			self.dwl=dwl
			self.withdrawn=withdrawn
		def printFullDetails(Self):
			print("Account Details:-")
			print("    Account Number: {0} \n    Account Balance: {1} \n    Branch Number: {2} \n    Daily withdrawing Limit: {3}".format(Self.accno,Self.balance,Self.branch.branchno,Self.dwl))
			Self.customer.printDetails()

	class Branches:
		def __init__(self,branchno,accnos):
			self.branchno=branchno
			self.accnos=accnos

		def printFullDetails(bSelf,self):
			print("Branch Number: ",bSelf.branchno)
			self.tabulateAcc(bSelf.accnos)

	class Transactions:
		def __init__(self,flag,acc1,acc2,val,date):
			self.flag=flag
			self.acc1=acc1
			self.acc2=acc2
			self.val=val
			self.date=date

	class Customers:
	    def __init__(self, accnos, name, address, email, pnumber,custid):
	        self.accnos = accnos
	        self.name = name
	        self.address = address 
	        self.email = email
	        self.phone_number = pnumber
	        self.custid= custid
	    def printDetails(Self):
	    	print("Customer Details:-\n    name: {0} \n    address: {1} \n    email: {2} \n    Phone Number: {3} \n    PersonID: {4}".format(Self.name,Self.address,Self.email,Self.phone_number,Self.custid))
	    def printFullDetails(cSelf,self):
	    	cSelf.printDetails()
	    	self.tabulateAcc(cSelf.accnos)


	def printFullDetails(self):
		print("Number of Branches: ",self.nextBranch-1)
		Bank.seg()
		res=Bank.dec('0.0')
		for i in range(1,self.nextBranch):
			self.Branch[i].printFullDetails(self)
			res+=self.accountsBalance(self.Branch[i].accnos)
			Bank.seg()
		print("Total Balance of the Bank: ",res)

	def dec(a):
		return decimal.Decimal(str(a))

	def seg():
		print('\033[0m'+"-----------------------------------------------------------------------------------------------"+'\033[31m')

	def tabulateAcc(self,accnos):
		print("All Account Details:- ")
		l=[[self.Acc[x].accno,self.Acc[x].branch.branchno,self.Acc[x].balance] for x in accnos]
		print(tabulate(l,headers=["Account Number","Branch Number","Balance"],tablefmt="psql"))
		print("Total Balance:",self.accountsBalance(accnos))

	def accountsBalance(self,accnos):
		tbal=Bank.dec('0.0')
		tbal+=sum([self.Acc[x].balance for x in accnos])
		return tbal

	def ttype(flag):
		if(flag==0):
			return "Credit"
		elif(flag==1):
			return "Debit"
		elif(flag==2):
			return "Transaction"

	def printTrans(self,transobj):
		l=[[Bank.ttype(x.flag),x.acc1,x.acc2,x.val,x.date] for x in transobj]
		print(tabulate(l,headers=["Type","AccountNo.1(from)","AccountNo.2(To)","Value","Date"],tablefmt="psql"))

	def createAccount(self):
		flag=inputf("Have you created an Account before?(y/n): ")
		while(flag!='y' and flag!='n'):
			flag=inputf("Please enter a valid input. Do you already have an Account(y/n): ")
		if(flag=='y'):

			custid=inputf("Enter your PersonID: ")
			if(custid in self.Cust):
				pass
			else:
				print("You don't have an account. Please restart")
				return
		else:
			custid=inputf("Enter PersonID: ")
			if(custid in self.Cust):
				print("You have already made an account before. Please start again")
				return
			name=inputf("Enter name: ")
			address=inputf("Enter address: ")
			email=inputf("Enter email: ")
			pnumber=inputf("Enter Phone Number: ")
			self.Cust[custid]=Bank.Customers([],name,address,email,pnumber,custid)

		bal=Bank.dec(inputf("Enter your initial Balance: "))
		bran=int(inputf("Enter BranchNo.: "))
		while(bran>=self.nextBranch):
			bran=int(inputf("Please enter a Valid Branch Number"))
		dwl=Bank.dec(inputf("Enter Daily withdrawal limit for the Account: "))
		self.Acc[self.nextAcc]=Bank.Accounts(self.nextAcc,self.Cust[custid],bal,self.Branch[bran],dwl)
		self.Cust[custid].accnos.append(self.nextAcc)
		self.Branch[bran].accnos.append(self.nextAcc)
		self.Acc[self.nextAcc].printFullDetails()
		self.nextAcc+=1
		print("Account Created!!")
		return

	def closeAccount(self):
		Accno=int(inputf("Please input your Account Number: "))
		if(Accno in self.Acc):
			self.Acc[Accno].customer.accnos.remove(Accno)
			self.Acc[Accno].branch.accnos.remove(Accno)
			del self.Acc[Accno]
			print("Your account has been deleted. Please take your money.")
		else:
			print("Account does not exist")

	def credit(self,accno,val):
		self.Acc[accno].balance+=val
		return 1

	def debit(self,accno,val):
		if(self.Acc[accno].balance-val<0):
			print("Sorry the account does not have that balance")
			return 0
		self.Acc[accno].balance-=val
		return 1

	def ask(self,flag):
		accno=int(inputf("Enter Account Number: "))
		if(accno not in self.Acc):
			print("Account does not exist")
			return
		val=Bank.dec(inputf("Enter amount: "))
		if(flag==0):
			res=self.credit(accno,val)
			if(res):
				self.Trans.append(Bank.Transactions(0,accno,None,val,self.date))
				print("Value Credited")
		elif(flag==1):
			if(self.Acc[accno].withdrawn+val<=self.Acc[accno].dwl):
				res=self.debit(accno,val)
				if(res):
					self.Trans.append(Bank.Transactions(1,accno,None,val,self.date))
					print("Value Debited")
					self.Acc[accno].withdrawn+=val
			else:
				print("Cannot proceed. Exceeding daily withdrawal limit")
	
	def makeTransaction(self):
		accno1=int(inputf("Transaction from Account Number: "))
		if(accno1 not in self.Acc):
			print("Account does not exist")
			return
		accno2=int(inputf("Transaction to Account Number: "))
		if(accno2 not in self.Acc):
			print("Account does not exist")
			return
		val=Bank.dec(inputf("Enter amount: "))
		res1=self.debit(accno1,val)
		if(res1):
			res2=self.credit(accno2,val)
			if(res2):
				print("Transaction Successful")
				self.Trans.append(Bank.Transactions(2,accno1,accno2,val,self.date))
		else:
			print("Transaction can't be proceeded")
			print("Error: {0} Not enough account balance".format(accno1))

	def getTransactionReport(self):
		print("Press\n    1 for Customer\n    2 for Branch\n    3 for Bank")
		choice=inputf("Enter choice: ")
		date_input=inputf("Enter lower date(YYYY-MM-DD): ")
		year, month, day = map(int, date_input.split('-'))
		date1 = datetime.date(year, month, day)

		date_input=inputf("Enter upper date(YYYY-MM-DD): ")
		year, month, day = map(int, date_input.split('-'))
		date2 = datetime.date(year, month, day)
		l=[]
		if(date2<date1):
			print("Invalid range")
			return
		if(choice=='1'):
			custid=inputf("Enter custid: ")
			if(custid not in self.Cust):
				print("Customer doesn't have an account")
				return
			l=list(filter(lambda x:((self.Acc[x.acc1].customer.custid==custid or (x.flag==2 and self.Acc[x.acc2].customer.custid==custid)) and date1<=x.date<=date2),self.Trans))
		elif(choice=='2'):
			branchno=int(inputf("Enter Branchno: "))
			if(branchno>=self.nextBranch):
				print("Branch Does not exist")
				return
			l=list(filter(lambda x:((self.Acc[x.acc1].branch.branchno==branchno or (x.flag==2 and self.Acc[x.acc2].branch.branchno==branchno)) and date1<=x.date<=date2), self.Trans))
		elif(choice=='3'):
			l=self.Trans
		self.printTrans(l)
			


	def run(self):
		if(len(self.Branch)==0):
			self.Branch[1]=Bank.Branches(1,[])
		while(1):
			print()
			print('\033[31m',end="")
			Bank.seg()
			print()
			Bank.seg()
			print('''Welcome to the Bank Menu. Press
			1  - Create Account
			2  - Close Account
			3  - Deposit Money
			4  - Withdraw Money
			5  - Make Transaction
			6  - Create Branch
			7  - Get Transaction report for a date range
			8  - Account Details
			9  - Customer Details
			10 - Branch Details
			11 - Bank Details
			12 - Roll the next date
			0  - exit ''')
			choice=inputf("Enter your Choice: ")
			Bank.seg()
			if(choice=='1'):
				self.createAccount()
			elif(choice=='2'):
				self.closeAccount()
			elif(choice=='3'):
				self.ask(0)
			elif(choice=='4'):
				self.ask(1)
			elif(choice=='5'):
				self.makeTransaction()
			elif(choice=='6'):
				self.Branch[self.nextBranch]=Bank.Branches(self.nextBranch,[])
				print("New Branch Created!!")
				print("New Branch Number:",self.nextBranch)
				self.nextBranch+=1
			elif(choice=='7'):
				self.getTransactionReport()
			elif(choice=='8'):
				accno=int(inputf("Enter Account Number: "))
				if(accno not in self.Acc):
					print("Account does not exist")
					continue
				self.Acc[accno].printFullDetails()
			elif(choice=='9'):
				custid=inputf("Enter PersonID: ")
				if(custid not in self.Cust):
					print("You don't have an account in the Bank yet.")
					continue
				self.Cust[custid].printFullDetails(self)
			elif(choice=='10'):
				branchno=int(inputf("Enter Branch Number: "))
				if(branchno not in self.Branch):
					print("Branch Does not exist")
					continue
				self.Branch[branchno].printFullDetails(self)
			elif(choice=='11'):
				self.printFullDetails()
			elif(choice=='12'):
				self.date=self.date+datetime.timedelta(days=1)
				for i in self.Acc:
					self.Acc[i].withdrawn=Bank.dec('0.0')
				print("Date changed!!")
				print("Current Date:",self.date)
			elif(choice=='0'):
				print('\033[0m')
				break



if __name__ == '__main__':
    bank=Bank()
    bank.run()
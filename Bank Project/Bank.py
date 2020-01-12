import decimal
import datetime
class Bank:
	def __init__(self,accounts={},customers={},transactions=[],nextAcc=1,nextBranch=2,threshold=1000000):
		self.Acc=accounts
		self.Cust=customers
		self.Trans=transactions
		self.nextAcc=nextAcc
		self.nextBranch=nextBranch
		self.threshold=threshold

	class Accounts:
		def __init__(self,accno,customer,balance,branchno):
			self.accno=accno
			self.customer=customer
			self.balance=balance
			self.branchno=branchno

	class Transactions:
		def __init__(self,flag,acc1,acc2,val,date):
			self.flag=flag
			self.acc1=acc1
			self.acc2=acc2
			self.date=date

	class Customers:
	    def __init__(self, accnos, name, address, email, pnumber,custid):
	        self.accnos = accnos
	        self.name = name
	        self.address = address 
	        self.email = email
	        self.phone_number = pnumber
	        self.custid= custid

	def dec(a):
		return decimal.Decimal(str(a))

	def createAccount(self):
		flag=input("Do you already have an Account(y/n): ")
		if(flag=='y'):

			custid=input("Enter your PersonID: ")
			if(custid in self.Cust):
				pass
			else:
				print("You don't have an account. Please restart")
				return
		else:
			custid=input("Enter PersonID: ")
			if(custid in self.Cust):
				print("You already have an account please start again")
				return
			name=input("Enter name: ")
			address=input("Enter address: ")
			email=input("Enter email: ")
			pnumber=input("Enter Phone Number: ")
			self.Cust[custid]=Bank.Customers([self.nextAcc,],name,address,email,pnumber,custid)

		bal=Bank.dec(input("Enter your initial Balance: "))
		bran=int(input("Enter BranchNo.: "))
		while(bran>=self.nextBranch):
			bran=int(input("Please enter a Valid Branch Number"))
		self.Acc[self.nextAcc]=Bank.Accounts(self.nextAcc,self.Cust[custid],bal,bran)
		self.Cust[custid].accnos.append(self.nextAcc)
		self.nextAcc+=1
		print("Account Created!!")
		return

	def closeAccount(self):
		Accno=int(input("Please input your Account Number: "))
		if(Accno in self.Acc):
			del self.Acc[Accno]
			print("Your account has been deleted. Please take your money.")
		else:
			print("Account does not exist")

	def credit(self,accno,val):
		if(self.Acc[accno].balance+val>self.threshold):
			print("Sorry the account balance will go above threshold")
			return 0
		self.Acc[accno].balance+=val
		return 1

	def debit(self,accno,val):
		if(self.Acc[accno].balance-val<0):
			print("Sorry the account does not have that balance")
			return 0
		self.Acc[accno].balance-=val
		return 1

	def ask(self,flag):
		accno=int(input("Enter Account Number: "))
		if(accno not in self.Acc):
			print("Account does not exist")
			return
		val=Bank.dec(input("Enter amount: "))
		date_input=input("Enter date(YYYY-MM-DD): ")
		year, month, day = map(int, date_input.split('-'))
		date1 = datetime.date(year, month, day)
		if(flag==0):
			res=self.credit(accno,val)
			if(res):
				self.Trans.append(Bank.Transactions(0,accno,None,val,date1))
				print("Value Credited")
		elif(flag==1):
			res=self.debit(accno,val)
			if(res):
				self.Trans.append(Bank.Transactions(1,accno,None,val,date1))
				print("Value Debited")
	
	def makeTransaction():
		accno1=int(input("Transaction from Account Number: "))
		if(accno1 not in self.Acc):
			print("Account does not exist")
			return
		accno2=int(input("Transaction to Account Number: "))
		if(accno2 not in self.Acc):
			print("Account does not exist")
			return
		val=Bank.dec(input("Enter amount: "))
		date_input=input("Enter date(YYYY-MM-DD): ")
		year, month, day = map(int, date_input.split('-'))
		date1 = datetime.date(year, month, day)
		res1=self.debit(accno1,val)
		if(res1):
			res2=self.credit(accno2,val)
			if(res2):
				print("Transaction Successful")
				self.Trans.append(Bank.Transactions(2,accno1,accno2,val,date1))
			else:
				print("Transaction can't be proceeded")
				print("Error: {0} Account balance will go above threshold".format(accno2))
				self.credit(accno1,val)
		else:
			print("Transaction can't be proceeded")
			print("Error: {0} Not enough account balance".format(accno1))



	def run(self):
		while(1):
			print()
			print('''Welcome to the Bank Menu. Press
						 	1  - Create Account
						 	2  - Close Account
						 	3  - Deposit Money
						 	4  - Withdraw Money
						 	5  - Make Transaction
						 	6  - Account Details
						 	7  - Create Branch
						 	8  - Branch Details
						 	9  - Bank Details
						 	10 - Change Threshold
						 	0  - exit ''')
			choice=input("Enter your Choice: ")
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
			elif(choice=='0'):
				break



if __name__ == '__main__':
    bank=Bank()
    bank.run()

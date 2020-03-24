import re
regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'
inputAddress = input('Please enter the emailAddress to verify:')
addressToVerify = str(inputAddress)
match = re.match(regex, addressToVerify)
if match == None:
	print('Bad Syntax')
else:
       print('Valid email')

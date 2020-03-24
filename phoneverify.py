import re
#regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'
regex = '^((\+){1}91){1}[1-9]{1}[0-9]{9}$'
inputno = input('Please enter the mobile no to verify:')
addressToVerify = str(inputno)
match = re.match(regex, addressToVerify)
if match == None:
        print('Bad Syntax!')
else:
       print('Valid mobile number!')


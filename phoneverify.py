import re
#regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'
def pverify(ph):
 #regex = '^((\+){1}91){1}[1-9]{1}[0-9]{9}$'
 #regex = '^[1-9]{1}[0-9]{9}$'
 regex = '^[1-9]{1}[0-9-]{0,15}$'
 phoneToVerify = str(ph)
 match = re.match(regex, phoneToVerify)
 if match == None:
       return 0
 else:
       return 1


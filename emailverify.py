import re
def everify(e):
# regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'
 regex ="(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
 addressToVerify = str(e)
 match = re.match(regex, addressToVerify)
 if match == None:
  return 0
 else:
  return 1

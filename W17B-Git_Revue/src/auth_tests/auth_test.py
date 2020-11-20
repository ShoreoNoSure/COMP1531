import auth
import pytest
from error import InputError
#import re

#regex = '\w+([\.-]?\w+)*@\w+([\.-]?w+)*\.\w{2,3})+$'
#def check(email):
   # if(re.search(regex,email)):
 #       return True
  #  else:
  #      return False
        
        
def test_incorrect_password():
    # if check(email) == True
    dict = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    token = dict["token"]
    u_id = dict["u_id"]
    auth.auth_logout(token)
   
    with pytest.raises(InputError):
        auth.auth_login("scnawa@hotmail.com", "qwertyuiop")

def test_correct_password():
    # if check(email) == True
    dict = auth.auth_register("scnawa@hotmail.com", "123456", "Sinha", "Nawa")
    token = dict["token"]
    u_id = dict["u_id"]
    auth.auth_logout(token)
   
    with pytest.raises(InputError):
        auth.auth_login("scnawa@hotmail.com", "123456")
        

    
        


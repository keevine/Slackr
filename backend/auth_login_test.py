import pytest
from functions.auth_functions import auth_register, auth_logout, auth_login
from functions.data import reset_data, is_logged_in

from functions.exceptions import ValueError, AccessError

#Assumptions: Email validation function is already implemented in auth_login.
#The database of registered users is empty.

#registered email and correct password
def test_auth_login_1():
    reset_data()
    dict1 = auth_register('myemail@gmail.com', 'mypassword', 'Kevin', 'Yasin')
    token1 = dict1['token']
    auth_logout(token1)
    dict2 = auth_login("myemail@gmail.com", "mypassword")
    token2 = dict2['token']
    assert(is_logged_in(token2))

#registered user, correct pass
def test_auth_login_2():
    reset_data()
    dict1 = auth_register('myemail2@gmail.com', 'mypassword', 'Steven', 'Peter')
    token1 = dict1['token']
    auth_logout(token1)
    dict2 = auth_login("myemail2@gmail.com", "mypassword")
    token2 = dict2['token']
    assert(is_logged_in(token2))

#registered email and incorrect pass
def test_auth_login_3():
    reset_data()
    dict1 = auth_register('myemail@gmail.com', 'mypassword', 'Kevin', 'Yasin')
    token1 = dict1['token']
    auth_logout(token1)
    with pytest.raises(ValueError):
        auth_login("myemail@gmail.com", "incorrectpass")

#unregistered email
def test_auth_login_4():
    reset_data()
    with pytest.raises(ValueError):
        auth_login("unregistereduser@gmail.com", "randompass")

#invalid email
def test_auth_login_5():
    reset_data()
    with pytest.raises(ValueError):
        auth_login("inVAL1D3mail$", "randompass")

#invalid email
def test_auth_login_6():
    reset_data()
    with pytest.raises(ValueError):
        auth_login("1", "1")

#invalid email
def test_auth_login_7():
    reset_data()
    with pytest.raises(ValueError):
        auth_login("", "")

#registered user, incorrect pass
def test_auth_login_8():
    reset_data()
    dict1 = auth_register('myemail2@gmail.com', 'mypassword', 'Steven', 'Peter')
    token1 = dict1['token']
    auth_logout(token1)
    with pytest.raises(ValueError):
        auth_login("myemail2@gmail.com", "mypasswordwrong")

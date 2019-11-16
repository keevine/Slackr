import pytest
from functions.auth_functions import auth_register
from functions.data import reset_data, is_logged_in

from functions.exceptions import ValueError, AccessError

#Database of registered users is empty.

#All details are valid
def test_auth_register_1():
    reset_data()
    dict = auth_register('email1@gmail.com', 'validpass', 'Yasin', 'Kevin')
    token = dict['token']
    assert(is_logged_in(token))


#All details are valid (2 consectuive registers)
def test_auth_register_2():
    reset_data()
    dict = auth_register('email1@gmail.com', 'validpass', 'Yasin', 'Kevin')
    token = dict['token']
    assert(is_logged_in(token))
    dict2 = auth_register('email2@gmail.com', 'validpass', 'Peter', 'Steven')
    token2 = dict['token']
    assert(is_logged_in(token2))

#All details are valid
def test_auth_register_3():
    reset_data()
    dict = auth_register('email3@gmail.com', 'validpass', 'Same', 'Same')
    token = dict['token']
    assert(is_logged_in(token))

#All details are valid
def test_auth_register_4():
    reset_data()
    dict = auth_register('email4@gmail.com', 'validpass', 'Y()@#@!#*##@', '#@$)(#)$(()#$()(#)@$)')
    token = dict['token']
    assert(is_logged_in(token))

#All details are valid (name is exactly 50 characters)
def test_auth_register_5():
    reset_data()
    dict = auth_register('emaail5@gmail.com', 'validpass', 'thisisindeeddefinitelyfiftycharacterslongexactlyxx', 'thisisindeeddefinitelyfiftycharacterslongexactlyxy')
    token = dict['token']
    assert(is_logged_in(token))

#Password is less than 6 characters (4)
def test_auth_register_6():
    reset_data()
    with pytest.raises(ValueError):
        auth_register('email6@gmail.com', 'four', 'First', 'Last')

#First name exceeds 50 characters
def test_auth_register_7():
    reset_data()
    with pytest.raises(ValueError):
        auth_register('email6@gmail.com', 'validPasss', 'Greaterthanfiftycharactersfirstnamewhichiswaytoolong', 'Last')

#Last name exceeds 50 characters
def test_auth_register_8():
    reset_data()
    with pytest.raises(ValueError):
        auth_register('email6@gmail.com', 'validPasss', 'First', 'GreaterthanfiftycharactersLastnamewhichiswaytoolong')

#Email address is already registered
def test_auth_register_9():
    reset_data()
    dict = auth_register('email1@gmail.com', 'validpass', 'Yasin', 'Kevin')
    with pytest.raises(ValueError):
        auth_register('email1@gmail.com', 'validPasss', 'First', 'Last')

#invalid email address
def test_auth_register_10():
    reset_data()
    with pytest.raises(ValueError):
        auth_register('1nVal1d3mail', 'validPasss', 'First', 'Last')


#Different combinations of invalid email, pass, first name, last name

def test_auth_register_11():
    reset_data()
    with pytest.raises(ValueError):
        auth_register('1nVal1d3mail', 'four', 'First', 'Last')

def test_auth_register_12():
    reset_data()
    with pytest.raises(ValueError):
        auth_register('1nVal1d3mail', 'four', 'Greaterthanfiftycharactersfirstnamewhichiswaytoolong', 'Last')

def test_auth_register_13():
    reset_data()
    with pytest.raises(ValueError):
        auth_register('1nVal1d3mail', 'four', 'Greaterthanfiftycharactersfirstnamewhichiswaytoolong', 'GreaterthanfiftycharactersLastnamewhichiswaytoolong')

def test_auth_register_14():
    reset_data()
    with pytest.raises(ValueError):
        auth_register('', '', '', '')

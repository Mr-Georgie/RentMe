# from authentication.models import User # for demo purposes only

def completed_profile(user):
    
    error_messages = []
    is_incomplete = []
    
    checks = {
        'bank account number': user.bank_account_number == None,
        'bank name': user.bank_name == None,
        'country': user.country == None,
        'phone number': user.phone_number == None
    }
    
    for field, check in checks.items():
        if check == True:
            error_messages.append('Please provide your ' + field + ' in your account page')
            is_incomplete.append(check)
    
    if True in is_incomplete:
        return {
            "is_profile_complete": False,
            "message": error_messages
        }
    
    else:
        return {
            "is_profile_complete": True,
            "message": None
        }

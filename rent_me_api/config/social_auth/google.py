from google.auth.transport import requests
from google.oauth2 import id_token
# import google


class Google:
    """Google class to fetch the user info """
    
    @staticmethod
    def validate(auth_token):
        """
        validates google auth token
        """
        try:
            id_info = id_token.verify_oauth2_token(
                auth_token, requests.Request()
            )
            
            print("Google User Id gotten successfully")
            
            if 'accounts.google.com' in id_info['iss']:
                return id_info
            
        except:
            # print(id_info)
            return "The token is either invalid or has expired"
        
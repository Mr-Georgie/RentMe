# from google.auth.transport import requests
# from google.oauth2 import id_token
import google


class Google:
    """Google class to fetch the user info """
    
    @staticmethod
    def validate(auth_token):
        """
        blah blah blah 
        """
        try:
            id_info = google.oauth2.id_token.verify_oauth2_token(
                auth_token, google.auth.transport.requests.Request()
            )
            
            if 'accounts.google.com' in id_info['iss']:
                return id_info
            
        except:
            return "The token is either invalid or has expired"
        
import facebook


class Facebook:
    """ Facebook class to fetch ..."""
    
    @staticmethod
    def validate(auth_token):
        """ validate method Queries ..."""
        
        try:
            graph = facebook.GraphAPI(access_token=auth_token)
            profile = graph.request('/me?fields=name,email')
            return profile
        except:
            return "The token is invalid or expired."
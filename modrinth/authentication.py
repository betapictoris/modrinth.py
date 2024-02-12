class State:
    def __init__(self, token: str):
        '''
        Currently this simply stores the token you supply, in the future it
        should be able to do more. 
        '''
        self.token: str = token

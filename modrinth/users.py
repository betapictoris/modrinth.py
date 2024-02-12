import requests

class User:
    def __init__(self, user: str):
        '''
        Stores information on `user`'s (username or ID) profile information.
        '''

        url  = f'https://api.modrinth.com/v2/user/{user}'
        data = requests.get(url).json()

        self.username = data['username']
        self.name = data['name']
        self.email = data['email']
        self.bio = data['bio']

        # TODO: Potentially parse this in a meaningful way
        self.payoutData = data['payout_data']

        self.id = data['id']
        self.avatarURL = data['avatar_url']
        
        # TODO: Potentially parse this as well.
        self.created   = data['created']

        self.role = data['role']
        self.badges = data['badges']
        self.authProviders = data['auth_providers']
        self.emailVerified = data['email_verified']
        self.hasPassword = data['has_password']
        self.hasTOTP = data['has_totp']
        self.githubID = data['github_id']

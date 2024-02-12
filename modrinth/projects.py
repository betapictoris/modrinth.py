import requests

class Project:
    def __init__(self, project: str):
        '''
        Takes a project ID or slug and gathers the information about that
        project.
        '''

        url  = f'https://api.modrinth.com/v2/project/{project}'
        data = requests.get(url).json()
        
        self.id          = data['id']
        self.slug        = data['slug']
        self.title       = data['title']
        self.team        = data['team']
        self.description = data['description']
        self.body        = data['body']

        self.gallery = data['gallery']

        self.clientSide = data['client_side']
        self.serverSide = data['server_side']

        self.status             = data['status']
        self.requestedStatus    = data['requested_status']
        self.monetizationStatus = data['monetization_status']

        self.categories           = data['categories']
        self.additionalCategories = data['additional_categories']

        self.issuesURL     = data['issues_url']
        self.sourceURL     = data['source_url']
        self.wikiURL       = data['wiki_url']
        self.discordURL    = data['discord_url']
        self.dontationURLs = data['donation_urls']
        self.iconURL       = data['icon_url']
        self.bodyURL       = data['body_url']

        self.downloads = data['downloads'] 
        self.followers = data['followers']

        self.projectType      = data['project_type']
        self.threadID         = data['thread_id']
        self.moderatorMessage = data['moderator_message']

        self.versions     = data['versions']
        self.gameVersions = data['game_versions']
        self.loaders      = data['loaders']

        # TODO: Maybe parse these
        self.published  = data['published']
        self.updated    = data['updated']
        self.approved   = data['approved']
        self.queued     = data['queued']
        
        # TODO: Maybe parse this
        self.license = data['license']


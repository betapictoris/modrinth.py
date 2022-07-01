#!/usr/bin/env python3
# -*- coding: utf8 -*-
'''
Modrinth.py - __init__.py 

Developed by Beta Pictoris <beta@ozx.me>
Modrinth Python API 
'''

import requests

__version__ = '0.1.0'

class Authentication:
    '''
    Authentication is done using a GitHub token, in the request header. Modrinth.py will automatically add
    the token to the request header and Labrinth's documentation says that the token is required for these
    requests: 
     - those which create data (such as version creation)
     - those which modify data (such as editing a project)
     - those which access private data (such as draft projects and notifications)

    For more information, see: https://docs.modrinth.com/api-spec/#section/Authentication
    '''
    class User:
        def __init__(self, token: str):
            '''
            token   ==>  String   ==>  GitHub token
            '''
            self.token: str = token

class Projects:
    class ModrinthProject:
        def __init__(self, project: str) -> None:
            '''
            project   ==>  String   ==>  Project ID or slug   |  Example: 'gravestones' or 'ssUbhMkL'
            '''

            url: str = 'https://api.modrinth.com/v2/project/{id}'
            data: dict = requests.get(url.format(id=project)).json()
            self.url: str = url.format(id=project)
            
            self.id: str                 = data['id']
            self.slug: str               = data['slug']
            self.projectType: str        = data['project_type']
            self.team: str               = data['team']
            self.name: str               = data['title']
            self.desc: str               = data['description']
            self.body: str               = data['body']
            self.bodyURL: str            = data['body_url']
            self.published: str          = data['published']
            self.updated: str            = data['updated']
            self.status: str             = data['status']
            self.moderatorMessage: str   = data['moderator_message']
            self.license: dict           = data['license']
            self.clientSide: str         = data['client_side']
            self.serverSide: str         = data['server_side']
            self.downloads: int          = data['downloads']
            self.followers: int          = data['followers']
            self.categories: list        = data['categories']
            self.versions: list          = data['versions']
            self.iconURL: str            = data['icon_url']
            self.issuesURL: str          = data['issues_url']
            self.sourceURL: str          = data['source_url']
            self.wikiURL: int            = data['wiki_url']
            self.discordURL: str         = data['discord_url']
            self.donationURLs: list      = data['donation_urls']
            self.gallery: list           = data['gallery']

        def toDict(self) -> dict:
            '''
            Convert the project object to a dictionary.
            '''
            return {'id': self.id, 'slug': self.slug, 'project_type': self.projectType, 'team': self.team, 'title': self.name, 'description': self.desc, 'body': self.body, 'body_url': self.bodyURL, 'published': self.published, 'updated': self.updated, 'status': self.status, 'moderator_message': self.moderatorMessage, 'license': self.license, 'client_side': self.clientSide, 'server_side': self.serverSide, 'downloads': self.downloads, 'followers': self.followers, 'categories': self.categories, 'versions': self.versions, 'icon_url': self.iconURL, 'issues_url': self.issuesURL, 'source_url': self.sourceURL, 'wiki_url': self.wikiURL, 'discord_url': self.discordURL, 'donation_urls': self.donationURLs, 'gallery': self.gallery}

        def isServerSide(self) -> bool:
            '''
            Check if the project is server side.
            '''
            if self.serverSide == 'optional' or self.serverSide == 'required':
                return True
        
        def isClientSide(self) -> bool:
            '''
            Check if the project is client side.
            '''
            if self.clientSide == 'optional' or self.serverSide == 'required':
                return True
        
        def isUniversal(self) -> bool:
            '''
            Check if the project is both server side or client side.
            '''
            if self.serverSide in ['universal', 'required'] and self.clientSide in ['universal', 'required']:
                return True
        
        def getDependencies(self) -> dict:
            '''
            Get the project dependencies.
            '''
            data = requests.get(self.url + '/dependencies').json()

            # TODO: Convert this to an object
            return data
        
        def follow(self, user: Authentication.User):
            '''
            Follow a project, given a user.
            '''
            url = self.url + '/follow'
            headers = {'Authorization': user.token}
            requests.post(url, headers=headers)
        
        def unfollow(self, user: Authentication.User):
            '''
            Unfollow a project, given a user. 
            '''
            url = self.url + '/follow'
            headers = {'Authorization': user.token}
            requests.delete(url, headers=headers)
        
        def getVersion(self, version):
            '''
            Shorthand for Versions.Version with no project argument
            '''
            return Versions.ModrinthVersion(self, version=version)

    class Search:
        def __init__(self, query: str, categories: list=[], versions: list=[], project_types: list=[], licenses: list=[], index: str='relevance', offset: int=0, limit: int=10, filters: str="") -> None:
            '''
            query           ==>   String   ==>  The query to search for          |   Example: 'gravestones'
            categories      ==>   List     ==>  The categories to search for     |   Example: ['gravestones', 'gravestones-mod']
            versions        ==>   List     ==>  The versions to search for       |   Example: ['1.0.0', '1.0.1']
            project_types   ==>   List     ==>  The project types to search for  |   Example: ['mod', 'modpack']
            licenses        ==>   List     ==>  The licenses to search for       |   Example: ['MIT', 'GPLv3']
            index           ==>   String   ==>  The index to search for          |   Example: 'relevance', 'downloads', 'follows', 'newest', 'updated'
            offset          ==>   Int      ==>  The offset to search for         |   Example: 0
            limit           ==>   Int      ==>  The limit to search for          |   Example: 10
            filters         ==>   String   ==>  The filters to search for        |   Example: 'categories="fabric" AND (categories="technology" OR categories="utility")'
            '''

            cats: str = ""
            for category in categories:
                cat: str = f'["categories:{category}"]'
                cats += cat

                if len(categories) > 1 and category != categories[len(categories) - 1]:
                    cats += ","
            
            vers: str = ""
            for version in versions:
                ver: str = f'["versions:{version}"]'
                vers += ver
                
                if len(versions) >1  and version != versions[len(versions) - 1]:
                    vers += ','
            
            proj_types: str = ""
            for project_type in project_types:
                proType: str = f'["project_type:{project_type}"]'
                proj_types += proType
                
                if len(project_types) and project_type != project_types[len(project_types) - 1]:
                    proj_types += ','

            lics = ""
            for license in licenses:
                lic: str = f'["license:{license}"]'
                lics += lic
                
                if len(licenses) and license != licenses[len(licenses) - 1]:
                    lics += ','
            
            facets = "["
            if cats != "":
                facets += cats
            if vers != "":
                if cats != "":
                    facets += ","
                facets += vers
            if proj_types != "":
                if cats != "" or vers != "":
                    facets += ","
                facets += proj_types
            if lics != "":
                if cats != "" or vers != "" or proj_types != "":
                    facets += ","
                facets += lics
            facets += "]"
            facetsInURL: str = ""
            if facets != "[]":
                facetsInURL = f'&facets={facets}'


            url: str = f'https://api.modrinth.com/v2/search?query={query}{facetsInURL}&index={index}&offset={offset}&limit={limit}&filters={filters}'
            r: requests.Response = requests.get(url)
            rJSON: dict = r.json()

            self.hits: list   = []
            for hit in rJSON['hits']:
                project = Projects.ModrinthProject(hit['project_id'])
                self.hits.append(project)
            self.offset: int  = rJSON['offset']
            self.limit:  int  = rJSON['limit']
            self.total:  int  = rJSON['total_hits']

        def toDict(self) -> dict:
            return {'hits': self.hits, 'offset': self.offset, 'limit': self.limit, 'total': self.total}

class Versions:
    '''
    Versions have information about the version of a project, including the change log, downloads,
    and downloads. 
    '''
    class ModrinthVersion:
        def __init__(self, project:Projects.ModrinthProject, version:str):
            '''
            project    ==>  ModrinthProject type    ==>     The project to be getting the version of
            version    ==>  String                  ==>     The version of the project to be getting
            '''
            # Check the values of project and version to see if they are valid.
            if not isinstance(project, Projects.ModrinthProject):
                raise TypeError("project must be a ModrinthProject type")
            if version not in project.versions:
                raise ValueError("version must be a valid version of the project")
            
            self.project: Projects.ModrinthProject = project
            self.version: str = version
            self.url: str = f'https://api.modrinth.com/v2/version/{version}'

            r: requests.Response = requests.get(self.url)
            rJSON: dict = r.json()

            self.projectID:     str = rJSON['project_id']
            self.AuthorID:      str = rJSON['author_id']
            self.datePublished: str = rJSON['date_published']
            self.downloads:     int = rJSON['downloads']
            self.files:        list = rJSON['files']
            self.name:          str = rJSON['name']
            self.versionNumber: str = rJSON['version_number']
            self.gameVersions: list = rJSON['game_versions']
            self.versionType:   str = rJSON['version_type']
            self.loaders:      list = rJSON['loaders']
            self.featured:     bool = rJSON['featured']
            self.changeLog:     str = rJSON['changelog']
            self.dependencies: list = rJSON['dependencies']
            self.changeLogURL:  str = rJSON['changelog_url']
        
        def getPrimaryFile(self, hash:str='sha1') -> str:
            '''
            Returns the primary file hash of the version.
            '''
            if hash not in ['sha1', 'sha512']:
                raise ValueError("hash must be either sha1 or sha512")
            for file in self.files:
                if file['primary']:
                    return file['hashes'][hash]
            raise ValueError("No primary file found")
        
        def getDownload(self, hash, hashMethod:str='sha1') -> str:
            '''
            Returns the download link of the version.
            '''
            if hashMethod not in ['sha1', 'sha512']:
                raise ValueError("hash must be either sha1 or sha512")
            for file in self.files:
                if file['hashes'][hashMethod] == hash:
                    return file['url']
            raise ValueError("No download with that hash was found")
#!/usr/bin/env python3
# -*- coding: utf8 -*-
'''
Modrinth.py - __init__.py 

Developed by Beta Pictoris <beta@ozx.me>
Modrinth Python API 
'''

import requests
from warnings import warn

__version__ = '0.1.5'

BASE_URL = 'https://api.modrinth.com'

import modrinth.users
import modrinth.authentication
import modrinth.projects

class Projects:
    class Search:
        def __init__(self, query: str, categories: list = [], versions: list = [], project_types: list = [], licenses: list = [], index: str = 'relevance', offset: int = 0, limit: int = 10, filters: str = "") -> None:
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

                if len(versions) > 1 and version != versions[len(versions) - 1]:
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

            url: str = BASE_URL + f'/v2/search?query={query}{facetsInURL}&index={index}&offset={offset}&limit={limit}&filters={filters}'
            r: requests.Response = requests.get(url)
            rJSON: dict = r.json()

            self.hits: list = []
            for hit in rJSON['hits']:
                project = projects.Project(hit['project_id'])
                self.hits.append(project)
            self.offset: int = rJSON['offset']
            self.limit:  int = rJSON['limit']
            self.total:  int = rJSON['total_hits']

        def toDict(self) -> dict:
            return {'hits': self.hits, 'offset': self.offset, 'limit': self.limit, 'total': self.total}


class Versions:
    '''
    Versions have information about the version of a project, including the change log, downloads,
    and downloads. 
    '''
    class ModrinthVersion:
        def __init__(self, project: projects.Project, version: str):
            '''
            project    ==>  ModrinthProject type    ==>     The project to be getting the version of
            version    ==>  String                  ==>     The version of the project to be getting
            '''
            # Check the values of project and version to see if they are valid.
            if not isinstance(project, projects.Project):
                raise TypeError("project must be a ModrinthProject type")
            if version not in project.versions:
                raise ValueError(
                    "version must be a valid version of the project")

            self.project: projects.Project = project
            self.version: str = version
            self.url: str = BASE_URL + f'/v2/version/{version}'

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
        
        def getFiles(self, hash: str = 'sha1', primary: bool = True, optional: bool = True) -> str:
            '''
            Returns the file hashes of the version.
            '''
            files = []

            if hash not in ['sha1', 'sha512']:
                raise ValueError("hash must be either sha1 or sha512")
            for file in self.files:
                if file['primary'] and primary:
                    files.append(file['hashes'][hash])
                elif not file['primary'] and optional:
                    files.append(file['hashes'][hash])
            
            return files


        def getPrimaryFile(self, hash: str = 'sha1') -> str:
            '''
            Returns the primary file hash of the version.

            Deprecate: Use getFiles instead, getPrimaryFile may be removed in
                       a future update.
            '''
            warn("getPrimaryFile is deprecated, use getFiles instead.")
            if hash not in ['sha1', 'sha512']:
                raise ValueError("hash must be either sha1 or sha512")
            for file in self.files:
                if file['primary']:
                    return file['hashes'][hash]
            raise ValueError("No primary file found")

        def getDownload(self, hash, hashMethod: str = 'sha1') -> str:
            '''
            Returns the download link of the version.
            '''
            if hashMethod not in ['sha1', 'sha512']:
                raise ValueError("hash must be either sha1 or sha512")
            for file in self.files:
                if file['hashes'][hashMethod] == hash:
                    return file['url']
            raise ValueError("No download with that hash was found")

    def getVersions(project: projects.Project, ids: list) -> list:
        '''
        Get a list of versions, given a list of IDs.
        '''
        return [Versions.ModrinthVersion(project, id) for id in ids]
    
    def getLatestVersion(project: projects.Project) -> ModrinthVersion:
        '''
        Gets the latest version, given a project.
        '''
        return project.getAllVersions()[-1]

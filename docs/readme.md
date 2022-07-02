# Modrinth.py
Interact with Modrinth's Labrinth API through Python. 

## API Version

 Service              | Version
----------------------|----------
 Modrinth.py version  | v0.1.2
 Labrinth API version | v2.4.4

*Modrinth.py works on the latest Labrinth version!*

## To-do
 - [x] Search for projects
 - [x] (Un)follow projects
 - [x] Basic authentication
 - [ ] Documentation
 - [ ] Create and delete projects
 - [ ] Modify projects (PATCH requests to `/project/{id|slug}` and `/project/{id|slug}/gallery` requests)
 - [x] Built-in function to get multiple projects at once
 - [ ] Project dependencies management
 - [x] Get project versions
 - [x] Get project details
 - [ ] Create, modify, and delete projects (POST requests to `/version` and PATCH/DELETE to `/version/{id}`)
 - [x] Built-in function to get multiple versions
 - [ ] Upload files to version
 - [ ] Get a version from `sha1` or `sha512`
 - [ ] Delete a file from its hash (DELETE requests to `/version_file`)
 - [ ] Get latest project(s) version(s)
 - [ ] Get project version from hash
 - [ ] Read user(s) data
 - [ ] Delete and modify user data
 - [ ] Read team data 
 - [ ] Add users to teams
 - [ ] Join a team
 - [ ] Modify user roles/perms within a team
 - [ ] Remove user(s) from a team
 - [ ] Change team owner
 - [ ] Get categories, mod loaders, game versions, licenses, donation sites, and report types. ("tags")
 - [ ] Support for more branches (ie. staging)



## API Documentation

### Usage
#### Through pip
```bash
pip install modrinth
```
View the project page on [GitHub](https://github.com/BetaPictoris/modrinth.py) or [pip](https://pypi.org/project/modrinth/)

### Users (`Users`)
User data includes their username, name, email, bio, etc. this class hold functions and objects that relate
to authentication and user data.  

Authentication is done using a GitHub token, in the request header. Modrinth.py will automatically add
the token to the request header and Labrinth's documentation says that the token is required for these
requests: 
 - those which create data (such as version creation)
 - those which modify data (such as editing a project)
 - those which access private data (such as draft projects and notifications)

For more information, see: https://docs.modrinth.com/api-spec/#section/Authentication

#### User 
```python
user = modrinth.Users.ModrinthUser('yyy') # Find a user with the username/ID yyy

print(user.name)  # Print the user's name
```

#### Authentication
```python
authedUser = modrinth.Users.AuthenticatedUser('ghp_xxx') # GitHub token

# After authentication we can interact with projects, such as following and unfollowing a mod.
project = modrinth.Projects.ModrinthProject('zzz')
project.unfollow(authedUser)
```

## Getting project information
### Projects (`Projects`)
The `Projects` class is used to interact with projects. These interactions include getting a project from slug/ID, searching for projects, and (un)following a project. With more projects being planned, this class will be expanded. Projects are mods and modpacks.

#### Searching for projects
```python
projects = modrinth.Projects.Search('mod')
print(projects.hits[0].name) # Prints the name of the first project found
```

#### Get project from slug/ID
```python
project = modrinth.Projects.ModrinthProject('zzz')
print(project.name) # Prints the name of the project
```

## Getting version information
### Versions (`Versions`)
The `Versions` class is used to interact with versions. It currently can only get version information, such as downloads and files. 
#### Get version information
The suggested way to get a version is through the `Project.ModrinthProject.getVersion()` shorthand, although you can also use the `Versions.ModrinthVersion` class directly.
```python
project = modrinth.Projects.ModrinthProject('zzz') # Get a project from slug/ID
version = project.getVersion('aaa111bb')           # Get the version with ID 'aaa111bb'

primaryFile = version.getPrimaryFile()  # Returns the hash of the primary file
print(version.getDownload(primaryFile)) # Returns the download URL of the primary file
```
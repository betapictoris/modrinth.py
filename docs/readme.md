# Modrinth.py
Interact with Modrinth's Labrinth API through Python. 

## API Version

 Service              | Version
----------------------|----------
 Modrinth.py version  | v0.0.1
 Labrinth API version | v2.4.4

*Modrinth.py works on the latest Labrinth version!*

## To-do
 - [x] Search for projects
 - [x] (Un)follow projects
 - [x] Basic authentication
 - [ ] Documentation
 - [ ] Create and delete projects
 - [ ] Modify projects (PATCH requests to `/project/{id|slug}` and `/project/{id|slug}/gallery` requests)
 - [ ] Built-in function to get multiple projects at once
 - [ ] Project dependencies management
 - [ ] Get project versions
 - [ ] Get project details
 - [ ] Create, modify, and delete projects (POST requests to `/version` and PATCH/DELETE to `/version/{id}`)
 - [ ] Built-in function to get multiple versions
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
### Authentication (`Authentication` and `Authentication.User`)
Authentication is done using a GitHub token, in the request header. Modrinth.py will automatically add the token to the request header and Labrinth's documentation says that the token is required for these requests: 

 - those which create data (such as version creation)
 - those which modify data (such as editing a project)
 - those which access private data (such as draft projects and notifications)

#### Demo
```python
authedUser = modrinth.Authentication.User('ghp_xxx') # GitHub token

# After authentication we can interact with projects, such as following and unfollowing a mod.
project = modrinth.Projects.ModrinthProject('zzz')
project.unfollow(authedUser)
```
For more information, see: https://docs.modrinth.com/api-spec/#section/Authentication

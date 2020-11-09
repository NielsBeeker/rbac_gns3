# rbac_gns3
Working on a rbac implementation

#About: 

src/db: Contains db for the project

src/dependencies: Contains middleware for api

src/endpoint: Contains functions for api's endpoint

src/models: Contains class to use for the different functions


#Todo:

-create little database manager for local project

-create database, table and fill it in local

-get user scope from db

-get user role from db

-get user deny scope from db

-add all user info to the token

#Working:

-verify if role fits with endpoint

-verify if deny scopes fits with endpoint

-verify if scopes fits with endpoint

-get usage from endpoint


#Done: 


-authenticate and create an encoded token throw a endpoint and return it

-get current user and decode its token

-get deny scope from user, get role from user, get scope from user

#Tested:





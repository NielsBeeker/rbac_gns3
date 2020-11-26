# rbac_gns3

Working on a rbac implementation for gns3

#About: 

    src/db: Contains db for the project

    src/dependencies: Contains middleware for apim

    src/endpoint: Contains functions for api's endpoint

    src/models: Contains class to use for the different functions


#Todo:
    
    create a function to generate test

    create unit tests for all endpoint
    
#Working:

    finish get_get_scope and get_post_scope

    check scope matching

#Done: 
    
    authentication:
        -create acces_token and return it
        -get all information about user and put it in the token
    
    verification:
        -get request and return endpoint object related to the query
        -decode the token and get all information about
        -verify that the scope are matching with permission and role
    
    test:
        -added pytest to project
        -add user_token to test
#Tested:
    




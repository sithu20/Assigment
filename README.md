

API List

1) https://0ezmflojw5.execute-api.ap-southeast-1.amazonaws.com/prod/register/ (User Registration)
2) https://0ezmflojw5.execute-api.ap-southeast-1.amazonaws.com/prod/login/ (User Login)
3) https://0ezmflojw5.execute-api.ap-southeast-1.amazonaws.com/prod/profile/ (User Profile, Need to add Authorization parameter in header with JWT Token)
4) https://0ezmflojw5.execute-api.ap-southeast-1.amazonaws.com/prod/alloccupation/ (ALl Occupations of Users)
5) https://0ezmflojw5.execute-api.ap-southeast-1.amazonaws.com/prod/user/1/occupation/ (individual user's occupation, required authentication)
6) https://0ezmflojw5.execute-api.ap-southeast-1.amazonaws.com/prod/occupation/1 
   1) Create Occupation : /occupation/ (Post Method)
   2) View Detail Occupation : /occupation/occupation_id (GET Method)
   3) Update Detail Occupation : /occupation/occupation_id , PUT Method
7) https://0ezmflojw5.execute-api.ap-southeast-1.amazonaws.com/prod/deletememcode/ (Delete Memercode of requested user)
8) https://0ezmflojw5.execute-api.ap-southeast-1.amazonaws.com/prod/loginlogs (User Login Logs)
9) https://0ezmflojw5.execute-api.ap-southeast-1.amazonaws.com/prod/allusers (All User List)

POSTMAN collection
https://www.getpostman.com/collections/6c5ff3f7b9052909bdcf


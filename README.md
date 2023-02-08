# API Final Project Documentation


# Roles <br>

| ROLE | GROUP | HAS RESTRICTION | CAN PERFORM (ACTIONS) |
| --- | --- | --- | --- |
| Unauthenticated |     | YES | 1 |
| Customer | Customer | YES |  |
| Delivery Crew | Delivery Crew | YES |  |
| Manager | Manager | YES |  |
| System Administrator | SysAdmin | NO |  |
<br><br>


# Users Endpoints<br>

**/api/users**

| ROLE | METHOD | ACTION | METHOD | ACTION | RESTRICTIONS |
| --- | --- | --- | --- | --- | --- |
| Unauthenticated | GET | Not allowed | POST | Create new customer | Can only create users |
| Customer |
| Manager | GET | RETRIVE users in Customer and Manager groups | | | Can't list users in the Admin group |
| Admin | GET | RETRIVE users in every group | | | None |
<br>

**/api/users/me**

| ROLE | METHOD | ACTION | METHOD | ACTION | RESTRICTIONS |
| --- | --- | --- | --- | --- | --- |
| Customer | GET | User details | PUT, PATCH, DELETE | Update and delete the user |
| Manager | GET | See customers’ and managers’ account details | POST, DELETE | Update and delete customers, managers |
| Admin | GET | See customers, managers, and admins | POST, DELETE | Create and delete customers, managers, and admins |
<br>

# Groups Endpoints <br>

**/api/groups**

| ROLE | METHOD | ACTION | METHOD | ACTION | RESTRICTIONS |
| --- | --- | --- | --- | --- | --- |
| Manager | GET | RETRIVE the list of groups | POST | CREATE groups | Admin group is unreachable |
| Admin | GET | Retrive the list of groups | POST | CREATE groups | None |
<br>

**api/groups/{groupId}**

| ROLE | METHOD | ACTION | METHOD | ACTION | RESTRICTIONS |
| --- | --- | --- | --- | --- | --- |
| Manager | GET | RETRIVE details for the group | PUT, PATCH, DELETE | UPDATE and DELETE groups | Not allowed to UPDATE or DELETE Manager and Admin groups |
| Admin | GET | RETRIVE details for the group | PUT, PATCH, DELETE | CREATE, UPDATE, and DELETE groups | None |
<br>

### Customers
**api/groups/customers**

| ROLE | METHOD | ACTION | METHOD | ACTION | RESTRICTIONS |
| --- | --- | --- | --- | --- | --- |
| Manager | GET | RETRIVE the list of users in Customer group | POST, DELETE | ADD/DELETE users to/from the Customer group | None |
| Admin | GET | RETRIVE the list of users in Customer group | POST, DELETE | ADD/DELETE users to/from the Customer group |
<br>

**api/groups/customers/{userId}**

| ROLE | METHOD | ACTION | METHOD | ACTION | RESTRICTIONS |
| --- | --- | --- | --- | --- | --- |
| Customer | GET | RETRIEVE user details | PUT, PATCH, DELETE | UPDATE, DELETE user | Customers can only interact with their owr user |
| Manager | GET | RETRIEVE user details | PUT, PATCH, DELETE | UPDATE, DELETE user | None |
| Admin | GET | RETRIEVE user details | PUT, PATCH, DELETE | UPDATE, DELETE user | None |
<br>

### Delivery Crew
**api/groups/delivery-crew**

| ROLE | METHOD | ACTION | METHOD | ACTION | RESTRICTIONS |
| --- | --- | --- | --- | --- | --- |
| Manager | GET | RETRIEVE lits of users in Delivery Crew group | POST, DELETE | ADD/DELETE users to/from Delivery Crew group | None |
| Admin | GET | RETRIEVE lits of users in Delivery Crew group | POST, DELETE | ADD/DELETE users to/from Delivery Crew group | None |
<br

**api/groups/delivery-crew/{userId}**

| ROLE | METHOD | ACTION | METHOD | ACTION | RESTRICTIONS |
| --- | --- | --- | --- | --- | --- |
| Delivery Crew | GET | RETRIEVE user details | PUT, PATCH, DELETE | UPDATE/DELETE user | Other Delivery Crew users are unrechable |
| Manager | GET | RETRIEVE user details | PUT, PATCH, DELETE | UPDATE/DELETE user | None
| Admin | GET | RETRIEVE user details | PUT, PATCH, DELETE | UPDATE/DELETE user | None
<br

### Managers
**api/groups/managers/**

| ROLE | METHOD | ACTION | METHOD | ACTION | RESTRICTIONS |
| --- | --- | --- | --- | --- | --- |
| Manager | GET | RETRIEVE lits of users in Manager group | POST | ADD users to/from Manager group | None |
| Admin   | GET | RETRIEVE lits of users in Manager group | POST | ADD users to/from Manager group | None |
<br

**api/groups/managers/{userId}**

| ROLE | METHOD | ACTION | METHOD | ACTION | RESTRICTIONS |
| --- | --- | --- | --- | --- | --- |
| Manager | GET | RETRIEVE user details | PUT, PATCH, DELETE | UPDATE/DELETE user | Managers can only UPDATE/DELETE their own user |
| Admin   | GET | RETRIEVE user details | PUT, PATCH, DELETE | UPDATE/DELETE user | None |
<br

### Admins
**api/groups/admins/**

| ROLE | METHOD | ACTION | METHOD | ACTION | RESTRICTIONS |
| --- | --- | --- | --- | --- | --- |
| Admin | GET | RETRIEVE lits of users in Admin group | POST, DELETE | ADD/DELETE users to/from Admin group | None |
<br

**api/groups/delivery-crew/{userId}**

| ROLE | METHOD | ACTION | METHOD | ACTION | RESTRICTIONS |
| --- | --- | --- | --- | --- | --- |
| Admin | GET | RETRIEVE user details | PUT, PATCH, DELETE | UPDATE/DELETE user | None |
<br


# Menu Items

**api/groups/menu-items/**

| ROLE | METHOD | ACTION | METHOD | ACTION | RESTRICTIONS |
| --- | --- | --- | --- | --- | --- |
| Customer      | GET | RETRIEVE lits of menu-items | POST, DELETE | Methods not allowed for Customers     | Customers can only see menu-items |
| Delivery Crew | GET | RETRIEVE lits of menu-items | POST, DELETE | Methods not allowed for Delivery Crew | Delivery Crew can only see menu-items |
| Manager       | GET | RETRIEVE lits of menu-items | POST, DELETE | ADD menu-items                        | None |
| Admin         | GET | RETRIEVE lits of menu-items | POST, DELETE | ADD menu-items                        | None |
<br

**api/groups/menu-items/{menu-itemId}**

| ROLE | GET | PUT/PATCH/DELETE | RESTRICTIONS |
| --- | --- | --- | --- |
| Customer      | RETRIEVE menu-items details | Methods not allowed for Customers     | Customers can only see menu-items |
| Delivery Crew | RETRIEVE menu-items details | Methods not allowed for Delivery Crew | Delivery Crew can only see menu-items |
| Manager       | RETRIEVE menu-items details | UPDATE/DELETE menu-items              | None |
| Admin         | RETRIEVE menu-items details | UPDATE/DELETE menu-items              | None |
<br


# Order Items

**api/groups/order-items/**

| ROLE | GET | POST | RESTRICTIONS |
| --- | --- | --- | --- |
| Customer      | RETRIEVE list of order-items | CREATE order-items                    | None |
| Delivery Crew | RETRIEVE list of order-items | Methods not allowed for Delivery Crew | Delivery Crew can only see order-items |
| Manager       | RETRIEVE list of order-items | CREATE order-items                    | None |
| Admin         | RETRIEVE list of order-items | CREATE order-items                    | None |
<br

**api/groups/order-items/{order-itemId}**

| ROLE | GET | PUT/PATCH/DELETE | RESTRICTIONS |
| --- | --- | --- | --- |
| Customer      | RETRIEVE order-items details | UPDATE/DELETE order-item               | None |
| Delivery Crew | RETRIEVE order-items details | Methods not allowed for Delivery Crew  | Delivery Crew can only see order-items |
| Manager       | RETRIEVE order-items details | UPDATE/DELETE order-item               | None |
| Admin         | RETRIEVE order-items details | UPDATE/DELETE order-item               | None |
<br


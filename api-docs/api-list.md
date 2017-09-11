# 7Chefs API Documentation
This `api` documentation contains a list of available Restful `api` for interacting with 7Chefs backend server.

## Available APIs
- [Recipe Related APIs](#recipe)
- [User Related Api](#user)


## Recipe

### View recipe details
View a recipe details with a recipe id

```
GET - api/v1.0/recipe/{recipe_id}/
```
```
Sample Response:
STATUS: 200 OK
```

### Upload empty recipe
Allow uploading a recipe with at least its name, and description

```
POST - api/v1.0/recipe/upload/
```
```
Sample Request Body:
{
    "name": "Recipe 1",
    "description": "New Recipe",
    "difficulty": 0,
    "duration_minute": 60,
    "duration_hour": 1
}
```
```
Sample Response:
STATUS: 201 CREATED
```

### Comment a recipe
Comment a recipe by providing a recipe id. Comment text should be send in body param
```
POST - api/v1.0/recipe/comment/{recipe_id}/
```
```
Sample Request Body:
{
    "comment": "Comment for the recipe"
}
```
```
Sample Response:
STATUS: 201 CREATED
```

### Add recipe tag to a recipe
Add a tag to recipe by providing a recipe id. A list of tag id should be provided in body param
```
POST - api/v1.0/recipe/add/tag/{recipe_id}/
```
```
Sample Request Body:
{
    "tag_ids": [1,2]
}
```
```
Sample Response:
STATUS: 201 CREATED
```

## User

### Create a new user account
Create a new user account with email, username and password

```
POST - api/v1.0/user/signup/
```
```
Sample Request Body:
{
    "email": "admin@example.com",
    "username": "admin",
    "password": "password1"
}
```
```
Sample Response:
STATUS: 201 CREATED
```

### View profile of a user
View the profile of a user given a user id

```
POST - api/v1.0/user/profile/{user_id}/
```
```
Sample Response:
STATUS: 200 OK
```

### View profile of all username
View the profile of all user

```
POST - api/v1.0/user/all/
```
```
Sample Response:
STATUS: 200 OK
```

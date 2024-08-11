# Social-Media
#### A Django Social-Media with templates .

## Tools :
- Django
- HTML
- Css
- Java Script
  
## Featues :
- Register , Login, Logout, Email Confirmation
- Public Profile view , Edit profile settings
- Follow and Unfollow another profiles
- Feed with recently posts
- Create custom Posts with text and pics , Delete Posts
- Like , Unlike , Comments on posts
- Searching for username
- Suggested users

## Installation :
  ### Requirements
  - Python (3.x.x)
  ### SetUp
  - Create virtual environment in Unix , Windows
    ```
    python -m venv venv
    ```
  - Copy project folder to /venv/
    
  - Activate Virtual Environment
    
    Windows
    ```
    /venv/Scripts/activate
    ```
    Unix
    ```
    source /venv/Scripts/activate
    ```
  - Create database
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
  - Create Admin User
    ```
    python manage.py createsuperuser
    ```
  - Runserver
    ```
    python manage.py runserver
    ```
## Running Tests
run the following command :
```
python manage.py test
```


# Exam Portal In Django

### To run this project follow the instructions given below:

### Please Note: Python 3.8.2 is needed to run this project

#### First we will need a .env file for storing email credentials
```
git clone https://github.com/rishank-shah/Exam-Portal.git
cd Exam-Portal
touch .env
```

#### Contents of .env file
```
export EMAIL_HOST_PASSWORD=<PASSWORD_OF_EMAIL_ACCOUNT>
export EMAIL_HOST_USER=<EMAIL_ACCOUNT>
export EMAIL_HOST=<SMTP>
export DEFAULT_FROM_EMAIL=<EMAIL_ACCOUNT>
```

#### Now if on linux run in cmd
```
source .env
```

#### If on Windows
##### Create a env.bat file with following contents and then run that bat file in cmd
```
set EMAIL_HOST_PASSWORD=<PASSWORD_OF_EMAIL_ACCOUNT>
set EMAIL_HOST_USER=<EMAIL_ACCOUNT>
set EMAIL_HOST=<SMTP>
set DEFAULT_FROM_EMAIL=<EMAIL_ACCOUNT>
```

#### After running env file commands as per os 
```
pip install pipenv
pipenv shell
pipenv install
cd Exam
python manage.py runserver
```
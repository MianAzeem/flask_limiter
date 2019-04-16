A simple flask application using flask-lmiter with the integration of flask-jwt-extended.

**Local Setup:**

- Clone repo into local machine:

  `git clone https://github.com/MianAzeem/flask_limiter.git`

- Create a virtual environement from shell:

  `python -m venv <venv_name>`
  
- Activate virtual env:

  `source /<venv_name>/bin activate`

- Insatll requirements: 

    `pip install -r requirements.txt`

- Install redis using:

  `brew install redis`

- After installing redis start service using:

  `brew services start redis`
  
- > To stop redis service: `brew services stop redis` 

- Create database using the following commands from shell:

  - `python manage.py db init`
  - `python manage.py db migrate`
  - `python manage.py db upgrade`
  
- Run app:
  
  `python limiter.py`
  

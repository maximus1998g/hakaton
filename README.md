# Project Hakaton HR Backend

Server part of the website by:
- Searching for vacancies, internships and internships for students, including from third-party services (SuperJob);
- Search for employees for companies;
- Automation of the work of university personnel;
- Telegram bot to notify students about new vacancies suitable for their specialization;
- Convenient and native system of skills and search for the necessary vacancies.

## Demo
Web client: http://findfound.me/

## Built with
- [Django](https://www.djangoproject.com/) - a free framework for web applications in Python
- [DRF](https://www.django-rest-framework.org/) - a library that works with standard Django models to create flexible and powerful API
- [SuperJob Api](https://api.superjob.ru/) - open source of the organization for the search and placement of vacancies
- [Telegram Bot Api](https://core.telegram.org/bots/api) - api from the Telegram messenger to create chat bots

## Installation
<i> For questions: [@infernowadays](https://t.me/infernowadays "@infernowadays") </i>
- Install postgres and configure in
- `backend/settings.py`
- Open a command line window and go to the project's directory.
- `sudo apt-get install build-essential libssl-dev libffi-dev python3-dev python-dev`
- `pip install -r requirements.txt`
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py runserver` or `python manage.py runserver 0.0.0.0:<your_port>`

## Todo
- [ ] Electronic document management system
- [X] Useful metrics
- [ ] Atomicity of existence
- [ ] Distribution to the largest universities in the Russian Federation
- [ ] Worldwide distribution
- [ ] Spread across the galaxy
- [X] And many more interesting things!

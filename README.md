# Django Channels

The Django simple chat application
<hr>

## How to use

```bash
git clone https://github.com/AmirMhKE/Django-Channels.git
cd Django-Channels
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
docker pull redis
docker run -p6379:6379 redis
python manage.py runserver
```
## Finish
Open tab http://localhost:8000/chat/ in browser

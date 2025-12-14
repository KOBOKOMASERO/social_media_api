# Deployment Documentation

## Project
social_media_api – Django REST API for a social media platform

## Hosting Platform
Render (or Railway)

## Production Configuration
- DEBUG=False
- PostgreSQL database
- Gunicorn WSGI server
- WhiteNoise for static files

## Environment Variables
| Variable | Description |
|--------|-------------|
| SECRET_KEY | Django secret key |
| DEBUG | False in production |
| ALLOWED_HOSTS | Render/Railway domain |
| DATABASE_URL | PostgreSQL connection string |
| SECURE_SSL_REDIRECT | Enable HTTPS |

## Deployment Steps
1. Push code to GitHub
2. Create Web Service on Render/Railway
3. Set environment variables
4. Build command:
   ```bash
   pip install -r requirements.txt
   python manage.py collectstatic --noinput
   python manage.py migrate

## Start command

```bash
gunicorn social_media_api.wsgi:application

```
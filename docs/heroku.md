heroku login
heroku create <your-app-name>
heroku stack:set container --app <your-app-name>
git push heroku <branch name>
heroku ps:scale web=1 --app <your-app-name>



<!-- config -->

heroku config:set DEBUG=True \
  DJANGO_ALLOWED_HOSTS="*" \
  DJANGO_SECRET_KEY="hdvdhfe5jfejfe8$hgffg" \
  DJANGO_SU_EMAIL="admin@gmail.com" \
  DJANGO_SU_NAME="admin" \
  DJANGO_SU_PASSWORD="Admin_pass" \
  EMAIL_HOST_PASSWORD="mbbp uwcc vvvj shcy" \
  EMAIL_HOST_USER="labanrotich6544@gmail.com" \
  POSTGRES_DB="potgressDb" \
  POSTGRES_USER="kibe" \
  POSTGRES_PASSWORD="Laban254@" \
  --app  webscrapifyy 


heroku run python manage.py migrate --app webscrapifyy
heroku open --app webscrapifyy

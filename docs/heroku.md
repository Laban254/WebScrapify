heroku login
heroku create <your-app-name>
heroku stack:set container --app <your-app-name>
git push heroku main
heroku ps:scale web=1 --app <your-app-name> 


heroku run python manage.py migrate --app webscrapifyy
heroku open --app webscrapifyy


<!-- check for postgrss addons -->
heroku addons:plans heroku-postgresql 

 heroku addons:create heroku-postgresql:essential-0 --app webscrapifyy
heroku addons --app webscrapifyy


heroku run python manage.py createsuperuser --app webscrapifyy

heroku run python manage.py collectstatic --noinput --app webscrapifyy


heroku restart --app webscrapifyy

heroku logs --tail --app webscrapifyy

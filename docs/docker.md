<!-- Rebuild and Restart Docker Compose: -->
sudo docker-compose down -v
sudo docker-compose build --no-cache
sudo docker-compose up --force-recreate


sudo docker-compose up --build


<!-- logs -->
docker-compose logs flower
docker-compose logs web
 

Django Application: Open your browser and navigate to http://localhost:8001.
Flower Monitoring Tool: Open your browser and navigate to http://localhost:5556.

<!-- postgress -->
sudo docker-compose exec db psql -U postgres -c "DROP DATABASE potgressDb;"
sudo docker-compose exec db psql -U postgres -c "CREATE DATABASE potgressDb;"

<!-- migrations -->
sudo docker-compose exec web python manage.py makemigrations webScrapify_app
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# praktikum_new_diplom

sudo docker-compose up -d --build
sudo docker-compose exec backend python manage.py makemigrations --noinput
sudo docker-compose exec backend python manage.py migrate --noinput
sudo docker-compose exec backend python manage.py collectstatic --noinput
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py import_ingredients
sudo docker-compose down -v
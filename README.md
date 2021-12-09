"# tcloud"

```python
> pip install -r requirements.txt
> python manage.py showmigrations
> python manage.py migrate --fake virtualization zero
> python manage.py showmigrations
> python manage.py makemigrations
> python manage.py migrate
```

Local

```python
echo "# tcloud" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/lorenzorivas/cmapp.git
git push -u origin main

engineering>git add .
engineering>git commit -m "Modelos Area, OT, Update"
engineering>git push -u origin master
```

Remoto

```python
project_repository/git pull
```

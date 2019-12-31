import os
import django
import random
import urllib3 
import json
## run this first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forum_backend_project.settings')
django.setup()
from django.contrib.auth.models import User
from category.models import Category
from post.models import Post

# create admin and user
def create_user():
    users = [
        {
            "username":"admin",
            "email":"admin@gmail.com",
            "password":"zzradmin"
        },
        {
            "username":"zeron",
            "email":"zeron@gmail.com",
            "password":"zeron123"
        }
    ]
    db_users = User.objects.all()
    for user in users:
        if user['username'] == 'admin':
            db_users_names = [ db_user.username for db_user in db_users]
            if user['username'] in db_users_names:
                user['username'] = user['username'] + str(random.randint(1,100))
            User.objects.create_superuser(username=user['username'], password=user['password'], email=user['email'])
            continue
        if user['username'] in db_users_names:
            user['username'] = user['username'] + str(random.randint(1,100))
            User.objects.create_user(username=user['username'], password=user['password'], email=user['email'])
        else:
            User.objects.create_user(username=user['username'], password=user['password'], email=user['email'])
    print('create users done ~!')

def create_category():
    categorys = [
        {
            "name":"democracy"
        },
        {
            "name":"technology"
        },
        {
            "name":"freedom"
        },
        {
            "name":"philosophy"
        }
    ]
    for item in categorys:
        category,created = Category.objects.get_or_create(name=item['name'])
        if created:
            print(f'{item["name"]} of category was existed')
    
    print('create_category done')

def create_post():
    http = urllib3.PoolManager()
    headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        'referer': 'http://jsonplaceholder.typicode.com/'
    }
    response = http.request('GET','http://jsonplaceholder.typicode.com/posts',headers=headers)
    items = json.loads(response.data.decode('utf-8'))
    author = User.objects.get(username='admin')
    categorys = Category.objects.all()
    mo = len(items) % len(categorys)
    exact_division = len(items) - mo
    per_c_posts = int(exact_division / len(categorys))
    print(mo,exact_division,per_c_posts)
    def cut_items(items,n):
        for i in range(0,len(items),n):
            yield items[i:i+n]
    def skip_categorys():
        for c in categorys:
            yield c
    def create_by_category(items_generator,category_generator):
        for per_items in items_generator:
            for category in category_generator:
                for item in per_items:
                    post,created = Post.objects.get_or_create(category=category,author=author,title=item['title'],body=item['body'])
                    print(f'{post} create success !~')
                break
    def mo_create_by_category(right,mo_categorys):
        if len(right) == len(mo_categorys):
            i = 0
            for item in right:
                post,created = Post.objects.get_or_create(category=mo_categorys[i],author=author,title=item['title'],body=item['body'])
                print(f' mo {post} create success !~')
                i += 1
            return None
        print ('Somethings get error')
    if mo != 0:
        left,right = items[:exact_division] , items[-mo:]
        per_c_items_generator = cut_items(left,per_c_posts)
        category_generator = skip_categorys()
        create_by_category(per_c_items_generator,category_generator)
        mo_categorys = categorys[:mo]
        mo_create_by_category(right,mo_categorys)
        print('create_post done')
    else:
        per_c_items_generator = cut_items(items,per_c_posts)
        category_generator = skip_categorys()
        create_by_category(per_c_items_generator,category_generator)
        print('create_post done')

def delete_all():
    User.objects.all().delete()
    print('User delete done')
    Category.objects.all().delete()
    print('Category delete done')
    Post.objects.all().delete()
    print('Post delete done')

if __name__ == "__main__":
    delete_all()
    create_user()
    create_category()
    create_post()
## Flask API

We are going to create a basic api that performs all crud routes using Flask

- Create a new directory `mkdir flask-api`. 
- Now run `cd flask-api`.
- Run command `touch app.py models.py requirements.txt`

#### Setup virtualenv

- inside flask-api folder

```bash
virtualenv .env -p python3
source .env/bin/activate
```

#### Dependencies

```
pip3 install flask flask_cors flask-marshmallow flask-sqlalchemy marshmallow-sqlalchemy
pip3 freeze > requirements.txt
```


### Setup basic server 


```python
import os

from flask import Flask

app = Flask(__name__)

DEBUG = True
PORT = 8000

@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)
```

>8000 is the port number that your app will run on

Test everything bu running `python3 app.py` on terminal and then execute this [link](http://localhost:8000). You should get 'Hello World' in reponse.

Now initialize the databse object using SqlAlchemy:

### Database setup using SqlAlchemy

SqlAlchemy is an ORM used in Flask to connect and communicate with the database.

#### app.py

```python
import os

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

# Set Base Directory
basedir = os.path.abspath(os.path.dirname(__file__))

# SQLite Database
DATABASE = 'sqlite:///' + os.path.join(
    basedir, 'db.reddit')

# Local Postgres Database
# DATABASE = PostgresqlDatabase(
#     'reddit',
#     user='dalton',
#     password=''
# )

# Setup Database
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init Database
db = SQLAlchemy(app)

#Init Marshmallow
marshmallow = Marshmallow(app)

DEBUG = True
PORT = 8000


@app.route('/')
def hello_world():
    return 'Hello World'


if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)

```
> db.reddit is the db name.

Run your app using `python3 app.py` again to confirm that there are no errors. 

### Sub

Let's create our first model for our app in `models.py`.

#### models.py

```python
from app import db, marshmallow

class Sub(db.Model):
	 __table_args__ = {'extend_existing': True} 
	 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(300))

    def __init__(self, name, description):
        self.name = name
        self.description = description
        

if __name__ == 'models':
    db.create_all()
```
> When True, indicates that if this Table is already present in the given MetaData, apply further arguments within the constructor to the existing Table.

### Schema setup using Marshmallow

You can use this library to dictate what fields will be sent back to the user in response.

Using Marshmallow let's add sub schema in `models.py`.

```python
class SubSchema(marshmallow.Schema):
  class Meta:
    fields = ('id', 'name', 'description')

sub_schema = SubSchema(strict=True)
subs_schema = SubSchema(many=True, strict=True)
```

Now let's add create and get methods for Sub model in `models.py`

```python
class Sub(db.Model):
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(300))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    @classmethod
    def create_sub(cls, name, description):
        new_sub = Sub(name, description)
        try:
            db.session.add(new_sub)
            db.session.commit()
        except:
            db.session.rollback()
            raise Exception('Session rollback')
        return sub_schema.jsonify(new_sub)

    @classmethod
    def get_sub(cls, subid):
        sub = Sub.query.get(subid)
        return sub_schema.jsonify(sub)
        
class SubSchema(marshmallow.Schema):
  class Meta:
    fields = ('id', 'name', 'description')

sub_schema = SubSchema(strict=True)
subs_schema = SubSchema(many=True, strict=True)
```

Now, add routes for your Sub model in `app.py`.

```python
@app.route('/sub', methods=['POST'])
@app.route('/sub/<subid>', methods=['GET'])
def create_sub(subid=None):
    from models import Sub
    if subid == None:
        name = request.json['name']
        description = request.json['description']

        return Sub.create_sub(name, description)
    else:
        return Sub.get_sub(subid)
```

Use Postman to test both routes.

### Post

Let's create a Post model such that each post has a reference to one Sub.

```python
class Post(db.Model):
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime())
    user = db.Column(db.String(100))
    title = db.Column(db.String(200))
    text = db.Column(db.String(500))
    sub = db.Column(db.Integer, db.ForeignKey("sub.id"))

    def __init__(self, user, title, text, sub):
        self.user = user
        self.title = title
        self.text = text
        self.sub = sub

    @classmethod
    def create_post(cls, user, title, text, sub):
        new_post = Post(user, title, text, sub)
        try:
            db.session.add(new_post)
            db.session.commit()
        except:
            db.session.rollback()
            raise

        return post_schema.jsonify(new_post)

    @classmethod
    def get_post(cls,post_id):
        post = Post.query.get(post_id)
        return post_schema.jsonify(post)
``` 

```python
class PostSchema(marshmallow.Schema):
  class Meta:
    fields = ('id', 'user', 'title', 'text', 'sub')

# Init Schema
post_schema = PostSchema(strict=True)
posts_schema = PostSchema(many=True, strict=True)
```

```python
@app.route('/post', methods=['POST'])
@app.route('/post/<postid>', methods=['GET'])
def get_create_post(postid=None):
    from models import Post
    if postid == None:
        user = request.json['user']
        title = request.json['title']
        text = request.json['text']
        sub = request.json['sub']

        return Post.create_post(user, title, text, sub)
    else:
        return Post.get_post(postid)
```

## You Do: Comments on Posts

Here are some guidelines to follow as you build out routes for Comments for this project:

- Define a Comment model and connect it to the Post model
- Create a post and get methods in the model
- Create the schema for Comment
- Add routes in `app.py` to either get or post comments

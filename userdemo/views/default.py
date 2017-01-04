from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from pyramid.httpexceptions import HTTPFound
from ..models import Post
from ..security import check_credentials
from pyramid.security import NO_PERMISSION_REQUIRED
from userdemo.security import check_credentials


@view_config(route_name='login', renderer='../templates/login.jinja2', permission=NO_PERMISSION_REQUIRED)
def login(request):
    if request.method == 'POST':
        username = request.params.get('username', '')
        password = request.params.get('password', '')
        if check_credentials(username, password):
            headers = remember(request, username)
            return HTTPFound(location=request.route_url('home'), headers=headers)
    return {}



@view_config(route_name='home', renderer='../templates/home.jinja2')
def home(request):
    return "home"

@view_config(route_name="profile", renderer="../templates/profile.jinja2", permission='secret')
def detail_view(request):
    username = request.matchdict["username"]
    user = request.dbsession.query(User).get(username)
    return {"user": user}

# @view_config(route_name="edit", renderer="../templates/edit-post.jinja2")
# def edit_view(request):
#     post_id = int(request.matchdict["id"])
#     post = request.dbsession.query(Post).get(post_id)
#     return {"post": post}


@view_config(route_name='register', renderer="../templates/register.jinja2", permission='secret')
def register(request):
    if request.method == "POST":
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        username = request.POST["username"]
        email = request.POST["email"]
        favfood = request.POST["food"]
        password = request.POST["password"]
        new_user = User(firstname=firstname, lastname=lastname, username=username, email=email, favfood=favfood, password=password)
        request.dbsession.add(new_user)
        return HTTPFound(request.route_url('profile'))
    return {}


@view_config(route_name='logout', renderer="../templates/logout.jinja2", permission='secret')
def logout(request):
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_lj_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

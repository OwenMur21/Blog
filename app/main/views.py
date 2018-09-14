from flask import render_template,request,redirect,url_for,abort
from . import main
from flask_login import login_required, current_user
from .. import db,photos
from ..models import User, Blog, Comments
from .forms import PitchForm, CommentForm, UpdateProfile


@main.route('/')
def index():
    """
    View blogs 
    """
    blogs = Blog.query.all()
    if blogs is None:
        abort(404)
    return render_template('index.html', blogs=blogs)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/blog/new-blog/', methods=['GET', 'POST'])
@login_required
def new_blog():
    """
    Function that enables one to start a blog
    """
    form = PitchForm()
 
    if form.validate_on_submit():
        content = form.content.data
        new_blog = Blog(content = content,user_id = current_user.id)
        new_blog.save_blog()
        return redirect(url_for('main.index'))
    return render_template('new-blog.html',form=form)

@main.route('/view-blog/<int:id>', methods=['GET', 'POST'])
@login_required
def view_blog(id):
    """
    Returns the blog to be commented on
    """
    print(id)
    blogs = Blog.query.get(id)
    comments = Comments.get_comments(id)
    return render_template('view.html', blogs=blogs, comments=comments, id=id)

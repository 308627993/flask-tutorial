import datetime
from os import path
from sqlalchemy import func,text
from flask import render_template,Blueprint,redirect,url_for,abort
from webapp.config import db
from .models import Post,Tag,Comment,tags
from webapp.auth.models import User
from .forms import CommentForm,PostForm
from flask_login import login_required,current_user
from webapp.auth.extensions import poster_permission,admin_permission
from flask_principal import Permission,UserNeed

blog_blueprint = Blueprint(
    'blog',
    __name__,
    template_folder = './templates/blog',
    url_prefix = '/blog'
    )

def sidebar_data():
    recent = Post.query.order_by(Post.publish_date.desc()).limit(5).all()
    top_tags = db.session.query(Tag,func.count(tags.c.post_id).label('total')).join(tags).group_by(Tag).order_by(text('total DESC')).limit(5).all()
    return recent,top_tags

@blog_blueprint.route('/<int:page>')
def home(page=1):
    posts = Post.query.order_by(Post.publish_date.desc()).paginate(page,7)
    recent,top_tags = sidebar_data()
    return render_template(
        'home.html',
        posts=posts,
        recent=recent,
        top_tags=top_tags)

@blog_blueprint.route('/post/<int:post_id>',methods=('GET','POST'))
def post(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment()
        new_comment.name = form.name.data
        new_comment.text = form.text.data
        new_comment.post_id = post_id
        new_comment.date = datetime.datetime.now()
        db.session.add(new_comment)
        db.session.commit()
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    comments = post.comments.order_by(Comment.date.desc()).all()
    recent,top_tags = sidebar_data()
    return render_template(
        'post.html',
        post=post,
        tags=tags,
        comments=comments,
        recent=recent,
        top_tags=top_tags,
        form = form
        )

@blog_blueprint.route('/tag/<string:tag_name>')
def tag(tag_name):
    tag = Tag.query.filter_by(title=tag_name).first_or_404()
    posts = tag.posts.order_by(Post.publish_date.desc()).all()[:10]
    recent,top_tags = sidebar_data()
    return render_template(
        'tag.html',
        tag=tag,
        posts=posts,
        recent=recent,
        top_tags=top_tags
        )

@blog_blueprint.route('/user/<string:username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.publish_date.desc().all())
    recent,top_tags = sidebar_data()
    return render_template(
        'user.html',
        user=user,
        posts=posts,
        recent=recent,
        top_tags=top_tags
        )

@blog_blueprint.route('/new/',methods = ['POST','GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(form.title.data)
        new_post.text = form.text.data
        new_post.publish_date = datetime.datetime.now()
        new_post.user = current_user
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('.post',post_id = new_post.id))
    return render_template('new.html',form = form)

@blog_blueprint.route('/edit/<int:id>',methods = ['POST','GET'])
@login_required
@poster_permission.require(http_exception=403)
def edit_post(id):
    post = Post.query.get_or_404(id)
    permission = Permission(UserNeed(post.user_id))
    if permission.can() or admin_permission.can():
        form = PostForm()
        if form.validate_on_submit():
            '''
            new_post = Post(form.title.data)
            new_post.text = form.text.data
            new_post.publish_date = datetime.datetime.now()
            '''
            post.title = form.title.data
            post.text = form.text.data
            post.publish_date = datetime.datetime.now()
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('.post',post_id = post.id))
        form.text.data = post.text
        form.title.data = post.title
        return render_template('edit.html',form = form,post = post)
    abort(403)

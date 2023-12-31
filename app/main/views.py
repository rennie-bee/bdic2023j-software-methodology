import os
from datetime import datetime
from operator import or_
from flask import render_template, redirect, url_for, flash, request, \
    current_app, make_response
from flask_login import login_required, current_user
from sqlalchemy.sql.functions import func
from werkzeug.utils import secure_filename
from . import main
from .forms import UploadPhotoForm, CommentForm, PostMdForm
from .. import db
from ..models import Permission, User, Post, Comment, Notification, Like, Activity, Recruitment, Rank, Certification
from ..decorators import permission_required


# 首页基本信息展示
@main.route('/', methods=['GET', 'POST'])
def index():
    # GET method
    if request.method == 'GET':
        page1 = request.args.get('page', 1, type=int)
        query1 = Post.query
        # main page activity rank
        for item in query1:
            item.important = 0
            com_num = Comment.query.filter_by(post_id=item.id).count()
            li_num = Like.query.filter_by(liked_post_id=item.id).count()
            item.important = 7 * com_num + 3 * li_num
        hot = query1.order_by(Post.important.desc())
        li = Activity.query.filter_by(is_invalid=False)
        hot_activity = li.order_by(Activity.important.desc())

        if current_user.is_authenticated:
            if current_user.role_id == 3:
                # 主页的问题（帖子）根据最近被举报次数进行排序和分页
                pagination1 = query1.order_by(Post.report_time.desc()).paginate(
                    page1, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                    error_out=False)
                posts1 = pagination1.items
                return render_template('index.html', posts1=posts1, posts5=hot,
                                       pagination1=pagination1, panel_id=1)
            elif current_user.role_id == 1:
                pagination1 = query1.order_by(Post.recent_activity.desc()).paginate(
                    page1, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                    error_out=False)
                posts1 = pagination1.items
                return render_template('index.html', posts1=posts1, posts5=hot,
                                       pagination1=pagination1, hot_activity=hot_activity, panel_id=1)
            elif current_user.role_id == 2:
                pagination1 = query1.order_by(Post.recent_activity.desc()).paginate(
                    page1, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                    error_out=False)
                posts1 = pagination1.items
                return render_template('index.html', posts1=posts1, posts5=hot,
                                       pagination1=pagination1, hot_activity=hot_activity, panel_id=1)
        else:
            # 主页的问题（帖子）根据最近最近活跃度进行排序和分页 （最近活跃度指的是最近被访问，点赞和评论的帖子（问题））
            pagination1 = query1.order_by(Post.recent_activity.desc()).paginate(
                page1, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                error_out=False)
            posts1 = pagination1.items
            return render_template('index.html', posts1=posts1, posts5=hot,
                                   pagination1=pagination1, hot_activity=hot_activity, panel_id=1)

        # # 主页的问题（帖子）根据最近最近活跃度进行排序和分页 （最近活跃度指的是最近被访问，点赞和评论的帖子（问题））
        # pagination1 = query1.order_by(Post.recent_activity.desc()).paginate(
        #     page1, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        #     error_out=False)
        # posts1 = pagination1.items
        # return render_template('index.html', posts1=posts1, posts5=hot,
        #                        pagination1=pagination1, hot_activity=hot_activity, panel_id=1)
    # ’POST‘方法执行查询功能
    else:
        inf = request.form["search"]
        return redirect(url_for('.query', content=inf))


# 首页招募展示
@main.route('/recruitment/', methods=['GET', 'POST'])
def index_recruitment():
    if request.method == 'GET':
        recruitments = Recruitment.query.order_by(Recruitment.timestamp.desc())
        # hot
        query1 = Post.query
        for item in query1:
            item.important = 0
            com_num = Comment.query.filter_by(post_id=item.id).count()
            li_num = Like.query.filter_by(liked_post_id=item.id).count()
            item.important = 7 * com_num + 3 * li_num
        hot = query1.order_by(Post.important.desc())
        li = Activity.query.filter_by(is_invalid=False)
        hot_activity = li.order_by(Activity.important.desc())
        return render_template('index.html', posts5=hot,
                               hot_activity=hot_activity, recruitments=recruitments, panel_id=2)
    else:
        inf = request.form["search"]
        return redirect(url_for('.query', content=inf))

# 审查教授证明文件
@main.route('/cert/', methods=['GET', 'POST'])
def index_certification():
    if request.method == 'GET':
        # hot
        query1 = Post.query
        for item in query1:
            item.important = 0
            com_num = Comment.query.filter_by(post_id=item.id).count()
            li_num = Like.query.filter_by(liked_post_id=item.id).count()
            item.important = 7 * com_num + 3 * li_num
        hot = query1.order_by(Post.important.desc())
        query4 = current_user.unreviewed_certification
        certs4 = query4.order_by(Certification.timestamp)
        return render_template('index.html', certs4=certs4, posts6=hot, panel_id=2)
    else:
        inf = request.form["search"]
        return redirect(url_for('.query', content=inf))


# 首页排行榜展示
@main.route('/rank/', methods=['GET', 'POST'])
def index_rank():
    if request.method == 'GET':
        # hot
        query1 = Post.query
        for item in query1:
            item.important = 0
            com_num = Comment.query.filter_by(post_id=item.id).count()
            li_num = Like.query.filter_by(liked_post_id=item.id).count()
            item.important = 7 * com_num + 3 * li_num
        hot = query1.order_by(Post.important.desc())
        query1 = Rank.query
        ranks = query1.order_by(Rank.id)
        if current_user.is_authenticated:
            if current_user.role_id == 3:
                return render_template('index.html', ranks=ranks, posts6=hot, panel_id=3)
            elif current_user.role_id == 1 or current_user.role_id == 2:
                return render_template('index.html', ranks=ranks, posts5=hot, panel_id=3)
        else:
            return render_template('index.html', ranks=ranks, posts5=hot, panel_id=3)
    if request.method == 'POST':
        univ = Rank.query.filter_by(id=request.form["id"]).count()
        file = "../../static/rank/" + request.files["picture"].filename
        get_file = request.files["picture"]
        filename = secure_filename(get_file.filename)
        get_file.save(os.path.join('app', 'static', 'rank', filename))
        if univ == 0:
            university = Rank(id=request.form["id"], name=request.form["name"], country=request.form["country"], website=request.form["website"], picture_path=file)
            db.session.add(university)
            db.session.commit()
            flash("Add successfully")
        else:
            flash("Exist same rank university")
        return redirect(url_for('.index_rank'))


# 首页关注用户的帖子（问题）展示
@main.route('/foll/', methods=['GET', 'POST'])
def index_follow():
    if request.method == 'GET':
        # hot
        query1 = Post.query
        for item in query1:
            item.important = 0
            com_num = Comment.query.filter_by(post_id=item.id).count()
            li_num = Like.query.filter_by(liked_post_id=item.id).count()
            item.important = 7 * com_num + 3 * li_num
        hot = query1.order_by(Post.important.desc())
        query4 = current_user.followed_posts
        posts4 = query4.order_by(Post.recent_activity.desc())
        li = Activity.query.filter_by(is_invalid=False)

        hot_activity = li.order_by(Activity.important.desc())
        return render_template('index.html', posts4=posts4, posts5=hot, hot_activity=hot_activity, panel_id=4)
    else:
        inf = request.form["search"]
        return redirect(url_for('.query', content=inf))


@main.route('/favorites/', methods=['GET', 'POST'])
def index_favorites():
    if request.method == 'GET':
        # hot
        query1 = Post.query
        for item in query1:
            item.important = 0
            com_num = Comment.query.filter_by(post_id=item.id).count()
            li_num = Like.query.filter_by(liked_post_id=item.id).count()
            item.important = 7 * com_num + 3 * li_num
        hot = query1.order_by(Post.important.desc())
        li = Activity.query.filter_by(is_invalid=False)

        hot_activity = li.order_by(Activity.important.desc())
        return render_template('index.html',
                               favorites=[_favorite.favorite_post for _favorite in current_user.favorite_post],
                               posts5=hot, hot_activity=hot_activity, panel_id=5)
    else:
        inf = request.form["search"]
        return redirect(url_for('.query', content=inf))


# 查询功能（默认查询帖子（问题）），以及四种不同的排序方式
@main.route('/query/<content>', methods=['GET', 'POST'])
def query(content):
    if request.method == 'GET':
        print("get")
        inf = content
        search_result = "%" + inf + "%"
        result = Post.query.filter(or_(Post.title.like(search_result), Post.body.like(search_result)))
        for item in result:
            item.important = 0
            sentence = item.title + item.body
            counts = 0
            list1 = sentence.split(" ")
            for y in range(len(list1)):
                if list1[y].find(inf) != -1:
                    counts = counts + 1
            item.important = counts
            print(item.important)
        page = request.args.get('page', 1, type=int)
        pagination1 = result.order_by(Post.important.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        relevance = pagination1.items
        pagination2 = result.order_by(Post.timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        newest = pagination2.items
        for item in result:
            item.important = 0
            com_num = Comment.query.filter_by(post_id=item.id).count()
            item.important = com_num
        pagination3 = result.order_by(Post.important.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        hottest = pagination3.items
        for item in result:
            item.important = 0
            sentence = item.title + item.body
            counts = 0
            list1 = sentence.split(" ")
            for y in range(len(list1)):
                if list1[y].find(inf) != -1:
                    counts = counts + 1
            com_num = Comment.query.filter_by(post_id=item.id).count()
            li_num = Like.query.filter_by(liked_post_id=item.id).count()
            item.important = counts * 4 + 3 * com_num + 3 * li_num
        pagination4 = result.order_by(Post.important.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        combination = pagination4.items
        # print(show_newest + show_relevance + show_hottest)
        for item in result:
            item.important = 0
        return render_template('querypost.html', relevance=relevance, newest=newest, hottest=hottest,
                               combination=combination, title="Result of query", inf=inf, pagination1=pagination1,
                               pagination2=pagination2, pagination3=pagination3, pagination4=pagination4)
    if request.method == 'POST':
        inf = request.form["inf"]
        if inf == "":
            flash("Search content cannot be empty.")
            return render_template('querypost.html')
        search_result = "%" + inf + "%"
        result = Post.query.filter(or_(Post.title.like(search_result), Post.body.like(search_result)))
        for item in result:
            item.important = 0
            sentence = item.title + item.body
            counts = 0
            list1 = sentence.split(" ")
            for y in range(len(list1)):
                if list1[y].find(inf) != -1:
                    counts = counts + 1
                # print(list1[y])
            item.important = counts
            print(inf)
        page = request.args.get('page', 1, type=int)
        pagination1 = result.order_by(Post.important.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        relevance = pagination1.items
        pagination2 = result.order_by(Post.timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        newest = pagination2.items
        for item in result:
            item.important = 0
            com_num = Comment.query.filter_by(post_id=item.id).count()
            item.important = com_num
        pagination3 = result.order_by(Post.important.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        hottest = pagination3.items
        for item in result:
            item.important = 0
            sentence = item.title + item.body
            counts = 0
            list1 = sentence.split(" ")
            for y in range(len(list1)):
                if list1[y].find(inf) != -1:
                    counts = counts + 1
            com_num = Comment.query.filter_by(post_id=item.id).count()
            li_num = Like.query.filter_by(liked_post_id=item.id).count()
            item.important = counts * 4 + 3 * com_num + 3 * li_num
        pagination4 = result.order_by(Post.important.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        combination = pagination4.items
        # print(show_newest + show_relevance + show_hottest)
        for item in result:
            item.important = 0
        return render_template('querypost.html', relevance=relevance, newest=newest, hottest=hottest,
                               combination=combination, title="Result of query", inf=inf, pagination1=pagination1,
                               pagination2=pagination2, pagination3=pagination3, pagination4=pagination4)


# 查询其他用户的功能（根据用户名和学号）
@main.route('/query-user', methods=['GET', 'POST'])
def query_user():
    if request.method == 'GET':
        return render_template('queryuser.html')
    if request.method == 'POST':
        inf = request.form["user"]
        if inf == "":
            flash("Search content cannot be empty.")
            return render_template('queryuser.html')
        search_result = "%" + inf + "%"
        result = User.query.filter(or_(User.username.like(search_result), User.college_id.like(search_result)))
        page = request.args.get('page', 1, type=int)
        pagination = result.order_by(User.username.desc()).paginate(
            page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
            error_out=False)
        query = pagination.items
        return render_template('queryuser.html', query=query, title="Result of query", pagination=pagination, inf=inf)


# 查询二手交易的功能
@main.route('/query-recruitment', methods=['GET', 'POST'])
def query_recruitment():
    if request.method == 'GET':
        return render_template('queryrecruitment.html')
    if request.method == 'POST':
        inf = request.form["transaction"]
        if inf == "":
            flash("Search content cannot be empty.")
            return render_template('queryrecruitment.html')
        search_result = "%" + inf + "%"
        result = Recruitment.query.filter(or_(Recruitment.title.like(search_result),
                                              Recruitment.description.like(search_result)))
        page = request.args.get('page', 1, type=int)
        pagination = result.order_by(Recruitment.timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
            error_out=False)
        query = pagination.items
        return render_template('queryrecruitment.html', query=query, title="Result of query", pagination=pagination,
                               inf=inf)


# 访问用户主页的功能
@main.route('/user/<username>', methods=['GET', 'POST'])
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    liking = Like.query.filter_by(liker_id=user.id)
    posts = user.posts.order_by(Post.timestamp.desc())
    liking_posts = [{'post': item.liked_post, 'timestamp': item.timestamp} for item in liking.order_by(Like.timestamp.
        desc())]
    if user.role_id == 2:
        recruitments = user.recruitments.order_by(Recruitment.timestamp.desc())
    else:
        recruitments = None
    if request.method == 'GET':
        return render_template('user.html', user=user, posts=posts, liking_posts=liking_posts, recruitments=recruitments)
    if request.method == 'POST':
        message_info = request.form["message_info"]
        if message_info == "":
            flash("Message can not be null")
        else:
            n = Notification(receiver_id=user.id, timestamp=datetime.utcnow(),
                             username=current_user.username, action="has sent a private message to you",
                             object=message_info)
            db.session.add(n)
            db.session.commit()
            flash("You have sent a private message to " + user.username)
    return render_template('user.html', user=user, posts=posts, liking_posts=liking_posts, recruitments=recruitments)


# 显示消息提醒的功能
@main.route('/notification')
def notification():
    page = request.args.get('page', 1, type=int)
    pagination = current_user.notifications.order_by(Notification.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    notices = pagination.items
    return render_template('table/notifications.html', notices=notices,
                           pagination=pagination)


# 改变消息状态（通过点击消息的抬头来实现），已读的消息将不会显示在消息列表
@main.route('/change_read/<int:id>')
def change_read(id):
    notice = Notification.query.filter_by(id=id).first()
    notice.is_read = True
    db.session.add(notice)
    db.session.commit()
    flash("You have read one notification")
    return redirect(url_for('.notification'))


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allow_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 上传头像的功能，上传的头像会被默认保存在本地的 static/assets/位置
@main.route('/photo', methods=['POST'])
def uploadPhoto():
    form = UploadPhotoForm()
    f = form.photo.data
    if f and allow_file(f.filename):
        filename = secure_filename(f.filename)
        f.save(os.path.join('app', 'static', 'assets', filename))
        current_user.avatar_img = '/static/assets/' + filename
        db.session.commit()
    else:
        flash("Please upload a picture of the compound rule")
    return redirect(url_for('.edit_profile'))


# 编辑用户个人主页的功能
@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = UploadPhotoForm()
    if request.method == 'GET':
        return render_template('edit_profile.html', form=form)
    if request.method == 'POST':
        # 读取前端数据
        username_find = User.query.filter_by(username=request.form["username"]).first()
        if username_find is not None and username_find != current_user:
            flash("Your new username already exists, please change your username")
            return render_template('edit_profile.html', form=form)

        current_user.username = request.form["username"]
        current_user.college = request.form["collage"]
        current_user.about_me = request.form["aboutme"]
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))


# 显示某个帖子（问题）的相关信息的功能
@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    user_list = User.query.order_by(User.username)
    form = CommentForm()
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count('*') - 1) // \
               current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = Comment.query.with_parent(post).order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    """发表评论与回复"""
    if form.validate_on_submit():
        body = form.body.data
        if request.form.get('anonymous') == "on":
            is_anonymous = True
            username = "Anonymous"
        else:
            is_anonymous = False
            username = current_user.username
        comment = Comment(body=body,
                          post=post,
                          author=current_user._get_current_object(),
                          replied_id=request.args.get('reply'),
                          is_anonymous=is_anonymous)
        comment.post.recent_activity = datetime.utcnow()
        if comment.replied_id:
            replied = Comment.query.get_or_404(comment.replied_id)
            comment.replied = replied
            action1 = " has replied<" + comment.body + "> to your comment<" + comment.replied.body + "> in the posting "
            n1 = Notification(receiver_id=comment.replied.author_id, timestamp=datetime.utcnow(),
                              username=username, action=action1,
                              object=post.title, object_id=post.id)
            db.session.add(n1)
            db.session.commit()
            action2 = " has commented<" + comment.body + "> on your posting"
            n2 = Notification(receiver_id=post.author_id, timestamp=datetime.utcnow(),
                              username=username, action=action2,
                              object=post.title, object_id=post.id)
            db.session.add(n2)
            db.session.commit()
        else:
            action = " has commented<" + comment.body + "> on your posting"
            """传入通知信息"""
            n = Notification(receiver_id=post.author_id, timestamp=datetime.utcnow(),
                             username=username, action=action,
                             object=post.title, object_id=post.id)
            db.session.add(n)
            db.session.commit()
        db.session.add(comment)
        db.session.commit()
        if comment.is_anonymous:
            flash('Comment published anonymously')
        else:
            flash('Comment published successfully')
        return redirect(url_for('.post', id=post.id))
    return render_template('post.html', posts=[post], form=form, comments=comments,
                           pagination=pagination, user_list=user_list)


# 对评论（问题）的回复功能，即多级评论
@main.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    """作为中转函数通过URL传递被回复评论信息"""
    comment = Comment.query.get_or_404(comment_id)
    post1 = comment.post
    author = comment.author.username
    # 更细帖子（问题）的最近活跃度
    post1.recent_activity = datetime.utcnow()
    if comment.is_anonymous:
        author = "anonymous"
    db.session.commit()
    return redirect(url_for('.post', id=comment.post.id, reply=comment_id, author=author))


# 删除评论的功能
@main.route('/delete_comment/<int:id>')
@login_required
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    posts = Post.query.filter_by(id=comment.post_id).first()
    users = User.query.filter_by(id=posts.author_id).first()
    if current_user == comment.author or current_user == users:
        db.session.delete(comment)
        db.session.commit()
        flash('The comment has been deleted.')
        return redirect(url_for('.post', id=posts.id))
    else:
        flash('你没有删评论权限')
        return redirect(url_for('.post', id=posts.id))


# 删除帖子（问题）的功能（在个人主页删除）
@main.route('/delete_post_profile/<post_id>')
@login_required
def delete_post_inProfile(post_id):
    post = Post.query.filter_by(id=post_id).first()
    db.session.delete(post)
    db.session.commit()
    flash('The posting has been deleted.')
    return redirect(url_for('.user', username=current_user.username))


# 关注其他用户的功能
@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are now following %s.' % username)
    return redirect(url_for('.user', username=username))


# 取消关注其他用户的功能
@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('.user', username=username))


# 对帖子（问题）的点赞功能
@main.route('/like/<post_id>')
@login_required
@permission_required(Permission.FOLLOW)
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        flash('Invalid post.')
        return redirect(url_for('.index'))
    if current_user.is_liking(post):
        flash('You are already liking this post.')
        return redirect(url_for('.post', id=post_id))
    current_user.like(post)
    post.like(current_user)
    post.recent_activity = datetime.utcnow()
    db.session.commit()
    flash('You are now liking this post')
    return redirect(url_for('.index', id=post_id))


@main.route('/likeinpost/<post_id>')
@login_required
@permission_required(Permission.FOLLOW)
def like_inpost(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        flash('Invalid post.')
        return redirect(url_for('.index'))
    if current_user.is_liking(post):
        flash('You are already liking this post.')
        return redirect(url_for('.post', id=post_id))
    current_user.like(post)
    post.like(current_user)
    post.recent_activity = datetime.utcnow()
    db.session.commit()
    flash('You are now liking this post')
    return redirect(url_for('.post', id=post_id))


# 取消对帖子（问题）点赞的功能
@main.route('/dislike/<post_id>')
@login_required
@permission_required(Permission.FOLLOW)
def dislike(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        flash('Invalid post.')
        return redirect(url_for('.index'))
    if not current_user.is_liking(post):
        flash('You are not liking this post.')
        return redirect(url_for('.post', id=post_id))
    current_user.dislike(post)
    post.dislike(current_user)
    db.session.commit()
    flash('You are not liking this post')
    return redirect(url_for('.index', id=post_id))


@main.route('/dislikeinpost/<post_id>')
@login_required
@permission_required(Permission.FOLLOW)
def dislike_inpost(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        flash('Invalid post.')
        return redirect(url_for('.index'))
    if not current_user.is_liking(post):
        flash('You are not liking this post.')
        return redirect(url_for('.post', id=post_id))
    current_user.dislike(post)
    post.dislike(current_user)
    db.session.commit()
    flash('You are not liking this post')
    return redirect(url_for('.post', id=post_id))


# 显示所有followers的人
@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('table/followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


# 显示所有followed的人
@main.route('/followed_by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.following.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('table/followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)


# 显示所有喜欢这个post的人
@main.route('/liked_by/<post_id>')
def liked_by(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        flash('Invalid post.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = post.liker.paginate(
        page, per_page=current_app.config['FLASKY_LIKER_PER_PAGE'],
        error_out=False)
    liker = [{'user': item.liker, 'timestamp': item.timestamp}
             for item in pagination.items]
    return render_template('table/liker.html', post=post, title="The liker of",
                           endpoint='.liked_by', pagination=pagination,
                           liker=liker)


# 发布一条新的帖子（问题）
@main.route('/new_post_md', methods=['GET', 'POST'])
@login_required
def new_post_md():
    form = PostMdForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        title = request.form.get('title')
        body = form.body.data
        if request.form.get('anonymous') == "on":
            is_anonymous = True
        else:
            is_anonymous = False
        if title == "":
            flash("Title cannot be None!")
            return render_template('new_posting/new_mdpost.html', form=form)
        body_html = request.form['test-editormd-html-code']
        post = Post(title=title,
                    body=body,
                    body_html=body_html,
                    is_anonymous=is_anonymous,
                    author=current_user._get_current_object())
        post.recent_activity = datetime.utcnow()
        db.session.add(post)
        db.session.commit()
        if post.is_anonymous:
            flash("You have just posted a posting anonymously", 'success')
        else:
            flash("You have just posted a posting", 'success')
        return redirect(url_for('.index'))
    return render_template('new_posting/new_mdpost.html', form=form)


# 转发其他用户帖子的功能
@main.route('/share_post/<post_id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.FOLLOW)
def share_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if request.method == 'GET':
        return render_template('new_posting/share.html', post=post)
    else:
        title = request.form["new_title"]
        auth = User.query.filter_by(id=post.author_id).first_or_404()
        if title == "":
            flash("Title cannot be None!")
            return render_template('new_posting/share.html', post=post)
        new_post = Post(title=title,
                        body=post.body,
                        body_html=post.body_html,
                        is_anonymous=False,
                        is_shared=True,
                        shared_from=auth.username,
                        shared_content=post.title,
                        origin_post_id=post_id,
                        author=current_user._get_current_object())
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for(".index"))


@main.route('/favorite/<post_id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.FOLLOW)
def favorite(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        flash('Invalid post.')
        return redirect(url_for('.index'))
    if current_user.is_favorite(post):
        flash('You are already save this post as favorite.')
        return redirect(url_for('.post', id=post_id))
    current_user.favorite(post)
    post.favorite(current_user)
    post.recent_activity = datetime.utcnow()
    db.session.commit()
    flash('You are now save this post as favorite')
    return redirect(url_for('.index', id=post_id))


@main.route('/dis_favorite/<post_id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.FOLLOW)
def dis_favorite(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        flash('Invalid post.')
        return redirect(url_for('.index'))
    if not current_user.is_favorite(post):
        flash('You are have not save this post as favorite.')
        return redirect(url_for('.post', id=post_id))
    current_user.dis_favorite(post)
    post.dis_favorite(current_user)
    db.session.commit()
    flash('You remove this post from favorte')
    return redirect(url_for('.index', id=post_id))


# 邀请其他用户回答某个问题的功能
@main.route('/invite/<post_id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.FOLLOW)
def invite(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    user_list = User.query.order_by(User.username)
    if request.method == 'GET':
        return render_template('post_invite.html', user_list=user_list, posts=[post])
    if request.method == 'POST':
        info = request.form["invite"]
        user = User.query.filter_by(id=info).first_or_404()
        n = Notification(receiver_id=user.id, timestamp=datetime.utcnow(),
                         username=current_user.username, action="invites you to answer the question",
                         object=post.title, object_id=post.id)
        db.session.add(n)
        db.session.commit()
        flash("You have invited <" + user.username + "> to answer this question.")
        return redirect(url_for('main.post', id=post.id))
    return render_template('post_invite.html', user_list=user_list, posts=[post])


# 删除帖子（问题）的功能（在首页删除）
@main.route('/delete/<post_id>')
@login_required
def delete(post_id):
    post = Post.query.filter_by(id=post_id).first()
    db.session.delete(post)
    db.session.commit()
    flash('The posting has been deleted.')
    return redirect(url_for('.index'))


# 举报某个帖子（问题）的功能
@main.route('/report/<post_id>')
@login_required
def report(post_id):
    post = Post.query.filter_by(id=post_id).first()
    n = Notification(receiver_id=102, timestamp=datetime.utcnow(),
                     username=current_user.username, action="report the post",
                     object=post.title, object_id=post.id)
    post.report_time += 1
    flash("You have reported a post\nThis post is reported for {} times".format(post.report_time))
    db.session.add(n)
    db.session.commit()
    return redirect(url_for('main.index'))


# 举报某个评论（回答）的功能
@main.route('/report_comment/<comment_id>')
@login_required
def report_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    id = comment.post.id
    n = Notification(receiver_id='102', timestamp=datetime.utcnow(),
                     username=current_user.username, action="report the comment in",
                     object=comment.post.title, object_id=id)
    comment.report_time += 1
    flash("You have reported a comment\nThis comment is reported for %d times", post.report_time)
    db.session.add(n)
    db.session.commit()
    return redirect(url_for('main.post', id=id))


# 警告某个用户的功能
@main.route('/alert/<post_id>')
@login_required
def alert(post_id):
    post = Post.query.filter_by(id=post_id).first()
    n = Notification(receiver_id=post.author_id, timestamp=datetime.utcnow(),
                     username="Administrator", action="has deleted ",
                     object="your post", object_id=post.id)
    flash("You have deleted a post\nThe alert has been sent to the user")
    db.session.add(n)
    db.session.commit()
    return redirect(url_for('main.index'))

# 分享某个评论（回答）的功能
@main.route('/share_comment/<comment_id>', methods=['GET', 'POST'])
@login_required
def share_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first_or_404()
    user_list = User.query.order_by(User.username)
    post = comment.post
    if request.method == 'GET':
        return render_template("comment_share.html", comment=comment, posts=[post], user_list=user_list)
    if request.method == 'POST':
        info = request.form["share_to"]
        user = User.query.filter_by(id=info).first_or_404()
        n = Notification(receiver_id=user.id, timestamp=datetime.utcnow(),
                         username=current_user.username, action="shares an answer to you",
                         object=post.title, object_id=post.id)
        db.session.add(n)
        db.session.commit()
        return redirect(url_for(".post", id=post.id))

#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   db.Date    :   2022-05-17 15:16
#   Desc    :
from datetime import datetime

from website import db

def to_dict(orm_obj) -> dict:
    row_dict = {}
    columns = orm_obj.__table__.columns  # type: ignore
    for column in columns:
        value = getattr(orm_obj, column.key)
        if isinstance(value, datetime):
            row_dict[column.key] = value.strftime("%Y-%m-%d %H:%M:%S")
        else:
            row_dict[column.key] = value
    return row_dict


class Tag(db.Model):
    __tablename__ = "tag"

    id = db.Column(db.Integer, primary_key=True)
    tid = db.Column(db.String(100), nullable=False, index=True, unique=True)  # 对外的非递增 ID
    name = db.Column(db.String(150), nullable=False, unique=True)
    image_url = db.Column(db.String(150), nullable=True)
    is_show = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now)
    updated_at = db.Column(
        db.DateTime(timezone=True), default=datetime.now, onupdate=datetime.now
    )


class Star(db.Model):
    __tablename__ = "star"

    id = db.Column(db.Integer, primary_key=True)
    repo_id = db.Column(db.Integer, nullable=False)
    star = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.Date, nullable=False)
    created_month = db.Column(db.String(20), nullable=False)
    created_year = db.Column(db.String(20), nullable=False)
    __table_args__ = (db.UniqueConstraint("repo_id", "created_at", name="idx_repo_date"),)


class Image(db.Model):
    __tablename__ = "image"

    id = db.Column(db.Integer, primary_key=True)
    repo_id = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(150), nullable=True)
    file_path = db.Column(db.String(150), nullable=True)
    sm_id = db.Column(db.String(150), nullable=True)
    sm = db.Column(db.String(200), nullable=True)
    upyun = db.Column(db.String(200), nullable=True)
    use_img_for = db.Column(db.String(100), nullable=False)  # logo、效果图、封面、文章
    size = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now)
    updated_at = db.Column(
        db.DateTime(timezone=True), default=datetime.now, onupdate=datetime.now
    )


class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, index=True)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now)
    updated_at = db.Column(
        db.DateTime(timezone=True), default=datetime.now, onupdate=datetime.now
    )


class Volume(db.Model):
    __tablename__ = "volume"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, index=True)
    num = db.Column(db.Integer)
    is_publish = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now)
    updated_at = db.Column(
        db.DateTime(timezone=True), default=datetime.now, onupdate=datetime.now
    )
    publish_at = db.Column(db.DateTime(timezone=True), nullable=True, default=None)


class Repository(db.Model):
    """
    GitHub 项目
    """

    __tablename__ = "repository"

    id = db.Column(db.Integer, primary_key=True)
    rid = db.Column(db.String(100), nullable=False, index=True, unique=True)  # 对外的非递增 ID
    gid = db.Column(db.Integer, nullable=True, index=True, unique=True)
    url = db.Column(db.String(200), nullable=False, index=True)
    full_name = db.Column(db.String(150), nullable=True)
    source = db.Column(db.String(50), nullable=False)
    uid = db.Column(db.String(50), nullable=False)

    name = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)
    title = db.Column(db.String(200), nullable=True)
    summary = db.Column(db.Text, nullable=True)  # 人为增加的项目描述
    code = db.Column(db.Text, nullable=True)  # 代码示例

    primary_lang = db.Column(db.String(50), nullable=True)
    lang_color = db.Column(db.String(50), nullable=True)
    homepage = db.Column(db.String(150), nullable=True)
    license = db.Column(db.String(100), nullable=True)
    open_issues = db.Column(db.Integer, nullable=True)
    subscribers = db.Column(db.Integer, nullable=True)
    stars = db.Column(db.Integer, nullable=True)
    stars_str = db.Column(db.String(20), nullable=True)
    forks = db.Column(db.Integer, nullable=True)
    file_sha = db.Column(db.String(100), nullable=True)  # README 文件 sha

    has_chinese = db.Column(db.Boolean, default=False)
    is_org = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    is_forked = db.Column(db.Boolean, default=False)
    is_show = db.Column(db.Boolean, default=False)  # 是否展示（无敏感词才能展示）
    is_hot = db.Column(db.Boolean, default=False)  # 是否置顶

    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now)
    updated_at = db.Column(
        db.DateTime(timezone=True), default=datetime.now, onupdate=datetime.now
    )
    repo_created_time = db.Column(db.BigInteger, nullable=True)
    repo_created_at = db.Column(db.DateTime(timezone=True), nullable=True)
    repo_pushed_time = db.Column(db.BigInteger, nullable=True)
    repo_pushed_at = db.Column(db.DateTime(timezone=True), nullable=True)
    repo_update_time = db.Column(db.BigInteger, nullable=True)
    repo_update_at = db.Column(db.DateTime(timezone=True), nullable=True)
    __table_args__ = {"mysql_row_format": "DYNAMIC"}


class RepoTag(db.Model):
    __tablename__ = "repo_tag"

    id = db.Column(db.Integer, primary_key=True)
    rid = db.Column(db.String(100), nullable=False)
    tid = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now)
    updated_at = db.Column(
        db.DateTime(timezone=True), default=datetime.now, onupdate=datetime.now
    )
    __table_args__ = (db.UniqueConstraint("rid", "tid", name="idx_r_t"),)


class Periodical(db.Model):
    """
    月刊
    """

    __tablename__ = "periodical"

    id = db.Column(db.Integer, primary_key=True)
    brief = db.Column(db.Text, nullable=True)
    suggestions = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    code = db.Column(db.Text, nullable=True)

    volume_id = db.Column(db.Integer, db.ForeignKey("volume.id"), nullable=False)
    volume = db.relationship("Volume", backref="periodical_of_volume", lazy=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    category = db.relationship("Category", backref="periodical_of_category", lazy=False)
    repo_id = db.Column(db.Integer, db.ForeignKey("repository.id"), nullable=False)
    repository = db.relationship(
        "Repository", backref="periodical_of_repository", lazy=False
    )
    image_id = db.Column(db.Integer, db.ForeignKey("image.id"), nullable=True)
    image = db.relationship("Image", backref="periodical_of_image", lazy=False)
    is_publish = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now)
    updated_at = db.Column(
        db.DateTime(timezone=True), default=datetime.now, onupdate=datetime.now
    )


class Role(db.Model):
    """
    角色（荣誉）
    """

    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True)
    name_w = db.Column(db.String(50), unique=True)  # 文
    name_l = db.Column(db.String(50), unique=True)  # 武
    color = db.Column(db.String(50), unique=True)  # 角色称呼
    level = db.Column(db.Integer)
    min_value = db.Column(db.Integer)


class Permission(db.Model):
    """
    权限（权利）
    """

    __tablename__ = "permission"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    code = db.Column(db.String(50), unique=True, index=True)


class User(db.Model):
    __tablename__ = "new_user"

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(100), nullable=False, index=True, unique=True)  # 对外的非递增 ID
    openid = db.Column(db.String(150), nullable=False)
    unionid = db.Column(db.String(150), nullable=True)
    session_key = db.Column(db.String(150), nullable=True)  # wx session key
    nickname = db.Column(db.String(150), nullable=True)
    gender = db.Column(db.Integer)
    city = db.Column(db.String(150), nullable=True)
    province = db.Column(db.String(150), nullable=True)
    country = db.Column(db.String(150), nullable=True)
    avatar = db.Column(db.String(200), nullable=True)
    permission_id = db.Column(
        db.Integer, db.ForeignKey("permission.id"), nullable=False, default=1
    )
    permission = db.relationship("Permission", backref="user_of_permission", lazy=False)
    is_ban = db.Column(db.Boolean, default=False)
    first_login = db.Column(db.DateTime, default=datetime.now)
    last_login = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class Comment(db.Model):
    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True)
    # 对外的非递增 ID
    cid = db.Column(db.String(100), nullable=False, index=True, unique=True)
    uid = db.Column(db.String(100), nullable=False)  # 用户的 uid
    item_id = db.Column(db.String(100), nullable=False)  # 评论对应实体的非递增 ID
    comment = db.Column(db.Text, nullable=True)  # 评论内容
    belong_to = db.Column(db.String(100), nullable=False)  # 隶属于项目或者文章
    is_show = db.Column(db.Boolean, default=False)  # 是否展示（无敏感词才能展示）
    is_hot = db.Column(db.Boolean, default=False)  # 是否置顶
    votes = db.Column(db.Integer, default=0)
    # 创建文章的时间
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now)
    # 数据源更新时间
    updated_at = db.Column(
        db.DateTime(timezone=True), default=datetime.now, onupdate=datetime.now
    )


class Article(db.Model):
    __tablename__ = "article"

    id = db.Column(db.Integer, primary_key=True)
    aid = db.Column(db.String(150), unique=True)
    title = db.Column(db.String(255))  # 标题
    content = db.Column(db.Text, nullable=True)
    desc = db.Column(db.String(255), nullable=True)
    author = db.Column(db.String(255), default="HelloGitHub")
    clicks_count = db.Column(db.Integer, default=0)
    pv_count = db.Column(db.Integer, default=0)
    like_count = db.Column(db.Integer, default=0)
    content_type = db.Column(db.String(255), default="article")
    is_publish = db.Column(db.Boolean, default=False)

    publish_at = db.Column(db.DateTime(timezone=True), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now)  # 创建文章的时间
    updated_at = db.Column(
        db.DateTime(timezone=True), default=datetime.now, onupdate=datetime.now
    )  # 数据源更新时间
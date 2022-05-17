#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   db.Date    :   2022-05-17 15:25
#   Desc    :
import time

from website import db
from website.models import Repository, Periodical, Comment,\
    User, Tag, RepoTag, to_dict


def get_repos(page: int = 1, page_size: int = 20) -> tuple:
    repo_list = []

    # 统计项目对应的评论数
    stmt = (
        db.session.query(
            Comment.item_id,
            db.func.count("*").label("c_total"),
            Comment.created_at.label("last_comment_at"),
        )
            .filter_by(is_show=True, belong_to="repository")
            .group_by(Comment.item_id)
            .order_by(Comment.created_at.desc(),)
            .subquery()
    )

    _query = (
        db.session.query(
            Repository, Periodical, stmt.c.c_total, stmt.c.last_comment_at,
            User)
            .outerjoin(Periodical)
            .outerjoin(User, User.uid == Repository.uid)
            .outerjoin(stmt, Repository.rid == stmt.c.item_id)
            .filter(
            Repository.is_deleted == 0,
            Repository.is_show == 1,
            Repository.title.isnot(None),
        )
            .order_by(stmt.c.last_comment_at.desc())
    )
    # 多取 1 个用来判断是否还有下一页
    repos = _query.slice((page-1) * page_size, page * page_size + 1).all()

    for repo, period, c_total, last_comment_at, user in repos:
        repo_dict = to_dict(repo)
        repo_dict["item_id"] = repo.rid
        repo_dict["item_type"] = 1
        repo_dict["public_time"] = time.mktime(period.volume.publish_at.timetuple())
        repo_dict["volume_name"] = period.volume.name
        repo_dict["period_desc"] = period.description
        repo_dict["suggestions"] = period.suggestions
        repo_dict["brief"] = period.brief
        if period.image:
            repo_dict["image_url"] = period.image.upyun
        else:
            repo_dict["image_url"] = None

        repo_dict["comment_total"] = c_total or 0
        repo_dict["last_comment_at"] = last_comment_at or None

        tags = (
            db.session.query(RepoTag, Tag)
                .outerjoin(Tag, RepoTag.tid == Tag.tid)
                .filter(RepoTag.rid == repo.rid)
                .all()
        )
        tag_list = []
        for _, tag in tags:
            tag_list.append({"name": tag.name, "tid": tag.tid})
        repo_dict["tags"] = tag_list

        repo_dict["user"] = {
            "uid": user.uid,
            "nickname": user.nickname,
            "avatar": user.avatar,}
        repo_list.append(repo_dict)

    if len(repo_list) > page_size:
        has_more = True
    else:
        has_more = False
    return repo_list[:page_size], has_more


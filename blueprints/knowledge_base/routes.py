

"""
blueprints/knowledge_base/routes.py

Module 8: Knowledge Base
Browse, search, filter, and view plant-care articles.
"""

from flask import Blueprint, render_template, request

from models import KnowledgeBaseArticle


knowledge_base_bp = Blueprint(
    "knowledge_base",
    __name__,
    url_prefix="/knowledge-base"
)


@knowledge_base_bp.route("/")
def browse():
    """Browse and search Knowledge Base articles."""

    search_term = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()

    query = KnowledgeBaseArticle.query

    if search_term:
        search_pattern = f"%{search_term}%"
        query = query.filter(
            db_or_search(search_pattern)
        )

    if category:
        query = query.filter(
            KnowledgeBaseArticle.category == category
        )

    articles = query.order_by(
        KnowledgeBaseArticle.title.asc()
    ).all()

    categories = [
        item[0]
        for item in KnowledgeBaseArticle.query
        .with_entities(KnowledgeBaseArticle.category)
        .filter(KnowledgeBaseArticle.category.isnot(None))
        .distinct()
        .order_by(KnowledgeBaseArticle.category.asc())
        .all()
    ]

    return render_template(
        "knowledge_base/browse.html",
        articles=articles,
        categories=categories,
        query=search_term,
        category=category
    )


@knowledge_base_bp.route("/<article_id>")
def article(article_id):
    """Display an individual Knowledge Base article."""

    article = KnowledgeBaseArticle.query.get_or_404(article_id)

    return render_template(
        "knowledge_base/article.html",
        article=article
    )


def db_or_search(search_pattern):
    """Search article title, symptoms, and treatment."""

    from sqlalchemy import or_

    return or_(
        KnowledgeBaseArticle.title.ilike(search_pattern),
        KnowledgeBaseArticle.symptoms.ilike(search_pattern),
        KnowledgeBaseArticle.treatment.ilike(search_pattern)
    )

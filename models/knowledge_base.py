"""
models/knowledge_base.py

Implements `KnowledgeBaseArticle` from the Phase 03 Class Diagram -- used
starting with the Knowledge Base module.
"""
from extensions import db
from models.user import gen_id


class KnowledgeBaseArticle(db.Model):
    __tablename__ = "knowledge_base_articles"

    articleId = db.Column("article_id", db.String, primary_key=True, default=lambda: gen_id("kba"))
    title = db.Column(db.String(160), nullable=False)
    symptoms = db.Column(db.Text, nullable=True)
    treatment = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(80), nullable=True)  # e.g. plant/vegetable name

    def to_dict(self):
        return {
            "articleId": self.articleId, "title": self.title, "symptoms": self.symptoms,
            "treatment": self.treatment, "category": self.category,
        }

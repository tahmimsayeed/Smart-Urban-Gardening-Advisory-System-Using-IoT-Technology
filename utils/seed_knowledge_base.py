"""
utils/seed_knowledge_base.py

Seeds the Knowledge Base with plant care articles the first time the app
starts, if the table is empty -- Module 8 (Display plant care
information). Called once from app.py, right after db.create_all(), so
there's no extra manual step to run.

Content mirrors the disease labels documented in utils/treatment_tips.py
(Module 3) so a Gardener can find the same underlying information either
automatically during a diagnosis, or any time by browsing here -- the two
modules serve the same knowledge through two independently-built
interfaces (a fast internal lookup dict vs. a browsable, searchable
reference library), exactly as planned when treatment_tips.py was first
written back in Module 3.
"""
from extensions import db
from models import KnowledgeBaseArticle

ARTICLES = [
    # Bitter Gourd
    dict(title="Bitter Gourd - Downy Mildew", category="Bitter Gourd",
         symptoms="Yellow angular spots on the upper leaf surface with grey-purple fuzzy growth underneath, especially in humid weather.",
         treatment="Improve airflow and avoid overhead watering; remove and destroy infected leaves; apply a copper-based or mancozeb fungicide early in the outbreak."),
    dict(title="Bitter Gourd - Mosaic Virus", category="Bitter Gourd",
         symptoms="Mottled yellow-green mosaic pattern on leaves, leaf curling, and stunted vine growth.",
         treatment="No cure once infected -- remove and destroy affected plants to stop spread, and control aphids/whiteflies, which transmit the virus, with insecticidal soap."),
    dict(title="Bitter Gourd - Fusarium Wilt", category="Bitter Gourd",
         symptoms="Sudden wilting of leaves and vines, yellowing starting from lower leaves, brown discoloration inside the stem.",
         treatment="Remove and destroy infected plants; rotate crops away from cucurbits for 2-3 seasons; use well-drained soil and avoid overwatering."),
    dict(title="Bitter Gourd - Healthy Leaf Signs", category="Bitter Gourd",
         symptoms="Firm, deep-green leaves with no spotting, curling, or discoloration.",
         treatment="No treatment needed -- continue your current watering and care routine."),
    # Bottle Gourd
    dict(title="Bottle Gourd - Anthracnose", category="Bottle Gourd",
         symptoms="Small water-soaked spots that enlarge into dark, sunken lesions on leaves, stems, and fruit.",
         treatment="Remove infected debris, avoid overhead irrigation, and apply a chlorothalonil or copper-based fungicide at the first sign of spotting."),
    dict(title="Bottle Gourd - Downy Mildew", category="Bottle Gourd",
         symptoms="Yellow angular patches on top of leaves with pale downy growth on the underside.",
         treatment="Increase plant spacing for airflow, water at the base rather than overhead, and apply a suitable fungicide if the outbreak spreads."),
    dict(title="Bottle Gourd - Healthy Leaf Signs", category="Bottle Gourd",
         symptoms="Broad, unblemished green leaves with sturdy vines.",
         treatment="No treatment needed -- continue your current watering and care routine."),
    # Cauliflower
    dict(title="Cauliflower - Black Rot", category="Cauliflower",
         symptoms="Yellow V-shaped lesions starting at leaf edges, blackened veins, and eventually a foul-smelling head rot.",
         treatment="Remove and destroy infected plants, avoid working in the field when leaves are wet, and rotate with non-cruciferous crops for at least 2 years."),
    dict(title="Cauliflower - Downy Mildew", category="Cauliflower",
         symptoms="Pale yellow patches on the upper leaf surface with grey-white fuzzy mold underneath.",
         treatment="Improve drainage and airflow, avoid overhead watering, and apply a copper-based fungicide if conditions stay cool and humid."),
    dict(title="Cauliflower - Healthy Leaf Signs", category="Cauliflower",
         symptoms="Broad blue-green leaves wrapped snugly around a firm, white curd.",
         treatment="No treatment needed -- continue your current watering and care routine."),
    # Eggplant
    dict(title="Eggplant - Verticillium Wilt", category="Eggplant",
         symptoms="Yellowing and wilting of lower leaves, often on one side of the plant first, with stunted growth.",
         treatment="No chemical cure -- remove infected plants, rotate crops for several years, and use resistant varieties where possible."),
    dict(title="Eggplant - Cercospora Leaf Spot", category="Eggplant",
         symptoms="Small circular grey-brown spots with darker borders on leaves, which may merge and cause leaf drop.",
         treatment="Remove affected leaves, avoid overhead watering, improve air circulation, and apply a labeled fungicide if spotting spreads quickly."),
    dict(title="Eggplant - Begomovirus", category="Eggplant",
         symptoms="Yellow mosaic mottling, upward leaf curling, and stunted plants.",
         treatment="Remove and destroy infected plants; control whitefly populations (the virus's vector) with sticky traps or insecticidal soap; avoid planting near infected fields."),
    dict(title="Eggplant - Healthy Leaf Signs", category="Eggplant",
         symptoms="Glossy deep-green leaves with a slight purple tinge on the veins, no spotting or curling.",
         treatment="No treatment needed -- continue your current watering and care routine."),
    # Cucumber
    dict(title="Cucumber - Downy Mildew", category="Cucumber",
         symptoms="Angular yellow spots bound by leaf veins on top of leaves, with grey-purple fuzz underneath in humid conditions.",
         treatment="Water at the base, space plants for airflow, remove infected leaves promptly, and apply a copper-based fungicide if it spreads."),
    dict(title="Cucumber - Anthracnose", category="Cucumber",
         symptoms="Dark, sunken circular lesions on leaves and fruit, sometimes with a pinkish spore mass in humid weather.",
         treatment="Remove infected debris at season's end, rotate crops, avoid overhead watering, and apply a suitable fungicide early in an outbreak."),
    dict(title="Cucumber - Healthy Leaf Signs", category="Cucumber",
         symptoms="Large, rough-textured, bright-green leaves with no yellowing or spotting.",
         treatment="No treatment needed -- continue your current watering and care routine."),
    # Tomato
    dict(title="Tomato - Bacterial Spot", category="Tomato",
         symptoms="Small dark water-soaked spots on leaves and fruit that may have a yellow halo; leaves can eventually drop.",
         treatment="Avoid overhead watering and working with wet plants, remove infected debris, and apply a copper-based bactericide preventively in wet seasons."),
    dict(title="Tomato - Leaf Curl Virus", category="Tomato",
         symptoms="Upward curling and yellowing of leaves, stunted growth, and reduced fruit set.",
         treatment="Remove and destroy infected plants; control whiteflies (the virus's vector) aggressively; use resistant varieties where available."),
    dict(title="Tomato - Spotted Wilt", category="Tomato",
         symptoms="Bronze-purple ring spots on leaves, dark streaking on stems, and distorted, ring-patterned fruit.",
         treatment="Remove infected plants promptly, control thrips (the virus's vector) with sticky traps/insecticidal soap, and avoid planting near infected ornamentals."),
    dict(title="Tomato - Healthy Leaf Signs", category="Tomato",
         symptoms="Deep-green, slightly fuzzy leaves with no spotting, curling, or yellowing.",
         treatment="No treatment needed -- continue your current watering and care routine."),
    # General
    dict(title="Watering Guidance for Container Vegetables", category="General",
         symptoms="Wilting despite moist soil (overwatering) or dry, crispy leaf edges (underwatering).",
         treatment="Water when the top inch of soil feels dry; ensure pots have drainage holes; water at the base in the morning to reduce fungal risk. See the Weather & Care page on each plant for a live recommendation based on sensor data and forecast."),
    dict(title="Reading a Disease Detection Result", category="General",
         symptoms="A Disease Detection result names a specific disease with a confidence score below 100%.",
         treatment="Treat higher-confidence results with more certainty, and lower-confidence ones as a starting point for closer visual inspection. When in doubt, isolate the plant and monitor for a few days before treating."),
    dict(title="Setting Up a Threshold Alert", category="General",
         symptoms="You want to be notified automatically if a plant's soil gets too dry.",
         treatment="Pair an IoT sensor to the plant, then set a minimum soil moisture threshold on the plant's Alerts page. You'll get a Threshold Alert the next time a simulated reading falls below it."),
]


def seed_if_empty():
    """Returns the number of articles inserted (0 if the table already
    had content, so this is safe to call on every app startup)."""
    if KnowledgeBaseArticle.query.count() > 0:
        return 0
    for article_data in ARTICLES:
        db.session.add(KnowledgeBaseArticle(**article_data))
    db.session.commit()
    return len(ARTICLES)

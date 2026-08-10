"""
utils/treatment_tips.py

Treatment Recommendation (Module 3 sub-feature). A lightweight, local
lookup keyed by disease label -- separate from the Knowledge Base module
(Module 8), which holds the fuller, browsable plant-care article set.

Keys below match EXACTLY (case-sensitive) the 21 class names the real
trained model (plant_model.keras) actually outputs, taken directly from
the class_names list Colab printed during training. This replaces an
earlier guessed-format version -- the guessed names didn't match the
model's real output, so every prediction was silently falling through to
the generic fallback message until this update.
"""

TREATMENT_TIPS = {
    # Bitter Gourd
    "BitterGourd_Downeymildew": "Improve airflow and avoid overhead watering; remove and destroy infected leaves; apply a copper-based or mancozeb fungicide early in the outbreak.",
    "BitterGourd_Freshleaf": "No treatment needed -- this leaf looks healthy. Keep up your current watering and care routine.",
    "BitterGourd_Fusariumwilt": "Remove and destroy infected plants; rotate crops away from cucurbits for 2-3 seasons; use well-drained soil and avoid overwatering.",
    "BitterGourd_Mosaicvirus": "No cure once infected -- remove and destroy affected plants to stop spread, and control aphids/whiteflies, which transmit the virus, with insecticidal soap.",
    # Bottle Gourd
    "Bottlegourd_Anthracnose": "Remove infected debris, avoid overhead irrigation, and apply a chlorothalonil or copper-based fungicide at the first sign of spotting.",
    "Bottlegourd_Downeymildew": "Increase plant spacing for airflow, water at the base rather than overhead, and apply a suitable fungicide if the outbreak spreads.",
    "Bottlegourd_Freshleaf": "No treatment needed -- this leaf looks healthy. Keep up your current watering and care routine.",
    # Cauliflower
    "Cauliflower_BlackRot": "Remove and destroy infected plants, avoid working in the field when leaves are wet, and rotate with non-cruciferous crops for at least 2 years.",
    "Cauliflower_Downymildew": "Improve drainage and airflow, avoid overhead watering, and apply a copper-based fungicide if conditions stay cool and humid.",
    "Cauliflower_Freshleaf": "No treatment needed -- this leaf looks healthy. Keep up your current watering and care routine.",
    # Cucumber
    "Cucumber_Anthracnoselesions": "Remove infected debris at season's end, rotate crops, avoid overhead watering, and apply a suitable fungicide early in an outbreak.",
    "Cucumber_Downymildew": "Water at the base, space plants for airflow, remove infected leaves promptly, and apply a copper-based fungicide if it spreads.",
    "Cucumber_Freshleaf": "No treatment needed -- this leaf looks healthy. Keep up your current watering and care routine.",
    # Eggplant
    "Eggplant_EggplantCercoporaleafspot": "Remove affected leaves, avoid overhead watering, improve air circulation, and apply a labeled fungicide if spotting spreads quickly.",
    "Eggplant_Eggplantbegomovirus": "Remove and destroy infected plants; control whitefly populations (the virus's vector) with sticky traps or insecticidal soap; avoid planting near infected fields.",
    "Eggplant_Eggplantfreshleaf": "No treatment needed -- this leaf looks healthy. Keep up your current watering and care routine.",
    "Eggplant_Eggplantverticilliumwilt": "No chemical cure -- remove infected plants, rotate crops for several years, and use resistant varieties where possible.",
    # Tomato
    "Tomato_TomatoBacterialspot": "Avoid overhead watering and working with wet plants, remove infected debris, and apply a copper-based bactericide preventively in wet seasons.",
    "Tomato_TomatoFreshleaf": "No treatment needed -- this leaf looks healthy. Keep up your current watering and care routine.",
    "Tomato_Tomatoleafcurlvirus": "Remove and destroy infected plants; control whiteflies (the virus's vector) aggressively; use resistant varieties where available.",
    "Tomato_Tomatospottedwilt": "Remove infected plants promptly, control thrips (the virus's vector) with sticky traps/insecticidal soap, and avoid planting near infected ornamentals.",
}

GENERIC_FALLBACK = (
    "No specific treatment tip is available for this label yet. As a general "
    "precaution: isolate the plant from others, remove any visibly affected "
    "leaves, avoid overhead watering, and monitor closely over the next few days."
)


def get_treatment_tip(disease_label):
    return TREATMENT_TIPS.get(disease_label, GENERIC_FALLBACK)

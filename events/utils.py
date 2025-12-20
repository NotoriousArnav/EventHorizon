def extract_registration_schema(post_data):
    schema = []
    questions = {}

    for key, value in post_data.items():
        if key.startswith("question_label_"):
            index = key.split("_")[-1]
            questions.setdefault(index, {})["label"] = value
        elif key.startswith("question_type_"):
            index = key.split("_")[-1]
            questions.setdefault(index, {})["type"] = value
        elif key.startswith("question_id_"):
            index = key.split("_")[-1]
            questions.setdefault(index, {})["id"] = value

    for index, data in questions.items():
        label = data.get("label", "").strip()
        if label:
            schema.append(
                {
                    "id": data.get("id", f"q_{index}"),
                    "label": label,
                    "type": data.get("type", "text"),
                }
            )

    return schema

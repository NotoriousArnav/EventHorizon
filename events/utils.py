# Event Horizon - Futuristic Event Management Platform
# Copyright (C) 2025-2026 Arnav Ghosh
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.


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

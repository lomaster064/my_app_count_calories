import json
from dataclasses import dataclass

import httpx

from app.core.config import settings


@dataclass
class AIItem:
    name: str
    grams_estimate: float
    calories: float
    protein: float
    fat: float
    carbs: float
    confidence: float


@dataclass
class AIResult:
    items: list[AIItem]
    total_calories: float
    total_protein: float
    total_fat: float
    total_carbs: float
    needs_clarification: bool
    question: str | None


def _default_mock() -> AIResult:
    items = [
        AIItem(
            name="Овсянка с ягодами",
            grams_estimate=250,
            calories=320,
            protein=12,
            fat=8,
            carbs=48,
            confidence=0.62,
        )
    ]
    return AIResult(
        items=items,
        total_calories=320,
        total_protein=12,
        total_fat=8,
        total_carbs=48,
        needs_clarification=True,
        question="Уточните примерную граммовку или объем порции.",
    )


def analyze_food_photo(image_url: str) -> tuple[AIResult, dict]:
    if not settings.openai_api_key:
        return _default_mock(), {"provider": "mock"}

    prompt = (
        "Распознай еду на фото и верни строго JSON: "
        "{items:[{name,grams_estimate,calories,protein,fat,carbs,confidence}],"
        "total_calories,total_protein,total_fat,total_carbs,"
        "needs_clarification,question}."
    )

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Ты нутриционный ассистент."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            },
        ],
        "response_format": {"type": "json_object"},
    }

    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "Content-Type": "application/json",
    }

    with httpx.Client(timeout=30) as client:
        response = client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

    content = data["choices"][0]["message"]["content"]
    parsed = json.loads(content)
    items = [AIItem(**item) for item in parsed.get("items", [])]
    result = AIResult(
        items=items,
        total_calories=parsed.get("total_calories", 0),
        total_protein=parsed.get("total_protein", 0),
        total_fat=parsed.get("total_fat", 0),
        total_carbs=parsed.get("total_carbs", 0),
        needs_clarification=parsed.get("needs_clarification", False),
        question=parsed.get("question"),
    )
    return result, parsed

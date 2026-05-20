REQUIRED_FIELDS = ["name", "population", "capital", "year"]


def validate_country(data: dict, partial: bool = False) -> str | None:
    """
    partial=False → POST (все поля обязательны)
    partial=True  → PUT  (проверяем только переданные поля)
    Возвращает строку-ошибку или None если всё ок.
    """
    if not partial:
        for field in REQUIRED_FIELDS:
            if field not in data:
                return f"Missing required field: {field}"

    if "name" in data:
        if not isinstance(data["name"], str) or not data["name"].strip():
            return "Field 'name' must be a non-empty string"

    if "population" in data:
        pop = data["population"]
        if not isinstance(pop, int) or isinstance(pop, bool):
            return "Field 'population' must be an integer"
        if not (1 <= pop <= 2_000_000_000):
            return "Field 'population' must be between 1 and 2,000,000,000"

    if "capital" in data:
        if not isinstance(data["capital"], str) or not data["capital"].strip():
            return "Field 'capital' must be a non-empty string"

    if "year" in data:
        yr = data["year"]
        if not isinstance(yr, int) or isinstance(yr, bool):
            return "Field 'year' must be an integer"

    return None

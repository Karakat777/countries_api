class Record:
    def __init__(self, id, name, population, capital, year, user_id=None):
        self.id         = id
        self.name       = name
        self.population = population
        self.capital    = capital
        self.year       = year
        self.user_id    = user_id   # чей record (привязка к User)

    # ── сериализация ─────────────────────────────────────────────────
    def to_dict(self) -> dict:
        return {
            "id":         self.id,
            "name":       self.name,
            "population": self.population,
            "capital":    self.capital,
            "year":       self.year,
            "user_id":    self.user_id,
        }

    # ── десериализация ───────────────────────────────────────────────
    @classmethod
    def from_dict(cls, data: dict) -> "Record":
        return cls(
            id         = data["id"],
            name       = data["name"],
            population = data["population"],
            capital    = data["capital"],
            year       = data["year"],
            user_id    = data.get("user_id"),
        )

    def __repr__(self):
        return f"<Record id={self.id} name={self.name}>"

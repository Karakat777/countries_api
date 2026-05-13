# Countries REST API — Group 6

A Flask-based REST API for managing Country records.
Supports full CRUD operations and stores data in a local `countries.json` file using Python's built-in `json` and `os` modules.

---

## Setup

```bash
# 1. Unzip the project and enter the folder
cd countries_api

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
python app.py
```

Server starts at: **http://127.0.0.1:5001**

---

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/` | Welcome message |
| GET | `/countries` | Get all countries |
| GET | `/countries?capital=Astana` | Filter by capital |
| GET | `/countries?min_pop=1000000` | Filter by min population |
| GET | `/countries/<id>` | Get one country by ID |
| POST | `/countries` | Create a new country |
| PUT | `/countries/<id>` | Update a country (partial allowed) |
| DELETE | `/countries/<id>` | Delete a country |

---

## Example Requests & Responses

**GET /countries** → 200
```json
{
  "countries": [
    {"id": 1, "name": "Kazakhstan", "population": 19000000, "capital": "Astana", "year": 1991}
  ]
}
```

**GET /countries/99** → 404
```json
{"error": "Country with id 99 not found"}
```

**POST /countries** — request body:
```json
{"name": "France", "population": 68000000, "capital": "Paris", "year": 843}
```
→ 201
```json
{"message": "Country created", "country": {"id": 4, "name": "France", "population": 68000000, "capital": "Paris", "year": 843}}
```

**POST /countries** — missing field → 400
```json
{"error": "Missing required field: name"}
```

**PUT /countries/1** — partial update:
```json
{"population": 20000000}
```
→ 200
```json
{"message": "Country updated", "country": {"id": 1, "name": "Kazakhstan", "population": 20000000, "capital": "Astana", "year": 1991}}
```

**DELETE /countries/1** → 200
```json
{"message": "Country with id 1 deleted successfully"}
```

---

## Data Storage

- **File:** `countries.json`
- **Format:** JSON array of objects
- **Location:** Project root directory
- **Modules used:** `json`, `os` (no external databases)

---

## Validation Rules

| Field | Type | Rule |
|-------|------|------|
| name | string | Required, non-empty |
| population | int | Required, 1 – 2,000,000,000 |
| capital | string | Required, non-empty |
| year | int | Required, must be integer |

---

## Author

- **Name:** Karakat
- **Group:** SE-2507
- **Student ID:** 45

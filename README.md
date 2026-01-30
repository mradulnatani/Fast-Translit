---

#  AI-Powered Address Transliteration & Validation

An intelligent pipeline designed for e-commerce to bridge the gap between messy user inputs (voice-to-text, regional dialects) and clean, queryable geographic data.

##  The Problem

E-commerce logistics often fail due to "dirty" address data:

* **Phonetic Errors:** "Devas" vs "Dewas" (Common in Voice-to-Text).
* **Language Barriers:** Regional scripts (Hindi/Marathi/etc.) are difficult to query in standard SQL databases.
* **Spelling Inconsistency:** Non-standard transliteration of local landmarks.

##  The Solution

This system implements a two-layer validation strategy to ensure high-fidelity data:

1. **AI Transliteration Layer:** Powered by **AI4Bharat Indic Transliteration** to map regional scripts to phonetic Roman (English) script.
2. **OSM Validation Layer:** Cross-references the output with **OpenStreetMap (OSM)** binary data (`.pbf`) using **Fuzzy String Matching** to find the real-world geographic "Ground Truth."

---

##  Tech Stack

* **Backend:** FastAPI (Python 3.10)
* **Database:** PostgreSQL + SQLAlchemy ORM
* **NLP:** AI4Bharat Indic-Transliteration
* **Geo-Data:** Osmium & OpenStreetMap (PBF parsing)
* **Fuzzy Logic:** TheFuzz (Levenshtein Distance)

---

##  Project Structure

```text
AI-Transliteration/
├── Backend/
│   ├── db.py            # Database connection & Session local
│   ├── models.py        # SQLAlchemy Tables (submissions & normalized_data)
│   ├── schemas.py       # Pydantic models for API validation
│   ├── crud_helper.py   # Core Logic: Transliteration + OSM + Fuzzy Matching
│   ├── translit.py      # AI4Bharat wrapper logic
│   └── create_db.py     # Database schema initialization
├── osm-data/            # Storage for local .pbf geographic files
├── main.py              # FastAPI entry point & Routes
└── requirements.txt     # Project dependencies

```

---

##  Installation & Setup

### 1. Environment Setup

**Note:** Python 3.10 is strictly recommended due to AI library dependencies.

```bash
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

```

### 2. Database Configuration

Update your PostgreSQL credentials in `Backend/db.py`, then initialize the tables:

```bash
python Backend/create_db.py

```

### 3. Prepare Geographic Data

To maintain privacy and speed, we use local OSM extracts. Place your `.pbf` file in `osm-data/`.

```bash
# Example: Filtering for Ujjain to optimize performance
osmium tags-filter india-latest.osm.pbf addr:city=Ujjain -o osm-data/ujjain_filtered.osm.pbf

```

---

##  Usage

### Running the Server

```bash
fastapi run main.py

```

* **API Endpoint:** `http://localhost:8000/submit`
* **Interactive Docs:** `http://localhost:8000/docs`

### Example Request

```json
{
  "pin_code": 456001,
  "state": "मध्य प्रदेश",
  "city": "उज्जैन",
  "locality": "जवाहर मार्ग",
  "landmark": "शांतिलाल मुन्नालाल एंड कंपनी"
}

```

---

##  Validation Logic Workflow

1. **Ingestion:** Receives Hindi/Regional text via FastAPI.
2. **Transliteration:** AI4Bharat converts `जवाहर मार्ग` → `Jawahar Marg`.
3. **OSM Retrieval:** The system scans local `.pbf` data for nodes/ways matching the Pincode.
4. **Fuzzy Correction:** `TheFuzz` compares `Jawahar Marg` against all street names in the OSM extract.
5. **Normalization:** The most likely match (Ground Truth) is saved to the `normalized_data` table.


````markdown
# Nominatim Docker Setup

This guide explains how to set up Nominatim (OpenStreetMap geocoding engine) on your system using Docker. Nominatim allows you to get location information (like city, locality, or postal code) from coordinates or addresses.

---

## 1. Prepare your workspace

Create a folder to store your OSM data and Nominatim files.

```bash
mkdir -p ~/nominatim-data
cd ~/nominatim-data
````

This folder will hold the `.osm.pbf` data file and Nominatim database.

---

## 2. Download OSM data

You need a PBF file for the region you want. You can download it from [Geofabrik](https://download.geofabrik.de/).

```bash
# Example: Central India region
wget https://download.geofabrik.de/asia/india/central-india-latest.osm.pbf -O central-india.osm.pbf
```

This file contains all map data for your region.

---

## 3. Run Nominatim Docker container

Run the container and point it to your downloaded PBF file.

```bash
docker run -d \
  --name nominatim \
  -v ~/nominatim-data/central-india.osm.pbf:/nominatim/data/central-india.osm.pbf \
  -e PBF_PATH=/nominatim/data/central-india.osm.pbf \
  -p 7070:8080 \
  mediagis/nominatim:4.3
```

**Explanation:**

* `-v ...:/nominatim/data/...` → Mounts your local PBF file inside the container.
* `-e PBF_PATH=...` → Tells Nominatim where the data file is inside the container.
* `-p 7070:8080` → Exposes Nominatim on port 7070 locally.
* `mediagis/nominatim:4.3` → The Docker image for Nominatim. Use a specific version instead of `latest`.

> ⚠️ First-time setup will take **a long time** because Nominatim needs to import and index the entire OSM dataset.

---

## 4. Check container logs

To see the import progress:

```bash
docker logs -f nominatim
```

You will see messages like “Importing X nodes” and “Building indexes.” Wait until it finishes.

---

## 5. Access Nominatim API

Once the import is complete, you can query the API:

**Example: Get location info from postal code**

```bash
curl "http://localhost:7070/search?format=json&q=456001,India"
```

**Example: Reverse geocoding (coordinates → address)**

```bash
curl "http://localhost:7070/reverse?format=json&lat=23.25&lon=77.41"
```

---

## 6. Persisting data

* The imported database is stored inside the container by default.
* To avoid re-importing, mount a **volume** for the Postgres database (optional advanced setup).

---

## 7. Stopping and restarting

```bash
# Stop container
docker stop nominatim

# Start container
docker start nominatim
```

You **do not** need to re-import the dataset unless you delete the database or the container.

---

## 8. Notes

* Nominatim is for geocoding (address ↔ coordinates).
* For production, check [Nominatim’s official Docker docs](https://github.com/mediagis/nominatim-docker).
* Large datasets (like full India) require **tens of GBs** of RAM and disk space.

---

```


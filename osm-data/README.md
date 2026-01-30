# OSRM Server Setup Using Docker (Step-by-Step)

This document explains **exactly the steps** required to set up and run an **OSRM routing server locally using Docker**, along with **what each step does**.

The steps are written so you can **directly copy-paste the commands** when setting it up again.

---

## 1. Prerequisites

Make sure you have:

* Docker installed and running
* At least **8–12 GB RAM** (OSRM is memory-intensive)
* An `.osm.pbf` OpenStreetMap extract (India / region / city)

Check Docker:

```bash
docker --version
```

---

## 2. Directory Structure

Create a working directory (any name is fine):

```bash
mkdir osrm-data
cd osrm-data
```

This directory will hold:

* The raw `.osm.pbf` file
* All generated OSRM routing files

---

## 3. Place the OSM Data File

Example:

```bash
ls
central-zone-260126.osm.pbf
```

This file is the **raw OpenStreetMap data**.

---

## 4. OSRM Data Processing Pipeline (ONE-TIME SETUP)

OSRM **cannot route directly on `.osm.pbf` files**.
It must preprocess the data into routing graphs.

### Overview of the pipeline

1. **Extract** → parses roads & rules from OSM
2. **Contract / Partition + Customize** → builds fast routing graphs
3. **Route** → starts the HTTP server

---

## 5. Step 1: Extract Road Network

```bash
docker run -t -v "${PWD}:/data" osrm/osrm-backend \
  osrm-extract -p /opt/car.lua /data/central-zone-260126.osm.pbf
```

### What this does

* Reads raw OSM data
* Applies the **car routing profile** (`car.lua`)
* Extracts:

  * Roads
  * Turn restrictions
  * Speed limits
  * One-way rules
* Produces base `.osrm` files

### Output files created

```
central-zone-260126.osrm
central-zone-260126.osrm.names
central-zone-260126.osrm.geometry
central-zone-260126.osrm.edges
...
```

⏱️ **Slow** (CPU + RAM heavy)

---

## 6. Step 2: Build Routing Graph (CH algorithm)

```bash
docker run -t -v "${PWD}:/data" osrm/osrm-backend \
  osrm-contract /data/central-zone-260126.osrm
```

### What this does

* Converts extracted data into a **Contraction Hierarchy graph**
* Precomputes shortcuts for ultra-fast routing
* This is why OSRM answers queries in milliseconds

### Key points

* Very CPU & RAM intensive
* Must complete successfully before routing

---

## 7. IMPORTANT: Do I need to repeat these steps?

❌ **NO** — as long as:

* The `.osrm*` files remain
* You don’t change the `.osm.pbf` file

✅ These steps are **ONE-TIME ONLY** per dataset

You **do NOT** redo them when:

* Restarting your laptop
* Restarting Docker
* Restarting the OSRM server

---

## 8. Step 3: Start the OSRM Routing Server

```bash
docker run -d -p 5000:5000 -v "${PWD}:/data" osrm/osrm-backend \
  osrm-routed --algorithm ch /data/central-zone-260126.osrm
```

### What this does

* Starts an HTTP server on **port 5000**
* Loads the preprocessed routing graph into memory
* Ready to accept routing requests

---

## 9. Verify the Server

Test with a route request:

```bash
curl "http://localhost:5000/route/v1/driving/77.41,23.25;77.58,23.22?overview=false"
```

Expected response:

```json
{"code":"Ok","routes":[...]}
```

If you see `"code":"Ok"`, your OSRM server is working correctly.

---

## 10. What Happens on System Reboot?

After reboot:

### You ONLY need this:

```bash
docker run -d -p 5000:5000 -v "${PWD}:/data" osrm/osrm-backend \
  osrm-routed --algorithm ch /data/central-zone-260126.osrm
```

### You DO NOT rerun:

* `osrm-extract`
* `osrm-contract`

Unless you change the map data.

---

## 11. When to Re-run Full Processing

You must redo **extract + contract** if:

* You download a new `.osm.pbf`
* You change routing profile (car → bike → foot)
* You want updated roads

---

## 12. Summary

| Step     | Command         | Frequency        |
| -------- | --------------- | ---------------- |
| Extract  | `osrm-extract`  | Once per dataset |
| Contract | `osrm-contract` | Once per dataset |
| Serve    | `osrm-routed`   | Every start      |

---

## 13. Notes

* OSRM is a **routing engine**, not a map renderer
* Map visualization is done separately (Leaflet, MapLibre, etc.)
* This setup is identical to how production routing systems work

---

✅ You now have a clean, reproducible OSRM setup.


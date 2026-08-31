# CEP GeoFinder

CEP GeoFinder is a geospatial data processing tool for Brazilian postal codes (CEPs). It imports CEP and address data into PostgreSQL, associates CEPs with geographic coordinates through geocoding, and provides spatial queries for identifying CEPs within a specified radius of a geographic location.

The current project scope is limited to **CEPs within the city of São Paulo, Brazil**. This is a scope limitation of the current dataset and implementation rather than a fundamental limitation of the underlying approach.

The project is built around **Python, PostgreSQL and PostGIS**.

---

## Overview

CEP GeoFinder provides a pipeline for transforming CEP data into a geographically queryable dataset:

```text
OpenCEP Data
     │
     ▼
PostgreSQL
     │
     ▼
CEP Geocoding
     │
     ▼
Latitude / Longitude
     │
     ▼
PostGIS Spatial Queries
     │
     ▼
Nearby CEPs
```

The primary use case is determining which CEPs are geographically located within a specified distance of a latitude/longitude coordinate.

For example:

```text
Input:
    Latitude:  -23.5505
    Longitude: -46.6333
    Radius:     5 km

Output:
    CEPs located within 5 km of the specified point
```

---

## Features

* Import CEP and address data into PostgreSQL.
* Geocode CEPs using a local Nominatim service.
* Store geographic coordinates alongside CEP records.
* Perform radius-based geographic searches using PostGIS.
* Order matching CEPs by geographic distance.
* Perform spatial calculations directly in PostgreSQL.

---

## Technology Stack

| Component  | Purpose                                   |
| ---------- | ----------------------------------------- |
| Python     | Data processing and database interaction  |
| PostgreSQL | Persistent data storage                   |
| PostGIS    | Geographic data types and spatial queries |
| OpenCEP    | Source of CEP and address data            |
| Nominatim  | Geocoding service                         |

---

## Project Structure

```text
cep-geofinder/
│
├── data/
│   └── .gitkeep
│
├── scripts/
│   ├── cep_to_db.py
│   ├── cep_to_coordinate.py
│   └── check_area.py
│
├── sql/
│   └── .gitkeep
│
└── README.md
```

### `scripts/cep_to_db.py`

Imports CEP and address data from the OpenCEP dataset into PostgreSQL.

The importer reads the source JSON files and stores the relevant CEP and address fields in the `ceps` table. CEP values are normalized by removing the conventional hyphen.

The current dataset and import process are scoped to **São Paulo city**.

### `scripts/cep_to_coordinate.py`

Identifies CEP records that do not yet have geographic coordinates and submits them to a locally hosted Nominatim service.

The returned latitude and longitude values are stored in PostgreSQL.

Only records without existing coordinates are processed.

A delay is maintained between requests to reduce the request rate sent to the geocoding service.

### `scripts/check_area.py`

Provides the project's geographic lookup functionality.

Given a latitude, longitude, and radius in kilometers, the script uses PostGIS to identify CEPs located within the specified distance and orders the results by their distance from the requested coordinate.

---

## Requirements

The following software is required:

* Python 3
* PostgreSQL
* PostGIS
* OpenCEP data
* A local Nominatim instance

Python dependencies currently used by the scripts include:

```bash
pip install psycopg requests
```

PostGIS must be enabled in the PostgreSQL database:

```sql
CREATE EXTENSION postgis;
```

---

## Database Configuration

The current scripts use the following PostgreSQL development configuration:

```text
Host:     localhost
Port:     5432
Database: cep_geofinder
User:     postgres
```

The database can be created with:

```bash
createdb cep_geofinder
```

PostGIS can then be enabled with:

```sql
CREATE EXTENSION postgis;
```

Database credentials are currently defined directly in the Python scripts.

For production or shared environments, credentials should be moved to environment variables or another appropriate configuration mechanism.

---

## Data Import

CEP data is obtained from the OpenCEP dataset.

Place the dataset under the path expected by `cep_to_db.py`.

The current repository structure expects data under:

```text
data/
└── opencepdata/
    └── v1/
        └── ...
```

Once the dataset has been prepared, run:

```bash
python scripts/cep_to_db.py
```

The importer processes the available records and inserts the corresponding CEP and address information into PostgreSQL.

Duplicate CEP records are not inserted.

The current import process is scoped to **São Paulo city**.

---

## Geocoding

CEP records without geographic coordinates can be processed using:

```bash
python scripts/cep_to_coordinate.py
```

The current implementation expects a Nominatim-compatible service at:

```text
http://127.0.0.1:8088/search
```

The script queries the geocoding service using the CEP and stores the returned latitude and longitude values in PostgreSQL.

Only records for which coordinates have not yet been populated are processed.

### Nominatim

The geocoding service should be operated in accordance with the applicable Nominatim and OpenStreetMap usage policies.

A local Nominatim instance is particularly useful when processing a larger number of CEP records, as it avoids relying on a public geocoding endpoint for bulk requests.

---

## Geographic Queries

The geographic lookup functionality is implemented in `check_area.py`.

A query consists of:

* Latitude
* Longitude
* Search radius in kilometers

For example:

```python
from scripts.check_area import consulta

results = consulta(
    latitude=-23.5505,
    longitude=-46.6333,
    raio_km=5
)

for result in results:
    print(result)
```

The query returns CEP records located within the requested radius and orders them by distance.

---

## PostGIS

CEP GeoFinder uses PostGIS to perform geographic calculations directly within PostgreSQL.

The spatial query uses:

```sql
ST_DWithin()
```

to determine whether a CEP falls within the requested radius and:

```sql
ST_Distance()
```

to order matching records by geographic distance.

Coordinates use the WGS 84 coordinate reference system (`SRID 4326`), with geographic calculations performed in meters.

Conceptually:

```text
Latitude / Longitude
        │
        ▼
  Geographic Point
        │
        ▼
   ST_DWithin()
        │
        ├── Outside radius
        │       └── Excluded
        │
        └── Inside radius
                │
                ▼
         ST_Distance()
                │
                ▼
         Ordered results
```

This allows the database to perform the spatial filtering and distance calculations without requiring the application to calculate distances for every record.

---

## Example

Suppose a query needs to identify CEPs within a 10 km radius of a location in São Paulo city.

The input can be represented as:

```text
Latitude:  -23.5505
Longitude: -46.6333
Radius:    10 km
```

The geographic query returns CEPs that fall within the specified radius, ordered from nearest to farthest.

This can be useful for applications involving:

* Geographic segmentation
* Delivery-area analysis
* Service-area definition
* Regional analysis
* Location-based search
* Proximity-based CEP selection

---

## Data Accuracy

Geographic results should be considered approximate.

A CEP may correspond to multiple addresses or represent a geographic area rather than a single physical point. As a result, the coordinates obtained through geocoding should be treated as representative coordinates rather than exact locations for every address associated with a CEP.

The accuracy of the geographic results therefore depends on:

1. The underlying CEP and address data.
2. The geocoding service.
3. The methodology used to associate the CEP with a geographic coordinate.

CEP GeoFinder should therefore not be considered an address-level navigation or routing system.

---

## Configuration

Several configuration values are currently defined directly within the scripts.

For a more flexible deployment, the following values could be externalized:

```text
DATABASE_HOST
DATABASE_PORT
DATABASE_NAME
DATABASE_USER
DATABASE_PASSWORD

GEOCODER_URL
OPENCEP_PATH
```

Environment variables, configuration files, or another dedicated configuration mechanism can be used depending on the deployment environment.

---

## Data Sources

CEP GeoFinder relies on external data and services for its functionality.

Relevant sources include:

* **OpenCEP** — CEP and address data.
* **OpenStreetMap / Nominatim** — geographic data and geocoding.

Users are responsible for complying with the licenses, attribution requirements, usage policies, and rate limits applicable to each external source or service.

---

# CARE-SM Toolkit

## Why to use it?

The implementation of the Clinical And Registry Entries (CARE) Semantic Model for CSV data entails a meticulous and technically advanced workflow. By leveraging the power of the CARE-SM, YARRRML templates and incorporating the critical curation step executed by the CARE-SM toolkit, this implementation achieves robustness, accuracy, and reliability in generating RDF-based CARE SM-oriented patient data.

The toolkit serves as a module dedicated to performing a curation step prior to the conversion of data into RDF. The primary transformations carried out by the toolkit include:

* Quality control for column names.

* Adding every domain specific ontological term required to define every instances of the model, these terms are specific for every data element.

* Splitting the column labeled as `value` into distinct datatypes. This enables YARRRML to interpret each datatype differently, facilitating the subsequent processing.

* Conducting a quality control among `age`/`date`, `startdate` and `enddate` columns to ensure data consistency and validity.

* Eliminating any row that lacks the minimal required data to minimize the generation of incomplete RDF transformations.

* Creation of the column called `uniqid` that assigns a unique identifier to each observation. This prevents the RDF instances from overlapping with one another, ensuring their distinctiveness and integrity.

## Requirements 

* In order to use CARE-SM Toolkit functionality:
* All CSV files **MUST** be named according the data tags described at the CARE-SM glossary, documented at [CARE-SM implementation](https://github.com/wilkinsonlab/CARE-Semantic-Model-Version-2/blob/main/implementation/CSV/README.md) E.g.: `Diagnosis.csv`, `Birthdate.csv`

 * All your CSV data content **MUST** be compatible with the CARE-SM glossary, documented at [CARE-SM implementation](https://github.com/wilkinsonlab/CARE-Semantic-Model-Version-2/blob/main/implementation/CSV/README.md)


## Docker

There's a Docker-based implementation controlled via API (using FastAPI) that you can use for mounting this data transformation step as a part of your CARE-SM implementation.

You can edit the [docker-compose.yaml](https://github.com/wilkinsonlab/CARE-Semantic-Model-Version-2/blob/main/implementation/Toolkit/docker-compose.yaml) to control the volume folder in order to pass your CSV-based patient data:

```yaml
version: "3.8"

services:
  api:
    image: markw/care-sm-toolkit:2.0.0 # Check latest version
    ports:
      - "8000:8000"
    volumes:
      - ./location/of/your/data:/data
```

**Note:** the mounted folder's CSV files must sit directly inside it (no `obo`/`snomed` subfolder) — the API always processes as OBO, reading straight from that path. `/data` is a fixed convention (overridable via the `CARE_DATA_DIR` environment variable) — deliberately the same path [Sextans Fix](#sextans-fix) mounts its own data folder to, so this image is a drop-in replacement there.

**Note** IP and Port can be customized in the docker compose as well.

Run [docker compose](https://docs.docker.com/compose/) to start the containers:

``` 
 docker compose up -d
```

Once its running, you can use in your browser the OpenAPI documentation at http://localhost:8000/docs so inspect all the possible requests and trigger the execution

Alternatively, you trigger the data transformation in the terminal by the following:

```
curl -X POST http://localhost:8000/toolkit
```
 
**Congrats!** You will find your transformed data, stored as `CARE.csv` at the folder you defined as volume below.

To stop and remove the implementation, do the following:

```
docker compose down
```

(sextans-fix)=
## Sextans Fix

Most real deployments don't run this Docker image standalone — they run it as one of four services in [Sextans Fix](https://github.com/wilkinsonlab/Sextans-Suite), the packaged installer most CARE-SM users actually use to stand up a data server. Understanding how the pieces fit together is worth it even if you're only using this toolkit directly, since it's the shape the rest of the ecosystem assumes:

* **GraphDB** — holds the RDF-formatted record data.
* **Transformation Daemon** — orchestrator; the single HTTP endpoint you actually trigger (an empty `GET` request, no parameters). On request, it runs the CARE-SM curation step and then the RDF transformation, in order, and loads the result into GraphDB.
* **CARE-SM** (this toolkit) — enrichment and quality control over the CSV data, prior to transformation. This is the `caresm` service in Sextans Fix's `docker-compose-template.yml`.
* **yarrrml-rdfizer** — executes the actual CSV → RDF transformation using the [CARE-SM YARRRML mapping](https://github.com/wilkinsonlab/CARE-Semantic-Model-Version-2/tree/main/implementation/YARRRML).

The `caresm` and `yarrrml-rdfizer` services are two separate containers, each with its own filesystem, chained by mounting the **same host folder** at each container's own fixed internal path:

```yaml
services:
  caresm:
    image: fairdatasystems/care:2026-07-10   # or markw/care-sm-toolkit:2.0.0, drop-in compatible
    volumes:
      - ./data:/data          # this toolkit's own convention

  yarrrml-rdfizer:
    image: fairdatasystems/yrml:2026-07-10
    environment:
      - SERIALIZATION=nquads
    volumes:
      - ./data:/mnt/data      # yarrrml-rdfizer's own convention -- same host folder, different mount point
```

`caresm` reads raw per-model CSVs from `/data` and writes the curated `CARE.csv` back into that same folder. `yarrrml-rdfizer` then reads `/mnt/data/CARE.csv` and the YARRRML mapping (`/mnt/data/CARE_yarrrml.yaml`) from what is, on the host, the exact same folder — and writes the resulting triples to `./data/triples/`. Neither container needs to know about the other's internal path; the host folder is the only thing they actually share.

If you're deploying via Sextans Fix's installer directly, none of this needs manual configuration — `install-sextans-fix.sh` wires up the shared volume for you. This section exists for anyone running the CARE-SM toolkit's Docker image independently but planning to feed its output into a YARRRML/RML mapping step, so the same shared-volume pattern can be replicated by hand.

## Local implementation

If you are not interested in running our Docker image, you can install the Python module for local implementation. The PyPI-published `care-sm-toolkit` package predates this repo's model updates and is not currently compatible with it — install from source instead:

```
git clone https://github.com/wilkinsonlab/CARE-Semantic-Model-Version-2.git
cd CARE-Semantic-Model-Version-2/implementation/Toolkit
pip install .
```

Then, change the folder path inside the [trial.py](https://github.com/wilkinsonlab/CARE-Semantic-Model-Version-2/blob/main/implementation/Toolkit/trial.py) script. And run it:

```
python3 trial.py
```

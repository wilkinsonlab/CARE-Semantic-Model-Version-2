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
* All CSV files **MUST** be named according the data tags described at the CARE-SM glossary, documented at [CARE-SM implementation](https://github.com/CARE-SM/CARE-SM-Implementation/blob/main/CSV/README.md) E.g.: `Diagnosis.csv`, `Birthdate.csv`

 * All your CSV data content **MUST** be compatible with the CARE-SM glossary, documented at [CARE-SM implementation](https://github.com/CARE-SM/CARE-SM-Implementation/blob/main/CSV/README.md)


## Docker

There's a Docker-based implementation controlled via API (using FastAPI) that you can use for mounting this data transformation step as a part of your CARE-SM implementation.

You can edit the [docker-compose.yaml](https://github.com/CARE-SM/CARE-SM-Toolkit/blob/main/toolkit/API/docker-compose.yaml) to control the volume folder in order to pass your CSV-based patient data:

```yaml
version: "3.8"

services:
  api:
    image: pabloalarconm/care-sm-toolkit:1.1.0 # Check latest version
    ports:
      - "8000:8000"
    volumes:
      - ./location/of/your/data:/code/data
```

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

## Local implementation

If you are not interested in running our Docker image, you can install the Python module for local implementation. 

```
pip install care-sm-toolkit==1.1.0
```

Then, change the folder path inside the [trial.py](https://github.com/CARE-SM/CARE-SM-Toolkit/blob/main/trial.py) script. And run it:

```
python3 trial.py
```

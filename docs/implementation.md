# Implementation workflows

**Quick start**

To jump directly to the "just tell me what I have to do to make this work" using FAIR-in-a-box software, please [follow this link](https://github.com/ejp-rd-vp/FiaB/tree/main/CARE-SM-Fiab).

If you want to understand more deeply what you are doing, read on!

[CARE Semantic Model](https://github.com/CARE-SM/CARE-Semantic-Model) defines a set of clinical data elements used in the healthcare domain of knowledge. However, it doesn't specify a mechanism for bringing these to life. 

The proposed implementation workflows described in this repository (both Fiab and Standalone) uses a common set of technologies for the whole transformation of patient data into a RDF-representation.

1) **CSV**

      This workflow consumes CSV tables as the primary data source. Each row within these tables represents an individual observation. The required information for generating each module is defined within a set of columns. For instance, the diagnosis module requires several distinct columns, including those for patient identifier, diagnosis date, and the IRI used for disease definition. A predefined set of common column names is used to reference each specific clinical entries. These set of columns acts as a [data element glossary](https://github.com/CARE-SM/CARE-SM-Implementation/tree/main/CSV/README.md), templating which columns are required to be filled in every data element.

2) **YARRRML**

    These columns are referenced in an RDF-compliance template, which defines the structure of the resulting RDF shape. These templates are formulated in [YARRRML](https://rml.io/yarrrml/spec/), a versatile templating language capable of defining the RDF structure and uses the column names to reference the CSV data and create a complete RDF representation.


This implementation requires two main transformation steps:

1) **Data pre-validation and adaptation**

    After creating this CSV template with the patient data on it, this CSV template needs to be adapted to YARRRML template before performing RDF transformation. This modification add additional fields and automatically make certain translations that reduce the complexity and burden on the data provider. This translation is executed by a component called [CARE-SM Toolkit](https://care-sm.readthedocs.io/en/latest/toolkit.html#).

2) **Data transformation into RDF** 

    After the CSV template is curated using the CARE-SM Toolkit, it is fully compatible with the YARRRML template. These templates are then used as inputs to an RDFizer to produce RDF data.

## FAIR-in-a-box software

Born as a [European Joint Project on Rare Diseases (EJP-RD)](https://www.ejprarediseases.org/) initiative, a set of technologies and softwares have been created, capable of consuming data tables into RDF data representation. [FAIR-in-a-box](https://github.com/ejp-rd-vp/FiaB) has implemented a whole pipeline for patient-based data using CARE-SM. Same technologies can be used outside FAIR-in-a-box software in a standalone implementation.

FAIR-in-a-box solution is documented out of this repository, please [follow Fiab link](https://github.com/ejp-rd-vp/FiaB)

## Standalone implementation

From those who are not interested in using FAIR-in-a-box or interested in exploring every step in the workflow locally. You have the option to perform RDF transformations without relying on the FAIR-in-a-box solution. To support this process, we have developed Docker compose images that cover the entire transformation pipeline. The standalone implementation can be described as follows:

<p align="center"> 
  <img src="https://github.com/CARE-SM/CARE-SM-Implementation/blob/main/CARE-SM_workflow.png?raw=true"> 
<p align="center" ><b>Figure 1: Standalone CARE-SM implementation </b></p>

1) **CSV template creation:** First, a CSV data template is created using the CSV template defined by a [data element glossary](https://github.com/CARE-SM/CARE-SM-Implementation/tree/main/CSV/README.md) Rename your CSV file with one of the tagnames defined at the glossary. Eg.: "Diagnosis", "First_visit" or "Laboratory".

2) **Quality control by CARE-SM Toolkit**: CARE-SM Toolkit will transform all your tagged CSV files e.g.: `Diagnosis.csv` to the curated CSV template called `CARE.csv` (green boxes from Figure 1).  This step generates a much richer CSV file that is used by the YARRRML to do the final RDF transformation.

    Jump [here](https://care-sm.readthedocs.io/en/latest/toolkit.html#why-to-use-it) to know more in details about **CARE-SM Toolkit** how/why to use it.

3) **YARRRML template**: Alongside this standard CSV template, a YARRRML template defines the final RDF shape based on the CARE semantic model. This YARRRML template is provided [here](https://github.com/CARE-SM/CARE-SM-Implementation/tree/main/YARRRML/README.md) at this repository, so **there's no need for you to create it from scratch**.

    In case you're interested in more information about how we built our YARRRML template, check [EMbuilder YARRRML template builder](https://github.com/pabloalarconm/EMbuilder).

4) **Folder distribution:**
```bash
.
./data/
./data/CARE.csv  # CSV data file, explained above
./data/YARRRML_yarrrml.yaml # YARRRML template, explained above
./data/triples/  # Output RDF data ends up here, this folder will be automatically created.
./docker-compose.yaml # Docker image that will execute the transformation (step below)
```

5) **RDF transformation execution:**

You can use Docker compose to run the services (red box from Figure 1).

```yaml
version: "3"
services:
  yarrml-rdfizer:
    image: markw/yarrrml-rml-ejp:0.1.2
    container_name: yarrrml-rdfizer
    environment:
      # (nquads (default), trig, trix, jsonld, hdt, turtle)
      - SERIALIZATION=nquads
    ports:
      - "4567:4567"
    volumes:
      - ./data:/mnt/data
```

Once this services are running, call in your local browser this link: http://127.0.0.1:4567/CARE. The RDF file should be created at ./data/triples` folder.

# Example material

Explore practical resources to help you understand and implement the CARE-SM. 

**CSV – Patient Data (Before & After)**

Compare patient data representations **before and after** applying the CARE-SM Toolkit:  [CSV Data examples](https://github.com/CARE-SM/CARE-SM-Implementation/tree/main/CSV/)

**YARRRML Template**

Planning a standalone implementation?  Re-use our YARRRML template to generate RDF from CSV data: [CARE-SM YARRRML Template](https://github.com/CARE-SM/CARE-SM-Implementation/blob/main/YARRRML/CARE_yarrrml.yaml)

**RDF – Semantic Representation**

See the final RDF output of patient data modeled using CARE-SM: [RDF output data examples](https://github.com/CARE-SM/CARE-SM-Implementation/tree/main/RDF/)

**SPARQL – Query Examples and Validation**

Test and adapt SPARQL queries to explore your CARE-SM-based RDF data: [SPARQL queries folder](https://github.com/CARE-SM/CARE-SM-Implementation/tree/main/SPARQL)

We use SPARQL also for data validation. RDF-Quads is not well-managed with **ShEx** or **SHACL**. For this particular case, we propose SPARQL queries for this aspect. You can find them [here](https://github.com/CARE-SM/CARE-Semantic-Model/tree/main/schema).
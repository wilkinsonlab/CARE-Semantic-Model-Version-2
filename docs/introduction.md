# Introduction

<p align="center"> 
    <img src="https://github.com/CARE-SM/CARE-SM-docs/blob/main/docs/assets/care-sm.png?raw=true"width="400" height="400"> 
<p align="center" > </p> 
<p align="center"><b>Take CARE of your data! FAIRly!</b></p>
<hr>

Clinical And Registry Entries (CARE-SM) is a semantic data model designed to represent healthcare patient information by using knowledge graphs in the Resource Description Framework (RDF). This documentation aims to provide a comprehensive overview of CARE-SM, its origins, and the foundamental design principles that underlie its structure.

CARE-SM is built upon the [Semanticscience Integrated Ontology (SIO)](https://doi.org/10.1186/2041-1480-5-14) as its core structural schema. SIO is used to define every concept within the data model, utilizing upper-class classes and properties. This knowledge graph serves as a "scaffold" that holds every data element within its structure. By a combination of these instances defined by SIO, it becomes possible to represent every clinical entry comprehensively.

Moreover, each instance within CARE-SM is associated with a domain-specific ontological class from the [OBO Foundry](http://obofoundry.org/). For instance, the representation of patient birthdate is described at an upper-class level using the ontological term [SIO:attribute](http://semanticscience.org/resource/SIO_000614) and, at a domain-specific level, as [ncit:Birthdate](http://purl.obolibrary.org/obo/NCIT_C68615). This dual ontological characterization enhances data interoperability and precise semantic descriptions.

## Genesis of CARE-SM

CARE-SM is a more robust and matured representation of its precursor, the Common Data Element (CDE) semantic data model. The primary objective of its creation was to develop a semantic data model capable of representing [a set of common data elements for rare diseases registration](https://eu-rd-platform.jrc.ec.europa.eu/sites/default/files/CDS/EU_RD_Platform_CDS_Final.pdf) recommended by the European Commission Joint Research Centre. CARE-SM stands as the matured iteration of this CDE semantic model, extending its capabilities to encompass the representation of all data elements pertinent to patient registries and clinical encounters.

# Foundational design of CARE-SM

## Core Structure

CARE-SM is built upon the [Semanticscience Integrated Ontology (SIO)](https://doi.org/10.1186/2041-1480-5-14) as its core structural schema. SIO is used to define every concept within the data model, utilizing upper-class classes and properties. This knowledge graph serves as a "scaffold" that holds every data element within its structure (see Figure 1). By a combination of these instances defined by SIO, it becomes possible to represent every clinical entry comprehensively.

Moreover, each instance within CARE-SM is associated with a domain-specific ontological class from the [OBO Foundry](http://obofoundry.org/). For instance, the representation of patient birthdate is described at an upper-class level using the ontological term [SIO:attribute](http://semanticscience.org/resource/SIO_000614) and, at a domain-specific level, as [ncit:Birthdate](http://purl.obolibrary.org/obo/NCIT_C68615). This dual ontological characterization enhances data interoperability and precise semantic descriptions.

<p align="center">
    <a href="https://raw.githubusercontent.com/CARE-SM/CARE-Semantic-Model/main/images/CARE-SM-Core.drawio.png" target="_blank">
        <img src="https://raw.githubusercontent.com/CARE-SM/CARE-Semantic-Model/main/images/CARE-SM-Core.drawio.png">
    </a>
    <b>Figure 1: Core structure </b></p>

</p>


## Longitudinal records

To maintain a consistent core structure using CARE-SM, only one data element is modeled at a time. To support individual modeling, a metadata layer has been created around each data element representation (see Figure 2).

This metadata describes the context of each data element. The structure is preserved even when the primary objective of the data element is date/time information (e.g., symptom onset date or birthdate). This metadata layer connects all patient medical records in the form of a timeline, enabling the model to represent not only individual patient registry entries but also clinical encounters in a precise manner.

In addition to the patient timeline and temporal information, related records can be grouped under the same visit or event occurrence by connecting them through event nodes. These events provide a shared context among data elements, particularly in cases where multiple elements are related (e.g., condition/treatment scenarios or visit-based aggregated information). While the use of event nodes is optional, the model design fully supports this capability.

The metadata layer is implemented using named graphs, encapsulating each complete record within a dedicated named graph, as illustrated in Figures 2 and 3. The use of named graphs enhances query efficiency. By combining a common pattern across all data elements with the computational benefits of using both RDF-Quads and RDF-Triples, the model enables more efficient querying and retrieval of patient data using standardized query patterns.

<p align="center">
    <a href="https://raw.githubusercontent.com/CARE-SM/CARE-Semantic-Model/main/images/CARE-SM-Context.drawio.png">
        <img src="https://raw.githubusercontent.com/CARE-SM/CARE-Semantic-Model/main/images/CARE-SM-Context.drawio.png">
    </a>
    <b>Figure 2: Longitudinal record representation </b></p>
</p>

<p align="center">
    <a href="https://raw.githubusercontent.com/CARE-SM/CARE-Semantic-Model/main/images/CARE-SM-Timeline.drawio.png">
        <img src="https://raw.githubusercontent.com/CARE-SM/CARE-Semantic-Model/main/images/CARE-SM-Timeline.drawio.png">
    </a>
    <b>Figure 3: Timeline of a patient medical history </b></p>
</p>

**List of Data Elements**

- **Demographics:**
  - [Birthdate](https://care-sm.readthedocs.io/en/latest/data_elements.html#birthdate)
  - [Birthyear](https://care-sm.readthedocs.io/en/latest/data_elements.html#birthyear)
  - [Birthplace](https://care-sm.readthedocs.io/en/latest/data_elements.html#birthplace)
  - [Deathdate](https://care-sm.readthedocs.io/en/latest/data_elements.html#deathdate)
  - [Sex](https://care-sm.readthedocs.io/en/latest/data_elements.html#sex)

- **Participation and timeline:**
  - [First confirmed visit](https://care-sm.readthedocs.io/en/latest/data_elements.html#birthdate)
  - [Participation status](https://care-sm.readthedocs.io/en/latest/data_elements.html#participation-status)
  - [Symptoms onset](https://care-sm.readthedocs.io/en/latest/data_elements.html#symptoms-onset)

- **Conditions and findings:**
  - [Diagnosis](https://care-sm.readthedocs.io/en/latest/data_elements.html#diagnosis)
  - [Phenotype](https://care-sm.readthedocs.io/en/latest/data_elements.html#phenotype)

- **Clinical measurements:**
  - [Examination](https://care-sm.readthedocs.io/en/latest/data_elements.html#examination)
  - [Laboratory](https://care-sm.readthedocs.io/en/latest/data_elements.html#laboratory-measurement)
  - [Genetic](https://care-sm.readthedocs.io/en/latest/data_elements.html#genetic-testing)

- **Treatments and interventions:**
  - [Medication](https://care-sm.readthedocs.io/en/latest/data_elements.html#medication)
  - [Hospitalization](https://care-sm.readthedocs.io/en/latest/data_elements.html#hospitalization)
  - [Surgery](https://care-sm.readthedocs.io/en/latest/data_elements.html#surgical-intervention)

- **Patient-reported outcomes:**
  - [Questionnaire](https://care-sm.readthedocs.io/en/latest/data_elements.html#questionnaire)
  - [Disability](https://care-sm.readthedocs.io/en/latest/data_elements.html#disability)

- **Research samples:**
  - [Biobank](https://care-sm.readthedocs.io/en/latest/data_elements.html#biobank)
  - [Consent](https://care-sm.readthedocs.io/en/latest/data_elements.html#consent)
  - [Clinical trial](https://care-sm.readthedocs.io/en/latest/data_elements.html#clinical-trial)
  - [Cohort](https://care-sm.readthedocs.io/en/latest/data_elements.html#cohort)
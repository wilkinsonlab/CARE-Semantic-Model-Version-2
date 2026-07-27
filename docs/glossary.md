# CARE-SM CSV Glossary Documentation

CARE-SM implements a CSV template structure to populate patient registry information. This template consists of a defined set of columns used across different data model modules. Depending on the specific module, a subset of these columns may be required, optional, or not applicable.

## CSV template columns

The following table is the complete list of available columns:

| Name               | Datatype | Description |
|--------------------|----------|-------------|
| `model`            | Literal (string)   | Tag name used to identify the specific model to generate. |
| `pid`              | Literal (integer)  | Patient unique identifier. |
| `event_id`         | Literal (integer)  | Event-specific identifier used to contextualize several data elements under the same medical visit or encounter. |
| `value`            | Literal (string, number, or date)  | Lexical value of this data element. |
| `value_datatype`   | Literal (string)   | Additional metadata of the `value` column, using the [XML Schema Definition Language (XSD)](https://www.w3.org/TR/xmlschema11-1/). Expected datatype: `xsd:date`, `xsd:string`, `xsd:float`, `xsd:integer` or `xsd:boolean`.|
| `activity`         | IRI      | Full conceptual IRI describing a specific process associated with this data element, such as a clinical method or route of administration. |
| `unit`             | IRI      | Full conceptual IRI describing the data element’s unit of measurement. |
| `input`            | IRI      | Full conceptual IRI defining any input associated with the clinical procedure, such as a medication used or a related tissue sample. |
| `target`           | IRI      | Full conceptual IRI defining any target associated with the clinical procedure, such as an anatomical structure or a molecule. |
| `protocol_id`      | IRI      | Full conceptual IRI specifying any protocol or document that contextualizes the reported data element. |
| `duration_value`    | Literal (ISO 8601 duration      | Duration value, for instance, P10Y . it will be datatyped as `xsd:duration`. |
| `duration_startdate`   | Literal (ISO 8601 date)      | Start date of the duration time interval. |
| `duration_enddate`    | Literal (ISO 8601 date)     | End date of the duration interval.|
| `frequency_type`   | IRI      | Full conceptual IRI defining the frequency type of the associated clinical procedure. |
| `frequency_value`  | Literal (string)  | Numerical frequency value; combined with `frequency_type`, it defines the full frequency (e.g., “2 times per month”). |
| `startdate`        | Literal (ISO 8601 date)    | Start date of the data registration or time instant when the observation was taken. If identical to `value`, it is not required. |
| `enddate`          | Literal (ISO 8601 date)    | End date of the data registration, if it 's different from `startdate`. No need to add `enddate` if its a time point, only is required. |
| `age`              | Literal (integer)  | Age of the patient at the time of observation. |
| `comments`         | Literal (string)   | Human-readable comments or descriptions related to this data element. |
| `organisation`     | IRI      | IRI used to define the organisation identifier. |
| `identifier_value` | Literal (string)   | Lexical identifier value for a specific attribute, e.g. a sequence variant's HGVS notation. Rows sharing the same `pid` + `event_id` attach multiple such attributes to one shared record. |
| `input_value`      | Literal (string)   | Literal value carried by the input, when `input`'s type is a fixed constant and doesn't itself vary per record (e.g. a consent form's filename). |
| `attribute_type`   | IRI      | Full conceptual IRI for a per-record attribute annotation, e.g. sex, participation status, or the examined finding. Direct, model-specific meaning -- see the glossary entry for the model in question. |
| `output_type`      | IRI      | Full conceptual IRI classifying the output/record itself, e.g. the type of medication record or consent statement, when that classification varies per record rather than being fixed for the whole model. |
| `output_id`        | IRI      | Full IRI identifying the record's own output, e.g. a biobank collection or country-of-birth code, when the output itself needs an external identifier. |
| `cause_id`         | IRI      | Full conceptual IRI for a causally-related annotation, e.g. cause of death. |

## CSV template creation

This guide explains how to structure, populate, and utilize CSV files for patient data in CARE-SM.

1. **Create the CSV File**  
   
   This document would only allow a set of concrete columns names:
   - `model`, `pid`, `event_id`, `value`, `age`, `value_datatype`, `activity`, `unit`, `input`, `target`, `protocol_id`, `frequency_type`, `frequency_value`, `startdate`, `enddate`, `comments`, `organisation`, `duration_value`, `duration_startdate`, `duration_enddate`, `identifier_value`, `input_value`, `attribute_type`, `output_type`, `output_id`, `cause_id`.

   *Example:*
   ```text
   model,pid,event_id,value,age,value_datatype,activity,unit,input,target,protocol_id,frequency_type,frequency_value,startdate,enddate,comments,organisation,duration_value,duration_startdate,duration_enddate,identifier_value,input_value,attribute_type,output_type,output_id,cause_id
   ,,,,,,,,,,,,,,,,,,,,,,,,,,
   ```
2. **Populate Data**  
   Each data entry needs specific fields (not all fields are mandatory). See the glossary below for details.

    *Example:*
    ```text
    model,pid,event_id,target,value,value_datatype,startdate
    Diagnosis,30056,,http://www.orpha.net/ORDO/Orphanet_93552,true,xsd:boolean,2006-01-19
    ```

    For more examples, refer to the [`exemplar_data`](https://github.com/wilkinsonlab/CARE-Semantic-Model-Version-2/tree/main/implementation/CSV) folder.

## Data Element Glossary

**Legend:**
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) This column is **MANDATORY** for this case.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) This column is **OPTIONAL**. for this case
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) This column is **NOT APPLICABLE** for this case.
<hr>

(birthdate_glossary)=
### Birthdate

**This data element can be queried (in an aggregated and anonymized manner) through the Beacon API developed for CARE-SM. For more information, click [here](https://github.com/CARE-SM/beaconAPI4CARESM)**

- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **model**: Birthdate
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **pid**: Patient Unique Identifier.
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **value**: ISO 8601-formatted birthdate.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **value_datatype**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **activity**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **unit**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **target**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_value**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **startdate**: ISO 8601-formatted start date of the data registration., could be the same of the `value`
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **enddate**: ISO 8601-formatted end date of the data registration in case it is different from `startdate`.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **age**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **comments**: Additional human-readable comments.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **event_id**: Visit occurrence identifier.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **organisation**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **protocol_id**: IRI reference to any associated protocol.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_startdate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_enddate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **identifier_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **attribute_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_id**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **cause_id**:
<hr>

(birthyear_glossary)=
### Birthyear

**This data element can be queried (in an aggregated and anonymized manner) through the Beacon API developed for CARE-SM. For more information, click [here](https://github.com/CARE-SM/beaconAPI4CARESM)**

- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **model**: Birthdate
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **pid**: Patient Unique Identifier.
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **value**: The year (YYYY) in which a person was born.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **value_datatype**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **activity**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **unit**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **target**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_value**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **startdate**: ISO 8601-formatted start date of the data registration.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **enddate**: ISO 8601-formatted end date of the data registration in case it is different from `startdate`.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **age**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **comments**: Additional human-readable comments.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **event_id**: Visit occurrence identifier.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **organisation**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **protocol_id**: IRI reference to any associated protocol.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_startdate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_enddate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **identifier_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **attribute_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_id**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **cause_id**:
<hr>

(country_glossary)=
### Birthplace

**This data element can be queried (in an aggregated and anonymized manner) through the Beacon API developed for CARE-SM. For more information, click [here](https://github.com/CARE-SM/beaconAPI4CARESM)**

- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **model**: Birthplace
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **pid**: Patient Unique Identifier.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **value_datatype**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **activity**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **unit**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **target**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_value**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **startdate**: ISO 8601-formatted start date of the data registration.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **enddate**: ISO 8601-formatted end date of the data registration in case it is different from `startdate`.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **age**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **comments**: Additional human-readable comments.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **event_id**: Visit occurrence identifier.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **organisation**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **protocol_id**: IRI reference to any associated protocol.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_startdate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_enddate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **identifier_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **attribute_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_type**:
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **output_id**: Full IRI used as the annotation code for the country of birth.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **cause_id**:
<hr>

(deathdate_glossary)=
### Deathdate

- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **model**: Deathdate
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **pid**: Patient Unique Identifier.
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **value**: ISO 8601-formatted date of death (not date time)
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **value_datatype**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **activity**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **unit**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **target**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_value**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **startdate**: ISO 8601-formatted start date of the data registration., could be the same of the `value`
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **enddate**: ISO 8601-formatted end date of the data registration in case it is different from `startdate`.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **age**: The patient’s age at the time the observation was taken.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **comments**: Additional human-readable comments.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **event_id**: Visit occurrence identifier.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **organisation**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **protocol_id**: IRI reference to any associated protocol.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_startdate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_enddate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **identifier_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **attribute_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_id**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **cause_id**: Full concept IRI for the cause of death, when known.
<hr>

(sex_glossary)=
### Sex

**This data element can be queried (in an aggregated and anonymized manner) through the Beacon API developed for CARE-SM. For more information, click [here](https://github.com/CARE-SM/beaconAPI4CARESM)**

- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **model**: Sex
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **pid**: Patient Unique Identifier.
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **value**: Human-readable label of the concept IRI used for `attribute_type`.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **value_datatype**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **activity**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **unit**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **target**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_value**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **startdate**: ISO 8601-formatted start date of the data registration.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **enddate**: ISO 8601-formatted end date of the data registration in case it is different from `startdate`.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **age**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **comments**: Additional human-readable comments.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **event_id**: Visit occurrence identifier.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **organisation**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **protocol_id**: IRI reference to any associated protocol.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_startdate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_enddate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **identifier_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input_value**:
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **attribute_type**: Full concept IRI for the patient sex annotation.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_id**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **cause_id**:

** If you are representing CARE-SM with the **OBO Foundry**, use the one of the following **NCIT terms**:
  - http://purl.obolibrary.org/obo/NCIT_C16576 (Female)
  - http://purl.obolibrary.org/obo/NCIT_C20197 (Male)
  - http://purl.obolibrary.org/obo/NCIT_C124294 (Undetermined)
  - http://purl.obolibrary.org/obo/NCIT_C17998 (Unknown)
<hr>

(first-visit_glossary)=
### First Confirmed Visit

- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **model**: First_visit
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **pid**: Patient Unique Identifier.
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **value**: ISO 8601-formatted date of first confirmed visit.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **value_datatype**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **activity**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **unit**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **target**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_value**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **startdate**: ISO 8601-formatted start date of the data registration., could be the same of the `value`
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **enddate**: ISO 8601-formatted end date of the data registration in case it is different from `startdate`.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **age**: The patient’s age at the time the observation was taken.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **comments**: Additional human-readable comments.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **event_id**: Visit occurrence identifier.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **organisation**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **protocol_id**: IRI reference to any associated protocol.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_startdate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_enddate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **identifier_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **attribute_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_id**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **cause_id**:
<hr>

(status_glossary)=
### Participation status

- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **model**: Status
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **pid**: Patient Unique Identifier.
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **value**: Human-readable label of the concept IRI used for `attribute_type`.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **value_datatype**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **activity**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **unit**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **target**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_value**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **startdate**: ISO 8601-formatted start date of the data registration.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **enddate**: ISO 8601-formatted end date of the data registration in case it is different from `startdate`.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **age**: The patient’s age at the time the observation was taken.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **comments**: Additional human-readable comments.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **event_id**: Visit occurrence identifier.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **organisation**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **protocol_id**: IRI reference to any associated protocol.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_startdate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_enddate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **identifier_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input_value**:
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **attribute_type**: Full concept IRI for the participation status annotation.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_id**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **cause_id**:

** If you are representing CARE-SM with the **OBO Foundry**, use the one of the following **NCIT terms**:
  - http://purl.obolibrary.org/obo/NCIT_C37987 (Alive)
  - http://purl.obolibrary.org/obo/NCIT_C90387 (Found Dead)
  - http://purl.obolibrary.org/obo/NCIT_C70740 (Subject Lost to Follow Up)
  - http://purl.obolibrary.org/obo/NCIT_C124784 (Refusal To Participate)
<hr>

(symptoms_onset_glossary)=
### Symptoms onset

**This data element can be queried (in an aggregated and anonymized manner) through the Beacon API developed for CARE-SM. For more information, click [here](https://github.com/CARE-SM/beaconAPI4CARESM)**

- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **model**: Symptoms_onset
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **pid**: Patient Unique Identifier.
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **value**: One of the following:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **value_datatype**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **activity**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **unit**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **target**: Full concept IRI for the particular symptom annotation.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_value**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **startdate**: ISO 8601-formatted start date of registration
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **enddate**: ISO 8601-formatted end date of registration in case it is different from `startdate`.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **age**: The patient’s age at the time the observation was taken.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **comments**: Additional human-readable comments.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **event_id**: Visit occurrence identifier.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **organisation**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **protocol_id**: IRI reference to any associated protocol.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_startdate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_enddate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **identifier_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **attribute_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_id**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **cause_id**:

  * Age of the symptoms onset.
  * ISO 8601-formatted date of the symptoms occurrence.
<hr>

(phenotype_glossary)=
### Phenotype

**This data element can be queried (in an aggregated and anonymized manner) through the Beacon API developed for CARE-SM. For more information, click [here](https://github.com/CARE-SM/beaconAPI4CARESM)**

- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **model**: Phenotype
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **pid**: Patient Unique Identifier.
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **value**: Boolean result of the observation -- `true` if the phenotype was confirmed present, `false` if it was explicitly tested for and confirmed absent.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **value_datatype**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **unit**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input**:
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **target**: Full concept IRI for the phenotype being tested (e.g. an HPO code). Together with `value`, forms the complete assertion: "was this phenotype observed?"
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **duration_value**: ISO 8601 duration value of the phenotype duration interval, for instance, P10Y.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **duration_startdate**: ISO 8601 start date of the phenotype duration interval.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **duration_enddate**: ISO 8601 start date of the phenotype duration interval.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_value**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **startdate**: ISO 8601-formatted start date of the data registration.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **enddate**: ISO 8601-formatted end date of the data registration in case it is different from `startdate`.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **age**: The patient’s age at the time the observation was taken.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **comments**: Additional human-readable comments.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **event_id**: Visit occurrence identifier.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **organisation**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **protocol_id**: IRI reference to any associated protocol.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **activity**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **identifier_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input_value**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **attribute_type**: Only present when `value` is `true`: mirrors `target`'s phenotype code, so `Attribute_` exists only for a confirmed-present finding.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_id**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **cause_id**:
<hr>

(diagnosis_glossary)=
### Diagnosis

**This data element can be queried (in an aggregated and anonymized manner) through the Beacon API developed for CARE-SM. For more information, click [here](https://github.com/CARE-SM/beaconAPI4CARESM)**

- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **model**: Diagnosis
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **pid**: Patient Unique Identifier.
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **value**: Boolean result of the observation -- `true` if the diagnosis was confirmed, `false` if it was explicitly tested for and confirmed absent.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **value_datatype**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **activity**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **unit**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **input**: Structural schema placeholder only, never populated via CSV -- see the "Note on `Process_ --has input--> Input_`" in the Diagnosis diagram for why.
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **target**: Full concept IRI for the disease or disorder being tested for (e.g. an ORPHA code). Together with `value`, forms the complete assertion: "was this diagnosis confirmed?"
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_value**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **startdate**: ISO 8601-formatted start date of the data registration.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **enddate**: ISO 8601-formatted end date of the data registration in case it is different from `startdate`.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **age**: The patient’s age at the time the observation was taken.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **comments**: Additional human-readable comments.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **event_id**: Visit occurrence identifier.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **organisation**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **protocol_id**: IRI reference to any associated protocol.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **duration_value**: ISO 8601 duration value of the diagnosis duration interval, for instance, P10Y.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **duration_startdate**: ISO 8601 start date of the diagnosis duration interval.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **duration_enddate**: ISO 8601 start date of the diagnosis duration interval.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **identifier_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input_value**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **attribute_type**: Only present when `value` is `true`: mirrors `target`'s diagnosis code, so `Attribute_` exists only for a confirmed diagnosis.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_id**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **cause_id**:
<hr>

(examination_glossary)=
### Examination

- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **model**: Examination
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **pid**: Patient Unique Identifier.
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **value**: Resulting value from this examination.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **value_datatype**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **activity**: Full concept IRI for the specific method activity.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **unit**: Full concept IRI for the unit of measurement.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **target**: Full concept IRI for the anatomic structure examined.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_value**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **startdate**: ISO 8601-formatted start date of the data registration.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **enddate**: ISO 8601-formatted end date of the data registration in case it is different from `startdate`.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **age**: The patient’s age at the time the observation was taken.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **comments**: Additional human-readable comments.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **event_id**: Visit occurrence identifier.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **organisation**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **protocol_id**: URL reference to any protocol.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_startdate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_enddate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **identifier_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input_value**:
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **attribute_type**: Full concept IRI for the patient attribute/finding examined.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_id**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **cause_id**:

** If you are representing CARE-SM with the **OBO Foundry**, this is some example using **NCIT terms**:
  - http://purl.obolibrary.org/obo/NCIT_C25208 (Weight)
  - http://purl.obolibrary.org/obo/NCIT_C25347 (Height)
  - http://purl.obolibrary.org/obo/NCIT_C99524 (Left Ventricular Ejection Fraction)
  - http://purl.obolibrary.org/obo/NCIT_C16358 (Body Mass Index)
<hr>

(laboratory_glossary)=
### Laboratory

- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **model**: Laboratory
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **pid**: Patient Unique Identifier.
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **value**: value of the laboratory measurement.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **value_datatype**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **activity**: Full concept IRI for the specific method annotation.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **unit**: Full concept IRI for the unit of measurement.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **input**: Full concept IRI for the substance sample analysed.
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **target**: Full concept IRI for the compound measured in the sample.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_value**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **startdate**: ISO 8601-formatted start date of the data registration.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **enddate**: ISO 8601-formatted end date of the data registration in case it is different from `startdate`.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **age**: The patient’s age at the time the observation was taken.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **comments**: Additional human-readable comments.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **event_id**: Visit occurrence identifier.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **organisation**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **protocol_id**: URL reference to a protocol.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_startdate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_enddate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **identifier_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **attribute_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_id**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **cause_id**:
<hr>

(genotype_glossary)=
### Genetic

**This data element can be queried (in an aggregated and anonymized manner) through the Beacon API developed for CARE-SM. For more information, click [here](https://github.com/CARE-SM/beaconAPI4CARESM)**

- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **model**: Genetic
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **pid**: Patient Unique Identifier.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **value_datatype**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **activity**: Full concept IRI for the specific method.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **unit**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **input**: Full concept IRI for the type of substance sample analysed.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **target**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_value**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **startdate**: ISO 8601-formatted start date of the data registration.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **enddate**: ISO 8601-formatted end date of the data registration in case it is different from `startdate`.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **age**: The patient’s age at the time the observation was taken.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **comments**: Additional human-readable comments.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **event_id**: Visit occurrence identifier.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **organisation**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **protocol_id**: IRI reference to any associated protocol.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_startdate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_enddate**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **identifier_value**: Lexical notation for this specific variant (e.g. HGVS), e.g. `NC_000023.9:g.32317682G>A`. One row per variant: rows sharing the same `pid` + `event_id` attach multiple variants to the same report -- see `docs/migration.md`.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input_value**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **attribute_type**: Full concept IRI for the zygosity of this specific variant, e.g. heterozygosity or homozygosity.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_id**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **cause_id**:
<hr>

(medication_glossary)=
### Medication

- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **model**: Medication
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **pid**: Patient Unique Identifier.
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **value**: Prescribed or Administrated dose value.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **value_datatype**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **activity**: Full concept IRI for the route of administration.
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **unit**: Full concept IRI for the unit of measurement.
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **input**: Full concept IRI identifying the specific drug administered or prescribed. `Input_`'s type is always the fixed "Drug Product Component" constant; this is the drug's own identity.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **target**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **frequency_type**: Full concept IRI for the administered/prescribed frequency annotation.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **frequency_value**: frequency value prescribe to the patient
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **startdate**: ISO 8601-formatted start date of the data registration.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **enddate**: ISO 8601-formatted end date of the data registration in case it is different from `startdate`.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **age**: The patient’s age at the time the observation was taken.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **comments**: Additional human-readable comments.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **event_id**: Visit occurrence identifier.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **organisation**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **protocol_id**: URL reference to a protocol.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_startdate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_enddate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **identifier_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **attribute_type**:
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **output_type**: Full concept IRI for the type of medication record: Dose Administered or Prescribed Dose.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_id**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **cause_id**:

** If you are representing CARE-SM with the **OBO Foundry**, use the one of the following **NCIT terms**:
  - http://purl.obolibrary.org/obo/NCIT_C167190 (Dose Administered)
  - http://purl.obolibrary.org/obo/NCIT_C198143 (Prescribed Dose)
<hr>

(hospitalization_glossary)=
### Hospitalization

- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **model**: Hospitalization
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **pid**: Patient Unique Identifier.
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **value**: Generic optional output value, for future use -- no fixed meaning defined yet for hospitalization outcomes.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **value_datatype**:
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **activity**: Full concept IRI for the specific activity performed during the hospitalization.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **target**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_value**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **startdate**: ISO 8601-formatted start date of the data registration.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **enddate**: ISO 8601-formatted end date of the data registration in case it is different from `startdate`.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **age**: The patient’s age at the time the observation was taken.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **comments**: Additional human-readable comments.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **event_id**: Visit occurrence identifier.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **organisation**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **protocol_id**: URL reference to a protocol.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **unit**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **duration_value**: ISO 8601 duration value of the hospitalization duration interval, for instance, P10Y.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **duration_startdate**: ISO 8601 start date of the hospitalization duration interval.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **duration_enddate**: ISO 8601 start date of the hospitalization duration interval.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **identifier_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **attribute_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_id**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **cause_id**:
<hr>

(surgery_glossary)=
### Surgery

- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **model**: Surgery
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **pid**: Patient Unique Identifier.
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **value**: Generic optional output value, for future use -- no fixed meaning defined yet for surgical outcomes.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **value_datatype**:
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **activity**: Full concept IRI for the specific activity performed during the surgery.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **unit**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **target**: Full concept IRI for the anatomic structure that participates in the surgical intervention.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_value**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **startdate**: ISO 8601-formatted start date of the data registration.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **enddate**: ISO 8601-formatted end date of the data registration in case it is different from `startdate`.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **age**: The patient’s age at the time the observation was taken.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **comments**: Additional human-readable comments.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **event_id**: Visit occurrence identifier.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **organisation**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **protocol_id**: URL reference to a protocol.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **duration_value**: ISO 8601 duration value of the surgery duration interval, for instance, P10Y.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **duration_startdate**: ISO 8601 start date of the surgery duration interval.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **duration_enddate**: ISO 8601 start date of the surgery duration interval.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **identifier_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **attribute_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_id**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **cause_id**:
<hr>

(questionnaire_glossary)=
### Questionnaire

- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **model**: Questionnaire
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **pid**: Patient Unique Identifier.
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **value**: Score/value of the patient reported response.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **value_datatype**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **activity**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **unit**:
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **input**: Full concept IRI for the clinical question or statement to report.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **target**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_value**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **startdate**: ISO 8601-formatted start date of the data registration.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **enddate**: ISO 8601-formatted end date of the data registration in case it is different from `startdate`.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **age**: The patient’s age at the time the observation was taken.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **comments**: Additional human-readable comments.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **event_id**: Visit occurrence identifier.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **organisation**:
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **protocol_id**: Full concept IRI for the assessment tool or Patient Reported Outcome Measures specification.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_startdate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_enddate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **identifier_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **attribute_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_id**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **cause_id**:
<hr>

(functional_assessment_glossary)=
### Functional Assessment

- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **model**: Functional_Assessment
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **pid**: Patient Unique Identifier.
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **value**: Score/value of the patient reported response.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **value_datatype**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **activity**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **unit**: Full concept IRI for the unit of measurement.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **target**: Full concept IRI for the specific functional assessment instrument/metric used, e.g. WHODAS 2.0 or the 10-Metre Walk Test.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **duration_value**: ISO 8601 duration value of the functional assessment duration interval, for instance, P10Y.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **duration_startdate**: ISO 8601 start date of the functional assessment duration interval.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **duration_enddate**: ISO 8601 start date of the functional assessment duration interval.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_value**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **startdate**: ISO 8601-formatted start date of the data registration.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **enddate**: ISO 8601-formatted end date of the data registration in case it is different from `startdate`.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **age**: The patient’s age at the time the observation was taken.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **comments**: Additional human-readable comments.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **event_id**: Visit occurrence identifier.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **organisation**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **protocol_id**: Full concept IRI for the exact protocol or procedure used to administer the instrument (distinct from `target`, the instrument/metric itself) -- optional but recommended.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **identifier_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **attribute_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_id**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **cause_id**:
<hr>

(biobank_glossary)=
### Biobank

- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **model**: Biobank
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **pid**: Patient Unique Identifier.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **value_datatype**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **activity**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **unit**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **input**: Full concept IRI for the type of tissue/sample collected during the sampling process.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **target**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_value**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **startdate**: ISO 8601-formatted start date of the data registration.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **enddate**: ISO 8601-formatted end date of the data registration in case it is different from `startdate`.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **age**: The patient’s age at the time the observation was taken.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **comments**: Additional human-readable comments.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **event_id**: Visit occurrence identifier.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **organisation**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **protocol_id**: IRI reference to any associated protocol.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_startdate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_enddate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **identifier_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **attribute_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_type**:
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **output_id**: Full IRI identifying the biobank collection.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **cause_id**:
<hr>

(consent_glossary)=
### Consent

- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **model**: Consent
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **pid**: Patient Unique Identifier.
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **value**: some label describing consent outcome
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **value_datatype**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **activity**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **unit**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **input**: Structural only -- `Input_`'s type is always the fixed "Consent Form" constant; see `input_value` for the actual filename.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **target**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_value**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **startdate**: ISO 8601-formatted start date of the data registration.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **enddate**: ISO 8601-formatted end date of the data registration in case it is different from `startdate`.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **age**: The patient’s age at the time the observation was taken.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **comments**: Additional human-readable comments.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **event_id**: Visit occurrence identifier.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **organisation**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **protocol_id**: IRI reference to any associated protocol.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_startdate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_enddate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **identifier_value**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **input_value**: Consent form filename and version, e.g. `consent_form_v2.1.pdf` (not a URL).
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **attribute_type**:
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **output_type**: Full concept IRI describing the consent statement, e.g. Data Use Permission or willingness to be contacted.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_id**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **cause_id**:

** If you are representing CARE-SM with the **OBO Foundry**, use the one of the following **DUO and OBIB terms**:
  - http://purl.obolibrary.org/obo/DUO_0000001 (Data Use Permission)
  - http://purl.obolibrary.org/obo/OBIB_0000488 (willingness to be contacted)
<hr>

(clinical_trial_glossary)=
### Clinical trial

- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **model**: Clinical_trial
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **pid**: Patient Unique Identifier.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **value_datatype**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **unit**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input**:
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **target**: Full concept IRI for the genetic or disease condition.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_value**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **startdate**: ISO 8601-formatted start date of the data registration.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **enddate**: ISO 8601-formatted end date of the data registration in case it is different from `startdate`.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **age**: The patient’s age at the time the observation was taken.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **comments**: Additional human-readable comments.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **event_id**: Visit occurrence identifier.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **organisation**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **protocol_id**: IRI reference to any associated protocol.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **activity**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_startdate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_enddate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **identifier_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **attribute_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_type**:
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **output_id**: Full IRI identifying the clinical trial.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **cause_id**:

- ![](https://placehold.co/15x15/1589F0/1589F0..png) **value**: Study report name/identifier.
<hr>

(cohort_glossary)=
### Cohort

- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **model**: Cohort
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **pid**: Patient Unique Identifier.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **value_datatype**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **unit**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input**:
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **target**: Full concept IRI for the genetic or disease condition.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **frequency_value**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **startdate**: ISO 8601-formatted start date of the data registration.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **enddate**: ISO 8601-formatted end date of the data registration in case it is different from `startdate`.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **age**: The patient’s age at the time the observation was taken.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **comments**: Additional human-readable comments.
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **event_id**: Visit occurrence identifier.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **organisation**:
- ![](https://placehold.jp/12/d7a028/000000/20x20.png?text=O) **protocol_id**: IRI reference to any associated protocol.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **activity**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_startdate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **duration_enddate**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **identifier_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **input_value**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **attribute_type**:
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **output_type**:
- ![](https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M) **output_id**: Full IRI identifying the cohort.
- ![](https://placehold.jp/12/a29e96/000000/20x20.png?text=N) **cause_id**:

- ![](https://placehold.co/15x15/1589F0/1589F0..png) **value**: Study report name/identifier.
<hr>


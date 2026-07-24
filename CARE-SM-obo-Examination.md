# CARE-SM OBO Model — Examination

Mermaid transcription of [`CARE-SM-obo-Examination.drawio.png`](https://raw.githubusercontent.com/CARE-SM/CARE-Semantic-Model/main/images/obo/CARE-SM-obo-Examination.drawio.png).

**Legend**
- `sio:` = http://semanticscience.org/resource/
- `obo:` = http://purl.obolibrary.org/obo/
- Diamond, orange border = Used Instance
- Rectangle, green border = Class
- Rectangle, blue border = Data value

Note: "Unused Instance" nodes (grey diamonds) from the source diagram are omitted as uninformative.

```mermaid
flowchart TD
    classDef usedInstance fill:#ffffff,stroke:#d79b00,stroke-width:7px,color:#333
    classDef classNode fill:#ffffff,stroke:#82b366,stroke-width:7px,color:#333
    classDef dataValue fill:#ffffff,stroke:#6c8ebf,stroke-width:7px,color:#333
    linkStyle default stroke:#555,stroke-width:5px

    %% Instances
    ID_{{ID_}}:::usedInstance
    Individual_{{Individual_}}:::usedInstance
    Role_{{Role_}}:::usedInstance
    Process_{{Process_}}:::usedInstance
    Specific_method_{{Specific_method_}}:::usedInstance
    Target_{{Target_}}:::usedInstance
    URIProtocol{{"URI for the protocol"}}:::usedInstance
    Output_{{Output_}}:::usedInstance
    Attribute_{{Attribute_}}:::usedInstance
    Unit_{{Unit_}}:::usedInstance

    %% Classes
    SIO_000115["sio:SIO_000115<br/>(identifier)"]:::classNode
    SIO_000498["sio:SIO_000498<br/>(person)"]:::classNode
    OBI_0000093["obo:OBI_0000093<br/>(patient role)"]:::classNode
    SIO_000016["sio:SIO_000016<br/>(role)"]:::classNode
    SIO_000006["sio:SIO_000006<br/>(process)"]:::classNode
    MAXO_0000487["obo:MAXO_0000487<br/>(clinical assessment)"]:::classNode
    NCIT_C16536["IRI for the specific<br/>measurement method, e.g.:<br/>obo:NCIT_C16536 (Electrophoresis)"]:::classNode
    AnatomicStructureIRI["IRI for the anatomic structure<br/>measured, e.g.:<br/>obo:NCIT_C12419 (Head)"]:::classNode
    SIO_000015["sio:SIO_000015<br/>(information content entity)"]:::classNode
    OBI_0000272["obo:OBI_0000272<br/>(protocol)"]:::classNode
    SIO_000090["sio:SIO_000090<br/>(specification)"]:::classNode
    AnnotationCodeIRI["IRI for the annotation code of the<br/>examination, e.g.:<br/>obo:NCIT_C25208 (Weight)<br/>obo:NCIT_C25347 (Height)<br/>obo:NCIT_C99524 (Left Ventricular<br/>Ejection Fraction)<br/>obo:NCIT_C16358 (Body Mass Index)"]:::classNode
    SIO_000614["sio:SIO_000614<br/>(attribute)"]:::classNode
    NCIT_C70856["obo:NCIT_C70856<br/>(Observation Result)"]:::classNode
    UnitMeasurementIRI["IRI for unit of measurement"]:::classNode
    SIO_000074["sio:SIO_000074<br/>(unit of measurement)"]:::classNode

    %% Data values
    IndividualID["individual ID"]:::dataValue
    Comments["comments"]:::dataValue
    ExamMeasurementValue["Examination<br/>measurement value"]:::dataValue

    %% Real edges (indices 0-29)
    ID_ -->|"sio:SIO_000300 (has value)"| IndividualID
    ID_ -->|"rdf:type"| SIO_000115
    ID_ -->|"sio:SIO_000020 (denotes)"| Role_

    Individual_ -->|"rdf:type"| SIO_000498
    Individual_ -->|"sio:SIO_000228 (has role)"| Role_

    Role_ -->|"rdf:type"| OBI_0000093
    Role_ -->|"rdf:type"| SIO_000016
    Role_ -->|"sio:SIO_000356 (is realized in)"| Process_

    Process_ -->|"rdf:type"| SIO_000006
    Process_ -->|"rdf:type"| MAXO_0000487
    Process_ -->|"rdfs:comment"| Comments
    Process_ -->|"sio:SIO_000028 (has part)"| Specific_method_
    Process_ -->|"sio:SIO_000291 (has target)"| Target_
    Process_ -->|"sio:SIO_000339 (is specified by)"| URIProtocol
    Process_ -->|"sio:SIO_000229 (has output)"| Output_

    Specific_method_ -->|"rdf:type"| NCIT_C16536
    Specific_method_ -->|"rdf:type"| SIO_000006

    Target_ -->|"rdf:type"| AnatomicStructureIRI
    Target_ -->|"rdf:type"| SIO_000015

    URIProtocol -->|"rdf:type"| OBI_0000272
    URIProtocol -->|"rdf:type"| SIO_000090

    Output_ -->|"sio:SIO_000628 (refers to)"| Attribute_
    Output_ -->|"sio:SIO_000221 (has unit)"| Unit_
    Output_ -->|"rdf:type"| NCIT_C70856
    Output_ -->|"rdf:type"| SIO_000015
    Output_ -->|"sio:SIO_000300 (has value)"| ExamMeasurementValue

    Attribute_ -->|"rdf:type"| AnnotationCodeIRI
    Attribute_ -->|"rdf:type"| SIO_000614

    Unit_ -->|"rdf:type"| UnitMeasurementIRI
    Unit_ -->|"rdf:type"| SIO_000074

    %% Invisible layout-only chains (indices 30-40, hidden below) force siblings into one column
    IndividualID ~~~ SIO_000115
    OBI_0000093 ~~~ SIO_000016
    SIO_000006 ~~~ MAXO_0000487 ~~~ Comments
    NCIT_C16536 ~~~ SIO_000006
    AnatomicStructureIRI ~~~ SIO_000015
    OBI_0000272 ~~~ SIO_000090
    NCIT_C70856 ~~~ SIO_000015 ~~~ ExamMeasurementValue
    AnnotationCodeIRI ~~~ SIO_000614
    UnitMeasurementIRI ~~~ SIO_000074

    linkStyle 30,31,32,33,34,35,36,37,38,39,40 stroke:none
```

# CARE-SM OBO Model — Medication

Mermaid transcription of [`CARE-SM-obo-Medication.drawio.png`](https://raw.githubusercontent.com/CARE-SM/CARE-Semantic-Model/main/images/obo/CARE-SM-obo-Medication.drawio.png).

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
    classDef classNode fill:transparent,stroke:#b9c9b4,stroke-width:1.5px,color:#888,font-size:11px
    classDef dataValue fill:#ffffff,stroke:#6c8ebf,stroke-width:7px,color:#333
    linkStyle default stroke:#555,stroke-width:5px

    %% Instances
    ID_{{ID_}}:::usedInstance
    Individual_{{Individual_}}:::usedInstance
    Role_{{Role_}}:::usedInstance
    Process_{{Process_}}:::usedInstance
    Specific_method_{{Specific_method_}}:::usedInstance
    URIDrugIdentifier{{"URI for drug identifier"}}:::usedInstance
    Frequency_{{Frequency_}}:::usedInstance
    URITreatmentPlan{{"URI for the treatment plan"}}:::usedInstance
    Output_{{Output_}}:::usedInstance
    Unit_{{Unit_}}:::usedInstance

    %% Classes
    SIO_000115["sio:SIO_000115<br/>(identifier)"]:::classNode
    SIO_000498["sio:SIO_000498<br/>(person)"]:::classNode
    OBI_0000093["obo:OBI_0000093<br/>(patient role)"]:::classNode
    SIO_000016["sio:SIO_000016<br/>(role)"]:::classNode
    SIO_000006["sio:SIO_000006<br/>(process)"]:::classNode
    NCIT_C70962["obo:NCIT_C70962<br/>(Agent Administration)"]:::classNode
    NCIT_C28161["IRI for route of administration, e.g.:<br/>obo:NCIT_C28161<br/>(Intramuscular Route of Administration)"]:::classNode
    SIO_000015["sio:SIO_000015<br/>(information content entity)"]:::classNode
    NCIT_C177929["obo:NCIT_C177929<br/>(Drug Product Component)"]:::classNode
    SIO_001367["sio:SIO_001367<br/>(frequency)"]:::classNode
    NCIT_C66968["IRI for frequency, e.g.:<br/>obo:NCIT_C66968<br/>(Per Day)"]:::classNode
    SIO_000090["sio:SIO_000090<br/>(specification)"]:::classNode
    IAO_0000104["obo:IAO_0000104<br/>(plan specification)"]:::classNode
    DoseClasses["One of the following:<br/>obo:NCIT_C167190<br/>(Dose Administered)<br/>obo:NCIT_C198143<br/>(Prescribed Dose)"]:::classNode
    UO_0000022["IRI for unit of measurement, e.g.:<br/>obo:UO_0000022<br/>(milligram)"]:::classNode
    SIO_000074["sio:SIO_000074<br/>(unit of measurement)"]:::classNode

    %% Data values
    IndividualID["individual ID"]:::dataValue
    Comments["comments"]:::dataValue
    FrequencyValue["Frequency value:<br/>e.g. 2"]:::dataValue
    DoseValue["Dose value:<br/>e.g. 10.5"]:::dataValue

    %% Real edges (indices 0-30)
    ID_ -->|"sio:SIO_000300 (has value)"| IndividualID
    ID_ -->|"rdf:type"| SIO_000115
    ID_ -->|"sio:SIO_000020 (denotes)"| Role_

    Individual_ -->|"rdf:type"| SIO_000498
    Individual_ -->|"sio:SIO_000228 (has role)"| Role_

    Role_ -->|"rdf:type"| OBI_0000093
    Role_ -->|"rdf:type"| SIO_000016
    Role_ -->|"sio:SIO_000356 (is realized in)"| Process_

    Process_ -->|"rdf:type"| SIO_000006
    Process_ -->|"rdf:type"| NCIT_C70962
    Process_ -->|"sio:SIO_000028 (has part)"| Specific_method_
    Process_ -->|"sio:SIO_000230 (has input)"| URIDrugIdentifier
    Process_ -->|"sio:SIO_000900 (has frequency)"| Frequency_
    Process_ -->|"sio:SIO_000339 (is specified by)"| URITreatmentPlan
    Process_ -->|"rdfs:comment"| Comments
    Process_ -->|"sio:SIO_000229 (has output)"| Output_

    Specific_method_ -->|"rdf:type"| NCIT_C28161
    Specific_method_ -->|"rdf:type"| SIO_000006

    URIDrugIdentifier -->|"rdf:type"| SIO_000015
    URIDrugIdentifier -->|"rdf:type"| NCIT_C177929

    Frequency_ -->|"rdf:type"| SIO_001367
    Frequency_ -->|"rdf:type"| NCIT_C66968
    Frequency_ -->|"sio:SIO_000300 (has value)"| FrequencyValue

    URITreatmentPlan -->|"rdf:type"| SIO_000090
    URITreatmentPlan -->|"rdf:type"| IAO_0000104

    Output_ -->|"sio:SIO_000221 (has unit)"| Unit_
    Output_ -->|"rdf:type"| SIO_000015
    Output_ -->|"rdf:type"| DoseClasses
    Output_ -->|"sio:SIO_000300 (has value)"| DoseValue

    Unit_ -->|"rdf:type"| UO_0000022
    Unit_ -->|"rdf:type"| SIO_000074

    %% Invisible layout-only chains (indices 31-40, hidden below) force siblings into one column
    IndividualID ~~~ SIO_000115
    OBI_0000093 ~~~ SIO_000016
    SIO_000006 ~~~ NCIT_C70962 ~~~ Comments
    SIO_000015 ~~~ NCIT_C177929
    SIO_001367 ~~~ NCIT_C66968 ~~~ FrequencyValue
    SIO_000090 ~~~ IAO_0000104
    DoseClasses ~~~ DoseValue
    UO_0000022 ~~~ SIO_000074

    %% rdf:type edges (indices 1,3,5,6,8,9,16,17,18,19,20,21,23,24,26,27,29,30) de-emphasized so the structural backbone stands out
    linkStyle 1,3,5,6,8,9,16,17,18,19,20,21,23,24,26,27,29,30 stroke:#bbb,stroke-width:2px,stroke-dasharray:4 3
    linkStyle 31,32,33,34,35,36,37,38,39,40 stroke:none
```

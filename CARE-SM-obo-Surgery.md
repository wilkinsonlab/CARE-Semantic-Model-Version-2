# CARE-SM OBO Model — Surgical Intervention

Mermaid transcription of [`CARE-SM-obo-Surgery.drawio.png`](https://raw.githubusercontent.com/CARE-SM/CARE-Semantic-Model/main/images/obo/CARE-SM-obo-Surgery.drawio.png).

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

    %% Classes
    SIO_000115["sio:SIO_000115<br/>(identifier)"]:::classNode
    SIO_000498["sio:SIO_000498<br/>(person)"]:::classNode
    OBI_0000093["obo:OBI_0000093<br/>(patient role)"]:::classNode
    SIO_000016["sio:SIO_000016<br/>(role)"]:::classNode
    SIO_000006["sio:SIO_000006<br/>(process)"]:::classNode
    NCIT_C15329["obo:NCIT_C15329<br/>(Surgical Procedure)"]:::classNode
    NCIT_C164212["IRI for the specific cause of intervention and procedure, e.g.:<br/>obo:NCIT_C164212<br/>(Tumor Resection)"]:::classNode
    NCIT_C33024["IRI for the anatomic structure, e.g.:<br/>obo:NCIT_C33024<br/>(Lung Tissue)"]:::classNode
    SIO_000015["sio:SIO_000015<br/>(information content entity)"]:::classNode
    OBI_0000272["obo:OBI_0000272<br/>(protocol)"]:::classNode
    SIO_000090["sio:SIO_000090<br/>(specification)"]:::classNode

    %% Data values
    IndividualID["individual ID"]:::dataValue
    Comments["comments"]:::dataValue

    %% Real edges (indices 0-19)
    ID_ -->|"sio:SIO_000300 (has value)"| IndividualID
    ID_ -->|"rdf:type"| SIO_000115
    ID_ -->|"sio:SIO_000020 (denotes)"| Role_

    Individual_ -->|"rdf:type"| SIO_000498
    Individual_ -->|"sio:SIO_000228 (has role)"| Role_

    Role_ -->|"rdf:type"| OBI_0000093
    Role_ -->|"rdf:type"| SIO_000016
    Role_ -->|"sio:SIO_000356 (is realized in)"| Process_

    Process_ -->|"rdf:type"| SIO_000006
    Process_ -->|"rdf:type"| NCIT_C15329
    Process_ -->|"rdfs:comment"| Comments
    Process_ -->|"sio:SIO_000028 (has part)"| Specific_method_
    Process_ -->|"sio:SIO_000291 (has target)"| Target_
    Process_ -->|"sio:SIO_000339 (is specified by)"| URIProtocol

    Specific_method_ -->|"rdf:type"| NCIT_C164212
    Specific_method_ -->|"rdf:type"| SIO_000006

    Target_ -->|"rdf:type"| NCIT_C33024
    Target_ -->|"rdf:type"| SIO_000015

    URIProtocol -->|"rdf:type"| OBI_0000272
    URIProtocol -->|"rdf:type"| SIO_000090

    %% Invisible layout-only chains (indices 20-25, hidden below) force siblings into one column
    IndividualID ~~~ SIO_000115
    OBI_0000093 ~~~ SIO_000016
    SIO_000006 ~~~ NCIT_C15329 ~~~ Comments
    NCIT_C33024 ~~~ SIO_000015
    OBI_0000272 ~~~ SIO_000090

    linkStyle 20,21,22,23,24,25 stroke:none
```

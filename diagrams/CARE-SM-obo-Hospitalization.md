# CARE-SM OBO Model — Hospitalization

Mermaid transcription of [`CARE-SM-obo-Hospitalization.drawio.png`](https://raw.githubusercontent.com/CARE-SM/CARE-Semantic-Model/main/images/obo/CARE-SM-obo-Hospitalization.drawio.png).

**Legend**
- `sio:` = http://semanticscience.org/resource/
- `obo:` = http://purl.obolibrary.org/obo/
- Diamond, orange border = Used Instance
- Rectangle, green border = Class
- Rectangle, blue border = Data value

<br/>
<br/>

<!-- mermaid-start -->
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
    URIProtocol{{"URI for the protocol"}}:::usedInstance

    %% Classes
    SIO_000115["sio:SIO_000115<br/>(identifier)"]:::classNode
    SIO_000498["sio:SIO_000498<br/>(person)"]:::classNode
    OBI_0000093["obo:OBI_0000093<br/>(patient role)"]:::classNode
    SIO_000016["sio:SIO_000016<br/>(role)"]:::classNode
    SIO_000006["sio:SIO_000006<br/>(process)"]:::classNode
    NCIT_C25179["obo:NCIT_C25179<br/>(Hospitalization)"]:::classNode
    NCIT_C164212["IRI for the specific cause of<br/>intervention and procedure, e.g.:<br/>obo:NCIT_C164212<br/>(Tumor Resection)"]:::classNode
    OBI_0000272["obo:OBI_0000272<br/>(protocol)"]:::classNode
    SIO_000090["sio:SIO_000090<br/>(specification)"]:::classNode

    %% Data values
    IndividualID["individual ID"]:::dataValue
    Comments["comments"]:::dataValue

    %% Real edges (indices 0-16)
    ID_ -->|"sio:SIO_000300 (has value)"| IndividualID
    ID_ -->|"rdf:type"| SIO_000115
    ID_ -->|"sio:SIO_000020 (denotes)"| Role_

    Individual_ -->|"rdf:type"| SIO_000498
    Individual_ -->|"sio:SIO_000228 (has role)"| Role_

    Role_ -->|"rdf:type"| OBI_0000093
    Role_ -->|"rdf:type"| SIO_000016
    Role_ -->|"sio:SIO_000356 (is realized in)"| Process_

    Process_ -->|"rdf:type"| SIO_000006
    Process_ -->|"rdf:type"| NCIT_C25179
    Process_ -->|"sio:SIO_000028 (has part)"| Specific_method_
    Process_ -->|"rdfs:comment"| Comments
    Process_ -->|"sio:SIO_000339 (is specified by)"| URIProtocol

    Specific_method_ -->|"rdf:type"| SIO_000006
    Specific_method_ -->|"rdf:type"| NCIT_C164212

    URIProtocol -->|"rdf:type"| OBI_0000272
    URIProtocol -->|"rdf:type"| SIO_000090

    %% Invisible layout-only chains (indices 17-21, hidden below) force siblings into one column
    IndividualID ~~~ SIO_000115
    OBI_0000093 ~~~ SIO_000016
    SIO_000006 ~~~ NCIT_C25179 ~~~ Comments
    OBI_0000272 ~~~ SIO_000090

    %% rdf:type edges (indices 1,3,5,6,8,9,13,14,15,16) de-emphasized so the structural backbone stands out
    linkStyle 1,3,5,6,8,9,13,14,15,16 stroke:#bbb,stroke-width:2px,stroke-dasharray:4 3
    linkStyle 17,18,19,20,21 stroke:none
```
<!-- mermaid-end -->

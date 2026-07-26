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
    classDef usedInstance fill:#ffffff,stroke:#d79b00,stroke-width:7px,color:#333,font-size:20px
    classDef classNode fill:transparent,stroke:#b9c9b4,stroke-width:1.5px,color:#888,font-size:14px
    classDef dataValue fill:#ffffff,stroke:#6c8ebf,stroke-width:7px,color:#333,font-size:18px
    linkStyle default stroke:#555,stroke-width:5px

    %% Instances
    ID_{{ID_}}:::usedInstance
    Individual_{{Individual_}}:::usedInstance
    Role_{{Role_}}:::usedInstance
    Process_{{Process_}}:::usedInstance
    Specific_method_{{Specific_method_}}:::usedInstance
    URIProtocol{{"URI for the protocol"}}:::usedInstance
    Output_{{Output_}}:::usedInstance
    Duration_{{Duration_}}:::usedInstance
    Startdate_{{Startdate_}}:::usedInstance
    Enddate_{{Enddate_}}:::usedInstance

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
    SIO_000015["sio:SIO_000015<br/>(information content entity)"]:::classNode
    NCIT_C217011["obo:NCIT_C217011<br/>(Duration Quantity Value)"]:::classNode
    SIO_000417["sio:SIO_000417<br/>(time interval)"]:::classNode
    SIO_000031["sio:SIO_000031<br/>(start date)"]:::classNode
    SIO_000032["sio:SIO_000032<br/>(end date)"]:::classNode

    %% Data values
    IndividualID["individual ID"]:::dataValue
    Comments["comments"]:::dataValue
    OutputValue["Output value (optional, free-form --<br/>no output type has been defined for this<br/>model yet; add one here if/when needed)"]:::dataValue
    ISO8601Start["ISO 8601 formatted date"]:::dataValue
    ISO8601End["ISO 8601 formatted date"]:::dataValue

    %% Real edges (indices 0-28)
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
    Process_ -->|"sio:SIO_000229 (has output)"| Output_

    Specific_method_ -->|"rdf:type"| SIO_000006
    Specific_method_ -->|"rdf:type"| NCIT_C164212

    URIProtocol -->|"rdf:type"| OBI_0000272
    URIProtocol -->|"rdf:type"| SIO_000090

    Output_ -->|"rdf:type"| SIO_000015
    Output_ -->|"sio:SIO_000687 (exists at)"| Duration_
    Output_ -->|"sio:SIO_000300 (has value)"| OutputValue

    Duration_ -->|"rdf:type"| NCIT_C217011
    Duration_ -->|"rdf:type"| SIO_000417
    Duration_ -->|"sio:SIO_000680 (has start time)"| Startdate_
    Duration_ -->|"sio:SIO_000681 (has end time)"| Enddate_

    Startdate_ -->|"rdf:type"| SIO_000031
    Startdate_ -->|"sio:SIO_000300 (has value)"| ISO8601Start

    Enddate_ -->|"rdf:type"| SIO_000032
    Enddate_ -->|"sio:SIO_000300 (has value)"| ISO8601End

    %% Invisible layout-only chains (indices 29-40, hidden below) force siblings into one column
    IndividualID ~~~ SIO_000115
    OBI_0000093 ~~~ SIO_000016
    SIO_000006 ~~~ NCIT_C25179 ~~~ Comments
    OBI_0000272 ~~~ SIO_000090
    SIO_000015 ~~~ OutputValue
    NCIT_C217011 ~~~ SIO_000417
    SIO_000031 ~~~ ISO8601Start
    SIO_000032 ~~~ ISO8601End

    Specific_method_ ~~~ URIProtocol ~~~ Output_
    Startdate_ ~~~ Enddate_
    %% rdf:type edges (indices 1,3,5,6,8,9,14,15,16,17,18,21,22,25,27) de-emphasized so the structural backbone stands out
    linkStyle 1,3,5,6,8,9,14,15,16,17,18,21,22,25,27 stroke:#bbb,stroke-width:2px,stroke-dasharray:4 3
    linkStyle 29,30,31,32,33,34,35,36,37,38,39,40 stroke:none
```
<!-- mermaid-end -->

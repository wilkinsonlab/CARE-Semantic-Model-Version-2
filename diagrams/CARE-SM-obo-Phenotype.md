# CARE-SM OBO Model — Phenotype

Mermaid transcription of [`CARE-SM-obo-Phenotype.drawio.png`](https://raw.githubusercontent.com/CARE-SM/CARE-Semantic-Model/main/images/obo/CARE-SM-obo-Phenotype.drawio.png).

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
    Output_{{Output_}}:::usedInstance
    Duration_{{Duration_}}:::usedInstance
    URIProtocol{{"URI for the protocol"}}:::usedInstance
    Target_{{Target_}}:::usedInstance
    Startdate_{{Startdate_}}:::usedInstance
    Enddate_{{Enddate_}}:::usedInstance
    Attribute_{{Attribute_}}:::usedInstance

    %% Classes
    SIO_000115["sio:SIO_000115<br/>(identifier)"]:::classNode
    SIO_000498["sio:SIO_000498<br/>(person)"]:::classNode
    OBI_0000093["obo:OBI_0000093<br/>(patient role)"]:::classNode
    SIO_000016["sio:SIO_000016<br/>(role)"]:::classNode
    SIO_000006["sio:SIO_000006<br/>(process)"]:::classNode
    NCIT_C18020["obo:NCIT_C18020<br/>(Diagnostic Procedure)"]:::classNode
    OBI_0000272["obo:OBI_0000272<br/>(protocol)"]:::classNode
    SIO_000090["sio:SIO_000090<br/>(specification)"]:::classNode
    SIO_000015["sio:SIO_000015<br/>(information content entity)"]:::classNode
    PhenotypeCode["IRI for the phenotype being tested, e.g.:<br/>obo:HP_0001638 (Cardiomyopathy)"]:::classNode
    SIO_000614["sio:SIO_000614<br/>(attribute)"]:::classNode
    NCIT_C217011["obo:NCIT_C217011<br/>(Duration Quantity Value)"]:::classNode
    SIO_000417["sio:SIO_000417<br/>(time interval)"]:::classNode
    SIO_000031["sio:SIO_000031<br/>(start date)"]:::classNode
    SIO_000032["sio:SIO_000032<br/>(end date)"]:::classNode
    NCIT_C16977["obo:NCIT_C16977<br/>(Phenotype)"]:::classNode

    %% Data values
    IndividualID["individual ID"]:::dataValue
    Comments["comments"]:::dataValue
    PhenotypeName["Phenotype name"]:::dataValue
    PhenotypePresent["true / false"]:::dataValue
    ISO8601Start["ISO 8601 formatted date"]:::dataValue
    ISO8601End["ISO 8601 formatted date"]:::dataValue

    %% Real edges (indices 0-33)
    ID_ -->|"sio:SIO_000300 (has value)"| IndividualID
    ID_ -->|"rdf:type"| SIO_000115
    ID_ -->|"sio:SIO_000020 (denotes)"| Role_

    Individual_ -->|"rdf:type"| SIO_000498
    Individual_ -->|"sio:SIO_000228 (has role)"| Role_

    Role_ -->|"rdf:type"| OBI_0000093
    Role_ -->|"rdf:type"| SIO_000016
    Role_ -->|"sio:SIO_000356 (is realized in)"| Process_

    Process_ -->|"sio:SIO_000291 (has target)"| Target_
    Process_ -->|"sio:SIO_000339 (is specified by)"| URIProtocol
    Process_ -->|"rdf:type"| SIO_000006
    Process_ -->|"rdf:type"| NCIT_C18020
    Process_ -->|"rdfs:comment"| Comments
    Process_ -->|"sio:SIO_000229 (has output)"| Output_

    Target_ -->|"rdf:type"| SIO_000015
    Target_ -->|"rdf:type"| PhenotypeCode
    Target_ -->|"rdfs:label"| PhenotypeName

    URIProtocol -->|"rdf:type"| OBI_0000272
    URIProtocol -->|"rdf:type"| SIO_000090

    Output_ -->|"sio:SIO_000687 (exists at)"| Duration_
    Output_ -->|"sio:SIO_000300 (has value)"| PhenotypePresent
    Output_ -->|"sio:SIO_000628 (refers to)"| Attribute_
    Output_ -->|"rdf:type"| NCIT_C16977
    Output_ -->|"rdf:type"| SIO_000015

    Attribute_ -->|"rdf:type"| SIO_000614
    Attribute_ -->|"rdf:type"| PhenotypeCode

    Duration_ -->|"rdf:type"| NCIT_C217011
    Duration_ -->|"rdf:type"| SIO_000417
    Duration_ -->|"sio:SIO_000680 (has start time)"| Startdate_
    Duration_ -->|"sio:SIO_000681 (has end time)"| Enddate_

    Startdate_ -->|"rdf:type"| SIO_000031
    Startdate_ -->|"sio:SIO_000300 (has value)"| ISO8601Start

    Enddate_ -->|"sio:SIO_000300 (has value)"| ISO8601End
    Enddate_ -->|"rdf:type"| SIO_000032

    %% Invisible layout-only chains (indices 34-50, hidden below) force siblings into one column
    IndividualID ~~~ SIO_000115
    OBI_0000093 ~~~ SIO_000016
    SIO_000006 ~~~ NCIT_C18020 ~~~ Comments
    SIO_000015 ~~~ PhenotypeCode ~~~ PhenotypeName
    OBI_0000272 ~~~ SIO_000090
    NCIT_C16977 ~~~ SIO_000015 ~~~ PhenotypePresent
    SIO_000614 ~~~ PhenotypeCode
    NCIT_C217011 ~~~ SIO_000417
    SIO_000031 ~~~ ISO8601Start
    ISO8601End ~~~ SIO_000032
    Duration_ ~~~ Attribute_
    Startdate_ ~~~ Enddate_
    Target_ ~~~ URIProtocol ~~~ Output_

    %% rdf:type edges (indices 1,3,5,6,10,11,14,15,17,18,22,23,24,25,26,27,30,33) de-emphasized so the structural backbone stands out
    linkStyle 1,3,5,6,10,11,14,15,17,18,22,23,24,25,26,27,30,33 stroke:#bbb,stroke-width:2px,stroke-dasharray:4 3
    linkStyle 34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50 stroke:none
```
<!-- mermaid-end -->

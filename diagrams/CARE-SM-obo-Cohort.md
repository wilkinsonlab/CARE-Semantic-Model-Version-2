# CARE-SM OBO Model — Cohort

Mermaid transcription of [`CARE-SM-obo-Cohort.drawio.png`](https://raw.githubusercontent.com/CARE-SM/CARE-Semantic-Model/main/images/obo/CARE-SM-obo-Cohort.drawio.png).

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
%%{init: {"themeVariables": {"lineColor": "#888888"}}}%%
flowchart TD
    classDef usedInstance fill:#ffffff,stroke:#d79b00,stroke-width:7px,color:#333,font-size:20px
    classDef classNode fill:transparent,stroke:#b9c9b4,stroke-width:1.5px,color:#888,font-size:14px
    classDef dataValue fill:#ffffff,stroke:#6c8ebf,stroke-width:7px,color:#333,font-size:18px
    linkStyle default stroke:#888888,stroke-width:3px

    %% Instances
    ID_{{ID_}}:::usedInstance
    Individual_{{Individual_}}:::usedInstance
    Role_{{Role_}}:::usedInstance
    Process_{{Process_}}:::usedInstance
    Target_{{Target_}}:::usedInstance
    URIProtocol{{"URI for the protocol"}}:::usedInstance
    Output_{{Output_}}:::usedInstance
    Output_identifier_{{Output_identifier_}}:::usedInstance

    %% Classes
    SIO_000115["sio:SIO_000115<br/>(identifier)"]:::classNode
    SIO_000498["sio:SIO_000498<br/>(person)"]:::classNode
    OBI_0000097["obo:OBI_0000097<br/>(participant under investigation role)"]:::classNode
    SIO_000016["sio:SIO_000016<br/>(role)"]:::classNode
    SIO_000006["sio:SIO_000006<br/>(process)"]:::classNode
    NCIT_C15208["obo:NCIT_C15208<br/>(Cohort Study)"]:::classNode
    SIO_000614["sio:SIO_000614<br/>(attribute)"]:::classNode
    NCIT_C7057["obo:NCIT_C7057<br/>(Disease or Disorder)"]:::classNode
    OBI_0000272["obo:OBI_0000272<br/>(protocol)"]:::classNode
    SIO_000090["sio:SIO_000090<br/>(specification)"]:::classNode
    SIO_000015["sio:SIO_000015<br/>(information content entity)"]:::classNode
    NCIT_C142439["obo:NCIT_C142439<br/>(Clinical Study Report)"]:::classNode
    NCIT_C83082["obo:NCIT_C83082<br/>(Study Identifier)"]:::classNode

    %% Data values
    IndividualID["individual ID"]:::dataValue
    Comments["comments"]:::dataValue
    ReportStudyIdentifier["Report study identifier"]:::dataValue

    %% Real edges (indices 0-23)
    ID_ -->|"sio:SIO_000300 (has value)"| IndividualID
    ID_ -->|"rdf:type"| SIO_000115
    ID_ -->|"sio:SIO_000020 (denotes)"| Role_

    Individual_ -->|"rdf:type"| SIO_000498
    Individual_ -->|"sio:SIO_000228 (has role)"| Role_

    Role_ -->|"rdf:type"| OBI_0000097
    Role_ -->|"rdf:type"| SIO_000016
    Role_ -->|"sio:SIO_000356 (is realized in)"| Process_

    Process_ -->|"rdf:type"| SIO_000006
    Process_ -->|"rdf:type"| NCIT_C15208
    Process_ -->|"rdfs:comment"| Comments
    Process_ -->|"sio:SIO_000291 (has target)"| Target_
    Process_ -->|"sio:SIO_000339 (is specified by)"| URIProtocol
    Process_ -->|"sio:SIO_000229 (has output)"| Output_

    Target_ -->|"rdf:type"| SIO_000614
    Target_ -->|"rdf:type"| NCIT_C7057

    URIProtocol -->|"rdf:type"| OBI_0000272
    URIProtocol -->|"rdf:type"| SIO_000090

    Output_ -->|"rdf:type"| SIO_000015
    Output_ -->|"rdf:type"| NCIT_C142439
    Output_ -->|"sio:SIO_000671 (has identifier)"| Output_identifier_

    Output_identifier_ -->|"rdf:type"| SIO_000115
    Output_identifier_ -->|"rdf:type"| NCIT_C83082
    Output_identifier_ -->|"sio:SIO_000300 (has value)"| ReportStudyIdentifier

    %% Invisible layout-only chains (indices 24-32, hidden below) force siblings into one column
    IndividualID ~~~ SIO_000115
    OBI_0000097 ~~~ SIO_000016
    SIO_000006 ~~~ NCIT_C15208 ~~~ Comments
    SIO_000614 ~~~ NCIT_C7057
    OBI_0000272 ~~~ SIO_000090
    NCIT_C83082 ~~~ ReportStudyIdentifier

    Target_ ~~~ URIProtocol ~~~ Output_
    %% rdf:type edges (indices 1,3,5,6,8,9,14,15,16,17,18,19,21,22) de-emphasized so the structural backbone stands out
    linkStyle 1,3,5,6,8,9,14,15,16,17,18,19,21,22 stroke:#bbb,stroke-width:2px,stroke-dasharray:4 3
    linkStyle 24,25,26,27,28,29,30,31,32 stroke:none
```
<!-- mermaid-end -->

# CARE-SM OBO Model — Questionnaire

Mermaid transcription of [`CARE-SM-obo-Questionnaire.drawio.png`](https://raw.githubusercontent.com/CARE-SM/CARE-Semantic-Model/main/images/obo/CARE-SM-obo-Questionnaire.drawio.png).

**Legend**
- `sio:` = http://semanticscience.org/resource/
- `obo:` = http://purl.obolibrary.org/obo/
- Diamond, orange border = Used Instance
- Rectangle, green border = Class
- Rectangle, blue border = Data value

<br/>
<br/>

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
    Output_{{Output_}}:::usedInstance
    IRIQuestionCode{{"IRI for the question annotation code"}}:::usedInstance
    URIPROMsCode{{"URI for PROMs annotation code"}}:::usedInstance

    %% Classes
    SIO_000115["sio:SIO_000115<br/>(identifier)"]:::classNode
    SIO_000498["sio:SIO_000498<br/>(person)"]:::classNode
    OBI_0000093["obo:OBI_0000093<br/>(patient role)"]:::classNode
    SIO_000016["sio:SIO_000016<br/>(role)"]:::classNode
    SIO_000006["sio:SIO_000006<br/>(process)"]:::classNode
    NCIT_C20993["obo:NCIT_C20993<br/>(Research or Clinical Assessment Tool)"]:::classNode
    NCIT_C91102["obo:NCIT_C91102<br/>(Clinical or Research Assessment Question)"]:::classNode
    SIO_000015["sio:SIO_000015<br/>(information content entity)"]:::classNode
    SIO_000090["sio:SIO_000090<br/>(specification)"]:::classNode
    NCIT_C177377["obo:NCIT_C177377<br/>(Patient Reported Outcome Measures)"]:::classNode
    NCIT_C49149["obo:NCIT_C49149<br/>(Answer)"]:::classNode

    %% Data values
    IndividualID["individual ID"]:::dataValue
    Comments["comments"]:::dataValue
    LexicalOutcome["Lexical reported outcome value/score"]:::dataValue

    %% Real edges (indices 0-20)
    ID_ -->|"sio:SIO_000300 (has value)"| IndividualID
    ID_ -->|"rdf:type"| SIO_000115
    ID_ -->|"sio:SIO_000020 (denotes)"| Role_

    Individual_ -->|"rdf:type"| SIO_000498
    Individual_ -->|"sio:SIO_000228 (has role)"| Role_

    Role_ -->|"rdf:type"| OBI_0000093
    Role_ -->|"rdf:type"| SIO_000016
    Role_ -->|"sio:SIO_000356 (is realized in)"| Process_

    Process_ -->|"rdf:type"| SIO_000006
    Process_ -->|"rdf:type"| NCIT_C20993
    Process_ -->|"sio:SIO_000230 (has input)"| IRIQuestionCode
    Process_ -->|"rdfs:comment"| Comments
    Process_ -->|"sio:SIO_000339 (is specified by)"| URIPROMsCode
    Process_ -->|"sio:SIO_000229 (has output)"| Output_

    IRIQuestionCode -->|"rdf:type"| NCIT_C91102
    IRIQuestionCode -->|"rdf:type"| SIO_000015

    URIPROMsCode -->|"rdf:type"| SIO_000090
    URIPROMsCode -->|"rdf:type"| NCIT_C177377

    Output_ -->|"rdf:type"| NCIT_C49149
    Output_ -->|"rdf:type"| SIO_000015
    Output_ -->|"sio:SIO_000300 (has value)"| LexicalOutcome

    %% Invisible layout-only chains (indices 21-27, hidden below) force siblings into one column
    IndividualID ~~~ SIO_000115
    OBI_0000093 ~~~ SIO_000016
    SIO_000006 ~~~ NCIT_C20993 ~~~ Comments
    NCIT_C91102 ~~~ SIO_000015
    SIO_000090 ~~~ NCIT_C177377
    NCIT_C49149 ~~~ LexicalOutcome

    %% rdf:type edges (indices 1,3,5,6,8,9,14,15,16,17,18,19) de-emphasized so the structural backbone stands out
    linkStyle 1,3,5,6,8,9,14,15,16,17,18,19 stroke:#bbb,stroke-width:2px,stroke-dasharray:4 3
    linkStyle 21,22,23,24,25,26,27 stroke:none
```

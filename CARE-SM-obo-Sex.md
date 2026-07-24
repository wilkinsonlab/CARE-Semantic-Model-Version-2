# CARE-SM OBO Model — Sex

Mermaid transcription of [`CARE-SM-obo-Sex.drawio.png`](https://raw.githubusercontent.com/CARE-SM/CARE-Semantic-Model/main/images/obo/CARE-SM-obo-Sex.drawio.png).

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
    Output_{{Output_}}:::usedInstance
    Attribute_{{Attribute_}}:::usedInstance
    URIProtocol{{"URI for the protocol"}}:::usedInstance

    %% Classes
    SIO_000115["sio:SIO_000115<br/>(identifier)"]:::classNode
    SIO_000498["sio:SIO_000498<br/>(person)"]:::classNode
    OBI_0000093["obo:OBI_0000093<br/>(patient role)"]:::classNode
    SIO_000016["sio:SIO_000016<br/>(role)"]:::classNode
    SIO_000006["sio:SIO_000006<br/>(process)"]:::classNode
    NCIT_C142470["obo:NCIT_C142470<br/>(Data Capture)"]:::classNode
    OBI_0000272["obo:OBI_0000272<br/>(protocol)"]:::classNode
    SIO_000090["sio:SIO_000090<br/>(specification)"]:::classNode
    SIO_000015["sio:SIO_000015<br/>(information content entity)"]:::classNode
    NCIT_C160908["obo:NCIT_C160908<br/>(Sex Code)"]:::classNode
    SIO_000614["sio:SIO_000614<br/>(attribute)"]:::classNode
    SexOptions["One of the following:<br/>obo:NCIT_C16576 (Female)<br/>obo:NCIT_C20197 (Male)<br/>obo:NCIT_C89084 (Undetermined)<br/>obo:NCIT_C17998 (Unknown)"]:::classNode

    %% Data values
    IndividualID["individual ID"]:::dataValue
    Comments["comments"]:::dataValue
    SexName["Sex name"]:::dataValue

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
    Process_ -->|"rdf:type"| NCIT_C142470
    Process_ -->|"rdfs:comment"| Comments
    Process_ -->|"sio:SIO_000339 (is specified by)"| URIProtocol
    Process_ -->|"sio:SIO_000229 (has output)"| Output_

    URIProtocol -->|"rdf:type"| OBI_0000272
    URIProtocol -->|"rdf:type"| SIO_000090

    Output_ -->|"rdf:type"| NCIT_C160908
    Output_ -->|"rdf:type"| SIO_000015
    Output_ -->|"sio:SIO_000300 (has value)"| SexName
    Output_ -->|"sio:SIO_000628 (refers to)"| Attribute_

    Attribute_ -->|"rdf:type"| SIO_000614
    Attribute_ -->|"rdf:type"| SexOptions

    %% Invisible layout-only chains (indices 21-28, hidden below) force siblings into one column
    IndividualID ~~~ SIO_000115
    OBI_0000093 ~~~ SIO_000016
    SIO_000006 ~~~ NCIT_C142470 ~~~ Comments
    OBI_0000272 ~~~ SIO_000090
    NCIT_C160908 ~~~ SIO_000015 ~~~ SexName
    SIO_000614 ~~~ SexOptions

    linkStyle 21,22,23,24,25,26,27,28 stroke:none
```

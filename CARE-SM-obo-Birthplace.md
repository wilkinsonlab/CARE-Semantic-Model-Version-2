# CARE-SM OBO Model — Birthplace

Mermaid transcription of [`CARE-SM-obo-Birthplace.drawio.png`](https://raw.githubusercontent.com/CARE-SM/CARE-Semantic-Model/main/images/obo/CARE-SM-obo-Birthplace.drawio.png).

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
    Output_{{Output_}}:::usedInstance
    Attribute_{{Attribute_}}:::usedInstance
    URIProtocol{{"URI for the protocol"}}:::usedInstance
    IRICountryCode{{"IRI for country code"}}:::usedInstance

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
    NCIT_C25464["obo:NCIT_C25464<br/>(Country)"]:::classNode
    NCIT_C20108["obo:NCIT_C20108<br/>(Country Code)"]:::classNode
    SIO_000614["sio:SIO_000614<br/>(attribute)"]:::classNode
    NCIT_C176764["obo:NCIT_C176764<br/>(Birthplace)"]:::classNode

    %% Data values
    IndividualID["individual ID"]:::dataValue
    Comments["comments"]:::dataValue
    CountryName["Country name"]:::dataValue

    %% Real edges (indices 0-23)
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

    Output_ -->|"sio:SIO_000671 (has identifier)"| IRICountryCode
    Output_ -->|"rdf:type"| NCIT_C25464
    Output_ -->|"rdf:type"| SIO_000015
    Output_ -->|"sio:SIO_000628 (refers to)"| Attribute_

    IRICountryCode -->|"rdf:type"| SIO_000115
    IRICountryCode -->|"rdf:type"| NCIT_C20108
    IRICountryCode -->|"sio:SIO_000300 (has value)"| CountryName

    Attribute_ -->|"rdf:type"| SIO_000614
    Attribute_ -->|"rdf:type"| NCIT_C176764

    %% Invisible layout-only chains (indices 24-32, hidden below) force siblings into one column
    IndividualID ~~~ SIO_000115
    OBI_0000093 ~~~ SIO_000016
    SIO_000006 ~~~ NCIT_C142470 ~~~ Comments
    OBI_0000272 ~~~ SIO_000090
    NCIT_C25464 ~~~ SIO_000015
    SIO_000115 ~~~ NCIT_C20108 ~~~ CountryName
    SIO_000614 ~~~ NCIT_C176764

    %% rdf:type edges (indices 1,3,5,6,8,9,13,14,16,17,19,20,22,23) de-emphasized so the structural backbone stands out
    linkStyle 1,3,5,6,8,9,13,14,16,17,19,20,22,23 stroke:#bbb,stroke-width:2px,stroke-dasharray:4 3
    linkStyle 24,25,26,27,28,29,30,31,32 stroke:none
```

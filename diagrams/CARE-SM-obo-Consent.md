# CARE-SM OBO Model — Consent

Mermaid transcription of [`CARE-SM-obo-Consent.drawio.png`](https://raw.githubusercontent.com/CARE-SM/CARE-Semantic-Model/main/images/obo/CARE-SM-obo-Consent.drawio.png).

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
    URIProtocol{{"URI for the protocol"}}:::usedInstance
    Output_{{Output_}}:::usedInstance
    Attribute_{{Attribute_}}:::usedInstance
    Input_{{Input_}}:::usedInstance

    %% Classes
    SIO_000115["sio:SIO_000115<br/>(identifier)"]:::classNode
    SIO_000498["sio:SIO_000498<br/>(person)"]:::classNode
    OBI_0000093["obo:OBI_0000093<br/>(patient role)"]:::classNode
    SIO_000016["sio:SIO_000016<br/>(role)"]:::classNode
    SIO_000006["sio:SIO_000006<br/>(process)"]:::classNode
    OBI_0000810["obo:OBI_0000810<br/>(Informed consent process)"]:::classNode
    OBI_0000272["obo:OBI_0000272<br/>(protocol)"]:::classNode
    SIO_000090["sio:SIO_000090<br/>(specification)"]:::classNode
    SIO_000015["sio:SIO_000015<br/>(information content entity)"]:::classNode
    DUO_0000001["IRI that describes the consent statement, e.g.:<br/>obo:DUO_0000001 (Data Use Permission)<br/>obo:OBIB_0000488 (willingness to be contacted)"]:::classNode
    NCIT_C25460["obo:NCIT_C25460<br/>(Consent)"]:::classNode
    SIO_000614["sio:SIO_000614<br/>(attribute)"]:::classNode
    NCIT_C16468["obo:NCIT_C16468<br/>(Consent Form)"]:::classNode

    %% Data values
    IndividualID["individual ID"]:::dataValue
    Comments["comments"]:::dataValue
    LexicalConsentStatement["Lexical consent statement"]:::dataValue
    ConsentFormFilename["Consent form filename + version,<br/>e.g. 'consent_form_v2.1.pdf'<br/>(not a URL)"]:::dataValue

    %% Real edges (indices 0-24)
    ID_ -->|"sio:SIO_000300 (has value)"| IndividualID
    ID_ -->|"rdf:type"| SIO_000115
    ID_ -->|"sio:SIO_000020 (denotes)"| Role_

    Individual_ -->|"rdf:type"| SIO_000498
    Individual_ -->|"sio:SIO_000228 (has role)"| Role_

    Role_ -->|"rdf:type"| OBI_0000093
    Role_ -->|"rdf:type"| SIO_000016
    Role_ -->|"sio:SIO_000356 (is realized in)"| Process_

    Process_ -->|"rdf:type"| SIO_000006
    Process_ -->|"rdf:type"| OBI_0000810
    Process_ -->|"rdfs:comment"| Comments
    Process_ -->|"sio:SIO_000339 (is specified by)"| URIProtocol
    Process_ -->|"sio:SIO_000229 (has output)"| Output_
    Process_ -->|"sio:SIO_000230 (has input)"| Input_

    URIProtocol -->|"rdf:type"| OBI_0000272
    URIProtocol -->|"rdf:type"| SIO_000090

    Output_ -->|"sio:SIO_000628 (refers to)"| Attribute_
    Output_ -->|"rdf:type"| SIO_000015
    Output_ -->|"rdf:type"| DUO_0000001
    Output_ -->|"sio:SIO_000300 (has value)"| LexicalConsentStatement

    Attribute_ -->|"rdf:type"| NCIT_C25460
    Attribute_ -->|"rdf:type"| SIO_000614

    Input_ -->|"rdf:type"| SIO_000015
    Input_ -->|"rdf:type"| NCIT_C16468
    Input_ -->|"sio:SIO_000300 (has value)"| ConsentFormFilename

    %% Invisible layout-only chains (indices 25-36, hidden below) force siblings into one column
    IndividualID ~~~ SIO_000115
    OBI_0000093 ~~~ SIO_000016
    SIO_000006 ~~~ OBI_0000810 ~~~ Comments
    OBI_0000272 ~~~ SIO_000090
    SIO_000015 ~~~ DUO_0000001 ~~~ LexicalConsentStatement
    NCIT_C25460 ~~~ SIO_000614
    SIO_000015 ~~~ NCIT_C16468 ~~~ ConsentFormFilename

    URIProtocol ~~~ Output_ ~~~ Input_
    %% rdf:type edges (indices 1,3,5,6,8,9,14,15,17,18,20,21,22,23) de-emphasized so the structural backbone stands out
    linkStyle 1,3,5,6,8,9,14,15,17,18,20,21,22,23 stroke:#bbb,stroke-width:2px,stroke-dasharray:4 3
    linkStyle 25,26,27,28,29,30,31,32,33,34,35,36 stroke:none
```
<!-- mermaid-end -->

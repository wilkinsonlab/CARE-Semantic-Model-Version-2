# CARE-SM OBO Model — Genetic

Mermaid transcription of [`CARE-SM-obo-Genetic.drawio.png`](https://raw.githubusercontent.com/CARE-SM/CARE-Semantic-Model/main/images/obo/CARE-SM-obo-Genetic.drawio.png).

**Legend**
- `sio:` = http://semanticscience.org/resource/
- `obo:` = http://purl.obolibrary.org/obo/
- Diamond, orange border = Used Instance
- Rectangle, green border = Class
- Rectangle, blue border = Data value

**Note on `Output_` vs `Attribute_`:** a single sequence variant report (`Output_`, typed `obo:NCIT_C171178`) can describe *multiple* distinct variants, so `Output_` itself carries no identifying content — it's just the report container. Each individual variant is its own `Attribute_` instance, reached via a separate `Output_ --refers to--> Attribute_` edge (this edge can and should repeat, once per variant). Zygosity and the variant's own identifying notation both belong to *that specific variant*, not to the report as a whole, so both live on `Attribute_`: its `rdf:type` gives the zygosity (`GENO_0000133` and children), and its `has identifier` edge points to an `Identifier_` bnode carrying the variant's lexical notation (e.g. HGVS) as a literal value. A report with three variants is modeled as one `Output_` with three separate `Attribute_`/`Identifier_` pairs hanging off it, not one `Output_` trying to hold three identifiers at once.

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
    Specific_method_{{Specific_method_}}:::usedInstance
    Input_{{Input_}}:::usedInstance
    URIProtocol{{"URI for the protocol"}}:::usedInstance
    Output_{{Output_}}:::usedInstance
    Attribute_{{Attribute_}}:::usedInstance
    Identifier_{{Identifier_}}:::usedInstance

    %% Classes
    SIO_000115["sio:SIO_000115<br/>(identifier)"]:::classNode
    SIO_000498["sio:SIO_000498<br/>(person)"]:::classNode
    OBI_0000093["obo:OBI_0000093<br/>(patient role)"]:::classNode
    SIO_000016["sio:SIO_000016<br/>(role)"]:::classNode
    SIO_000006["sio:SIO_000006<br/>(process)"]:::classNode
    NCIT_C15709["obo:NCIT_C15709<br/>Genetic Testing"]:::classNode
    NCIT_C18477["IRI for a specific method, e.g.:<br/>obo:NCIT_C18477<br/>(Microarray Analysis)"]:::classNode
    NCIT_C17610["IRI for the input sample<br/>source, e.g.:<br/>obo:NCIT_C17610<br/>(Blood Sample)"]:::classNode
    SIO_000015["sio:SIO_000015<br/>(information content entity)"]:::classNode
    OBI_0000272["obo:OBI_0000272<br/>(protocol)"]:::classNode
    SIO_000090["sio:SIO_000090<br/>(specification)"]:::classNode
    SIO_000614["sio:SIO_000614<br/>(attribute)"]:::classNode
    GENO_0000133["Child of obo:GENO_0000133<br/>(zygosity) e.g.:<br/>obo:GENO_0000134 (hemizygosity)<br/>obo:GENO_0000135 (heterozygosity)<br/>obo:GENO_0000136 (homozygosity)<br/>obo:GENO_0000978 (nullizygosity)<br/>obo:GENO_0000402 (compound heterozygosity)"]:::classNode
    NCIT_C171178["obo:NCIT_C171178<br/>(Sequence Variant Report)"]:::classNode
    NCIT_C164607["obo:NCIT_C164607<br/>(Sequence Identifier)"]:::classNode

    %% Data values
    IndividualID["individual ID"]:::dataValue
    Comments["comments"]:::dataValue
    LexicalSequenceVariant["Lexical sequence variant, e.g.:<br/>NC_000023.9:g.32317682G>A"]:::dataValue

    %% Real edges (indices 0-29)
    ID_ -->|"sio:SIO_000300 (has value)"| IndividualID
    ID_ -->|"rdf:type"| SIO_000115
    ID_ -->|"sio:SIO_000020 (denotes)"| Role_

    Individual_ -->|"rdf:type"| SIO_000498
    Individual_ -->|"sio:SIO_000228 (has role)"| Role_

    Role_ -->|"rdf:type"| OBI_0000093
    Role_ -->|"rdf:type"| SIO_000016
    Role_ -->|"sio:SIO_000356 (is realized in)"| Process_

    Process_ -->|"rdf:type"| SIO_000006
    Process_ -->|"rdf:type"| NCIT_C15709
    Process_ -->|"rdfs:comment"| Comments
    Process_ -->|"sio:SIO_000028 (has part)"| Specific_method_
    Process_ -->|"sio:SIO_000230 (has input)"| Input_
    Process_ -->|"sio:SIO_000339 (is specified by)"| URIProtocol
    Process_ -->|"sio:SIO_000229 (has output)"| Output_

    Specific_method_ -->|"rdf:type"| SIO_000006
    Specific_method_ -->|"rdf:type"| NCIT_C18477

    Input_ -->|"rdf:type"| NCIT_C17610
    Input_ -->|"rdf:type"| SIO_000015

    URIProtocol -->|"rdf:type"| OBI_0000272
    URIProtocol -->|"rdf:type"| SIO_000090

    Output_ -->|"sio:SIO_000628 (refers to)"| Attribute_
    Output_ -->|"rdf:type"| SIO_000015
    Output_ -->|"rdf:type"| NCIT_C171178

    Attribute_ -->|"rdf:type"| SIO_000614
    Attribute_ -->|"rdf:type"| GENO_0000133
    Attribute_ -->|"sio:SIO_000671 (has identifier)"| Identifier_

    Identifier_ -->|"rdf:type"| SIO_000115
    Identifier_ -->|"sio:SIO_000300 (has value)"| LexicalSequenceVariant
    Identifier_ -->|"rdf:type"| NCIT_C164607

    %% Invisible layout-only chains (indices 30-43, hidden below) force siblings into one column
    IndividualID ~~~ SIO_000115
    OBI_0000093 ~~~ SIO_000016
    SIO_000006 ~~~ NCIT_C15709 ~~~ Comments
    SIO_000006 ~~~ NCIT_C18477
    NCIT_C17610 ~~~ SIO_000015
    OBI_0000272 ~~~ SIO_000090
    SIO_000015 ~~~ NCIT_C171178
    SIO_000614 ~~~ GENO_0000133
    SIO_000115 ~~~ LexicalSequenceVariant ~~~ NCIT_C164607

    Specific_method_ ~~~ Input_ ~~~ URIProtocol ~~~ Output_
    %% rdf:type edges (indices 1,3,5,6,8,9,15,16,17,18,19,20,22,23,24,25,27,29) de-emphasized so the structural backbone stands out
    linkStyle 1,3,5,6,8,9,15,16,17,18,19,20,22,23,24,25,27,29 stroke:#bbb,stroke-width:2px,stroke-dasharray:4 3
    linkStyle 30,31,32,33,34,35,36,37,38,39,40,41,42,43 stroke:none
```
<!-- mermaid-end -->

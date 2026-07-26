# CARE-SM OBO Model — Diagnosis

Mermaid transcription of [`CARE-SM-obo-Diagnosis.drawio.png`](https://raw.githubusercontent.com/CARE-SM/CARE-Semantic-Model/main/images/obo/CARE-SM-obo-Diagnosis.drawio.png).

**Legend**
- `sio:` = http://semanticscience.org/resource/
- `obo:` = http://purl.obolibrary.org/obo/
- Diamond, orange border = Used Instance
- Rectangle, green border = Class
- Rectangle, blue border = Data value

**Note on `Process_ --has input--> Input_`:** this edge is a deliberate schema placeholder, not an actively populated relationship. A diagnosis is generally *informed by* prior evidence (lab results, genotyping, phenotype observations, etc.), and `has-input` is the structurally correct place to express that provenance if it's ever needed. However, "which evidence supports this diagnosis" is an interpretive judgment that can legitimately differ between users of the same data — it is not a fixed fact that should be asserted once and stored. Baking a specific evidentiary link into the graph would freeze one interpretation as ground truth. Instead, evidence-gathering is expected to happen at query time, as an ad hoc join across the independently-existing `Output_` nodes of whatever processes occurred for the same patient/encounter — nothing needs to be pre-linked for that to work. Consequently, `Input_` is emitted as an empty bnode typed only `rdf:type sio:SIO_000015` (information content entity) — present in the schema, intentionally inert. A future use case that genuinely needs to persist a specific evidentiary link could extend `Input_` with real content (e.g. a stringified reference, following the same bnode-plus-literal-value pattern used for `Identifier_` elsewhere in this model) without breaking anything that depends on the current empty form.

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
    Target_{{Target_}}:::usedInstance
    URIProtocol{{"URI for the protocol"}}:::usedInstance
    Output_{{Output_}}:::usedInstance
    Attribute_{{Attribute_}}:::usedInstance
    Input_{{Input_}}:::usedInstance
    Duration_{{Duration_}}:::usedInstance
    Startdate_{{Startdate_}}:::usedInstance
    Enddate_{{Enddate_}}:::usedInstance

    %% Classes
    SIO_000115["sio:SIO_000115<br/>(identifier)"]:::classNode
    SIO_000498["sio:SIO_000498<br/>(person)"]:::classNode
    OBI_0000093["obo:OBI_0000093<br/>(patient role)"]:::classNode
    SIO_000016["sio:SIO_000016<br/>(role)"]:::classNode
    SIO_000006["sio:SIO_000006<br/>(process)"]:::classNode
    NCIT_C18020["obo:NCIT_C18020<br/>(Diagnostic Procedure)"]:::classNode
    SIO_000015["sio:SIO_000015<br/>(information content entity)"]:::classNode
    DiagnosisCode["IRI for the diagnosis being tested, e.g.:<br/>obo:ORDO_Orphanet_93552 (Marfan syndrome)"]:::classNode
    OBI_0000272["obo:OBI_0000272<br/>(protocol)"]:::classNode
    SIO_000090["sio:SIO_000090<br/>(specification)"]:::classNode
    SIO_000614["sio:SIO_000614<br/>(attribute)"]:::classNode
    OGMS_0000073["obo:OGMS_0000073<br/>(Diagnosis)"]:::classNode
    NCIT_C217011["obo:NCIT_C217011<br/>(Duration Quantity Value)"]:::classNode
    SIO_000417["sio:SIO_000417<br/>(time interval)"]:::classNode
    SIO_000031["sio:SIO_000031<br/>(start date)"]:::classNode
    SIO_000032["sio:SIO_000032<br/>(end date)"]:::classNode

    %% Data values
    IndividualID["individual ID"]:::dataValue
    Comments["comments"]:::dataValue
    DiagnosisName["Diagnosis name"]:::dataValue
    DiagnosisPresent["true / false"]:::dataValue
    ISO8601Start["ISO 8601 formatted date"]:::dataValue
    ISO8601End["ISO 8601 formatted date"]:::dataValue

    %% Real edges (indices 0-35)
    ID_ -->|"sio:SIO_000300 (has value)"| IndividualID
    ID_ -->|"rdf:type"| SIO_000115
    ID_ -->|"sio:SIO_000020 (denotes)"| Role_

    Individual_ -->|"rdf:type"| SIO_000498
    Individual_ -->|"sio:SIO_000228 (has role)"| Role_

    Role_ -->|"rdf:type"| OBI_0000093
    Role_ -->|"rdf:type"| SIO_000016
    Role_ -->|"sio:SIO_000356 (is realized in)"| Process_

    Process_ -->|"rdf:type"| SIO_000006
    Process_ -->|"rdf:type"| NCIT_C18020
    Process_ -->|"rdfs:comment"| Comments
    Process_ -->|"sio:SIO_000291 (has target)"| Target_
    Process_ -->|"sio:SIO_000339 (is specified by)"| URIProtocol
    Process_ -->|"sio:SIO_000229 (has output)"| Output_
    Process_ -->|"sio:SIO_000230 (has input)"| Input_

    Target_ -->|"rdf:type"| SIO_000015
    Target_ -->|"rdf:type"| DiagnosisCode
    Target_ -->|"rdfs:label"| DiagnosisName

    URIProtocol -->|"rdf:type"| OBI_0000272
    URIProtocol -->|"rdf:type"| SIO_000090

    Output_ -->|"sio:SIO_000628 (refers to)"| Attribute_
    Output_ -->|"sio:SIO_000687 (exists at)"| Duration_
    Output_ -->|"sio:SIO_000300 (has value)"| DiagnosisPresent
    Output_ -->|"rdf:type"| OGMS_0000073
    Output_ -->|"rdf:type"| SIO_000015

    Attribute_ -->|"rdf:type"| SIO_000614
    Attribute_ -->|"rdf:type"| DiagnosisCode

    %% Input_ is a deliberate empty-bnode placeholder -- see the note above the diagram
    Input_ -->|"rdf:type"| SIO_000015

    Duration_ -->|"rdf:type"| NCIT_C217011
    Duration_ -->|"rdf:type"| SIO_000417
    Duration_ -->|"sio:SIO_000680 (has start time)"| Startdate_
    Duration_ -->|"sio:SIO_000681 (has end time)"| Enddate_

    Startdate_ -->|"rdf:type"| SIO_000031
    Startdate_ -->|"sio:SIO_000300 (has value)"| ISO8601Start

    Enddate_ -->|"rdf:type"| SIO_000032
    Enddate_ -->|"sio:SIO_000300 (has value)"| ISO8601End

    %% Invisible layout-only chains (indices 36-53, hidden below) force siblings into one column
    IndividualID ~~~ SIO_000115
    OBI_0000093 ~~~ SIO_000016
    SIO_000006 ~~~ NCIT_C18020 ~~~ Comments
    SIO_000015 ~~~ DiagnosisCode ~~~ DiagnosisName
    OBI_0000272 ~~~ SIO_000090
    OGMS_0000073 ~~~ SIO_000015 ~~~ DiagnosisPresent
    SIO_000614 ~~~ DiagnosisCode

    Target_ ~~~ URIProtocol ~~~ Output_ ~~~ Input_
    Attribute_ ~~~ Duration_
    NCIT_C217011 ~~~ SIO_000417
    SIO_000031 ~~~ ISO8601Start
    SIO_000032 ~~~ ISO8601End
    Startdate_ ~~~ Enddate_
    %% rdf:type edges (indices 1,3,5,6,8,9,15,16,18,19,23,24,25,26,27,28,29,32,34) de-emphasized so the structural backbone stands out
    linkStyle 1,3,5,6,8,9,15,16,18,19,23,24,25,26,27,28,29,32,34 stroke:#bbb,stroke-width:2px,stroke-dasharray:4 3
    linkStyle 36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53 stroke:none
```
<!-- mermaid-end -->

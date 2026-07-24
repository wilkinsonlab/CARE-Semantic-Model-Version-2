# Clinical And Registry Entries (CARE) Semantic Model — Version 2

![GitHub tag](https://img.shields.io/github/v/tag/wilkinsonlab/CARE-Semantic-Model-Version-2)
[![Documentation Status](https://readthedocs.org/projects/care-sm-semantic-model-v2/badge/?version=latest)](https://care-sm-semantic-model-v2.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/github/license/wilkinsonlab/CARE-Semantic-Model-Version-2)](LICENSE)
[![Code of Conduct](https://img.shields.io/badge/code%20of%20conduct-contributor%20covenant-4baaaa.svg)](CODE_OF_CONDUCT.md)

<p align="center">
  <img
    src="https://github.com/CARE-SM/CARE-SM-docs/blob/main/docs/assets/care-sm.png?raw=true"
    alt="CARE-SM logo"
    width="300"
    height="300"
  >
</p>

<p align="center">
  <strong>Take CARE of your data! FAIRly!</strong>
</p>

---

## About This Version

This repository is a **new, evolving version of the CARE Semantic Model**, derived from the [original CARE-SM](https://github.com/CARE-SM/CARE-Semantic-Model) developed by Pablo Alarcón-Moreno as part of his PhD thesis, [*"Applying deep semantics to the representation of clinical data to improve machine usability"*](https://oa.upm.es/83239/) (Universidad Politécnica de Madrid, 2024).

Building on that foundation, this version aims to:

- **Consolidate and harmonize** several of the original individual data element models into a more unified, consistent representation.
- **Adapt the models to handle real-world use-cases** that could not be represented in the original CARE-SM. For example, the original model had no way to represent a *negative* observation — e.g. a phenotype test whose result is "false" — even though that absence-of-finding is itself an important, recordable fact.

**This work is under active construction.** Models, structures, and documentation here may change as the harmonization effort progresses. We welcome feedback, questions, and suggestions — see [Communication and Feedback](#communication-and-feedback) below.

---
## Full Documentation

You can explore the complete documentation
[on ReadTheDocs](https://care-sm-semantic-model-v2.readthedocs.io/en/latest/)



The documentation includes:
- Detailed descriptions of all data elements
- Implementation guidelines
- Tools
- Exemplar data
- Additional resources

---

## Communication and Feedback

Your feedback is more than welcome and will help us improve the CARE Semantic Model.

Please use **GitHub Issues** to provide feedback or report problems:  
https://github.com/CARE-SM/CARE-Semantic-Model/issues

---

## Cite Us

Zenodo link
<a href="https://zenodo.org/records/18785871">here</a>

If you used CARE-SM in your work, please cite the following publication:

```bibtex
@inproceedings{caresm2024,
  author       = {Pablo Alarc{\'o}n-Moreno and Mark Denis Wilkinson},
  title        = {{Take CARE of your patient data: Clinical And Registry Entries (CARE) Semantic Model}},
  booktitle    = {Proceedings of the 15th International Conference on Semantic Web Applications and Tools for Health Care and Life Sciences (SWAT4HCLS 2024)},
  year         = {2024},
  publisher    = {CEUR-WS.org},
  series       = {CEUR Workshop Proceedings},
  volume       = {3890},
  url          = {https://ceur-ws.org/Vol-3890/paper-11.pdf}
}
```

<p><strong>Previous publication:</strong><br>
<a href="https://doi.org/10.1186/s13326-022-00264-6">
Semantic modeling of common data elements for rare disease registries, and a prototype workflow for their deployment over registry data
</a>
</p>

<hr>

<h2>Acknowledgement</h2>

<p>
This work originated in the
<a href="https://www.ejprarediseases.org/">European Joint Programme on Rare Diseases (EJP RD)</a>,
which received funding from the European Union’s <strong>Horizon 2020 research and innovation programme</strong>
under grant agreement <strong>No. 825575</strong>.
</p>

<p align="center">
  <img src="https://github.com/CARE-SM/CARE-SM-docs/blob/main/docs/assets/ejprd.png?raw=true" alt="EJPRD logo" height="50">
  <img src="https://github.com/CARE-SM/CARE-SM-docs/blob/main/docs/assets/eu.png?raw=true" alt="EU logo" height="50">
</p>

<p>
It is now continued as part of the
<a href="https://erdera.org/">European Rare Disease Research Alliance (ERDERA)</a>,
which receives funding from the European Union’s <strong>Horizon Europe research and innovation programme</strong>
under grant agreement <strong>No. 101156595</strong>.
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/wilkinsonlab/CARE-Semantic-Model-Version-2/main/docs/assets/erdera.svg" alt="ERDERA logo" height="50">
  <img src="https://github.com/CARE-SM/CARE-SM-docs/blob/main/docs/assets/eu.png?raw=true" alt="EU logo" height="50">
</p>

<p>

After the end of the EJP RD project, this work has been led and maintained by researchers from the
<a href="http://wilkinsonlab.info/">Wilkinson Lab</a>
at <strong>Universidad Politécnica de Madrid</strong>.
</p>

<p>
<p align="center">
  <img src="https://github.com/CARE-SM/CARE-SM-docs/blob/main/docs/assets/UPM.png?raw=true" alt="EU logo" width="130">
</p>

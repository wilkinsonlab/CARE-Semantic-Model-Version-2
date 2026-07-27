# CARE-SM Toolkit
**Repository dedicated to CARE-SM Toolkit**

[![Toolkit tests](https://github.com/wilkinsonlab/CARE-Semantic-Model-Version-2/actions/workflows/toolkit-tests.yml/badge.svg)](https://github.com/wilkinsonlab/CARE-Semantic-Model-Version-2/actions/workflows/toolkit-tests.yml)

<p align="center"> 
    <img src="https://raw.githubusercontent.com/wilkinsonlab/CARE-Semantic-Model-Version-2/main/docs/assets/care-sm.png" alt="CARE-SM logo" width="300" height="300">
<p align="center" > </p> 

## Documentation

Learn more about our documentation for this toolkit [here](https://care-sm-semantic-model-v2.readthedocs.io/en/latest/toolkit.html).

## Docker

The current version is tracked in [`VERSION`](VERSION). Build and run locally with:

```bash
docker build -t markw/care-sm-toolkit:$(cat VERSION) .
docker compose up
```

This serves the API on `http://localhost:8000` (interactive docs at `/docs`). `docker-compose.yaml` mounts `./toolkit/data/obo` to `/data` (also overridable via the `CARE_DATA_DIR` environment variable) for input CSVs and the `CARE.csv` output.

Most real deployments run this image as part of [Sextans Fix](https://github.com/wilkinsonlab/Sextans-Suite), which chains it with `yarrrml-rdfizer` over a shared data volume — see [Docker](https://care-sm-semantic-model-v2.readthedocs.io/en/latest/toolkit.html#docker) in the full docs for how that fits together.

## Communication and feedback
Your feedback is more than welcome. It will help us improve our semantic data model. Please use [github issues](https://github.com/wilkinsonlab/CARE-Semantic-Model-Version-2/issues) to provide your feedback.

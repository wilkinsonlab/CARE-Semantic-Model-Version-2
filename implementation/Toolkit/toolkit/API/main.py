from fastapi import FastAPI, Response, status
import uvicorn
import os
from pathlib import Path
from toolkit.main import Toolkit
import logging
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CARE-SM Toolkit",
    description="Toolkit for data transformation using CARE-SM",
    version="2.0.0"
)

# /data is the fixed convention this image is deployed under (e.g. Sextans
# Fix's docker-compose-template.yml mounts ./data:/data for this service,
# and ./data:/mnt/data for the downstream yarrrml-rdfizer that consumes
# this service's CARE.csv output from the same shared host folder).
# Previously computed as Path(__file__).resolve().parent.parent / "data",
# which only produced /data if this file happened to sit two directories
# below the container root -- fragile and silently wrong at any other
# COPY/WORKDIR layout. Override via CARE_DATA_DIR if you need something else.
folder = Path(os.environ.get("CARE_DATA_DIR", "/data"))

@app.get("/")
async def api_running():
    return {
        "status": "ok",
        "message": "API is running. See /docs for interactive documentation.",
    }
@app.head(
    "/", summary="Health check (HEAD)", description="HEAD health check",)
async def health_check_head():
    return

@app.post("/toolkit", summary="Perform the transformation and validation from CSV-glossary-based data into a unified CSV prepared for RDF serialization using YARRRML.", status_code=status.HTTP_200_OK)
async def csv_transformation_by_caresm_toolkit():
    toolkit_instance = Toolkit()

    try:
        toolkit_instance.whole_method(folder_path=str(folder), template_type="OBO")
        logger.info("Structural Transformation completed successfully.")
        return {"message": "Structural Transformation done"}
    except Exception as e:
        return Response(
            content=f"An error occurred: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@app.post("/CSV2OBO",summary="Perform the transformation and validation from CSV-glossary-based data into a unified CSV prepared for RDF serialization using YARRRML.", status_code=status.HTTP_200_OK)
async def csv_transformation_by_caresm_toolkit():
    toolkit_instance = Toolkit()

    try:
        toolkit_instance.whole_method(folder_path=str(folder), template_type="OBO")
        logger.info("Structural Transformation completed successfully.")
        return {"message": "Structural Transformation done"}
    except Exception as e:
        return Response(
            content=f"An error occurred: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@app.post("/CSV2SNOMED",summary="Perform the transformation and validation from CSV-glossary-based data into a unified CSV prepared for RDF serialization using YARRRML.", status_code=status.HTTP_200_OK)
async def csv_transformation_by_caresm_toolkit():
    toolkit_instance = Toolkit()

    try:
        toolkit_instance.whole_method(folder_path=str(folder), template_type="SNOMED")
        logger.info("Structural Transformation completed successfully.")
        return {"message": "Structural Transformation done"}
    except Exception as e:
        return Response(
            content=f"An error occurred: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

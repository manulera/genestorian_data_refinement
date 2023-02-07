from fastapi import FastAPI
from starlette.responses import RedirectResponse
from pydantic import BaseModel


# We have to define classes that the API will receive as json

# The class for the request
class ProcessAlleleRequest(BaseModel):
    name: str

    # This is the example provided in the docs
    # In json it would be:
    # {
    #   'name': 'cut11-mch:ura4+'
    # }
    class Config:
        schema_extra = {
            "example": {"name": "cut11-mch:ura4+"}
        }


# The class for the response
class ProcessAlleleResponse(BaseModel):
    name: str
    pattern: list[tuple[str, list[str]]]


app = FastAPI()


@ app.get("/")
async def root():
    return RedirectResponse("/docs")


@ app.post("/process_allele", response_model=ProcessAlleleResponse)
async def check_allele(request: ProcessAlleleRequest):

    # This variable contains the allele name, in the example cut11-mch:ura4+
    allele_name = request.name

    # Here is where your function would take the allele name and return the pattern
    # allele_pattern = your_function(allele_name)

    # For now there is this dummy allele_pattern, you can comment this when
    # you have added your function:
    allele_pattern = [["GENE", ["cut11"]], ["-", ["-"]],
                      ["TAG", ["mch"]], ["-", [":"]], ["ALLELE", ["ura4+"]]]

    # Here you instantiate the response object
    response = ProcessAlleleResponse(
        name=allele_name,
        pattern=allele_pattern
    )

    return response

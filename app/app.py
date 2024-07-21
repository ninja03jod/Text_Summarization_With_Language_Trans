from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from langchain_community.llms import Ollama
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from googletrans import Translator, LANGUAGES
import uvicorn

# Initialize the app
app = FastAPI()

# Initialize the LLM and translator
llm = Ollama(model="llama3", temperature=0.7)
translator = Translator()

# Language codes for reference
language_codes = {lang.lower(): code for code, lang in LANGUAGES.items()}

class Tone(str, Enum):
    neutral = "neutral"
    friendly = "friendly"
    formal = "formal"
    casual = "casual"
    assertive = "assertive"
    apologetic = "apologetic"

class Length(str, Enum):
    short = "short"
    medium = "medium"
    long = "long"

class SummaryRequest(BaseModel):
    text: str
    tone: Tone = Tone.neutral
    length: Length = Length.medium
    max_length: int = 100
    target_language: Optional[str] = "hi"
    expand: Optional[bool] = False
    alter_text: Optional[bool] = False
    translate: Optional[bool] = False

class SummaryResponse(BaseModel):
    summary: str
    language_code: Optional[str] = None

@app.post("/summarize", response_model=SummaryResponse)
async def summarize(request: SummaryRequest):
    """
    Generate a summary of the given text with specified tone and length.
    Optionally expand or alter the text, and translate it to the target language.
    """
    # Validate the target language if translation is requested
    if request.translate and request.target_language and request.target_language.lower() not in language_codes:
        raise HTTPException(status_code=400, detail="Invalid target language")

    # Construct the prompt based on the input parameters
    prompt = f"Summarize the following text in a {request.tone} tone and {request.length} length (maximum {request.max_length} characters):\n\n{request.text}"

    # Create a Document object
    document = Document(page_content=prompt)

    # Load the summarize chain
    chain = load_summarize_chain(llm, chain_type="map_reduce")

    # Generate the summary using the LLM
    summary = chain.run([document])

    # Optionally expand the summary
    if request.expand:
        expansion_prompt = f"Expand the following summary with more details while retaining its meaning:\n\n{summary}"
        expansion_document = Document(page_content=expansion_prompt)
        expansion_chain = load_summarize_chain(llm, chain_type="map_reduce")
        summary = expansion_chain.run([expansion_document])
    
    # Optionally alter the summary
    if request.alter_text:
        alteration_prompt = f"Alter the following summary to improve clarity or style without changing its meaning:\n\n{summary}"
        alteration_document = Document(page_content=alteration_prompt)
        alteration_chain = load_summarize_chain(llm, chain_type="map_reduce")
        summary = alteration_chain.run([alteration_document])

    # Optionally translate the summary
    language_code = None
    if request.translate and request.target_language:
        language_code = language_codes.get(request.target_language.lower(), "hi")
        translation = translator.translate(summary, dest=language_code)
        summary = translation.text

    return SummaryResponse(summary=summary, language_code=language_code)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
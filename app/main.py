from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from langchain_community.llms import Ollama
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from googletrans import Translator, LANGUAGES

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
    target_language: str = "hi"

class SummaryResponse(BaseModel):
    summary: str
    language_code: str
    
@app.post("/summarize", response_model=SummaryResponse)
async def summarize(request: SummaryRequest):
    """
    Generate a summary of the given text with specified tone and length, and translate it to the target language.
    """
    if request.target_language.lower() not in language_codes:
        raise HTTPException(status_code=400, detail="Invalid target language")

    # Construct the prompt based on the input parameters
    prompt = f"Summarize the following text in a {request.tone} tone and {request.length} length (maximum {request.max_length} characters):\n\n{request.text}"

    # Create a Document object
    document = Document(page_content=prompt)

    # Load the summarize chain
    chain = load_summarize_chain(llm, chain_type="map_reduce")

    # Generate the summary using the LLM
    summary = chain.run([document])  # Use invoke instead of run

    # Translate the summary to the target language
    translation = translator.translate(summary, dest=language_codes[request.target_language.lower()])
    summary_text = translation.text

    return SummaryResponse(summary=summary_text, language_code=language_codes[request.target_language.lower()])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
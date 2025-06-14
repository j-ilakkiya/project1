import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

# Load your CSVs
df_discourse = pd.read_csv("discourse.csv")
df_tds = pd.read_csv("tds.csv")

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
def answer_question(request: QuestionRequest):
    query = request.question.lower()
    matches = []

    for _, row in df_discourse.iterrows():
        if query in str(row.get("Content", "")).lower() or query in str(row.get("Title", "")).lower():
            matches.append({
                "answer": row.get("Content", ""),
                "url": row.get("URL", ""),
                "source": "Discourse",
                "title": row.get("Title", "")
            })

    for _, row in df_tds.iterrows():
        combined_text = " ".join([str(x).lower() for x in row.astype(str)])
        if query in combined_text:
            matches.append({
                "answer": combined_text,
                "url": row.get("URL", "#"),
                "source": "TDS Project Page",
                "title": row.get("Title", "")
            })

    if not matches:
        return JSONResponse(content={"answer": "No relevant content found.", "links": []})

    top = matches[0]
    return {
        "answer": top["answer"],
        "links": [{"url": top["url"], "text": top["title"] or "Click here", "source": top["source"]}]
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

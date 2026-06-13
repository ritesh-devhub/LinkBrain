from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from retrieval import retrieval
from dotenv import load_dotenv
import config
from utils.helpers import SYSTEM_MESSAGE
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


model = ChatGoogleGenerativeAI(model = config.LLM_MODEL)



def answer_query(user_query):

    context, sources = retrieval.retrieve_context(user_query)

    if not context:
        return {
        "success": False,
        "error": str("Not able to gather Context")
    }

    prompt = f"""
                Context:
                {context}

                Question:
                {user_query}

                Answer using only the context above.
                If the answer is not present, say that you do not have enough information.
            """

    try:
        response = model.invoke(
            [SystemMessage(content=SYSTEM_MESSAGE),
            HumanMessage(content=prompt)]
            )
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    

    seen = set()

    for source in sources :
        citation = (
            source['title'],
            source['url']
        )
        if citation not in seen:
            seen.add(citation)

    return {
    "answer": response.content,
    "sources": list(seen)
}


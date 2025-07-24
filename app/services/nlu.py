import os
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser


load_dotenv()

llm = ChatMistralAI(
    model="mistral-large-latest",
    api_key=os.getenv("MISTRAL_API_KEY"),
    temperature=0
)


intent_prompt = PromptTemplate.from_template("""
Classifique a frase do cliente em UMA categoria:
- SAUDACAO
- PEDIDO_ORCAMENTO
- PERGUNTA_PRODUTO
- HORARIO_FUNCIONAMENTO
- VAGA_EMPREGO
- FORA_REGIAO
- CONTINUIDADE_FLUXO
- DESPEDIDA
- CONFIRMACAO
- OUTRO

Frase: {texto}
Categoria:
""")

slots_prompt = PromptTemplate.from_template("""
Extraia os seguintes dados em JSON:
- produto
- volume_aproximado
- localidade
- prazo

Retorne APENAS JSON.
Frase: {texto}
JSON:
""")

async def classify_intent(texto: str) -> str:
    chain = intent_prompt | llm | StrOutputParser()
    return await chain.ainvoke({"texto": texto})

async def extract_slots(texto: str) -> dict:
    chain = slots_prompt | llm | JsonOutputParser()
    return await chain.ainvoke({"texto": texto})

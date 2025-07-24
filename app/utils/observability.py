import mlflow

async def log_interaction(pergunta, resposta, intencao, slots, docs):
    mlflow.set_experiment("chat")
    with mlflow.start_run():
        mlflow.log_param("intencao", intencao)
        mlflow.log_param("pergunta", pergunta)
        mlflow.log_param("resposta", resposta[:300])
        mlflow.log_dict({
            "slots": slots,
            "docs": [d.page_content for d in docs]
        }, "interaction.json")

from transformers import pipeline, AutoTokenizer, AutoModelForQuestionAnswering


if __name__ == "__main__":

    # Use the pipeline high-level interface to NLP workflow
    question_anwerer = pipeline("question-answering")
    context = """🤗 Transformers is backed by the three most popular deep learning libraries — Jax, PyTorch, and TensorFlow — with a seamless integration
    between them. It's straightforward to train your models with one before loading them for inference with the other.
    """
    context_2 = """Ray is an open-source unified framework for scaling AI and Python applications like machine learning. 
    It provides the compute layer for parallel processing so that you don’t need to be a distributed systems expert. 
    Ray minimizes the complexity of running your distributed individual and end-to-end machine learning workflows with these components:
    Scalable libraries for common machine learning tasks such as data preprocessing, distributed training, hyperparameter tuning, reinforcement learning, and model serving.
    Pythonic distributed computing primitives for parallelizing and scaling Python applications.
    
    For data scientists and machine learning practitioners, Ray lets you scale jobs without needing infrastructure cloud expertise on Kubernetes, AWS, GCP, and Azure
    """

    question = "Which deep learning libraries back 🤗 Transformers?"
    response = question_anwerer(question=question, context=context)
    
    print(response)
    question_2 = "Data scientists and machine learning preactioners can scale jobs on what cloud infrastructure"
    response = question_anwerer(question=question_2, context=context_2)
    print(response)
    question_3 = "What is Ray?"
    response = question_anwerer(question=question_3, context=context_2)
    print(response)

    # Let's use the model for inference instead of pipeline
    model_checkpoint = "distilbert-base-cased-distilled-squad"
    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
    model = AutoModelForQuestionAnswering.from_pretrained(model_checkpoint)

    inputs = tokenizer(question, context, return_tensors="pt")
    outputs = model(**inputs)

    # Examine the logits
    start_logits = outputs.start_logits
    end_logits = outputs.end_logits
    print(start_logits.shape, end_logits.shape)

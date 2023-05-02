from transformers import AutoTokenizer

# Let try two different kind of model and see how their tokenizers normalize tokens
# bert-base-cased and bert-base-uncased

tokens_lst = ["hello how are u?", "Héllò hôw are ü?", "Hello How are U t'day"]

if __name__ == "__main__":
    tokenizer_bert_uncased = AutoTokenizer.from_pretrained("bert-base-uncased")
    tokenizer_bert_cased = AutoTokenizer.from_pretrained("bert-base-cased")
    tokenizer_gpt_2 = AutoTokenizer.from_pretrained("gpt2")
    tokenizer_t5 = AutoTokenizer.from_pretrained("t5-small")

    tokenizers = [ tokenizer_bert_uncased, tokenizer_bert_cased, tokenizer_t5]

    for tokenizer in tokenizers:
        print(f"tokenizer: {tokenizer.name_or_path}")
        for t_str in tokens_lst:
            print(f"token string: {t_str}")
            print(f"tokens: {tokenizer.backend_tokenizer.normalizer.normalize_str(t_str)}")
            tokenizer.backend_tokenizer.pre_tokenizer.pre_tokenize_str("Hello, how are  you?")
        
        print("--" * 5)

    print("++++ pretokinzations" )
    for tokenizer in tokenizers:
        print(f"tokenizer: {tokenizer.name_or_path}")
        for t_str in tokens_lst:
            print(f"token string: {t_str}")
            print(f"pre-tokenization: {tokenizer.backend_tokenizer.pre_tokenizer.pre_tokenize_str(t_str)}")

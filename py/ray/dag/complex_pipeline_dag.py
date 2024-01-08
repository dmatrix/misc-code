import ray
from typing import List
from gen_sentences import generate_n_random_sentences

@ray.remote
def gen_data(num) -> List[str]:
    return generate_n_random_sentences(num)

@ray.remote 
def capitalize(sentences: List[str]) -> List[str]:
    return [s.upper() for s in sentences]

@ray.remote
def lowercase(sentences: List[str]) -> List[str]:
    return [s.lower() for s in sentences]

@ray.remote
def aggregate(data: List[str]) -> int:
    print(f"Aggregating data: {ray.get(data)})")
    return sum(ray.get(data))

@ray.remote
def sentence_count(data: List[str]) -> int:
    count = 0
    # print(f"Counting words in data: {data}")
    for sentence in data:
        # print(f"Counting words in sentence: {sentence}")
        count += len(sentence.split()) if isinstance(sentence, str) else sentence
    print(f"Total count: {count}")
    return count

if __name__ == "__main__":
    # Initialize Ray
    if not ray.is_initialized():
        ray.init()

    # Build the DAG:
    # data -> capitalize_data -> aggregated_data
    #       \____lowercase____/
    #        \__sentencecount_/
    
    # Generate 25 random sentences
    
    data_node_1 = gen_data.bind(10)
    data_node_2 = gen_data.bind(10)


    # Capitalize and lowercase the sentences
    capitalized_data_node = capitalize.bind(data_node_1)
    lowercased_data_node = lowercase.bind(data_node_2)

    # Aggregate the data
    sentence_count_node_1 = sentence_count.bind(capitalized_data_node)
    sentence_count_node_2 = sentence_count.bind(lowercased_data_node)
    aggregated_data_node = aggregate.bind([sentence_count_node_1, sentence_count_node_2])
    results = ray.get(aggregated_data_node.execute())
    print(f"Aggregated word count of merged list: {results}")
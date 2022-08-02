def objective(tensor):
    acc = (tensor ** 2 + 2.5)/10e5
    acc *= random.uniform(0,1)
    return acc
    
def model(batch):
    scores=[]
    # print(f"type:{type(batch)} batch of size: {batch.shape}")
    for score in np.nditer(batch):
        res = objective(score)
        scores.append(res)
    return 100.00 if sum(scores) > 100.00 else sum(scores)
import re
import math
import random

def tokenise(filename):
    with open(filename, 'r') as f:
        return [i for i in re.split(r'(\d|\W)', f.read().replace('_', ' ').lower()) if i and i != ' ' and i != '\n']

def build_unigram(sequence):
    # Task 1.1
    # Return a unigram model.
    # Replace the line below with your code.
    counts = {}
    for token in sequence:
        if token in counts:
            counts[token] += 1
        else:
            counts[token] = 1
    return {(): counts}

def build_bigram(sequence):
    # Task 1.2
    # Return a bigram model.
    # Replace the line below with your code.
    model = {}
    for i in range(len(sequence) - 1):
        context = (sequence[i],)
        next_token = sequence[i + 1]
        if context not in model:
            model[context] = {}
        if next_token in model[context]:
            model[context][next_token] += 1
            
        else:
            model[context][next_token] = 1
    return model

def build_n_gram(sequence, n):
    # Task 1.3
    # Return an n-gram model.
    # Replace the line below with your code.
    if n == 1:
        return build_unigram(sequence)
    

    model = {}
    for i in range(len(sequence) - (n - 1)):
        context = tuple(sequence[i:i + n - 1])
        next_token = sequence[i + n - 1]
        if context not in model:
            model[context] = {}
        if next_token in model[context]:
            model[context][next_token] += 1
        else:
            model[context][next_token] = 1
    return model

def query_n_gram(model, sequence):
    # Task 2
    # Return a prediction as a dictionary.
    # Replace the line below with your code.
    if () in model:
        return model[()]
    
    context_len = len(list(model.keys())[0])
    context = tuple(sequence[-context_len:])
    
    if context in model:
        return model[context]
    return None

def blended_probabilities(preds, factor=0.8):
    blended_probs = {}
    mult = factor
    comp = 1 - factor
    for pred in preds[:-1]:
        if pred:
            weight_sum = sum(pred.values())
            for k, v in pred.items():
                if k in blended_probs:
                    blended_probs[k] += v * mult / weight_sum
                else:
                    blended_probs[k] = v * mult / weight_sum
            mult = comp * factor
            comp -= mult
    pred = preds[-1]
    mult += comp
    weight_sum = sum(pred.values())
    for k, v in pred.items():
        if k in blended_probs:
            blended_probs[k] += v * mult / weight_sum
        else:
            blended_probs[k] = v * mult / weight_sum
    weight_sum = sum(blended_probs.values())
    return {k: v / weight_sum for k, v in blended_probs.items()}

def sample(sequence, models):
    # Task 3
    # Return a token sampled from blended predictions.
    # Replace the line below with your code.
    preds = []
    for model in models:
        if () in model:
            n=1
        else:
            n = len(list(model.keys())[0]) + 1
        if len(sequence) >= n -1:
            pred = query_n_gram(model, tuple(sequence))
            preds.append(pred)
    
    preds = [p for p in preds if p is not None]
    
    blended = blended_probabilities(preds)
    
    tokens = list(blended.keys())
    probs = list(blended.values())
    return random.choices(tokens, weights=probs, k=1)[0]

def log_likelihood_ramp_up(sequence, models):
    # Task 4.1
    # Return a log likelihood value of the sequence based on the models.
    # Replace the line below with your code.
    total = 0.0

    for i in range(len(sequence)):
        model_index = max(0, len(models)- 1 - i)
        model = models[model_index]
        
        context = tuple(sequence[:i])
        pred = query_n_gram(model, context)
        
        token = sequence[i]
        
        if pred is None or token not in pred:
            return - math.inf
        
        prob = pred[token]/sum(pred.values())
        total += math.log(prob)
    
    return total


def log_likelihood_blended(sequence, models):
    # Task 4.2
    # Return a log likelihood value of the sequence based on the models.
    # Replace the line below with your code.
    total = 0.0
    
    for i in range(len(sequence)):
        token = sequence[i]
        context = tuple(sequence[:i])
        
        preds = []
        for model in models:
            if () in model:
                n = 1
            else:
                n = len(list(model.keys())[0]) + 1    
            if len(context) >= n - 1:
                pred = query_n_gram(model, context)
                preds.append(pred)
        preds = [p for p in preds if p is not None]
        blended = blended_probabilities(preds)
        
        if token not in blended:
            return -math.inf
        total += math.log(blended[token])
    
    return total

if __name__ == '__main__':

    sequence = tokenise('assignment3corpus.txt')
    # Task 1.1 test code
    model = build_unigram(sequence[:20])
    print(model)


    # Task 1.2 test code
    model = build_bigram(sequence[:20])
    print(model)

    # Task 1.3 test code
    model = build_n_gram(sequence[:20], 5)
    print(model)

    # Task 2 test code
    print(query_n_gram(model, tuple(sequence[:4])))

    # Task 3 test code
    models = [build_n_gram(sequence, i) for i in range(10, 0, -1)]
    head = []
    for _ in range(100):
        tail = sample(head, models)
        print(tail, end=' ')
        head.append(tail)
    print()

    # Task 4.1 test code
    print(log_likelihood_ramp_up(sequence[:20], models))
    
    # Task 4.2 test code
    print(log_likelihood_blended(sequence[:20], models))
    

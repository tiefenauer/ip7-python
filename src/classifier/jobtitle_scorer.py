tag_weight = {
    'h1': 0.6,
    'h2': 0.3,
    'h3': 0.1,
    'default': 0.1
}


def normalize(rank):
    if rank < 1:
        return rank
    return 1 / rank


def calculate_score(features):
    rank = 0
    key = features['tag'] if features['tag'] in tag_weight else 'default'
    rank += tag_weight[key]
    # todo: add more feature values here if available
    return normalize(rank)

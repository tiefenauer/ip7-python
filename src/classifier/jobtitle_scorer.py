tag_weight = {
    'h1': 0.6,
    'h2': 0.3,
    'h3': 0.1,
    'default': 0
}


def normalize(rank):
    if rank < 1:
        return rank
    return 1 / rank


def calculate_score(features):
    rank = 0
    if features['tag']:
        rank += tag_weight[features['tag']]
    # todo: add more feature values here if available
    return normalize(rank)

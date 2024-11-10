import random


def main(args):
    user_id = args.get("user_id", "stranger")
    slug = random.randint(1, 5)
    score_rng = random.Random(str(user_id) + str(slug))
    score = score_rng.random()

    return {
        "body": {"slug": slug, "score": score},
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        }
    }

from semantic_router import Route, RouteLayer
from semantic_router.encoders import OpenAIEncoder


def build_route_layer():
    question = Route(
        name="question",
        utterances=[
            "what do you mean?",
            "What is IFS?",
            "I'm not sure",
            "What is a protector?"
        ]
    )

    response = Route(
        name="response",
        utterances=[
            "I think I feel anxiety.",
            "It think it's trying to protect an exile",
            "I feel angry towards the part",
            "I am feeling frustrated",
        ],
    )

    routes: list = [question, response]
    return RouteLayer(encoder=OpenAIEncoder(), routes=routes)




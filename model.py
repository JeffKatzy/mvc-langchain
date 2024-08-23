from langchain_core.pydantic_v1 import BaseModel, Field


class IFSPart(BaseModel):
    part: str = Field("",
        description="A feeling, struggle, thought pattern, or part they encounter.",
    )
    aware_of_part: str = Field("",
        description="Physical feeling of part or the sense of the part",
    )
    
    def views(self):
        return {'ask_if_part': 
                        {'text': "Ask if there's a feeling, struggle, thought pattern, or part they need help with.",
                        'field': 'part'},
        'judge_awareness': {"text": "Ask if they are able to feel the part in their body, if they are not able to feel it, ask if they have a sense of the part", 
                            "field": "aware_of_part"},
        }

    def render(self, step):
        return self.views()[step]['text']

    def get_next_field(self):
        priority_steps = ['ask_if_part', 'judge_awareness']
        for step in priority_steps:
            if not getattr(self, self.views()[step]['field']):
                return step

class GeneralResponse(BaseModel):
    """Use this when the other parser is not applicable.  This is for storing general information about the user responses."""
    text: str = Field("",
        description="This is the user input",
    )
    
    
    
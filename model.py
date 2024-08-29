from typing import Callable, Optional

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.pydantic_v1 import BaseModel, Field

from prompt import next_message_prompt
from view_utils import BaseWorkflow, WField

# from pydantic import BaseModel

class IFSPart(BaseModel):
    part: str = Field("",
        description="A feeling, struggle, thought pattern, or part they encounter.",
    )
    aware_of_part: str = Field("",
        description="Physical feeling of part or the sense of the part",
    )
    feeling_to_part: str = Field("",
        description="Emotion or response towards the primary part")
    # achieved_unblending: bool = Field("")

class IFSWorkflow(BaseWorkflow):
    _model: IFSPart

    find_part: WField = WField(prompt="Ask if there's a feeling, struggle, thought pattern, or part they need help with.",
        skip=lambda view: bool(view._model.part))
    assess_awareness: WField = WField(prompt = "Thank them, mirror using parts language.  Then ask if they're aware of this part and how they sense or are aware of the part.",
                        skip=lambda view: bool(view._model.aware_of_part))
    ask_feeling_towards_part: WField = WField(prompt = "Ask how they feel toward the target part.",
                                skip=lambda view: bool(view._model.feeling_to_part))
    unblend_from_part: WField = WField(prompt = "If the user feels negative qualities towards the part, help them unblend.", 
                                    skip=lambda view: bool(view._model.achieved_unblending))
    ask_to_share_feelings: WField = WField(prompt = "If the user confirms the feelings are from Self and they feel positively toward the part, ask them to share their feelings with the part",
                                skip=lambda view: bool(view._model.shared_feelings))
    ask_how_receieved: WField = WField(prompt = "Ask how the part received the shared feelings.")

    def __init__(self, model, **data):
        super().__init__(**data)
        self._model = model
    
    def prompt(self):
        return next_message_prompt

class GeneralResponse(BaseModel):
    """Use this when the other parser is not applicable.  This is for storing general information about the user responses."""
    text: str = Field("",
        description="This is the user input",
    )
    
    
    
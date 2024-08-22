from langchain_core.pydantic_v1 import BaseModel, Field


class PersonalDetails(BaseModel):
    first_name: str = Field("",
        description="This is the first name of the user.",
    )
    last_name: str = Field("",
        description="This is the last name or surname of the user.",
    )
    full_name: str = Field("",
        description="Is the full name of the user ",
    )
    city: str = Field("",
        description="The name of the city where someone lives",
    )
    email: str = Field("",
        description="an email address that the person associates as theirs",
    )
    language: str = Field([],enum=["spanish", "english", "french", "german", "italian"]
    )

    def get_next_field(self):
        priority_fields = ['first_name', 'last_name', 'full_name', 'city', 'email', 'language']
        for field in priority_fields:
            if not getattr(self, field):
                return field

    def render(self, field):
        views = {'first_name': 'Ask the user for the first name',
        'last_name': 'Ask the user for their last name',
        'full_name': 'Ask the user for their full name',
        'city': 'Ask the user for their city',
        'email': 'Ask the user for their email'
        }
        return views[field]
    
    

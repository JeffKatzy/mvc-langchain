
https://python.langchain.com/v0.1/docs/expression_language/how_to/message_history/

https://jayant017.medium.com/efficient-few-shot-prompting-in-langchain-output-parsers-part-3-56c036a01321

Todo:

* Potentially refactor more with langchain
    * See if can stream solutions so can hook into chainlit
    * Refactor with langgraph state?  Does this slow it down?
* Refactor the parse details so that will work more generically
* Need more thought on linking steps vs linking the parser
    * For example, more logic as to when to move onto the next question
        * Eg for some, maybe ok to move on, even if we don't have the answer
* Organize files
* Still should look into Zep for output parsing
MVC Langchain pattern implementation.

* Separates models from workflows (ie. views), to allow for separate logic from parsing and prompting.
* Both sequenced and non-sequenced responses achieved via routing.
* When sequenced workflow used, looks at skip logic of each question to see if step is complete.

Todo:

* Potentially refactor more with langchain
    * See if can stream solutions so can hook into chainlit
    * Refactor with langgraph state?  Does this slow it down?
* Refactor the parse details so that will work more generically
* Still should look into Zep for output parsing
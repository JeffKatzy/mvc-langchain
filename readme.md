MVC Langchain pattern implementation.

* Separates models from workflows (ie. views), to allow for separate logic from parsing and prompting.
* Both sequenced and non-sequenced responses achieved via routing.
* When sequenced workflow used, looks at skip logic of each question to see if step is complete.

To run:

* `git clone https://github.com/JeffKatzy/mvc-langchain`
* `cd mvc-langchain`
* `python3 -m venv venv`
* `pip3 install -r requirements.txt`
* `mv .env.example .env`
* Add your openai api key
* python3 -i console.py

Todo:

* Potentially refactor more with langchain
    * Refactor with langgraph state?  Does this slow it down?
* Still should look into Zep for output parsing
* Look at Cerebras for latency
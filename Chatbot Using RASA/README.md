## RASA Chatbot

Rasa is an open source machine learning framework for automated text and voice-based conversations. Understand messages, hold conversations, and connect to messaging channels and APIs.

### Installing RASA

To install RASA and dependency libraries in our local system, we use the pip installation technique.Then download en_core_web_md, a medium-sized english model trained on written web text.

```
pip install nest_asyncio==1.3.3
pip install rasa_nlu[spacy]
pip install rasa_core
pip install -U ipython
python -m spacy download en_core_web_md
pip install h5py==2.10.0
```

### RASA Chatbot

- [Chatbot](./RASA_Chatbot.ipynb)
- [Domain](./domain.yml)
- [NLU](./nlu.md)
- [Configuration](./config.yml)
- [Stories](./stories.md)

## References

[Basics of building an assistant with Rasa Open Source with this interactive guide](https://rasa.com/docs/rasa/playground/) .

#### CONTRIBUTED BY

[Shreya Ghosh](https://github.com/shreya024)

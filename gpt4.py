import g4f

def gpt(data):
    try:
        response = g4f.ChatCompletion.create(
            model="gpt-4-32k-0613",        # g4f.models.gpt_4
            provider=g4f.Provider.GPTalk, # gemini, bard
            messages=[{"role" : "user", "content" : data}],
            stream=True
        )
        sentence = ""
        for word in response:
            sentence+=word
            print(word, end="", flush=True)
        return sentence
    except Exception as e:
        print(f'Exception: {e}')
        
gpt('hey')
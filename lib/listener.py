import speech_recognition as sr

def listen():
    r = sr.Recognizer()

    print('Listening...')
    with sr.Microphone() as source:
        audio = r.listen(source)

    print('Recognizing...')

    data = ''
    
    try:    
        data = str(r.recognize_google(audio)).lower()
        print(data)
        
    except:
        None

    return data

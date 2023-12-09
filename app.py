from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import speech_recognition as sr
import openai
# Set your OpenAI GPT-3 API key
#####openai.api_key = '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'
#openai.api_key = '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'
openai.api_key = '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'
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'})

    audio_file = request.files['audio']

    if audio_file.filename == '':
        return jsonify({'error': 'No selected file'})

    if audio_file and allowed_file(audio_file.filename):
        filename = secure_filename(audio_file.filename)
        audio_path = f"{app.config['UPLOAD_FOLDER']}/{filename}"
        audio_file.save(audio_path)

        recognizer = sr.Recognizer()
        #with sr.AudioFile(audio_path) as source:
            #audio_text = recognizer.recognize_google(source)
        clean_support_call = sr.AudioFile(audio_path)
        with clean_support_call as source:
                clean_support_call_audio = recognizer.record(source)
        type(clean_support_call_audio)		
        audio_text=recognizer.recognize_google(audio_data=clean_support_call_audio)
        print(audio_text)
        prompt = 'Generate the overall Agent Report on the scale of 5 ( ratings - 1 poor 3 average 5 awesome) based on Was agent greeted yes/no? understood problem yes/no? solved it yes/no? engaged -yes/no?'
        #prompt = 'Generate the overall Agent Report on the scale of 5 ( ratings - 1 poor 3 average 5 awesome) for the provided Conversations in array explaining What agent should stop,start,continue doing?'
        '''
        #prompt = Give me feedback yes/no/partial on following questions
                 1. Was the agent greeted customer?
                 2. Did the agent understood the problem of the customer?
                 3. Was the agent able to handle objections?
                 4. Was the agent engaged with the customer through out call?
                 5. Was the resolution provided in the first call?
        '''
        ######sample1
        #audio_text='cust: I have a problem \n agent: how can I help \n cust: my laptop has been really slow lately\n agent: lets check for background processes and running applications, and optimize your startup programs\n Resolved: Yes'
        ######sample2
        #audio_text='cust: Need assistance \n agent: whats the issue \n cust: my Wi-Fi keeps dropping \n agent: try resetting your router, and if that doesnt work, we can troubleshoot further \n Resolved: No'
        ######sample3
        #audio_text='cust: Facing trouble \n agent: please explain \n cust: my printer wont print \n agent: ensure theres enough paper, check for any paper jams, and restart both your printer and computer \n Resolved: Yes'
        ######sample4
        #audio_text='cust: Help needed \n agent: Im here \n cust: I accidentally deleted an important document \n agent: check your recycle bin, and if its not there, we can try data recovery tools \n Resolved: No'
        ######sample5
        #audio_text='cust: Technical issue \n agent: tell me more \n cust: my phones battery drains very fast \n agent: lets analyze your battery usage, close unnecessary background apps, and consider replacing the battery if needed \n Resolved: Yes'
        ######sample6 - all together
        #audio_text='cust: I have a problem \n agent: how can I help \n cust: my laptop has been really slow lately \n agent: lets check for background processes and running applications, and optimize your startup programs \n Resolved: Yes \n cust: Need assistance \n agent: whats the issue \n cust: my Wi-Fi keeps dropping \n agent: try resetting your router, and if that doesnt work, we can troubleshoot further \n Resolved: No \n cust: Facing trouble \n agent: please explain \n cust: my printer wont print \n agent: ensure theres enough paper, check for any paper jams, and restart both your printer and computer \n Resolved: Yes \n cust: Help needed \n agent: Im here \n cust: I accidentally deleted an important document \n agent: check your recycle bin, and if its not there, we can try data recovery tools \n Resolved: No \n cust: Technical issue \n agent: tell me more \n cust: my phones battery drains very fast \n agent: lets analyze your battery usage, close unnecessary background apps, and consider replacing the battery if needed \n Resolved: Yes'
        print(audio_text)
        
        response = openai.Completion.create(
            engine="text-davinci-002",  # You can choose a different engine based on your needs
            prompt=prompt+audio_text,
            max_tokens=100  # Adjust max_tokens based on your desired response length
        )
        print(response)
        
        # Extract and print the generated text from the API response
        generated_text = response['choices'][0]['text']
        print(generated_text)
        return jsonify({'text': audio_text,'ke': generated_text})

    return jsonify({'error': 'Invalid file format'})

if __name__ == '__main__':
    app.run(debug=True)


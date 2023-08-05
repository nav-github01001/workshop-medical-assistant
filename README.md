## Note

This repository is archived.  You can still fork it but this repository wont recieve updates. 
# Bootcamp Medical Assistant
Medical assistant using OpenAI API in python

Idea: Personalized AI Health Assistant for Chronic Disease Management

### Problem
Chronic diseases, such as diabetes, hypertension, asthma, and heart disease, affect a large population worldwide. Managing these conditions effectively requires continuous monitoring, adherence to treatment plans, and lifestyle modifications. However, patients often struggle to keep up with their healthcare routine and might not have access to real-time medical advice.

Solution: Our vision is to develop a personalized AI health assistant that uses cutting-edge machine learning and natural language processing technologies to support patients in managing their chronic conditions effectively. This AI health assistant will provide personalized recommendations, monitor health parameters, offer medication reminders, and deliver timely health-related insights to users.

### Implementation

Medication Reminders and Adherence:The AI assistant will send personalized medication reminders to patients, ensuring they take their prescribed medications on time. It will also monitor adherence and provide motivational messages to encourage compliance.

Lifestyle Recommendations: Understanding the impact of lifestyle choices on chronic conditions, the AI assistant will offer personalized lifestyle recommendations, including diet plans, exercise routines, and stress management techniques, tailored to the individual's needs.

Communication Channel: Utilizing advanced natural language processing capabilities, the AI assistant will communicate with patients in a conversational manner, allowing users to ask questions, seek clarification, or discuss health concerns comfortably.

### Benefits

Improved Disease Management: With the support of our personalized AI health assistant, patients can take charge of their health, leading to better disease management outcomes and improved quality of life.

Enhanced Patient Engagement:Medication reminders and interactive communication will empower patients to actively engage in their healthcare routine and make informed decisions.

Reduced Healthcare Burden: By assisting patients in managing chronic conditions effectively, our AI health assistant has the potential to reduce hospital readmissions and alleviate the overall burden on the healthcare system.

## The Project
This project is divided into two parts: The Frontend and The Backend

The backend uses Python and SQLite(for prototyping) and the frontend is made using CSS,HTML,vanilla JS

### Process
The backend uses OpenAI API at its core [GPT-3.5], SQLite for conversational history.

Once a message is sent, it is sent to OpenAI which then creates a response which we add to our database (for conversational history). This data is not used for training and is automatically discarded after reaching 20 conversations (although the same cannot be said of OpenAI. Read the [DISCLAIMER](#disclaimer))

### How to run it locally
First, clone the repository 
```sh
git clone https://github.com/nav-github01001/workshop-medical-assistant
cd workshop-medical-assistant
```


**Note: This assumes you are running Windows as your OS, with Vanilla Python and have installed Git in your system**


You will need `python>=3.10` to run it

1. To run it,first install the dependencies

For PyArgon2, library that enables password storage, MSVC is required 

```sh
pip install -r requirements.txt
```



2. Configurations:

Make a new file `config.toml`

Then, you need to create an api key from OpenAI. Create it [here](https://platform.openai.com/account/api-keys)

After that,create a secret key with random numbers,characters

After that, put this in `config.toml`

```toml
openai_api_key = [YOUR OPENAI API KEY HERE]
token_secret = [YOUR SECRET KEY HERE]
```

3. Then, run this

```sh 
py start.py
py ./backend/web_server.py
```

That simple!

#### Install in Linux/Virtual Environment (venv)

**Note: Due to [PEP668](https://peps.python.org/pep-0668/), Linux installs can only be performed in venv to prevent breaking system packages**


##### For the quick and dirty:

1. Go to the directory where you cloned this repo:

``` sh
python3 -m venv YourBotEnvName
```

2. Activate the venv
If you don't know how to see it [here](https://docs.python.org/3/library/venv.html)

Follow the instructions given above

## DISCLAIMER
Our AI health assistant is designed to complement professional medical advice, not replace it. Patients should always be encouraged to consult with healthcare professionals for any specific medical concerns or emergencies. ***Additionally, we use a third-party [OpenAI] for the chatbot capabilities and they might use the data for training***

## LICENSE

This project is licensed with the MIT License.
import pandas as pd
import re
import openai
from lingua import LanguageDetectorBuilder

def chat(system, user_assistant, classification):
    assert isinstance(system, str), "`system` should be a string"
    assert isinstance(user_assistant, list), "`user_assistant` should be a list"
    system_msg = [{"role": "system", "content": system}]
    user_assistant_msgs = [
        {"role": "assistant", "content": user_assistant[i]} if i % 2 else {"role": "user", "content": user_assistant[i]}
        for i in range(len(user_assistant))]

    msgs = system_msg + user_assistant_msgs
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=msgs)
    status_code = response["choices"][0]["finish_reason"]
    assert status_code == "stop", f"The status code was {status_code}."
    return response["choices"][0]["message"]["content"], classifications[classification]

def detect_language(text):
    detector = LanguageDetectorBuilder.from_all_languages().build()
    language = detector.detect_language_of(text)
    return language.iso_code_639_1.name if language else 'N/A'


classifications = {
    "RFI": "Requests for specific, mostly non-publicly available information from a particular company...",
    "RFQ": "Inquiries regarding a general need for products or services that could potentially be met by a variety of providers...",
    "Donations": "Calls and requests for financial or in-kind donations, typically for non-profit organizations and charitable purposes..."
}

# df = pd.read_csv('LLM_02.csv', nrows=2)
df = pd.read_csv('LLM_02.csv')
df['language'] = ''

df['message'] = df['message'].apply(lambda x: re.sub(r'\b\w+@\w+\.\w+\b', 'email', x))
df['message'] = df['message'].apply(lambda x: re.sub(r'\d', '0', x))

for idx, row in df.iterrows():
    message = row['message']
    language = detect_language(message)
    df.loc[idx, 'language'] = language
    df['language'] = df['language'].astype(str)
    # system_message = f"Classify the following message: '{message}'"
    # user_assistant = [system_message]
    # classification, description = chat(system_message, user_assistant, row['label_class_human'])
    # df.loc[idx, 'label_class_llm_x'] = classification
    # df.loc[idx, 'description'] = description
    # if classification != row['label_class_human']:
    #     system_message = f"Why did you classify the message as '{classification}' instead of '{row['label_class_human']}'?"
    #     user_assistant = [system_message]
    #     improvement_idea = chat(system_message, user_assistant, row['label_class_human'])
    #     df.loc[idx, 'improvement_ideas'] = improvement_idea

df.to_csv('updated_file.csv', index=False)

import requests
from Doctor.searching import to_check_querr
import datetime


def doctor_call(name, number,mail,contact_id):
    # TODO: Move these to environment variables for better security
    auth_token = '0f4fbb74-f6df-4b5f-83dc-6e7f380e6cf0'
    phone_number_id = "e40be9bc-0eda-468d-b414-7ee56f71529b"

    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }
    data = {
        'assistant': {
        "firstMessage":"Hello, This is simran, thank you for calling Apollo Hospitals, Banglore. How can I assist you today?",
        
        "model": {
            "provider": "openai",
            "model": "gpt-4",
            "knowledgeBaseId": "339dc0b7-e333-413e-a977-4439e863c043",
            "messages": [
                {
                    "role": "system",
                    "content": f'''You are simran a front desk at Apollo hospital , currently the time is {current_time} and date is {now}.user's name is {name} .ask questions one by one after taking the user response don't ask all the questions at once Your task is to clear the user query , book appointments and give reccomendations in medical field . If the user asks any question other than the medical field or hospital just say that you called at Apollo hospital please check the number . Don't say redundantly sorry even if it is your mistake or anything else.give intutive answers , act like a human receptionist don't say that you are a n ai or live in digital world . Don't talk about anything other than the medical field or apollo hospital.keep your answers short.Don't say sorry or appolize redundantly or agin and again.  Take help from external context also . 
                    '''
                }
            ]
        },
        "voice": {
            "provider": '11labs',
            "voiceId": "ftDdhfYtmfGP0tFlBYA1",
        },
        "backgroundSound":'office',
        },
        'phoneNumberId': phone_number_id,
        'type': 'outboundPhoneCall',
        'customer': {
            'number': number,
            'name': name 
        },  
    }  
    

    try:
        response = requests.post(
            'https://api.vapi.ai/call/phone', headers=headers, json=data)
        
        response_data = response.json()
        print(response_data)   
        call_id = response_data.get('id')
        print("got the id")
        print("calling to check querry")
        querry=to_check_querr(call_id,mail,number,name,contact_id)
        print("checked querry")
        return response_data
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return {"error": f"Network error: {str(e)}"}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": str(e)}


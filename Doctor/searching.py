import requests
from Doctor.send_mail import send_mail
from Doctor.groqmodel import groq_suum
from Doctor.whatsapp import create_pdf
from Doctor.add_summary_call_back import update_summary
def to_check_querr(call_id,mail,number,name,contact_id):
  auth_token = '0f4fbb74-f6df-4b5f-83dc-6e7f380e6cf0'
  url = f"https://api.vapi.ai/call/{call_id}"
  headers = {
      'Authorization': f'Bearer {auth_token}',
      'Content-Type': 'application/json',
  }
  while True:
    response = requests.get(url, headers=headers)
    trans = response.json()
    print(trans[ 'monitor']['listenUrl'])
    print(trans['transport'])
    print(trans['status'])
    if trans['status'] =='ended' :
      try:
        transcript= trans['transcript']
        print("data")
        dat=groq_suum(transcript,name) 
        print("mailing")# for now like hospital data only
        send_mail(dat,mail,"Your appointment details")
        update_summary(contact_id,dat)
        create_pdf(number,dat)
        return "Success"
      except Exception as e:
         print(f"An error occurred: {e}")
         return "Error occurred"

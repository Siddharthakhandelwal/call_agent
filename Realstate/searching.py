import requests
from Realstate.send_mail import send_mail
from Realstate.groq_summarizer import groq_suum
from Realstate.whatsapp import create_pdf,send_image
from Realstate.groq_image import groq_image
from Realstate.search_and_download import main
from general.groq_date import groq_date
from general.supabase_general import update_callback_time,update_summary
def to_check_querr(name,call_id,mail,number,contact_id):
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
        data=groq_suum(transcript,name) 
        call_back=groq_date(transcript)
        create_pdf(number,data)
        image=groq_image(transcript)
        update_summary(contact_id,data)
        if "none" not in call_back or "None" not in call_back:
            update_callback_time(call_id,call_back)
        if image != "None":
          main(image)
          array=send_image(number)
          send_mail(data,mail,"Documents that you asked for",array)
      except Exception as e:
         print(f"An error occurred: {e}")
         return "Error occurred"
      return "Success"
    

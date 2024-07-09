from django.shortcuts import render
from django.http import JsonResponse
import openai
import os
import traceback

openai.api_key = os.getenv("OPENAI_API_KEY")

def index(request):
    return render(request, 'index.html')

def get_response(request):
    if request.method == 'POST':
        try:
            user_message = request.POST.get('message')
            if not user_message:
                raise ValueError("Message cannot be empty")

            print(f"User message: {user_message}")
            print(f"OpenAI API Key: {openai.api_key}")

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message}
                ]
            )
            chatbot_response = response.choices[0].message['content'].strip()
            print(f"Chatbot response: {chatbot_response}")

            return JsonResponse({'response': chatbot_response})

        except Exception as e:
            print(f"Error: {e}")
            print(traceback.format_exc())
            return JsonResponse({'response': 'Error processing your request.'}, status=500)

    return JsonResponse({'response': 'Invalid request method.'}, status=400)


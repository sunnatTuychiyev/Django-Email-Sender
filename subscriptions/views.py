from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.conf import settings

def subscribe(request):
    if request.method == 'POST':
        # Foydalanuvchi kiritgan subject va message
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        file = request.FILES.get('file')  # Yuklangan .txt faylni olish

        if file and file.name.endswith('.txt'):
            # Fayldagi barcha email manzillarni o'qish
            email_list = file.read().decode('utf-8').splitlines()
            
            # Har bir email uchun xabar yuborish
            for recipient in email_list:
                if recipient:  # Bo'sh email manzillarni o'tkazib yuborish
                    email = EmailMessage(
                        subject,
                        message,
                        settings.EMAIL_HOST_USER,
                        [recipient],
                    )
                    # Emailni yuborish
                    email.send(fail_silently=False)
            
            messages.success(request, 'Emails have been sent successfully!')
        else:
            messages.error(request, 'Please upload a valid .txt file containing email addresses.')
        
        return redirect('subscribe')
    
    return render(request, 'subscriptions/home.html')

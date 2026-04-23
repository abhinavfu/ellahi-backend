from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .serializers import ContactSerializer
from django.conf import settings

class ContactView(APIView):
    def post(self, request):
        serializer = ContactSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            # Send email
            subject = f"New Contact Form Submission from {data['name']}"
            from_email = settings.EMAIL_HOST_USER
            to_email = settings.EMAIL_HOST_TO
            
            # Render HTML email
            html_message = render_to_string('contact/contact_email.html', {
                'name': data['name'],
                'email': data['email'],
                'phone': data.get('phone', ''),
                'service': data.get('service', ''),
                'message': data['message'],
                'time': data.get('time', ''),
            })
            
            email = EmailMessage(
                subject=subject,
                body=html_message,
                from_email=from_email,
                to=[to_email],
            )
            
            try:
                email.content_subtype = 'html'  # Set email to HTML
                email.send()
            except Exception as e:
                print("EMAIL ERROR:", str(e))
                return Response({"error": "Failed to send email"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

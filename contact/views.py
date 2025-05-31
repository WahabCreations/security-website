from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ContactSubmissionSerializer
from .models import ContactSubmission

class ContactFormView(APIView):
    def post(self, request, format=None):
        serializer = ContactSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            # Save to database
            contact = serializer.save()
            
            # Render HTML email template
            email_html = render_to_string('email/contact_template.html', {
                'name': contact.name,
                'email': contact.email,
                'phone': contact.phone if contact.phone else 'Not provided',
                'message': contact.message,
            })
            
            # Render confirmation email template
            confirmation_html = render_to_string('email/confirmation_template.html', {
                'name': contact.name,
            })
            
            try:
                # Send professional email to admin
                admin_email = EmailMessage(
                    subject=f"New Contact Form Submission from {contact.name}",
                    body=email_html,
                    from_email='info@zeesecurity.co.uk',
                    to=['info@zeesecurity.co.uk'],
                    reply_to=[contact.email],
                )
                admin_email.content_subtype = "html"
                admin_email.send()
                
                # Send confirmation to user if email was provided
                if contact.email:
                    confirmation_email = EmailMessage(
                        subject="Thank you for contacting Zee Security",
                        body=confirmation_html,
                        from_email='info@zeesecurity.co.uk',
                        to=[contact.email],
                    )
                    confirmation_email.content_subtype = "html"
                    confirmation_email.send()
                
                return Response(
                    {"message": "Form submitted successfully"}, 
                    status=status.HTTP_201_CREATED
                )
                
            except Exception as e:
                # Log the error but still return success since data is saved
                print(f"Email sending failed: {str(e)}")
                return Response(
                    {"message": "Form submitted but email failed to send. We'll contact you soon."},
                    status=status.HTTP_201_CREATED
                )
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
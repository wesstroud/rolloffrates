import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logger = logging.getLogger("junk_king_scraper")

class EmailNotifier:
    """
    Utility class to send email notifications for errors or completion.
    """
    def __init__(self, smtp_server, smtp_port, username, password, sender_email):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.sender_email = sender_email
    
    def send_notification(self, recipient_email, subject, message_body, is_html=False):
        """
        Send an email notification.
        
        Args:
            recipient_email (str): Email address of the recipient
            subject (str): Email subject
            message_body (str): Email body content
            is_html (bool): Whether the message body is HTML
        
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            if is_html:
                msg.attach(MIMEText(message_body, 'html'))
            else:
                msg.attach(MIMEText(message_body, 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            logger.info(f"Email notification sent to {recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email notification: {str(e)}")
            return False
    
    def send_error_notification(self, recipient_email, error_message, details=None):
        """
        Send an error notification email.
        
        Args:
            recipient_email (str): Email address of the recipient
            error_message (str): Brief error message for the subject
            details (str, optional): Detailed error information for the body
        """
        subject = f"Junk King Scraper Error: {error_message}"
        body = f"The Junk King price scraper encountered an error:\n\n{error_message}"
        
        if details:
            body += f"\n\nDetails:\n{details}"
        
        return self.send_notification(recipient_email, subject, body)
    
    def send_completion_notification(self, recipient_email, stats):
        """
        Send a completion notification email with statistics.
        
        Args:
            recipient_email (str): Email address of the recipient
            stats (dict): Dictionary containing statistics about the scraping run
        """
        subject = "Junk King Scraper: Monthly Run Completed"
        
        body = "The monthly Junk King price scraping job has completed.\n\n"
        body += f"Total cities processed: {stats.get('total', 0)}\n"
        body += f"Successful: {stats.get('success', 0)}\n"
        body += f"No service available: {stats.get('no_service', 0)}\n"
        body += f"Errors: {stats.get('error', 0)}\n\n"
        
        if stats.get('error', 0) > 0:
            body += "There were some errors during the scraping process. Please check the logs for details."
        
        return self.send_notification(recipient_email, subject, body)

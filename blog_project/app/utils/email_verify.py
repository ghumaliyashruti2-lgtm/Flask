from email.mime.text import MIMEText
import smtplib 
import re
 
# ==================
# EMAIL VALIDATION 
# ================== 

def valid_email(email):

    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if re.match(pattern, email):
        return True
    return False


# ================
# OTP SEDN 
# ================
 
def send_otp_email(receiver, otp):

    sender = "ghumaliyashruti2@gmail.com"
    password = "wxtx wbvm ygri ffei" # APP PASSWORD

    msg = MIMEText(f"Your OTP is: {otp}")
    msg["Subject"] = "Email Verification OTP"
    msg["From"] = sender
    msg["To"] = receiver

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)

    server.sendmail(sender, receiver, msg.as_string())
    server.quit()
    

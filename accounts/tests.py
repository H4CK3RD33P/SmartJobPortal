from django.test import TestCase
import cv2
import mediapipe
from deepface import DeepFace
import os
from jobportal.settings import BASE_DIR
import smtplib
from email.message import EmailMessage
import mimetypes
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import time

# Create your tests here.
def is_jobseeker(user):
    if user.groups.filter(name='jobseeker').exists():
        return True
    else:
        return False

def is_employer(user):
    if user.groups.filter(name='employer').exists():
        return True
    else:
        return False

def is_unauthenticated_user(user):
    if user.is_authenticated:
        return False
    else:
        return True

def is_authenticated_user(user):
    if user.is_authenticated:
        return True
    else:
        return False


def is_unauthenticated_employer(user):
    if user.groups.filter(name='employer').exists() and user.is_authenticated:
        return False
    else:
        True

def is_unauthenticated_jobseeker(user):
    if user.groups.filter(name='jobseeker').exists() and user.is_authenticated:
        return False
    else:
        True
def capture_and_verify(profilepic):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
    cam = cv2.VideoCapture(0)
    mpHands = mediapipe.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mediapipe.solutions.drawing_utils
    while True:
        _,img=cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 1)
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        multihandlandmarks = results.multi_hand_landmarks
        if multihandlandmarks:
            for handlandmarks in multihandlandmarks:
                mpDraw.draw_landmarks(img,handlandmarks,mpHands.HAND_CONNECTIONS)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(img,"Hit 'Spacebar' to click your photo",(50,450),cv2.FONT_HERSHEY_SIMPLEX,
                    1,(0,0,255),thickness=3)
        cv2.putText(img,"LOGIN VERIFICATION",(50,25),cv2.FONT_HERSHEY_SIMPLEX,
                    1,(0,0,255),thickness=2)
        cv2.imshow("test",img)
        k = cv2.waitKey(1)
        if k==32:
            filepath = f"{os.getcwd()}/media/images/current.jpg"
            cv2.imwrite(filepath,img)
            break
    cam.release()
    cv2.destroyAllWindows()
    cwd = os.getcwd()+profilepic
    user = DeepFace.verify(img,cwd)
    return user['verified']

def create_and_send_email(recipient,subject,content,attachment=None):
    sender = 'sender@gmail.com'
    password = 'senderpassword'
    mail_server = smtplib.SMTP_SSL('smtp.gmail.com')
    mail_server.login(sender,password)

    email = EmailMessage()
    email['To'] = recipient
    email['From'] = sender
    email['Subject'] = subject
    email.set_content(content)

    if attachment is not None:
        filename = os.path.basename(attachment)
        mime_full_type,_ = mimetypes.guess_type(attachment)
        mime_type,sub_type = mime_full_type.split('/')
        with open(attachment,'rb') as attached_file:
            email.add_attachment(attached_file.read(),
                                maintype=mime_type,
                                subtype= sub_type,
                                filename=filename)

    mail_server.send_message(email)
    mail_server.quit()

def createjobbrochure(job):
    now = time.strftime("%Y-%m-%d-%H-%M-%S",time.gmtime())
    filename = f"{os.getcwd()}/media/documents/{job.title}{now}.pdf"
    brochure = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    brochure_title = Paragraph(f"{job.title}, {job.employer.organization}",styles['h1'])
    location = Paragraph(f"{job.location}, {job.job_type}, {job.operation_type}",styles['h2'])
    head_a = Paragraph("Duration per day (in hours): ", styles['h3'])
    duration = Paragraph(f"{job.duration_per_day}",styles['Normal'])
    head_b = Paragraph("Responsibilities: ", styles['h3'])
    responsibilities = Paragraph(f"{job.responsibilities}",styles['Normal'])
    head_c = Paragraph("Salary (Lakhs per annum in Rs.): ", styles['h3'])
    salary= Paragraph(f"{job.salary_in_LPA}",styles['Normal'])
    head_d = Paragraph("Eligibility: ", styles['h3'])
    eligibility = Paragraph(f'''{job.eligibility}''',styles['Normal'])
    head_e = Paragraph("Preferred: ", styles['h3'])
    preferred = Paragraph(f'''{job.preferred}''',styles['Normal'])
    brochure.build([brochure_title,location,
                    head_a,duration,
                    head_b,responsibilities,
                    head_c,salary,
                    head_d,eligibility,
                    head_e,preferred])
    
    return filename
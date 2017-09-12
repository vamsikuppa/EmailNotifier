# -*- coding: utf-8 -*-
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime


ranCDRM=False
ranStarter=False

def send_mail(finalList):
    # me == my email address
    # you == recipient's email address
    todaysDate = datetime.datetime.today().strftime('%d-%b')
    me = "vamsi.k.kuppa@oracle.com"
    recipients = ['vamsi.k.kuppa@oracle.com','shashank.sahay@oracle.com','ankita.yerawar@oracle.com','anudeep.tangudu@oracle.com','kalva.avinash@oracle.com']
    #you = "sasasriv_org_ww@oracle.com"
    #you = "vamsi.k.kuppa@oracle.com"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Automation Notifier - " + todaysDate
    msg['From'] = me
    msg['To'] = ", ".join(recipients)
    #msg['To'] = you
    # Create the body of the message (a plain-text and an HTML version).
    text = "#DispositionsDUE Today: Please find the priorities below:"
    html = """\
    <html xmlns:o="http://www.w3.org/1999/xhtml">
    <head>
    
        <meta http-equiv="content-type" content="text/html; charset=utf-8">
    </head>
    <body text="#000000" bgcolor="#FFFFFF">
    <div class="moz-forward-container"><br>
        <div class="moz-forward-container"><br>
            <div class="moz-forward-container">
                <div class="moz-forward-container">
                        <div class="moz-forward-container">
                            <div class="moz-forward-container">
                                <div class="moz-forward-container">
                                    <div class="moz-forward-container">
                                        <div class="moz-forward-container">
                                            <div class="WordSection1">
                                                <div>
                                                    <p><span style="color:rgb(255,0,0);"> <strong>#DispositionsDUE
                                      Today: Please find the priorities
                                      below</strong></span></p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    </body>
    </html>
    """
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')

    # Attach parts into message container.
    msg.attach(part1)
    #To encode in utf-8
    # Attach based on the list length and return the HTML Message of UL List in each iteration
    run_once = False  # Flag to run the analysis date only once
    chunks = []
    stringChunks = ""
    mutipleTabRows=[]
    for i,el in reversed(list(enumerate(finalList))):
        flag = False # Counter to break inner loop
        for el1 in el:
            if (isinstance(el1, list)):
                chunks.append(generate_html_for_preflight_list(el)) # Pass the preflight table details
                run_once = True
                break
            else: #Check here whether the next el[i++] is also a table row, if present append it
                if(run_once == True):
                    chunks.append(append_analysisdate_for_dte_list(el)) #Append analysis date once
                    run_once = False
                chunks.append(generate_html_for_dte_list(el))  # Pass on the dte table details
                #if(ranCDRM==True):

                flag = True
                break
        if(flag==True):
            continue
            # As per doc https://docs.python.org/3/faq/programming.html#what-is-the-most-efficient-way-to-concatenate-many-strings-together
    for i, x in enumerate(chunks):
        stringChunks = stringChunks + str(x)
    listHtml1 = html + stringChunks
    part3 = MIMEText(listHtml1, 'html')
    msg.attach(part3)  # ****** This is Working :)
    s = smtplib.SMTP_SSL('stbeehive.oracle.com')
    s.login(me, "Skyfall@1")
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    #s.sendmail(me, you, msg.as_string())
    s.sendmail(me, recipients, msg.as_string())
    s.quit()


def generate_html_for_dte_list(finalList1):
    #*****Have to write logic to handle both CDRM and starter list of lists
    # if(finalList[3]=='STARTER') write logic here to append the starter dte id
    # if(finalList[3] == 'CDRM') write logic here to append the CDRM dte id
    # [x.encode('utf-8') for x in finalList1]
    try:
        envType = str(finalList1[3].encode('utf-8'))
    except IndexError:
        print "Env Type Index Error occurred"
    if(envType == "CDRM"):
        msg = """<li>CDRM: <a href="http://preflightmanager.us.oracle.com/apex/f?p=121:14:7285005355584:5541213953682:NO::P14_DTE_ID,P14_RERUN_ID:{},1">{}</a></li>
                    </ul></ul>
                    """.format(finalList1[0].encode('utf-8'),finalList1[0].encode('utf-8'))
        ranCDRM=True
        #return msg
    else:
        msg = """<ul><ul><li>STARTER: <a href="http://preflightmanager.us.oracle.com/apex/f?p=121:14:7285005355584:5541213953682:NO::P14_DTE_ID,P14_RERUN_ID:{},1">{}</a></li>
                </ul></ul></ul></ul>
                """.format(finalList1[0].encode('utf-8'),finalList1[0].encode('utf-8'))
        ranStarter=True
        #return msg
    return msg

def generate_html_for_preflight_list(finalList2):
    finalList3=[]
    for x in finalList2:
        flag = False
        for x1 in x:
            flag = True
            finalList3.append(x1.encode('utf-8'))
        if(flag == True):
            continue
    #finalList3 now contains data encoded in utf-8
    msg="""<ul type="disc"><li>Preflight: {}</li>
    <ul><li>Purpose: {}</li>
    """.format(finalList3[0],finalList3[3])
    return msg


def append_analysisdate_for_dte_list(finalList1):
    msg = """<li class="MsoNormal" style="mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;mso-list:l2level1 lfo2">
                    <font color="#ff0000">Analysis due date: {}</font></li>
                    """.format(str(finalList1[7].encode('utf-8')).decode('utf-8').replace(u"\xa0"," ").encode('utf-8')) # To replace ascii character
    return msg


def close_two_uls():
    msg="""</ul></ul>"""
def close_three_uls():
    msg="""</ul></ul></ul>"""


#Code to get preflight label
# def getP4faLabel():
#     s = requests.session()
#     s.get()
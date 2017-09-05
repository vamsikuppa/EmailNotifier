# -*- coding: utf-8 -*-
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime


def send_mail(finalList):
    # me == my email address
    # you == recipient's email address
    todaysDate = datetime.datetime.today().strftime('%d-%b')
    me = "vamsi.k.kuppa@oracle.com"
    #recipients = ['vamsi.k.kuppa@oracle.com','shashank.sahay@oracle.com']
    #you = "sasasriv_org_ww@oracle.com"
    you = "vamsi.k.kuppa@oracle.com"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Automation Notifier - " + todaysDate
    msg['From'] = me
    #msg['To'] = ", ".join(recipients)
    msg['To'] = you
    # Create the body of the message (a plain-text and an HTML version).
    text = "#Critical items (immediate action): Highlighted in blue" \
           "#Important/Please Note*:" \
           "[ Hard Deadline ] - (FINC Code Only) Merge your unstable by 09/08" \
           "REL 13.17.11A unstable pass are being discussed in Meg's 4pm meeting."
    html = """\
    <!DOCTYPE html>
<html xmlns:o="http://www.w3.org/1999/xhtml">
<head>

    <meta http-equiv="content-type" content="text/html; charset=utf-8">
</head>
<body text="#000000" bgcolor="#FFFFFF">
<div class="moz-forward-container"><br>
    <div class="moz-forward-container"><br>
        <div class="moz-forward-container">
            <div class="moz-forward-container">
                <div class="moz-forward-container"> #Critical items
                    (immediate action): Highlighted in <span
                            style="color:#3333FF">blue</span>
                    <o:p></o:p>
                    <div class="moz-forward-container">
                        <div class="moz-forward-container">
                            <div class="moz-forward-container">
                                <div class="moz-forward-container">
                                    <div class="moz-forward-container">
                                        <div class="WordSection1">
                                            <div>
                                                <p><strong><span style="color:red">#Important/Please
                                  Note</span></strong><span
                                                        style="color:red">:</span>
                                                    <o:p></o:p>
                                                </p>
                                                <ul type="disc">
                                                    <ul type="circle">
                                                        <li class="MsoNormal"
                                                            style="mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;mso-list:l6
                                  level2 lfo1"><font color="#3333ff">[
                                                            Hard Deadline ] - (FINC Code Only)
                                                            Merge your unstable by 09/08</font></li>
                                                        <li class="MsoNormal"
                                                            style="mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;mso-list:l6
                                  level2 lfo1">REL 13.17.11A unstable
                                                            pass are being discussed in Meg's 4pm
                                                            meeting.
                                                        </li>
                                                    </ul>
                                                </ul>
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
    for i,el in reversed(list(enumerate(finalList))):
        flag = False # Counter to break inner loop
        for el1 in el:
            if (isinstance(el1, list)):
                chunks.append(generate_html_for_preflight_list(el)) # Pass the preflight table details
                run_once = True
                break
            else:
                if(run_once == True):
                    chunks.append(append_analysisdate_for_dte_list(el)) #Append analysis date once
                    run_once = False
                chunks.append(generate_html_for_dte_list(el))  # Pass on the dte table details
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
    # else:
    #     chunks.append(generate_html_for_dte_list(finalList[0]))  # Pass on the dte table details
    #     # As per doc https://docs.python.org/3/faq/programming.html#what-is-the-most-efficient-way-to-concatenate-many-strings-together
    #     # listHtml1 = html.join(chunks) # The original
    #     stringChunks = ""
    #     for i, x in enumerate(chunks):
    #         stringChunks = stringChunks + str(x)
    #     listHtml1 = html + stringChunks
    #     part3 = MIMEText(listHtml1, 'html')
    #     msg.attach(part3)  # ****** This is Working :)
    # Send the message via local SMTP server.
    s = smtplib.SMTP_SSL('stbeehive.oracle.com')
    s.login(me, "Skyfall@1")
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(me, you, msg.as_string())
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
        msg = """<ul type="circle"><a href="http://preflightmanager.us.oracle.com/apex/f?p=121:14:7285005355584:5541213953682:NO::P14_DTE_ID,P14_RERUN_ID:{},1"><li>CDRM: {}</li></a>
                    </ul>
                    """.format(finalList1[0].encode('utf-8'),finalList1[0].encode('utf-8'))  # ****For testing purpose only #For dates use encode('utf-8')
        return msg
    else:
        msg = """<ul type="circle"><a href="http://preflightmanager.us.oracle.com/apex/f?p=121:14:7285005355584:5541213953682:NO::P14_DTE_ID,P14_RERUN_ID:{},1"><li>STARTER: {}</li></a>
                </ul></ul></body></html>
                """.format(finalList1[0].encode('utf-8'),finalList1[0].encode('utf-8'))  # ****For testing purpose only #For dates use encode('utf-8')
        return msg

def generate_html_for_preflight_list(finalList2):
    #Encoding problem here
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
    <ul><li>Purpose: {}</li></ul>
    """.format(finalList3[0],finalList3[3])
    return msg


def append_analysisdate_for_dte_list(finalList1):
    msg = """<ul><li class="MsoNormal" style="mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;mso-list:l2level1 lfo2">
                    <font color="#ff0000">Analysis due date: {}</font></li></ul>
                    """.format(str(finalList1[7].encode('utf-8')).decode('utf-8').replace(u"\xa0"," ").encode('utf-8')) # To replace ascii character
    return msg



#Code to remove duplicates
#def cleanup_list(finalList):

#Code to get preflight label
# def getP4faLabel():
#     s = requests.session()
#     s.get()
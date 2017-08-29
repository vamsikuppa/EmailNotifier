import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime


def send_mail(finalList):
    # me == my email address
    # you == recipient's email address
    todaysDate = datetime.datetime.today().strftime('%d-%b')
    me = "vamsi.k.kuppa@oracle.com"
    you = "vamsi.k.kuppa@oracle.com"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Automation Notifier - " + todaysDate
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    text = "#Critical items (immediate action): Highlighted in blue #Important/Please Note:" \
           "Teams please find the new update process for Mergedown runs -->> ALM Update process" \
           "Please note : this process is applicable only for FINC mergedown runs." \
           "Teams, please tag all 17.11 Merge Down bugs with below tags." \
           "1711_P4FA FIN bug having Techstack bug as Base bug" \
           "1711_FAAT : For testware fixes bugs Merge Down dashboard " \
           "1711A CDRM Environment will be patching to 0823.0831 label today"
    html = """\
    <html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body bgcolor="#FFFFFF" text="#000000">
<div class="moz-forward-container">
    <div class="moz-forward-container">
        <div class="moz-forward-container">
            <meta http-equiv="content-type" content="text/html;
            charset=utf-8">
            <br>
            #Critical items (immediate action): Highlighted in <span
                style="color:#3333FF">blue</span>
            <o:p></o:p>
            <div class="moz-forward-container">
                <div class="moz-forward-container">
                    <div class="moz-forward-container">
                        <div class="moz-forward-container">
                            <div class="moz-forward-container">
                                <div class="WordSection1">
                                    <div>
                                        <p><strong><span
                                                style="color:red">#Important/Please
                                                      Note</span></strong><span
                                                style="color:red">:</span>
                                            <o:p></o:p>
                                        </p>
                                        <ul type="disc">
                                            <ul type="circle">
                                                <li
                                                        class="MsoNormal"
                                                        style="mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;mso-list:l6
                                                      level2 lfo1">Teams
                                                    please find the
                                                    new update process
                                                    for Mergedown runs
                                                    --&gt;&gt; <a
                                                            moz-do-not-send="true"
                                                            href="https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=81464107">ALM
                                                        Update
                                                        process</a>
                                                    <o:p></o:p>
                                                </li>
                                                <li
                                                        class="MsoNormal"
                                                        style="mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;mso-list:l6
                                                      level2 lfo1">Please
                                                    note : this
                                                    process is
                                                    applicable only
                                                    for FINC mergedown
                                                    runs.
                                                    <o:p></o:p>
                                                </li>
                                                <li
                                                        class="MsoNormal"
                                                        style="mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;mso-list:l6
                                                      level2 lfo1"><span
                                                        style="color:#3366FF">Teams, please tag all 17.11 Merge Down bugs with
                                                        below tags. </span>
                                                    <o:p></o:p>
                                                </li>
                                            </ul>
                                        </ul>
                                        <ul type="disc">
                                            <ul type="circle">
                                                <ul type="square">
                                                    <li
                                                            class="MsoNormal"
                                                            style="mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;mso-list:l6
                                                        level3 lfo1"><span
                                                            style="color:#3366FF">1711_P4FA FIN bug having Techstack bug as Base
                                                          bug</span>
                                                        <o:p></o:p>
                                                    </li>
                                                    <li
                                                            class="MsoNormal"
                                                            style="mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;mso-list:l6
                                                        level3 lfo1"><span
                                                            style="color:#3366FF">1711_INTERMITTENT : For all product intermittent,
                                                          setup issues
                                                          bugs</span>
                                                        <o:p></o:p>
                                                    </li>
                                                    <li
                                                            class="MsoNormal"
                                                            style="mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;mso-list:l6
                                                        level3 lfo1"><span
                                                            style="color:#3366FF">1711_FA: For code fixes bugs</span>
                                                        <o:p></o:p>
                                                    </li>
                                                    <li
                                                            class="MsoNormal"
                                                            style="mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;mso-list:l6
                                                        level3 lfo1"><span
                                                            style="color:#3366FF">1711_FAAT : For testware fixes bugs</span>
                                                    </li>
                                                </ul>
                                                <li
                                                        class="MsoNormal"
                                                        style="mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;mso-list:l6
                                                      level2 lfo1"><a
                                                        moz-do-not-send="true"
                                                        href="https://rms.us.oracle.com/analytics/saw.dll?Dashboard&amp;PortalPath=%2Fshared%2FFUSION%3AFINANCIALS%2F_portal%2FFinancials&amp;Page=Merge%20Down&amp;PageIdentifier=2kqavjq4k325i1km&amp;BookmarkState=3mbo5odbnnunipd9hejo8qb30i&amp;options=frd">Merge
                                                    Down dashboard</a>
                                                </li>
                                            </ul>
                                        </ul>
                                        <p><span style="color:rgb(255,0,0);">
                                        <strong>#DispositionsDUE Today: Please find the priorities below</strong></span></p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    </html>
    """
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')

    # Attach parts into message container.
    msg.attach(part1)
    # Attach based on the list length and return the HTML Message of UL List in each iteration
    chunks = []
    #for i, val in enumerate(finalList):
    if(len(finalList)>1):
        chunks.append(generate_html_for_preflight_list(finalList[1])) # Pass the preflight table details
        chunks.append(generate_html_for_dte_list(finalList[0]))  # Pass on the dte table details
        # As per doc https://docs.python.org/3/faq/programming.html#what-is-the-most-efficient-way-to-concatenate-many-strings-together
        # listHtml1 = html.join(chunks) # The original
        stringChunks = ""
        for i, x in enumerate(chunks):
            stringChunks = stringChunks + str(x)
        listHtml1 = html + stringChunks
        part3 = MIMEText(listHtml1, 'html')
        msg.attach(part3)  # ****** This is Working :)
    else:
        chunks.append(generate_html_for_dte_list(finalList[0]))  # Pass on the dte table details
        # As per doc https://docs.python.org/3/faq/programming.html#what-is-the-most-efficient-way-to-concatenate-many-strings-together
        # listHtml1 = html.join(chunks) # The original
        stringChunks = ""
        for i, x in enumerate(chunks):
            stringChunks = stringChunks + str(x)
        listHtml1 = html + stringChunks
        part3 = MIMEText(listHtml1, 'html')
        msg.attach(part3)  # ****** This is Working :)
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
    msg = """<ul><li class="MsoNormal" style="mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;mso-list:l2level1 lfo2">
    <font color="#ff0000">Analysis due date :{}</font></li></ul>
        <ul type="circle"><li>CDRM:</li><li>STARTER:{}</li></ul></body></html>
    """.format(str(finalList1[7].encode('utf-8')),finalList1[0])  # ****For testing purpose only #For dates use encode('utf-8')
    return msg

def generate_html_for_preflight_list(finalList2):
    #Encoding problem here
    msg="""<ul type="disc"><li>Preflight :{}</li>
    <ul><li>Purpose:{}</li></ul>
    """.format(finalList2[2],finalList2[3])
    return msg
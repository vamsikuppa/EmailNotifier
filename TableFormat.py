# -*- coding: utf-8 -*-
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime


def tableFormat(finalList):
    todaysDate = datetime.datetime.today().strftime('%d-%b')
    me = "vamsi.k.kuppa@oracle.com"
    you = "vamsi.k.kuppa@oracle.com"
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Automation Notifier - " + todaysDate
    msg['From'] = me
    msg['To'] = you
    chunks = []
    stringChunks = ""
    chunks.append(addTableHeaders())
    appendedStarter=False
    for i, el in reversed(list(enumerate(finalList))):
        if(appendedStarter==True):
            appendedStarter=False
            continue
        flag = False  # Counter to first break inner loop
        isInstanceFlag = False #Counter to break second inner loop
        for el1 in el:
            if (isinstance(el1, list)):
                chunks.append(generate_html_for_preflight_list(el))  # Pass the preflight table details
                #run_once = True
                break
            else:
                for nextEle in finalList[i-1]:
                    if (isinstance(nextEle, list)): #Only one row
                        #chunks.append(append_analysisdate_for_dte_list(el))
                        chunks.append(generate_html_for_dte_list(el))
                        isInstanceFlag =  True
                        #run_once = False
                        break
                    else: # Found the second Starter or CDRM row
                        # if (run_once == True):
                        #     chunks.append(append_analysisdate_for_dte_list(el))  # Append analysis date once
                        #     run_once = False
                        chunks.append(generate_html_for_dte_list(el,finalList[i-1]))  # Pass on the dte table details
                        appendedStarter=True
                        break
                if(isInstanceFlag==True or appendedStarter==True): #Condition to break second inner loop
                    break
            continue
    for i, x in enumerate(chunks):
        stringChunks = stringChunks + str(x)
    part3 = MIMEText(stringChunks, 'html')
    msg.attach(part3)  # ****** This is Working :)
    s = smtplib.SMTP_SSL('stbeehive.oracle.com')
    s.login(me, "Skyfall@1")
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    # s.sendmail(me, you, msg.as_string())
    s.sendmail(me, you, msg.as_string())
    s.quit()

def addTableHeaders():
    msg ="""
            <table height="59" border="1" cellpadding="2" cellspacing="2"
       width="1127">
    <tbody>
    <tr>
        <th bgcolor="#ff0000" valign="top"><span style="font-family:
                   sans-serif; color: #ffffff; font-size: smaller; ">Environment<br>
        </span></th>
        <td bgcolor="#ff0000" valign="top"><span style="font-family:
                   sans-serif; color: #ffffff; font-size: smaller; ">Purpose<br>
        </span></td>
        <td bgcolor="#ff0000" valign="top"><span style="font-family:
                   sans-serif; color: #ffffff; font-size: smaller; ">Due Today<br>
        </span></td>
        <td bgcolor="#ff0000" valign="top"><span style="font-family:
                   sans-serif; color: #ffffff; font-size: smaller; ">DTE ID<br>
        </span></td>
        <td bgcolor="#cccccc" valign="top"><span style="font-family:
                  sans-serif; font-size: smaller; "><b>POC/Final Report</b><br>
        </span></td>
    </tr>
    """
    return msg # Have to close tbody and table tags at end of mail
def generate_html_for_dte_list(finalList1,i=None):
    if i is None:
        try:
            envType = str(finalList1[3].encode('utf-8'))
        except IndexError:
            print "Env Type Index Error occurred"
        msg = """<td valign="top"><span style="font-family:  sans-serif; font-size: smaller; ">{}</span></td>
                            """.format(str(finalList1[7].encode('utf-8')).decode('utf-8').replace(u"\xa0", " ").encode(
            'utf-8')) # For appending analysis due date
        msg +="""<td valign="top">"""
        if (envType == "CDRM"):
            msg += """<span
                    style="font-family:  sans-serif; font-size: smaller; ">CDRM: <a href="http://preflightmanager.us.oracle.com/apex/f?p=121:14:7285005355584:5541213953682:NO::P14_DTE_ID,P14_RERUN_ID:{},1">{}</a>
                            </span>
                            """.format(finalList1[0].encode('utf-8'), finalList1[0].encode('utf-8'))
        else:
            msg += """<span style="font-family:  sans-serif; font-size: smaller; ">STARTER: <a href="http://preflightmanager.us.oracle.com/apex/f?p=121:14:7285005355584:5541213953682:NO::P14_DTE_ID,P14_RERUN_ID:{},1">{}</a>
                        </span>
                        """.format(finalList1[0].encode('utf-8'), finalList1[0].encode('utf-8'))

        msg +="""</td><td valign="top"><span
                style="font-family:  sans-serif; font-size: smaller; "><br></span></td>"""
        return msg
    else:
        try:
            dteID1 = str(finalList1[0].encode('utf-8'))
            envType1 = str(finalList1[3].encode('utf-8'))
            analysisDueDate1 = str(finalList1[7].encode('utf-8')).decode('utf-8').replace(u"\xa0", " ").encode('utf-8')
            dteID2 = str(i[0].encode('utf-8'))
            envType2 = str(i[3].encode('utf-8'))
            analysisDueDate2 = str(i[7].encode('utf-8')).decode('utf-8').replace(u"\xa0", " ").encode('utf-8')
        except IndexError:
            print "Env Type and DTE ID Index Error occurred"
        msg = """<td valign="top"><span style="font-family:  sans-serif; font-size: smaller; ">{}</span></td>
                            """.format(analysisDueDate1)
        msg += """<td valign="top">"""
        if (envType1 == "CDRM"):
            msg += """<span style="font-family:  sans-serif; font-size: smaller; ">CDRM: <a href="http://preflightmanager.us.oracle.com/apex/f?p=121:14:7285005355584:5541213953682:NO::P14_DTE_ID,P14_RERUN_ID:{},1">{}</a>
                                        </span>
                                        """.format(dteID1,dteID1)
        else:
            msg += """<span style="font-family:  sans-serif; font-size: smaller; ">STARTER: <a href="http://preflightmanager.us.oracle.com/apex/f?p=121:14:7285005355584:5541213953682:NO::P14_DTE_ID,P14_RERUN_ID:{},1">{}</a>
                                                    </span>
                                                    """.format(dteID1, dteID1)
        if(envType2 == "CDRM"):
            msg += """<span style="font-family:  sans-serif; font-size: smaller; ">CDRM: <a href="http://preflightmanager.us.oracle.com/apex/f?p=121:14:7285005355584:5541213953682:NO::P14_DTE_ID,P14_RERUN_ID:{},1">{}</a>
                                                    </span>
                                                    """.format(dteID2, dteID2)
        else:
            msg += """<span style="font-family:  sans-serif; font-size: smaller; ">STARTER: <a href="http://preflightmanager.us.oracle.com/apex/f?p=121:14:7285005355584:5541213953682:NO::P14_DTE_ID,P14_RERUN_ID:{},1">{}</a>
                                                                </span>
                                                                """.format(dteID2, dteID2)
        msg += """</td><td valign="top"><span
                        style="font-family:  sans-serif; font-size: smaller; "><br></span></td>"""
        return msg



def generate_html_for_preflight_list(finalList2):
    finalList3 = []
    for x in finalList2:
        flag = False
        for x1 in x:
            flag = True
            finalList3.append(x1.encode('utf-8'))
        if (flag == True):
            continue
    # finalList3 now contains data encoded in utf-8
    msg = """<tr>
            <th valign="top"><span
                    style="font-family:  sans-serif; font-size: smaller; ">{}<br>
            </span></th>
            <td valign="top"><span
                style="font-family:  sans-serif; font-size: smaller; ">{}<br>
            </span></td>
    """.format(finalList3[0],finalList3[3])
    return msg


def append_analysisdate_for_dte_list(finalList1):
    msg = """<td valign="top"><span style="font-family:  sans-serif; font-size: smaller; ">{}</span></td>
                    """.format(str(finalList1[7].encode('utf-8')).decode('utf-8').replace(u"\xa0", " ").encode(
        'utf-8'))  # To replace ascii character
    return msg

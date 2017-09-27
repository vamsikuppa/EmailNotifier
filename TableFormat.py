# -*- coding: utf-8 -*-
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime


def tableFormat(finalList, finalDailyRunsList):
    todaysDate = datetime.datetime.today().strftime('%d-%b')
    me = "vamsi.k.kuppa@oracle.com"
    #you = "vamsi.k.kuppa@oracle.com"
    you = "sasasriv_org_ww@oracle.com"
    recipients = ['vamsi.k.kuppa@oracle.com', 'shashank.sahay@oracle.com', 'ankita.yerawar@oracle.com',
                  'anudeep.tangudu@oracle.com', 'kalva.avinash@oracle.com']
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "FinTech Automation Notifier - " + todaysDate
    msg['From'] = me
    # msg['To'] = ", ".join(recipients)
    msg['To'] = you
    html = """<html>
            <head>
            
                <meta http-equiv="content-type" content="text/html; charset=windows-1252">
            </head>
            <body text="#000000" bgcolor="#FFFFFF">
            <br>
            #Critical items (immediate action): Highlighted in <span
                    style="color:#3333FF">blue</span>
            <div class="moz-forward-container">
                <div class="moz-forward-container">
                    <div class="moz-forward-container">
                        <div class="moz-forward-container">
                            <div class="moz-forward-container">
                                <div class="moz-forward-container">
                                    <div class="moz-forward-container">
                                        <div class="WordSection1">
                                            <div>
                                                <p><strong><span style="color:red">#Important/Please
                                        Note</span></strong><span style="color:red">:</span></p>
                                                <ul type="disc">
                                                    <ul type="circle">
                                                        <li>Teams please find the new update process
                                                            for Mergedown runs --&gt;&gt; <span
                                                                    style="color: #000000; "><a
                                                                    href="https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=81464107">ALM
                                                                Update process</a></span></li>
                                                        <li>Please note : this process is applicable
                                                            only for FINC mergedown runs.
                                                        </li>
                                                        <li><span style="color: #3366ff; ">Teams, please tag
                                                            all </span><span style="color: #3366ff; ">1802B
                                                            Merge Down bugs with below tags. <br>
                                                        </span></li>
                                                        <ul>
                                                            <span style="color: #3366ff; "> </span>
                                                            <li><span style="color: #3366ff; ">1802B_P4FA – FIN
                                                                bug having Techstack bug as Base bug</span></li>
                                                            <span style="color: #3366ff; "> </span>
                                                            <li><span style="color: #3366ff; ">1802B_INTERMITTENT
                                                                : For all product intermittent, setup
                                                                issues bugs</span></li>
                                                            <span style="color: #3366ff; "> </span>
                                                            <li><span style="color: #3366ff; ">1802B_FA: For code
                                                                fixes bugs</span></li>
                                                            <span style="color: #3366ff; "> </span>
                                                            <li><span style="color: #3366ff; ">1802B_FAAT : For
                                                                testware fixes bugs</span></li>
                                                        </ul>
                                                        <li><a
                                                                href="https://rms.us.oracle.com/analytics/saw.dll?Dashboard&amp;PortalPath=%2Fshared%2FFUSION%3AFINANCIALS%2F_portal%2FFinancials&amp;Page=Merge%20Down&amp;PageIdentifier=2kqavjq4k325i1km&amp;BookmarkState=3mbo5odbnnunipd9hejo8qb30i&amp;options=frd">Merge
                                                            Down dashboard</a></li>
                                                    </ul>
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="moz-forward-container">
                                    <div class="moz-forward-container">
                                        <div class="moz-forward-container">
                                            <div class="moz-forward-container">
                                                <div class="moz-forward-container">
                                                    <div class="moz-forward-container">
                                                        <div class="moz-forward-container">
                                                            <div class="moz-forward-container">
                                                                <div class="WordSection1">
                                                                    <div>
                                                                        <p><span style="color:rgb(255,0,0);">
                                                                              <strong>#Dispositions DUE Today:
                                                                                Please find the priorities below
                                                                                <br></strong></span></p>
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
                    </div>
                </div>
            </div>
            </body>
            </html>
        """
    chunks = []
    stringChunks = ""
    chunks.append(addTableHeaders())
    appendedStarter = False
    for i, el in reversed(list(enumerate(finalList))):
        if (appendedStarter == True):
            appendedStarter = False
            continue
        flag = False  # Counter to first break inner loop
        isInstanceFlag = False  # Counter to break second inner loop
        for el1 in el:
            if (isinstance(el1, list)):
                chunks.append(generate_html_for_preflight_list(el))  # Pass the preflight table details
                # run_once = True
                break
            else:
                for nextEle in finalList[i - 1]:
                    if (isinstance(nextEle, list)):  # Only one row
                        # chunks.append(append_analysisdate_for_dte_list(el))
                        chunks.append(generate_html_for_dte_list(el))
                        isInstanceFlag = True
                        # run_once = False
                        break
                    else:  # Found the second Starter or CDRM row
                        # if (run_once == True):
                        #     chunks.append(append_analysisdate_for_dte_list(el))  # Append analysis date once
                        #     run_once = False
                        # if (isinstance(finalList[i - 2]), list):
                        chunks.append(
                            generate_html_for_dte_list(el, finalList[i - 1]))  # Pass on the dte table details
                        appendedStarter = True
                        break
                        # else:
                        #     chunks.append(generate_html_for_dte_list(el, finalList[i - 1]))
                if (isInstanceFlag == True or appendedStarter == True):  # Condition to break second inner loop
                    break
            continue
    for i, x in enumerate(chunks):
        stringChunks = stringChunks + str(x)
    if finalDailyRunsList is None:
        listHtml1 = html + stringChunks
    else:
        listHtml1 = html + stringChunks + createTableForDailyRuns(finalDailyRunsList)
    part3 = MIMEText(listHtml1, 'html')
    msg.attach(part3)  # ****** This is Working :)
    s = smtplib.SMTP_SSL('stbeehive.oracle.com')
    s.login(me, "Skyfall@1")
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    # s.sendmail(me, recipients, msg.as_string())
    s.sendmail(me, you, msg.as_string())
    s.quit()


def addTableHeaders():
    msg = """<table height="59" border="1" cellpadding="2" cellspacing="2"
       width="100%">
    <tbody>
    <tr>
        <th bgcolor="#cccccc" valign="top"><span style="font-family:
                  sans-serif; font-size: medium;width:10% "><b>Priority/Comments</b><br>
        </span></th>
        <th bgcolor="#ff0000" valign="top"><span style="font-family:
                   sans-serif; color: #ffffff; font-size: medium;width:40% ">Environment<br>
        </span></th>
        <th bgcolor="#ff0000" valign="top"><span style="font-family:
                   sans-serif; color: #ffffff; font-size: medium;width:20% ">Purpose<br>
        </span></th>
        <th bgcolor="#ff0000" valign="top"><span style="font-family:
                   sans-serif; color: #ffffff; font-size: medium;width:15% ">Due date<br>
        </span></th>
        <th bgcolor="#ff0000" valign="top"><span style="font-family:
                   sans-serif; color: #ffffff; font-size: medium; width:15%">DTE ID<br>
        </span></th>
    </tr>
    """
    return msg  # Have to close tbody and table tags at end of mail


def generate_html_for_dte_list(finalList1, i=None):
    if i is None:
        try:
            envType = str(finalList1[3].encode('utf-8'))
        except IndexError:
            print "Env Type Index Error occurred"
        msg = """<td valign="top"><span style="font-family:  sans-serif; font-size: medium; ">{}</span></td>
                            """.format(str(finalList1[7].encode('utf-8')).decode('utf-8').replace(u"\xa0", " ").encode(
            'utf-8'))  # For appending analysis due date
        msg += """<td valign="top">"""
        if (envType == "CDRM"):
            msg += """<span
                    style="font-family:  sans-serif; font-size: medium;white-space:nowrap;width:15% ">CDRM: <a href="http://preflightmanager.us.oracle.com/apex/f?p=121:14:7285005355584:5541213953682:NO::P14_DTE_ID,P14_RERUN_ID:{},1">{}</a>
                            </span>
                            """.format(finalList1[0].encode('utf-8'), finalList1[0].encode('utf-8'))
        else:
            msg += """<span style="font-family:  sans-serif; font-size: medium;white-space:nowrap;width:15% ">STARTER: <a href="http://preflightmanager.us.oracle.com/apex/f?p=121:14:7285005355584:5541213953682:NO::P14_DTE_ID,P14_RERUN_ID:{},1">{}</a>
                        </span>
                        """.format(finalList1[0].encode('utf-8'), finalList1[0].encode('utf-8'))

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
        msg = """<td valign="top"><span style="font-family:  sans-serif; font-size: medium;white-space:nowrap;width:15% ">{}</span></td>
                            """.format(analysisDueDate1)
        msg += """<td valign="top">"""
        if (envType1 == "CDRM"):
            msg += """<span style="font-family:  sans-serif; font-size: medium;white-space:nowrap;width:15% ">CDRM: <a href="http://preflightmanager.us.oracle.com/apex/f?p=121:14:7285005355584:5541213953682:NO::P14_DTE_ID,P14_RERUN_ID:{},1">{}</a>
                                        </span>
                                        """.format(dteID1, dteID1)
        else:
            msg += """<span style="font-family:  sans-serif; font-size: medium;white-space:nowrap;;width:15% ">STARTER: <a href="http://preflightmanager.us.oracle.com/apex/f?p=121:14:7285005355584:5541213953682:NO::P14_DTE_ID,P14_RERUN_ID:{},1">{}</a>
                                                    </span>
                                                    """.format(dteID1, dteID1)
        if (envType2 == "CDRM"):
            msg += """<span style="font-family:  sans-serif; font-size: medium;white-space:nowrap;width:15% ">CDRM: <a href="http://preflightmanager.us.oracle.com/apex/f?p=121:14:7285005355584:5541213953682:NO::P14_DTE_ID,P14_RERUN_ID:{},1">{}</a>
                                                    </span>
                                                    """.format(dteID2, dteID2)
        else:
            msg += """<span style="font-family:  sans-serif; font-size: medium;white-space:nowrap;width:15% ">STARTER: <a href="http://preflightmanager.us.oracle.com/apex/f?p=121:14:7285005355584:5541213953682:NO::P14_DTE_ID,P14_RERUN_ID:{},1">{}</a>
                                                                </span>
                                                                """.format(dteID2, dteID2)
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
            <td valign="left"><span
                    style="font-family:  sans-serif; font-size: medium;white-space:nowrap; wrap="hard";width:10%"><br>
            </span></td>
            <td valign="top"><span
                    style="font-family: sans-serif; font-size: medium;white-space:pre-wrap; word-wrap: break-word;width:40%">{}<br>
            </span></td>
            <td valign="top"><span
                style="font-family:  sans-serif; font-size: medium;white-space:pre-wrap; word-wrap: break-word;width:40%">{}<br>
            </span></td>
    """.format(finalList3[0], finalList3[3]) #To print env name and purpose
    return msg


def append_analysisdate_for_dte_list(finalList1):
    msg = """<td valign="top"><span style="font-family:  sans-serif; font-size: medium;word-wrap: break-word;width:15% ">{}</span></td>
                    """.format(str(finalList1[7].encode('utf-8')).decode('utf-8').replace(u"\xa0", " ").encode(
        'utf-8'))  # To replace ascii character
    return msg

def createTableForDailyRuns(finalDailyRunsList):
    print finalDailyRunsList
    finalMsg = ""
    for DailyRunList in finalDailyRunsList:
        if len(DailyRunList)==3:
            msg = """<tr>
                <td valign="left"><span
                        style="font-family:  sans-serif; font-size: medium;white-space:nowrap; wrap="hard"><br>
                </span></td>
            <td valign="top"><span style="font-family:  sans-serif; font-size: medium;word-wrap: break-word;width:40% ">{}</span></td>
            <td valign="top"><span style="font-family:  sans-serif; font-size: medium;word-wrap: break-word;width:40% ">{}</span></td>
            <td valign="top"><span style="font-family:  sans-serif; font-size: medium;word-wrap: break-word;width:40% "></span></td>
            <td valign="top"><span style="font-family:  sans-serif; font-size: medium; "><a href="http://preflightmanager.us.oracle.com/apex/f?p=121:14:7285005355584:5541213953682:NO::P14_DTE_ID,P14_RERUN_ID:{},1">{}</a></span></td>
                            """.format(str(DailyRunList[1].encode('utf-8')),
                                       str(DailyRunList[2]).encode('utf-8'),
                                       str(DailyRunList[0]).encode('utf-8'),
                                       str(DailyRunList[0]).encode('utf-8'))
        else:
            msg ="""<tr>
                <td valign="left"><span
                        style="font-family:  sans-serif; font-size: medium;white-space:nowrap; wrap="hard"><br>
                </span></td>
            <td valign="top"><span style="font-family:  sans-serif; font-size: medium;word-wrap: break-word ">{}</span></td>
            <td valign="top"><span style="font-family:  sans-serif; font-size: medium;word-wrap: break-word;width:40% "></span></td>
            <td valign="top"><span style="font-family:  sans-serif; font-size: medium;word-wrap: break-word;width:40% "></span></td>
            <td valign="top"><span style="font-family:  sans-serif; font-size: medium;word-wrap: break-word;width:15% "><a href="http://preflightmanager.us.oracle.com/apex/f?p=121:14:7285005355584:5541213953682:NO::P14_DTE_ID,P14_RERUN_ID:{},1">{}</a></span></td>
                            """.format(str(DailyRunList[1].encode('utf-8')),
                                       str(DailyRunList[0]).encode('utf-8'),
                                       str(DailyRunList[0]).encode('utf-8'))

        finalMsg +=msg
    return finalMsg
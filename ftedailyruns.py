# -*- coding: utf-8 -*-
import imaplib
import email
from bs4 import BeautifulSoup

def dailyRunsMailsInit(host, username, password):
    mail = imaplib.IMAP4_SSL(host)
    mail.login(username, password)
    mail.select("FTEDailyRuns", readonly=1)
    return mail


def get_text_block(email_message_instance):
    if email_message_instance.is_multipart():
        for payload in email_message_instance.get_payload():
            # if payload.is_multipart(): ...
            print payload.get_payload()
    else:
        return email_message_instance.get_payload()


def fetchDailyRunsBody(mail, uidsList):
    finalFTEDailyRunMailList = []
    dailyRunMailList = []
    print "There are {} FTE Daily runs mails found".format(len(uidsList))
    for uid in uidsList:
        flag = False
        result, data = mail.fetch(uid,
                                  "(UID BODY[])")  # Alternative way of fetching message body , ref; https://stackoverflow.com/questions/19540192/imap-get-sender-name-and-body-text
        msg = email.message_from_string(data[0][1])
        htmlbody = get_text_block(msg)
        if (htmlbody != ''):
            tree = BeautifulSoup(htmlbody, "lxml")  # Never return the tree here as it will take only the last return
            dailyRunsList = []
            dailyRunsTable = tree.find("table")
            dailyRunsTableRows = []
            dailyRunsTableRows = dailyRunsTable.find_all('tr')
            if dailyRunsTableRows:
                try:
                    dteIdRow = dailyRunsTableRows[0]  # To get the DTE ID
                    envNameRow = dailyRunsTableRows[1]  # To get the Env Name
                    # purposeRow = dailyRunsTableRows[7]  # To get the purpose row
                except IndexError:
                    "Occurred Index Error for fetching dte id or Env row"
                #DTE ID Row
                dailyRunsTableCols = dteIdRow.find_all('td')
                for i, dailyRunsTableColEle in enumerate(dailyRunsTableCols):
                    if (i == 1):
                        dteId = dailyRunsTableColEle.text.strip().encode('utf-8')
                        dailyRunMailList.append(dteId)
                    else:
                        continue
                # Env Name Row
                dailyRunsTableCols = envNameRow.find_all('td')
                for i, dailyRunsTableColEle in enumerate(dailyRunsTableCols):
                    if (i == 1):
                        envName = dailyRunsTableColEle.text.strip().encode('utf-8')
                        dailyRunMailList.append(envName)
                    else:
                        continue
                #Purpose row
                # dailyRunsTableCols = purposeRow.find_all('td')
                # for i, dailyRunsTableColEle in enumerate(dailyRunsTableCols):
                #     if (i == 1):
                #         purposeName = dailyRunsTableColEle.text.strip().encode('utf-8')
                #         dailyRunMailList.append(purposeName)
                #     else:
                #         continue
            else:
                continue
        if not dailyRunMailList:
            continue
        finalFTEDailyRunMailList.append(dailyRunMailList)
        dailyRunMailList=[]
    return finalFTEDailyRunMailList

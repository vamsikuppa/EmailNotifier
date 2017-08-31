# -*- coding: utf-8 -*-
import imaplib
import datetime
import email
import lxml
from bs4 import BeautifulSoup
import EmailSend
import test_list

def init(host, username, password):
    mail = imaplib.IMAP4_SSL(host)
    mail.login(username, password)
    mail.select("PreflightMails", readonly=1)
    return mail


def get_uids(mail):
    date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")  # Change logic here for daterange
    #date = (datetime.datetime.today() - datetime.timedelta(2)).strftime("%d-%b-%Y:%H-%M-%S")
    result, data = mail.search(None, '(SENTSINCE {date})'.format(date=date))
    # print result ===>> OK #Can have a check to see result is OK
    # result, data = mail.search(None, '(UNSEEN)')  # to get the unread emails #Always use mail.search() here
    ids = data[0]  # Returns uids of mails
    ids_list = ids.split()
    return ids_list


def fetch_header(mail, uidsList):  # Write code here to hetch headers Ref : http://www.rfc-base.org/txt/rfc-2060.txt
    # ref; https://stackoverflow.com/questions/19540192/imap-get-sender-name-and-body-text
    for uid in uidsList:
        result, data = mail.fetch(uid,
                                  "(BODY[HEADER.FIELDS (FROM)])")  # fetch the From address of the mail from headers
        print data[0][1]


def fetch_body(mail, uidsList):
    finalMailingList = []
    print "There are {} mails found".format(len(uidsList))
    for uid in uidsList:
        flag = False
        # result, data = mail.fetch(uid, "(RFC822)")  # fetch the email body (RFC822) for the given ID
        # raw_email = data[0][1]  # here's the body, which is raw text of the whole email # including headers and alternate payloads
        # msg = email.message_from_string(raw_email)
        result, data = mail.fetch(uid,
                                  "(UID BODY[TEXT])")  # Alternative way of fetching message body , ref; https://stackoverflow.com/questions/19540192/imap-get-sender-name-and-body-text
        msg = email.message_from_string(data[0][1])
        htmlbody = get_text_block(msg)
        tree = BeautifulSoup(htmlbody, "lxml")  # Never return the tree here as it will take only the last return
        dtetablesList = get_table(tree)
        #Logic if the dtetablesList contains 2 rows i.e CDRM and starter
        if(len(dtetablesList)==3):
            for i,val in enumerate(dtetablesList[0:2]):  #Access the first two rows to get dte table list
                #i=0
                analysisDueDate=str(val[7].encode('utf-8')).strip().decode('utf-8')  # This returns you the Analysis date of CDRM and Starter
                analysisDueDate = analysisDueDate.replace("Sept","Sep")
                if (len(analysisDueDate.encode('utf-8')) == 25): #date-format: Aug. 29, 2017, 4 p.m. PT
                    reqDate = validate_date(analysisDueDate[:-11])  # Date format = Aug. 24, 2017
                elif(len(analysisDueDate.encode('utf-8')) == 24): #date-format: Aug. 1, 2017, 4 p.m. PT
                    reqDate = validate_date(analysisDueDate[:-11])
                else: #Date- format:Aug. 30, 2017, noon PT
                    reqDate = validate_date(analysisDueDate[:-9])
                currentDate = datetime.datetime.now().strftime("%Y-%m-%d")
                topology = str(val[4].encode('utf-8')) # This returns the topology
                envType = str(dtetablesList[i][3].encode('utf-8'))  #Checking for CDRM or STARTER
                if ((reqDate >= currentDate) and ((topology=="GSI") or (topology=="FSCM")) and (envType == "CDRM")):  # For testing purpose only, have to change the logic to equals.
                    print "{} is true".format(analysisDueDate.encode('utf-8'))
                    print "appending list before sending it to mail"
                    #for i,val in enumerate(dtetablesList[i]):
                    finalMailingList.append(dtetablesList[i])
                    print "appending complete"
                    flag = True
                else:
                    print "Analysis date didnot pass the validation continuing with the next mail for {}".format(dtetablesList[0])
                    flag = False
            if(flag == True):
                finalMailingList.append(dtetablesList[2]) #Append only when the condition is satisfied
        #Logic if the dtetablesList contains one row i.e CDRM or starter then comparing for its due date with today
        elif(len(dtetablesList)==2):
            analysisDueDate = str(dtetablesList[0][7].encode('utf-8')).strip().decode('utf-8')
            analysisDueDate = analysisDueDate.replace("Sept", "Sep")
            if (len(analysisDueDate.encode('utf-8')) == 25):
                reqDate=validate_date(analysisDueDate[:-11])  # Date format = Aug. 24, 2017
            elif (len(analysisDueDate.encode('utf-8')) == 24):
                reqDate = validate_date(analysisDueDate[:-11])
            else:
                reqDate = validate_date(analysisDueDate[:-9])
            currentDate = datetime.datetime.now().strftime("%Y-%m-%d")
            #Checking for CDRM or STARTER
            envType = str(dtetablesList[0][3].encode('utf-8'))
            #Checking GSI or FSCM topology
            topology = str(dtetablesList[0][4].encode('utf-8'))
            if ((reqDate >= currentDate)and((topology=="GSI") or (topology=="FSCM")) and (envType == "CDRM")):  # For testing purpose only, have to change the logic to equals.
                print "{} is true".format(analysisDueDate.encode('utf-8'))
                print "appending list before sending it to mail"
                #for i,val in enumerate(dtetablesList):
                finalMailingList.append(dtetablesList[0])
                print "appending complete"
                flag = True
            else:
                print "Analysis date or Topology validation or Env Type didnot pass the validation continuing with the next mail for {}".format(dtetablesList[0])
                flag = False
            if(flag == True):
                finalMailingList.append(dtetablesList[1]) #Append only when the condition is satisfied
        else:
            continue
    return finalMailingList


def get_text_block(email_message_instance):
    if email_message_instance.is_multipart():
        for payload in email_message_instance.get_payload():
            # if payload.is_multipart(): ...
            print payload.get_payload()
    else:
        return email_message_instance.get_payload()


def get_table(tree):
    # Getting the Pre flights table
    allTablesList = []
    preflightsList = []
    preflightsListStr = ""
    preflightTable = tree.find("table", {"id": "preflight_details_table"})
    preflightTableBody = preflightTable.find('tbody')
    preflightTableRows = preflightTableBody.find_all('tr')
    for preflightTableRow in preflightTableRows:
        preflightTableCols = preflightTableRow.find_all('td')
        preflightTableColEles = [preflightTableColEle.text.strip() for preflightTableColEle in preflightTableCols]
        preflightsList.append([colEle for colEle in preflightTableColEles if colEle]) # Get rid of empty values
        #preflightsListStr = preflightsListStr.join(colEle.encode('utf-8') for colEle in preflightTableColEles if colEle)
    # Now preflightList contains the Preflight Table Second column values
    # Getting the Dte details table
    dtedetailsList = []
    dtetable = tree.find("table", {"id": "dte_details_table"})  # To get the dte table
    table_body = dtetable.find('tbody')
    rows = table_body.find_all('tr')
    # Logic for dte table contains multiple rows (CDRM and DTE)
    if(len(rows)>1):
        dteTableRowsData=[[td.text.strip() for td in rows[i].find_all('td')] for i in range(len(rows))]
        # for i,val in enumerate(preflightsList):
        #     dteTableRowsData.append(val)
        dteTableRowsData.append(preflightsList)
        return dteTableRowsData # This will return both DTE and the preflight details
    #Logic for single row in dte table
    else:
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            dtedetailsList.append([ele for ele in cols if ele])  # Get rid of empty values
        dtedetailsList.append(preflightsList) # here append both dte details table and pre flight tables
    return dtedetailsList


def validate_date(date_text):
    #try:
        #datetime.datetime.strptime(date_text, '%b. %d, %Y')
        reqDate = datetime.datetime.strptime(date_text, "%b. %d, %Y").strftime("%Y-%m-%d")
        return reqDate
    #except ValueError:
        #raise ValueError("Incorrect date format should be MMM. DD, YYYY. Or Analysis due date doesnt have proper date")


def check_if_today(reqDate, currentDate):
    if (reqDate == currentDate):
        return True
    else:
        return False


def exit(mail):
    mail.close()
    mail.logout()


def main():
    finalMailingList = []
    host = "stbeehive.oracle.com"
    username = "vamsi.k.kuppa@oracle.com"
    password = "Skyfall@1"
    mail = init(host, username, password)
    uidsList = get_uids(mail)
    # fetch_header(mail, uidsList) #Write code here to fetch headers
    if(len(uidsList)>0): #Check for mAails count
        finalMailingList = fetch_body(mail, uidsList)  # The Final Maliling List that need to be sent
        if(len(finalMailingList)==0):
            print "Analysis date validation did not pass"
            exit(mail)
            return
        print "This is the final list that will be printed in mail"
        print finalMailingList
        #test_list.list_iterate(finalMailingList)
        EmailSend.send_mail(finalMailingList)
        exit(mail)
    else:
        print "No mails found. Exiting the mailbox notifier"
        exit(mail)


if __name__ == '__main__':
    main()

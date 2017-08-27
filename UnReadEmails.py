import imaplib
import lxml
import datetime
from lxml import html
import email


def main():
    h_o_s_t = 'stbeehive.oracle.com'
    u_s_e_r_n_a_m_e = 'vamsi.k.kuppa@oracle.com'
    p_a_s_s_w_o_r_d = 'Skyfall@1'
    folder = 'PreflightMails'
    mail = imaplib.IMAP4_SSL(h_o_s_t)
    mail.login(u_s_e_r_n_a_m_e, p_a_s_s_w_o_r_d)
    mail.select(folder,readonly=1)
    resp, items = mail.search(None, '(UNSEEN)')
    # date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")  # Search for emails since in the past day
    # result, items = mail.uid('search', None, '(SENTSINCE {date})'.format(date=date))
    items = items[0].split(' ')

    for emailid in items:
        # getting the mail content
        #resp, data = mail.fetch(emailid, '(UID BODY[TEXT])')
        typ, data = mail.fetch(emailid, '(RFC822)')
        msg = email.message_from_string(data[0][1])
        print msg
        #tree = html.fromstring(text)
        #print tree
        # dte_bugs_table = tree.xpath("//table[@id='dte_details_table']")
        # print dte_bugs_table

if __name__ == '__main__':
    main()

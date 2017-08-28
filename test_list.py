

def list_iterate(finalList):
    process_list(finalList[0])




def process_list(sub_list):
    chunks = []
    for i, val in enumerate(sub_list):
        chunks.append(generate_html_for_list(val))  # Pass on the each index of list to generate html
        # As per doc https://docs.python.org/3/faq/programming.html#what-is-the-most-efficient-way-to-concatenate-many-strings-together
    # listHtml1 = html.join(chunks) # The original
    stringChunks = ""
    # for i, x in enumerate(chunks):
    #     stringChunks = stringChunks + str(x)
    # listHtml1 = html + stringChunks
    # print listHtml1
    #print stringChunks


def generate_html_for_list(firstList1):
    # [x.encode('utf-8') for x in finalList1]
    # msg = """<html><body>
    # <ul type="disc">
    #     <li>Preflight :</li>
    #     <ul><li>Analysis due date :{}</li>
    #     <li>Purpose:</li></ul>
    #     <ul type="circle"><li>CDRM:</li><li>STARTER:{}</li></ul></ul></body></html>
    # """.format(finalList1[7].encode('utf-8'),
    #            finalList1[1])  # ****For testing purpose only #For dates use encode('utf-8')
    # return msg
    print "First list values are"
    print firstList1[0]
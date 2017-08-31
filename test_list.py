

def list_iterate(finalList):
    for el in finalList:
        for el1 in el:
            if(isinstance(el1,list)):
                print el # At this step send it to the generate_html_for_preflight_list
                break
            else:
                print el #At this step send it to the generate_html_for_dte_list
                break





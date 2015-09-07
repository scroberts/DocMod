#!/usr/bin/env python3

# external modules
import DocMod
import os
import json

# my modules
import DCC
import Config as CF

# This code takes a search criteria, defined in "docinfo", and searches
# the DOORS document module (as stored in TraceTree) to find matches. 
# It prints a report on all files found based on the list of attributes
# in "docmodreport".
# In setting search criteria it is possible to look for undefined
# attributes by using '_UNASSIGNED' as the matching criteria.

            
if os.path.isfile(CF.tracetreefilepath + CF.docmod_dict_file):
    print('Found existing DocMod file: ', CF.docmod_dict_file)
else:
    print('Creating DocMod file: ', CF.docmod_dict_file)
    docmod.create_docmod_file(CF.docmod_dict_file)
    
# Open the document module
fh = open(CF.tracetreefilepath + CF.docmod_dict_file,'r')
dm = json.load(fh)
fh.close()

# construct reflist to determine the search criteria
reflist = {}

docinfo = {}
# docinfo['dccDocNo'] = 'TMT.CTR.ICD.13.003'
# docinfo['dccDocStatus'] = 'LATEST'
# docinfo['CRNumbers'] = '_UNASSIGNED'
docinfo['TMTPublished'] = 'True'
reflist['ICD'] = docinfo

# print(reflist)

## Here are other example reflists commented out
# docinfo['dccDocStatus'] = 'LATEST'
# docinfo['dccDocTitle'] = 'Observatory Architecture Document (OAD)'
# docinfo['dccDocNo'] = 'TMT.SEN.DRD.05.002'
# docinfo['WIP-ParentDocumentNo'] = ''
# 
# reflist['AD1'] = docinfo
# 
# docinfo = {}
# docinfo['dccDocStatus'] = 'LATEST'
# docinfo['dccDocHandleNo'] =	'7842'
# 
# reflist['AD2'] = docinfo
# 
# docinfo = {}
# docinfo['dccDocStatus'] = 'LATEST'
# docinfo['dccDocVersionHyperlink'] =	'https://docushare.tmt.org/docushare/dsweb/Get/Version-49415'
# 
# reflist['AD3'] = docinfo


# construct document module report list
docmodreport = []
docmodreport.append('dccDocTitle')
docmodreport.append('dccDocNo')
docmodreport.append('dccDocRev')
docmodreport.append('DocType')
docmodreport.append('dccDocHandleHyperlink')
docmodreport.append('dccDocVersionHyperlink')
docmodreport.append('dccDocSignedApproved')
docmodreport.append('TMTPublished')
docmodreport.append('dccStatusCheckDate')
docmodreport.append('WIP-ParentDocumentNo')
docmodreport.append('CRNumbers')

s = DCC.login(CF.dcc_url + CF.dcc_login)

for ref in reflist.items():
    print('looking for ', ref[0], ref[1])
    for doc in dm.items():
        if DocMod.is_in_dict(ref[1],doc[1]):
            print('Found Document Module Object #:', doc[0])
            DocMod.print_report(docmodreport, doc[1])
         
#          The following code prints all DCC information on the found files 
   
            fd = DCC.prop_get(s, DCC.get_handle(doc[1]['dccDocHandleHyperlink']), InfoSet = 'DocAll')
            DCC.print_doc_all(fd)
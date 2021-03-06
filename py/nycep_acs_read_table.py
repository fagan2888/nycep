import os
from nycep_acs_tract_logrecno import *

# -------- 
#  Read the data from an ACS table
#
#  Example:
#    data = nycep_acs_read_table('B01001',dpath='../../data/acs',summary=5)
#
#  2014/06/06 - Written by Greg Dobler (CUSP/NYU)
# -------- 

def nycep_acs_read_table(tlabel, year=2012, summary=5, dpath=None, 
                         margins=False):

    # -- check path
    if dpath==None:
        print("Must set data path to ACS data!")
        return


    # -- utilities
    eom   = 'm' if margins else 'e'
    sfile = os.path.join(dpath,str(year),str(summary),
                         'Sequence_Number_and_Table_Number_Lookup.txt')


    # -- read in the sequence number file
    fopen  = open(sfile,'r')
    slines = [line for line in fopen if 'CELL' in line]
    fopen.close()


    # -- get the sequence number, start, and # of cells for the requested table
    recs   = slines[[line.split(',')[1] for line in slines].index(tlabel)
                    ].split(',')
    seqnum = recs[2]
    cstart = int(recs[4])-1
    ncell  = int(''.join([i for i in recs[5] if i.isdigit()]))


    # -- read the estimates (or margins) file
    dfile  = os.path.join(dpath,str(year),str(summary),
                          eom+str(year)+str(summary)+'ny'+seqnum+'000.txt')
    fopen  = open(dfile,'r')

    data = {'fileid'   : '',
            'filetype' : '',
            'stusab'   : '',
            'chariter' : '',
            'sequence' : '',
            'logrecno' : [],
            'vals'     : []}

    if summary==5:
        logrecno = nycep_acs_tract_logrecno(dpath=dpath)
        dlines   = []
        for line in fopen:
            recs = line.split(',')
            if recs[5] in logrecno:
                data['fileid']   = recs[0]
                data['filetype'] = recs[1]
                data['stusab']   = recs[2]
                data['chariter'] = recs[3]
                data['sequence'] = recs[4]
                data['logrecno'].append(recs[5])
                data['vals'].append(recs[cstart:cstart+ncell])
    elif summary==1:
        data = [line.split(',')[cstart:cstart+ncell] for line in fopen]
    else:
        print("Only 1 and 5 year summaries supported!!!")
        return

    fopen.close()


    # -- return data
    return data

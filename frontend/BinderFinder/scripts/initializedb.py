import os
import sys
import transaction
import re

from Bio import SeqIO

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from ..models import (
    User, 
    Search,
    Domain, 
    Sequence,
    )
from ..models.records import SearchRecord

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def pop_domain_table(dbsession, pfam_handle, counter):

    with open(pfam_handle) as p_handle:
        domains = [] # list for objects to be added
        for line in p_handle.readlines():
            if (counter % 5000) == 0: # commit every 5000 objects to avoid memory overload
                dbsession.add_all(domains)
                transaction.commit() # commit adds
                dbsession.expunge_all() # clear memory
                domains = []
            emblid, pfamid = line.strip().split('\t') # parse tab delimited values
            pfamid = pfamid.split('.')[0][2:] # remove pfam subclassification and the superfluous "PF"
            domains.append(Domain(domainID=counter, pfamID=pfamid, emblID=emblid))
            counter += 1

    dbsession.add_all(domains) # add the final batch
    transaction.commit() # commit...
    dbsession.expunge_all() # clear memory

    print ('Added {} entries to the domain table'.format(counter))


def pop_seq_table(dbsession, fasta_file, seqid):
    """
    Populates the sql database seq table with embl ids and sequences.
    """

    records = []
    for rec in SeqIO.parse(fasta_file, "fasta"): 
        m = re.search("PN:US(\d+)", rec.description) # match patent regex in the sequence header
        if m: # if there is a US based patent id...
            patid = m.group(1) # ...extract the embl id
            emblid = rec.id.split(":")[1].split("|")[0] # extract the emblid
            seq = str(rec.seq)
            try:
                sequence = Sequence(seqID=seqid, emblID=emblid, 
                                    patID=patid, seq=seq)
                records.append(sequence)
                seqid += 1
            except:
                print(sys.exc_info()[0])
        else: 
            pass # skip if there isn't a US based patent number
        
        if (seqid % 5000) == 0: # commit every 5000 sequences
            dbsession.add_all(records)
            transaction.commit()
            dbsession.expunge_all()
            records = []

        dbsession.add_all(records)
        transaction.commit()
        dbsession.expunge_all()
        records = []


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.create_all(engine)


    session_factory = get_session_factory(engine)

    update_domain_table = False # change to True in order to add more domain-pfam entries
    update_sequence_table = False # change to True in order to add more sequence-emblid entries

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        
        ## todo ## 
        # use config file to put all hard-coded files in one place
        if update_domain_table:
            d_handle = '' # put in filename to update
            counter = 0 # set to largest existing id to avoid unique clash, 0 for building new
            pop_domain_table(dbsession, d_handle, counter)


        if update_sequence_table:
            d_handle = '' # put in filename to update
            counter = 0 # set to largest existing id to avoid unique clash, 0 for building new
            pop_seq_table(dbsession, file, counter)


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

def domain_pop(dbsession, pfam_handle):
    for i, line in enumerate(open(pfam_handle).readlines()):
        emblid, pfamid = line.strip().split(',')
        domain = Domain(domainID=i, pfamID=pfamid, emblID=emblid)
        dbsession.add(domain)

def pop_seq_table(dbsession, fasta_file):
    """
    Populates the sql database seq table with embl ids and sequences.
    """
    seqid = 0
    for rec in SeqIO.parse(fasta_file, "fasta"): 
        m = re.search("PN:US(\d+)", rec.description)

        if m:
            patid = m.group(1)
            # ...extract the embl id
            emblid = rec.id.split(":")[1].split("|")[0] 
            seq = str(rec.seq)

            try:
                sequence = Sequence(seqID=seqid, emblID=emblid, 
                                    patID=patid, seq=seq)
                dbsession.add(sequence)
                seqid += 1
            except:
                print(sys.exc_info()[0])
        else:   
            pass
    return seqid

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

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        
        domain_pop(dbsession, "../test/pfam_ids.csv")
        pop_seq_table(dbsession, "../test/nrp_patent_003.fasta")


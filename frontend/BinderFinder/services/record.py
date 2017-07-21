import sqlalchemy as sa
from ..models.records import SearchRecord

class SearchRecordService(object):
    
    @classmethod
    def by_id(cls, _id, request):
        query = request.dbsession.query(SearchRecord)
        return query.get(_id)


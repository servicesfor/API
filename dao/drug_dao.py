import random

from dao import BaseDao
from logger import api_logger

class Drugs(BaseDao):
    def find(self,**values):
        api_logger.info('db query drugs <%s>' % values['drug_id'])
        #科室名称

        return super(Drugs, self).save('yl_user', **values)



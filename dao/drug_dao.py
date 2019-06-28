import random

from dao import BaseDao
from logger import api_logger

class DrugsDao(BaseDao):
    def find(self,**values):

        api_logger.info('db query drugs <%s>' % values['drug_id'])
        #疾病


        return super(DrugsDao, self).save('yl_user', **values)

    def find_illness(self):

        sql = 'select id as ill_id ,ill_name  from liftyl_diseases'
        data = self.query(sql)


        return data





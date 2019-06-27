from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from libs import rd

import random

def new_code(phone):
    """
    获取验证码
    :param phone:
    :return:
    """
    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    rd.set(phone,code)          #将生成的验证码保存在redis中

    rd.expire(phone, 120)  # 有效时间： 12小时
    # 发送验证给用户
    send_sms_code(phone, code)


def confirm(phone, input_code):
    # 从缓存cache中读取phone对应的验证码
    # 和input_code进行比较，如果通过则返回True

    return input_code == rd.get(phone).decode()



def send_sms_code(phone, code):

    client = AcsClient('LTAIRiQGIywYBeYN', 'ZOHiNBYPr72dCFog2fLU5Pu9RvVAIf', 'cn-hangzhou')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', phone)
    request.add_query_param('SignName', "Disen工作室")
    request.add_query_param('TemplateCode', "SMS_128646125")
    request.add_query_param('TemplateParam', '{"code":"%s"}' % code)

    response = client. do_action_with_exception(request)
    print(str(response, encoding='utf-8'))



#_*_coding:utf-8_*_

import urllib2,urllib,json,re
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

class SaltAPI(object):
    def __init__(self,url,username,password):
        self.__url = url.rstrip("/")
        self.__user = username
        self.__password = password
        self.__token_id = self.saltLogin()

    def saltLogin(self):
        params = {'eauth':'pam','username':self.__user,'password':self.__password}
        encode = urllib.urlencode(params)
        obj = urllib.unquote(encode)
        headers = {'X-Auth-Token':''}
        url = self.__url + '/login'
        req = urllib2.Request(url,obj,headers)
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        try:
            token = content['return'][0]['token']
            return token
        except KeyError:
            raise KeyError

    def postRequest(self,obj,prefix='/'):
        url = self.__url + prefix
        headers = {'X-Auth-Token': self.__token_id}
        req = urllib2.Request(url,obj,headers)
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        return content

    def PostRequest(self, obj, prefix='/'):
        url = self.__url + prefix
        headers = {'X-Auth-Token': self.__token_id}
        if obj:
            data, number = re.subn("arg\d*", 'arg', obj) #将arg1 arg2这些关键字都替换成arg，number为替换次数
        else:
            data=None
        print "data",data
        req = urllib2.Request(url, data, headers)  # obj为传入data参数字典，data为None 则方法为get，有date为post方法
        opener = urllib2.urlopen(req)
        middle_str = unicode(opener.read(), errors='ignore')
        content = json.loads(middle_str)
        return content

    def asyncMasterToMinion(self, tgt, fun, arg):
        '''
        异步执行，当target为部分minion时，Master操作Minion；
        :param target: 目标服务器ID组成的字符串；
        :param fun: 使用的salt模块，如state.sls, cmd.run
        :param arg: 传入的命令或sls文件
        :return: jid字符串
        '''
        if tgt == '*':
            params = {'client': 'local_async', 'tgt': tgt, 'fun': fun, 'arg': arg}
        else:
            params = {'client': 'local_async', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': 'list'}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid

    def masterToMinionContent(self, tgt, fun, arg):
        '''
            Master控制Minion，返回的结果是内容，不是jid；
            目标参数tgt是一个如下格式的字符串：'*' 或 'zhaogb-201, zhaogb-202, zhaogb-203, ...'
        '''
        if tgt == '*':
            params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg}
        else:
            params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': 'list'}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        result = content['return'][0]
        return result

    def saltRun(self,tgt,func,client='local',expr_form='glob',arg=None,**kwargs):
        params = {'client': client, 'fun': func, 'tgt': tgt, 'expr_form': expr_form}
        if arg:
            a = arg.split(',')  # 参数按逗号分隔
            for i in a:
                b = i.split('=')  # 每个参数再按=号分隔
                if len(b) > 1:
                    params[b[0]] = '='.join(b[1:])  # 带=号的参数作为字典传入
                else:
                    params['arg%s' % (a.index(i) + 100)] = i
        if kwargs:
            print "using **kwargs===>"
            params = dict(params.items() + kwargs.items())
        # print params
        print "params==>", params
        obj = urllib.urlencode(params)
        res = self.PostRequest(obj)
        # print res
        return res

    def allMinionKeys(self):
        '''
        返回所有Minion keys；
        分别为 已接受、待接受、已拒绝；
        :return: [u'local', u'minions_rejected', u'minions_denied', u'minions_pre', u'minions']
        '''
        params = {'client': 'wheel', 'fun': 'key.list_all'}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        minions = content['return'][0]['data']['return']['minions']
        minions_pre = content['return'][0]['data']['return']['minions_pre']
        minions_rej = content['return'][0]['data']['return']['minions_rejected']
        return minions, minions_pre, minions_rej

    def actionKyes(self, keystrings, action):
        '''
        对Minion keys 进行指定处理；
        :param keystrings: 将要处理的minion id字符串；
        :param action: 将要进行的处理，如接受、拒绝、删除；
        :return:
        {"return": [{"tag": "salt/wheel/20160322171740805129", "data": {"jid": "20160322171740805129", "return": {}, "success": true, "_stamp": "2016-03-22T09:17:40.899757", "tag": "salt/wheel/20160322171740805129", "user": "zhaogb", "fun": "wheel.key.delete"}}]}
        '''
        func = 'key.' + action
        params = {'client': 'wheel', 'fun': func, 'match': keystrings}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret

    def acceptKeys(self, keystrings):
        '''
        接受Minion发过来的key；
        :return:
        '''
        params = {'client': 'wheel', 'fun': 'key.accept', 'match': keystrings}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret

    def deleteKeys(self, keystrings):
        '''
        删除Minion keys；
        :param node_name:
        :return:
        '''
        params = {'client': 'wheel', 'fun': 'key.delete', 'match': keystrings}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret

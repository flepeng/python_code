# -*- coding:utf-8 -*-
"""
    @Time  : 2022/3/29  11:29
    @Author: Feng Lepeng
    @File  : awvs.py.py
    @Desc  : awvs 相关
"""


import requests
import time
import json
import urllib3
from flask import current_app


verify = False
token = ''


class Awvs(object):

    def __init__(self):
        self.url = current_app.config.get("AWVS_URL")
        self.api_key = current_app.config.get("AWVS_API_KEY")
        self.target_id = ''
        self.scan_id = ''
        self.session_id = ''

    def build_url(self, url=None, sub_url=None):
        return '{0}{1}'.format(url, sub_url)

    def connect(self, method=None, sub_url=None, data=None):
        """
            该模块用来定制连接
        """

        headers = {
            'content-type': 'application/json',
            'X-Auth': self.api_key,
        }
        try:
            data = json.dumps(data)
            urllib3.disable_warnings()

            if method == 'POST':
                r = requests.post(self.build_url(self.url, sub_url), data=data, headers=headers, verify=verify)
            elif method == 'PUT':
                r = requests.put(self.build_url(self.url, sub_url), data=data, headers=headers, verify=verify)
            elif method == 'DELETE':
                r = requests.delete(self.build_url(self.url, sub_url), data=data, headers=headers, verify=verify)
            elif method == 'PATCH':
                r = requests.patch(self.build_url(self.url, sub_url), data=data, headers=headers, verify=verify)
            else:
                r = requests.get(self.build_url(self.url, sub_url), params=data, headers=headers, verify=verify)
        except Exception as e:
            print(e)
            return False

        # Exit if there is an error.
        if r.status_code == 204:
            return True
        elif r.status_code != 200:
            e = r.json()
            return e

        if 'download' in sub_url:
            return r.content
        else:
            return r.json()

    def connect_all(self, method=None, sub_url=None, data=None):
        """
            该模块用来定制连接
        """

        headers = {
            'content-type': 'application/json',
            'X-Auth': self.api_key,
        }

        try:
            data = json.dumps(data)
            urllib3.disable_warnings()

            if method == 'POST':
                r = requests.post(self.build_url(self.url, sub_url), data=data, headers=headers, verify=verify)
            elif method == 'PUT':
                r = requests.put(self.build_url(self.url, sub_url), data=data, headers=headers, verify=verify)
            elif method == 'DELETE':
                r = requests.delete(self.build_url(self.url, sub_url), data=data, headers=headers, verify=verify)
            elif method == 'PATCH':
                r = requests.patch(self.build_url(self.url, sub_url), data=data, headers=headers, verify=verify)
            else:
                r = requests.get(self.build_url(self.url, sub_url), params=data, headers=headers, verify=verify)
        except Exception as e:
            return e
        return r

    def add_target(self, address=None, description=None):
        scan = {
            'address': address,
            'description': description,
            'criticality': '10',
        }

        try:
            data = self.connect('POST', '/api/v1/targets', data=scan)
            self.target_id = data['target_id']
            return self.target_id

        except Exception as e:
            print(e)
            return 'error'

    def start_job(self, target_id=None):
        """
            11111111-1111-1111-1111-111111111112    High Risk Vulnerabilities
            11111111-1111-1111-1111-111111111115    Weak Passwords
            11111111-1111-1111-1111-111111111117    Crawl Only
            11111111-1111-1111-1111-111111111116    Cross-site Scripting Vulnerabilities
            11111111-1111-1111-1111-111111111113    SQL Injection Vulnerabilities
            11111111-1111-1111-1111-111111111118    quick_profile_2: 0: {"wvs": {"profile": "continuous_quick"}}
            11111111-1111-1111-1111-111111111114    quick_profile_1: 0: {"wvs": {"profile": "continuous_full"}}
            11111111-1111-1111-1111-111111111111    Full Scan: 1: {"wvs": {"profile": "Default"}}
        """
        target_id = target_id if target_id else self.target_id
        scan = {
            'target_id': target_id,
            'profile_id': '11111111-1111-1111-1111-111111111111',
            'schedule': {
                'disable': False,
                'start_date': None,
                'time_sensitive': False,
            },
            'report_template_id': '11111111-1111-1111-1111-111111111111'
        }
        data = self.connect('POST', '/api/v1/scans', data=scan)
        """返回值
            {
                u'schedule': {
                    u'disable': False, 
                    u'time_sensitive': False, 
                    u'start_date': None, 
                    u'triggerable': False
                },
                u'profile_id': u'11111111-1111-1111-1111-111111111111', 
                u'target_id': u'0bb03c60-4946-42fc-8687-669cd161c523',
                u'ui_session_id': None, 
                u'incremental': False, 
                u'report_template_id': u'21111111-1111-1111-1111-111111111111',
                u'max_scan_time': 0
            }
        """
        return data

    def get_all_scans(self):
        # 获取所有扫描
        scans = self.connect('GET', '/api/v1/scans')
        return scans

    def get_specify_scan_id(self, target_id=''):
        # 根据target_id 匹配 最新的扫描id
        target_id = target_id if target_id else self.target_id
        scans = self.get_all_scans()

        for scan in scans['scans']:
            if scan['target_id'] == target_id:
                self.scan_id = scan['scan_id']
                return self.scan_id
        return self.scan_id

    def get_specify_scan_status(self, scan_id=''):
        # 根据 scan_id 获取当前状态 状态类型：queued：队列中 processing：运行中 aborted：禁止 completed：完成 scheduled

        scan_id = scan_id if scan_id else self.scan_id
        data = self.connect('GET', '/api/v1/scans/{0}'.format(scan_id))
        """
        {
            "criticality": 10,
            "current_session": {
                "acusensor": true,
                "event_level": 1,
                "progress": 100,
                "scan_session_id": "21124419-2a02-458e-82bf-fabab3462ddc",
                "severity_counts": {
                    "high": 45,
                    "info": 26,
                    "low": 10,
                    "medium": 66
                },
                "start_date": "2020-04-13T10:17:09.880580+00:00",
                "status": "completed",
                "threat": 3
            },
            "incremental": false,
            "manual_intervention": false,
            "max_scan_time": 0,
            "next_run": null,
            "profile_id": "11111111-1111-1111-1111-111111111111",
            "profile_name": "Full Scan",
            "report_template_id": null,
            "scan_id": "506a2238-aaf2-487a-884b-b152fedffb10",
            "schedule": {
                "disable": false,
                "history_limit": null,
                "recurrence": null,
                "start_date": null,
                "time_sensitive": false,
                "triggerable": false
            },
            "target": {
                "address": "http://testphp.vulnweb.com/",
                "criticality": 10,
                "description": "AWVS\u6d4b\u8bd5\u9776\u573a",
                "type": "default"
            },
            "target_id": "7b70e73f-bad0-4531-99a8-69d916ed7e66"
        }
        """

        status = data.get('current_session').get('status')
        return status

    def get_specify_scan_sessionid(self, scan_id=''):
        # 根据 scan_id 获取 session_id
        scan_id = scan_id if scan_id else self.scan_id
        data = self.connect('GET', '/api/v1/scans/{0}'.format(scan_id))
        self.session_id = data['current_session']['scan_session_id']
        return self.session_id

    def delete_specify_scan(self, scan_id):
        # 根据 scan_id 删除扫描
        data = self.connect('DELETE', '/api/v1/targets/{0}'.format(scan_id))
        return data

    def stop_specify_scan(self, scan_id):
        # 根据 scan_id 停止扫描
        data = self.connect('POST', '/api/v1/scans/{0}/abort'.format(scan_id))
        return data

    def get_statistics(self, scan_id, scan_session_id):
        # 根据 session_id 获取扫描状态信息
        data = self.connect('GET', '/api/v1/scans/{0}/results/{1}/statistics'.format(scan_id, scan_session_id))
        return data

    def get_specify_scan_vulns(self, scan_id, scan_session_id):
        # 根据 session_id 获取所有检测出的Item, 包括高危、中危、低危等
        """
            {u'vulnerabilities': [
                {u'status': u'open',
                 u'confidence': 95,
                 u'affects_url': u'https://misc.com/user/changeinfo/',
                 u'loc_id': 77,
                 u'severity': 2,
                 u'criticality': 10,
                 u'tags': [u'CWE-200', u'information_disclosure', u'error_handling'],
                 u'target_id': u'c156add1-b79b-49cc-8c1f-3eb7d3798fee',
                 u'vt_name': u'Application error message',
                 u'vuln_id': u'2400821291792729497',
                 u'affects_detail': u'description',
                 u'vt_id': u'760d5a01-dc58-fcbe-6c21-4f04c64a2467',
                 u'last_seen': None},
                {u'status': u'open',
                 u'confidence': 95,
                 u'affects_url': u'https://misc.com/user/changeinfo/',
                 u'loc_id': 77,
                 u'severity': 2,
                 u'criticality': 10,
                 u'tags': [u'CWE-200', u'information_disclosure', u'error_handling'],
                 u'target_id': u'c156add1-b79b-49cc-8c1f-3eb7d3798fee',
                 u'vt_name': u'Application error message',
                 u'vuln_id': u'2400821292186994075',
                 u'affects_detail': u'mobilephone',
                 u'vt_id': u'760d5a01-dc58-fcbe-6c21-4f04c64a2467',
                 u'last_seen': None}]
            }
        """

        data = self.connect('GET', '/api/v1/scans/{0}/results/{1}/vulnerabilities'.format(scan_id, scan_session_id))
        return data

    def get_specify_scan_specify_vulns(self, scan_id, scan_session_id, vuln_id):
        # 根据 vulnerable id 获取具体信息
        """
        {
            u'affects_detail': u'',
            u'references': [
                {u'href': u'https://www.php.net/manual/en/errorfunc.configuration.php#ini.display-errors', u'rel': u'PHP Runtime Configuration'},
                {u'href': u'https://www.owasp.org/index.php/Improper_Error_Handling', u'rel': u'Improper Error Handling'}
            ],
            u'recommendation': u'Verify that this page is disclosing error or warning messages and properly configure the application to log errors to a file instead of displaying the error to the user.',
            u'vt_id': u'd6b36f54-09ec-af8d-df8a-5f76932151ca',
            u'long_description': u'While information disclosure vulnerabilities are not directly exploitable by an attacker, they may help an attacker to learn about system specific information. The following is a list of <strong>some</strong> of the information an attacker may be able to obtain from application error disclosure.<br/>  <ul>   <li>Internal IP addresses</li>   <li>Secrets (passwords, keys, tokens...)</li>   <li>Operating system distributions</li>   <li>Software version numbers</li>   <li>Missing security patches</li>   <li>Application stack traces</li>   <li>SQL statements</li>   <li>Location of sensitive files (backups, temporary files...)</li>   <li>Location of sensitive resources (databases, caches, code repositories...)</li> <ul>',
            u'impact': u'Error messages may disclose sensitive information which can be used to escalate attacks.',
            u'confidence': 95,  # 可信度
            u'severity': 2,     # 严重程度
            u'highlights': [{u'index': 7745, u'length': 42, u'in': u'body'}],
            u'source': u'/Scripts/PerFolder/Invalid_Page_Text_Search.script',
            u'details': u' Pattern found: <pre><span class="bb-blue">You&#x27;re seeing this error because you have </span></pre> ',
            u'cvss_score': 5.3,
            u'vt_name': u'Error message on page',  # 名称
            u'status': u'open',  # 状态
            u'description': u'<div class="bb-coolbox"><span class="bb-dark">This alert requires manual confirmation</span></div><br/>\n\nApplication error or warning messages may expose sensitive information about an application\'s internal workings to an attacker.<br/><br/>\n\nAcunetix found an error or warning message that may disclose sensitive information. The message may also contain the location of the file that produced an unhandled exception. Consult the \'Attack details\' section for more information about the affected page.',
            u'criticality': 10,  # 可信度
            u'tags': [u'CWE-200', u'information_disclosure', u'error_handling'],  # 标签
            u'response_info': True,
            u'target_id': u'7088a410-93bc-4a11-86db-9ca05cb8326d',
            u'vuln_id': u'2409333161478587534',
            u'cvss2': u'AV:N/AC:L/Au:N/C:P/I:N/A:N',
            u'cvss3': u'CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N',
            u'affects_url': u'https://misc.inc.com/user/',  # 影响url
            u'loc_id': 6, u'request': u'GET /user/SIWGglZ5yA.jsp HTTP/1.1\r\nCookie: csrftoken=hcakXInVRnKQ0DiYNGI84T6fOlf0fbhQlj6vwdt0k36gcUIAtuhTZCTnSad4gVfX\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: gzip,deflate\r\nHost: misc.sec.com\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36\r\nConnection: Keep-alive\r\n\r\n'
        }
        """
        url = 'https://10.199.2.88:3443/api/v1/vulnerabilities/2313032422372934872'
        data = self.connect('GET', '/api/v1/scans/{}/results/{}/vulnerabilities/{}'.format(scan_id, scan_session_id, vuln_id))
        return data

    def make_report(self, scan_id):
        """
            11111111-1111-1111-1111-111111111111    Developer
            21111111-1111-1111-1111-111111111111    XML
            11111111-1111-1111-1111-111111111119    OWASP Top 10 2013
            11111111-1111-1111-1111-111111111112    Quick
        """

        data = {
            'template_id': '11111111-1111-1111-1111-111111111111',
            'source': {
                'list_type': 'scans',
                'id_list': [scan_id]
            }
        }
        response = self.connect_all('POST', '/api/v1/reports', data=data)
        header = response.headers

        report = self.url + header['Location'].replace('/api/v1/reports/', '/reports/download/') + '.xml'
        return report

    def get_all_report(self):
        """
            11111111-1111-1111-1111-111111111111    Developer
            21111111-1111-1111-1111-111111111111    XML
            11111111-1111-1111-1111-111111111119    OWASP Top 10 2013
            11111111-1111-1111-1111-111111111112    Quick
        """

        response = self.connect('GET', '/api/v1/reports')
        """
        {u'pagination': {
            u'count': 11, 
            u'sort': None, 
            u'cursors': [None],
            u'cursor_hash': u'8f629dd49f910b9202eb0da5d51fdb6e'}, 
            u'reports': [{
                u'status': u'completed', 
                u'template_name': u'Developer', 
                u'template_type': 0,
                u'source': {u'id_list': [u'519efd7f-5603-4f5b-88c1-18d631669366'],u'description': u'https://misc.com/user/;vms scan', u'list_type': u'scans'},
                u'download': [u'/api/v1/reports/download/1cd6907e3a2594f23f2fbc4b0efb276a9f6694fffa6f681b757a94e299530cbb09c09ff05f649286ade0184c-bbe1-4e99-a327-52c643beb94b.html',u'/api/v1/reports/download/c930856293fa388e604b9442f37835d81f6c7424864b58f96fb38c79aea6d6db179067985f649286ade0184c-bbe1-4e99-a327-52c643beb94b.pdf'],
                u'generation_date': u'2020-09-18T09:32:18.001845+00:00',
                u'template_id': u'11111111-1111-1111-1111-111111111111',
                u'report_id': u'ade0184c-bbe1-4e99-a327-52c643beb94b'}]
        }
        """
        return response

    def get_specify_report(self, scan_id):

        ret = self.get_all_report()
        for i in ret['reports']:
            if i['source']['id_list'] == [scan_id]:
                return i['download']
        """
        {u'pagination': {
            u'count': 11, 
            u'sort': None, 
            u'cursors': [None],
            u'cursor_hash': u'8f629dd49f910b9202eb0da5d51fdb6e'}, 
            u'reports': [{
                u'status': u'completed', 
                u'template_name': u'Developer', 
                u'template_type': 0,
                u'source': {u'id_list': [u'519efd7f-5603-4f5b-88c1-18d631669366'],u'description': u'https://misc.inc.com/user/;vms scan', u'list_type': u'scans'},
                u'download': [u'/api/v1/reports/download/1cd6907e3a2594f23f2fbc4b0efb276a9f6694fffa6f681b757a94e299530cbb09c09ff05f649286ade0184c-bbe1-4e99-a327-52c643beb94b.html',u'/api/v1/reports/download/c930856293fa388e604b9442f37835d81f6c7424864b58f96fb38c79aea6d6db179067985f649286ade0184c-bbe1-4e99-a327-52c643beb94b.pdf'],
                u'generation_date': u'2020-09-18T09:32:18.001845+00:00',
                u'template_id': u'11111111-1111-1111-1111-111111111111',
                u'report_id': u'ade0184c-bbe1-4e99-a327-52c643beb94b'}]
        }
        """
        return False

    def configure(self, target_id, cookie, url):
        """ 高级设置 """
        conf = {
            'custom_cookies': [{  # 自定义cookie
                'url': url,
                'cookie': cookie
            }]
        }
        res = self.connect('PATCH', '/api/v1/scans/{0}/configuration'.format(target_id), data=conf)
        if res:
            data = self.start_job(target_id)
        return data

    def site_login(self, target_id, user, password, cookie='', url=''):
        # 登录
        conf = {
            'login': {
                'kind': "automatic",
                'credentials': {
                    'enabled': 'true',
                    'username': user,
                    'password': password
                }
            }
        }

        res1 = self.connect('PATCH', '/api/v1/targets/{0}/configuration'.format(target_id), data=conf)  # 成功返回 True
        if res1:
            data = self.configure(target_id, cookie, url)
        return data

    def crawling(self, target_id, user, password, cookie, url, agent, exclude_url):
        conf = {
            "limit_crawler_scope": 'true',
            "case_sensitive": "no",
            "excluded_paths": [exclude_url],
            "user_agent": agent
        }

        res2 = self.connect('PATCH', '/api/v1/targets/{0}/configuration'.format(target_id), data=conf)
        if res2:
            # data = start(target_id, scanner_id)
            data = self.site_login(target_id, user, password, cookie, url)
        return data

    def advanced(self, target_id):
        conf = {
            "issue_tracker_id": "",
            "technologies": ["ASP", "ASP.NET"],
            "custom_headers": ["h4rdy:xxx"],
            "custom_cookies": [],
            "debug": 'false',
            "excluded_hours_id": ""
        }
        res = self.connect('PATCH', '/api/v1/scans/{0}/configuration'.format(target_id), data=conf)
        if res:
            data = self.start_job(target_id)
        return data


def factory_scan(url, user='', password=''):

    awvs = Awvs()
    target_id = awvs.add_target(url, 'vms scan')  # '0bb03c60-4946-42fc-8687-669cd161c523'

    if user:
        job_status = awvs.site_login(target_id, user, password)
    else:
        job_status = awvs.start_job(target_id)

    scan_id = awvs.get_specify_scan_id(target_id)
    scan_status = awvs.get_specify_scan_status(scan_id)
    while scan_status.lower() not in ['aborted', 'completed']:
        time.sleep(5)
        scan_status = awvs.get_specify_scan_status(scan_id)
    # print scan_status

    session_id = awvs.get_specify_scan_sessionid(scan_id)
    vulns = awvs.get_specify_scan_vulns(scan_id, session_id)
    vulns_list = []
    for vuln in vulns['vulnerabilities']:
        ret = awvs.get_specify_scan_specify_vulns(scan_id, session_id, vuln['vuln_id'])
        vulns_list.append(ret)
    return vulns_list

    # awvs.stop_specify_scan(scan_id)
    # awvs.delete_specify_scan(target_id)
    # todo: 删除记录，删除target


if __name__ == "__main__":
    """
    target_id: 节点id c156add1-b79b-49cc-8c1f-3eb7d3798fee
    scan_id：扫描id 519efd7f-5603-4f5b-88c1-18d631669366
    session_id：会话id
    """
    ret = factory_scan(url='https://misc.com/user/')









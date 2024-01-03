# -*- coding:utf-8 -*-
"""
    @Time  : 2022/3/14 18:19
    @Author: Feng Lepeng
    @File  : jira_util.py
    @Desc  : jira 脚本
"""

import os
import time
import datetime
import logging
from jira.client import JIRA

# from config.config import configs, Config
configs, Config = "", ""
from dateutil.parser import parse

# create logger
log = logging.getLogger(__name__)


class JiraOperate(object):

    def __init__(self):
        self._jira_server = "https://jira..com"
        self._jira_user = ""
        self._jira_password = ""
        self._project_key = ""

        self.jira = self.connect_jira()
        if self.jira is None:
            log.error("Failed to connect to jira.")

    def connect_jira(self):
        """
        Connect to JIRA. Return None on error
        """
        try:
            log.info("Connecting to JIRA: %s" % self._jira_server)
            jira_options = {'server': self._jira_server}
            jira = JIRA(options=jira_options, basic_auth=(self._jira_user, self._jira_password))
            # ^--- Note the tuple
            return jira
        except Exception as e:
            log.exception("Failed to connect to JIRA")
            return None

    def _refresh_config(self):
        jira_conf = {}
        conf_dir = configs.get("jiraAccount", {}).get("ConfigReleaseDir", "")
        config_path = os.path.join(conf_dir, "config/config.yaml")
        if os.path.exists(config_path):
            jira_conf = Config.load_config(config_path)
        if jira_conf is not None and "jiraAccount" in jira_conf:
            return jira_conf
        else:
            return configs

    def get_issue(self, issue_key):
        """
        获取 issue
        :param issue_key:
        :return:
        """
        jira_handler = self.jira
        issue_handler = None
        try:
            issue_handler = jira_handler.issue(issue_key)
            log.info("Get issue handler success.")
        except Exception as e:
            log.exception("Get issue({}) handler error".format(issue_key))
        return jira_handler, issue_handler

    def update_issue(self, issue_key, update_field, update_value):
        """
        更新 issue 字段值
        :param issue_key:
        :param update_field:
        :param update_value:
        :return
        """
        ret = None
        jira_handler, issue_handler = self.get_issue(issue_key)

        if issue_handler:
            ret = issue_handler.update(fields={update_field: update_value})
        else:
            logging.error("Update issue({}) error".format({update_field, update_value}))

        return ret

    def infoBackfill(self, jira_data, update_field, update_value):
        """
        信息回填
        :param jira_data:
        :param update_value:
        :param update_field:
        :return:
        """
        self.updateIssue(jira_data['key'], update_field, update_value)
        logging.info('信息回填%s！' % update_field)

    def associatedBackfill(self, jira_data, update_field, update_value):
        """
        信息回填到关联的问题中
        :param jira_data:
        :param update_value:
        :param update_field:
        :return:
        """
        if not jira_data.get('链接的问题'): return
        # 获取链接的问题key
        for i in jira_data.get('链接的问题'):
            for j in ('outwardIssue', 'inwardIssue'):
                try:
                    fiel_value = self.getFieldsValue(i.get(j).get('key'), update_field)
                    if isinstance(fiel_value, list): update_value = update_value + fiel_value
                    self.updateIssue(i.get(j).get('key'), update_field, update_value)
                    logging.info('信息回填%s！' % update_field)
                except Exception as e:
                    print(j, e)

    def associatedChangeDay(self, jira_data, time_field):
        """
        更新日期
        信息回填到关联的问题中
        """
        if not jira_data.get('链接的问题'): return
        # 获取链接的问题key
        for i in jira_data.get('链接的问题'):
            try:
                issue_key = i.get('outwardIssue').get('key')
                rel_sync = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                self.updateIssue(issue_key, time_field, rel_sync)
            except Exception as e:
                print(e)

    def correlative(self, jira_data, update_field):
        """
        链接的问题
        jira项目相互打通，问题关联，自动回填
        :param key:
        :param jira_data:
        :return:
        """
        if not jira_data.get('链接的问题'): return
        link_key_list = []
        # 获取链接的问题key
        for i in jira_data.get('链接的问题'):
            try:
                link_key_list.append(i.get('outwardIssue').get('key'))
            except Exception as e:
                print(e)
        # 自动回填到目标key中，相互关联
        for key in link_key_list:
            self.updateIssue(key, update_field, jira_data['key'])
            logging.info('信息回填%s！' % update_field)

    def associated_transform_workflow(self, jira_data, work_flow):
        """转换关联的问题工作流"""
        if not jira_data.get('链接的问题'): return
        # 获取链接的问题key
        for i in jira_data.get('链接的问题'):
            for j in ('outwardIssue', 'inwardIssue'):
                try:
                    self.jira.transition_issue(i.get(j).get('key'), work_flow)
                    logging.info('转换工作流%s' % work_flow)
                except Exception as e:
                    print(j, e)

    def transform_workflow(self, jira_data, work_flow):
        """转换工作流"""
        issue_key = jira_data['key']
        time.sleep(10)  # 等信息回填了在转换工作流
        self.jira.transition_issue(issue_key, work_flow)
        logging.info('转换工作流%s' % work_flow)

    def changeOperator(self, jira_data, user_id, owner_field):
        """
        更新经办人
        user_id 经办人名称
        owner_field 对应自定义字段
        :param jira_data:
        :param user_id:
        :param owner_field:
        :return:
        """

        issue_key = jira_data['key']
        self.updateIssue(issue_key, owner_field, {'name': user_id})
        logging.info("Change RD to %s" % user_id)

    def changeMultiUser(self, jira_data, user_list, owner_field):
        """
        修改多用户字段
        传入列表 ['caiqinxiong','zhaokeke'],转换成[{'name': 'caiqinxiong'},{'name':'zhaokeke'}]
        """
        user_dict = []
        for i in user_list:
            user_dict.append({'name': i})
        issue_key = jira_data['key']
        self.updateIssue(issue_key, owner_field, user_dict)
        logging.info("Change RD to %s" % user_list)

    def changeAssignee(self, jira_data, user_id):
        """
        更新经办人,系统自带经办人字段
        分配问题
        """
        self.jira.assign_issue(jira_data['key'], user_id)

    def changeDate(self, jira_data, time_field):
        """
        更新时间
        """
        issue_key = jira_data['key']
        rel_sync = '%sT%s.000+0800' % (
            time.strftime('%Y-%m-%d', time.localtime(time.time())),
            time.strftime('%H:%M:%S', time.localtime(time.time())))
        self.updateIssue(issue_key, time_field, rel_sync)

    def changeDay(self, jira_data, time_field):
        """
        更新日期
        """
        issue_key = jira_data['key']
        rel_sync = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        self.updateIssue(issue_key, time_field, rel_sync)

    def getParentIssueFields(self, issue_key):
        # 获取父任务ISSUE对象
        jira_handler, issue_handler = self.get_issue(issue_key)
        return issue_handler.fields

    def getFieldsValue(self, issue_key, fiel):
        """
        获取字段的值，链接的问题字段
        :param key:
        :param fiel:
        :return:
        """
        fiel_value = self.getParentIssueFields(issue_key).__dict__.get(fiel)
        return fiel_value

    def changeStatus(self, jira_data, work_flow):
        """
        更新jira工作流，状态转换
        :param jira_data:
        :param work_flow:
        :return:
        """
        issue_key = jira_data['key']
        self.jira.transition_issue(issue_key, work_flow)

    def get_all_comments(self, jira_data):
        """
        获取所有评论信息
        评论者：author
        评论日期：created （2021-07-14T10:29:12.738+0800）
        评论内容：body
        for i in comment_id_lsit:
            print(i.author)
            print(i.created)
            print(i.body)
        :return:
        """
        issue_key = jira_data['key']
        comment_id_list = self.jira.comments(issue_key)
        jira_data["所有评论"] = comment_id_list
        return jira_data

    def remove_duplicate_comments(self, jira_data):
        """
        去除重复评论，只获取个人最后一次评论
        :param jira_data:
        i.author.key = “caiqinxiong”
        :return:
        """
        tmp = {}
        comment_id_list = []
        # 利用字典的key唯一性，同人名的取最后一次值
        for i in jira_data["所有评论"]:
            tmp[i.author.key] = i
        # 只需获取字典的值就行
        for k, v in tmp.items():
            comment_id_list.append(v)
        jira_data["所有评论"] = comment_id_list
        return jira_data

    def remove_some_comments(self, jira_data, name_list, F=True):
        """去除机器人自动添加的评论信息,或其他不想展示的信息"""
        comment_list = []
        issue_key = jira_data['key']
        comment_id_list = self.jira.comments(issue_key)
        for i in comment_id_list:
            if F:
                if i.author.key in name_list: comment_list.append(i)
            else:
                if not i.author.key in name_list: comment_list.append(i)
        jira_data["所有评论"] = comment_list
        return jira_data

    def add_new_comment(self, jira_data, comment):
        """增加评论"""
        issue_key = jira_data['key']
        return self.jira.add_comment(issue_key, comment)

    def search_issues(self, jql, start_index=0, block_size=100):
        """
        通过jql对jira进行检索.
        :param jql:
        :return:
        """
        issues = []
        self.jql = jql

        while True:
            end_index = start_index + block_size
            _issues = self.jira.search_issues(jql, start_index, end_index, validate_query=False)
            issues += _issues

            if len(_issues) == 0:
                break
            start_index = end_index

        print("{} issues were found.".format(len(issues)))
        return issues

    def bug_close_use_time(self, jira_data, update_field, fiel_name):
        """自动回填BUG关闭用时"""
        try:
            createdtime = parse(jira_data.get('创建日期').split('.')[0].replace('T', ' '))
            currenttime = parse(jira_data.get('currenttime'))
            usedays = str((currenttime - createdtime).days)
            useseconds = (currenttime - createdtime).seconds
            useseconds = str(datetime.timedelta(seconds=useseconds))
            hours = str(useseconds.split(':')[0])
            minutes = str(useseconds.split(':')[1])
            seconds = str(useseconds.split(':')[2])
            usetime = usedays + "天" + hours + "小时" + minutes + "分钟" + seconds + "秒"
            jira_data[fiel_name] = usetime
            self.infoBackfill(jira_data, update_field, usetime)
        except Exception as e:
            print(e)

        return jira_data

    def get_expiration_time(self, last_updated_time, currenttime):
        """获取超时未更新时间"""
        try:
            last_updated_time = parse(last_updated_time.split('.')[0].replace('T', ' '))
            currenttime = parse(currenttime)
            usedays = str((currenttime - last_updated_time).days)
            useseconds = (currenttime - last_updated_time).seconds
            useseconds = str(datetime.timedelta(seconds=useseconds))
            hours = str(useseconds.split(':')[0])
            minutes = str(useseconds.split(':')[1])
            seconds = str(useseconds.split(':')[2])
            expirationtime = usedays + "天" + hours + "小时" + minutes + "分钟" + seconds + "秒"
        except Exception as e:
            print(e)
            expirationtime = ''
        return expirationtime

    def create_issuse(self, data):
        """
        创建一个 issue：
            data={
                'project':{'key':'TES'},
                'issuetype':'主流程-硬件项目流程',
                'summary':'脚本自动创建的哦',
                'customfield_12000':'V1.2.0',
                'customfield_12125':'开发目标',
                'customfield_12001':'2020-01-03',
                'customfield_12989':{'value':'是'},
                'customfield_12961':{'value':'是'},
            }
        :param data:
        :return:
        """
        return self.jira.create_issue(fields=data)

    def create_issuses(self, jira_data_list):
        """批量创建问题
        issue_list = [
            {
                'project': {'id': 123},
                'summary': 'First issue of many',
                'description': 'Look into this one',
                'issuetype': {'name': 'Bug'},
            },
            {
                'project': {'key': 'FOO'},
                'summary': 'Second issue',
                'description': 'Another one',
                'issuetype': {'name': 'Bug'},
            },
            {
                'project': {'name': 'Bar'},
                'summary': 'Last issue',
                'description': 'Final issue of batch.',
                'issuetype': {'name': 'Bug'},
            }]
            """
        return self.jira.create_issues(field_list=jira_data_list)

    def show_projects(self):
        print(self.jira.projects())
        for project in self.jira.projects():
            print(project.key)
            print(project.name)

    def show_project(self, project_key):
        project = self.jira.project(project_key)
        print(project.key, project.name, project.lead)

    def upload_attachment(self, issue_key, attachment):
        """
        上传附件
        :param issue_key:
        :return: 文件名
        """
        return self.jira.add_attachment(issue=issue_key, attachment=attachment)


if __name__ == "__main__":
    project_key = "SAFEDEMO"
    issue_key = "SAFEDEMO-7"
    obj = JiraOperate()
    print(obj.jira.fields())
    for i in obj.jira.fields():
        print(i.get("name"))
        print(i)
    # print(obj.getFieldsValue(issue_key, "description"))
    exit()
    data = {
        "project": {"key": project_key},
        "issuetype": {"name": "安全专项"},      # 问题类型。安全专项：11523
        # "issuetype": {"id": "11523"},          # 问题类型。安全专项：11523

        "summary": "test概要",                   # 概要

        "priority": {"id": "1"},                 # 优先级Highest：1 -->  lowest：5
        # "priority": {"name": "Highest"},       # 优先级Highest：1 -->  lowest：5

        "assignee": {"name": "-1"},              # 经办人 自动：-1

        # "customfield_11703": {"id": "11438", "1": "11446"},      # EBG产品族 koala 11438
        "customfield_11703": {"value": "Koala", "child": {"value": "Koala-通行"}},      # EBG产品族 koala 11438, Koala-通行 11446

        "customfield_13081": {"id": "14125"},               # 漏洞等级
        # "customfield_13081": {"value": "严重"},           # 漏洞等级

        "customfield_13078": {"value": "上线前安全测试"},  # 问题来源
        "customfield_12492": {"value": "必然出现"},        # 复现概率
        # "customfield_12946": ["V1.2.0", "1.0.5"],           # 影响版本
        # "customfield_12946": [{"value":"V1.2.0"}, {"value":"1.0.5"}],    # 影响版本
        "description": '',
        "customfield_13079": '2022-04-30',                   # 修复时间
        "customfield_12180": [{"name": 'fenglepeng'}],                   # 通知人
        "customfield_12886": [{"name": 'secteam'}],                   # 邮件组
    }
    ret = obj.create_issuse(data)
    # ret = obj.upload_attachment(issue_key)
    # ret = obj.update_issue(issue_key, "description", "<p>系统存在如下低版本依赖，可能存在可被利用的0day。</p>!!")
    print(ret)

#!/usr/bin/env python3
# =====================================================================
# jira_activities.py
# Description: Create any jira activities on the Jira board
# =====================================================================
# Date                    Author                      Desc
# ---------------------------------------------------------------------
# 03/29/2023        Omolewa Adaramola               Initial
# =====================================================================
import re
import requests
import json
from requests.auth import HTTPBasicAuth
from jira import JIRA
import credentials
#

class JiraActivities():
    def __init__(self):
        self.jira = JIRA(server=credentials.url,
                         basic_auth=(credentials.user_email, credentials.token))

        # for field in self.jira.fields():
        #     print(field.values())
        # print(self.jira.fields())
        #issue = self.jira.issue("BLT-1")
        #print(issue.get_field("customfield_10034"))

        # for field in fields:
        #     for key in field.items():
        #         print(key)
            # print(field.keys())
            # print(field.values())
        #print(self.jira.custom_field_option("customfield_10034"))

    def createSupportJira(self, reporter, priority, distruption, issue, reproduce, dump, fieldNames:dict=None):
        """

        :param reporter:
        :param priority:
        :param distruption:
        :param issue:
        :param reproduce:
        :param dump:
        :param test:
        :return:
        """
        diag = json.loads(dump)
        description = (
            "h4.-- PRIORITY --\r\n"
            f"{priority}\r\n"
            "h4.-- SERVICE DISTRUPTION --\r\n"
            f"{distruption}\r\n"
            "h4.-- ISSUE DISCRIBED --\r\n"
            f"{issue}\r\n"
            "h4.-- STEPS TO PRODUCE --\r\n"
            f"{reproduce}\r\n"
            "h4.-- DIAGNOSTIC INFO --\r\n"
            "h5.Browser: \r\n"
            f"{diag['browser']}\r\n"
            "hh5.Location: \r\n"
            f"{diag['location']}\r\n"
        )

        jira_dict = {
            "project":
                {
                    "key": "BLT"
                },
            "summary": f"Request By - {reporter.first_name} {reporter.last_name} {reporter.username}",
            "description": description,
            "issuetype": {
                "name": "Task"
            },
            "assignee": {
                "name": [reporter.username]
            }
        }
        create_issue = self.jira.create_issue(jira_dict)

        if fieldNames != None:
            customFieldIdDict = self.getCustomFieldId(list(fieldNames.keys()))

            for field in fieldNames.keys():
                create_issue.update(fields={customFieldIdDict[field]: [fieldNames[field]]})

        return create_issue

    def getCustomFieldId(self, *fieldNames):
        """
        This method is used to get the custom field id which is required to update
        :param fieldName: str -> jira cutom field name
        :return: str -> field id
        """
        fields = self.jira.fields()

        customFieldIdDict = {}
        for field in fields:
            if field['name'] in fieldNames:
                customFieldIdDict[field['name']] = field['id']

        return customFieldIdDict

    def searchIssues(self, projectID="ERT", maxResults=50):
        """

        :param projectID:
        :param maxResults:
        :return:
        """
        return self.jira.search_issues("project = "+projectID, maxResults=maxResults)

    def getProjects(self):
        """

        :return:
        """
        projects = self.jira.projects()
        return projects

    def searchForProject(self, projectKey):
        """

        :param projectKey:
        :return:
        """
        projects = self.getProjects()
        keys = [project.key for project in projects if (project.key == projectKey)]
        if len(keys) > 0:
            return True
        return False

    def getComment(self, ticketNumber):
        """

        :param ticketNumber:
        :return:
        """
        issue = self.jira.issue(f"BLUE-1")

        atl_comments = [
            comment
            for comment in issue.fields.comment.comments
            if re.search(r"@atlassian.com$", comment.author)
        ]
        return atl_comments

    def addComment(self, issue, comment):
        """

        :param issue: str -> issue number: ex. "BLUE-1"
        :param comment: str -> the comments to add to the issue
        :return:
        """
        self.jira.add_comment(issue, comment)


if __name__ == "__main__":
    jira = JiraActivities()
    print(jira.getCustomFieldId("Business Sponsor"))
    # print(jira.searchForProject("BLUE"))
    # print(jira.addComment("BLUE-1"))


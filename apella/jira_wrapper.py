#!/usr/bin/env python
# -*- coding: utf-8 -*-
from jira import JIRA

from django.conf import settings


def create_issue(jira_issue):
    jira = JIRA(
        options = settings.JIRA_OPTIONS, basic_auth=settings.JIRA_LOGIN)
    issue = {
        'project': settings.JIRA_PROJECT,
        'summary': jira_issue.title,
        'description': jira_issue.description,
        'issuetype': {'name' : 'Πρόβλημα'},
        'customfield_12350': jira_issue.reporter.username,
        'customfield_12552': jira_issue.user.username,
        'customfield_12550': jira_issue.user.email
    }

    created_issue = jira.create_issue(issue)
    return created_issue

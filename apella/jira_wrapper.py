#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from jira import JIRA
from django.conf import settings

ISSUE_TYPES = {
    "complaint": "Παράπονα",
    "error": "Πρόβλημα",
    "general_information": "Γενικές πληροφορίες",
    "account_modification": "Μεταβολή στοιχείων",
    "registration": "Εγγραφή/Πιστοποίηση",
    "login": "Θέματα πρόσβασης"
}

logger = logging.getLogger(__name__)


def create_issue(jira_issue):
    jira = JIRA(
        options=settings.JIRA_OPTIONS, basic_auth=settings.JIRA_LOGIN)
    issue = {
        'project': settings.JIRA_PROJECT,
        'labels': [settings.JIRA_LABEL],
        'summary': jira_issue.title,
        'description': jira_issue.description,
        'issuetype': {'name': ISSUE_TYPES.get(jira_issue.issue_type)},
        'customfield_12350': jira_issue.reporter.username,
        'customfield_12552': jira_issue.user.username,
        'customfield_12550': jira_issue.user.email
    }

    created_issue = jira.create_issue(issue)
    logger.info("created jira issue %i", created_issue.id)
    return created_issue

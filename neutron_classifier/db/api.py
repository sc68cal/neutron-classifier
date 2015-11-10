# Copyright (c) 2015 Mirantis, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from neutron_classifier.db import models
from oslo_db.sqlalchemy import enginefacade


@enginefacade.transaction_context_provider
class ClassifierContext(object):
    "Classifier Database Context."


def get_classifier_chain():
    pass


@enginefacade.writer
def create_classifier_chain(context, classifier_group, classifier):
    chain = models.ClassifierChainEntry()
    chain.sequence = 1
    chain.classifier = classifier
    chain.classifier_group = classifier_group
    context.session.add(chain)


@enginefacade.writer
def convert_security_group_rule_to_classifier(context, security_group_rule):
    # TODO(sc68cal) Pass in the classifier group
    group = models.ClassifierGroup()
    group.service = 'security-group'

    # Pull the source from the SG rule
    cl1 = models.IpClassifier()
    cl1.source_ip_prefix = security_group_rule['remote_ip_prefix']

    # Ports
    cl2 = models.TransportClassifier()
    cl2.destination_port_range_min = security_group_rule['port_range_min']
    cl2.destination_port_range_max = security_group_rule['port_range_max']

    chain1 = models.ClassifierChainEntry()
    chain1.classifier_group = group
    chain1.classifier = cl1
    chain1.sequence = 1

    chain2 = models.ClassifierChainEntry()
    chain2.classifier_group = group
    chain2.classifier = cl2
    # Security Group classifiers might not need to be nested or have sequences
    chain2.sequence = 1
    context.session.add(group)
    context.session.add(cl1)
    context.session.add(cl2)
    context.session.add(chain1)
    context.session.add(chain2)


@enginefacade.writer
def convert_firewall_rule_to_classifier(context, firewall_rule):
    pass


@enginefacade.reader
def convert_classifier_chain_to_security_group(context, chain_id):
    pass


@enginefacade.reader
def convert_classifier_to_firewall_policy(context, chain_id):
    pass

FROM fedora:28
RUN dnf install -y --nogpgcheck ansible \
    && dnf clean all
RUN mkdir /playbooks/
COPY semimodular_deployment /playbooks/semimodular_deployment
COPY semimodular-play.yml /playbooks/

RUN ansible-playbook -i "localhost," -c local /playbooks/semimodular-play.yml

#belongs in the playbook, but gpg checking can not seem to be disabled
RUN dnf update -y --nogpgcheck dnf \
    && dnf clean all

#belongs in the playbook, but gpg checking can not seem to be disabled
RUN dnf install -y --enablerepo "updates-testing" --nogpgcheck  fedora-repos-modular \
    && dnf clean all


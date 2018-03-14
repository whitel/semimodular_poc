FROM fedora-minimal:28
RUN sed -i -e 's/gpgcheck=1/gpgcheck=0/g' /etc/yum.repos.d/*
RUN microdnf install -y dnf ansible
RUN mkdir /playbooks/
COPY semimodular_deployment /playbooks/semimodular_deployment
COPY semimodular-play.yml /playbooks/

RUN ansible-playbook -i "localhost," -c local /playbooks/semimodular-play.yml

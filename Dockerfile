FROM fedora
RUN dnf install -y ansible
RUN mkdir /playbooks/
COPY semimodular_deployment /playbooks/semimodular_deployment
COPY semimodular-play.yml /playbooks/

RUN ansible-playbook -i "localhost," -c local /playbooks/semimodular-play.yml


# !/bin/bash
set -x

readonly AWS_CREDENTIALS="${HOME}/.aws/credentials"
readonly SSH_DIR="${HOME}/.ssh"
readonly ANSIBLE_PEM="${SSH_DIR}/ansible.pem"
readonly ANSIBLE_HOSTS="${HOME}/hosts"


[[ -f "${AWS_CREDENTIALS}" ]] || exit 1

pushd tf

if [[ -d ".terraform" ]]; then
    terraform init
fi
terraform plan -output .tfplan
terraform apply -auto-approve .tfplan
terraform output -raw private-key > "${ANSIBLE_PEM}"

echo '[master]' > "${ANSIBLE_HOSTS}"
echo "$(terraform output -raw ansible-0)" >> "${ANSIBLE_HOSTS}"
echo '[nodes]' >> "${ANSIBLE_HOSTS}"

for index in $(seq 1 2);
do
    echo "$(terraform output -raw "ansible-${index}")" >> "${ANSIBLE_HOSTS}"
done
popd

source ./ansible-install.sh

pushd ./ansible
ansible-playbook -vv --private-key "${ANSIBLE_PEM}" -i "${ANSIBLE_HOSTS}" users.yml
ansible-playbook -vv --private-key "${ANSIBLE_PEM}" -i "${ANSIBLE_HOSTS}" install-k8s.yml
# This will require sudo password
ansible-playbook -vv --private-key "${ANSIBLE_PEM}" -i "${ANSIBLE_HOSTS}" -K k8s-master.yml 
ansible-playbook -vv --private-key "${ANSIBLE_PEM}" -i "${ANSIBLE_HOSTS}" -K k8s-nodes.yml
popd
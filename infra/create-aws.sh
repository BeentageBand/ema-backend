# !/bin/bash
set -x

readonly AWS_CREDENTIALS="${HOME}/.aws/credentials"
readonly SSH_DIR="${HOME}/.ssh"
readonly ANSIBLE_PEM="${SSH_DIR}/ansible.pem"
readonly ANSIBLE_HOSTS="${HOME}/hosts"


[[ -f "${AWS_CREDENTIALS}" ]] || exit 1

pushd tf

terraform init
terraform apply -auto-approve
terraform output -raw private-key > "${ANSIBLE_PEM}"

echo '[master]' > "${ANSIBLE_HOSTS}"
echo "$(terraform output -raw ansible-0)" >> "${ANSIBLE_HOSTS}"
echo '[nodes]' >> "${ANSIBLE_HOSTS}"

for index in $(seq 1 2);
do
    echo "$(terraform output -raw "ansible-${index}")" >> "${ANSIBLE_HOSTS}"
done
popd

exit 0


pushd ./ansible
ansible-playbook --private-key "${ANSIBLE_PEM}" -u 'ubuntu' -i "${ANSIBLE_HOSTS}" users.yml
ansible-playbook --private-key "${ANSIBLE_PEM}" -u 'ubuntu' -i "${ANSIBLE_HOSTS}" install-k8s.yml
ansible-playbook --private-key "${ANSIBLE_PEM}" -u 'ubuntu' -i "${ANSIBLE_HOSTS}" master.yml
ansible-playbook --private-key "${ANSIBLE_PEM}" -u 'ubuntu' -i "${ANSIBLE_HOSTS}" join-workers.yml
popd
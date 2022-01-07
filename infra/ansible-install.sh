# !/bin/bash
set -x
# Node Installation
if ! command -v ansible; then
    sudo apt update
    sudo apt install -y ansible 
    sudo sed -i '71s;.*;host_key_checking = False;' /etc/ansible/ansible.cfg
    sudo sed -i '136s;.*;private_key= ~/.ssh/ema.pem;' /etc/ansible/ansible.cfg
fi

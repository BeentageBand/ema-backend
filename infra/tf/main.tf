provider "aws" {
  shared_credentials_file = "~/.aws/credentials"
  profile                 = "default"
  region                  = "us-east-1"
}

resource "tls_private_key" "private-key" {
  algorithm   = "RSA"
  rsa_bits    = 2048
}

resource "aws_key_pair" "deployer" {
  key_name   = "deployer-key"
  public_key = tls_private_key.private-key.public_key_openssh
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_security_group" "ansible-sg" {
  name = "Ansible-SG"
  description = "Student security group"

  tags = {
    Name = "Ansible-SG"
    Environment = terraform.workspace
  }
}

resource "aws_security_group_rule" "create-sgr-ssh" {
  security_group_id = aws_security_group.ansible-sg.id
  cidr_blocks       = ["0.0.0.0/0"]
  from_port         = 22
  protocol          = "tcp"
  to_port           = 22
  type              = "ingress"
}

resource "aws_security_group_rule" "create-sgr-inbound" {
  security_group_id = aws_security_group.ansible-sg.id
  cidr_blocks       = ["0.0.0.0/0"]
  from_port         = 0
  protocol          = "all"
  to_port           = 65535
  type              = "ingress"
}

resource "aws_security_group_rule" "create-sgr-outbound" {
  security_group_id = aws_security_group.ansible-sg.id
  cidr_blocks         = ["0.0.0.0/0"]
  from_port         = 0
  protocol          = "all"
  to_port           = 65535
  type              = "egress"
}

resource "aws_instance" "ansible" {
  count         = 3
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
  key_name      = aws_key_pair.deployer.key_name
  security_groups = ["Ansible-SG"]
  tags = {
    Name = "Ansible${count.index}"
  }
}

resource "null_resource" "ansible-node" {
    depends_on = [null_resource.ansible-pem]

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = tls_private_key.private-key.private_key_pem
      host        = aws_instance.ansible.*.public_dns[0]
    }


    provisioner "file" {
        source      = "${path.cwd}/ansible-node.sh"
        destination = "/tmp/ansible-node.sh"
    }

    provisioner "remote-exec" {
        inline = [
          "chmod u+x /tmp/ansible-node.sh",
          "/tmp/ansible-node.sh",
          "echo '[ansible]' > ~/hosts",
          "echo '${aws_instance.ansible.*.public_dns[1]}' >> ~/hosts",
          "echo '${aws_instance.ansible.*.public_dns[2]}' >> ~/hosts"
        ]
    }
}

resource "null_resource" "ansible-pem" {
    depends_on = [aws_instance.ansible]
    count = length(aws_instance.ansible)

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = tls_private_key.private-key.private_key_pem
      host        = aws_instance.ansible.*.public_dns[count.index]
    }

    provisioner "remote-exec" {
      inline =[
        "echo '${tls_private_key.private-key.private_key_pem}' > ~/.ssh/ansible.pem && chmod 600 ~/.ssh/ansible.pem",
      ]
    }

    provisioner "local-exec" {
      command = "echo '${tls_private_key.private-key.private_key_pem}' > ~/.ssh/ansible.pem && chmod 600 ~/.ssh/ansible.pem "
    }
}

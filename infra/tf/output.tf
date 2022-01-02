output "private-key" {
  value = tls_private_key.private-key.private_key_pem
  sensitive = true
}

output "public-key-openssh" {
  value = tls_private_key.private-key.public_key_openssh
}

output "ansible-0" {
  value = aws_instance.ansible.*.public_ip[0]
}

output "ansible-1" {
  value = aws_instance.ansible.*.public_ip[1]
}

output "ansible-2" {
  value = aws_instance.ansible.*.public_ip[2]
}

resource "aws_instance" "web" {
  ami           = "ami-04f59c565deeb2199"
  instance_type = "t2.medium"
  key_name      = "richardnv"
  # No security group specified = uses default
  user_data = file("${path.module}/setup.sh")
  tags = {
    Name = "Richard_Instance"
  }
}
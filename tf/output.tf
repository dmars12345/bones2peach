output "secret_key" {
value = aws_iam_access_key.test43.secret
sensitive = true
}


output "access_key" {
  value = aws_iam_access_key.test43.id
}

resource "local_file" "secret" {
    content  = aws_iam_access_key.test43.secret
    filename = "secret.txt"
}

resource "local_file" "id" {
    content  = aws_iam_access_key.test43.id
    filename = "id.txt"
}

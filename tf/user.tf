resource "aws_iam_user" "test43" {
  name = "test43"
}

resource "aws_iam_access_key" "test43" {
  user = aws_iam_user.test43.name
}

resource "aws_s3_bucket" "primalformulas" {
    bucket = "primalformulas.ie"

    tags = {
        Name = "primalformulas.ie"
    }
}

resource "aws_s3_bucket_ownership_controls" "primalformulas_ownership" {
  bucket = aws_s3_bucket.primalformulas.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "primalformulas_acl" {
  depends_on = [aws_s3_bucket_ownership_controls.primalformulas_ownership]

  bucket = aws_s3_bucket.primalformulas.id
  acl    = "public-read"
}

resource "aws_s3_bucket_public_access_block" "primalformulas_access_block" {
  bucket = aws_s3_bucket.primalformulas.id

  block_public_acls   = false
  ignore_public_acls  = false
  block_public_policy = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "primalformulas_policy" {
    bucket = aws_s3_bucket.primalformulas.id

    policy = jsonencode({
        Version = "2012-10-17",
        Statement = [
            {
                Sid = "AllowPublicRead",
                Action = "s3:GetObject",
                Effect = "Allow",
                Principal = { "AWS": "*" },
                Resource = "arn:aws:s3:::primalformulas.ie/*"
            }
        ]
    })
}

resource "aws_s3_bucket_cors_configuration" "primalformulas_cors" {
    bucket = aws_s3_bucket.primalformulas.id

    cors_rule {
        allowed_headers = ["*"]
        allowed_methods = [            
            "GET",
            "PUT",
            "POST",
            "DELETE",
            "HEAD"
        ]
        allowed_origins = ["*"]
        expose_headers  = ["Etag"]
        max_age_seconds = 3000
    }
}
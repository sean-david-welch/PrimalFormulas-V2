!#/bin/zsh

curl -X POST http://127.0.0.1:8000/api/products \  ─╯
-H 'Content-Type: application/json' \
	-d '{
    "name": "Test Product",
    "description": "Product Description",
    "price": 10.99,
    "image": "image.url"
}'

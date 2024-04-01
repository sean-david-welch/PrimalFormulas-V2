!#/bin/zsh

# Post Products
curl -X POST http://127.0.0.1:8000/api/products \
-H 'Content-Type: application/json' \
	-d '{
    "name": "Test Product",
    "description": "Product Description",
    "price": 10.99,
    "image": "image.url"
}'

curl -X POST http://127.0.0.1:8000/api/about \
-H 'Content-Type: application/json' \
	-d '{
    "title": "Test About",
    "description": "Product Description",
    "image": "image.url"
}'

curl -X PUT http://127.0.0.1:8000/api/about/1d01de5a-d6b4-46af-8ec4-a1ebb9d6e4c8/ \
-H 'Content-Type: application/json' \
-d '{
    "title": "Updated Test About",
    "description": "Updated Product Description",
    "image": "updated.image.url"
}'

curl -X DELETE http://127.0.0.1:8000/api/about/1d01de5a-d6b4-46af-8ec4-a1ebb9d6e4c8/

curl -X POST http://127.0.0.1:8000/logout \
     -H "Authorization: Token your_token_here"

curl -X POST http://127.0.0.1:8000/register \
     -H "Content-Type: application/json" \
     -d '{
           "username": "newuser",
           "email": "newuser@example.com",
           "password": "securepassword",
           "is_superuser": false
         }'


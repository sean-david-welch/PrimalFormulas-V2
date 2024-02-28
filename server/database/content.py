# import logging

# from uuid import uuid4
# from datetime import datetime

# from models.models import Content
# from utils.database import get_async_pool

# pool = get_async_pool()
# logger = logging.getLogger()

# async def get_content() -> list[Content]:
#     query = "SELECT * FROM content"

#     try:
#         async with pool.connection() as conn, conn.cursor() as cursor:
#             await cursor.execute(query)
#             rows = await cursor.fetchall()

#             return [
#                 Content[
#                     id
#                 ]
#             ]

import asyncio, aiohttp, aiofiles, maya

from datetime import datetime

VALID_DATE = datetime(2021,9,22).date()
TOKEN = open('TOKEN', 'r').readline()
HEADERS = {'Accepts': 'application/json', 'Authorization': f'token {TOKEN}'}

async def get_repository_info(repository, api_url):
  async with aiohttp.ClientSession(headers=HEADERS) as session:
    async with session.get(api_url) as response:
      response = await response.json()
      is_valid_repository = True
      
      try:
        created_at = maya.parse(response['created_at']).datetime().date()
      except:
        is_valid_repository = False

      if VALID_DATE > created_at or not is_valid_repository:
        async with aiofiles.open('invalid_github_repositories.csv', 'a') as f:
          await f.write(repository)

      return response


repositories = open('github_urls.csv','r').readlines()
tasks = []

for repository in repositories:
  repository_api_url = repository.replace('https://github.com/', 'https://api.github.com/repos/')

  tasks.append(get_repository_info(repository, repository_api_url))

asyncio.run(asyncio.wait(tasks))

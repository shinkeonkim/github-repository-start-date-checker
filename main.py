# coding: utf8
import asyncio, aiohttp, aiofiles, maya

from datetime import datetime

VALID_DATE = datetime(2021,9,22).date()
TOKEN = open('TOKEN', 'r').readline()
HEADERS = {'Accepts': 'application/json', 'Authorization': f'token {TOKEN}'}

async def get_repository_info(team_number, team_name, repository, api_url):
  async with aiohttp.ClientSession(headers=HEADERS) as session:
    async with session.get(api_url) as response:
      response = await response.json()
      is_valid_repository = True
      
      try:
        created_at = maya.parse(response['created_at']).datetime().date()
      except:
        created_at = 'ERROR'
        is_valid_repository = False

      if not is_valid_repository or VALID_DATE > created_at or response['fork']:
        async with aiofiles.open('invalid_github_repositories.csv', 'a',encoding='utf8') as f:
          await f.write(repository)
      async with aiofiles.open('results.csv', 'a',encoding='utf8') as f:
        await f.write(",".join([team_number, team_name, str(created_at), repository]))

      return response


repositories = open('github_urls.csv','r',encoding='utf8').readlines()
tasks = set()

for repository_info in repositories:
  team_number, team_name, repository = repository_info.split(',')
  
  repository_api_url = repository.replace('https://github.com/', 'https://api.github.com/repos/')
  tasks.add(get_repository_info(team_number, team_name, repository, repository_api_url))

asyncio.run(asyncio.wait(tasks))

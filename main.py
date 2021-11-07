import aiohttp as aih
import asyncio
import sys
import json
import aiofiles

async def download(session,url,name):
    print("Starting download "+name)
    async with session.get(url) as resp:
        if resp.status == 200:
            f = await aiofiles.open(name, mode='wb')
            await f.write(await resp.read())
            await f.close()
            print("Download of "+name+" OKAY!")

async def getrawdata():
    async with aih.ClientSession() as ses:
        async with ses.get("https://tenor.com/search/"+sys.argv[-1]+"-gifs") as resp:
            return await resp.text()

async def getJSON():
    e = await getrawdata()
    e=e[e.find("<script id=\"store-cache\" type=\"text/x-cache\" nonce="):]
    e = json.loads(e[e.find("{"):e.find("</script>")])
    return e

async def geturls():
    e = await getrawdata()
    e=e[e.find("<script id=\"store-cache\" type=\"text/x-cache\" nonce="):]
    e = json.loads(e[e.find("{"):e.find("</script>")])['gifs']['search']
    e = e[list(e.keys())[0]]['results']
    urls = []
    for i in e:
        urls.append(i['media'][0]['gif']['url'])
    return urls

async def main():
    # TODO: Argparser, download mp4 files (they exists)
    if len(sys.argv[1:])==0:
        print("Search query not specified... Exiting...")
        exit()
    urls = await geturls()
    print("=====[Gotta download "+str(len(urls))+" GIFs!]=====")
    async with aih.ClientSession() as session:
        print("Getting ready...")
        tasks = []
        for url in urls:
            tasks.append(asyncio.ensure_future(download(session, url, url.split("/")[-1])))

        result = await asyncio.gather(*tasks)

asyncio.run(main())

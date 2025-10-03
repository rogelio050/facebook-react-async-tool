import aiohttp
import aiofiles
import asyncio

FB_REACT_URL = "https://graph.facebook.com/v18.0/{}/reactions"
CONCURRENCY_LIMIT = 10  # Adjust as needed

async def send_reaction(session, post_id, access_token, reaction_type, sem):
    url = FB_REACT_URL.format(post_id)
    params = {
        "type": reaction_type,
        "access_token": access_token
    }
    async with sem:
        try:
            async with session.post(url, params=params, timeout=10) as resp:
                data = await resp.json()
                if resp.status != 200 or 'error' in data:
                    print(f"Error for token {access_token[:6]}...: {data}")
                else:
                    print(f"Success for token {access_token[:6]}...: {data}")
        except Exception as e:
            print(f"Request failed for token {access_token[:6]}...: {e}")

async def load_tokens(filename):
    tokens = []
    async with aiofiles.open(filename, "r") as f:
        async for line in f:
            token = line.strip()
            if token:
                tokens.append(token)
    return tokens

async def main(post_id, reaction_type, tokens_file):
    tokens = await load_tokens(tokens_file)
    sem = asyncio.Semaphore(CONCURRENCY_LIMIT)
    async with aiohttp.ClientSession() as session:
        tasks = [
            send_reaction(session, post_id, token, reaction_type, sem)
            for token in tokens
        ]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python facebook_react_async.py <post_id> <reaction_type> <tokens_file>")
        sys.exit(1)
    post_id = sys.argv[1]
    reaction_type = sys.argv[2]
    tokens_file = sys.argv[3]
    asyncio.run(main(post_id, reaction_type, tokens_file))

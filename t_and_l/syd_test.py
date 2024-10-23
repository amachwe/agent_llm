import asyncio

from sydney import SydneyClient

async def main() -> None:
	prompt = f"Generate a list of three made up book titles including authors and genres. Return in JSON format"
	
	async with SydneyClient() as syd:
		
		print("S:",end="", flush=True)
		async for response in syd.ask_stream(prompt):
			print(response, end="", flush=True)
		print("\n")

if __name__ == "__main__":
	asyncio.run(main())
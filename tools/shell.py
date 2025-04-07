import asyncio

async def run(command: str, thread: dict):
    """
    Runs the given command, like ls, cat, sed, echo, curl, python3, etc. in a Linux shell.
    Commands run in a docker container sandbox, so feel free to write to disk, etc.
    """
    print(f"{thread["assistant"]}: shell: {command}")
    out, err = await (await asyncio.create_subprocess_shell(
        command,
        stdout = asyncio.subprocess.PIPE,
        stderr = asyncio.subprocess.PIPE
    )).communicate()
    return (out or err).decode()

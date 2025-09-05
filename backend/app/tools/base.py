from langchain.tools import BaseTool
from typing import Optional, Type

class CustomBaseTool(BaseTool):
    name: str
    description: str
    args_schema: Optional[Type] = None

    def _run(self, *args, **kwargs):
        raise NotImplementedError("Synchronous _run() must be implemented.")

    async def _arun(self, *args, **kwargs):
        raise NotImplementedError("Asynchronous _arun() must be implemented.")

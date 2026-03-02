from src.repositories import LogRepository

class Logger:
    def __init__(self, log_repo: LogRepository):
        self._repo = log_repo

    async def info(self, message: str, *, component: str, metadata: dict | None = None):
        await self._write("INFO", component, message, metadata)

    async def warn(self, message: str, *, component: str, metadata: dict | None = None):
        await self._write("WARN", component, message, metadata)

    async def error(self, message: str, *, component: str, metadata: dict | None = None):
        await self._write("ERROR", component, message, metadata)

    async def _write(self, level, component, message, metadata):
        try:
            await self._repo.insert_log(level, component, message, metadata)
            print(f"{level} | message: {message} | component: {component} | metadata: {metadata}")
        except Exception:
            return
from fastmcp import FastMCP
from fastmcp.server.middleware import Middleware, MiddlewareContext

# 创建一个简单的日志记录中间件
class LoggingMiddleware(Middleware):
    async def on_message(self, context: MiddlewareContext, call_next):
        print(f"[LOG] Received request: {context.method} {context.message}")
        try:
            result = await call_next(context)
            print(f"[LOG] Request succeeded: {context.method}")
            return result
        except Exception as e:
            print(f"[LOG] Request failed: {context.method}, error: {str(e)}")
            raise

# 创建代理
proxy = FastMCP.as_proxy(
    "http://127.0.0.1:5030/sse",
    name="chatlogmcp",
)

# 将中间件添加到代理服务器
proxy.add_middleware(LoggingMiddleware())

if __name__ == "__main__":
    proxy.run(transport='stdio')


from fastmcp import FastMCP
from fastmcp.server.middleware import Middleware, MiddlewareContext

class LoggingMiddleware(Middleware):
    async def on_message(self, context: MiddlewareContext, call_next):
        print(f"[LOG] Received request: {context.method} {context.message}")
        try:
            result = await call_next(context)
            
            # 检查结果是否包含 content 属性（通常是 MCP 响应格式）
            if hasattr(result, 'content'):
                # 遍历 content 数组，查找 text 类型的条目
                for item in result.content:
                    if hasattr(item, 'text'):
                        # 1. 按照 \n\n 进行分割
                        segments = item.text.split('\n\n')
                        
                        # 2. 过滤掉包含 ![图片] 或 ![动画表情] 的分割项
                        filtered_segments = [
                            segment for segment in segments 
                            if '![图片]' not in segment and '![动画表情]' not in segment
                        ]
                        
                        # 3. 重新拼接处理后的内容
                        processed_text = '\n\n'.join(filtered_segments)
                        
                        # 更新内容的 text 属性
                        item.text = processed_text
            
            
            
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


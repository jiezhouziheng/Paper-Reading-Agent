# Frontend

最小前端模块。

当前使用原生 HTML、CSS 和 JavaScript，先提供一个简单页面用于连接后端论文分析接口。后续可以按需要升级为 React 或 Vue。

## 本地预览

直接在浏览器中打开 `index.html` 即可。

如果需要调用后端接口，请先启动后端服务：

```bash
cd backend
uvicorn app.main:app --reload
```

页面顶部会显示后端状态：

- `后端状态：可用` 表示接口可以访问。
- `后端状态：不可用` 表示先检查后端服务是否启动。

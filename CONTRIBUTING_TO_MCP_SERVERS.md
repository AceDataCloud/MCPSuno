# 提交到 MCP Servers 官方仓库指南

本文档说明如何将 mcp-suno 提交到 [MCP Servers 官方仓库](https://github.com/modelcontextprotocol/servers)。

## 步骤

### 1. Fork 官方仓库

访问 https://github.com/modelcontextprotocol/servers 并点击 Fork。

### 2. 克隆你的 Fork

```bash
git clone https://github.com/YOUR_USERNAME/servers.git
cd servers
```

### 3. 添加你的 Server 条目

编辑 `README.md`，在合适的分类下添加你的 server。

在 **Media** 或 **Third-Party Servers** 分类下添加：

```markdown
### Suno AI Music (mcp-suno)

- **Repository**: [AceDataCloud/mcp-suno](https://github.com/AceDataCloud/mcp-suno)
- **Author**: [AceDataCloud](https://platform.acedata.cloud)
- **License**: MIT

Generate AI music, lyrics, and manage audio projects using Suno through the AceDataCloud API.

**Features:**
- Music generation from text prompts
- Custom lyrics and style control
- Song extension and cover creation
- Lyrics generation
- Persona/voice style management
- Task progress tracking

**Installation:**
```bash
pip install mcp-suno
```

**Configuration:**
```json
{
  "mcpServers": {
    "suno": {
      "command": "mcp-suno",
      "env": {
        "ACEDATA_API_TOKEN": "your_token"
      }
    }
  }
}
```
```

### 4. 创建 Pull Request

```bash
git checkout -b add-mcp-suno
git add README.md
git commit -m "Add mcp-suno: AI music generation server via AceDataCloud"
git push origin add-mcp-suno
```

然后在 GitHub 上创建 Pull Request。

### PR 描述模板

```markdown
## Add mcp-suno Server

### Description
This PR adds mcp-suno, an MCP server for AI music generation using Suno through the AceDataCloud API.

### Server Details
- **Name**: mcp-suno
- **Repository**: https://github.com/AceDataCloud/mcp-suno
- **Package**: https://pypi.org/project/mcp-suno/
- **Language**: Python
- **License**: MIT

### Features
- Generate AI music from text prompts
- Custom lyrics, title, and style control
- Extend existing songs from any timestamp
- Create cover/remix versions
- Generate structured lyrics
- Persona/voice style management
- Task progress tracking

### Checklist
- [x] Server is open source
- [x] Has clear documentation
- [x] Follows MCP specification
- [x] Tested and working
- [x] Published to PyPI
```

## 注意事项

1. **先发布到 PyPI** - 确保你的包已经发布到 PyPI 后再提交 PR
2. **完善文档** - 确保 README 清晰说明安装和使用方法
3. **遵循格式** - 按照官方仓库现有的格式添加条目
4. **响应评审** - PR 提交后可能需要根据维护者反馈进行修改

## 相关链接

- MCP Servers 仓库: https://github.com/modelcontextprotocol/servers
- MCP 规范: https://spec.modelcontextprotocol.io
- mcp-suno 仓库: https://github.com/AceDataCloud/mcp-suno

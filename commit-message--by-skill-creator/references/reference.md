# Conventional Commits 完整规范

## 格式

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Type 详解

| Type | 说明 | 何时使用 | 示例 |
|------|------|----------|------|
| `feat` | 新功能 | 向用户可见的新功能、API 端点、UI 组件 | `feat(api): add rate limiting middleware` |
| `fix` | Bug 修复 | 修复错误行为、崩溃、数据不一致 | `fix(auth): handle expired refresh tokens` |
| `docs` | 文档 | README、注释、API 文档、CHANGELOG | `docs(readme): add installation instructions` |
| `style` | 代码风格 | 不影响代码含义的变更（空格、格式化、分号） | `style: fix indentation in utils.py` |
| `refactor` | 重构 | 既不是修复也不是添加功能的代码变更 | `refactor(parser): simplify regex extraction` |
| `perf` | 性能优化 | 提升性能的代码变更 | `perf(db): add index to user lookup` |
| `test` | 测试 | 新增或修改测试用例、测试工具 | `test(auth): add unit tests for JWT validation` |
| `build` | 构建系统 | 构建脚本、依赖管理、打包配置 | `build(deps): upgrade react to v18` |
| `ci` | CI/CD | CI 配置、工作流、部署脚本 | `ci(github-actions): add linting step` |
| `chore` | 杂项 | 不属于以上类别的维护性变更 | `chore: update .gitignore for env files` |
| `revert` | 回退 | 回退之前的提交 | `revert: revert "feat(api): add rate limiting"` |

## Scope 建议

Scope 应描述变更影响的功能区域，常见命名：

- **按模块**：`auth`、`api`、`ui`、`db`、`cache`、`queue`
- **按文件/目录**：`readme`、`deps`、`github-actions`
- **按组件**：`navbar`、`login-form`、`payment-gateway`

Scope 不是必须的，以下情况可以省略：
- 变更影响多个不相关的模块
- 变更是全局性的（如格式化、依赖升级）
- 无法明确归属范围

## Body 编写指南

Body 是可选的，以下情况应该添加：
- 变更的动机不够明显，需要解释「为什么」
- 多个提交会被合并，需要保留详细信息
- 有 Breaking Change，需要详细说明
- 变更涉及多个文件的协调修改

Body 不需要包含：
- 具体的代码实现细节（diff 已经展示了）
- 过于冗长的背景说明（保持 2-3 段以内）

## Footer 类型

| Footer | 说明 | 示例 |
|--------|------|------|
| `BREAKING CHANGE` | 不兼容的 API 变更 | `BREAKING CHANGE: remove deprecated auth endpoint` |
| `Closes #N` | 关闭 Issue | `Closes #42` |
| `Refs #N` | 关联 Issue | `Refs #15, #23` |
| `Co-authored-by:` | 合作者 | `Co-authored-by: Name <email@example.com>` |
| `Reviewed-by:` | 审查者 | `Reviewed-by: Name <email@example.com>` |

## 常见错误

| 错误 | 问题 | 正确写法 |
|------|------|----------|
| `feat(auth): added JWT validation` | 使用过去式 | `feat(auth): add JWT validation` |
| `feat(auth): Add JWT validation.` | 末尾有句号 | `feat(auth): add JWT validation` |
| `feat(auth): update auth` | 过于模糊 | `feat(auth): add JWT-based token validation` |
| `feat: this is a very long subject line that exceeds the limit` | 超过 72 字符 | 使用 body 补充详情 |
| `update stuff` | 没有 type | `feat(core): add user preference caching` |

## 多行提交信息示例

```
feat(api): add rate limiting middleware

Implement token bucket algorithm to protect API endpoints from
abuse. Configurable via environment variables.

Default: 100 requests per minute per IP.

Closes #42
BREAKING CHANGE: rate limit headers are now required on all endpoints
```

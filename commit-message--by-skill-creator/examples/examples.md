# Commit Message 示例库

按场景分类的提交信息示例，供参考和复制。

## 新功能 (feat)

```
# 单一功能
feat(auth): add JWT-based user authentication

# 带 body 的完整描述
feat(api): implement rate limiting middleware

Protect API endpoints from abuse using token bucket algorithm.
Configurable via RATE_LIMIT_MAX and RATE_LIMIT_WINDOW env vars.

Default: 100 requests per minute per IP.

# UI 组件
feat(ui): add dark mode toggle to settings panel

# 数据库
feat(db): add user_preferences table with JSON settings column

# API 端点
feat(api): add POST /users/:id/avatar endpoint

# 工具函数
feat(utils): add debounce helper for event handlers
```

## Bug 修复 (fix)

```
# 空值检查
fix(ui): prevent crash when user list is empty

# 边界情况
fix(api): handle missing Authorization header gracefully

# 数据一致性问题
fix(db): use transaction for order + inventory updates

# 回归修复
fix(auth): revert to bcrypt 4.0 to fix login timeout

# 前端渲染
fix(navbar): close mobile menu on route change

# 并发问题
fix(queue): prevent duplicate job execution with mutex lock
```

## 文档 (docs)

```
docs(readme): add installation and setup instructions

docs(api): document rate limit headers in OpenAPI spec

docs(changelog): update v2.3.0 release notes
```

## 重构 (refactor)

```
refactor(parser): simplify regex extraction with named groups

refactor(auth): extract token validation into separate module

refactor(db): replace raw queries with query builder
```

## 性能 (perf)

```
perf(db): add composite index on (user_id, status)

perf(api): cache user profile lookups for 5 minutes

perf(build): parallelize webpack compilation with thread-loader
```

## 测试 (test)

```
test(auth): add unit tests for JWT token generation

test(api): add integration tests for rate limiting

test(e2e): add login flow Cypress test
```

## 样式 (style)

```
style: fix inconsistent indentation in auth.py

style(utils): format with prettier config

style: remove trailing whitespace from all .js files
```

## 构建/依赖 (build)

```
build(deps): upgrade react to v18.2.0

build(deps): add @types/node for TypeScript support

build(docker): update base image to node:20-alpine
```

## CI/CD (ci)

```
ci(github-actions): add linting step to pull request workflow

ci: split test matrix into unit and integration jobs

ci(deploy): add manual approval gate for production
```

## 杂项 (chore)

```
chore: update .gitignore for local env files

chore: bump version to 2.3.0

chore(scripts): clean up unused migration files
```

## 回退 (revert)

```
revert: revert "feat(api): add rate limiting middleware"

This caused timeout errors on high-traffic endpoints.
Will re-implement with adjusted thresholds.
```

## Breaking Change

```
feat(auth): replace session-based auth with JWT

BREAKING CHANGE: all existing sessions are invalidated.
Users must log in again to obtain a JWT token.

Closes #15, #23
```

## 多个不相关变更（建议拆分）

当变更涉及多个不相关领域时，**应该建议拆分**而非合并：

**不要这样做：**
```
chore: add Shopify template, QR code, and update settings
```

**应该建议拆分：**
```
建议拆分为 3 个独立提交：

1. feat(shopify): add product section Liquid template
2. chore: add QR code for mobile app pairing
3. chore(config): update Claude Code local permission settings
```

---
name: commit-message-creator
description: 使用 Conventional Commits 规范生成 Git 提交信息。当用户想要提交代码、创建 commit、写提交信息，或请求 git 提交帮助时触发。也应在用户说「代码写完了」「帮我保存进度」「任务完成了」或类似「帮我提交」「写个commit」「create a commit」「commit message」时触发——即使用户没有明确提到「Conventional Commits」。如果用户有未提交的变更且看起来准备提交，主动建议使用此 skill。
---

# 提交信息生成 Skill

根据当前工作树的实际代码变更，生成清晰、规范的 Conventional Commits 格式提交信息。

## 资源文件

| 路径 | 说明 | 何时使用 |
|------|------|----------|
| `references/reference.md` | Conventional Commits 完整规范（type/scope/body/footer 详解、常见错误对照） | 需要确认类型分类、footer 语法或 Breaking Change 格式时 |
| `examples/examples.md` | 按 12 种 type 分类的 50+ 条真实提交信息示例 | 需要参考类似变更的提交格式时 |
| `scripts/generate_commit_message.py` | Python 脚本：自动分析 git 变更并生成候选提交信息 | 变更文件较多，需要快速生成初稿时 |
| `agents/reviewer.md` | 提交信息质量审查子代理指令 | 需要二次审查提交信息是否符合规范时 |
| `assets/commit_template.txt` | Git commit 模板文件（可直接用于 `git commit -t`） | 用户想在本地编辑器中手动编写提交信息时 |
| `eval-viewer/generate_review.py` | 测试结果查看器（生成 HTML 报告） | 运行完测试用例后需要可视化对比结果时 |

## 工作流程

### 1. 分析变更内容

运行以下命令了解当前 git 状态：

```bash
git status
git diff          # 未暂存的变更
git diff --cached # 已暂存的变更
```

如果没有任何变更，告知用户并停止。

### 2. 确定提交类型

根据变更内容，选择合适的类型。详见 `references/reference.md` 中的 Type 详解表。

快速参考：

| 类型 | 适用场景 |
|------|----------|
| `feat` | 新功能或新特性 |
| `fix` | 修复 bug 或错误 |
| `docs` | 仅文档变更 |
| `style` | 代码格式、空格、lint（不影响代码逻辑） |
| `refactor` | 代码重构，行为不变 |
| `perf` | 性能优化 |
| `test` | 新增或修改测试 |
| `build` | 构建脚本、依赖管理 |
| `ci` | CI/CD 流水线变更 |
| `chore` | 其他维护性变更 |
| `revert` | 回退之前的提交 |

### 3. 确定影响范围（可选）

从变更文件中识别受影响的功能区域——如 `auth`、`api`、`ui`、`db`、`config`。如果变更涉及太多不相关的区域或范围不明确，可以省略 scope。

### 4. 编写提交信息

使用以下格式：

```
<type>(<scope>): <subject>

<body>          # 可选，仅在变更需要额外解释时添加

<footers>       # 可选，如 BREAKING CHANGE、Closes #123
```

**标题行规则：**
- 使用祈使句：「add」而非「added」或「adds」
- 末尾不加句号
- 总长度不超过 72 个字符（包含 type 和 scope）
- 默认英文，但如果用户偏好中文或项目使用中文提交信息，则用中文
- 要具体：「add JWT token validation」而非「update auth」
- **文件名不等于用途**：不要根据文件名前缀推断文件类型。例如 `test.liquid` 是 Shopify 模板文件而非测试文件，始终通过文件扩展名和实际内容来判断变更性质

**正文规则（如有）：**
- 说明变更的**内容**和**原因**（而非**方式**——diff 已经展示了）
- 段落之间空一行
- 每行不超过 72 个字符

### 5. 使用辅助脚本（可选）

当变更文件较多时，可以使用 `scripts/generate_commit_message.py` 快速生成初稿：

```bash
python scripts/generate_commit_message.py [--staged-only] [--scope SCOPE] [--language en|zh]
```

生成的结果作为参考，仍需人工审核和调整。

### 6. 质量审查（可选）

当需要确保提交信息符合规范时，可参考 `agents/reviewer.md` 中的审查清单：
- 格式合规检查（type/scope/subject/body 格式）
- 内容质量检查（是否具体、类型是否匹配）
- Breaking Change 和 Issue 链接检查

### 7. 向用户展示

提交前先展示拟好的提交信息，征求用户确认。示例：

```
拟好的提交信息：
---
feat(auth): add JWT token validation

- Implement HS256-based token generation
- Add middleware to verify Authorization header
- Update login endpoint to return refresh tokens
---
是否确认？我可以直接提交，你也可以提出修改建议。
```

### 8. 执行提交（需用户确认）

仅在用户明确同意后才运行 `git commit`。使用已确认的信息作为提交正文。

## 边界情况处理

- **多个不相关的变更**：必须明确建议拆分成独立提交，而非打包。例如变更包含 Shopify 模板、二维码图片和配置文件时，应分别建议三个 commit，而不是合并为一个。
- **文件名不等于用途**：不要根据文件名前缀推断文件类型。例如 `test.liquid` 是 Shopify 模板文件而非测试文件，`config.ini` 不一定属于 `chore` 类型。始终通过文件扩展名和实际内容来判断变更性质。
- **chore 类型要具体**：即使使用 `chore` 类型，subject 也要描述清楚做了什么。用 `chore: add Shopify template and QR code` 而非 `chore: add test files`。
- **变更量巨大**：如果变更太多无法简洁总结，提供一个高层级的标题，正文中列出关键变更。
- **无变更内容**：告知用户没有可提交的内容。
- **仅有已暂存的变更**：如果部分变更已暂存，优先基于已暂存的内容生成信息，再单独提及未暂存的变更。
- **用户想换风格**：如果用户说「简单点就行」或不认可 Conventional Commits，按用户偏好调整。

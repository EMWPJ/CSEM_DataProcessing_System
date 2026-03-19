# 贡献指南

欢迎参与CSEM数据处理系统的开发！

## 工作流程

### 1. 创建功能分支

从 `dev` 分支创建新分支：

```bash
git checkout dev
git checkout -b feature/功能名称
# 或
git checkout -b fix/问题描述
```

### 2. 开发与提交

```bash
# 开发...
git add .
git commit -m "描述: 具体做了什么"

# 推送到远程
git push -u origin feature/功能名称
```

### 3. 创建Pull Request

1. 在 GitHub 上创建 Pull Request
2. 目标分支选择 `dev`
3. 描述你的改动
4. 等待代码审查

### 4. 合并后清理

```bash
git checkout dev
git pull origin dev
git branch -d feature/功能名称  # 删除本地分支
```

---

## 分支命名规范

| 类型 | 命名格式 | 示例 |
|-----|---------|------|
| 功能 | `feature/名称` | `feature/emission-extractor` |
| 修复 | `fix/问题` | `fix/preprocessing-bug` |
| 文档 | `docs/内容` | `docs/api-guide` |
| 重构 | `refactor/模块` | `refactor/gui-widgets` |

---

## 提交信息规范

格式：`类型: 描述`

```
feat: 添加发射时段提取功能
fix: 修复带通滤波器边界问题
docs: 更新README
style: 格式化代码
refactor: 重构阻抗计算模块
test: 添加单元测试
```

---

## 模块任务分配

| 模块 | 状态 | 负责人 |
|-----|------|-------|
| `core/data_reader.py` | ✅ 基础框架 | - |
| `core/preprocessing.py` | ✅ 基础框架 | - |
| `core/spectrum.py` | ✅ 基础框架 | - |
| `core/emission_extractor.py` | ⏳ 待实现 | - |
| `core/impedance.py` | ✅ 基础框架 | - |
| `core/resistivity.py` | ✅ 基础框架 | - |
| `core/phase.py` | ✅ 基础框架 | - |
| `gui/` | ✅ 基础框架 | - |

---

## 开发规范

### Python 代码风格
- 使用 `snake_case` 命名变量和函数
- 类名使用 `PascalCase`
- 私有变量用 `_` 前缀
- 所有公共函数添加类型注解和docstring

### Git 规范
- 不要直接向 `main` 分支推送
- 功能完成后创建 Pull Request
- 每次提交应该是原子性的（完成一个功能或修复一个问题）

---

## 获取帮助

- 查看 [开发文档](docs/DEVELOP.md)
- 查看 [需求规格](SPEC.md)
- 提交 Issue 提问

---

## 许可证

本项目采用 MIT 许可证。

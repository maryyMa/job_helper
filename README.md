# Job Helper - 求职助手

基于AI的求职助手，根据用户信息和岗位JD生成定制简历和面试指南。

---

## 项目简介

这是一个opencode Agent项目，用于帮助求职者：
1. 根据目标岗位JD定制简历
2. 生成全面的面试准备指南
3. 确保所有内容基于真实数据，禁止编造

---

## 文件结构

```
job-helper/
├── AGENTS.md                              # Agent配置文件（核心）
├── 简历模板.md                              # 简历模板
├── .gitmessage                            # Git提交规范
├── .gitignore                             # Git忽略规则
├── README.md                              # 项目说明（本文件）
├── client/                                # 个人经历目录（不提交）
│   └── example.md                         # 示例文件
└── .opencode/
    └── skills/
        ├── analyze-jd/
        │   └── SKILL.md                   # 岗位分析技能
        ├── generate-resume/
        │   └── SKILL.md                   # 简历生成技能
        ├── generate-interview-guide/
        │   └── SKILL.md                   # 面试指南生成技能
        └── company-research/
            └── SKILL.md                   # 公司调研技能
```

---

## 配置步骤

### 1. 克隆仓库

```bash
git clone git@github.com:maryyMa/job_helper.git
cd job_helper
```

### 2. 配置个人经历

在 `client/` 目录下创建你的个人经历文件：

```bash
# 复制示例文件
cp client/example.md client/你的名字.md

# 例如
cp client/example.md client/张三.md
```

然后编辑 `client/你的名字.md`，填写你的个人信息：
- 基本信息（姓名、电话、邮箱、GitHub）
- 技术栈
- 工作经历
- 项目经验
- 教育背景
- 其他（博客、开源贡献、证书等）

### 3. 启动opencode

```bash
opencode
```

### 4. 使用Agent

```
@AGENTS 帮我生成简历，目标岗位是字节跳动的高级Android开发工程师
```

Agent会自动读取 `client/你的名字.md` 中的个人经历，并生成定制简历和面试指南。

---

## 使用方法

### 基本用法

```
@AGENTS 帮我生成简历
```

### 指定目标岗位

```
@AGENTS 帮我生成简历，目标岗位JD如下：
[粘贴岗位描述]
```

### 只做岗位分析

```
@AGENTS 分析一下这个岗位的要求
[粘贴岗位描述]
```

### 只做公司调研

```
@AGENTS 帮我调研一下字节跳动这家公司
```

---

## Agent功能

### 输入
- 个人经历：从 `client/你的名字.md` 读取
- 目标岗位JD：用户输入或指定公司+岗位

### 输出
1. **岗位分析**：关键词提取、理想候选人画像、岗位挑战
2. **公司调研**：公司背景、薪资、文化、近期动态
3. **定制简历**：基于简历模板生成的定制化简历
4. **面试指南**：面试问题预测、弱点应对、薪资谈判、面试Checklist

---

## 内容真实性保障

所有外部信息必须通过工具查询，禁止编造：
- 公司背景：使用webfetch访问官网
- 薪资数据：使用websearch搜索招聘平台
- 行业趋势：使用websearch搜索行业报告

---

## Skill说明

| Skill | 功能 |
|-------|------|
| analyze-jd | 分析岗位JD，提取关键词、画像、挑战 |
| generate-resume | 生成定制化简历 |
| generate-interview-guide | 生成面试指南 |
| company-research | 调研公司信息 |

---

## Git提交规范

提交信息格式：
```
<type>(<scope>): <subject>
```

Type类型：
- feat：新功能
- fix：修复bug
- docs：文档更新
- refactor：重构
- chore：构建/工具变更

详见 [.gitmessage](./.gitmessage)

---

## 注意事项

1. `client/` 目录包含个人敏感信息，不会被提交到Git
2. 请勿将个人经历文件提交到公开仓库
3. 所有外部信息必须通过工具查询，禁止编造

---

## 许可证

MIT

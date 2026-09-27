## Github Profile

![](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg) 

这是一个特殊的项目仓库， [README.md](README.md) 会直接展现在个人的 [Github Profile](https://github.com/lyy289065406) 。

为了可以实时刷新 Github 的工作状态到 [Github Profile](https://github.com/lyy289065406) ，利用了 [GraphQL](https://developer.github.com/v4/) 接口提取 Github 的动作进行统计分析，并通过 [Github Actions](.github/workflows/autorun.yml) 把统计数据定时更新到 [README.md](README.md) 。

目前会动态刷新的数据如下：


### 状态卡片

主要利用 [github-readme-stats](https://github.com/anuraghazra/github-readme-stats) 实现，只需定制 HTML 代码即可，详见官方教程。


### 时间分配

每个 repo 通过设置 Topic 标签标记其属于 `Programming`、 `Learning`、 `Writing` 或 `Playing` 中的一种， 通过 [GraphQL](https://developer.github.com/v4/) 接口提取每种 repo 投入的 commit 数量多寡，把统计结果换算为时间分配情况。


### 最近动态

通过 GraphQL 的 `viewer.repositories` 查询个人拥有、直接协作和通过组织成员身份可访问的仓库（`OWNER`、`COLLABORATOR`、`ORGANIZATION_MEMBER`），逐页读取并按 `pushedAt` 降序排列。跳过 Fork、空仓库及配置排除项，展示数量由 `app.activity_num` 决定。

组织 Owner 不需要逐个添加为仓库协作者。此列表展示仓库最近推送动态，不等同于本人的贡献记录；不再使用仅返回贡献仓库的 `repositoriesContributedTo`。查询范围仍受 Actions 中 `GRAPHQL_TOKEN` 的仓库访问权限及组织 SSO 授权限制。


### 最近文章

直接读取 [exp-blog.com](https://exp-blog.com) 的 [sitemap](https://exp-blog.com/sitemap.xml) 或 [rss](https://exp-blog.com/rss.xml) 提取最近发表的 TOP3 文章列表。

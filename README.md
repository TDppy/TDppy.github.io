# 项目介绍
每年只需要花几块钱买域名，在公网上建立一个漂亮的个人博客站点？
是的，通过Hexo + Github page就可以实现！
- Hexo是一个简单、高效的Node.js博客框架，有活跃的用户社区，海量的博客主题，可以快速生成静态博客站点。
- Github page提供了免费高效的网页托管功能，可以将Hexo项目托管到Github page上，通过**用户名.github.io**的方式进行访问。
- 在该项目后台设置配置Github action工作流，当有任何博客更新时，会自动同步部署到公网，实现持续集成（CI)/持续部署(CD)。
- 通过源码分支(main)和网站分支(gh-pages)的分离，可以实现开发和发布互不干扰。

# Quick Start
**首先需要安装node.js和git**
  不再赘述
  
**通过npm安装Hexo**

``` bash
$ npm install hexo-cli -g
```

Install with [brew](https://brew.sh/) on macOS and Linux:

```bash
$ brew install hexo
```

**克隆项目**
注意，主分支是源码分支，其中包含了hexo的项目配置、包依赖，还有所有.md格式的博客。
``` bash
git clone https://github.com/TDppy/TDppy.github.io.git
git checkout main
```

**启动并运行**
``` bash
hexo clean && hexo generate && hexo 
```
控制台输出网站开始运行时，在浏览器中打开即可。
**Hexo is running at http://localhost:4000/ . Press Ctrl+C to stop**

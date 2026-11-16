# 📚 BOOK-LIST

个人电子书仓库，用来归档和检索收藏的书籍。

## 目录结构

```
BOOK-LIST/
├── books/                 # 书籍文件（PDF / EPUB / MOBI / TXT）
│   └── <分类>/            # 可选：按分类建子目录
├── scripts/
│   └── build_index.py     # 扫描 books/ 自动生成下方书籍清单
└── README.md
```

## 书籍清单

<!-- BOOKLIST:START -->
| # | 书名 | 作者 | 分类 | 格式 | 大小 | 文件 |
| :-: | :--- | :--- | :--- | :--: | ---: | :--- |
| — | *暂无书籍，把文件放进 `books/` 后运行 `python3 scripts/build_index.py`* | | | | | |
<!-- BOOKLIST:END -->

## 添加书籍

1. 把文件放进 `books/`（可按分类建子目录，如 `books/技术/`）
2. 文件名建议用 `书名 - 作者.epub`，生成的清单会自动拆分书名和作者
3. 运行 `python3 scripts/build_index.py` 刷新上面的清单，然后提交：

```bash
git add .
git commit -m "add: 《书名》"
git push
```

## 说明

- **单文件限制**：GitHub 单文件上限 100 MB，超过会被拒收；整个仓库建议控制在 1 GB 以内。
- **大文件**：若书籍普遍较大，可改用 Git LFS 管理（`git lfs track "books/**"`）。
- **版权**：请仅存放自己有权使用或分发的书籍；本仓库为公开仓库，任何人可下载。

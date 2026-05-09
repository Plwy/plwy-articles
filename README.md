# plwy-articles

这是文章仓库，网页仓库会直接读取这里的内容。

## 目录约定

- `articles/<分类>/<文章>.md`
- `scripts/build_indexes.py`
- `posts.json`
- `categories.json`

## 日常写文章

默认只需要做一件事：

1. 把 Markdown 放到对应分类目录里

例如：

```text
articles/llm/LLM_note.md
articles/cpp/cpp_issue.md
```

然后运行：

```bash
python scripts/build_indexes.py
```

它会自动生成：

- `posts.json`
- `categories.json`

## 可选文章元数据

如果某篇文章需要“精品文章”标记或标签，不改 Markdown 也可以。

只要在文章旁边放一个同名 sidecar 文件：

```text
articles/llm/LLM_note.md
articles/llm/LLM_note.meta.json
```

示例：

```json
{
  "featured": true,
  "tags": ["LLM", "Transformer", "RAG"]
}
```

支持字段：

- `featured`: `true` 时会进入首页“精品文章”
- `tags`: 标签数组
- `title`: 可选标题覆盖
- `excerpt`: 可选摘要覆盖

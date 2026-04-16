## pytest

```
pip install pytest
```





- **测试文件**：必须以 `test_` 开头或 `_test.py` 结尾。

- **测试函数/方法**：必须以 `test_` 开头。

- **断言**：直接用 `assert`。

  判断是否得到预期结果

- **fixture**：用 `@pytest.fixture` 管理资源。

  用于准备测试环境（如数据库连接、临时文件等）

- **参数化**：

  用 `@pytest.mark.parametrize` 测试多组数据。

- **跳过测试和预期失败**

  - **跳过测试**：`@pytest.mark.skip`
  - **预期失败**：`@pytest.mark.xfail`

### 例子

`test_001.py`

```python
from funcs.algo import add, subtract

def test_add():
    print("Testing add function")
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
    assert add(100, 200) == 300
    assert add(-5, -5) == -10
    assert add(1.5, 2.5) == 4.0
    assert add(1, -1) == 0
    assert add(10, 20) == 30

def test_subtract():
    print("Testing subtract function")
    assert subtract(5, 3) == 2
    assert subtract(0, 0) == 0
    assert subtract(10, 5) == 5
    assert subtract(-1, -1) == 0
    assert subtract(100, 200) == -100
    assert subtract(2.5, 1.5) == 1.0
    assert subtract(1, -1) == 2
    assert subtract(20, 10) == 10
```

**执行：**

```bash
pytest test_001.py
pytest test_001.py -v #详细输出
```



### Fixture

使用 @pytest.fixture() 装饰器定义一个 Fixture 函数，并在测试函数中通过参数传递使用该 Fixture。例如：

```python
# test_db.py

import pytest

@pytest.fixture
def sample_data():
    return [1, 2, 3, 4]

def test_sum(sample_data):
    assert sum(sample_data) == 10

def test_max(sample_data):
    assert max(sample_data) == 4
```



### 多组数据测试`@pytest.mark.parametrize()`

用 `@pytest.mark.parametrize` 测试多组输入

```python
@pytest.mark.parametrize("test_input", [
    {"simple": "value"},
    [1, 2, 3],
    {"nested": {"key": "value"}},
    ["mixed", 1, True, None],
    {"unicode": "🌍"}
])
def test_various_input_types(test_input):
    """Test compression and decompression with various input types"""
    compressed = JsonCompressor.compress_json(test_input)
    decompressed = JsonCompressor.decompress_json(compressed)
    assert test_input == decompressed
```



###  **跳过测试和预期失败**

```python
@pytest.mark.skip(reason="暂时跳过此测试")
def test_skip_example():
    assert False

@pytest.mark.xfail
def test_expected_failure():
    assert 1 == 2
```


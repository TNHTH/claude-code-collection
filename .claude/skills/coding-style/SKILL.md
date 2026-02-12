---
name: coding-style
description: |
  编码规范参考。触发词：编码规范、代码风格、PEP8、C++规范、命名规范、代码检查。
  Coding style guidelines for Python, C/C++, and general best practices. Loaded on demand.
version: 1.0
author: Claude
---

> **Skill名称**: coding-style
> **版本**: v1.0
> **创建时间**: 2026-02-10 17:57:00
> **适用场景**: 编写/审查Python、C/C++代码时按需加载

## Skill描述

编码规范参考文档，包含Python、C/C++和通用编码原则。按需加载，不随每次对话自动加载。

**核心能力**:
- Python编码规范（PEP 8、类型提示、dataclass、Context Manager）
- C/C++编码规范（const/constexpr、智能指针、RAII、enum class）
- 通用原则（不可变性优先、纯函数、显式错误处理、命名清晰）
- 禁止模式与检查清单

## 使用方法

当用户编写或审查代码时，按需加载本Skill。

---

## 核心原则

### 1. 不可变性优先 (Immutability First)

```python
# ✅ 好: 使用tuple（不可变）
coordinates = (1, 2, 3)

# ✅ 好: 返回新对象而非修改原对象
new_users = users + [new_user]
new_dict = {**old_dict, "key": "value"}

# ❌ 差: 修改原对象
users.append(new_user)
```

### 2. 纯函数优先 (Pure Functions First)

```python
# ✅ 好: 纯函数（相同输入→相同输出，无副作用）
def add_user(users: list[User], user: User) -> list[User]:
    return users + [user]

# ❌ 差: 有副作用（修改输入参数）
def add_user(users: list[User], user: User) -> None:
    users.append(user)
```

### 3. 显式错误处理 (Explicit Error Handling)

```python
# ✅ 好: 显式处理，具体异常
def fetch_data(url: str) -> dict:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.Timeout:
        logger.error(f"Timeout fetching {url}")
        raise
    except requests.HTTPError as e:
        logger.error(f"HTTP {e.response.status_code} for {url}")
        raise

# ❌ 差: 裸except，吞噬错误
def fetch_data(url: str) -> dict:
    try:
        return requests.get(url).json()
    except:
        return None
```

### 4. 类型安全 + 命名清晰

```python
# ✅ 好
def process_users(users: list[User]) -> dict[str, int]:
    return {u.name: u.age for u in users}

user_ids = [1, 2, 3]
fetch_user_data()

# ❌ 差
def process_users(users):
    return {u.name: u.age for u in users}

data = [1, 2, 3]
process()
```

---

## Python特定规范

### PEP 8命名
- 函数: `snake_case`
- 类: `PascalCase`
- 常量: `UPPER_SNAKE_CASE`
- 缩进: 4空格

### 推荐模式
- 简单列表推导 > 循环（复杂逻辑用循环）
- `with`语句管理资源（文件、锁）
- `@dataclass`定义数据结构（Python 3.7+）

```python
# dataclass示例
from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
    email: str
```

---

## C/C++特定规范

### 命名约定
- 函数: `snake_case`
- 类/结构体: `PascalCase`
- 常量/宏: `UPPER_SNAKE_CASE`
- 成员变量: `m_snake_case` 或 `trailing_underscore_`

### 核心规范（C++11+）
- `const`/`constexpr` 确保不可变
- `std::unique_ptr`/`std::shared_ptr` 替代裸指针
- RAII管理资源（`std::lock_guard`、`std::ifstream`）
- `enum class` 替代 `enum`
- `nullptr` 替代 `NULL`
- 范围for循环 + `auto`（适度使用）

```cpp
// ✅ 智能指针
auto user = std::make_unique<User>();

// ✅ RAII
{
    std::lock_guard<std::mutex> lock(mutex);
    // 互斥锁在作用域结束时自动释放
}

// ✅ enum class
enum class Color { RED, GREEN, BLUE };
```

### C语言规范
- `typedef`定义类型别名
- `malloc`/`free`配对
- `static`限制全局变量作用域
- 检查指针是否为`NULL`

---

## 通用规范（跨语言）

1. **魔法数字 → 命名常量**: `SECONDS_PER_DAY = 86400`
2. **注释掉的代码 → 删除**: 用Git管理历史
3. **嵌套过深 → 提前返回**: 嵌套不超过3层

---

## 禁止模式

1. 吞噬异常（裸except）
2. 全局变量（除非必要）
3. 循环中修改正在迭代的列表
4. `type(var) == Type`（用`isinstance()`）
5. 可变默认参数（`def func(items=[])`）

---

## 检查清单

### Python
- [ ] 函数有类型提示
- [ ] 异常处理具体（非裸except）
- [ ] 遵循PEP 8命名
- [ ] 使用with语句、dataclass

### C++
- [ ] const/constexpr、智能指针
- [ ] nullptr、enum class
- [ ] RAII管理资源

### 通用
- [ ] 无魔法数字
- [ ] 命名清晰
- [ ] 嵌套≤3层

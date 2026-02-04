---
name: error-handling-protocol
description: 统一错误处理协议
---

# 统一错误处理协议

> **创建时间**: 2026-02-01 14:30:00
> **适用范围**: 所有Agent开发（Backend、Frontend、DevOps等）
> **目的**: 提供一致的错误处理标准和模板

---

## 核心原则

```
1. 错误分层：区分可恢复错误和不可恢复错误
2. 用户友好：错误消息面向用户，不泄露技术细节
3. 日志详细：内部日志记录完整错误栈和上下文
4. 统一格式：所有错误响应使用相同的JSON结构
```

---

## 错误分类

### 1. 客户端错误 (4xx)

| 错误码 | 场景 | 示例 |
|--------|------|------|
| 400 Bad Request | 参数验证失败 | 缺少必填字段 |
| 401 Unauthorized | 未认证 | Token缺失或过期 |
| 403 Forbidden | 无权限 | 非管理员访问管理接口 |
| 404 Not Found | 资源不存在 | 用户ID不存在 |
| 409 Conflict | 资源冲突 | 用户名已存在 |
| 422 Unprocessable Entity | 业务逻辑错误 | 余额不足 |
| 429 Too Many Requests | 速率限制 | 超过API调用频率 |

### 2. 服务端错误 (5xx)

| 错误码 | 场景 | 示例 |
|--------|------|------|
| 500 Internal Server Error | 未预期的错误 | 数据库连接失败 |
| 502 Bad Gateway | 上游服务错误 | 第三方API超时 |
| 503 Service Unavailable | 服务不可用 | 数据库维护中 |

---

## 统一错误响应格式

### JSON结构

```typescript
interface ErrorResponse {
  success: false;
  error: {
    code: string;           // 错误代码（业务唯一标识）
    message: string;        // 用户友好的错误消息
    details?: string;       // 可选的详细信息
    field?: string;         // 验证错误的字段名
    timestamp: string;      // ISO 8601时间戳
    requestId?: string;     // 请求追踪ID（可选）
  };
}
```

### 示例

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": "Email format is invalid",
    "field": "email",
    "timestamp": "2026-02-01T14:30:00Z",
    "requestId": "req_abc123"
  }
}
```

---

## Backend错误处理模板

### 1. 参数验证错误

```typescript
// ❌ 错误示例
if (!email) {
  throw new Error('Email is required');
}

// ✅ 正确示例
if (!email) {
  return res.status(400).json({
    success: false,
    error: {
      code: 'VALIDATION_ERROR',
      message: 'Missing required field',
      field: 'email',
      timestamp: new Date().toISOString()
    }
  });
}
```

### 2. 资源不存在错误

```typescript
const user = await db.users.findById(id);

if (!user) {
  return res.status(404).json({
    success: false,
    error: {
      code: 'RESOURCE_NOT_FOUND',
      message: 'User not found',
      details: `No user with ID ${id}`,
      timestamp: new Date().toISOString()
    }
  });
}
```

### 3. 业务逻辑错误

```typescript
if (user.balance < amount) {
  return res.status(422).json({
    success: false,
    error: {
      code: 'INSUFFICIENT_BALANCE',
      message: 'Insufficient account balance',
      details: `Required: ${amount}, Available: ${user.balance}`,
      timestamp: new Date().toISOString()
    }
  });
}
```

### 4. 未预期错误（全局捕获）

```typescript
// Express全局错误处理中间件
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  // 记录详细错误日志
  console.error('Unhandled error:', {
    error: err.message,
    stack: err.stack,
    url: req.url,
    method: req.method,
    timestamp: new Date().toISOString()
  });

  // 返回用户友好的错误消息
  res.status(500).json({
    success: false,
    error: {
      code: 'INTERNAL_SERVER_ERROR',
      message: 'An unexpected error occurred',
      timestamp: new Date().toISOString(),
      requestId: req.id // 如果有请求ID中间件
    }
  });
});
```

### 5. Try-Catch包装

```typescript
async function createUser(req: Request, res: Response) {
  try {
    // 验证输入
    const { username, email, password } = req.body;

    if (!username || !email || !password) {
      return res.status(400).json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Missing required fields',
          timestamp: new Date().toISOString()
        }
      });
    }

    // 业务逻辑
    const user = await userService.create({ username, email, password });

    // 成功响应
    return res.status(201).json({
      success: true,
      data: user
    });

  } catch (error) {
    // 区分已知错误和未知错误
    if (error instanceof ValidationError) {
      return res.status(400).json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: error.message,
          field: error.field,
          timestamp: new Date().toISOString()
        }
      });
    }

    if (error instanceof ConflictError) {
      return res.status(409).json({
        success: false,
        error: {
          code: 'RESOURCE_CONFLICT',
          message: error.message,
          timestamp: new Date().toISOString()
        }
      });
    }

    // 未知错误：记录详细日志，返回通用消息
    console.error('Create user error:', error);
    return res.status(500).json({
      success: false,
      error: {
        code: 'INTERNAL_SERVER_ERROR',
        message: 'Failed to create user',
        timestamp: new Date().toISOString()
      }
    });
  }
}
```

---

## Frontend错误处理模板

### 1. API调用错误处理

```typescript
async function fetchUsers(): Promise<User[]> {
  try {
    const response = await fetch('/api/users');

    // 检查HTTP状态码
    if (!response.ok) {
      const errorData = await response.json();
      throw new ApiError(
        errorData.error.code,
        errorData.error.message,
        response.status
      );
    }

    const data = await response.json();
    return data.data;

  } catch (error) {
    // 网络错误（无响应）
    if (error instanceof TypeError) {
      throw new NetworkError('Network connection failed');
    }

    // API错误（有响应）
    if (error instanceof ApiError) {
      throw error;
    }

    // 未知错误
    throw new Error('An unexpected error occurred');
  }
}
```

### 2. 自定义错误类

```typescript
// src/errors/ApiError.ts
export class ApiError extends Error {
  constructor(
    public code: string,
    message: string,
    public statusCode: number
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

// src/errors/NetworkError.ts
export class NetworkError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'NetworkError';
  }
}
```

### 3. React组件错误处理

```tsx
function UserList() {
  const [state, setState] = useState<'loading' | 'success' | 'error'>('loading');
  const [users, setUsers] = useState<User[]>([]);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    loadUsers();
  }, []);

  async function loadUsers() {
    try {
      setState('loading');
      setError(null);

      const data = await fetchUsers();
      setUsers(data);
      setState('success');

    } catch (err) {
      setState('error');

      // 区分错误类型，显示不同消息
      if (err instanceof NetworkError) {
        setError(new Error('Network connection failed. Please check your internet.'));
      } else if (err instanceof ApiError) {
        setError(new Error(err.message));
      } else {
        setError(new Error('An unexpected error occurred. Please try again.'));
      }
    }
  }

  // Loading状态
  if (state === 'loading') {
    return <UserListSkeleton />;
  }

  // Error状态
  if (state === 'error') {
    return (
      <ErrorMessage
        message={error?.message || 'Unknown error'}
        onRetry={loadUsers}
      />
    );
  }

  // Success状态
  return <div>{/* 渲染用户列表 */}</div>;
}
```

### 4. 错误边界（Error Boundary）

```tsx
// src/components/ErrorBoundary.tsx
import React, { Component, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    // 记录错误到监控服务
    console.error('React Error Boundary caught:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="error-boundary">
          <h2>Something went wrong</h2>
          <p>{this.state.error?.message}</p>
          <button onClick={() => window.location.reload()}>
            Reload Page
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
```

---

## 错误码规范

### 命名规则

```
格式: [CATEGORY]_[SPECIFIC_ERROR]
示例: VALIDATION_ERROR, AUTH_TOKEN_EXPIRED, DB_CONNECTION_FAILED
```

### 常用错误码

```typescript
// src/constants/errorCodes.ts
export const ErrorCodes = {
  // 验证错误
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  MISSING_FIELD: 'MISSING_FIELD',
  INVALID_FORMAT: 'INVALID_FORMAT',

  // 认证错误
  AUTH_REQUIRED: 'AUTH_REQUIRED',
  AUTH_TOKEN_EXPIRED: 'AUTH_TOKEN_EXPIRED',
  AUTH_INVALID_CREDENTIALS: 'AUTH_INVALID_CREDENTIALS',

  // 权限错误
  PERMISSION_DENIED: 'PERMISSION_DENIED',

  // 资源错误
  RESOURCE_NOT_FOUND: 'RESOURCE_NOT_FOUND',
  RESOURCE_CONFLICT: 'RESOURCE_CONFLICT',

  // 业务逻辑错误
  INSUFFICIENT_BALANCE: 'INSUFFICIENT_BALANCE',
  OPERATION_NOT_ALLOWED: 'OPERATION_NOT_ALLOWED',

  // 服务器错误
  INTERNAL_SERVER_ERROR: 'INTERNAL_SERVER_ERROR',
  DB_CONNECTION_FAILED: 'DB_CONNECTION_FAILED',
  EXTERNAL_SERVICE_ERROR: 'EXTERNAL_SERVICE_ERROR',
} as const;
```

---

## 日志记录规范

### 1. 错误日志结构

```typescript
interface ErrorLog {
  timestamp: string;
  level: 'error' | 'warn' | 'info';
  code: string;
  message: string;
  stack?: string;
  context: {
    userId?: string;
    requestId?: string;
    url?: string;
    method?: string;
    [key: string]: any;
  };
}
```

### 2. 日志记录示例

```typescript
function logError(error: Error, context: Record<string, any> = {}) {
  const errorLog: ErrorLog = {
    timestamp: new Date().toISOString(),
    level: 'error',
    code: (error as any).code || 'UNKNOWN_ERROR',
    message: error.message,
    stack: error.stack,
    context: {
      ...context,
      environment: process.env.NODE_ENV
    }
  };

  // 开发环境：输出到控制台
  if (process.env.NODE_ENV === 'development') {
    console.error(JSON.stringify(errorLog, null, 2));
  } else {
    // 生产环境：发送到日志服务（如Sentry、Datadog）
    // logService.send(errorLog);
    console.error(JSON.stringify(errorLog));
  }
}
```

---

## 最佳实践

### ✅ 推荐做法

1. **使用统一的错误响应格式**
   ```typescript
   return res.status(400).json({
     success: false,
     error: { code, message, timestamp }
   });
   ```

2. **区分用户消息和日志消息**
   ```typescript
   // 用户看到的
   message: 'User not found'

   // 日志记录的
   console.error('User lookup failed:', { userId, error })
   ```

3. **使用自定义错误类**
   ```typescript
   throw new ValidationError('Invalid email', 'email');
   ```

4. **Try-Catch包装所有异步操作**
   ```typescript
   try {
     await riskyOperation();
   } catch (error) {
     handleError(error);
   }
   ```

5. **前端显示用户友好的错误消息**
   ```tsx
   {error && <ErrorMessage message={error.message} onRetry={retry} />}
   ```

### ❌ 避免做法

1. **直接抛出原始错误**
   ```typescript
   // ❌ 错误
   throw error;

   // ✅ 正确
   throw new ApiError('USER_NOT_FOUND', 'User not found', 404);
   ```

2. **泄露敏感信息**
   ```typescript
   // ❌ 错误
   return res.json({ error: `Database error: ${dbError.message}` });

   // ✅ 正确
   console.error('DB error:', dbError);
   return res.json({ error: 'Database error occurred' });
   ```

3. **忽略错误**
   ```typescript
   // ❌ 错误
   try {
     await operation();
   } catch (error) {
     // 空catch块
   }

   // ✅ 正确
   try {
     await operation();
   } catch (error) {
     console.error('Operation failed:', error);
     handleError(error);
   }
   ```

4. **裸except/catch**
   ```typescript
   // ❌ 错误
   } catch (error) {
     return res.status(500).json({ error: 'Error' });
   }

   // ✅ 正确
   } catch (error) {
     if (error instanceof ValidationError) {
       return res.status(400).json({ error: error.message });
     }
     // ... 处理其他类型错误
   }
   ```

---

## 与其他协议的关系

- **参考**: `shared/communication-protocol.md` - Agent之间的错误传递
- **参考**: `shared/agent-work-principles.md` - 错误处理的工作原则
- **应用**: Backend Agent、Frontend Agent、DevOps Agent

---

## 示例：完整的错误处理流程

```typescript
// Backend: src/controllers/userController.ts
export class UserController {
  async createUser(req: Request, res: Response) {
    try {
      // 1. 验证输入
      const { username, email, password } = req.body;

      if (!username || !email || !password) {
        return res.status(400).json({
          success: false,
          error: {
            code: ErrorCodes.MISSING_FIELD,
            message: 'Missing required fields',
            timestamp: new Date().toISOString()
          }
        });
      }

      // 2. 业务逻辑
      const user = await this.userService.create({ username, email, password });

      // 3. 成功响应
      return res.status(201).json({
        success: true,
        data: user
      });

    } catch (error) {
      // 4. 错误分类处理
      if (error instanceof ValidationError) {
        return res.status(400).json({
          success: false,
          error: {
            code: ErrorCodes.VALIDATION_ERROR,
            message: error.message,
            field: error.field,
            timestamp: new Date().toISOString()
          }
        });
      }

      if (error instanceof ConflictError) {
        return res.status(409).json({
          success: false,
          error: {
            code: ErrorCodes.RESOURCE_CONFLICT,
            message: error.message,
            timestamp: new Date().toISOString()
          }
        });
      }

      // 5. 记录未知错误
      logError(error, {
        controller: 'UserController',
        method: 'createUser',
        body: req.body
      });

      // 6. 返回通用错误
      return res.status(500).json({
        success: false,
        error: {
          code: ErrorCodes.INTERNAL_SERVER_ERROR,
          message: 'Failed to create user',
          timestamp: new Date().toISOString()
        }
      });
    }
  }
}
```

```typescript
// Frontend: src/api/users.ts
export async function createUser(data: CreateUserDto): Promise<User> {
  try {
    const response = await fetch('/api/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new ApiError(
        errorData.error.code,
        errorData.error.message,
        response.status
      );
    }

    const result = await response.json();
    return result.data;

  } catch (error) {
    if (error instanceof TypeError) {
      throw new NetworkError('Network connection failed');
    }
    throw error;
  }
}
```

```tsx
// Frontend: src/components/CreateUserForm.tsx
function CreateUserForm() {
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(data: CreateUserDto) {
    try {
      setError(null);
      await createUser(data);
      // 成功处理
    } catch (err) {
      // 用户友好的错误消息
      if (err instanceof NetworkError) {
        setError('Network connection failed. Please check your internet.');
      } else if (err instanceof ApiError) {
        if (err.code === 'RESOURCE_CONFLICT') {
          setError('Username already exists. Please choose another.');
        } else {
          setError(err.message);
        }
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      {error && <ErrorMessage message={error} />}
      {/* 表单字段 */}
    </form>
  );
}
```

---

## 更新日志

- **2026-02-01**: 创建统一错误处理协议

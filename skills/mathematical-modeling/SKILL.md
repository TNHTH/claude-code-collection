---
name: mathematical-modeling
description: Quantitative decision support tools including weighted scoring, NPV calculation, and Monte Carlo simulations.
version: 1.0
author: Claude
---

> **名称**: mathematical-modeling
> **版本**: v2.5
> **类型**: Analysis & Decision Support
> **核心功能**: 提供加权评分、NPV计算等量化决策工具

## 核心工作流 (Workflow)

1. **定义问题 (Define)**: 使用苏格拉底诘法或第一性原理明确决策目标。
2. **选择模型 (Select)**:
   - 多选项比较 → `weighted_score`
   - 长期财务决策 → `npv_calculator`
3. **计算求解 (Calculate)**: 运行脚本获取量化结果。
4. **分析验证 (Analyze)**: 使用敏感性分析和墨菲定律验证结论稳健性。

## 可用脚本工具

### 1. 加权评分 (Weighted Score)
- **脚本**: `scripts/weighted_score.py`
- **用途**: 选Offer、选学校、多维度评估。
- **输入**: 权重字典 + 选项得分字典。

### 2. 净现值计算 (NPV)
- **脚本**: `scripts/npv_calculator.py`
- **用途**: 买房vs租房、长期投资回报分析。
- **输入**: 折现率 + 现金流列表（负数为支出，正数为收入）。

### 3. 蒙特卡洛模拟 (Risk Assessment)
- **脚本**: `scripts/monte_carlo.py`
- **用途**: 项目工期预估、成本风险分析 (PERT)。
- **输入**: 乐观值、名义值、悲观值 (Optimistic, Nominal, Pessimistic)。

### 4. 贝叶斯推断 (Bayesian Inference)
- **脚本**: `scripts/bayes_updater.py`
- **用途**: 解释体检报告、更新信念、招聘筛选。
- **输入**: 先验概率、敏感度、特异度。

## 详细指南

> 📚 完整的方法论、生活场景速查表和详细案例请参阅:
> **[Mathematical Modeling Method Guide](references/method-guide.md)**

## 最佳实践

- **结合思维工具**: 计算前先用 **DR-019** (思维工具箱) 明确需求。
- **验证假设**: 对关键参数（如折现率、权重）做敏感性测试。
- **保持简单**: 遵循奥卡姆剃刀，不要引入不必要的复杂变量。

## Common Errors & Solutions
1. **Invalid input data**: Non-numeric values provided for calculations.
   - *Solution*: Ensure all input lists (weights, scores, cash flows) contain only numbers.
2. **Dimension mismatch**: Weights and scores lists have different lengths.
   - *Solution*: Verify that every criterion in the weights dictionary has a corresponding score in the options.
3. **Zero division**: Risk parameters set to zero in simulations.
   - *Solution*: Ensure optimistic/pessimistic range values are non-zero where used as denominators.

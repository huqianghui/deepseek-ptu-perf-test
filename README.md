# Azure AI DeepSeek Performance Benchmark Test

这是一个用于测试Azure AI DeepSeek模型性能的benchmark工具，支持两种调用方式：
- Azure AI Inference SDK
- 直接HTTP请求

## 功能特性

- 支持顺序和并行请求测试
- 提供详细的性能指标（延迟、吞吐量、成功率等）
- 支持自定义测试问题数量和并发线程数
- 生成详细的测试报告和汇总结果
- 支持两种不同的调用后端（SDK vs HTTP）

## 安装依赖

```bash
# 安装项目依赖
uv sync
# 或者使用pip
pip install -r requirements.txt
```

## 使用方法

### 基本用法

```bash
# 使用SDK后端，测试10个问题
python main.py --backend sdk --num-questions 10

# 使用HTTP后端，测试20个问题
python main.py --backend http --num-questions 20

# 并行测试，使用5个线程
python main.py --backend sdk --num-questions 20 --parallel 5

# 指定结果输出文件
python main.py --backend sdk --num-questions 10 --result-file my_results.jsonl
```

### 参数说明

- `--backend`: 选择后端类型
  - `sdk`: 使用Azure AI Inference SDK（默认）
  - `http`: 使用直接HTTP请求
- `--num-questions`: 测试问题数量（1-20，默认10）
- `--parallel`: 并行线程数（默认1，顺序执行）
- `--result-file`: 结果输出文件（默认benchmark_results.jsonl）

### 输出文件

1. **详细结果文件**: `benchmark_output_{backend}_{timestamp}.txt`
   - 包含每个请求的详细信息
   - 响应内容、token使用量、错误信息等

2. **汇总结果文件**: `benchmark_results.jsonl`（或自定义文件名）
   - JSON格式的汇总数据
   - 便于后续分析和比较

## 性能指标

脚本会输出以下关键指标：
- **总延迟**: 完成所有请求的总时间
- **成功率**: 成功请求的百分比
- **平均延迟**: 每个请求的平均响应时间
- **吞吐量**: 每秒处理的请求数
- **Token统计**: 总token数和平均token数

## 示例输出

```
=== Azure AI Benchmark Test ===
Backend: sdk
Model: DeepSeek-R1-2
Number of questions: 10
Parallel threads: 1
Endpoint: https://ai-qiah-1368.services.ai.azure.com/models
==================================================
Running sequential benchmark...
Processing question 1/10: What are the main attractions in Paris?...
...

==================================================
=== Benchmark Results ===
Total Latency: 15.234s
Total Requests: 10
Successful Requests: 10
Success Rate: 100.00%
Average Latency per Request: 1.523s
Requests per Second: 6.564
Total Tokens: 3245
Average Tokens per Request: 324.50
```

## 配置

在使用前，请确保在`main.py`中正确配置：
- `endpoint`: Azure AI服务端点
- `model_name`: 模型名称
- `key`: API密钥

## 注意事项

- 确保Azure AI服务配置正确且有足够的配额
- 并行测试时注意不要超过服务的并发限制
- 测试结果可能会受到网络延迟和服务负载的影响
- 建议多次运行以获得更稳定的性能数据
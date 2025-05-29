import argparse
import json
import time
import concurrent.futures
import threading
from typing import List, Dict, Any
import os
import dotenv

import requests

# Load environment variables from .env file
dotenv.load_dotenv()

# Azure AI配置
endpoint = os.getenv("AZURE_ENDPOINT")
model_name = os.getenv("AZURE_MODEL_NAME")
api_version = os.getenv("AZURE_API_VERSION")
key = os.getenv("AZURE_API_KEY")

system_prompt = "You are a helpful assistant. Please provide clear and concise answers."

# 测试问题列表 - 从文件加载
def load_test_questions():
    """从JSON文件加载测试问题"""
    try:
        with open('test_questions_1000.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # 如果文件不存在，返回默认的小量测试问题
        return [
            "What are the main attractions in Paris?",
            "Explain the concept of machine learning in simple terms.",
            "What are the benefits of cloud computing?",
            "How does photosynthesis work?",
            "What are the key principles of effective communication?",
            "Describe the process of software development lifecycle.",
            "What are the advantages of renewable energy?",
            "How do neural networks function?",
            "What are the main components of a computer system?",
            "Explain the importance of data security.",
            "What are the different types of databases?",
            "How does artificial intelligence impact society?",
            "What are the principles of good user interface design?",
            "Describe the concept of microservices architecture.",
            "What are the key factors in project management?",
            "How does encryption protect data?",
            "What are the benefits of agile methodology?",
            "Explain the role of APIs in modern software development.",
            "What are the challenges of distributed systems?",
            "How does version control help in software development?"
        ]

# 加载测试问题
test_questions = load_test_questions()
print(f"Loaded {len(test_questions)} test questions.")

class AzureAIBenchmark:
    def __init__(self):
        """Initialize benchmark for HTTP-only requests (SDK doesn't support PTU endpoints)"""
        pass
    
    def test_connection(self) -> bool:
        """测试连接和认证"""
        try:
            url = f"{endpoint}/openai/deployments/{model_name}/chat/completions?api-version={api_version}"
            headers = {
                "Content-Type": "application/json",
                "api-key": key
            }
            payload = {
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 10
            }
            response = requests.post(url, headers=headers, json=payload)
            return response.status_code == 200
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False
    


    
    def single_request_http(self, question: str) -> Dict[str, Any]:
        """使用HTTP直接请求进行单个请求"""
        deployment_endpoint = f"{endpoint}/openai/deployments/{model_name}/chat/completions?api-version={api_version}"
        
        headers = {
            "Content-Type": "application/json",
            "api-key": key
        }
        
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            "max_tokens": 2048,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(deployment_endpoint, headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "content": result['choices'][0]['message']['content'],
                    "usage": result.get('usage', {}).get('total_tokens', None)
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text[:200]}",
                    "content": None,
                    "usage": None
                }
                    
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "content": None,
                "usage": None
            }
    
    def run_single_request(self, question: str) -> Dict[str, Any]:
        """运行单个请求（仅支持HTTP）"""
        return self.single_request_http(question)

def run_benchmark_sequential(benchmark: AzureAIBenchmark, questions: List[str]) -> tuple:
    """顺序执行benchmark测试"""
    results = []
    successful_requests = 0
    total_tokens = 0
    
    start_time = time.perf_counter()
    
    for i, question in enumerate(questions):
        print(f"Processing question {i+1}/{len(questions)}: {question[:50]}...")
        result = benchmark.run_single_request(question)
        results.append(result)
        
        if result["success"]:
            successful_requests += 1
            if result["usage"]:
                total_tokens += result["usage"]
    
    end_time = time.perf_counter()
    latency = end_time - start_time
    
    return results, latency, successful_requests, total_tokens

def run_benchmark_parallel(benchmark: AzureAIBenchmark, questions: List[str], num_threads: int) -> tuple:
    """并行执行benchmark测试"""
    results = [None] * len(questions)
    successful_requests = 0
    total_tokens = 0
    
    def process_question(index, question):
        nonlocal successful_requests, total_tokens
        result = benchmark.run_single_request(question)
        results[index] = result
        
        if result["success"]:
            with threading.Lock():
                nonlocal successful_requests, total_tokens
                successful_requests += 1
                if result["usage"]:
                    total_tokens += result["usage"]
    
    start_time = time.perf_counter()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for i, question in enumerate(questions):
            future = executor.submit(process_question, i, question)
            futures.append(future)
        
        # 等待所有任务完成
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            print(f"Completed {i+1}/{len(questions)} requests")
    
    end_time = time.perf_counter()
    latency = end_time - start_time
    
    return results, latency, successful_requests, total_tokens

def save_results(args, latency: float, num_requests: int, successful_requests: int, total_tokens: int, results: List[Dict]):
    """保存测试结果"""
    # 保存详细结果到文本文件
    output_file = f"benchmark_output_{time.strftime('%Y%m%d_%H%M%S')}.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"=== Azure AI Benchmark Results ===\n")
        f.write(f"Model: {model_name}\n")
        f.write(f"Total Requests: {num_requests}\n")
        f.write(f"Successful Requests: {successful_requests}\n")
        f.write(f"Total Latency: {latency:.3f}s\n")
        f.write(f"Average Latency per Request: {latency/num_requests:.3f}s\n")
        f.write(f"Requests per Second: {num_requests/latency:.3f}\n")
        f.write(f"Total Tokens: {total_tokens}\n")
        f.write(f"Parallel Threads: {args.parallel}\n\n")
        
        for i, result in enumerate(results):
            f.write(f"--- Request {i+1} ---\n")
            if result["success"]:
                f.write(f"Content: {result['content'][:200]}...\n")
                f.write(f"Tokens: {result['usage']}\n")
            else:
                f.write(f"Error: {result['error']}\n")
            f.write("\n")
    
    print(f"Detailed results saved to: {output_file}")
    
    # 保存汇总结果到JSON文件
    if args.result_file:
        summary = {
            "task": "azure_ai_benchmark",
            "model": model_name,
            "latency": round(latency, 3),
            "num_requests": num_requests,
            "successful_requests": successful_requests,
            "success_rate": round(successful_requests / num_requests * 100, 2),
            "avg_latency_per_request": round(latency / num_requests, 3),
            "requests_per_second": round(num_requests / latency, 3),
            "total_tokens": total_tokens,
            "avg_tokens_per_request": round(total_tokens / successful_requests, 2) if successful_requests > 0 else 0,
            "other": {
                "parallel": args.parallel,
                "endpoint": endpoint
            }
        }
        
        with open(args.result_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(summary, ensure_ascii=False) + "\n")
        
        print(f"Summary results appended to: {args.result_file}")

def main(args):
    """主函数"""
    # 获取测试问题
    questions = test_questions[:args.num_questions]
    
    print(f"=== Azure AI Benchmark Test ===")
    print(f"Model: {model_name}")
    print(f"Number of questions: {len(questions)}")
    print(f"Parallel threads: {args.parallel}")
    print(f"Endpoint: {endpoint}")
    print("=" * 50)
    
    # 初始化benchmark
    benchmark = AzureAIBenchmark()
    
    # 测试连接
    print("Testing connection...")
    connection_ok = benchmark.test_connection()
    if connection_ok:
        print("✓ Connection test passed!")
    else:
        print("✗ Connection test failed!")
        return
    
    print("=" * 50)
    
    # 运行测试
    if args.parallel == 1:
        print("Running sequential benchmark...")
        results, latency, successful_requests, total_tokens = run_benchmark_sequential(benchmark, questions)
    else:
        print(f"Running parallel benchmark with {args.parallel} threads...")
        results, latency, successful_requests, total_tokens = run_benchmark_parallel(benchmark, questions, args.parallel)
    
    # 打印结果
    print("\n" + "=" * 50)
    print("=== Benchmark Results ===")
    print(f"Total Latency: {latency:.3f}s")
    print(f"Total Requests: {len(questions)}")
    print(f"Successful Requests: {successful_requests}")
    print(f"Success Rate: {successful_requests/len(questions)*100:.2f}%")
    print(f"Average Latency per Request: {latency/len(questions):.3f}s")
    print(f"Requests per Second: {len(questions)/latency:.3f}")
    print(f"Total Tokens: {total_tokens}")
    if successful_requests > 0:
        print(f"Average Tokens per Request: {total_tokens/successful_requests:.2f}")
    
    # 保存结果
    save_results(args, latency, len(questions), successful_requests, total_tokens, results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Azure AI Benchmark Test")
    parser.add_argument("--num-questions", type=int, default=2000,
                       help="Number of questions to test (max 2000)")
    parser.add_argument("--parallel", type=int, default=1000,
                       help="Number of parallel threads for requests")
    parser.add_argument("--result-file", type=str, default="benchmark_results.jsonl",
                       help="File to append benchmark results")
    
    args = parser.parse_args()
    
    # 验证参数
    if args.num_questions > len(test_questions):
        args.num_questions = len(test_questions)
        print(f"Warning: num_questions limited to available questions ({len(test_questions)})")
    
    main(args)
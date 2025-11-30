import json
from typing import List, Dict
import time
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline import RAGPipeline

class Evaluator:
    def __init__(self, pipeline: RAGPipeline):
        self.pipeline = pipeline
        self.results = []
        self.start_time = None
        self.end_time = None
    
    def load_benchmark(self, path: str = "evaluation/benchmark_questions.json"):
        """Load benchmark questions"""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data['questions']
    
    def evaluate(self):
        """Run evaluation"""
        questions = self.load_benchmark()
        
        print("\n" + "=" * 70)
        print("STARTING EVALUATION - MULTI-MODAL RAG SYSTEM")
        print("=" * 70)
        print(f"Total questions: {len(questions)}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70 + "\n")
        
        self.start_time = time.time()
        
        for q in questions:
            print(f"\n{'='*70}")
            print(f"[Question {q['id']}/{len(questions)}]")
            print(f"Type: {q['type'].upper()} | Category: {q['category']}")
            print(f"Q: {q['question']}")
            print(f"Expected: {q['expected_answer']}")
            print("-" * 70)
            
            start_time = time.time()
            
            try:
                result = self.pipeline.query(q['question'])
                latency = time.time() - start_time
                
                # Extract key info
                answer_preview = result['answer'][:300] + "..." if len(result['answer']) > 300 else result['answer']
                
                self.results.append({
                    'id': q['id'],
                    'question': q['question'],
                    'type': q['type'],
                    'category': q['category'],
                    'expected_answer': q.get('expected_answer', 'N/A'),
                    'answer': result['answer'],
                    'answer_preview': answer_preview,
                    'sources': result['sources'],
                    'num_sources': len(result['sources']),
                    'latency': latency,
                    'success': True
                })
                
                print(f"✓ COMPLETED in {latency:.2f}s")
                print(f"A: {answer_preview}")
                print(f"Sources: {len(result['sources'])} chunks retrieved")
                
            except Exception as e:
                latency = time.time() - start_time
                print(f"✗ FAILED: {str(e)}")
                self.results.append({
                    'id': q['id'],
                    'question': q['question'],
                    'type': q['type'],
                    'category': q['category'],
                    'expected_answer': q.get('expected_answer', 'N/A'),
                    'success': False,
                    'error': str(e),
                    'latency': latency
                })
        
        self.end_time = time.time()
        self.print_summary()
        self.save_results()
    
    def print_summary(self):
        """Print evaluation summary"""
        successful = [r for r in self.results if r.get('success')]
        failed = [r for r in self.results if not r.get('success')]
        
        if successful:
            avg_latency = sum(r['latency'] for r in successful) / len(successful)
            min_latency = min(r['latency'] for r in successful)
            max_latency = max(r['latency'] for r in successful)
            avg_sources = sum(r.get('num_sources', 0) for r in successful) / len(successful)
        else:
            avg_latency = min_latency = max_latency = avg_sources = 0
        
        total_time = self.end_time - self.start_time if self.end_time else 0
        
        # Group by type and category
        by_type = {}
        by_category = {}
        
        for r in successful:
            # By type
            if r['type'] not in by_type:
                by_type[r['type']] = {'total': 0, 'success': 0}
            by_type[r['type']]['total'] += 1
            by_type[r['type']]['success'] += 1
            
            # By category
            if r['category'] not in by_category:
                by_category[r['category']] = {'total': 0, 'success': 0}
            by_category[r['category']]['total'] += 1
            by_category[r['category']]['success'] += 1
        
        for r in failed:
            if r['type'] not in by_type:
                by_type[r['type']] = {'total': 0, 'success': 0}
            by_type[r['type']]['total'] += 1
            
            if r['category'] not in by_category:
                by_category[r['category']] = {'total': 0, 'success': 0}
            by_category[r['category']]['total'] += 1
        
        print("\n" + "=" * 70)
        print("EVALUATION SUMMARY REPORT")
        print("=" * 70)
        
        print(f"\n📊 OVERALL PERFORMANCE:")
        print(f"  • Total questions: {len(self.results)}")
        print(f"  • Successful: {len(successful)} ✓")
        print(f"  • Failed: {len(failed)} ✗")
        print(f"  • Success Rate: {len(successful)/len(self.results)*100:.1f}%")
        
        print(f"\n⏱️  LATENCY METRICS:")
        print(f"  • Average: {avg_latency:.2f}s")
        print(f"  • Minimum: {min_latency:.2f}s")
        print(f"  • Maximum: {max_latency:.2f}s")
        print(f"  • Total evaluation time: {total_time:.1f}s ({total_time/60:.1f} minutes)")
        
        print(f"\n📚 RETRIEVAL METRICS:")
        print(f"  • Avg sources per query: {avg_sources:.1f}")
        
        print(f"\n📝 PERFORMANCE BY QUESTION TYPE:")
        for qtype, stats in sorted(by_type.items()):
            success_rate = stats['success'] / stats['total'] * 100 if stats['total'] > 0 else 0
            bar = "█" * int(success_rate / 5)
            print(f"  • {qtype.capitalize():15s}: {stats['success']:2d}/{stats['total']:2d} ({success_rate:5.1f}%) {bar}")
        
        print(f"\n🏷️  PERFORMANCE BY CATEGORY:")
        for cat, stats in sorted(by_category.items()):
            success_rate = stats['success'] / stats['total'] * 100 if stats['total'] > 0 else 0
            bar = "█" * int(success_rate / 5)
            print(f"  • {cat:25s}: {stats['success']:2d}/{stats['total']:2d} ({success_rate:5.1f}%) {bar}")
        
        if failed:
            print(f"\n❌ FAILED QUESTIONS:")
            for r in failed:
                print(f"  • Q{r['id']:2d}: {r['question'][:60]}...")
                print(f"         Error: {r.get('error', 'Unknown error')}")
        
        print("\n" + "=" * 70)
    
    def save_results(self):
        """Save evaluation results"""
        os.makedirs('evaluation', exist_ok=True)
        
        # Save detailed results
        with open('evaluation/results.json', 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'total_questions': len(self.results),
                'successful': len([r for r in self.results if r.get('success')]),
                'failed': len([r for r in self.results if not r.get('success')]),
                'results': self.results
            }, f, indent=2, ensure_ascii=False)
        
        # Save summary report
        successful = [r for r in self.results if r.get('success')]
        avg_latency = sum(r['latency'] for r in successful) / len(successful) if successful else 0
        
        summary = {
            'timestamp': datetime.now().isoformat(),
            'metrics': {
                'total_questions': len(self.results),
                'successful': len(successful),
                'failed': len(self.results) - len(successful),
                'success_rate': len(successful) / len(self.results) * 100,
                'avg_latency': round(avg_latency, 2),
                'avg_sources_per_query': round(sum(r.get('num_sources', 0) for r in successful) / len(successful), 1) if successful else 0
            }
        }
        
        with open('evaluation/summary.json', 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n💾 RESULTS SAVED:")
        print(f"  • evaluation/results.json (detailed results)")
        print(f"  • evaluation/summary.json (summary metrics)")
        print("\n" + "=" * 70 + "\n")

if __name__ == "__main__":
    print("\n🚀 Initializing RAG Pipeline...")
    pipeline = RAGPipeline()
    
    print("\n📋 Starting Evaluation...")
    evaluator = Evaluator(pipeline)
    evaluator.evaluate()
    
    print("\n✅ Evaluation Complete!")
    print("Check evaluation/results.json for detailed results")
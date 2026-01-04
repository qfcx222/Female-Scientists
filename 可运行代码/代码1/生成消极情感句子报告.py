#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json

def load_negative_sentences(file_path):
    """加载消极情感句子数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def generate_negative_sentences_report():
    """生成消极情感句子报告"""
    # 设置目录路径
    negative_sentences_dir = "output/negative_sentences"
    
    # 创建报告文件
    report_file = os.path.join("output", "消极情感句子分析报告.txt")
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("女科学家传记消极情感句子分析报告\n")
        f.write("=" * 50 + "\n\n")
        
        # 获取所有科学家的消极句子文件
        negative_files = [f for f in os.listdir(negative_sentences_dir) if f.endswith('_消极情感句子.json') and f != '所有科学家消极情感句子.json']
        
        total_negative_sentences = 0
        
        # 按科学家处理
        for filename in sorted(negative_files):
            scientist_name = filename.replace('_消极情感句子.json', '')
            file_path = os.path.join(negative_sentences_dir, filename)
            
            # 加载消极句子
            negative_sentences = load_negative_sentences(file_path)
            
            # 写入科学家标题
            f.write(f"\n{scientist_name}\n")
            f.write("-" * 30 + "\n")
            f.write(f"消极句子数量: {len(negative_sentences)}\n\n")
            
            # 写入前10个消极句子（按情感得分排序）
            sorted_sentences = sorted(negative_sentences, key=lambda x: x['情感得分'])
            for i, sentence_data in enumerate(sorted_sentences[:10]):
                f.write(f"{i+1}. 情感得分: {sentence_data['情感得分']}\n")
                f.write(f"   句子: {sentence_data['句子']}\n\n")
            
            total_negative_sentences += len(negative_sentences)
        
        # 写入总结
        f.write("=" * 50 + "\n")
        f.write("总结\n")
        f.write("=" * 50 + "\n")
        f.write(f"总共分析了 {len(negative_files)} 位科学家\n")
        f.write(f"总共找到 {total_negative_sentences} 个消极情感句子\n\n")
        
        # 按消极句子数量排序并显示
        scientist_counts = []
        for filename in negative_files:
            scientist_name = filename.replace('_消极情感句子.json', '')
            file_path = os.path.join(negative_sentences_dir, filename)
            negative_sentences = load_negative_sentences(file_path)
            scientist_counts.append((scientist_name, len(negative_sentences)))
        
        # 按数量降序排序
        scientist_counts.sort(key=lambda x: x[1], reverse=True)
        
        f.write("各科学家消极句子数量排序:\n")
        for i, (scientist, count) in enumerate(scientist_counts, 1):
            f.write(f"{i:2d}. {scientist:<10}: {count:>3d} 个消极句子\n")
    
    print(f"消极情感句子分析报告已生成: {report_file}")

def main():
    generate_negative_sentences_report()

if __name__ == "__main__":
    main()
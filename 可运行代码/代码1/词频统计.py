#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from collections import Counter
import pandas as pd

def load_association_data(file_path):
    """加载关联分析数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def calculate_word_frequency(words):
    """计算词频"""
    # 使用Counter计算词频
    word_freq = Counter(words)
    return word_freq

def analyze_scientist_frequency(scientist_name, association_file):
    """分析单个科学家的词频"""
    print(f"正在分析 {scientist_name} 的词频...")
    
    # 加载关联分析数据
    words = load_association_data(association_file)
    
    # 计算词频
    word_freq = calculate_word_frequency(words)
    
    # 获取前100个高频词
    top_words = word_freq.most_common(100)
    
    # 创建结果列表
    results = []
    for word, freq in top_words:
        results.append({
            '科学家': scientist_name,
            '词语': word,
            '频次': freq
        })
    
    return results, word_freq

def generate_overall_frequency(association_dir):
    """生成整体词频统计"""
    print("正在生成整体词频统计...")
    
    all_words = []
    
    # 遍历所有科学家的关联分析数据
    for filename in os.listdir(association_dir):
        if filename.endswith('_关联分析.json'):
            file_path = os.path.join(association_dir, filename)
            words = load_association_data(file_path)
            all_words.extend(words)
    
    # 计算整体词频
    overall_freq = calculate_word_frequency(all_words)
    
    # 获取前100个高频词
    top_overall = overall_freq.most_common(100)
    
    # 保存整体词频统计
    overall_results = []
    for word, freq in top_overall:
        overall_results.append({
            '词语': word,
            '频次': freq
        })
    
    return overall_results, overall_freq

def save_frequency_results(results, output_file):
    """保存词频统计结果"""
    # 创建DataFrame
    df = pd.DataFrame(results)
    
    # 保存为CSV文件
    csv_file = output_file.replace('.json', '.csv')
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    
    # 保存为JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"结果已保存到 {csv_file} 和 {output_file}")

def main():
    # 设置目录路径
    association_dir = "output/association_data"
    output_dir = "output/word_frequency"
    
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 存储所有科学家的词频结果
    all_scientist_results = []
    
    # 分析每个科学家的词频
    for filename in os.listdir(association_dir):
        if filename.endswith('_关联分析.json'):
            scientist_name = filename.replace('_关联分析.json', '')
            file_path = os.path.join(association_dir, filename)
            
            # 分析词频
            results, word_freq = analyze_scientist_frequency(scientist_name, file_path)
            all_scientist_results.extend(results)
            
            # 保存单个科学家的词频统计
            output_file = os.path.join(output_dir, f"{scientist_name}_词频统计.json")
            save_frequency_results(results, output_file)
            
            # 打印前10个高频词
            print(f"\n{scientist_name} 的前10个高频词:")
            for i, (word, freq) in enumerate(word_freq.most_common(10)):
                print(f"  {i+1}. {word}: {freq}")
            print()
    
    # 生成整体词频统计
    overall_results, overall_freq = generate_overall_frequency(association_dir)
    
    # 保存整体词频统计
    overall_file = os.path.join(output_dir, "整体词频统计.json")
    save_frequency_results(overall_results, overall_file)
    
    # 保存所有科学家的词频统计
    all_scientists_file = os.path.join(output_dir, "所有科学家词频统计.json")
    save_frequency_results(all_scientist_results, all_scientists_file)
    
    # 打印整体前20个高频词
    print("整体前20个高频词:")
    for i, (word, freq) in enumerate(overall_freq.most_common(20)):
        print(f"  {i+1}. {word}: {freq}")
    
    print(f"\n词频统计完成! 结果保存在 {output_dir} 目录中。")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import pandas as pd

def load_sentiment_details(file_path):
    """加载情感分析详情数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def extract_negative_sentences(sentiment_data, scientist_name):
    """提取消极情感句子"""
    negative_sentences = []
    
    for item in sentiment_data:
        if item.get('情感类别') == '负面' or item.get('情感得分', 0) < 0:
            negative_sentences.append({
                '科学家': scientist_name,
                '句子编号': item.get('句子编号'),
                '句子': item.get('句子'),
                '情感得分': item.get('情感得分')
            })
    
    return negative_sentences

def main():
    # 设置目录路径
    sentiment_details_dir = "output/sentiment_analysis"
    output_dir = "output/negative_sentences"
    
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 存储所有消极句子
    all_negative_sentences = []
    
    # 遍历所有科学家的情感分析详情文件
    for filename in os.listdir(sentiment_details_dir):
        if filename.endswith('_情感分析详情.json') and filename != '所有科学家情感分析详情.json':
            scientist_name = filename.replace('_情感分析详情.json', '')
            file_path = os.path.join(sentiment_details_dir, filename)
            
            print(f"正在处理 {scientist_name} 的情感分析数据...")
            
            # 加载情感分析详情
            sentiment_data = load_sentiment_details(file_path)
            
            # 提取消极句子
            negative_sentences = extract_negative_sentences(sentiment_data, scientist_name)
            all_negative_sentences.extend(negative_sentences)
            
            # 保存单个科学家的消极句子
            if negative_sentences:
                output_file = os.path.join(output_dir, f"{scientist_name}_消极情感句子.json")
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(negative_sentences, f, ensure_ascii=False, indent=2)
                
                # 也保存为CSV格式
                df = pd.DataFrame(negative_sentences)
                csv_file = output_file.replace('.json', '.csv')
                df.to_csv(csv_file, index=False, encoding='utf-8-sig')
                
                print(f"  找到 {len(negative_sentences)} 个消极句子，已保存到 {output_file}")
            else:
                print(f"  未找到消极句子")
    
    # 保存所有科学家的消极句子
    if all_negative_sentences:
        all_output_file = os.path.join(output_dir, "所有科学家消极情感句子.json")
        with open(all_output_file, 'w', encoding='utf-8') as f:
            json.dump(all_negative_sentences, f, ensure_ascii=False, indent=2)
        
        # 也保存为CSV格式
        df_all = pd.DataFrame(all_negative_sentences)
        all_csv_file = all_output_file.replace('.json', '.csv')
        df_all.to_csv(all_csv_file, index=False, encoding='utf-8-sig')
        
        print(f"\n总共找到 {len(all_negative_sentences)} 个消极句子")
        print(f"所有结果已保存到 {output_dir} 目录")
        
        # 按科学家分组显示统计
        scientists = set([item['科学家'] for item in all_negative_sentences])
        print("\n各科学家消极句子统计:")
        for scientist in scientists:
            count = len([item for item in all_negative_sentences if item['科学家'] == scientist])
            print(f"  {scientist}: {count} 个消极句子")
    else:
        print("未找到任何消极情感句子")

if __name__ == "__main__":
    main()
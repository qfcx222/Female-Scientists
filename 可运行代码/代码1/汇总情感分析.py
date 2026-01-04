#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd

def summarize_all_sentiment_analysis():
    """汇总所有科学家的情感分析结果"""
    sentiment_analysis_dir = "output/sentiment_analysis"
    
    # 存储所有统计数据
    all_stats = []
    
    # 遍历所有情感分析统计文件
    for filename in os.listdir(sentiment_analysis_dir):
        if filename.endswith('_情感分析统计.csv'):
            file_path = os.path.join(sentiment_analysis_dir, filename)
            
            # 读取CSV文件
            df = pd.read_csv(file_path)
            
            # 添加到统计数据中
            all_stats.append(df.iloc[0])  # 每个文件只有一行数据
    
    # 创建汇总DataFrame
    summary_df = pd.DataFrame(all_stats)
    
    # 按平均情感得分排序
    summary_df = summary_df.sort_values(by='平均情感得分', ascending=False)
    
    # 保存汇总结果
    summary_csv = os.path.join(sentiment_analysis_dir, "所有科学家情感分析汇总.csv")
    summary_df.to_csv(summary_csv, index=False, encoding='utf-8-sig')
    
    # 打印汇总结果
    print("所有科学家情感分析汇总结果:")
    print("=" * 80)
    print(f"{'科学家':<12} {'总句子数':<10} {'正面句子数':<12} {'负面句子数':<12} {'中性句子数':<12} {'平均情感得分':<12} {'整体情感倾向':<10}")
    print("-" * 80)
    
    for _, row in summary_df.iterrows():
        print(f"{row['科学家']:<12} {row['总句子数']:<10} {row['正面句子数']:<12} {row['负面句子数']:<12} {row['中性句子数']:<12} {row['平均情感得分']:<12} {row['整体情感倾向']:<10}")
    
    print("=" * 80)
    print(f"汇总结果已保存到: {summary_csv}")
    
    return summary_df

if __name__ == "__main__":
    summarize_all_sentiment_analysis()
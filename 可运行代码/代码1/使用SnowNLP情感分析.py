#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import pandas as pd
from snownlp import SnowNLP

def load_sentiment_data(file_path):
    """加载情感分析数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def analyze_sentiment_with_snownlp(sentence):
    """使用SnowNLP分析句子情感"""
    try:
        s = SnowNLP(sentence)
        # SnowNLP的情感分析返回0-1之间的值，0.5为中性，>0.5为正面，<0.5为负面
        sentiment_score = s.sentiments
        return sentiment_score
    except Exception as e:
        print(f"分析句子时出错: {sentence}, 错误: {e}")
        return 0.5  # 返回中性值

def analyze_scientist_sentiment(scientist_name, sentences):
    """分析单个科学家的情感"""
    print(f"正在使用SnowNLP分析 {scientist_name} 的情感...")
    
    # 存储结果
    results = []
    
    # 分析每句话的情感
    for i, sentence in enumerate(sentences):
        # 使用SnowNLP计算情感得分
        sentiment_score = analyze_sentiment_with_snownlp(sentence)
        
        # 确定情感类别 (SnowNLP: 0-1, 0.5为中性)
        if sentiment_score > 0.6:
            sentiment_category = "正面"
        elif sentiment_score < 0.4:
            sentiment_category = "负面"
        else:
            sentiment_category = "中性"
        
        results.append({
            '科学家': scientist_name,
            '句子编号': i + 1,
            '句子': sentence,
            '情感得分': round(sentiment_score, 4),
            '情感类别': sentiment_category
        })
    
    return results

def generate_overall_sentiment(results):
    """生成整体情感统计"""
    # 统计各类情感的句子数量
    sentiment_counts = {'正面': 0, '负面': 0, '中性': 0}
    total_score = 0.0
    total_sentences = len(results)
    
    for result in results:
        sentiment_counts[result['情感类别']] += 1
        total_score += result['情感得分']
    
    # 计算平均得分
    avg_score = total_score / total_sentences if total_sentences > 0 else 0.0
    
    # 确定整体情感倾向
    if avg_score > 0.6:
        overall_sentiment = "正面"
    elif avg_score < 0.4:
        overall_sentiment = "负面"
    else:
        overall_sentiment = "中性"
    
    return {
        '总句子数': total_sentences,
        '正面句子数': sentiment_counts['正面'],
        '负面句子数': sentiment_counts['负面'],
        '中性句子数': sentiment_counts['中性'],
        '平均情感得分': round(avg_score, 4),
        '整体情感倾向': overall_sentiment
    }

def save_sentiment_results(results, overall_stats, output_dir, scientist_name):
    """保存情感分析结果"""
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 保存详细结果
    df_detailed = pd.DataFrame(results)
    
    # 保存为CSV
    csv_file = os.path.join(output_dir, f"{scientist_name}_SnowNLP情感分析详情.csv")
    df_detailed.to_csv(csv_file, index=False, encoding='utf-8-sig')
    
    # 保存为JSON
    json_file = os.path.join(output_dir, f"{scientist_name}_SnowNLP情感分析详情.json")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # 保存整体统计
    overall_data = {
        '科学家': scientist_name,
        '统计信息': overall_stats
    }
    
    overall_csv = os.path.join(output_dir, f"{scientist_name}_SnowNLP情感分析统计.csv")
    df_overall = pd.DataFrame([overall_stats])
    df_overall.insert(0, '科学家', scientist_name)
    df_overall.to_csv(overall_csv, index=False, encoding='utf-8-sig')
    
    overall_json = os.path.join(output_dir, f"{scientist_name}_SnowNLP情感分析统计.json")
    with open(overall_json, 'w', encoding='utf-8') as f:
        json.dump(overall_data, f, ensure_ascii=False, indent=2)
    
    print(f"{scientist_name} 的SnowNLP情感分析结果已保存到 {output_dir} 目录")

def main():
    # 设置目录路径
    sentiment_dir = "output/sentiment_data"
    output_dir = "output/sentiment_analysis_snownlp"
    
    # 存储所有结果
    all_results = []
    
    # 遍历所有科学家的情感数据
    for filename in os.listdir(sentiment_dir):
        if filename.endswith('_情感分析.json'):
            scientist_name = filename.replace('_情感分析.json', '')
            file_path = os.path.join(sentiment_dir, filename)
            
            # 加载情感数据
            sentences = load_sentiment_data(file_path)
            
            # 分析情感
            results = analyze_scientist_sentiment(scientist_name, sentences)
            all_results.extend(results)
            
            # 生成整体统计
            overall_stats = generate_overall_sentiment(results)
            
            # 打印统计信息
            print(f"\n{scientist_name} SnowNLP情感分析统计:")
            print(f"  总句子数: {overall_stats['总句子数']}")
            print(f"  正面句子数: {overall_stats['正面句子数']}")
            print(f"  负面句子数: {overall_stats['负面句子数']}")
            print(f"  中性句子数: {overall_stats['中性句子数']}")
            print(f"  平均情感得分: {overall_stats['平均情感得分']}")
            print(f"  整体情感倾向: {overall_stats['整体情感倾向']}")
            
            # 保存结果
            save_sentiment_results(results, overall_stats, output_dir, scientist_name)
    
    # 保存所有结果
    all_df = pd.DataFrame(all_results)
    all_csv = os.path.join(output_dir, "所有科学家SnowNLP情感分析详情.csv")
    all_df.to_csv(all_csv, index=False, encoding='utf-8-sig')
    
    all_json = os.path.join(output_dir, "所有科学家SnowNLP情感分析详情.json")
    with open(all_json, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    # 生成汇总统计
    summary_data = []
    scientists = set([result['科学家'] for result in all_results])
    for scientist in scientists:
        scientist_results = [r for r in all_results if r['科学家'] == scientist]
        stats = generate_overall_sentiment(scientist_results)
        stats['科学家'] = scientist
        summary_data.append(stats)
    
    # 按平均情感得分排序
    summary_data.sort(key=lambda x: x['平均情感得分'], reverse=True)
    
    # 保存汇总统计
    summary_df = pd.DataFrame(summary_data)
    summary_csv = os.path.join(output_dir, "所有科学家SnowNLP情感分析汇总.csv")
    summary_df.to_csv(summary_csv, index=False, encoding='utf-8-sig')
    
    print(f"\n所有科学家的SnowNLP情感分析完成! 结果保存在 {output_dir} 目录中。")

if __name__ == "__main__":
    main()
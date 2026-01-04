#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def create_comprehensive_pie_charts():
    """创建综合情感分析饼图"""
    # 读取自研情感分析汇总数据
    custom_summary_file = "output/sentiment_analysis/所有科学家情感分析汇总.csv"
    custom_df = pd.read_csv(custom_summary_file)
    
    # 读取SnowNLP情感分析汇总数据
    snownlp_summary_file = "output/sentiment_analysis_snownlp/所有科学家SnowNLP情感分析汇总.csv"
    snownlp_df = pd.read_csv(snownlp_summary_file)
    
    # 计算总体统计数据
    total_custom_positive = custom_df['正面句子数'].sum()
    total_custom_negative = custom_df['负面句子数'].sum()
    total_custom_neutral = custom_df['中性句子数'].sum()
    
    total_snownlp_positive = snownlp_df['正面句子数'].sum()
    total_snownlp_negative = snownlp_df['负面句子数'].sum()
    total_snownlp_neutral = snownlp_df['中性句子数'].sum()
    
    # 创建综合饼图
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
    
    # 1. 自研方法总体情感分布饼图
    custom_sizes = [total_custom_positive, total_custom_negative, total_custom_neutral]
    custom_labels = [f'正面\n({total_custom_positive})', f'负面\n({total_custom_negative})', f'中性\n({total_custom_neutral})']
    custom_colors = ['green', 'red', 'gray']
    
    wedges1, texts1, autotexts1 = ax1.pie(custom_sizes, labels=custom_labels, colors=custom_colors, autopct='%1.1f%%', startangle=90)
    ax1.set_title('自研情感分析方法 - 总体情感分布', fontsize=16, pad=20)
    
    # 2. SnowNLP方法总体情感分布饼图
    snownlp_sizes = [total_snownlp_positive, total_snownlp_negative, total_snownlp_neutral]
    snownlp_labels = [f'正面\n({total_snownlp_positive})', f'负面\n({total_snownlp_negative})', f'中性\n({total_snownlp_neutral})']
    snownlp_colors = ['lightgreen', 'lightcoral', 'lightgray']
    
    wedges2, texts2, autotexts2 = ax2.pie(snownlp_sizes, labels=snownlp_labels, colors=snownlp_colors, autopct='%1.1f%%', startangle=90)
    ax2.set_title('SnowNLP情感分析方法 - 总体情感分布', fontsize=16, pad=20)
    
    # 3. 两种方法正面情感对比饼图
    comparison_positive_sizes = [total_custom_positive, total_snownlp_positive]
    comparison_positive_labels = [f'自研方法\n({total_custom_positive})', f'SnowNLP\n({total_snownlp_positive})']
    comparison_positive_colors = ['blue', 'orange']
    
    wedges3, texts3, autotexts3 = ax3.pie(comparison_positive_sizes, labels=comparison_positive_labels, colors=comparison_positive_colors, autopct='%1.1f%%', startangle=90)
    ax3.set_title('正面情感句子数量对比', fontsize=16, pad=20)
    
    # 4. 两种方法负面情感对比饼图
    comparison_negative_sizes = [total_custom_negative, total_snownlp_negative]
    comparison_negative_labels = [f'自研方法\n({total_custom_negative})', f'SnowNLP\n({total_snownlp_negative})']
    comparison_negative_colors = ['darkred', 'crimson']
    
    wedges4, texts4, autotexts4 = ax4.pie(comparison_negative_sizes, labels=comparison_negative_labels, colors=comparison_negative_colors, autopct='%1.1f%%', startangle=90)
    ax4.set_title('负面情感句子数量对比', fontsize=16, pad=20)
    
    # 调整文本大小
    for autotext in autotexts1 + autotexts2 + autotexts3 + autotexts4:
        autotext.set_fontsize(12)
        autotext.set_color('white')
        autotext.set_weight('bold')
    
    plt.tight_layout()
    plt.savefig('output/sentiment_visualizations/综合情感分析饼图.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 创建按科学家分布的饼图
    create_scientist_distribution_pie_charts(custom_df, snownlp_df)

def create_scientist_distribution_pie_charts(custom_df, snownlp_df):
    """创建按科学家分布的情感分析饼图"""
    # 按总句子数排序
    custom_df_sorted = custom_df.sort_values('总句子数', ascending=False)
    
    # 创建按科学家正面情感分布的饼图
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    
    # 自研方法各科学家正面句子数
    scientists = custom_df_sorted['科学家'].tolist()
    custom_positive_counts = custom_df_sorted['正面句子数'].tolist()
    
    # 为避免颜色重复，生成一组颜色
    colors = plt.cm.Set3(np.linspace(0, 1, len(scientists)))
    
    wedges1, texts1, autotexts1 = ax1.pie(custom_positive_counts, labels=scientists, colors=colors, autopct='%1.1f%%', startangle=90)
    ax1.set_title('自研情感分析方法 - 各科学家正面句子分布', fontsize=16, pad=20)
    
    # SnowNLP方法各科学家正面句子数
    # 按相同顺序排列科学家
    snownlp_positive_counts = []
    for scientist in scientists:
        count = snownlp_df[snownlp_df['科学家'] == scientist]['正面句子数'].iloc[0]
        snownlp_positive_counts.append(count)
    
    wedges2, texts2, autotexts2 = ax2.pie(snownlp_positive_counts, labels=scientists, colors=colors, autopct='%1.1f%%', startangle=90)
    ax2.set_title('SnowNLP情感分析方法 - 各科学家正面句子分布', fontsize=16, pad=20)
    
    # 调整文本大小
    for autotext in autotexts1 + autotexts2:
        autotext.set_fontsize(10)
        autotext.set_color('white')
        autotext.set_weight('bold')
    
    # 减少标签字体大小以避免重叠
    for text in texts1 + texts2:
        text.set_fontsize(9)
    
    plt.tight_layout()
    plt.savefig('output/sentiment_visualizations/各科学家正面情感分布饼图.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 创建按科学家负面情感分布的饼图
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    
    # 自研方法各科学家负面句子数
    custom_negative_counts = custom_df_sorted['负面句子数'].tolist()
    
    wedges1, texts1, autotexts1 = ax1.pie(custom_negative_counts, labels=scientists, colors=colors, autopct='%1.1f%%', startangle=90)
    ax1.set_title('自研情感分析方法 - 各科学家负面句子分布', fontsize=16, pad=20)
    
    # SnowNLP方法各科学家负面句子数
    snownlp_negative_counts = []
    for scientist in scientists:
        count = snownlp_df[snownlp_df['科学家'] == scientist]['负面句子数'].iloc[0]
        snownlp_negative_counts.append(count)
    
    wedges2, texts2, autotexts2 = ax2.pie(snownlp_negative_counts, labels=scientists, colors=colors, autopct='%1.1f%%', startangle=90)
    ax2.set_title('SnowNLP情感分析方法 - 各科学家负面句子分布', fontsize=16, pad=20)
    
    # 调整文本大小
    for autotext in autotexts1 + autotexts2:
        autotext.set_fontsize(10)
        autotext.set_color('white')
        autotext.set_weight('bold')
    
    # 减少标签字体大小以避免重叠
    for text in texts1 + texts2:
        text.set_fontsize(9)
    
    plt.tight_layout()
    plt.savefig('output/sentiment_visualizations/各科学家负面情感分布饼图.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    print("正在生成综合情感分析饼图...")
    create_comprehensive_pie_charts()
    print("综合情感分析饼图已生成完成！")
    print("结果保存在 output/sentiment_visualizations 目录中")

if __name__ == "__main__":
    main()
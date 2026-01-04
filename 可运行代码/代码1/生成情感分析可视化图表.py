#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def load_sentiment_stats(file_path):
    """加载情感分析统计数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def collect_all_sentiment_data():
    """收集所有科学家的情感分析数据"""
    # 收集自研情感分析数据
    custom_sentiment_dir = "output/sentiment_analysis"
    custom_stats = {}
    
    for filename in os.listdir(custom_sentiment_dir):
        if filename.endswith('_情感分析统计.json'):
            scientist_name = filename.replace('_情感分析统计.json', '')
            file_path = os.path.join(custom_sentiment_dir, filename)
            data = load_sentiment_stats(file_path)
            custom_stats[scientist_name] = data['统计信息']
    
    # 收集SnowNLP情感分析数据
    snownlp_sentiment_dir = "output/sentiment_analysis_snownlp"
    snownlp_stats = {}
    
    for filename in os.listdir(snownlp_sentiment_dir):
        if filename.endswith('_SnowNLP情感分析统计.json'):
            scientist_name = filename.replace('_SnowNLP情感分析统计.json', '')
            file_path = os.path.join(snownlp_sentiment_dir, filename)
            data = load_sentiment_stats(file_path)
            snownlp_stats[scientist_name] = data['统计信息']
    
    return custom_stats, snownlp_stats

def create_bar_chart_comparison(custom_stats, snownlp_stats):
    """创建柱状图对比不同情感分析方法的结果"""
    scientists = list(custom_stats.keys())
    
    # 提取数据
    custom_positive = [custom_stats[s]['正面句子数'] for s in scientists]
    custom_negative = [custom_stats[s]['负面句子数'] for s in scientists]
    custom_neutral = [custom_stats[s]['中性句子数'] for s in scientists]
    
    snownlp_positive = [snownlp_stats[s]['正面句子数'] for s in scientists]
    snownlp_negative = [snownlp_stats[s]['负面句子数'] for s in scientists]
    snownlp_neutral = [snownlp_stats[s]['中性句子数'] for s in scientists]
    
    # 创建图表
    fig, ax = plt.subplots(figsize=(16, 10))
    
    x = np.arange(len(scientists))
    width = 0.35
    
    # 自研方法数据
    rects1 = ax.bar(x - width/2, custom_positive, width, label='自研方法-正面', alpha=0.8, color='green')
    rects2 = ax.bar(x - width/2, custom_negative, width, bottom=custom_positive, label='自研方法-负面', alpha=0.8, color='red')
    rects3 = ax.bar(x - width/2, custom_neutral, width, bottom=np.array(custom_positive)+np.array(custom_negative), label='自研方法-中性', alpha=0.8, color='gray')
    
    # SnowNLP方法数据
    bottoms_snownlp = np.zeros(len(scientists))
    rects4 = ax.bar(x + width/2, snownlp_positive, width, label='SnowNLP-正面', alpha=0.8, color='lightgreen')
    bottoms_snownlp += snownlp_positive
    rects5 = ax.bar(x + width/2, snownlp_negative, width, bottom=bottoms_snownlp, label='SnowNLP-负面', alpha=0.8, color='lightcoral')
    bottoms_snownlp += snownlp_negative
    rects6 = ax.bar(x + width/2, snownlp_neutral, width, bottom=bottoms_snownlp, label='SnowNLP-中性', alpha=0.8, color='lightgray')
    
    # 设置图表属性
    ax.set_xlabel('科学家')
    ax.set_ylabel('句子数量')
    ax.set_title('不同情感分析方法结果对比')
    ax.set_xticks(x)
    ax.set_xticklabels(scientists, rotation=45, ha='right')
    ax.legend()
    
    # 保存图表
    output_dir = "output/sentiment_visualizations"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '情感分析方法对比柱状图.png'), dpi=300, bbox_inches='tight')
    plt.close()

def create_pie_charts(custom_stats, snownlp_stats):
    """为每个科学家创建饼图"""
    output_dir = "output/sentiment_visualizations"
    pie_charts_dir = os.path.join(output_dir, "情感分布饼图")
    if not os.path.exists(pie_charts_dir):
        os.makedirs(pie_charts_dir)
    
    scientists = list(custom_stats.keys())
    
    for scientist in scientists:
        # 创建子图
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
        
        # 自研方法饼图
        custom_data = custom_stats[scientist]
        sizes_custom = [custom_data['正面句子数'], custom_data['负面句子数'], custom_data['中性句子数']]
        labels_custom = ['正面', '负面', '中性']
        colors_custom = ['green', 'red', 'gray']
        
        ax1.pie(sizes_custom, labels=labels_custom, colors=colors_custom, autopct='%1.1f%%', startangle=90)
        ax1.set_title(f'{scientist} - 自研情感分析')
        
        # SnowNLP方法饼图
        snownlp_data = snownlp_stats[scientist]
        sizes_snownlp = [snownlp_data['正面句子数'], snownlp_data['负面句子数'], snownlp_data['中性句子数']]
        labels_snownlp = ['正面', '负面', '中性']
        colors_snownlp = ['lightgreen', 'lightcoral', 'lightgray']
        
        ax2.pie(sizes_snownlp, labels=labels_snownlp, colors=colors_snownlp, autopct='%1.1f%%', startangle=90)
        ax2.set_title(f'{scientist} - SnowNLP情感分析')
        
        plt.tight_layout()
        plt.savefig(os.path.join(pie_charts_dir, f'{scientist}_情感分布饼图.png'), dpi=300, bbox_inches='tight')
        plt.close()

def create_horizontal_bar_chart(custom_stats, snownlp_stats):
    """创建横向柱状图显示平均情感得分"""
    scientists = list(custom_stats.keys())
    
    # 提取平均情感得分
    custom_avg_scores = [custom_stats[s]['平均情感得分'] for s in scientists]
    snownlp_avg_scores = [snownlp_stats[s]['平均情感得分'] for s in scientists]
    
    # 创建横向柱状图
    fig, ax = plt.subplots(figsize=(14, 10))
    
    y = np.arange(len(scientists))
    height = 0.35
    
    bars1 = ax.barh(y - height/2, custom_avg_scores, height, label='自研方法', alpha=0.8, color='blue')
    bars2 = ax.barh(y + height/2, snownlp_avg_scores, height, label='SnowNLP', alpha=0.8, color='orange')
    
    # 添加数值标签
    for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
        ax.text(bar1.get_width() + 0.01, bar1.get_y() + bar1.get_height()/2, 
                f'{custom_avg_scores[i]:.3f}', ha='left', va='center')
        ax.text(bar2.get_width() + 0.01, bar2.get_y() + bar2.get_height()/2, 
                f'{snownlp_avg_scores[i]:.3f}', ha='left', va='center')
    
    # 设置图表属性
    ax.set_ylabel('科学家')
    ax.set_xlabel('平均情感得分')
    ax.set_title('不同情感分析方法平均得分对比')
    ax.set_yticks(y)
    ax.set_yticklabels(scientists)
    ax.legend()
    ax.grid(axis='x', alpha=0.3)
    
    # 保存图表
    output_dir = "output/sentiment_visualizations"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '情感分析平均得分对比.png'), dpi=300, bbox_inches='tight')
    plt.close()

def create_stacked_area_chart(custom_stats, snownlp_stats):
    """创建堆叠面积图显示情感分布趋势"""
    scientists = list(custom_stats.keys())
    
    # 提取比例数据
    custom_positive_ratio = [custom_stats[s]['正面句子数']/custom_stats[s]['总句子数'] for s in scientists]
    custom_negative_ratio = [custom_stats[s]['负面句子数']/custom_stats[s]['总句子数'] for s in scientists]
    custom_neutral_ratio = [custom_stats[s]['中性句子数']/custom_stats[s]['总句子数'] for s in scientists]
    
    snownlp_positive_ratio = [snownlp_stats[s]['正面句子数']/snownlp_stats[s]['总句子数'] for s in scientists]
    snownlp_negative_ratio = [snownlp_stats[s]['负面句子数']/snownlp_stats[s]['总句子数'] for s in scientists]
    snownlp_neutral_ratio = [snownlp_stats[s]['中性句子数']/snownlp_stats[s]['总句子数'] for s in scientists]
    
    # 创建堆叠面积图
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
    
    x = np.arange(len(scientists))
    
    # 自研方法
    ax1.fill_between(x, 0, custom_positive_ratio, label='正面', alpha=0.7, color='green')
    ax1.fill_between(x, custom_positive_ratio, np.array(custom_positive_ratio)+np.array(custom_negative_ratio), 
                     label='负面', alpha=0.7, color='red')
    ax1.fill_between(x, np.array(custom_positive_ratio)+np.array(custom_negative_ratio), 
                     np.array(custom_positive_ratio)+np.array(custom_negative_ratio)+np.array(custom_neutral_ratio), 
                     label='中性', alpha=0.7, color='gray')
    ax1.set_title('自研情感分析方法 - 情感分布')
    ax1.set_xticks(x)
    ax1.set_xticklabels(scientists, rotation=45, ha='right')
    ax1.set_ylabel('比例')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # SnowNLP方法
    ax2.fill_between(x, 0, snownlp_positive_ratio, label='正面', alpha=0.7, color='lightgreen')
    ax2.fill_between(x, snownlp_positive_ratio, np.array(snownlp_positive_ratio)+np.array(snownlp_negative_ratio), 
                     label='负面', alpha=0.7, color='lightcoral')
    ax2.fill_between(x, np.array(snownlp_positive_ratio)+np.array(snownlp_negative_ratio), 
                     np.array(snownlp_positive_ratio)+np.array(snownlp_negative_ratio)+np.array(snownlp_neutral_ratio), 
                     label='中性', alpha=0.7, color='lightgray')
    ax2.set_title('SnowNLP情感分析方法 - 情感分布')
    ax2.set_xticks(x)
    ax2.set_xticklabels(scientists, rotation=45, ha='right')
    ax2.set_ylabel('比例')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 保存图表
    output_dir = "output/sentiment_visualizations"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '情感分布堆叠面积图.png'), dpi=300, bbox_inches='tight')
    plt.close()

def create_heatmap(custom_stats, snownlp_stats):
    """创建热力图显示情感分布"""
    scientists = list(custom_stats.keys())
    
    # 创建数据矩阵
    data = []
    for scientist in scientists:
        row = [
            custom_stats[scientist]['正面句子数'],
            custom_stats[scientist]['负面句子数'],
            custom_stats[scientist]['中性句子数'],
            snownlp_stats[scientist]['正面句子数'],
            snownlp_stats[scientist]['负面句子数'],
            snownlp_stats[scientist]['中性句子数']
        ]
        data.append(row)
    
    # 创建热力图
    fig, ax = plt.subplots(figsize=(14, 10))
    
    im = ax.imshow(data, cmap='RdYlGn', aspect='auto')
    
    # 设置标签
    ax.set_xticks(np.arange(6))
    ax.set_xticklabels(['自研-正面', '自研-负面', '自研-中性', 'SnowNLP-正面', 'SnowNLP-负面', 'SnowNLP-中性'], rotation=45, ha='right')
    ax.set_yticks(np.arange(len(scientists)))
    ax.set_yticklabels(scientists)
    
    ax.set_title('情感分析结果热力图')
    
    # 添加颜色条
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('句子数量')
    
    # 在每个单元格中添加文本
    for i in range(len(scientists)):
        for j in range(6):
            text = ax.text(j, i, data[i][j], ha="center", va="center", color="black")
    
    # 保存图表
    output_dir = "output/sentiment_visualizations"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '情感分析热力图.png'), dpi=300, bbox_inches='tight')
    plt.close()

def main():
    print("正在收集情感分析数据...")
    custom_stats, snownlp_stats = collect_all_sentiment_data()
    
    print("正在生成柱状图对比...")
    create_bar_chart_comparison(custom_stats, snownlp_stats)
    
    print("正在生成饼图...")
    create_pie_charts(custom_stats, snownlp_stats)
    
    print("正在生成横向柱状图...")
    create_horizontal_bar_chart(custom_stats, snownlp_stats)
    
    print("正在生成堆叠面积图...")
    create_stacked_area_chart(custom_stats, snownlp_stats)
    
    print("正在生成热力图...")
    create_heatmap(custom_stats, snownlp_stats)
    
    print("所有情感分析可视化图表已生成完成！")
    print("结果保存在 output/sentiment_visualizations 目录中")

if __name__ == "__main__":
    main()
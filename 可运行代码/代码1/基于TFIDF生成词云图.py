#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def load_tfidf_data(file_path):
    """加载TF-IDF统计数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def generate_wordcloud_from_tfidf(tfidf_dict, scientist_name, output_path):
    """根据TF-IDF数据生成词云图"""
    # 创建词云对象
    wc = WordCloud(
        font_path="C:/Windows/Fonts/simhei.ttf",  # Windows系统中黑体字体路径
        width=800,
        height=600,
        background_color='white',
        max_words=200,
        colormap='plasma'
    )
    
    # 生成词云（TF-IDF值作为权重）
    wc.generate_from_frequencies(tfidf_dict)
    
    # 显示图片
    plt.figure(figsize=(10, 8))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'{scientist_name} TF-IDF词云图', fontsize=20)
    
    # 保存图片
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def process_all_scientists_tfidf():
    """处理所有科学家的TF-IDF数据并生成词云图"""
    input_dir = 'e:/女科学家/数据清理/output/tfidf_analysis'
    output_dir = 'e:/女科学家/数据清理/output/tfidf_word_clouds'
    
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 获取所有TF-IDF json文件
    json_files = [f for f in os.listdir(input_dir) if f.endswith('_TFIDF词汇.json')]
    
    for json_file in json_files:
        print(f"正在处理 {json_file}...")
        
        # 加载TF-IDF数据
        file_path = os.path.join(input_dir, json_file)
        tfidf_data = load_tfidf_data(file_path)
        
        # 提取科学家姓名
        scientist_name = json_file.replace('_TFIDF词汇.json', '')
        
        # 生成词云图
        output_path = os.path.join(output_dir, f'{scientist_name}_TFIDF词云图.png')
        generate_wordcloud_from_tfidf(tfidf_data, scientist_name, output_path)
        print(f"{scientist_name} TF-IDF词云图已生成: {output_path}")

if __name__ == '__main__':
    process_all_scientists_tfidf()
    print("所有科学家的TF-IDF词云图生成完毕！")
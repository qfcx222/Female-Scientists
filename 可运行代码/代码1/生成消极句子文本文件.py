#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json

def load_negative_sentences(file_path):
    """加载消极情感句子数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def generate_negative_sentences_text_files():
    """为每个科学家生成消极情感句子的文本文件"""
    # 设置目录路径
    negative_sentences_dir = "output/negative_sentences"
    output_dir = "output/negative_sentences_text"
    
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 获取所有科学家的消极句子文件
    negative_files = [f for f in os.listdir(negative_sentences_dir) if f.endswith('_消极情感句子.json') and f != '所有科学家消极情感句子.json']
    
    # 为每个科学家生成文本文件
    for filename in sorted(negative_files):
        scientist_name = filename.replace('_消极情感句子.json', '')
        file_path = os.path.join(negative_sentences_dir, filename)
        
        # 加载消极句子
        negative_sentences = load_negative_sentences(file_path)
        
        # 创建文本文件
        text_file = os.path.join(output_dir, f"{scientist_name}_消极情感句子.txt")
        
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(f"{scientist_name}的消极情感句子\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"总共找到 {len(negative_sentences)} 个消极情感句子\n\n")
            
            # 按情感得分排序（从最消极到 least 消极）
            sorted_sentences = sorted(negative_sentences, key=lambda x: x['情感得分'])
            
            # 写入所有消极句子
            for i, sentence_data in enumerate(sorted_sentences, 1):
                f.write(f"{i:3d}. 情感得分: {sentence_data['情感得分']}\n")
                f.write(f"    句子编号: {sentence_data['句子编号']}\n")
                f.write(f"    句子内容: {sentence_data['句子']}\n\n")
        
        print(f"已生成 {scientist_name} 的消极情感句子文本文件: {text_file}")
    
    print(f"\n所有科学家的消极情感句子文本文件已生成到 {output_dir} 目录")

def main():
    generate_negative_sentences_text_files()

if __name__ == "__main__":
    main()
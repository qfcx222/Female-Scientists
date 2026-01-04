#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import pandas as pd

def generate_summary_report():
    """生成数据清理总结报告"""
    report_lines = []
    report_lines.append("# 女科学家传记数据清理总结报告")
    report_lines.append("")
    report_lines.append("## 处理概览")
    report_lines.append("")
    
    # 统计信息
    total_scientists = 0
    total_sentiment_sentences = 0
    total_association_words = 0
    total_cleaned_chars = 0
    
    scientists_data = []
    
    # 遍历所有科学家的数据
    sentiment_dir = "output/sentiment_data"
    association_dir = "output/association_data"
    cleaned_dir = "output/cleaned_data"
    
    for filename in os.listdir(sentiment_dir):
        if filename.endswith("_情感分析.json"):
            scientist_name = filename.replace("_情感分析.json", "")
            total_scientists += 1
            
            # 读取情感分析数据
            sentiment_file = os.path.join(sentiment_dir, filename)
            with open(sentiment_file, 'r', encoding='utf-8') as f:
                sentiment_data = json.load(f)
            sentiment_count = len(sentiment_data)
            total_sentiment_sentences += sentiment_count
            
            # 读取关联分析数据
            association_file = os.path.join(association_dir, f"{scientist_name}_关联分析.json")
            with open(association_file, 'r', encoding='utf-8') as f:
                association_data = json.load(f)
            association_count = len(association_data)
            total_association_words += association_count
            
            # 读取清洗后文本
            cleaned_file = os.path.join(cleaned_dir, f"{scientist_name}_清洗文本.txt")
            with open(cleaned_file, 'r', encoding='utf-8') as f:
                cleaned_text = f.read()
            cleaned_chars = len(cleaned_text)
            total_cleaned_chars += cleaned_chars
            
            scientists_data.append({
                "科学家": scientist_name,
                "情感句子数": sentiment_count,
                "关联词汇数": association_count,
                "清洗后字符数": cleaned_chars
            })
    
    report_lines.append(f"总共处理科学家数量: {total_scientists}")
    report_lines.append(f"总共情感分析句子数: {total_sentiment_sentences}")
    report_lines.append(f"总共关联分析词汇数: {total_association_words}")
    report_lines.append(f"总共清洗后字符数: {total_cleaned_chars}")
    report_lines.append("")
    
    report_lines.append("## 各科学家数据详情")
    report_lines.append("")
    
    # 创建DataFrame并排序
    df = pd.DataFrame(scientists_data)
    df = df.sort_values(by="清洗后字符数", ascending=False)
    
    # 添加表格
    report_lines.append("| 科学家 | 情感句子数 | 关联词汇数 | 清洗后字符数 |")
    report_lines.append("|--------|------------|------------|--------------|")
    for _, row in df.iterrows():
        report_lines.append(f"| {row['科学家']} | {row['情感句子数']} | {row['关联词汇数']} | {row['清洗后字符数']} |")
    
    report_lines.append("")
    report_lines.append("## 数据处理说明")
    report_lines.append("")
    report_lines.append("1. **格式转换与基础提取**: 使用python-docx库提取.docx文件中的段落文本")
    report_lines.append("2. **去噪处理**: 去除特殊符号、引用标注、URL和邮箱等无关信息")
    report_lines.append("3. **字符标准化**: 统一全角/半角字符")
    report_lines.append("4. **分词与去停用词**: 使用jieba进行中文分词，并去除停用词")
    report_lines.append("5. **实体对齐**: 统一科学家名称的不同表达方式")
    report_lines.append("6. **定制化清洗**: 为情感分析和关联分析分别准备不同的数据格式")
    report_lines.append("")
    report_lines.append("## 输出文件结构")
    report_lines.append("")
    report_lines.append("```\noutput/\n├── sentiment_data/     # 情感分析数据（按句子分割）\n├── association_data/   # 关联分析数据（分词结果）\n└── cleaned_data/      # 清洗后的纯文本\n```")
    
    # 保存报告
    with open("数据清理总结报告.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    
    print("数据清理总结报告已生成: 数据清理总结报告.md")
    
    # 打印简要报告
    print("\n=== 数据清理总结报告 ===")
    print(f"总共处理科学家数量: {total_scientists}")
    print(f"总共情感分析句子数: {total_sentiment_sentences}")
    print(f"总共关联分析词汇数: {total_association_words}")
    print(f"总共清洗后字符数: {total_cleaned_chars}")
    print("\n各科学家数据详情:")
    print(df.to_string(index=False))

if __name__ == "__main__":
    generate_summary_report()
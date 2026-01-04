#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import jieba
import pandas as pd
from collections import defaultdict

def load_sentiment_data(file_path):
    """加载情感分析数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def get_sentiment_lexicon():
    """获取情感词典"""
    # 正面情感词
    positive_words = {
        '优秀', '杰出', '卓越', '伟大', '杰出', '出色', '优异', '精彩', '辉煌', '成功',
        '胜利', '幸福', '快乐', '喜悦', '欢乐', '欣慰', '满意', '赞美', '敬佩', '崇敬',
        '热爱', '喜欢', '欣赏', '感动', '激动', '兴奋', '骄傲', '自豪', '感动', '温暖',
        '美好', '美丽', '优美', '动人', '感人', '温馨', '甜蜜', '舒适', '安心', '放心',
        '希望', '期待', '向往', '追求', '奋斗', '努力', '坚持', '坚强', '勇敢', '无畏',
        '智慧', '聪明', '机智', '才华', '天赋', '才能', '本领', '技能', '专业', '专长',
        '贡献', '奉献', '付出', '努力', '辛勤', '勤劳', '认真', '负责', '敬业', '专注',
        '创新', '创造', '发明', '发现', '突破', '进步', '发展', '成长', '提升', '改善',
        '帮助', '支持', '援助', '协助', '合作', '团结', '友爱', '关爱', '关心', '照顾',
        '尊重', '尊敬', '敬重', '敬仰', '仰慕', '崇拜', '信任', '信赖', '依赖', '依靠'
    }
    
    # 负面情感词
    negative_words = {
        '糟糕', '恶劣', '差劲', '失败', '挫折', '困难', '艰难', '艰苦', '痛苦', '悲伤',
        '伤心', '难过', '失望', '绝望', '沮丧', '沮丧', '郁闷', '烦恼', '焦虑', '担忧',
        '恐惧', '害怕', '畏惧', '胆怯', '懦弱', '退缩', '逃避', '放弃', '绝望', '无助',
        '愤怒', '生气', '恼怒', '愤慨', '憎恨', '厌恶', '讨厌', '嫌弃', '排斥', '歧视',
        '孤独', '寂寞', '冷清', '凄凉', '悲凉', '悲哀', '哀伤', '忧伤', '忧郁', '抑郁',
        '疲惫', '疲劳', '劳累', '辛苦', '艰辛', '困苦', '贫苦', '贫穷', '贫困', '穷困',
        '疾病', '病痛', '痛苦', '折磨', '煎熬', '苦难', '不幸', '悲剧', '灾难', '祸害',
        '阻碍', '障碍', '阻力', '困难', '麻烦', '问题', '困扰', '烦恼', '忧虑', '担心',
        '批评', '指责', '责备', '责怪', '抱怨', '埋怨', '不满', '失望', '绝望', '无助',
        '背叛', '欺骗', '谎言', '虚假', '虚伪', '假冒', '伪造', '欺骗', '诈骗', '坑害'
    }
    
    # 程度副词
    degree_words = {
        '非常': 2.0, '很': 1.5, '特别': 2.0, '十分': 1.8, '极其': 2.2, '超级': 2.0,
        '相当': 1.3, '比较': 1.2, '较为': 1.1, '有点': 0.8, '稍微': 0.6, '略微': 0.5,
        '极': 2.0, '挺': 1.2, '蛮': 1.0, '颇': 1.1, '甚': 1.8, '最': 2.5
    }
    
    # 否定词
    negation_words = {'不', '没', '无', '非', '未', '否', '别', '勿', '毋', '莫'}
    
    return positive_words, negative_words, degree_words, negation_words

def calculate_sentence_sentiment(sentence, positive_words, negative_words, degree_words, negation_words):
    """计算句子情感得分"""
    # 分词
    words = jieba.lcut(sentence)
    
    # 初始化得分
    sentiment_score = 0.0
    word_count = 0
    
    # 遍历词语
    i = 0
    while i < len(words):
        word = words[i]
        
        # 检查是否为情感词
        if word in positive_words:
            score = 1.0
            # 检查前面是否有程度副词
            if i > 0 and words[i-1] in degree_words:
                score *= degree_words[words[i-1]]
            # 检查前面是否有否定词
            if i > 0 and words[i-1] in negation_words:
                score *= -1
            elif i > 1 and words[i-2] in negation_words:
                score *= -1
            sentiment_score += score
            word_count += 1
        elif word in negative_words:
            score = -1.0
            # 检查前面是否有程度副词
            if i > 0 and words[i-1] in degree_words:
                score *= degree_words[words[i-1]]
            # 检查前面是否有否定词
            if i > 0 and words[i-1] in negation_words:
                score *= -1
            elif i > 1 and words[i-2] in negation_words:
                score *= -1
            sentiment_score += score
            word_count += 1
            
        i += 1
    
    # 计算平均得分
    if word_count > 0:
        avg_score = sentiment_score / word_count
    else:
        avg_score = 0.0
    
    return avg_score

def analyze_scientist_sentiment(scientist_name, sentences):
    """分析单个科学家的情感"""
    print(f"正在分析 {scientist_name} 的情感...")
    
    # 获取情感词典
    positive_words, negative_words, degree_words, negation_words = get_sentiment_lexicon()
    
    # 存储结果
    results = []
    
    # 分析每句话的情感
    for i, sentence in enumerate(sentences):
        # 计算情感得分
        sentiment_score = calculate_sentence_sentiment(
            sentence, positive_words, negative_words, degree_words, negation_words
        )
        
        # 确定情感类别
        if sentiment_score > 0.1:
            sentiment_category = "正面"
        elif sentiment_score < -0.1:
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
    sentiment_counts = defaultdict(int)
    total_score = 0.0
    total_sentences = len(results)
    
    for result in results:
        sentiment_counts[result['情感类别']] += 1
        total_score += result['情感得分']
    
    # 计算平均得分
    avg_score = total_score / total_sentences if total_sentences > 0 else 0.0
    
    # 确定整体情感倾向
    if avg_score > 0.1:
        overall_sentiment = "正面"
    elif avg_score < -0.1:
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
    csv_file = os.path.join(output_dir, f"{scientist_name}_情感分析详情.csv")
    df_detailed.to_csv(csv_file, index=False, encoding='utf-8-sig')
    
    # 保存为JSON
    json_file = os.path.join(output_dir, f"{scientist_name}_情感分析详情.json")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # 保存整体统计
    overall_data = {
        '科学家': scientist_name,
        '统计信息': overall_stats
    }
    
    overall_csv = os.path.join(output_dir, f"{scientist_name}_情感分析统计.csv")
    df_overall = pd.DataFrame([overall_stats])
    df_overall.insert(0, '科学家', scientist_name)
    df_overall.to_csv(overall_csv, index=False, encoding='utf-8-sig')
    
    overall_json = os.path.join(output_dir, f"{scientist_name}_情感分析统计.json")
    with open(overall_json, 'w', encoding='utf-8') as f:
        json.dump(overall_data, f, ensure_ascii=False, indent=2)
    
    print(f"{scientist_name} 的情感分析结果已保存到 {output_dir} 目录")

def main():
    # 设置目录路径
    sentiment_dir = "output/sentiment_data"
    output_dir = "output/sentiment_analysis"
    
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
            print(f"\n{scientist_name} 情感分析统计:")
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
    all_csv = os.path.join(output_dir, "所有科学家情感分析详情.csv")
    all_df.to_csv(all_csv, index=False, encoding='utf-8-sig')
    
    all_json = os.path.join(output_dir, "所有科学家情感分析详情.json")
    with open(all_json, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n所有科学家的情感分析完成! 结果保存在 {output_dir} 目录中。")

if __name__ == "__main__":
    main()
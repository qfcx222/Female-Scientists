#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import jieba
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def load_cleaned_text(file_path):
    """加载清洗后的文本"""
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

def load_association_words(file_path):
    """加载关联分析词汇"""
    with open(file_path, 'r', encoding='utf-8') as f:
        words = json.load(f)
    return words

def prepare_documents(cleaned_dir):
    """准备文档集合"""
    documents = {}
    scientist_names = []
    
    print("正在加载文档...")
    for filename in os.listdir(cleaned_dir):
        if filename.endswith('_清洗文本.txt'):
            scientist_name = filename.replace('_清洗文本.txt', '')
            file_path = os.path.join(cleaned_dir, filename)
            
            # 加载清洗后的文本
            text = load_cleaned_text(file_path)
            documents[scientist_name] = text
            scientist_names.append(scientist_name)
            print(f"已加载 {scientist_name} 的文档")
    
    return documents, scientist_names

def calculate_tfidf(documents, scientist_names):
    """计算TF-IDF值"""
    print("正在计算TF-IDF值...")
    
    # 准备文档列表
    docs = [documents[name] for name in scientist_names]
    
    # 创建TF-IDF向量化器
    # 使用中文停用词
    stop_words = get_chinese_stopwords()
    
    # 初始化TF-IDF向量化器
    vectorizer = TfidfVectorizer(
        tokenizer=chinese_tokenizer,
        stop_words=stop_words,
        max_features=10000,  # 最多保留10000个特征
        ngram_range=(1, 2),  # 使用1-gram和2-gram
        min_df=2,  # 词语至少出现在2个文档中
        max_df=0.8  # 词语最多出现在80%的文档中
    )
    
    # 计算TF-IDF矩阵
    tfidf_matrix = vectorizer.fit_transform(docs)
    
    # 获取特征名称
    feature_names = vectorizer.get_feature_names_out()
    
    return tfidf_matrix, feature_names, vectorizer

def chinese_tokenizer(text):
    """中文分词器"""
    # 使用jieba进行分词
    words = jieba.lcut(text)
    # 过滤掉单字符词（除了重要的单字）
    filtered_words = [word for word in words if len(word) > 1 or word in ['一', '不', '了', '的', '是']]
    return filtered_words

def get_chinese_stopwords():
    """获取中文停用词表"""
    stopwords = {
        '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去',
        '你', '会', '着', '没有', '看', '好', '自己', '这', '那', '它', '他', '她', '我们', '你们', '他们', '这个', '那个',
        '什么', '怎么', '为什么', '哪里', '哪个', '多少', '几', '些', '每', '各', '另', '别', '其他', '另外', '此外',
        '而且', '或者', '如果', '虽然', '但是', '然而', '因此', '所以', '为了', '因为', '由于', '通过', '经过', '作为',
        '对于', '关于', '有关', '按照', '根据', '依据', '随着', '同时', '以及', '及其', '与其', '或是', '还有', '只有',
        '只要', '才能', '使得', '可以', '能够', '应该', '必须', '需要', '愿意', '希望', '打算', '准备', '开始', '继续',
        '停止', '结束', '出来', '起来', '下去', '下来', '过去', '过来', '回去', '出来', '以来', '以后', '以前', '以后',
        '时候', '时间', '时候', '之后', '之前', '期间', '年代', '世纪', '年', '月', '日', '时', '分', '秒'
    }
    return list(stopwords)

def get_top_tfidf_words(tfidf_matrix, feature_names, scientist_names, top_n=50):
    """获取每个科学家的Top TF-IDF词汇"""
    print("正在提取每个科学家的Top TF-IDF词汇...")
    
    results = {}
    
    for i, scientist_name in enumerate(scientist_names):
        # 获取该科学家文档的TF-IDF值
        tfidf_scores = tfidf_matrix[i].toarray()[0]
        
        # 创建词汇和分数的配对
        word_scores = list(zip(feature_names, tfidf_scores))
        
        # 按分数排序
        word_scores.sort(key=lambda x: x[1], reverse=True)
        
        # 获取Top N词汇
        top_words = word_scores[:top_n]
        
        results[scientist_name] = top_words
        
        print(f"\n{scientist_name} 的Top {top_n} TF-IDF词汇:")
        for j, (word, score) in enumerate(top_words[:10]):  # 只打印前10个
            print(f"  {j+1}. {word}: {score:.4f}")
    
    return results

def calculate_document_similarity(tfidf_matrix, scientist_names):
    """计算文档相似度"""
    print("正在计算文档相似度...")
    
    # 计算余弦相似度矩阵
    similarity_matrix = cosine_similarity(tfidf_matrix)
    
    # 创建相似度DataFrame
    similarity_df = pd.DataFrame(
        similarity_matrix,
        index=scientist_names,
        columns=scientist_names
    )
    
    return similarity_df

def save_tfidf_results(results, output_dir):
    """保存TF-IDF结果"""
    print("正在保存TF-IDF结果...")
    
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 保存每个科学家的TF-IDF词汇
    for scientist_name, word_scores in results.items():
        # 转换为DataFrame
        df = pd.DataFrame(word_scores, columns=['词语', 'TF-IDF值'])
        
        # 保存为CSV
        csv_file = os.path.join(output_dir, f"{scientist_name}_TFIDF词汇.csv")
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        
        # 保存为JSON
        json_file = os.path.join(output_dir, f"{scientist_name}_TFIDF词汇.json")
        word_dict = {word: float(score) for word, score in word_scores}
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(word_dict, f, ensure_ascii=False, indent=2)
    
    print(f"TF-IDF结果已保存到 {output_dir} 目录")

def save_similarity_results(similarity_df, output_dir):
    """保存相似度结果"""
    print("正在保存相似度结果...")
    
    # 保存相似度矩阵
    csv_file = os.path.join(output_dir, "科学家相似度矩阵.csv")
    similarity_df.to_csv(csv_file, encoding='utf-8-sig')
    
    # 保存为JSON
    json_file = os.path.join(output_dir, "科学家相似度矩阵.json")
    similarity_dict = similarity_df.to_dict()
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(similarity_dict, f, ensure_ascii=False, indent=2)
    
    # 打印相似度摘要
    print("\n科学家相似度摘要:")
    for scientist in similarity_df.index:
        # 获取与其他科学家的相似度（排除自己）
        similarities = similarity_df.loc[scientist].drop(scientist)
        top_similar = similarities.nlargest(3)
        print(f"\n{scientist} 最相似的三位科学家:")
        for similar_scientist, similarity in top_similar.items():
            print(f"  {similar_scientist}: {similarity:.4f}")

def main():
    # 设置目录路径
    cleaned_dir = "output/cleaned_data"
    output_dir = "output/tfidf_analysis"
    
    # 准备文档
    documents, scientist_names = prepare_documents(cleaned_dir)
    
    # 计算TF-IDF
    tfidf_matrix, feature_names, vectorizer = calculate_tfidf(documents, scientist_names)
    
    # 获取每个科学家的Top TF-IDF词汇
    tfidf_results = get_top_tfidf_words(tfidf_matrix, feature_names, scientist_names, top_n=100)
    
    # 计算文档相似度
    similarity_df = calculate_document_similarity(tfidf_matrix, scientist_names)
    
    # 保存结果
    save_tfidf_results(tfidf_results, output_dir)
    save_similarity_results(similarity_df, output_dir)
    
    print(f"\nTF-IDF分析完成! 结果保存在 {output_dir} 目录中。")

if __name__ == "__main__":
    main()
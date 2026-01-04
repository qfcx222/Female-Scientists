#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import jieba
import pandas as pd
from docx import Document
try:
    import opencc
except ImportError:
    from opencc import OpenCC as opencc

class DataCleaningPipeline:
    def __init__(self):
        # 简体到繁体转换器
        try:
            self.cc = opencc.OpenCC('s2t')
        except AttributeError:
            self.cc = opencc('s2t')
        # 自定义词典，添加科学家姓名和专业术语
        self.custom_words = [
            '屠呦呦', '居里夫人', '玛丽·居里', '丽丝·迈特纳', '何泽慧', 
            '卡塔林·考里科', '吴健雄', '埃达·洛夫莱斯', '杜德娜', 
            '林巧稚', '谢希德', '诺贝尔奖', '青蒿素'
        ]
        for word in self.custom_words:
            jieba.add_word(word)
        
        # 中文停用词表
        self.chinese_stopwords = {
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', 
            '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去',
            '你', '会', '着', '没有', '看', '好', '自己', '这'
        }
        
        # 领域特定停用词（用于情感分析）
        self.domain_stopwords = {
            '出生于', '担任', '就职', '获得', '成为', '从事', '研究', 
            '发现', '发明', '提出', '建立', '创办'
        }
    
    def extract_text_from_docx(self, file_path):
        """第一阶段：格式转换与基础提取"""
        try:
            doc = Document(file_path)
            paragraphs = []
            
            # 提取段落文本
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    paragraphs.append(paragraph.text)
            
            # 合并所有段落文本
            full_text = '\n'.join(paragraphs)
            return full_text
        except Exception as e:
            print(f"Error reading {file_path}: {str(e)}")
            return ""
    
    def noise_removal(self, text):
        """去噪处理"""
        # 去除特殊符号
        text = re.sub(r'[\r\n\t]', '', text)
        
        # 去除乱码字符（简单的处理方式）
        text = re.sub(r'[^\u4e00-\u9fff\u0020-\u007e\u00a0-\u00ff]', '', text)
        
        # 去除引用标注 [1], (2020) 等
        text = re.sub(r'\[\d+\]', '', text)
        text = re.sub(r'\(\d{4}\)', '', text)
        
        # 去除URL和邮箱
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        text = re.sub(r'\S+@\S+', '', text)
        
        return text
    
    def normalize_characters(self, text):
        """全角/半角转换"""
        # 将全角字符转换为半角字符
        normalized_text = ""
        for char in text:
            # 全角空格
            if char == '\u3000':
                normalized_text += ' '
            # 全角字符转半角字符
            elif '\uff01' <= char <= '\uff5e':
                normalized_text += chr(ord(char) - 0xfee0)
            else:
                normalized_text += char
        return normalized_text
    
    def tokenize_chinese(self, text):
        """中文分词"""
        # 使用jieba进行分词
        words = jieba.lcut(text)
        return words
    
    def remove_stopwords(self, words, for_sentiment=False):
        """去除停用词"""
        filtered_words = []
        stopwords = self.chinese_stopwords.copy()
        
        # 如果是为情感分析准备，则不过滤领域停用词
        if not for_sentiment:
            stopwords.update(self.domain_stopwords)
        
        for word in words:
            # 过滤掉空字符串和停用词
            if word.strip() and word not in stopwords:
                filtered_words.append(word)
        
        return filtered_words
    
    def entity_resolution(self, words):
        """实体对齐处理"""
        # 实体映射表
        entity_mapping = {
            '玛丽·居里': '居里夫人',
            '玛丽': '居里夫人',
            '她': '居里夫人',
            '丽丝': '丽丝·迈特纳',
            '卡塔林': '卡塔林·考里科',
            '杜德纳': '杜德娜'
        }
        
        resolved_words = []
        for word in words:
            if word in entity_mapping:
                resolved_words.append(entity_mapping[word])
            else:
                resolved_words.append(word)
        
        return resolved_words
    
    def prepare_for_sentiment_analysis(self, text):
        """为情感分析准备数据"""
        # 保留标点符号（感叹号、问号等）
        # 分句处理
        sentences = re.split(r'[。！？]', text)
        cleaned_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                # 可以在这里添加更多针对情感分析的处理
                cleaned_sentences.append(sentence)
        
        return cleaned_sentences
    
    def prepare_for_association_analysis(self, text):
        """为关联分析准备数据"""
        # 分词
        words = self.tokenize_chinese(text)
        
        # 去除停用词（包括领域停用词）
        filtered_words = self.remove_stopwords(words, for_sentiment=False)
        
        # 实体对齐
        resolved_words = self.entity_resolution(filtered_words)
        
        # 保留名词为主的词汇（简化处理，实际应用中可以使用词性标注）
        noun_like_words = [word for word in resolved_words if len(word) > 1]
        
        return noun_like_words
    
    def process_single_document(self, file_path):
        """处理单个文档"""
        print(f"Processing {file_path}...")
        
        # 第一阶段：提取文本
        raw_text = self.extract_text_from_docx(file_path)
        if not raw_text:
            return None, None
        
        # 第二阶段：去噪和标准化
        cleaned_text = self.noise_removal(raw_text)
        normalized_text = self.normalize_characters(cleaned_text)
        
        # 第三阶段：分词和去停用词
        words = self.tokenize_chinese(normalized_text)
        filtered_words = self.remove_stopwords(words, for_sentiment=True)
        clean_text_for_sentiment = ' '.join(filtered_words)
        
        # 第四阶段：为不同任务定制清洗策略
        # 情感分析数据
        sentiment_data = self.prepare_for_sentiment_analysis(normalized_text)
        
        # 关联分析数据
        association_data = self.prepare_for_association_analysis(normalized_text)
        
        return sentiment_data, association_data
    
    def process_all_documents(self, folder_path):
        """处理所有文档"""
        results = {}
        
        for filename in os.listdir(folder_path):
            if filename.endswith('.docx'):
                file_path = os.path.join(folder_path, filename)
                sentiment_data, association_data = self.process_single_document(file_path)
                
                if sentiment_data is not None and association_data is not None:
                    scientist_name = filename.replace('.docx', '')
                    results[scientist_name] = {
                        'sentiment_data': sentiment_data,
                        'association_data': association_data
                    }
        
        return results

def main():
    pipeline = DataCleaningPipeline()
    
    # 处理所有文档
    folder_path = "."
    results = pipeline.process_all_documents(folder_path)
    
    # 输出结果示例
    for scientist, data in results.items():
        print(f"\n=== {scientist} ===")
        print("情感分析数据（前5句）:")
        for i, sentence in enumerate(data['sentiment_data'][:5]):
            print(f"  {i+1}. {sentence}")
        
        print("\n关联分析数据（前10个词）:")
        print("  ", data['association_data'][:10])

if __name__ == "__main__":
    main()
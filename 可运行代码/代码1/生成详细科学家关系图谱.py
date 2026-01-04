#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def load_association_data(file_path):
    """加载关联分析数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def extract_entities_from_text(text_data, scientist_name):
    """从文本数据中提取实体"""
    # 过滤掉一些常见的停用词和无关词汇
    stop_words = {'的', '了', '在', '是', '有', '和', '与', '或', '但', '而', '也', '都', '就', '把', '被', '给', '让', '使', '为', '以', '可', '到', '过', '之', '第', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '这', '那', '个', '些', '每', '各', '多', '少', '很', '太', '更', '最', '只', '还', '又', '便', '却', '如', '若', '及', '以及', '或者', '而且', '然而', '因此', '所以', '由于', '因为', '虽然', '尽管', '无论', '不但', '不仅', '而且', '同时', '此外', '另外', '还有', '再说', '接着', '然后', '最后', '终于', '结果', '总之', '总而言之', '综上所述'}
    
    # 提取可能的人名（假设长度在2-4个字符之间且不是停用词）
    potential_names = [word for word in text_data if 2 <= len(word) <= 4 and word not in stop_words]
    
    # 统计词频
    name_counter = Counter(potential_names)
    
    # 过滤出高频词作为可能的重要人物
    threshold = max(3, len(text_data) // 1000)  # 动态调整阈值
    important_names = [name for name, count in name_counter.most_common(50) if count >= threshold and name != scientist_name]
    
    return important_names[:20]  # 返回前20个最重要的名字

def build_detailed_person_graph(scientist_name, associated_persons):
    """构建详细的人物关系图谱"""
    # 创建图
    G = nx.Graph()
    
    # 添加科学家节点
    G.add_node(scientist_name, type="scientist", size=3000, color='red')
    
    # 添加关联人物节点
    for i, person in enumerate(associated_persons):
        # 根据出现频率设置节点大小
        size = max(1000, 2000 - i * 50)
        G.add_node(person, type="person", size=size, color='lightblue')
        # 添加关系边
        G.add_edge(scientist_name, person, relation="关联人物", weight=max(1, 5 - i//5))

    # 添加科学家之间的合作关系（基于共同领域）
    collaboration_relations = [
        ("屠呦呦", "居里夫人", "医学研究"),
        ("吴健雄", "何泽慧", "物理学研究"),
        ("杜德娜", "谢希德", "生物医学研究"),
        ("丽丝·迈特纳", "居里夫人", "放射性研究"),
        ("卡塔林·考里科", "杜德娜", "生物化学研究")
    ]
    
    # 如果当前科学家在合作列表中，则添加合作关系
    for scientist1, scientist2, field in collaboration_relations:
        if scientist1 == scientist_name and scientist2 in associated_persons:
            G.add_edge(scientist_name, scientist2, relation="科学合作", weight=3, field=field, color='green')
        elif scientist2 == scientist_name and scientist1 in associated_persons:
            G.add_edge(scientist_name, scientist1, relation="科学合作", weight=3, field=field, color='green')
    
    return G

def visualize_detailed_graph(G, scientist_name, output_path):
    """可视化详细人物关系图谱"""
    print(f"正在生成{scientist_name}的详细关系图谱可视化...")
    
    # 设置图形大小
    plt.figure(figsize=(16, 12))
    
    # 为节点分配位置
    pos = nx.spring_layout(G, k=3, iterations=100)
    
    # 绘制节点
    for node, attrs in G.nodes(data=True):
        nx.draw_networkx_nodes(G, pos, nodelist=[node], 
                              node_color=attrs.get('color', 'lightblue'), 
                              node_size=attrs.get('size', 1000), 
                              alpha=0.9)
    
    # 绘制边（区分关系类型）
    collaboration_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('relation') == '科学合作']
    person_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('relation') == '关联人物']
    
    # 绘制合作关系边（绿色，较粗）
    nx.draw_networkx_edges(G, pos, edgelist=collaboration_edges, 
                          width=3, alpha=0.8, edge_color='green', label='科学合作')
    
    # 绘制人物关系边（灰色，较细）
    nx.draw_networkx_edges(G, pos, edgelist=person_edges, 
                          width=1.5, alpha=0.6, edge_color='gray', label='关联人物')
    
    # 绘制标签
    labels = {}
    for node in G.nodes():
        labels[node] = node
    
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_family='sans-serif')
    
    plt.title(f"{scientist_name}详细关系图谱", fontsize=18)
    plt.legend(prop={'size': 12})
    plt.axis('off')
    
    # 保存图像
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"{scientist_name}的详细关系图谱已保存到 {output_path}")

def main():
    # 创建输出目录
    output_dir = "output/detailed_person_graphs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 获取所有关联分析文件
    association_dir = "output/association_data"
    association_files = [f for f in os.listdir(association_dir) if f.endswith('_关联分析.json')]
    
    # 为每个科学家生成详细的简化关系图谱
    for assoc_file in association_files:
        print(f"正在处理 {assoc_file}...")
        
        # 加载关联分析数据
        file_path = os.path.join(association_dir, assoc_file)
        text_data = load_association_data(file_path)
        
        # 提取科学家姓名
        scientist_name = assoc_file.replace('_关联分析.json', '')
        
        # 从文本数据中提取关联人物
        associated_persons = extract_entities_from_text(text_data, scientist_name)
        
        # 构建详细的关系图谱
        G = build_detailed_person_graph(scientist_name, associated_persons)
        
        # 生成可视化
        output_path = os.path.join(output_dir, f"{scientist_name}_详细关系图谱.png")
        visualize_detailed_graph(G, scientist_name, output_path)
    
    print(f"\n所有科学家的详细关系图谱构建完成！结果保存在 {output_dir} 目录中。")

if __name__ == "__main__":
    main()
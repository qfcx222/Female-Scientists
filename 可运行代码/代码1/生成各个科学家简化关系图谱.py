#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import networkx as nx
import matplotlib.pyplot as plt

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def extract_key_persons():
    """提取关键人物信息"""
    # 手动定义关键人物关系
    person_relations = {
        "屠呦呦": ["屠濂规", "姚仲千", "李廷钊", "楼之岑", "林达尔", "威廉姆·坎贝尔", "大村智"],
        "居里夫人": ["皮埃尔·居里", "玛丽·居里", "艾芙·居里", "伊雷娜·约里奥-居里"],
        "吴健雄": ["袁家骝", "李政道", "杨振宁", "钱学森"],
        "何泽慧": ["钱三强", "钱学森", "何泽明", "王大珩"],
        "谢希德": ["曹天钦", "黄昆", "王守武"],
        "林巧稚": ["协和医院", "北京协和医学院"],
        "杜德娜": ["查尔斯·格利斯曼", "埃马纽埃尔·卡彭蒂耶"],
        "丽丝·迈特纳": ["奥托·哈恩", "弗里茨·施特拉斯曼"],
        "卡塔林·考里科": ["德鲁·韦斯曼", "乌尔里希·瓦莱"],
        "埃达·洛夫莱斯": ["查尔斯·巴贝奇", "维多利亚女王"]
    }
    
    return person_relations

def build_individual_simplified_graph(scientist_name, persons):
    """为单个科学家构建简化的关系图谱"""
    # 创建图
    G = nx.Graph()
    
    # 添加科学家节点
    G.add_node(scientist_name, type="scientist", size=2000)
    
    # 添加人物节点和关系
    for person in persons:
        # 添加人物节点
        G.add_node(person, type="person", size=1000)
        # 添加关系边
        G.add_edge(scientist_name, person, relation="关联人物", weight=1)
    
    return G

def visualize_individual_graph(G, scientist_name, output_path):
    """可视化单个科学家的简化关系图谱"""
    print(f"正在生成{scientist_name}的简化关系图谱可视化...")
    
    # 设置图形大小
    plt.figure(figsize=(12, 10))
    
    # 为节点分配位置
    pos = nx.spring_layout(G, k=3, iterations=50)
    
    # 区分节点类型
    scientist_nodes = [n for n, attr in G.nodes(data=True) if attr.get('type') == 'scientist']
    person_nodes = [n for n, attr in G.nodes(data=True) if attr.get('type') == 'person']
    
    # 绘制节点
    nx.draw_networkx_nodes(G, pos, nodelist=scientist_nodes, 
                          node_color='red', node_size=3000, alpha=0.9, label='科学家')
    nx.draw_networkx_nodes(G, pos, nodelist=person_nodes, 
                          node_color='lightblue', node_size=1500, alpha=0.7, label='相关人物')
    
    # 绘制边
    nx.draw_networkx_edges(G, pos, width=2, alpha=0.6, edge_color='gray')
    
    # 绘制标签
    labels = {}
    for node in G.nodes():
        labels[node] = node
    
    nx.draw_networkx_labels(G, pos, labels, font_size=12, font_family='sans-serif')
    
    plt.title(f"{scientist_name}简化关系图谱", fontsize=16)
    plt.legend(prop={'size': 12})
    plt.axis('off')
    
    # 保存图像
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"{scientist_name}的简化关系图谱已保存到 {output_path}")

def main():
    # 创建输出目录
    output_dir = "output/individual_simplified_graphs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 获取关键人物关系
    person_relations = extract_key_persons()
    
    # 为每个科学家生成单独的简化关系图谱
    for scientist_name, persons in person_relations.items():
        print(f"正在处理 {scientist_name}...")
        
        # 构建单个科学家的关系图谱
        G = build_individual_simplified_graph(scientist_name, persons)
        
        # 生成可视化
        output_path = os.path.join(output_dir, f"{scientist_name}_简化关系图谱.png")
        visualize_individual_graph(G, scientist_name, output_path)
    
    print(f"\n所有科学家的简化关系图谱构建完成！结果保存在 {output_dir} 目录中。")

if __name__ == "__main__":
    main()
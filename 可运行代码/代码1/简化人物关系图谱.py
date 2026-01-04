#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import pandas as pd
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def load_association_data(file_path):
    """加载关联分析数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

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

def build_simplified_person_graph():
    """构建简化的人物关系图谱"""
    # 创建图
    G = nx.Graph()
    
    # 获取关键人物关系
    person_relations = extract_key_persons()
    
    # 添加科学家节点
    scientists = list(person_relations.keys())
    for scientist in scientists:
        G.add_node(scientist, type="scientist", size=2000)
    
    # 添加人物节点和关系
    for scientist, persons in person_relations.items():
        for person in persons:
            # 添加人物节点
            G.add_node(person, type="person", size=1000)
            # 添加关系边
            G.add_edge(scientist, person, relation="关联人物", weight=1)
    
    # 添加科学家之间的合作关系（基于共同领域）
    collaboration_relations = [
        ("屠呦呦", "居里夫人", "医学研究"),
        ("吴健雄", "何泽慧", "物理学研究"),
        ("杜德娜", "谢希德", "生物医学研究"),
        ("丽丝·迈特纳", "居里夫人", "放射性研究"),
        ("卡塔林·考里科", "杜德娜", "生物化学研究")
    ]
    
    for scientist1, scientist2, field in collaboration_relations:
        G.add_edge(scientist1, scientist2, relation="科学合作", weight=2, field=field)
    
    return G, scientists

def visualize_simplified_graph(G, scientists, output_path="output/simplified_person_graph.png"):
    """可视化简化人物关系图谱"""
    print("正在生成简化人物关系图谱可视化...")
    
    # 设置图形大小
    plt.figure(figsize=(20, 15))
    
    # 为节点分配位置
    pos = nx.spring_layout(G, k=2, iterations=50)
    
    # 区分节点类型
    scientist_nodes = [n for n, attr in G.nodes(data=True) if attr.get('type') == 'scientist']
    person_nodes = [n for n, attr in G.nodes(data=True) if attr.get('type') == 'person']
    
    # 绘制节点
    nx.draw_networkx_nodes(G, pos, nodelist=scientist_nodes, 
                          node_color='red', node_size=3000, alpha=0.9, label='科学家')
    nx.draw_networkx_nodes(G, pos, nodelist=person_nodes, 
                          node_color='lightblue', node_size=1500, alpha=0.7, label='相关人物')
    
    # 绘制边（区分关系类型）
    collaboration_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('relation') == '科学合作']
    person_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('relation') == '关联人物']
    
    # 绘制合作关系边（绿色，较粗）
    nx.draw_networkx_edges(G, pos, edgelist=collaboration_edges, 
                          width=3, alpha=0.7, edge_color='green', label='科学合作')
    
    # 绘制人物关系边（灰色，较细）
    nx.draw_networkx_edges(G, pos, edgelist=person_edges, 
                          width=1, alpha=0.5, edge_color='gray', label='关联人物')
    
    # 绘制标签
    labels = {}
    for node in G.nodes():
        labels[node] = node
    
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_family='sans-serif')
    
    plt.title("女科学家简化人物关系图谱", fontsize=20)
    plt.legend(prop={'size': 12})
    plt.axis('off')
    
    # 保存图像
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"简化人物关系图谱已保存到 {output_path}")

def export_simplified_graph_data(G, output_path="output/simplified_person_graph_data.json"):
    """导出简化人物关系图数据为JSON格式"""
    graph_data = {
        "nodes": [],
        "edges": []
    }
    
    # 添加节点
    for node, attrs in G.nodes(data=True):
        graph_data["nodes"].append({
            "id": node,
            "type": attrs.get("type", "unknown"),
            "size": attrs.get("size", 1000)
        })
    
    # 添加边
    for source, target, attrs in G.edges(data=True):
        edge_data = {
            "source": source,
            "target": target,
            "relation": attrs.get("relation", "")
        }
        if "weight" in attrs:
            edge_data["weight"] = attrs["weight"]
        if "field" in attrs:
            edge_data["field"] = attrs["field"]
        graph_data["edges"].append(edge_data)
    
    # 保存到文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, ensure_ascii=False, indent=2)
    
    print(f"简化人物关系图数据已导出到 {output_path}")

def generate_simplified_statistics(G, scientists):
    """生成简化人物关系图谱统计信息"""
    print("\n=== 简化人物关系图谱统计信息 ===")
    print(f"节点总数: {G.number_of_nodes()}")
    print(f"边总数: {G.number_of_edges()}")
    print(f"科学家数量: {len(scientists)}")
    
    # 计算每个科学家关联的人物数
    print("\n每个科学家关联的人物数:")
    for scientist in scientists:
        neighbors = list(G.neighbors(scientist))
        person_count = len([n for n in neighbors if G.nodes[n].get('type') == 'person'])
        scientist_count = len([n for n in neighbors if G.nodes[n].get('type') == 'scientist'])
        print(f"  {scientist}: {person_count}个关联人物, {scientist_count}个科学家合作")

def main():
    # 创建输出目录
    output_dir = "output/simplified_person_graph"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 构建简化人物关系图谱
    print("正在构建简化人物关系图谱...")
    G, scientists = build_simplified_person_graph()
    
    # 生成统计信息
    generate_simplified_statistics(G, scientists)
    
    # 可视化简化人物关系图谱
    visualize_path = os.path.join(output_dir, "简化人物关系图谱.png")
    visualize_simplified_graph(G, scientists, visualize_path)
    
    # 导出图数据
    graph_data_path = os.path.join(output_dir, "简化人物关系图数据.json")
    export_simplified_graph_data(G, graph_data_path)
    
    print(f"\n简化人物关系图谱构建完成！结果保存在 {output_dir} 目录中。")

if __name__ == "__main__":
    main()
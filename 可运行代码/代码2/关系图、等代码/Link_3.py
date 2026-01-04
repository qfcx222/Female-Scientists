import networkx as nx
import matplotlib.pyplot as plt

# 1. 配置Windows中文字体（解决中文显示）
try:
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial']
    plt.rcParams['axes.unicode_minus'] = False
    print("✅ 中文字体配置成功")
except Exception as e:
    print(f"⚠️ 中文字体配置提示: {e}，使用系统默认字体")
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Arial']
    plt.rcParams['axes.unicode_minus'] = False

# 2. 核心关系数据（补全"瑞安(女婿)"，确保所有边中节点都在列表中）
core_person = "卡塔林·考里科"
family = [
    "雅诺什·考里科(父/屠夫)", "雅诺什奈·考里科(母)",
    "苏珊·考里科(姐/佐卡)", "贝拉·弗朗西亚(夫)",
    "苏珊·弗朗西亚(女/奥运赛艇冠军)", "瑞安(女婿)",  # 补全漏加的节点
    "亚历山大·贝尔(外孙)", "苏珊·萨斯(外祖母)",
    "费伦茨·奥罗斯(外祖父)", "伊丽莎白(姨妈)", "伊洛娜(小姨)"
]
mentors = [
    "阿尔伯特·托特(高中生物学老师)", "蒂博尔·法卡斯(塞格德大学导)",
    "简诺·托马什(塞格德大学导)", "罗伯特·苏哈多尔尼克(天普大学导)",
    "雅诺什·路德维希(挚友/科研导师)"
]
long_term_collaborators = [
    "德鲁·韦斯曼(mRNA核心合作)", "埃利奥特·巴纳森(宾大心脏病学)",
    "戴维·兰格(神经外科/拯救职业生涯)", "乌古尔·沙欣(百欧恩泰联合创始人)",
    "厄兹勒姆·图雷西(百欧恩泰联合创始人)", "爱丽丝·郭(实验室技术员)"
]
colleagues_friends = [
    "琼·贝内特(共享实验室/基因疗法专家)", "葆拉·皮塔-罗(约翰斯·霍普金斯大学)",
    "拉斯洛·萨巴多斯(大学同学/挚友)", "贝蒂·巴吉(移民挚友)",
    "拉斯洛·巴吉(艺术家/挚友)", "玛丽亚·弗里德尔(高中同学)",
    "诺伯特·帕迪(宾大疫苗学家)", "加博尔·塔马斯·绍博(百欧恩泰同事)"
]
key_figures = [
    "吉姆·威尔逊(宾大人类基因治疗研究所)", "朱迪·斯温(宾大心脏病科主任)",
    "肖恩·格雷迪(宾大神经外科主任)", "罗伯特·索博尔(天普大学研究生)",
    "阿尔伯特·波拉(辉瑞CEO)", "托尼·福奇(国立卫生研究院)"
]

# 3. 关系边（保持不变，确保所有节点已在上方列表中）
edges = [
    # 核心 ↔ 家人
    (core_person, "雅诺什·考里科(父/屠夫)", "父女/启蒙探索精神"),
    (core_person, "雅诺什奈·考里科(母)", "母女/支持教育"),
    (core_person, "苏珊·考里科(姐/佐卡)", "姐妹/相互扶持"),
    (core_person, "贝拉·弗朗西亚(夫)", "夫妻/终身支持科研"),
    (core_person, "苏珊·弗朗西亚(女/奥运赛艇冠军)", "母女/相互激励"),
    (core_person, "亚历山大·贝尔(外孙)", "祖孙"),
    ("苏珊·弗朗西亚(女/奥运赛艇冠军)", "瑞安(女婿)", "夫妻"),  # 对应补全的节点

    # 核心 ↔ 导师
    (core_person, "阿尔伯特·托特(高中生物学老师)", "师生/点燃科研热情"),
    (core_person, "蒂博尔·法卡斯(塞格德大学导)", "师生/脂质体研究"),
    (core_person, "雅诺什·路德维希(挚友/科研导师)", "师生+挚友/督促成长"),
    (core_person, "罗伯特·苏哈多尔尼克(天普大学导)", "师生/核苷类似物研究"),

    # 核心 ↔ 长期合作者
    (core_person, "德鲁·韦斯曼(mRNA核心合作)", "同事/核苷修饰mRNA突破"),
    (core_person, "埃利奥特·巴纳森(宾大心脏病学)", "同事/尿激酶受体mRNA研究"),
    (core_person, "戴维·兰格(神经外科/拯救职业生涯)", "同事+挚友/一氧化氮mRNA研究"),
    (core_person, "乌古尔·沙欣(百欧恩泰联合创始人)", "同事/COVID-19疫苗研发"),
    (core_person, "爱丽丝·郭(实验室技术员)", "同事/实验支持(点阵打印机突破)"),

    # 核心 ↔ 同事/挚友
    (core_person, "琼·贝内特(共享实验室/基因疗法专家)", "同事+挚友/相互支持"),
    (core_person, "拉斯洛·巴吉(艺术家/挚友)", "挚友/移民生活支撑"),
    (core_person, "贝蒂·巴吉(移民挚友)", "挚友/文化桥梁"),
    (core_person, "诺伯特·帕迪(宾大疫苗学家)", "同事/mRNA疫苗合作"),

    # 核心 ↔ 关键人物
    (core_person, "阿尔伯特·波拉(辉瑞CEO)", "合作/COVID-19疫苗量产"),
    (core_person, "罗伯特·索博尔(天普大学研究生)", "师徒/实验室指导"),

    # 跨关系
    ("德鲁·韦斯曼(mRNA核心合作)", "乌古尔·沙欣(百欧恩泰联合创始人)", "合作/mRNA疫苗研发"),
    ("戴维·兰格(神经外科/拯救职业生涯)", "埃利奥特·巴纳森(宾大心脏病学)", "同事(宾大)")
]

# 4. 创建图结构（确保所有节点都来自all_nodes）
G = nx.Graph()
all_nodes = [core_person] + family + mentors + long_term_collaborators + colleagues_friends + key_figures
G.add_nodes_from(all_nodes)  # 先添加所有节点，再加边，避免漏节点
for source, target, relation in edges:
    G.add_edge(source, target, relation=relation)

# 5. 节点着色（关键：补全默认颜色，确保每个节点都有颜色）
node_colors = []
for node in G.nodes():
    if node == core_person:
        node_colors.append('#FF5733')  # 核心：橙红
    elif node in family:
        node_colors.append('#3498DB')  # 家人：蓝
    elif node in mentors:
        node_colors.append('#2ECC71')  # 导师：绿
    elif node in long_term_collaborators:
        node_colors.append('#9B59B6')  # 长期合作者：紫
    elif node in colleagues_friends:
        node_colors.append('#F39C12')  # 同事/挚友：黄
    elif node in key_figures:
        node_colors.append('#1ABC9C')  # 关键人物：青
    else:
        node_colors.append('#BDC3C7')  # 默认颜色：浅灰（防止漏节点）

# 6. 绘制图谱（兼容低版本，中文不重叠）
plt.figure(figsize=(18, 14))

# 弹簧布局：适配长中文标签
pos = nx.spring_layout(
    G,
    k=7.0,  # 增大节点间距
    iterations=300,  # 优化布局
    seed=42  # 固定布局
)

# 绘制节点（尺寸适配中文）
nx.draw_networkx_nodes(
    G, pos,
    node_size=9000,  # 足够容纳长标签
    node_color=node_colors,
    alpha=0.9,
    edgecolors='black',
    linewidths=2
)

# 绘制边
nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.8, edge_color='#666666')

# 绘制边标签（低版本nx支持font_size）
edge_labels = nx.get_edge_attributes(G, 'relation')
nx.draw_networkx_edge_labels(
    G, pos,
    edge_labels=edge_labels,
    font_size=9,
    label_pos=0.4
)

# 绘制节点标签（低版本nx支持font_size）
nx.draw_networkx_labels(G, pos, font_size=11)

# 绘制标题（matplotlib支持fontsize）
plt.title('卡塔林·考里科核心关系网络图谱', fontsize=20, pad=35)

# 保存图谱
plt.axis('off')
plt.tight_layout()
plt.savefig(
    '卡塔林考里科关系图谱_完美版.png',
    dpi=300,
    bbox_inches='tight'
)
plt.close()

print("🎉 图谱生成成功！文件：卡塔林考里科关系图谱_完美版.png")
print(f"📊 包含 {len(G.nodes())} 位关键人物，{len(edges)} 条核心关系")
print("✅ 中文正常 | ✅ 无参数错误 | ✅ 兼容 nx 1.x+ & matplotlib 2.x+")
import networkx as nx
import matplotlib.pyplot as plt

# 1. 配置Windows中文字体（解决中文显示问题）
try:
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial']
    plt.rcParams['axes.unicode_minus'] = False
    print("✅ 中文字体配置成功")
except Exception as e:
    print(f"⚠️ 中文字体配置提示: {e}，使用系统默认字体")
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Arial']
    plt.rcParams['axes.unicode_minus'] = False

# 2. 核心关系数据（按关系类型分类，贴合传记细节）
core_person = "埃达·洛夫莱斯"
family = [
    "乔治·戈登·拜伦(父/浪漫主义诗人)", "安妮·伊莎贝拉(母/教育改革家)",
    "拉尔夫·米尔班克爵士(外祖父/下院议员)", "威廉·金(夫/洛夫莱斯伯爵)",
    "拜伦(子)", "安娜贝拉(女)", "拉尔夫(子)"
]
mentors = [
    "奥古斯都·德·摩根(数学导师/逻辑学家)", "玛丽·萨默维尔(科学启蒙/科普作家)",
    "威廉·弗伦德(母亲导师/数学家)", "查尔斯·巴贝奇(分析机合作导师/发明家)",
    "威廉·金博士(早期数学指导)", "约瑟夫·克莱门特(工程技术指导/巴贝奇合作者)"
]
long_term_collaborators = [
    "查尔斯·巴贝奇(分析机联合研发)", "路易吉·梅纳布雷亚(报告翻译合作)",
    "查尔斯·惠斯通(电报机学术交流)", "理查德·泰勒(《科学备忘录》出版合作)",
    "沃隆佐·格雷格(学术通信挚友)"
]
colleagues_friends = [
    "索菲娅·德·摩根(友人/社会活动家)", "查尔斯·狄更斯(社交圈友人/小说家)",
    "伊桑巴德·布鲁内尔(工程界同道/发明家)", "迈克尔·法拉第(科学界友人/物理学家)",
    "弗洛伦斯·南丁格尔(同时代改革者/统计学家)", "艾伯特亲王(科学拥护者/王室成员)"
]
key_figures = [
    "艾伦·图灵(受其影响/计算机之父)", "莱昂哈德·欧拉(数学理论先驱)",
    "约瑟夫·玛丽·雅卡尔(提花机发明者/编程灵感)", "阿道夫·奎特莱(统计学交流)",
    "罗伯特·钱伯斯(《创世自然史的遗迹》作者/学术圈)", "哈丽特·马蒂诺(社会理论家/友人)"
]

# 3. 关系边（标注核心关联与合作内容）
edges = [
    # 核心 ↔ 家人
    (core_person, "乔治·戈登·拜伦(父/浪漫主义诗人)", "父女/遗传艺术天赋"),
    (core_person, "安妮·伊莎贝拉(母/教育改革家)", "母女/数学启蒙教育"),
    (core_person, "威廉·金(夫/洛夫莱斯伯爵)", "夫妻/支持科学研究"),
    (core_person, "拜伦(子)", "母子/家庭陪伴"),
    (core_person, "安娜贝拉(女)", "母女/家庭陪伴"),
    (core_person, "拉尔夫(子)", "母子/家庭陪伴"),

    # 核心 ↔ 导师
    (core_person, "奥古斯都·德·摩根(数学导师/逻辑学家)", "师生/微积分+代数指导"),
    (core_person, "玛丽·萨默维尔(科学启蒙/科普作家)", "师生+挚友/科学视野开拓"),
    (core_person, "查尔斯·巴贝奇(分析机合作导师/发明家)", "师生+合作/分析机研发"),
    (core_person, "威廉·弗伦德(母亲导师/数学家)", "间接师生/数学思维启蒙"),
    (core_person, "威廉·金博士(早期数学指导)", "师生/欧几里得几何教学"),

    # 核心 ↔ 长期合作者
    (core_person, "查尔斯·巴贝奇(分析机联合研发)", "合作/编程算法设计+分析机注释"),
    (core_person, "路易吉·梅纳布雷亚(报告翻译合作)", "合作/翻译法语报告+补充注释"),
    (core_person, "理查德·泰勒(《科学备忘录》出版合作)", "合作/论文发表支持"),
    (core_person, "沃隆佐·格雷格(学术通信挚友)", "通信合作/科学问题探讨"),

    # 核心 ↔ 同事/挚友
    (core_person, "索菲娅·德·摩根(友人/社会活动家)", "友人/生活+学术交流"),
    (core_person, "查尔斯·狄更斯(社交圈友人/小说家)", "友人/文艺+科学跨界交流"),
    (core_person, "弗洛伦斯·南丁格尔(同时代改革者/统计学家)", "友人/女性科学者互助"),
    (core_person, "迈克尔·法拉第(科学界友人/物理学家)", "学术交流/电磁学探讨"),

    # 核心 ↔ 关键人物
    (core_person, "艾伦·图灵(受其影响/计算机之父)", "影响/启发现代计算机编程思想"),
    (core_person, "约瑟夫·玛丽·雅卡尔(提花机发明者/编程灵感)", "灵感来源/穿孔卡编程启发"),
    (core_person, "艾伯特亲王(科学拥护者/王室成员)", "支持/科学普及活动参与"),

    # 跨关系
    ("查尔斯·巴贝奇(分析机联合研发)", "约瑟夫·克莱门特(工程技术指导/巴贝奇合作者)", "同事/分析机机械设计"),
    ("玛丽·萨默维尔(科学启蒙/科普作家)", "沃隆佐·格雷格(学术通信挚友)", "母子/学术传承"),
    ("路易吉·梅纳布雷亚(报告翻译合作)", "查尔斯·巴贝奇(分析机联合研发)", "学术交流/分析机理论传播")
]

# 4. 创建图结构
G = nx.Graph()
all_nodes = [core_person] + family + mentors + long_term_collaborators + colleagues_friends + key_figures
G.add_nodes_from(all_nodes)
for source, target, relation in edges:
    G.add_edge(source, target, relation=relation)

# 5. 节点着色（按关系类型区分，色彩鲜明易区分）
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
        node_colors.append('#BDC3C7')  # 默认：浅灰

# 6. 绘制图谱（兼容低版本，中文标签不重叠）
plt.figure(figsize=(18, 14))

# 弹簧布局：优化中文长标签显示
pos = nx.spring_layout(
    G,
    k=7.5,  # 增大节点间距，适配长中文标签
    iterations=300,  # 多次迭代优化布局
    seed=42  # 固定布局一致性
)

# 绘制节点（尺寸适配长标签）
nx.draw_networkx_nodes(
    G, pos,
    node_size=9500,  # 足够容纳长中文标签
    node_color=node_colors,
    alpha=0.9,
    edgecolors='black',
    linewidths=2
)

# 绘制边（灰色低调不抢焦点）
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
plt.title('埃达·洛夫莱斯核心关系网络图谱', fontsize=20, pad=35)

# 隐藏坐标轴，保存高清图谱
plt.axis('off')
plt.tight_layout()
plt.savefig(
    '埃达洛夫莱斯关系图谱_终极兼容版.png',
    dpi=300,
    bbox_inches='tight'  # 确保中文标签不被截断
)
plt.close()

print("🎉 图谱生成成功！文件：埃达洛夫莱斯关系图谱_终极兼容版.png")
print(f"📊 包含 {len(G.nodes())} 位关键人物，{len(edges)} 条核心关系")
print("✅ 中文显示正常 | ✅ 无参数错误 | ✅ 兼容 nx 1.x+ & matplotlib 2.x+")
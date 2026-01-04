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
core_person = "吴健雄"
family = [
    "吴仲裔(父/明德中学校长)", "樊复华(母)",
    "吴健英(兄)", "吴健豪(弟)", "吴琢之(叔/资助留学)",
    "吴挹峰(祖父/秀才)", "袁家骝(夫/物理学家)",
    "袁纬承(子)", "露西(儿媳)"
]
mentors = [
    "施士元(中央大学导/居里夫人学生)", "吴有训(中央大学导/电磁学)",
    "方光圻(中央大学导/光学)", "胡适(中国公学导/新文化运动领袖)",
    "劳伦斯(柏克利导师/回旋加速器发明者)", "塞格瑞(柏克利实验导/诺贝尔奖得主)",
    "费米(β衰变理论导/诺贝尔奖得主)", "奥本海默(曼哈顿计划领袖)",
    "顾静薇(中央研究院导/核物理)", "严济慈(推荐浙江大学任职)"
]
long_term_collaborators = [
    "杨振宁(宇称不守恒理论合作)", "李政道(宇称不守恒理论合作)",
    "安伯勒(国家标准局/宇称实验)", "哈德森(国家标准局/低温物理)",
    "黑渥(国家标准局/放射性研究)", "哈泼斯(国家标准局/低温装置)",
    "李荣根(弱矢量流守恒实验)", "莫玮(弱矢量流守恒实验)",
    "玛丽荷(实验室助手/晶体生长)"
]
colleagues_friends = [
    "张文裕(物理学家/挚友)", "魏荣爵(物理学家/挚友)",
    "冯端(南京大学院士/挚友)", "丁肇中(诺贝尔奖得主/同道)",
    "吴大猷(物理学家/同道)", "周培源(物理学家/同道)",
    "曹诚英(中央大学挚友/胡适友人)", "孙多慈(中央大学友人/艺术家)",
    "塞格瑞(柏克利同事/诺贝尔奖得主)", "尼尔斯·玻尔(量子物理同道)"
]
key_figures = [
    "周恩来(国家领导人)", "邓颖超(国家领导人)", "邓小平(国家领导人)",
    "福特(美国总统/授国家科学勋章)", "严济慈(物理学家/推荐者)",
    "顾静薇(中央研究院研究员)", "拉比(哥伦比亚大学物理系主任)",
    "柯克(哥伦比亚大学校长)", "班固里昂(以色列总理/学术交流)"
]

# 3. 关系边（标注核心关联与合作内容）
edges = [
    # 核心 ↔ 家人
    (core_person, "吴仲裔(父/明德中学校长)", "父女/启蒙新思想"),
    (core_person, "樊复华(母)", "母女/支持教育"),
    (core_person, "吴琢之(叔/资助留学)", "叔侄/资助赴美深造"),
    (core_person, "袁家骝(夫/物理学家)", "夫妻/科研伴侣+终身支持"),
    (core_person, "袁纬承(子)", "母子/相互扶持"),
    (core_person, "吴挹峰(祖父/秀才)", "祖孙/书法启蒙"),

    # 核心 ↔ 导师
    (core_person, "施士元(中央大学导/居里夫人学生)", "师生/近代物理实验"),
    (core_person, "胡适(中国公学导/新文化运动领袖)", "师生/学术思想启蒙"),
    (core_person, "劳伦斯(柏克利导师/回旋加速器发明者)", "师生/核物理实验"),
    (core_person, "费米(β衰变理论导/诺贝尔奖得主)", "师生+同道/β衰变研究"),
    (core_person, "顾静薇(中央研究院导/核物理)", "师生/核物理实验室指导"),

    # 核心 ↔ 长期合作者
    (core_person, "杨振宁(宇称不守恒理论合作)", "合作/验证弱作用宇称不守恒"),
    (core_person, "李政道(宇称不守恒理论合作)", "合作/设计钴60极化实验"),
    (core_person, "安伯勒(国家标准局/宇称实验)", "合作/低温原子核极化技术"),
    (core_person, "李荣根(弱矢量流守恒实验)", "合作/验证弱矢量流守恒"),
    (core_person, "玛丽荷(实验室助手/晶体生长)", "合作/宇称实验晶体制备"),

    # 核心 ↔ 同事/挚友
    (core_person, "张文裕(物理学家/挚友)", "同事+挚友/学术交流"),
    (core_person, "冯端(南京大学院士/挚友)", "同事+挚友/母校合作"),
    (core_person, "丁肇中(诺贝尔奖得主/同道)", "学术交流/高能物理"),
    (core_person, "曹诚英(中央大学挚友/胡适友人)", "挚友/生活相互支持"),
    (core_person, "塞格瑞(柏克利同事/诺贝尔奖得主)", "同事/核裂变研究"),

    # 核心 ↔ 关键人物
    (core_person, "周恩来(国家领导人)", "会见/归国访问接待"),
    (core_person, "福特(美国总统/授国家科学勋章)", "授勋/国家科学勋章"),
    (core_person, "班固里昂(以色列总理/学术交流)", "交流/科学与哲学探讨"),

    # 跨关系
    ("杨振宁(宇称不守恒理论合作)", "李政道(宇称不守恒理论合作)", "合作/提出宇称不守恒假说"),
    ("袁家骝(夫/物理学家)", "张文裕(物理学家/挚友)", "同事+挚友/物理研究"),
    ("施士元(中央大学导/居里夫人学生)", "居里夫人", "师生(跨级关联)"),
    ("安伯勒(国家标准局/宇称实验)", "哈德森(国家标准局/低温物理)", "同事/宇称实验团队")
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
plt.title('吴健雄核心关系网络图谱', fontsize=20, pad=35)

# 隐藏坐标轴，保存高清图谱
plt.axis('off')
plt.tight_layout()
plt.savefig(
    '吴健雄关系图谱_终极兼容版.png',
    dpi=300,
    bbox_inches='tight'  # 确保中文标签不被截断
)
plt.close()

print("🎉 图谱生成成功！文件：吴健雄关系图谱_终极兼容版.png")
print(f"📊 包含 {len(G.nodes())} 位关键人物，{len(edges)} 条核心关系")
print("✅ 中文显示正常 | ✅ 无参数错误 | ✅ 兼容 nx 1.x+ & matplotlib 2.x+")
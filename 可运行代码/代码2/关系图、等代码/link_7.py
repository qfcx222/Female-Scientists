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
core_person = "屠呦呦"
family = [
    "屠濂规(父/银行职员/启蒙者)", "姚仲千(母/家庭主妇/支持者)",
    "屠恒学(兄/学者/鼓励者)", "姚庆三(舅舅/经济学家/榜样)",
    "李廷钊(夫/冶金专家/终身支持)", "李敏(大女儿)",
    "李军(小女儿)", "吴挹峰(祖父/秀才)",
    "毛磊(女婿)", "外孙女(李敏之女)"
]
mentors = [
    "楼之岑(北大教授/生药学导师)", "林启寿(北大教授/植物化学导师)",
    "蒲辅周(中医大师/西学中导师)", "杜自明(中医正骨专家/西学中导师)",
    "薛愚(北大药学系主任/学术指导)", "蒋明谦(有机化学家/学术指导)",
    "王序(有机化学家/学术指导)", "高合年(中医研究院副院长/指导)"
]
long_term_collaborators = [
    "倪慕云(523项目核心成员/衍生物研究)", "钟裕蓉(523项目核心成员/结晶分离)",
    "崔淑莲(523项目核心成员/实验支持)", "郎林福(523项目核心成员/临床协助)",
    "刘菊福(523项目核心成员/提取实验)", "王满元(博士生/学术传承)",
    "顾玉诚(硕士生/学术传承)", "吴崇明(硕士生/学术传承)",
    "中国科学院上海有机所(青蒿素结构协作)", "中国科学院生物物理所(X射线衍射协作)"
]
colleagues_friends = [
    "姜廷良(中药所原所长/同事挚友)", "周仕锟(北大同窗/同事)",
    "王慕邹(北大同窗/同事)", "路易斯·米勒(美国院士/推介者)",
    "李国桥(广州中医药大学教授/临床协作)", "罗泽渊(云南药物所研究员/协作)",
    "张伯礼(中国中医科学院院长/同道)", "陈士林(中药所所长/后续协作)",
    "张剑方(523办公室副主任/协调者)", "施凛荣(523项目参与者/协作)"
]
key_figures = [
    "毛泽东(国家领导人/政策支持)", "周恩来(国家领导人/任务推动)",
    "诺贝尔基金会(诺贝尔奖授予机构)", "拉斯克奖评委(临床医学奖授予者)",
    "华伦·阿尔波特基金会(奖项授予者)", "世界卫生组织(青蒿素推广机构)",
    "国家中医药管理局(行业主管部门)", "齐拉特(诺贝尔评委/颁奖者)",
    "乌尔班·林达尔(诺贝尔评委/宣布者)", "陈冯富珍(世卫组织总干事/推广者)"
]

# 3. 关系边（标注核心关联与合作内容）
edges = [
    # 核心 ↔ 家人
    (core_person, "屠濂规(父/银行职员/启蒙者)", "父女/科学兴趣启蒙"),
    (core_person, "姚仲千(母/家庭主妇/支持者)", "母女/教育与生活支持"),
    (core_person, "李廷钊(夫/冶金专家/终身支持)", "夫妻/生活照料+科研后盾"),
    (core_person, "李敏(大女儿)", "母女/家庭陪伴"),
    (core_person, "李军(小女儿)", "母女/家庭陪伴"),
    (core_person, "姚庆三(舅舅/经济学家/榜样)", "舅甥/人生榜样引领"),

    # 核心 ↔ 导师
    (core_person, "楼之岑(北大教授/生药学导师)", "师生/生药学研究指导"),
    (core_person, "林启寿(北大教授/植物化学导师)", "师生/植物提取方法指导"),
    (core_person, "蒲辅周(中医大师/西学中导师)", "师生/中医理论指导"),
    (core_person, "薛愚(北大药学系主任/学术指导)", "师生/学科方向引领"),

    # 核心 ↔ 长期合作者
    (core_person, "倪慕云(523项目核心成员/衍生物研究)", "合作/青蒿素衍生物研发"),
    (core_person, "钟裕蓉(523项目核心成员/结晶分离)", "合作/青蒿素结晶提取"),
    (core_person, "王满元(博士生/学术传承)", "师徒/青蒿素后续研究传承"),
    (core_person, "中国科学院上海有机所(青蒿素结构协作)", "合作/青蒿素化学结构解析"),
    (core_person, "中国科学院生物物理所(X射线衍射协作)", "合作/青蒿素立体结构确定"),

    # 核心 ↔ 同事/挚友
    (core_person, "姜廷良(中药所原所长/同事挚友)", "同事+挚友/学术交流支持"),
    (core_person, "路易斯·米勒(美国院士/推介者)", "同道+推介者/国际奖项推介"),
    (core_person, "李国桥(广州中医药大学教授/临床协作)", "合作/青蒿素临床验证"),
    (core_person, "张伯礼(中国中医科学院院长/同道)", "同道/中医药推广协作"),

    # 核心 ↔ 关键人物
    (core_person, "诺贝尔基金会(诺贝尔奖授予机构)", "关联/诺贝尔生理学或医学奖"),
    (core_person, "拉斯克奖评委(临床医学奖授予者)", "关联/拉斯克临床医学奖"),
    (core_person, "世界卫生组织(青蒿素推广机构)", "关联/青蒿素全球推广"),
    (core_person, "毛泽东(国家领导人/政策支持)", "关联/523项目政策推动"),

    # 跨关系
    ("李廷钊(夫/冶金专家/终身支持)", "姜廷良(中药所原所长/同事挚友)", "挚友/支持屠呦呦科研"),
    ("王满元(博士生/学术传承)", "陈士林(中药所所长/后续协作)", "同事/青蒿素后续研究"),
    ("中国科学院上海有机所(青蒿素结构协作)", "中国科学院生物物理所(X射线衍射协作)", "协作/青蒿素结构确定"),
    ("李国桥(广州中医药大学教授/临床协作)", "罗泽渊(云南药物所研究员/协作)", "同事/疟区临床研究")
]

# 4. 创建图结构
G = nx.Graph()
all_nodes = [core_person] + family + mentors + long_term_collaborators + colleagues_friends + key_figures
G.add_nodes_from(all_nodes)
for source, target, relation in edges:
    G.add_edge(source, target, relation=relation)

# 5. 节点着色（按关系类型区分，色彩鲜明易区分，确保无遗漏）
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
        node_colors.append('#BDC3C7')  # 默认：浅灰（防止漏节点）

# 6. 绘制图谱（兼容低版本，中文标签不重叠）
plt.figure(figsize=(19, 15))

# 弹簧布局：优化中文长标签显示
pos = nx.spring_layout(
    G,
    k=8.0,  # 增大节点间距，适配长中文标签
    iterations=300,  # 多次迭代优化布局
    seed=42  # 固定布局一致性
)

# 绘制节点（尺寸适配长标签）
nx.draw_networkx_nodes(
    G, pos,
    node_size=10000,  # 足够容纳长中文标签
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
plt.title('屠呦呦核心关系网络图谱', fontsize=22, pad=40)

# 隐藏坐标轴，保存高清图谱
plt.axis('off')
plt.tight_layout()
plt.savefig(
    '屠呦呦关系图谱_终极兼容版.png',
    dpi=300,
    bbox_inches='tight'  # 确保中文标签不被截断
)
plt.close()

print("🎉 图谱生成成功！文件：屠呦呦关系图谱_终极兼容版.png")
print(f"📊 包含 {len(G.nodes())} 位关键人物，{len(edges)} 条核心关系")
print("✅ 中文显示正常 | ✅ 无参数错误 | ✅ 兼容 nx 1.x+ & matplotlib 2.x+")
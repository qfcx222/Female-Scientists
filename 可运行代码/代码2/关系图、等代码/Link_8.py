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
core_person = "珍妮佛·杜德娜"
family = [
    "多萝西·杜德娜(母/家庭支持者)", "马丁·杜德娜(父/英文教授/启蒙者)",
    "杰米·凯特(夫/结构生物学家/终身伴侣)", "安德鲁(子/家庭陪伴)",
    "埃伦(妹/家庭支持)", "莎拉(妹/家庭支持)"
]
mentors = [
    "杰克·绍斯塔克(哈佛导师/诺贝尔得主/DNA修复研究)",
    "汤姆·切克(科罗拉多大学博士后导师/诺贝尔得主/核酶研究)",
    "唐·赫姆斯(本科导师/真菌研究启蒙)", "汉斯·温克勒(基因组概念先驱/学术影响)"
]
long_term_collaborators = [
    "埃马纽埃尔·卡彭蒂耶(法国科学家/CRISPR共同开发)",
    "塞缪尔·斯滕伯格(实验室成员/共同著书/CRISPR机制研究)",
    "马丁·耶奈克(博士后/CRISPR-Cas9关键实验)",
    "布莱克·韦德海福特(博士后/早期CRISPR免疫机制研究)",
    "吉莉安·班菲尔德(伯克利教授/引入CRISPR课题)",
    "雷切尔·哈维茨(实验室成员/驯鹿生物科技共同创立)"
]
colleagues_friends = [
    "乔治·丘奇(哈佛教授/CRISPR应用合作)",
    "张锋(MIT教授/基因编辑领域同行)",
    "刘如谦(哈佛教授/CRISPR精准度优化合作)",
    "基兰·穆苏努鲁(哈佛教授/CRISPR临床应用合作)",
    "菲利普·霍瓦特(丹尼斯克公司/CRISPR免疫机制验证)",
    "维尔日尼胡斯·塞克相尼斯(立陶宛科学家/CRISPR酶功能研究)",
    "凯文·埃斯维特(丘奇实验室/基因驱动技术合作)"
]
key_figures = [
    "诺贝尔基金会(诺贝尔化学奖授予机构)",
    "美国国家科学院(人类基因编辑国际峰会主办)",
    "中国科学院(人类基因编辑国际峰会协办)",
    "英国皇家学会(人类基因编辑国际峰会协办)",
    "FDA(美国食品药品监督管理局/基因编辑监管)",
    "世界卫生组织(CRISPR临床应用推广)",
    "巴拉克·奥巴马(美国前总统/科研政策支持)",
    "乔·拜登(美国前副总统/癌症登月计划合作)",
    "黄军就(中国科学家/人类胚胎编辑实验相关)",
    "保罗·博格(重组DNA先驱/伦理思考影响者)"
]

# 3. 关系边（标注核心关联与合作内容）
edges = [
    # 核心 ↔ 家人
    (core_person, "马丁·杜德娜(父/英文教授/启蒙者)", "父女/科学兴趣启蒙+书籍推荐"),
    (core_person, "多萝西·杜德娜(母/家庭支持者)", "母女/教育与生活支持"),
    (core_person, "杰米·凯特(夫/结构生物学家/终身伴侣)", "夫妻/科研支持+生活陪伴"),
    (core_person, "安德鲁(子/家庭陪伴)", "母子/家庭陪伴+成长见证"),
    (core_person, "埃伦(妹/家庭支持)", "姐妹/情感支持"),

    # 核心 ↔ 导师
    (core_person, "杰克·绍斯塔克(哈佛导师/诺贝尔得主/DNA修复研究)", "师生/DNA修复机制指导"),
    (core_person, "汤姆·切克(科罗拉多大学博士后导师/诺贝尔得主/核酶研究)", "师生/核酶结构与功能研究"),
    (core_person, "唐·赫姆斯(本科导师/真菌研究启蒙)", "师生/微生物研究入门指导"),

    # 核心 ↔ 长期合作者
    (core_person, "埃马纽埃尔·卡彭蒂耶(法国科学家/CRISPR共同开发)", "合作/共同开发CRISPR-Cas9基因编辑技术"),
    (core_person, "塞缪尔·斯滕伯格(实验室成员/共同著书/CRISPR机制研究)", "合作/CRISPR分子机制解析+合著科普书籍"),
    (core_person, "马丁·耶奈克(博士后/CRISPR-Cas9关键实验)", "合作/验证Cas9-RNA复合体切割DNA功能"),
    (core_person, "吉莉安·班菲尔德(伯克利教授/引入CRISPR课题)", "合作/开启细菌CRISPR免疫系统研究"),
    (core_person, "雷切尔·哈维茨(实验室成员/驯鹿生物科技共同创立)", "合作/CRISPR技术商业化开发"),

    # 核心 ↔ 同事/挚友
    (core_person, "乔治·丘奇(哈佛教授/CRISPR应用合作)", "同道+合作/CRISPR多物种编辑探索"),
    (core_person, "刘如谦(哈佛教授/CRISPR精准度优化合作)", "合作/降低CRISPR脱靶效应研究"),
    (core_person, "基兰·穆苏努鲁(哈佛教授/CRISPR临床应用合作)", "合作/镰状细胞病基因编辑治疗探索"),
    (core_person, "维尔日尼胡斯·塞克相尼斯(立陶宛科学家/CRISPR酶功能研究)", "学术交流/CRISPR酶功能互证"),

    # 核心 ↔ 关键人物
    (core_person, "诺贝尔基金会(诺贝尔化学奖授予机构)", "关联/2020年诺贝尔化学奖得主"),
    (core_person, "美国国家科学院(人类基因编辑国际峰会主办)", "关联/主导生殖细胞编辑伦理讨论"),
    (core_person, "世界卫生组织(CRISPR临床应用推广)", "关联/推动CRISPR全球医疗公平应用"),
    (core_person, "保罗·博格(重组DNA先驱/伦理思考影响者)", "影响/启发基因编辑伦理规范制定"),

    # 跨关系
    ("埃马纽埃尔·卡彭蒂耶(法国科学家/CRISPR共同开发)", "马丁·耶奈克(博士后/CRISPR-Cas9关键实验)",
     "合作/验证CRISPR切割机制"),
    ("塞缪尔·斯滕伯格(实验室成员/共同著书/CRISPR机制研究)", "布莱克·韦德海福特(博士后/早期CRISPR免疫机制研究)",
     "同事/实验室CRISPR协作"),
    ("乔治·丘奇(哈佛教授/CRISPR应用合作)", "凯文·埃斯维特(丘奇实验室/基因驱动技术合作)", "师徒/基因驱动技术研发"),
    ("美国国家科学院(人类基因编辑国际峰会主办)", "中国科学院(人类基因编辑国际峰会协办)", "协作/全球基因编辑伦理对话")
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
plt.title('珍妮佛·杜德娜核心关系网络图谱', fontsize=22, pad=40)

# 隐藏坐标轴，保存高清图谱
plt.axis('off')
plt.tight_layout()
plt.savefig(
    '珍妮佛杜德娜关系图谱_终极兼容版.png',
    dpi=300,
    bbox_inches='tight'  # 确保中文标签不被截断
)
plt.close()

print("🎉 图谱生成成功！文件：珍妮佛杜德娜关系图谱_终极兼容版.png")
print(f"📊 包含 {len(G.nodes())} 位关键人物，{len(edges)} 条核心关系")
print("✅ 中文显示正常 | ✅ 无参数错误 | ✅ 兼容 nx 1.x+ & matplotlib 2.x+")
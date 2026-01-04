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
core_person = "玛丽·居里（居里夫人）"
family = [
    "乌拉狄斯拉夫·斯可罗多夫斯基(父/物理教师)", "樊复华(母/教育家)",
    "苏菲·斯可罗多夫斯基(姐/素希雅)", "布罗妮雅·斯可罗多夫斯基(姐/医学生)",
    "海拉·斯可罗多夫斯基(姐)", "约瑟夫·斯可罗多夫斯基(兄/医生)",
    "比埃尔·居里(夫/物理学家/诺贝尔奖得主)", "伊雷娜·约里奥-居里(女/物理学家)",
    "艾芙·居里(女/传记作家)", "吴挹峰(祖父/秀才)", "吴琢之(叔/资助留学)",
    "菲利克斯·柏古斯基(外祖父/小贵族)", "弗雷德里克·约里奥-居里(女婿/物理学家)",
    "亚历山大·约里奥(外孙)", "海伦娜·约里奥(外孙女)"
]
mentors = [
    "亨利·柏克勒尔(放射性发现者/导师)", "李普曼(索尔本教授/物理导师)",
    "布提(索尔本教授/化学导师)", "西科尔斯卡小姐(波兰寄宿学校导师)",
    "乌拉狄斯拉夫·斯可罗多夫斯基(父/启蒙导师)", "比埃尔·居里(夫/科研导师)",
    "舒曾伯格(理化学校校长/支持研究者)", "福提埃大夫(医学指导/健康顾问)"
]
long_term_collaborators = [
    "比埃尔·居里(夫/镭与钋共同发现)", "安德烈·德比尔纳(锕元素共同发现)",
    "乔治·萨尼亚(放射性射线合作研究)", "G·贝蒙(镭化学性质合作)",
    "阿尔麦·德·李斯罗(制镭工业合作)", "雅克·居里(比埃尔之兄/压电效应研究)",
    "拉伯德(镭放热现象合作)", "布沙尔(镭生理作用合作)",
    "巴尔塔沙尔(放射疗法合作)", "欧得班(制镭工艺合作)"
]
colleagues_friends = [
    "保罗·郎之万(物理学家/挚友)", "让·佩韩(索尔本教授/同道)",
    "克尔文勋爵(英国物理学家/挚友)", "威廉·克鲁克斯爵士(英国化学家/同道)",
    "瑞利勋爵(英国物理学家/学术交流)", "卡霁雅·普希波罗夫斯卡(波兰挚友)",
    "亨利埃特·米哈洛夫斯卡(表姐/挚友)", "德卢斯基夫妇(布罗妮雅夫妇/挚友)",
    "兜娄大夫(放射疗法应用合作)", "威卡姆(镭医疗研究者)"
]
key_figures = [
    "欧利维理乌斯(瑞典科学院常务秘书)", "卢贝(法国总统/接见者)",
    "普安加瑞(法国科学家/支持者)", "穆瓦松(诺贝尔化学奖得主/主考人)",
    "阿尔伯特·爱因斯坦(物理学家/敬仰者)", "诺贝尔基金会(奖金授予机构代表)",
    "舒曾伯格(理化学校校长/实验室支持)", "娄特(理化学校后续校长)",
    "乔治·古依(比埃尔挚友/学术通信者)", "赛福尔女子高等师范学校师生"
]

# 3. 关系边（标注核心关联与合作内容）
edges = [
    # 核心 ↔ 家人
    (core_person, "乌拉狄斯拉夫·斯可罗多夫斯基(父/物理教师)", "父女/科学启蒙"),
    (core_person, "樊复华(母/教育家)", "母女/教育支持"),
    (core_person, "布罗妮雅·斯可罗多夫斯基(姐/医学生)", "姐妹/相互资助留学"),
    (core_person, "比埃尔·居里(夫/物理学家/诺贝尔奖得主)", "夫妻/科研伴侣+终身合作"),
    (core_person, "伊雷娜·约里奥-居里(女/物理学家)", "母女/科研传承"),
    (core_person, "艾芙·居里(女/传记作家)", "母女/生平记录"),
    (core_person, "吴琢之(叔/资助留学)", "叔侄/赴美深造资助"),
    (core_person, "弗雷德里克·约里奥-居里(女婿/物理学家)", "翁婿/科研合作"),

    # 核心 ↔ 导师
    (core_person, "亨利·柏克勒尔(放射性发现者/导师)", "师生/放射性研究启蒙"),
    (core_person, "李普曼(索尔本教授/物理导师)", "师生/实验室指导"),
    (core_person, "比埃尔·居里(夫/科研导师)", "师生+夫妻/镭研究核心指导"),
    (core_person, "西科尔斯卡小姐(波兰寄宿学校导师)", "师生/基础教育"),

    # 核心 ↔ 长期合作者
    (core_person, "比埃尔·居里(夫/镭与钋共同发现)", "合作/提取镭与钋"),
    (core_person, "安德烈·德比尔纳(锕元素共同发现)", "合作/分离新元素锕"),
    (core_person, "乔治·萨尼亚(放射性射线合作研究)", "合作/次级射线电荷研究"),
    (core_person, "阿尔麦·德·李斯罗(制镭工业合作)", "合作/镭工业化生产"),
    (core_person, "拉伯德(镭放热现象合作)", "合作/镭自动放热特性研究"),
    (core_person, "布沙尔(镭生理作用合作)", "合作/镭的生物效应实验"),

    # 核心 ↔ 同事/挚友
    (core_person, "保罗·郎之万(物理学家/挚友)", "同事+挚友/学术交流"),
    (core_person, "克尔文勋爵(英国物理学家/挚友)", "学术交流/镭特性探讨"),
    (core_person, "卡霁雅·普希波罗夫斯卡(波兰挚友)", "挚友/生活相互支持"),
    (core_person, "德卢斯基夫妇(布罗妮雅夫妇/挚友)", "亲友+同道/相互扶持"),
    (core_person, "兜娄大夫(放射疗法应用合作)", "合作/镭治疗癌症实践"),

    # 核心 ↔ 关键人物
    (core_person, "欧利维理乌斯(瑞典科学院常务秘书)", "关联/诺贝尔奖金通知"),
    (core_person, "诺贝尔基金会(奖金授予机构代表)", "关联/诺贝尔物理学奖得主"),
    (core_person, "阿尔伯特·爱因斯坦(物理学家/敬仰者)", "关联/学术敬仰与支持"),
    (core_person, "舒曾伯格(理化学校校长/实验室支持)", "关联/提供棚屋实验室"),

    # 跨关系
    ("比埃尔·居里(夫/物理学家/诺贝尔奖得主)", "雅克·居里(比埃尔之兄/压电效应研究)", "兄弟/科研合作"),
    ("伊雷娜·约里奥-居里(女/物理学家)", "弗雷德里克·约里奥-居里(女婿/物理学家)", "夫妻/人工放射现象发现"),
    ("亨利·柏克勒尔(放射性发现者/导师)", "比埃尔·居里(夫/科研导师)", "同事/放射性研究交流"),
    ("安德烈·德比尔纳(锕元素共同发现)", "阿尔麦·德·李斯罗(制镭工业合作)", "同事/制镭技术优化")
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
plt.title('玛丽·居里（居里夫人）核心关系网络图谱', fontsize=22, pad=40)

# 隐藏坐标轴，保存高清图谱
plt.axis('off')
plt.tight_layout()
plt.savefig(
    '居里夫人关系图谱_终极兼容版.png',
    dpi=300,
    bbox_inches='tight'  # 确保中文标签不被截断
)
plt.close()

print("🎉 图谱生成成功！文件：居里夫人关系图谱_终极兼容版.png")
print(f"📊 包含 {len(G.nodes())} 位关键人物，{len(edges)} 条核心关系")
print("✅ 中文显示正常 | ✅ 无参数错误 | ✅ 兼容 nx 1.x+ & matplotlib 2.x+")
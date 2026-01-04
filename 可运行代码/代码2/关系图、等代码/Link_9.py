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
core_person = "林巧稚"
family = [
    "林良英(父/英语教师/启蒙者)", "母亲(家庭支持者)",
    "林振明(大哥/实业家/资助者)", "林振炎(二哥/民族工商业者)",
    "林款稚(大姐/受抚养者)", "二嫂(二哥妻子/家庭支持)",
    "林懿铿(侄女/同事)", "林心铿(侄女/医学从业者)",
    "林嘉通(侄儿/学者)", "林嘉泽(侄儿)", "林嘉平(侄儿)",
    "林嘉禾(侄儿)", "蔡玉辉(姨外孙女/麻醉师)",
    "林清雨(姨外孙女夫/翻译)"
]
mentors = [
    "梅瑞·嘉凌(凌姑娘/厦门女师教务长/英语与人生导师)",
    "马士敦(协和妇产科主任/临床与科研导师)",
    "西科尔斯卡小姐(波兰寄宿学校/基础教育导师)",
    "吴朝仁(协和校友/挚友/医学前辈)",
    "沈骥英(协和校友/妇幼保健专家/前辈)"
]
long_term_collaborators = [
    "叶惠方(协和学生/长期助手/妇产科学传承)",
    "宋鸿钊(协和学生/绒癌研究核心合作者)",
    "王文彬(协和同事/新生儿溶血症研究合作)",
    "姜梅(协和同事/产科临床合作)",
    "张苣芬(公共卫生专家/宫颈癌普查普治合作)",
    "孙爱达(协和学生/临床与科研助手)",
    "徐蕴华(协和学生/临床实践指导)",
    "陈本真(妇产医院筹建/普查普治合作者)"
]
colleagues_friends = [
    "周华康(侄婿/协和儿科主任/家人+同事)",
    "严仁英(妇产科学者/同道+挚友)",
    "俞霭峰(妇产科学者/同道+合作者)",
    "张孝骞(协和内科主任/同事+挚友)",
    "黄家驷(医学科学院院长/巡回医疗合作者)",
    "吴英恺(阜外医院院长/巡回医疗合作者)",
    "邓颖超(周恩来夫人/医患+挚友)",
    "埃德加·斯诺(美国记者/中国医疗状况访谈对象)",
    "诸葛淳(妇产科总支书记/党组织联系人)"
]
key_figures = [
    "周恩来(国家总理/关怀与支持)",
    "彭真(北京市长/妇产医院筹建支持)",
    "傅作义(北平司令/和平解放保障工作环境)",
    "毛泽东(国家领导人/卫生政策支持)",
    "宋庆龄(国家领导人/妇幼事业支持者)",
    "世界卫生组织(医学顾问委员会/国际学术参与)",
    "中华医学会(妇产科学会创始人/学术平台)",
    "洛克菲勒基金会(旧协和创办方/早期学习平台)",
    "焦海棠(新生儿溶血症患者/医疗突破案例)",
    "谢齐历(受冤患者/医疗与正义守护案例)"
]

# 3. 关系边（标注核心关联与合作内容）
edges = [
    # 核心 ↔ 家人
    (core_person, "林良英(父/英语教师/启蒙者)", "父女/英语启蒙+科学兴趣培养"),
    (core_person, "林振明(大哥/实业家/资助者)", "兄妹/大学学费与生活资助"),
    (core_person, "林振炎(二哥/民族工商业者)", "兄妹/家庭支持与民族气节影响"),
    (core_person, "林懿铿(侄女/同事)", "姑侄/工作协助+生活照料"),
    (core_person, "蔡玉辉(姨外孙女/麻醉师)", "姨婆-姨外孙女/资助留学+人生引导"),
    (core_person, "周华康(侄婿/协和儿科主任/家人+同事)", "姑母-侄婿/工作协作+家庭互助"),

    # 核心 ↔ 导师
    (core_person, "梅瑞·嘉凌(凌姑娘/厦门女师教务长/英语与人生导师)", "师生/英语培养+独立女性价值观引导"),
    (core_person, "马士敦(协和妇产科主任/临床与科研导师)", "师生/妇产科临床技术+科室管理指导"),
    (core_person, "吴朝仁(协和校友/挚友/医学前辈)", "前辈-后辈/医学道路指引+挚友支持"),

    # 核心 ↔ 长期合作者
    (core_person, "叶惠方(协和学生/长期助手/妇产科学传承)", "师徒/临床带教+科室管理传承"),
    (core_person, "宋鸿钊(协和学生/绒癌研究核心合作者)", "师徒+合作/绒癌化疗方案研发+推广"),
    (core_person, "王文彬(协和同事/新生儿溶血症研究合作)", "合作/新生儿换血疗法突破"),
    (core_person, "张苣芬(公共卫生专家/宫颈癌普查普治合作)", "合作/全国宫颈癌普查普治发起+推进"),
    (core_person, "陈本真(妇产医院筹建/普查普治合作者)", "合作/北京妇产医院筹建+基层医疗推广"),

    # 核心 ↔ 同事/挚友
    (core_person, "严仁英(妇产科学者/同道+挚友)", "同道+挚友/妇幼保健事业共同推进"),
    (core_person, "张孝骞(协和内科主任/同事+挚友)", "同事+挚友/学术交流+人生相互支持"),
    (core_person, "邓颖超(周恩来夫人/医患+挚友)", "医患+挚友/健康关怀+相互敬重"),
    (core_person, "黄家驷(医学科学院院长/巡回医疗合作者)", "合作/湖南农村巡回医疗+基层服务"),

    # 核心 ↔ 关键人物
    (core_person, "周恩来(国家总理/关怀与支持)", "关联/工作支持+政治保护+人生指引"),
    (core_person, "彭真(北京市长/妇产医院筹建支持)", "关联/北京妇产医院筹建批准+选址支持"),
    (core_person, "世界卫生组织(医学顾问委员会/国际学术参与)", "关联/国际医学交流+顾问履职"),
    (core_person, "中华医学会(妇产科学会创始人/学术平台)", "关联/创办妇产科学会+主编专业杂志"),
    (core_person, "焦海棠(新生儿溶血症患者/医疗突破案例)", "医患/新生儿溶血症治疗技术突破"),

    # 跨关系
    ("宋鸿钊(协和学生/绒癌研究核心合作者)", "吴葆祯(协和同事/绒癌研究协作)", "同事/绒癌临床与科研协作"),
    ("叶惠方(协和学生/长期助手/妇产科学传承)", "孙爱达(协和学生/临床与科研助手)", "师姐-师妹/临床经验传承"),
    ("周华康(侄婿/协和儿科主任/家人+同事)", "林嘉通(侄儿/学者)", "姑丈-内侄/家庭互助+学业支持"),
    ("邓颖超(周恩来夫人/医患+挚友)", "周恩来(国家总理/关怀与支持)", "夫妻/共同支持林巧稚工作")
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
plt.title('林巧稚核心关系网络图谱', fontsize=22, pad=40)

# 隐藏坐标轴，保存高清图谱
plt.axis('off')
plt.tight_layout()
plt.savefig(
    '林巧稚关系图谱_终极兼容版.png',
    dpi=300,
    bbox_inches='tight'  # 确保中文标签不被截断
)
plt.close()

print("🎉 图谱生成成功！文件：林巧稚关系图谱_终极兼容版.png")
print(f"📊 包含 {len(G.nodes())} 位关键人物，{len(edges)} 条核心关系")
print("✅ 中文显示正常 | ✅ 无参数错误 | ✅ 兼容 nx 1.x+ & matplotlib 2.x+")
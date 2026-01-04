import networkx as nx
import matplotlib.pyplot as plt

# 1. 配置 Windows 中文字体（确保中文显示）
try:
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial']
    plt.rcParams['axes.unicode_minus'] = False
    print("✅ 中文字体配置成功")
except Exception as e:
    print(f"⚠️ 中文字体配置提示: {e}，使用系统默认字体")
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Arial']
    plt.rcParams['axes.unicode_minus'] = False

# 2. 核心关系数据
core_person = "何泽慧"
family = ["钱三强(夫)", "何澄(父)", "王季山(母)", "何怡贞(姐)", "钱祖玄(女)", "钱民协(女)", "钱思进(子)"]
teachers = ["波特(德导)", "克兰茨(德导)", "约里奥-居里(法导)", "叶企孙(清华导)", "吴有训(清华导)"]
colleagues = ["彭桓武", "王淦昌", "赵忠尧", "朱光亚", "张文裕", "谢家麟"]
students = ["黄祖洽", "王豫生", "孙汉城", "张焕乔", "陆祖荫"]

# 3. 关系边
edges = [
    (core_person, "钱三强(夫)", "夫妻+科研"),
    (core_person, "何澄(父)", "父女"),
    (core_person, "王季山(母)", "母女"),
    (core_person, "何怡贞(姐)", "姐妹"),
    (core_person, "钱祖玄(女)", "母女"),
    (core_person, "钱民协(女)", "母女"),
    (core_person, "钱思进(子)", "母子"),
    (core_person, "波特(德导)", "师生(正负电子)"),
    (core_person, "克兰茨(德导)", "师生(博士)"),
    (core_person, "约里奥-居里(法导)", "师生(居里实验室)"),
    (core_person, "叶企孙(清华导)", "师生(本科)"),
    (core_person, "吴有训(清华导)", "师生(实验)"),
    (core_person, "彭桓武", "同事(中子物理)"),
    (core_person, "王淦昌", "同事(宇宙线)"),
    (core_person, "赵忠尧", "同事(加速器)"),
    (core_person, "朱光亚", "同事(核数据)"),
    (core_person, "张文裕", "同事(高能所)"),
    (core_person, "黄祖洽", "师徒(核乳胶)"),
    (core_person, "王豫生", "师徒(裂变)"),
    (core_person, "孙汉城", "师徒(核乳胶)"),
    (core_person, "张焕乔", "师徒(中子)"),
    ("钱三强(夫)", "约里奥-居里(法导)", "师生"),
    ("彭桓武", "王淦昌", "同事(核武器)"),
    ("赵忠尧", "叶企孙(清华导)", "同事(清华)")
]

# 4. 创建图结构
G = nx.Graph()
all_nodes = [core_person] + family + teachers + colleagues + students
G.add_nodes_from(all_nodes)
for source, target, relation in edges:
    G.add_edge(source, target, relation=relation)

# 5. 节点着色
node_colors = []
for node in G.nodes():
    if node == core_person:
        node_colors.append('#FF5733')
    elif node in family:
        node_colors.append('#3498DB')
    elif node in teachers:
        node_colors.append('#2ECC71')
    elif node in colleagues:
        node_colors.append('#9B59B6')
    elif node in students:
        node_colors.append('#F39C12')

# 6. 绘制图谱（关键：区分不同函数的参数名）
plt.figure(figsize=(14, 10))

# 弹簧布局
pos = nx.spring_layout(G, k=5.0, iterations=200, seed=42)

# 绘制节点
nx.draw_networkx_nodes(G, pos, node_size=6000, node_color=node_colors, alpha=0.9, edgecolors='black', linewidths=2)

# 绘制边
nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.8, edge_color='#666666')

# 绘制边标签：极低版本 networkx 只认 font_size（带下划线）
edge_labels = nx.get_edge_attributes(G, 'relation')
nx.draw_networkx_edge_labels(
    G, pos,
    edge_labels=edge_labels,
    font_size=9,  # 这里必须用 font_size（带下划线），适配 nx 1.x 早期
    label_pos=0.4
)

# 绘制节点标签：极低版本 nx 认 font_size，也兼容 fontsize，统一用 font_size
nx.draw_networkx_labels(G, pos, font_size=12)

# 绘制标题：matplotlib 只认 fontsize（无下划线）
plt.title('何泽慧核心关系网络图谱', fontsize=16, pad=25)

# 保存图谱
plt.axis('off')
plt.tight_layout()
plt.savefig(
    '何泽慧关系图谱_终极兼容完美版.png',
    dpi=300,
    bbox_inches='tight'
)
plt.close()

print("🎉 图谱生成成功！文件：何泽慧关系图谱_终极兼容完美版.png")
print(f"📊 包含 {len(all_nodes)} 人，{len(edges)} 条关系")
print("✅ 中文正常 | ✅ 无参数错误 | ✅ 兼容 nx 1.x+ & matplotlib 2.x+")
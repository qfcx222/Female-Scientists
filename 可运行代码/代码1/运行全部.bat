@echo off
echo 开始女科学家传记数据清理项目...

echo 正在安装依赖包...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo 正在运行数据清理管道...
python advanced_data_cleaning.py

echo 正在生成总结报告...
python generate_report.py

echo 项目执行完成！
echo.
echo 清理后的数据保存在 output 目录中
echo 数据统计报告请查看 "数据清理总结报告.md"
echo 详细使用说明请查看 "使用说明.md"

pause
import os
import shutil
import pikepdf
from io import BytesIO
from bs4 import BeautifulSoup
from googlesearch import search
import re
import requests
# 从给定文本中提取排名前10的房地产公司
raw_text = "TOP10依次是：万科（1515.33亿元）、碧桂园（1401.42亿元）、恒大（1266.05亿元）、融创中国（1022.95亿元）、保利地产（1015.16亿元）、中海地产（989.06亿元）、华润置地（917.70亿元）、龙湖集团（880.28亿元）、世茂集团（804.79亿元）、招商蛇口（755.23亿元）。"
pattern = re.compile(r'([\u4e00-\u9fa5]+)\（')
top_10_companies = pattern.findall(raw_text)

print("提取到的排名前10的房地产公司：")
print(top_10_companies)

# 确保ESG_reports目录存在
if not os.path.exists('ESG_reports'):
    os.makedirs('ESG_reports')

# 搜索ESG报告
for company in top_10_companies:
    query = f"{company} ESG报告 filetype:pdf"
    try:
        # 使用googlesearch库进行搜索
        for result in search(query, num_results=10):
            print(f"找到可能的 {company} 的ESG报告: {result}")

            # 使用requests库下载PDF文件
            response = requests.get(result)

            # 检查PDF页数
            with pikepdf.open(BytesIO(response.content)) as pdf:
                num_pages = len(pdf.pages)
                if num_pages < 10:
                    print(f"跳过，不足10页")
                    continue

            # 保存PDF文件
            temp_file_path = "temp_esg_report.pdf"
            with open(temp_file_path, "wb") as file:
                file.write(response.content)

            # 将PDF文件重命名为公司名字
            file_name = f"{company}_ESG报告.pdf"
            file_path = os.path.join("ESG_reports", file_name)
            shutil.move(temp_file_path, file_path)
            print(f"下载成功: {file_path}")
            break  # 下载完成后，跳出循环

    except Exception as e:
        print(f"搜索 {company} 的ESG报告时出错: {e}")
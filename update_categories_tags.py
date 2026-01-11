import os
import re

posts_dir = 'source/_posts'

files = [f for f in os.listdir(posts_dir) if f.endswith('.md')]

for f in files:
    path = os.path.join(posts_dir, f)
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Find title
    title_match = re.search(r'title: (.+)', content)
    if not title_match:
        continue
    title = title_match.group(1).strip()

    # Assign categories and tags based on filename or title
    categories = []
    tags = []

    if 'IC设计' in f or 'IC设计' in title:
        categories.append('数字IC设计')
        # Add specific tags
        if 'Verilog' in title or '序列机' in title or '分频' in title or 'FIFO' in title or '锁存器' in title or '边沿检测' in title or 'RAM' in title:
            tags.append('Verilog')
        if 'Chisel' in title:
            tags.append('Chisel')
        if 'FPGA' in title or 'Vivado' in title or 'ZC706' in title or 'Zynq' in title:
            tags.append('FPGA')
        if 'AXI' in title:
            tags.append('AXI')
        if 'Cache' in title:
            tags.append('Cache')
        if 'Synopsys' in title or 'DC' in title or 'ICC' in title:
            tags.append('EDA工具')
        if 'NoC' in title or '路由算法' in title:
            tags.append('NoC')
        if '时序分析' in title:
            tags.append('时序分析')
        if '跨时钟' in title:
            tags.append('异步电路')
        if '任意倍数' in title or '奇数分频' in title:
            tags.append('分频器')
        if 'Scala' in title:
            tags.append('Scala')
        if 'Mill' in title:
            tags.append('Mill')
        if 'Verilator' in title:
            tags.append('Verilator')
    elif 'CCNA' in f:
        categories.append('计算机网络')
        tags.extend(['CCNA', '思科', '路由器'])
        if 'Mac地址' in title or 'vlan' in title or 'trunk' in title:
            tags.append('交换机')
    elif '安装配置' in f:
        categories.append('环境配置')
        if 'WSL' in title:
            tags.extend(['WSL', 'Linux'])
        if 'Docker' in title:
            tags.append('Docker')
        if 'IDEA' in title or 'Maven' in title:
            tags.extend(['IDEA', 'Java'])
        if 'Linux' in title and 'mysql' in title:
            tags.extend(['MySQL', 'Linux'])
        if 'Tomcat' in title:
            tags.append('Tomcat')
        if 'redis' in title:
            tags.append('Redis')
        if '双系统' in title:
            tags.extend(['双系统', 'Windows'])
        if 'devc++' in title:
            tags.extend(['Dev-C++', 'C++'])
        if '阿里云' in title:
            tags.append('SSL证书')
    elif '异常处理' in f:
        categories.append('异常处理')
        tags.extend(['调试', '错误解决'])
        if 'Git' in title:
            tags.append('Git')
        if 'Chisel' in title:
            tags.append('Chisel')
        if 'cmake' in title:
            tags.append('CMake')
        if 'verilator' in title:
            tags.append('Verilator')
        if 'word' in title:
            tags.append('Office')
        if 'z3' in title:
            tags.append('z3')
    elif '操作系统' in f:
        categories.append('操作系统')
        tags.append('操作系统')
        if 'xv6' in title:
            tags.extend(['xv6', '教学操作系统'])
        if 'RISC-V' in title:
            tags.append('RISC-V')
    elif '片上网络专题讨论一' in f:
        categories.append('片上网络')
        tags.extend(['片上网络', '总线'])
    elif 'OFDM' in f:
        categories.append('通信系统')
        tags.extend(['OFDM', 'DFT', '信号处理'])
    elif '程序人生' in f:
        categories.append('程序人生')
        tags.extend(['研究生', '经历', '分享'])
    elif '读书笔记' in f:
        categories.append('读书笔记')
        tags.extend(['读书笔记', '学术'])
    elif 'PyTorch' in title:
        categories.append('编程与算法')
        tags.extend(['PyTorch', '深度学习', 'Python'])
    elif 'EOJ' in f:
        categories.append('编程与算法')
        tags.extend(['算法', '编程竞赛', 'C++'])
    elif 'arpspoof' in f:
        categories.append('网络安全')
        tags.extend(['网络安全', '中间人攻击', 'Linux'])
    elif 'helloworld' in f:
        categories.append('编程与算法')
        tags.extend(['C语言', '编程入门'])
    elif 'C语言取反运算符' in f:
        categories.append('编程与算法')
        tags.extend(['C语言', '运算符'])
    elif 'JavaWeb' in f:
        categories.append('编程与算法')
        tags.extend(['Java', 'Web开发'])
    elif 'java学习' in f:
        categories.append('编程与算法')
        tags.extend(['Java', '面向对象'])
    elif 'Java学习' in f:
        categories.append('编程与算法')
        tags.extend(['Java', '短信'])
    elif 'Linux下C' in f:
        categories.append('编程与算法')
        tags.extend(['C语言', 'Linux', '多进程'])
    elif 'linux下C' in f:
        categories.append('编程与算法')
        tags.extend(['C语言', 'Linux', '动态库'])
    elif 'linux学习' in f:
        categories.append('编程与算法')
        tags.extend(['Linux', '链接'])
    elif '你未必了解的Java注释知识' in f:
        categories.append('编程与算法')
        tags.extend(['Java', '注释'])
    elif '准研一学习' in f:
        categories.append('编程与算法')
        tags.extend(['Verilog', 'FPGA'])
    elif '前端学习' in f:
        categories.append('编程与算法')
        tags.extend(['前端', '图标库'])
    elif '字符编码' in f:
        categories.append('编程与算法')
        tags.extend(['字符编码', 'GB2312'])
    elif 'Git_Github学习' in f:
        categories.append('编程与算法')
        tags.extend(['Git', 'GitHub'])

    # Limit
    categories = categories[:3]
    tags = list(set(tags))[:5]  # unique and limit to 5

    # Update content
    lines = content.split('\n')
    in_front = False
    for i, line in enumerate(lines):
        if line.strip() == '---':
            if not in_front:
                in_front = True
            else:
                break
        if in_front:
            if line.startswith('categories:'):
                lines[i] = f'categories: {", ".join(categories)}'
            elif line.startswith('tags:'):
                lines[i] = f'tags: [{", ".join(tags)}]'

    new_content = '\n'.join(lines)

    with open(path, 'w', encoding='utf-8') as file:
        file.write(new_content)

print("Updated categories and tags for all posts.")
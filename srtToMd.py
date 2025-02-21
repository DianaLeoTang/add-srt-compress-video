import re
import jieba
import os
from collections import defaultdict
import logging

jieba.setLogLevel(logging.INFO)

class SRTToMindmap:
    def __init__(self):
        # 扩大关键词集合
        self.important_words = set([
            '首先', '其次', '然后', '最后', '另外', '总之', '因此', '所以',
            '这节课', '这一节', '我们来', '咱们来', '接下来', '下面', 
            '第一', '第二', '第三', '第四', '重点', '主要', '关键',
            '讲解', '介绍', '说明', '演示', '学习', '理解'
        ])

    def convert_file(self, file_path):
        """转换单个SRT文件"""
        try:
            # 1. 读取文件
            print("\n=== 开始读取文件 ===")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"原始内容长度: {len(content)}")
            
            # 2. 清理内容
            print("\n=== 开始清理内容 ===")
            cleaned_content = self._clean_content(content)
            print(f"清理后内容长度: {len(cleaned_content)}")
            
            # 3. 提取主题
            print("\n=== 开始提取主题 ===")
            topics = self._extract_topics(cleaned_content)
            print(f"提取到主题数量: {len(topics)}")
            
            # 4. 生成markdown
            print("\n=== 开始生成Markdown ===")
            markdown = self._generate_markdown(topics)
            
            # 5. 保存文件
            print("\n=== 开始保存文件 ===")
            output_path = os.path.splitext(file_path)[0] + '.md'
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown)
            print(f"已保存到: {output_path}")
            
        except Exception as e:
            print(f"处理文件出错: {e}")

    def _clean_content(self, content):
        """清理内容"""
        # 先按行分割
        lines = content.split('\n')
        valid_lines = []
        
        for line in lines:
            line = line.strip()
            
            # 跳过无效行
            if not line or line.isdigit() or '-->' in line:
                continue
                
            # 跳过纯英文行和过短的行
            if re.match(r'^[a-zA-Z\s,\.]+$', line) or len(line) < 5:
                continue
                
            valid_lines.append(line)
        
        # 合并行并按句号分割
        text = ''.join(valid_lines)
        sentences = re.split(r'[。！？\n]', text)
        
        # 过滤无效句子
        valid_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) >= 5:
                valid_sentences.append(sentence)
        
        return valid_sentences

    def _extract_topics(self, sentences):
        """提取主题"""
        topics = defaultdict(list)
        current_topic = "概述"
        found_first_topic = False
        
        for sentence in sentences:
            # 检查是否包含关键词
            words = jieba.lcut(sentence)
            contains_keyword = any(word in self.important_words for word in words)
            
            # 第一个包含关键词的句子作为标题
            if not found_first_topic and contains_keyword:
                current_topic = sentence
                found_first_topic = True
            # 之后的关键词句子作为主题
            elif contains_keyword and len(sentence) >= 10:
                current_topic = sentence
            # 其他句子作为子主题
            elif len(sentence) >= 5:
                topics[current_topic].append(sentence)
        
        # 如果没有找到任何主题，使用默认主题
        if not topics:
            topics["主要内容"] = [s for s in sentences if len(s) >= 5]
            
        return topics

    def _generate_markdown(self, topics):
        """生成markdown"""
        lines = ["# 内容大纲\n"]
        
        for topic, subtopics in topics.items():
            # 添加主题
            lines.append(f"\n## {topic}\n")
            
            # 过滤并添加子主题
            filtered_subtopics = []
            for subtopic in subtopics:
                if len(subtopic) >= 5 and subtopic not in filtered_subtopics:
                    filtered_subtopics.append(subtopic)
                    lines.append(f"- {subtopic}\n")
        
        return ''.join(lines)

    def convert_directory(self, directory_path):
        """处理目录下的所有SRT文件"""
        for filename in os.listdir(directory_path):
            if filename.endswith('.srt'):
                file_path = os.path.join(directory_path, filename)
                print(f"\n处理文件: {filename}")
                self.convert_file(file_path)

if __name__ == "__main__":
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"当前目录: {script_dir}")
    
    # 处理文件
    converter = SRTToMindmap()
    converter.convert_directory(script_dir)
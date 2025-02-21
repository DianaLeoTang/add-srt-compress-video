import re
import jieba
import os
from collections import defaultdict
import logging

jieba.setLogLevel(logging.INFO)

class SRTToMindmap:
    def __init__(self):
        self.stopwords = set(['的', '了', '是', '在', '和', '就', '都', '而', '与'])
        self.important_words = set(['首先', '其次', '然后', '最后', '总之', '因此', '所以'])

    def convert_file(self, file_path):
        """转换单个SRT文件"""
        try:
            # 1. 读取文件
            print("\n=== 开始读取文件 ===")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"原始内容长度: {len(content)}")
            print("原始内容前100字符:")
            print(content[:100])
            
            # 2. 清理内容
            print("\n=== 开始清理内容 ===")
            cleaned_content = self._clean_content(content)
            print(f"清理后内容长度: {len(cleaned_content)}")
            print("清理后内容前100字符:")
            print(cleaned_content[:100])
            
            # 3. 提取主题
            print("\n=== 开始提取主题 ===")
            topics = self._extract_topics(cleaned_content)
            print(f"提取到主题数量: {len(topics)}")
            for topic, subtopics in topics.items():
                print(f"\n主题: {topic}")
                print(f"子主题数量: {len(subtopics)}")
                if subtopics:
                    print("第一个子主题示例:")
                    print(subtopics[0])
            
            # 4. 生成markdown
            print("\n=== 开始生成Markdown ===")
            markdown = self._generate_markdown(topics)
            print(f"生成的Markdown长度: {len(markdown)}")
            
            # 5. 保存文件
            print("\n=== 开始保存文件 ===")
            output_path = os.path.splitext(file_path)[0] + '.md'
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown)
            print(f"已保存到: {output_path}")
            
        except Exception as e:
            print(f"处理文件出错: {e}")
            import traceback
            print(traceback.format_exc())

    def _clean_content(self, content):
        """清理内容"""
        # 显示处理过程
        lines = content.split('\n')
        print(f"总行数: {len(lines)}")
        
        valid_lines = []
        for i, line in enumerate(lines):
            line = line.strip()
            # 跳过空行、数字行和时间戳行
            if not line:
                continue
            if line.isdigit():
                continue
            if '-->' in line:
                continue
                
            valid_lines.append(line)
            
            # 显示前几行有效内容
            if len(valid_lines) <= 5:
                print(f"有效行 {len(valid_lines)}: {line}")
        
        print(f"有效行数: {len(valid_lines)}")
        return ' '.join(valid_lines)

    def _extract_topics(self, text):
        """提取主题"""
        topics = defaultdict(list)
        current_topic = "主要内容"
        
        # 分句
        sentences = re.split('[。！？]', text)
        print(f"分句数量: {len(sentences)}")
        
        # 处理每个句子
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            # 显示正在处理的句子
            print(f"\n处理句子: {sentence}")
            
            # 检查是否为主题
            is_topic = False
            for word in self.important_words:
                if word in sentence:
                    current_topic = sentence
                    is_topic = True
                    print(f"发现新主题: {sentence}")
                    break
                    
            if not is_topic and len(sentence) > 5:
                topics[current_topic].append(sentence)
                print(f"添加子主题到 '{current_topic}'")
        
        return topics

    def _generate_markdown(self, topics):
        """生成markdown"""
        lines = ["# 内容大纲\n"]
        
        for topic, subtopics in topics.items():
            # 添加主题
            lines.append(f"\n## {topic}\n")
            # 添加子主题
            for subtopic in subtopics:
                lines.append(f"- {subtopic}\n")
        
        result = ''.join(lines)
        print("\n生成的Markdown内容:")
        print(result[:200] + "...")  # 显示前200字符
        return result

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
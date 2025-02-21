import re
import jieba
import os
from collections import defaultdict
import logging

# 隐藏jieba的日志输出
jieba.setLogLevel(logging.INFO)

class SRTToMindmap:
    def __init__(self, language='zh'):
        self.language = language
        self.stopwords = set([
            '的', '了', '是', '在', '我', '和', '就', '都', '而', '及', '与', '这', '那',
            '你', '我们', '他们', '它', '这个', '那个', '这些', '那些', '一个', '一些',
            '什么', '怎么', '为什么', '如何', '哪里', '什么时候', '谁'
        ])
        self.important_words = set([
            '首先', '其次', '然后', '最后', '另外', '总之', '因此', '所以', '但是', '不过',
            '第一', '第二', '第三', '第四', '第五', '重点', '核心', '主要', '关键',
            '总结', '注意', '特别', '特点', '步骤', '方法', '目的', '原因', '结果'
        ])

    def convert_directory(self, directory_path):
        """处理目录下的所有SRT文件"""
        # 确保目录路径存在
        if not os.path.isdir(directory_path):
            print(f"错误: {directory_path} 不是有效的目录")
            return
            
        # 遍历目录中的所有文件
        for filename in os.listdir(directory_path):
            if filename.endswith('.srt'):
                file_path = os.path.join(directory_path, filename)
                self.convert_file(file_path)

    def convert_file(self, file_path):
        """转换单个SRT文件"""
        try:
            # 读取文件内容
            print(f"\n处理文件: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 清理内容
            cleaned_content = self.clean_srt(content)
            if not cleaned_content:
                print(f"警告: {file_path} 清理后内容为空")
                return
                
            # 提取主题
            topics = self._extract_chinese_topics(cleaned_content)
            
            # 生成markdown
            markdown = self.generate_markdown(topics)
            
            # 生成输出文件路径
            output_path = os.path.splitext(file_path)[0] + '.md'
            
            # 保存文件
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown)
                
            print(f"成功: 已生成 {output_path}")
            
        except Exception as e:
            print(f"错误: 处理 {file_path} 时出错 - {e}")

    def clean_srt(self, content):
        """清理SRT文件格式,只保留对话内容"""
        if not content:
            return ""
            
        # 移除时间戳
        content = re.sub(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', '', content)
        # 移除序号
        content = re.sub(r'^\d+$', '', content, flags=re.MULTILINE)
        # 移除空行
        content = re.sub(r'\n\s*\n', '\n', content)
        # 移除特殊字符
        content = re.sub(r'[^\w\s。！？，：；（）\u4e00-\u9fff]', '', content)
        
        return content.strip()
    
    def _extract_chinese_topics(self, text):
        """提取中文主题"""
        topics = defaultdict(list)
        current_topic = "概述"
        
        # 分句
        sentences = re.split('[。！？]', text)
        
        for sentence in sentences:
            if not sentence.strip():
                continue
                
            # 使用jieba分词
            words = jieba.lcut(sentence)
            
            # 检查是否包含重要词汇作为新主题
            has_important = False
            for word in words:
                if word in self.important_words:
                    current_topic = sentence.strip()
                    has_important = True
                    break
            
            if not has_important:
                # 清理句子中的停用词
                cleaned_sentence = "".join([w for w in sentence if w not in self.stopwords])
                if cleaned_sentence:
                    topics[current_topic].append(cleaned_sentence)
        
        return topics
    
    def generate_markdown(self, topics):
        """生成Markdown格式的思维导图"""
        markdown = []
        indent = "  "
        
        # 添加标题
        markdown.append("# 内容大纲\n")
        
        # 添加主题和子主题
        for topic, subtopics in topics.items():
            if topic == "概述":
                markdown.append("## 主要内容\n")
            else:
                markdown.append(f"## {topic}\n")
            
            for subtopic in subtopics:
                if len(subtopic.strip()) > 0:
                    markdown.append(f"{indent}- {subtopic}\n")
            
            markdown.append("")  # 添加空行
            
        return "".join(markdown)

if __name__ == "__main__":
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 创建转换器实例
    converter = SRTToMindmap(language='zh')
    
    # 处理目录下的所有SRT文件
    converter.convert_directory(script_dir)
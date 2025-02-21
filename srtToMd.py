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
        
    def read_srt(self, filepath):
        """读取SRT文件内容"""
        print(f"正在读取文件: {filepath}")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"文件读取成功，内容长度: {len(content)} 字符")
            return content
        except Exception as e:
            print(f"读取文件出错: {e}")
            return None
    
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
        
        cleaned_content = content.strip()
        print(f"清理后的内容长度: {len(cleaned_content)} 字符")
        return cleaned_content
    
    def _extract_chinese_topics(self, text):
        """提取中文主题"""
        topics = defaultdict(list)
        current_topic = "概述"
        
        # 分句
        sentences = re.split('[。！？]', text)
        print(f"分句数量: {len(sentences)}")
        
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
        
        print(f"提取的主题数量: {len(topics)}")
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
        
        result = "".join(markdown)
        print(f"生成的Markdown内容长度: {len(result)} 字符")
        return result

    def convert(self, srt_file):
        """转换SRT文件为思维导图"""
        # 获取绝对路径
        srt_file = os.path.abspath(srt_file)
        print(f"\n开始处理文件: {srt_file}")
        
        # 验证文件是否存在
        if not os.path.exists(srt_file):
            print(f"错误: 文件 {srt_file} 不存在")
            return False
            
        # 获取文件名（不含扩展名）和输出路径
        file_base = os.path.splitext(srt_file)[0]
        output_file = f"{file_base}.md"
        print(f"输出文件路径: {output_file}")
        
        # 读取和清理内容
        content = self.read_srt(srt_file)
        if not content:
            print("错误: 文件读取失败")
            return False
            
        cleaned_content = self.clean_srt(content)
        if not cleaned_content:
            print("错误: 文件内容为空")
            return False
        
        # 提取主题
        topics = self._extract_chinese_topics(cleaned_content)
        
        # 生成markdown
        markdown = self.generate_markdown(topics)
        
        # 保存结果
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown)
            print(f"成功: 思维导图已保存到 {output_file}")
            return True
        except Exception as e:
            print(f"错误: 保存文件失败 - {e}")
            return False

def process_directory(directory_path, language='zh'):
    """处理指定目录下的所有SRT文件"""
    # 获取绝对路径
    directory_path = os.path.abspath(directory_path)
    print(f"\n开始处理目录: {directory_path}")
    
    if not os.path.exists(directory_path):
        print(f"错误: 目录 {directory_path} 不存在")
        return []
        
    converter = SRTToMindmap(language=language)
    processed_files = []
    
    # 遍历目录下的所有文件
    for filename in os.listdir(directory_path):
        if filename.lower().endswith('.srt'):
            file_path = os.path.join(directory_path, filename)
            success = converter.convert(file_path)
            if success:
                processed_files.append(filename)
    
    return processed_files

# 使用示例
if __name__ == "__main__":
    # 获取当前Python文件所在目录的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 1. 处理单个文件
    srt_file = input('/[4.2]--Chrome浏览器渲染机制内幕.srt' )
    srt_path = os.path.join(current_dir, srt_file)
    converter = SRTToMindmap(language='zh')
    converter.convert(srt_file)
    
    # 2. 或者处理整个目录
    # directory = input("请输入SRT文件所在目录路径: ")
    # processed_files = process_directory(directory)
    # print(f"\n处理完成的文件:")
    # for file in processed_files:
    #     print(f"- {file}")
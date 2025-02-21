import re
import jieba
from collections import defaultdict

class SRTToMindmap:
    def __init__(self, language='zh'):
        self.language = language  # 'zh' for Chinese, 'en' for English
        self.stopwords = set(['的', '了', '是', '在', '我', '和', '就', '都', '而', '及', '与', '这', '那'])
        self.important_words = set(['首先', '其次', '然后', '最后', '另外', '总之', '因此', '所以', '但是', '不过'])
        
    def read_srt(self, filepath):
        """读取SRT文件内容"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    
    def clean_srt(self, content):
        """清理SRT文件格式,只保留对话内容"""
        # 移除时间戳
        content = re.sub(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', '', content)
        # 移除序号
        content = re.sub(r'^\d+$', '', content, flags=re.MULTILINE)
        # 移除空行
        content = re.sub(r'\n\s*\n', '\n', content)
        return content.strip()
    
    def extract_topics(self, text):
        """提取主题和子主题"""
        if self.language == 'zh':
            return self._extract_chinese_topics(text)
        else:
            return self._extract_english_topics(text)
            
    def _extract_chinese_topics(self, text):
        """提取中文主题"""
        topics = defaultdict(list)
        current_topic = "主题"
        
        # 分句
        sentences = re.split('[。！？]', text)
        
        for sentence in sentences:
            if not sentence.strip():
                continue
                
            # 使用jieba分词
            words = jieba.lcut(sentence)
            
            # 检查是否包含重要词汇
            has_important = False
            for word in words:
                if word in self.important_words:
                    current_topic = sentence
                    has_important = True
                    break
            
            if not has_important:
                topics[current_topic].append(sentence)
        
        return topics
    
    def generate_markdown(self, topics):
        """生成Markdown格式的思维导图"""
        markdown = []
        indent = "  "
        
        # 添加标题
        markdown.append("# 内容大纲\n")
        
        # 添加主题和子主题
        for topic, subtopics in topics.items():
            markdown.append(f"## {topic}\n")
            
            for subtopic in subtopics:
                if len(subtopic.strip()) > 0:
                    # 去除停用词
                    cleaned = "".join([w for w in subtopic if w not in self.stopwords])
                    if len(cleaned) > 0:
                        markdown.append(f"{indent}- {cleaned}\n")
            
            markdown.append("")  # 添加空行
            
        return "".join(markdown)

    def convert(self, srt_file, output_file=None):
        """转换SRT文件为思维导图"""
        # 读取和清理内容
        content = self.read_srt(srt_file)
        cleaned_content = self.clean_srt(content)
        
        # 提取主题
        topics = self.extract_topics(cleaned_content)
        
        # 生成markdown
        markdown = self.generate_markdown(topics)
        
        # 保存或返回结果
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown)
            return f"思维导图已保存到 {output_file}"
        
        return markdown

# 使用示例
if __name__ == "__main__":
    # converter = SRTToMindmap(language='zh')  # 或 'en' 用于英文
    # result = converter.convert('./[4.2]--Chrome浏览器渲染机制内幕.srt')
    # print(result)

    srt_file = './[4.2]--Chrome浏览器渲染机制内幕.srt'  
    converter = SRTToMindmap(language='zh')
    converter.convert(srt_file)  # 将生成 example.md

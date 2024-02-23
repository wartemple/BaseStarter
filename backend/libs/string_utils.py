

class StringUtils:
    punctuation_chars = set([
        '｡', '。', ';', '；', '!', '?', '।', '॥', '၊', '။', '።', '፧', '፨', '᙮', '᠃', '᠉', '᱾', '᱿', '‼', '‽', '⁇', '⁈',
        '⁉', '⸮', '⸼', '꓿', '꘎', '꘏', '꡶', '꡷', '꧈', '꧉', '﹖', '﹗', '！', '．', '？', '𐩖', '𐩗', '𑁇', '𑁈', '𑅁', '𑅂', '𑅃',
        '\n'
    ])

    @classmethod
    def split_by_symbol(cls, string, sentence_length=None):
        sentences = []
        temp_text = ''
        temp_sentence = ''
        for word in string:
            temp_sentence += word
            # 没出现标点符号，直接跳过
            if word not in cls.punctuation_chars:
                continue
            # 情况一：指定句子长度
            if sentence_length is not None:
                # 子情况：长度不到，可正常合并
                if len(temp_sentence) + len(temp_text) <= sentence_length:
                    temp_text += temp_sentence
                    temp_sentence = ''
                    continue
                # 合并超出长度，若临时句子长度过长，就讲临时句子和临时文本进行清空
                elif len(temp_sentence) > sentence_length:
                    sentences.append(temp_text)
                    sentences.append(temp_sentence)
                    temp_text = ''
                    temp_sentence = ''
                    continue
                # 合并超出长度，若临时文本长度过长，就讲临时文本进行清空，
                else:
                    sentences.append(temp_text)
                    temp_text, temp_sentence = temp_sentence, ''
                    continue
            # 不指定分割长度，每个字符串都会进行字符串分割
            sentences.append(temp_sentence)
            temp_sentence = ''
        if temp_sentence or temp_text:
            temp_text += temp_sentence
            sentences.append(temp_text)
        return sentences

    @classmethod
    def hits_merge_highlight(self, hits):
        """
        hits = [{
            "content": "天安门今天的景色真的不错呀",
            "highlights": [
                {"word": "天安门", "suffix": "</span>", "prefix": "<span class='2'>", "start_index": 0, "end_index": 3},
                {"word": "天安门今天的景色", "suffix": "</span>", "prefix": "<span class='1'>", "start_index": 0, "end_index": 8},
                {"word": "景色", "suffix": "</span>", "prefix": "<span class='3'>", "start_index": 6, "end_index": 8},
                {"word": "不错", "suffix": "</span>", "prefix": "<span class='4'>", "start_index": 10, "end_index": 12},
            ]
        }]"""
        content = ''
        for hit in hits:
            hit['highlights'].sort(key=lambda x: (x['start_index'], -len(x['word'])))
            add_all_index = 0
            add_prefix_index = 0
            raw_end_index = 0
            raw_start_index = 0
            for highlight in hit['highlights']:
                start_index = highlight["start_index"]
                end_index = highlight["end_index"]
                # # 第一种起始的大于结束
                if start_index > raw_end_index:
                    start_index += add_all_index
                    end_index += add_all_index
                # 相交的情况直接丢弃
                elif start_index < raw_end_index and end_index > raw_end_index and start_index != raw_start_index:
                    continue
                # 嵌套的情况
                else:
                    start_index += add_prefix_index
                    end_index += add_prefix_index
                # 替换
                highlight_word = f"{highlight['prefix']}{highlight['word']}{highlight['suffix']}"
                # 只有出现最大的后缀索引才进行替换
                if highlight["end_index"] > raw_end_index:
                    raw_end_index = highlight["end_index"]
                raw_start_index = highlight["start_index"]
                hit['content'] = hit['content'][:start_index] + highlight_word + hit['content'][end_index:]
                add_prefix_index = add_all_index + len(highlight['prefix'])
                add_all_index += len(highlight['prefix']) + len(highlight['suffix'])
            content += hit['content']
        return content
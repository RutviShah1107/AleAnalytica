class SplitText():
    def __init__(self):
          pass
    def split_text(self, text, max_chars=30):
        if type(text) != str and type(text) != list:
          return ""
        lines = []
        line = ""
        for word in text.split():
            if len(line) + len(word) <= max_chars:
                line += (word + " ")
            else:
                lines.append(line)
                line = word + " "
        if line:
            lines.append(line)
        return "<br>".join(lines)

    def split_dict_text(self, data, max_chars=30):
      try:
        return {key: self.split_text(value, max_chars) for key, value in data.items()}
      except:
        return {key: [self.split_text(text, max_chars) for text in value] for key, value in data.items()}

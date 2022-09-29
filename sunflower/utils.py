def save_html(file_path, html):
   html = html.encode()
   with open(file_path, "wb") as f:
      f.write(html)

def load_html(file_path):
   with open(file_path, "rb") as f:
      return f.read().decode()

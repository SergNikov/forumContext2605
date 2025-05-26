import gradio as gr
import datetime

class Message:
    def __init__(self, id, author, title, text, slot_name=None, parent_id=None):
        self.id = id
        self.author = author
        self.title = title
        self.text = text
        self.slot_name = slot_name
        self.parent_id = parent_id
        self.created_at = datetime.datetime.now()
        self.children = []

    def display(self, indent=0):
        slot_info = f"[слот: {self.slot_name}]" if self.slot_name else ""
        return "  " * indent + f"{self.id}. {self.title} {slot_info} от {self.author} ({self.created_at.strftime('%Y-%m-%d %H:%M')}):\n" + \
               "  " * indent + f"→ {self.text}\n" + \
               "\n".join(child.display(indent + 1) for child in self.children)

class Forum:
    def __init__(self):
        self.messages = {}
        self.next_id = 1

    def add_message(self, author, title, text, slot_name=None, parent_id=None):
        msg = Message(self.next_id, author, title, text, slot_name, parent_id)
        self.messages[self.next_id] = msg
        if parent_id:
            self.messages[parent_id].children.append(msg)
        self.next_id += 1

    def show_all(self):
        return "\n— Текущая структура обсуждения —\n\n" + \
               "\n".join(msg.display() for msg in self.messages.values() if msg.parent_id is None)

forum = Forum()

def add_message_interface(author, title, text, slot_name=None, parent_id=None):
    parent_id = int(parent_id) if parent_id else None
    forum.add_message(author, title, text, slot_name, parent_id)
    return forum.show_all()

with gr.Blocks() as demo:
    gr.Markdown("## Форум")
    with gr.Row():
        with gr.Column():
            author = gr.Textbox(label="Автор")
            title = gr.Textbox(label="Заголовок")
            text = gr.Textbox(label="Текст")
            slot_name = gr.Textbox(label="Название слота (необязательно)")
            parent_id = gr.Textbox(label="ID родительского сообщения (необязательно)")
            submit = gr.Button("Добавить сообщение")
        with gr.Column():
            output = gr.Textbox(label="Структура обсуждения", lines=20)

    submit.click(add_message_interface, inputs=[author, title, text, slot_name, parent_id], outputs=output)

if __name__ == "__main__":
    demo.launch()
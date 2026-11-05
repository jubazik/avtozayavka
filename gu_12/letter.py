from docxtpl import DocxTemplate

def save_docx(zayavka):
    result = "_".join(str(n)[-3:] for n in zayavka.wagons)

    doc = DocxTemplate('../templates/zayavka.docx') # путь к шаблону
    context = {
        'month': zayavka.month,
        'decade': zayavka.ordinal_to_words(),
        'count_text': zayavka.count_text(),
        'wagons': ", ".join(zayavka.wagons),
    }
    doc.render(context)

    path = f'output/zayavka_{result}.docx'
    doc.save(path)
    return path

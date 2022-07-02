import os
import uuid
from flask import Flask, render_template, request, send_file
import shutil
from docx2pdf import convert
from pdftools.pdftools import pdf_add, pdf_copy, pdf_insert, pdf_merge, pdf_remove, pdf_rotate, pdf_split, pdf_zip

app = Flask(__name__)


@app.route('/')
def form():
    return render_template("index.html")


@app.route('/merge')
def merge():
    return render_template("buttons/merge.html")


@app.route('/merge/transaction', methods=["POST"])
def merge_view():
    files = request.files.getlist('data_files')
    if not files:
        return('No file')

    userpath, userUUIDString = open_user_folder()

    i = 0
    destination_file_paths = []
    for file in files:

        destination_file_paths.append(userpath + '\\file'+str(i)+'.pdf')
        destination_file1 = open(destination_file_paths[i], 'wb')
        shutil.copyfileobj(file, destination_file1)
        i += 1

    pdf_merge(inputs=(destination_file_paths), output=userpath+"\\output.pdf")

    return send_file('files\\'+userUUIDString+'\\output.pdf', as_attachment=True)


@app.route('/add')
def add():
    return render_template("buttons/add.html")


@app.route('/add/transaction', methods=["POST"])
def add_view():
    request_file1 = request.files['data_file1']
    if not request_file1:
        return "No file"

    request_file2 = request.files['data_file2']
    if not request_file2:
        return "No file"

    userpath, userUUIDString = open_user_folder()
    source_file1 = request_file1
    destination_file_path1 = userpath + '\\file1.pdf'
    destination_file1 = open(destination_file_path1, 'wb')
    shutil.copyfileobj(source_file1, destination_file1)
    source_file2 = request_file2
    destination_file_path2 = userpath + '\\file2.pdf'
    destination_file2 = open(destination_file_path2, 'wb')
    shutil.copyfileobj(source_file2, destination_file2)

    request_file3 = request.form.get('data_file3')
    if request_file3:
        str_list = request_file3.split()
        pdf_add(destination_file_path1, destination_file_path2,
                str_list, userpath+"\\output.pdf")
    else:
        pdf_add(dest=(destination_file_path1), source=(
            destination_file_path2), output=(userpath+"\\output.pdf"), pages=None)

    return send_file('files\\'+userUUIDString+'\\output.pdf', as_attachment=True)


@app.route('/copy')
def copy():
    return render_template("buttons/copy.html")


@app.route('/copy/transaction', methods=["POST"])
def copy_view():
    request_file1 = request.files['data_file1']
    if not request_file1:
        return "No file"

    userpath, userUUIDString = open_user_folder()
    source_file1 = request_file1
    destination_file_path1 = userpath + '\\file1.pdf'
    destination_file1 = open(destination_file_path1, 'wb')
    shutil.copyfileobj(source_file1, destination_file1)

    request_input1 = request.form.get('input1')
    if not request_input1:
        return "No input"
    str_list = request_input1.split()
    pdf_copy(destination_file_path1, userpath+"\\output.pdf", str_list)

    return send_file('files\\'+userUUIDString+'\\output.pdf', as_attachment=True)


@app.route('/insert')
def insert():
    return render_template("buttons/insert.html")


@app.route('/insert/transaction', methods=["POST"])
def insert_view():
    request_file1 = request.files['data_file1']
    if not request_file1:
        return "No file"

    request_file2 = request.files['data_file2']
    if not request_file2:
        return "No file"

    userpath, userUUIDString = open_user_folder()
    source_file1 = request_file1
    destination_file_path1 = userpath + '\\file1.pdf'
    destination_file1 = open(destination_file_path1, 'wb')
    shutil.copyfileobj(source_file1, destination_file1)
    source_file2 = request_file2
    destination_file_path2 = userpath + '\\file2.pdf'
    destination_file2 = open(destination_file_path2, 'wb')
    shutil.copyfileobj(source_file2, destination_file2)
    request_file4 = request.form.get('input2')
    if not request_file4:
        return "No file"
    else:
        request_file4 = int(request_file4)
    request_file3 = request.form.get('input1')
    if request_file3:
        str_list = request_file3.split()
        # num_list=[]
        # for i in str_list:
        #     num_list.append(int(i))
        pdf_insert(dest=(destination_file_path2), source=(destination_file_path1), output=(
            userpath+"\\output.pdf"), pages=str_list, index=request_file4)
    else:
        pdf_insert(dest=(destination_file_path2), source=(destination_file_path1), output=(
            userpath+"\\output.pdf"), pages=None, index=request_file4)

    return send_file('files\\'+userUUIDString+'\\output.pdf', as_attachment=True)


@app.route('/remove')
def remove():
    return render_template("buttons/remove.html")


@app.route('/remove/transaction', methods=["POST"])
def remove_view():
    request_file1 = request.files['data_file1']
    if not request_file1:
        return "No file"

    userpath, userUUIDString = open_user_folder()
    source_file1 = request_file1
    destination_file_path1 = userpath + '\\file1.pdf'
    destination_file1 = open(destination_file_path1, 'wb')
    shutil.copyfileobj(source_file1, destination_file1)

    request_input1 = request.form.get('input1')
    if not request_input1:
        return "No input"
    str_list = request_input1.split()
    # num_list=[]
    # for i in str_list:
    #     num_list.append(int(i))
    pdf_remove(destination_file_path1, str_list, userpath+"\\output.pdf")

    return send_file('files\\'+userUUIDString+'\\output.pdf', as_attachment=True)


@app.route('/rotate')
def rotate():
    return render_template("buttons/rotate.html")


@app.route('/rotate/transaction', methods=["POST"])
def rotate_view():
    request_file1 = request.files['data_file1']
    if not request_file1:
        return "No file"

    userpath, userUUIDString = open_user_folder()
    source_file1 = request_file1
    destination_file_path1 = userpath + '\\file1.pdf'
    destination_file1 = open(destination_file_path1, 'wb')
    shutil.copyfileobj(source_file1, destination_file1)

    request_input1 = request.form.get('input1')
    if not request_input1:
        str_list = None
    else:
        str_list = request_input1.split()
    
    request_file4 = request.form.get('input2')
    if not request_file4:
        request_file4 = 90
    else:
        request_file4 = int(request_file4)
    pdf_rotate(destination_file_path1, request_file4,
               False, str_list, userpath+"\\output.pdf")

    return send_file('files\\'+userUUIDString+'\\output.pdf', as_attachment=True)


@app.route('/rotate/transaction/left', methods=["POST"])
def rotate_view_right():
    request_file1 = request.files['data_file1']
    if not request_file1:
        return "No file"

    userpath, userUUIDString = open_user_folder()
    source_file1 = request_file1
    destination_file_path1 = userpath + '\\file1.pdf'
    destination_file1 = open(destination_file_path1, 'wb')
    shutil.copyfileobj(source_file1, destination_file1)

    request_input1 = request.form.get('input1')
    if not request_input1:
        str_list = None
    else:
        str_list = request_input1.split()
    
    request_file4 = request.form.get('input2')
    if not request_file4:
        request_file4 = 90
    else:
        request_file4 = int(request_file4)
    pdf_rotate(destination_file_path1, request_file4,
               True, str_list, userpath+"\\output.pdf")

    return send_file('files\\'+userUUIDString+'\\output.pdf', as_attachment=True)


@app.route('/split')
def split():
    return render_template("buttons/split.html")


@app.route('/split/transaction', methods=["POST"])
def split_view():
    request_file1 = request.files['data_file1']
    if not request_file1:
        return "No file"

    userpath, userUUIDString = open_user_folder()
    os.mkdir(userpath+"\\outputs")
    source_file1 = request_file1
    destination_file_path1 = userpath + '\\file1.pdf'
    destination_file1 = open(destination_file_path1, 'wb')
    shutil.copyfileobj(source_file1, destination_file1)

    request_input1 = request.form.get('input1')
    if not request_input1:
        num_list = None
    else:
        str_list = request_input1.split()
        num_list = []
        for i in str_list:
            num_list.append(i)

    request_input2 = request.form.get('input2')
    if (not request_input1) and (not request_input2):
        return render_template("buttons/split.html")

    if not request_input2:
        request_input2 = None
    else:
        request_input2 = int(request_input2)

    pdf_split(destination_file_path1, userpath +
              "\\outputs\\output", request_input2, num_list)

    def make_archive(source, destination):
        base = os.path.basename(destination)
        name = base.split('.')[0]
        format = base.split('.')[1]
        archive_from = os.path.dirname(source)
        archive_to = os.path.basename(source.strip(os.sep))
        shutil.make_archive(name, format, archive_from, archive_to)
        shutil.move('%s.%s' % (name, format), destination)

    make_archive(userpath+"\\outputs", userpath+"\\output.zip")
    return send_file('files\\'+userUUIDString+'\\output.zip', as_attachment=True)


@app.route('/zip')
def zip():
    return render_template("buttons/zip.html")


@app.route('/zip/transaction', methods=["POST"])
def zip_view():
    request_file1 = request.files['data_file1']
    if not request_file1:
        return "No file"

    request_file2 = request.files['data_file2']
    if not request_file2:
        return "No file"

    userpath, userUUIDString = open_user_folder()
    source_file1 = request_file1
    destination_file_path1 = userpath + '\\file1.pdf'
    destination_file1 = open(destination_file_path1, 'wb')
    shutil.copyfileobj(source_file1, destination_file1)
    source_file2 = request_file2
    destination_file_path2 = userpath + '\\file2.pdf'
    destination_file2 = open(destination_file_path2, 'wb')
    shutil.copyfileobj(source_file2, destination_file2)
    pdf_zip(destination_file_path1, destination_file_path2,
            userpath+"\\output.pdf")
    return send_file('files\\'+userUUIDString+'\\output.pdf', as_attachment=True)

@app.route('/doc-to-pdf')
def route():
    return render_template("buttons/doc-to-pdf.html")


@app.route('/doc-to-pdf/transaction', methods=["POST"])
def route_view():
    request_file1 = request.files['data_file1']
    if not request_file1:
        return "No file"

    userpath, userUUIDString = open_user_folder()
    source_file1 = request_file1
    destination_file_path1 = userpath + '\\file1.docx'
    destination_file1 = open(destination_file_path1, 'wb')
    shutil.copyfileobj(source_file1, destination_file1)
    
    convert(destination_file_path1,userpath+"\\output.pdf")
    return send_file('files\\'+userUUIDString+'\\output.pdf', as_attachment=True)

def open_user_folder():
    userUUID = uuid.uuid4()
    userUUIDString = str(userUUID)
    userpath = 'app\\files\\'+userUUIDString
    os.mkdir(userpath)
    return userpath, userUUIDString

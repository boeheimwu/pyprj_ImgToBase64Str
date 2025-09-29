#pip install img2html (已內含 pillow/PIL)
import os
import base64
import sys
from PIL import Image
#from img2html.converter import Img2HTMLConverter

def img_def_extensions():
    # 支援的圖片副檔名
    supported_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp")
    return supported_extensions

def target_html_name():
    return "output.html"

def working_dir():
    folder_path = "./"  
    return folder_path
    
def img_to_htmlimg():    
    folder_path = working_dir()
    html_output_file = target_html_name()
    # 支援的圖片副檔名
    supported_extensions = img_def_extensions()
    
    # 取得資料夾內所有圖片檔
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(supported_extensions)]
    image_files_len = len(image_files)
    print(f"[start :: img_to_htmlimg],image_files: {image_files_len}")
    
    # 建立 table 的 rows
    table_rows = ""
    for img_file in image_files:
        file_path = os.path.join(folder_path, img_file)
        
        # 檢查檔案是否存在
        if not os.path.isfile(file_path):
            print(f"檔案不存在: {file_path}")
            continue
    
        # 取得檔名
        file_name = os.path.basename(file_path)
        
        # 取得檔案大小 KB
        file_size_kb = round(os.path.getsize(file_path) / 1024, 2)
        
        # 使用 Img2HTMLConverter 轉換圖片為 base64 的 <img> tag
        # 這是因為在 Python 3 中，字串（str）已經是 Unicode 格式，並不需要再進行解碼 decode()）。然而， 套件的某些版本仍然包含了 .decode('utf-8')
        #converter = Img2HTMLConverter()
        #img_tag = converter.convert(file_path)
        with open(file_path, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode("utf-8")
    
        # 生成 <img> 標籤
        img_tag = f'<img src="data:image/{img_file.name.split(".")[-1]};base64,{img_base64}" />'
        
        # 建立 table row
        table_rows += f"""
            <tr>
                <td>{file_name}</td>
                <td>{file_size_kb} KB</td>
                <td>{img_tag}</td>
            </tr>
        """
    
    # 建立完整 HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <title>圖片資訊表</title>
    </head>
    <body>
        <table border="1">
            <tr>
                <th>檔名</th>
                <th>檔案大小 (KB)</th>
                <th>圖片</th>
            </tr>
            {table_rows}
        </table>
    </body>
    </html>
    """
    
    # 寫入 HTML 檔案
    with open(html_output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"[target_html is done]: {html_output_file}")
    #print(f"共 {len(image_files)} 張圖片已加入 table。")
    
def get_img_cnt():
    folder_path = working_dir()
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(img_def_extensions())]
    image_files_len = len(image_files)
    return image_files_len
    
def get_imgFn_join(sep):
    folder_path = working_dir()
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(img_def_extensions())]
    # https://stackoverflow.com/questions/53832607
    return sep.join(image_files)  
    
def begin_copy_with_jpg(fn):
    #print ("begin_copy_with_jpg")
    file_name = os.path.basename(fn)
    file = os.path.splitext(file_name)
    #print(file)  # returns tuple of string --> 輸出內容 ('1', '.jpg')
    print(f"[copy_src]fileName= {file[0]},extension={file[1]}")

    # 讀取輸入檔 (JPG)
    img = Image.open(fn)

    # 轉存為 PNG
    img.save(file[0]+".png", "PNG")

    # 轉存為 BMP
    img.save(file[0]+".bmp", "BMP")

    # 轉存為 GIF
    img.save(file[0]+".gif", "GIF")

def begin_copy_with_png(fn):
    #print ("begin_copy_with_png")
    file_name = os.path.basename(fn)
    file = os.path.splitext(file_name)
    #print(file)  # returns tuple of string --> 輸出內容 ('1', '.jpg')
    print(f"[copy_src]fileName= {file[0]},extension={file[1]}")
    
    img = Image.open(fn)
    
    # 轉存為 JPG
    img.convert("RGB").save(file[0]+".jpg", "JPEG")  # PNG 可能有透明通道，需要轉成 RGB

    # 轉存為 BMP
    img.save(file[0]+".bmp", "BMP")

    # 轉存為 GIF
    img.save(file[0]+".gif", "GIF")

def task_clean():
    print(f"[task_clean]")
    folder_path = working_dir()
    # 針對 html
    html_output_file = target_html_name()
    
    dc_exist_file = os.path.join(folder_path, html_output_file) 
    # 檢查檔案是否存在
    if os.path.isfile(dc_exist_file):
        os.remove(dc_exist_file)
        print (f"[remove :: html]:{html_output_file}")
    else:
        print (f"contains 0 html")
    
    if get_img_cnt()==0 :
        print (f"contains 0 image")
    else:
        # 支援的圖片副檔名
        supported_extensions = img_def_extensions()
        # 取得資料夾內所有圖片檔
        image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(supported_extensions)]
        for f in image_files:
            dc_file_name = os.path.basename(f)
            os.remove(f)
            print (f"[remove :: img]{dc_file_name}")

def task_gen():
    if get_img_cnt()==0 :
        print(f"[task_gen]no img exist")

    if get_img_cnt()==1 :
        singleImg = get_imgFn_join("|")
        if singleImg.lower().endswith(".png"):
            begin_copy_with_png(singleImg)
        if singleImg.lower().endswith(".jpg"):
            begin_copy_with_jpg(singleImg)

    if get_img_cnt()>=1 :
        img_to_htmlimg()

def main():
    if len(sys.argv)==2:
        if(sys.argv[1]=="C"):
            task_clean()
        elif(sys.argv[1]=="G"):
            task_gen()
        else:
            print("unknown parameter:", sys.argv[1])  
    elif len(sys.argv)==1:
            print("must enter taks_param[(C)lean, (G)en]")  
            print("python appCoder.py C")  
            print("python appCoder.py G")  

# python appCoder.py C
# python appCoder.py G
if __name__=="__main__":
    main()
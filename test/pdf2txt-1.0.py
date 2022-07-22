import os
import PyPDF2
from multiprocessing import Pool
from tqdm import tqdm
path = "E:/pdf2txt/年报/"
path_result = "E:/pdf2txt/完成txt/"
os.chdir(path)#os.chdir() 方法用于改变当前工作目录到指定的路径
dirlist = os.listdir(path)

def dir_pdf2txt(dir_name):
    path_new = path+dir_name
    filelist = os.listdir(path_new)
    result_path = path_result + dir_name
    if os.path.isdir(result_path):
        pass
    else:
        os.mkdir(result_path)   
    for pdf_name in filelist:
        path_pdf_name = path_new+"/"+pdf_name
        pdf_name_list=list(pdf_name)
        if "".join(pdf_name_list[-4:None]).lower()==".pdf":
            txt_name="".join(pdf_name_list[None:-4])+".txt"
            path_txt_name=result_path+"/"+txt_name
        else:
            with open(path_result+"非pdf文件.csv","a",encoding='utf-8') as file:
                file.write('%s\n' % (path_pdf_name))
                continue
        if os.path.isfile(path_txt_name):
            continue
        else:
            pdfReader=PyPDF2.PdfReader(path_pdf_name)
            text=""
            for i,page in enumerate(pdfReader.pages):
                try:
                    text+=page.extract_text()
                except Exception as e:
                    with open(path_result+"extract_text_error.csv","a",encoding='utf-8') as file:
                        import traceback
                        file.write('%s,%s,"%s"\n' % (path_pdf_name,i,traceback.format_exc().replace('"',"'")))
                        continue
            # try:
            #     with open(path_txt_name,"a",encoding='utf-16',errors="replace") as file:
            #         file.writelines(text)
            # except:
            #     with open(path_result+"写入异常文件.csv","a",encoding='utf-8') as file:
            #         file.write('%s\n' % (path_pdf_name))

if __name__=="__main__":
    with Pool(6) as par:
        for _ in tqdm(par.imap_unordered(dir_pdf2txt,dirlist) , total=len(dirlist),bar_format='{l_bar}{bar:50}{r_bar}{bar:-10b}'):
            pass
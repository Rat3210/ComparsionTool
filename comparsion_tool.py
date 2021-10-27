from genericpath import isdir
import os
import logging
import filecmp
from difflib import HtmlDiff
import inspect
import datetime
import glob

target_lists = []
diff_lists = []
not_FD_files = []
date_now = datetime.datetime.now()
date_str = f'{date_now.year}{date_now.month}{date_now.day}_{date_now.hour}{date_now.minute}{date_now.second}'

def setup_debug():
  global logger
  logger = logging.getLogger('DebugTest')
  if not os.path.isdir('log'):
    os.makedirs('log')
  log_file = logging.FileHandler('log\\DebugLog.log')
  logger.setLevel(logging.DEBUG)
  logger.addHandler(log_file)
  formatter = logging.Formatter('%(asctime)s:%(lineno)d:%(levelname)s:%(message)s')
  log_file.setFormatter(formatter)

def get_target_conf(target):
  logger.info(f'{inspect.currentframe().f_code.co_name}')
  directory = f'target\\{target}'
  tmp_list = []
  for current, subfolder, subfiles in os.walk(directory):
    for file in subfiles:
      tmp_list.append(os.path.join(current, file))
  return tmp_list

def get_target_directory():
  logger.info(f'{inspect.currentframe().f_code.co_name}')
  exe_path = ".\\target"
  tmp_dir = os.listdir(exe_path)
  tmp_dir = [f for f in tmp_dir if os.path.isdir(os.path.join(exe_path, f))]
  return tmp_dir

def get_files():
  logger.info(f'{inspect.currentframe().f_code.co_name}')
  global target_lists
  target_lists = get_target_directory()
  if len(target_lists) < 2:
    err_title = 'There are not enough folders.'
    message = 'targetフォルダに格納されている比較対象のフォルダ数が足りません。\n比較したいフォルダを2つ格納してください。'
    logger.error(f'{inspect.currentframe().f_code.co_name}-[There are not enough folders.]')
    push_code(err_title, message, 1)
  elif len(target_lists) > 2:
    err_title = 'There are too many folders.'
    message = 'targetフォルダに格納されている比較対象のフォルダ数が多過ぎです。\n比較したいフォルダを2つ格納してください。'
    logger.error(f'{inspect.currentframe().f_code.co_name}-[There are too many folders.]')
    push_code(err_title, message, 1)
  for target in target_lists:
    diff_lists.append(get_target_conf(target))
  
def make_diff_html(comp_sour, comp_dest, html_name):
  logger.info(f'{inspect.currentframe().f_code.co_name}')
  comp_sour = f'.\\{comp_sour}'
  comp_dest = f'.\\{comp_dest}'
  html_name = f'diff_html\\{html_name}.html'
  df = HtmlDiff(tabsize = 16, wrapcolumn = 74)

  with  open(comp_sour, 'r') as f:
    comp_sour = f.readlines()
  
  with  open(comp_dest, 'r') as f:
    comp_dest = f.readlines()
  
  make_dir('diff_html')
  
  with  open(html_name, 'w') as html:
    html.writelines(df.make_file(comp_sour, comp_dest))

def make_dir(dir_name):
  logger.info(f'{inspect.currentframe().f_code.co_name}')
  dir_name = f'.\\{dir_name}\\'
  if not os.path.isdir(dir_name):
    os.makedirs(dir_name)

def check_file_exist(sour_file, dest_list, target_num):
  logger.info(f'{inspect.currentframe().f_code.co_name}')
  new_dirname = target_lists[0]
  old_dirname = target_lists[target_num]

  if target_num == 0:
    new_dirname = target_lists[1]
  
  sour_file = sour_file.replace(old_dirname, new_dirname)

  if sour_file in dest_list:
    return True
  else:
    return False

def get_diff_num(sour_file, dest_list, target_num):
  logger.info(f'{inspect.currentframe().f_code.co_name}')
  new_dirname = target_lists[0]
  old_dirname = target_lists[target_num]

  if target_num == 0:
    new_dirname = target_lists[1]
    target_num = 1
  else:
    target_num = 0
      
  sour_file = sour_file.replace(old_dirname, new_dirname)
  return dest_list.index(sour_file)

def check_file_diff(comp_sour, comp_dest):
  logger.info(f'{inspect.currentframe().f_code.co_name}')
  return filecmp.cmp(comp_sour, comp_dest, shallow = True)

def check_diff():
  logger.info(f'{inspect.currentframe().f_code.co_name}')
  for list_num in range(len(diff_lists)):
    for file_num in range(len(diff_lists[list_num])):
      if list_num == 0:
        if check_file_exist(diff_lists[list_num][file_num], diff_lists[1], list_num):
          diff_num = get_diff_num(diff_lists[list_num][file_num], diff_lists[1], list_num)
          if check_file_diff(diff_lists[list_num][file_num], diff_lists[1][diff_num]):
            continue
          else:
            html_name = f'【Diff_result】{target_lists[0]}_{target_lists[1]}_{diff_lists[list_num][file_num]}'
            html_name = html_name.replace('.','_')
            html_name = html_name.replace('\\','_')

            make_diff_html(diff_lists[list_num][file_num], diff_lists[1][diff_num], html_name)
        else:
          not_FD_files.append(diff_lists[list_num][file_num])
      elif list_num == 1:
        if check_file_exist(diff_lists[list_num][file_num], diff_lists[0], list_num):
          continue
        else:
          not_FD_files.append(diff_lists[list_num][file_num])

def push_code(title, message, code_num):
  logger.info(f'{inspect.currentframe().f_code.co_name}')
  if code_num == 0:
    code = 'NORMAL'
  elif code_num == 1:
    code = 'ERROR'

  print(f'\n\n**********【code】{code}:{title}**********')
  print('\nComment：')
  print(f'{message}')
  print('\n**********************************************************')

  if code_num == 1:
    print('\nプログラムを終了します。')
    input('エンターキーを押して、処理を終了してください。\nPress the Enter key to end the process.')
    exit()

def first_process():
  logger.info(f'{inspect.currentframe().f_code.co_name}')
  print('==========================================================')
  print('コンフィグ比較プログラムを実行します。')
  print('==========================================================')

  if not os.path.isdir('.\\target'):
    make_dir('target') 
    message = 'targetフォルダが確認出来なかったため、targetフォルダを作成します。\n比較したいコンフィグファイルの入ったフォルダを2つ用意し、targetフォルダへ格納してください。'
    err_title = 'The target folder cannot be found.'
    logger.error(f'{inspect.currentframe().f_code.co_name}-[First problem check completed.]')
    push_code(err_title, message, 1)
  
  title = 'First problem check completed.'
  message = 'targetフォルダの存在を確認しました。\n各種正常性を確認しながらコンフィグ比較プロセスを実行します。'
  logger.info(f'{inspect.currentframe().f_code.co_name}-[Completed successfully]')
  push_code(title, message, 0)


def end_process():
  logger.info(f'{inspect.currentframe().f_code.co_name}')
  title = 'All processes completed successfully'
  message = '全てのプロセスは正常に完了しました。\n差分のあるファイルが見つかった場合はdiff_htmlフォルダを作成し、結果をHTMLファイルで保存しています。\n中身を確認してください。\nプログラムを終了します。'

  push_code(title, message, 0)
  
  input('エンターキーを押して、処理を終了してください。\nPress the Enter key to end the process.')
  exit()

def export_nfd_files(nfd_files, diff1, diff2):
  logger.info(f'{inspect.currentframe().f_code.co_name}')
  if len(nfd_files) > 0:
    logger.debug(f'{inspect.currentframe().f_code.co_name}[date_str]：{date_str}')
    make_dir('log\\NotFoundFiles')
    filepath = f'.\\log\\NotFoundFiles\\【NotFoundFiles】{diff1}_{diff2}_{date_str}.txt'
    logger.debug(f'{inspect.currentframe().f_code.co_name}[filepath]：{filepath}')
    f = open(filepath, 'w')
    for file in nfd_files:
      f.write(file + '\n')

def export_file_paths(diff1, diff2):
  logger.info(f'{inspect.currentframe().f_code.co_name}')
  if len(diff_lists) > 0:
    logger.debug(f'{inspect.currentframe().f_code.co_name}[date_str]：{date_str}')
    make_dir('log\\FilePathList')
    filepath = f'.\\log\\FilePathList\\【FilePathList】{diff1}_{diff2}_{date_str}.txt'
    logger.debug(f'{inspect.currentframe().f_code.co_name}[filepath]：{filepath}')
    f = open(filepath, 'w')
    for list in diff_lists:
      for file in list:
        f.write(file + '\n')

def export_dir_paths():
  logger.info(f'{inspect.currentframe().f_code.co_name}')
  make_dir('log\\DirList')
  for target in target_lists:
    filepath = f'.\\log\\DirList\\{target}_{date_str}.txt'
    target_dirs = []
    target_dirs = glob.glob(f'.\\target\\{target}\\**\\', recursive = True)
    f = open(filepath, 'w')
    for dir in target_dirs:
      f.write(dir + '\n')

def main_process():
  get_files()
  check_diff()

def export_process():
  export_nfd_files(not_FD_files, target_lists[0], target_lists[1])
  export_file_paths(target_lists[0], target_lists[1])
  export_dir_paths()

#処理実行:Processing execution
setup_debug()
first_process()
main_process()
export_process()
end_process()
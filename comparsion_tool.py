from genericpath import isdir
import os
import logging
import filecmp
from difflib import HtmlDiff
import inspect
import datetime
import glob
from tqdm import tqdm

target_lists = []
diff_lists = []
not_FD_files = []
sum_lists = []
date_now = datetime.datetime.now()
date_str = f'{date_now:%Y%m%d}_{date_now:%H%M%S}'

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
  logger.info(f'{inspect.currentframe().f_code.co_name}:Ready')

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
    message = 'targetフォルダに格納されている比較対象のフォルダ数が足りません。\n\
      比較したいフォルダを2つ格納してください。'
    
    logger.error(f'{inspect.currentframe().f_code.co_name}-[There are not enough folders.]')
    push_code(err_title, message, 1)
  for target in target_lists:
    diff_lists.append(get_target_conf(target))
  
def make_diff_html(comp_sour, comp_dest, html_name, dir_name):
  logger.info(f'{inspect.currentframe().f_code.co_name}')

  comp_sour = f'.\\{comp_sour}'
  comp_dest = f'.\\{comp_dest}'
  html_name = f'{dir_name}\\{date_str}\\{html_name}.html'
  df = HtmlDiff(tabsize = 16, wrapcolumn = 74)

  with  open(comp_sour, 'r') as f:
    comp_sour = f.readlines()
  
  with  open(comp_dest, 'r') as f:
    comp_dest = f.readlines()
  
  make_dir(f'{dir_name}')
  make_dir(f'{dir_name}\\{date_str}')
  
  with  open(html_name, 'w') as html:
    html.writelines(df.make_file(comp_sour, comp_dest))

def make_dir(dir_name):
  logger.info(f'{inspect.currentframe().f_code.co_name}')

  dir_name = f'.\\{dir_name}\\'
  if not os.path.isdir(dir_name):
    os.makedirs(dir_name)

def check_file_exist(sour_file, dest_list, old_dir_num, new_dir_num):
  logger.info(f'{inspect.currentframe().f_code.co_name}')

  sour_file = sour_file.replace(target_lists[old_dir_num], target_lists[new_dir_num])

  if sour_file in dest_list:
    return True
  else:
    return False

def get_diff_num(sour_file, dest_list, old_dir_num, new_dir_num):
  logger.info(f'{inspect.currentframe().f_code.co_name}')

  sour_file = sour_file.replace(target_lists[old_dir_num], target_lists[new_dir_num])
  return dest_list.index(sour_file)

def check_file_diff(comp_sour, comp_dest):
  logger.info(f'{inspect.currentframe().f_code.co_name}')

  return filecmp.cmp(comp_sour, comp_dest, shallow = True)

def check_diff():
  logger.info(f'{inspect.currentframe().f_code.co_name}')

  progress_total = 0
  i = len(target_lists)
  for target_num in range(len(target_lists)):
    progress_total += len(diff_lists[target_num]) * (i - 1)
    i -= 1
  
  progress_bar = tqdm(total = progress_total)
  progress_bar.set_description('Difference progress confirmation.')
  
  for target_num in range(len(target_lists)):
    logger.debug(f'{inspect.currentframe().f_code.co_name}-[for[target_num]]')
    if target_num >= 1:
      logger.debug(f'{inspect.currentframe().f_code.co_name}-[for[target_num]_if[target_num]-True:[target_num]{target_num}]')

      for reverse_num in reversed(range(0, target_num)):
        logger.debug(f'{inspect.currentframe().f_code.co_name}-[for[target_num]_if[target_num]-True_for[reverse_num]:[reverse_num]{reverse_num}]')

        for file_num in range(len(diff_lists[target_num])): 
          if check_file_exist(diff_lists[target_num][file_num], diff_lists[reverse_num], target_num, reverse_num):
            logger.debug(f'{inspect.currentframe().f_code.co_name}-[for[target_num]_if[target_num]-True_for[reverse_num]_for[file_num]_if[check_file_exist]-True:continue')

            continue
          else:
            logger.debug(f'{inspect.currentframe().f_code.co_name}-[for[target_num]_if[target_num]-True_for[reverse_num]_for[file_num]_if[check_file_exist]-False:NFD.append')

            not_FD_files.append(f'{target_lists[target_num]}_{target_lists[reverse_num]}:{diff_lists[target_num][file_num]}')
    if target_num == len(target_lists) - 1:
      logger.debug(f'{inspect.currentframe().f_code.co_name}-[for[target_num]_if[target_num]-False:continue')
      continue
    for file_num in range(len(diff_lists[target_num])):
      logger.debug(f'{inspect.currentframe().f_code.co_name}-[for[target_num]_for[file_num]:[file_num:{file_num}]')

      for dest_target_num in range(target_num, len(target_lists)):
        logger.debug(f'{inspect.currentframe().f_code.co_name}-[for[target_num]_for[file_num]_for[dest_target_num]:[target_num:{target_num}][dest_target_num:{dest_target_num}]')
        if target_num == dest_target_num:
          logger.debug(f'{inspect.currentframe().f_code.co_name}-[for[target_num]_for[file_num]_for[dest_target_num]_if[target_num]-True:contine')

          continue
        if check_file_exist(diff_lists[target_num][file_num], diff_lists[dest_target_num], target_num, dest_target_num):
          logger.debug(f'{inspect.currentframe().f_code.co_name}-[for[target_num]_for[file_num]_for[dest_target_num]_if[check_file_exist]-True')

          diff_num = get_diff_num(diff_lists[target_num][file_num], diff_lists[dest_target_num], target_num, dest_target_num)
          if check_file_diff(diff_lists[target_num][file_num], diff_lists[dest_target_num][diff_num]):
            logger.debug(f'{inspect.currentframe().f_code.co_name}-[for[target_num]_for[file_num]_for[dest_target_num]_if[check_file_exist]-True_if[check_file_diff]-True')

            html_name = f'【Sum_result】{target_lists[target_num]}_{target_lists[dest_target_num]}_{diff_lists[target_num][file_num]}'
            html_name = html_name.replace('.','_')
            html_name = html_name.replace('\\','_')
            logger.info(f'{inspect.currentframe().f_code.co_name}-[for[target_num]_for[file_num]_for[dest_target_num]_if[check_file_exist]-True_if[check_file_diff]-True:[html_name:{html_name}]')

            make_diff_html(diff_lists[target_num][file_num], diff_lists[dest_target_num][diff_num], html_name, 'sum_html')
            sum_lists.append(f'{target_lists[target_num]}_{target_lists[dest_target_num]}:{diff_lists[target_num][file_num]}')
            progress_bar.update(1)
            continue
          else:
            logger.debug(f'{inspect.currentframe().f_code.co_name}-[for[target_num]_for[file_num]_for[dest_target_num]_if[check_file_exist]-True_if[check_file_diff]-else')

            html_name = f'【Diff_result】{target_lists[target_num]}_{target_lists[dest_target_num]}_{diff_lists[target_num][file_num]}'
            html_name = html_name.replace('.','_')
            html_name = html_name.replace('\\','_')
            logger.info(f'{inspect.currentframe().f_code.co_name}-[for[target_num]_for[file_num]_for[dest_target_num]_if[check_file_exist]-True_if[check_file_diff]-else:[html_name:{html_name}]')

            make_diff_html(diff_lists[target_num][file_num], diff_lists[dest_target_num][diff_num], html_name, 'diff_html')
            progress_bar.update(1)
        else:
          logger.debug(f'{inspect.currentframe().f_code.co_name}-[for[target_num]_for[file_num]_for[dest_target_num]_if[check_file_exist]-else')
          logger.info(f'{inspect.currentframe().f_code.co_name}-[not_FD_files[ADD]{diff_lists[target_num][file_num]}]')

          not_FD_files.append(f'{target_lists[target_num]}_{target_lists[dest_target_num]}:{diff_lists[target_num][file_num]}')
          progress_bar.update(1)

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
    input('エンターキーを押して、処理を終了してください。\n\
      Press the Enter key to end the process.')
    
    exit()

def first_process():
  logger.info(f'{inspect.currentframe().f_code.co_name}')
  print('==========================================================')
  print('コンフィグ比較プログラムを実行します。')
  print('==========================================================')

  if not os.path.isdir('.\\target'):
    make_dir('target') 
    message = 'targetフォルダが確認出来なかったため、targetフォルダを作成します。\n\
      比較したいコンフィグファイルの入ったフォルダを2つ用意し、targetフォルダへ格納してください。'
    
    err_title = 'The target folder cannot be found.'
    logger.error(f'{inspect.currentframe().f_code.co_name}-[First problem check completed.]')
    push_code(err_title, message, 1)
  
  title = 'First problem check completed.'
  message = 'targetフォルダの存在を確認しました。\n\
    各種正常性を確認しながらコンフィグ比較プロセスを実行します。'
  logger.info(f'{inspect.currentframe().f_code.co_name}-[Completed successfully]')
  push_code(title, message, 0)


def end_process():
  logger.info(f'{inspect.currentframe().f_code.co_name}')
  title = 'All processes completed successfully'
  message = '全てのプロセスは正常に完了しました。\n\
    差分のあるファイルが見つかった場合はdiff_htmlフォルダを作成し、結果をHTMLファイルで保存しています。\n\
    差分のないファイルについてはエビデンスとしてsum_htmlフォルダを作成し、結果をHTMLファイルで保存しています。\n\
    中身を確認してください。\n\
    プログラムを終了します。'

  push_code(title, message, 0)
  
  input('エンターキーを押して、処理を終了してください。\n\
    Press the Enter key to end the process.')
  exit()

def export_nfd_files():
  logger.info(f'{inspect.currentframe().f_code.co_name}')
  if len(not_FD_files) > 0:
    logger.debug(f'{inspect.currentframe().f_code.co_name}[date_str]：{date_str}')
    make_dir('log\\NotFoundFiles')
    filepath = f'.\\log\\NotFoundFiles\\【NotFoundFiles】{date_str}.txt'
    logger.debug(f'{inspect.currentframe().f_code.co_name}[filepath]：{filepath}')
    f = open(filepath, 'w')
    for file in not_FD_files:
      f.write(file + '\n')

def export_file_paths():
  logger.info(f'{inspect.currentframe().f_code.co_name}')
  if len(diff_lists) > 0:
    logger.debug(f'{inspect.currentframe().f_code.co_name}[date_str]：{date_str}')
    for target in range(len(target_lists)):
      make_dir('log\\FilePathList')
      filepath = f'.\\log\\FilePathList\\【FilePathList】{target_lists[target]}_{date_str}.txt'
      logger.debug(f'{inspect.currentframe().f_code.co_name}[filepath]：{filepath}')
      f = open(filepath, 'w')
      for file in diff_lists[target]:
        f.write(file + '\n')

def export_dir_paths():
  logger.info(f'{inspect.currentframe().f_code.co_name}')
  make_dir('log\\DirList')
  for target in target_lists:
    filepath = f'.\\log\\DirList\\【DirList】{target}_{date_str}.txt'
    target_dirs = []
    target_dirs = glob.glob(f'.\\target\\{target}\\**\\', recursive = True)
    f = open(filepath, 'w')
    for dir in target_dirs:
      f.write(dir + '\n')

def export_sum_lists():
  logger.info(f'{inspect.currentframe().f_code.co_name}')

  if len(sum_lists) > 0:
    logger.debug(f'{inspect.currentframe().f_code.co_name}[date_str]：{date_str}')
    make_dir('sum_html')
    filepath = f'.\\sum_html\\【SumLists】{date_str}.txt'
    logger.debug(f'{inspect.currentframe().f_code.co_name}[filepath]：{filepath}')
    f = open(filepath, 'w')
    
    for list in sum_lists:
      f.write(list + '\n')

def main_process():
  get_files()
  check_diff()

def export_process():
  export_nfd_files()
  export_file_paths()
  export_dir_paths()
  export_sum_lists()

#処理実行:Processing execution
setup_debug()
first_process()
main_process()
export_process()
end_process()
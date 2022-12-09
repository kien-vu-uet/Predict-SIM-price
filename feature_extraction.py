import datetime
import pandas as pd
import argparse

def is_ordered(a):
  if '_' in a or len(a) <= 2:  return 0
  b = []
  for c in a:
    if c == '0' and len(b) > 0 and b[-1] == 1: 
      b[-1] = 10
    else: b.append(int(c))
  mark = {b[i+1] - b[i] : 1 for i in range(len(b) - 1)}
  if len(mark) > 1: return 0
  mark = [k for k in mark.keys() if k != 0] 
  return 0 if len(mark) != 1 else mark[0]

'''
Check tam hoa, tứ quý, ngũ quý, lục quý, ... và các đặc trưng có liên quan
'''
def lap_cung_gia_tri(sim: int or str):
  if isinstance(sim, int): sim = str(sim)  
  if len(sim) > 9: sim = sim[-9:]
  features = []
  for d in range(10):
    for l in range(9, 1, -1):
      try:
        for s in range(9-l):
          p = sim.index(str(d) * l, s)
          sim = sim[:p] + str('_' * l) + sim[p+l:]
          if (d, p) not in [(_d, _p) for (_d, _p, _l) in features]: 
            features.append((d, p, l))
      except:
        pass
  # print(sim)
  values = {
        'nhi_hoa_sl': 0,
        'nhi_hoa_dep' : 0,
        'tam_hoa_sl': 0,
        'tam_hoa_dep' : 0,
        'tu_quy_sl' : 0,
        'tu_quy_dep' : 0,
        'ngu_quy_sl' : 0,
        'luc_quy_sl' : 0,
        'that_quy_sl' : 0,
        'bat_quy_sl' : 0,
        'cuu_quy_sl' : 0,
        '5+_quy_dep' : 0,
        'lap#_sieu_dep' : 0,
        'lap#_o_duoi' : 1 if sim[-1] == '_' else 0
        }  

  e = {p:d for (d, p, l) in features}
  e_p = list(e.keys())
  e_p.sort()
  e = [str(e[p]) for p in e_p]
  e = ''.join(e)
  if is_ordered(e): values['lap#_sieu_dep'] = 1

  for l in range(2, 10):
    count = 0
    btf = 0
    for item in features:
      if item[-1] == l: 
        count += 1
        if item[0] in [6, 8, 9]: btf += 1
        if l == 5 and item[0] == 5: btf += 1
    if l == 2:
      values['nhi_hoa_sl'] = count
      if (count > 3 or btf > 2): values['nhi_hoa_dep'] = 1
      if (count >= 3 and btf >= 3): values['lap#_sieu_dep'] = 1
    if l == 3:
      values['tam_hoa_sl'] = count
      if btf > 0: values['tam_hoa_dep'] = 1
      if (btf > 1 or count == 3): values['lap#_sieu_dep'] = 1
    elif l == 4:
      values['tu_quy_sl'] = count
      if btf > 0: values['tu_quy_dep'] = 1
      if (btf > 1 or count == 2): values['lap#_sieu_dep'] = 1
    else:
      if count == 0: continue
      if btf > 0: values['5+_quy_dep'] = 1
      if l > 5 or (l >= item[0]): values['lap#_sieu_dep'] = 1
      if l == 5: values['ngu_quy_sl'] = count 
      elif l == 6: values['luc_quy_sl'] = count
      elif l == 7: values['that_quy_sl'] = count
      elif l == 8: values['bat_quy_sl'] = count
      elif l == 9: values['cuu_quy_sl'] = count

  return values


'''
Check sảnh tiến / lùi
'''
def sanh_tien_lui(sim:int or str):
  if isinstance(sim, int): sim = str(sim)
  if len(sim) > 9: sim = sim[-9:]

  values = {
      'sanh_tien_3_sl' : 0,
      'sanh_tien_4_sl' : 0,
      'sanh_tien_5_sl' : 0,
      'sanh_tien_6_sl' : 0,
      'sanh_tien_7_sl' : 0,
      'sanh_tien_8_sl' : 0,
      'sanh_tien_9_sl' : 0,
      'sanh_tien_3_dep' : 0,
      'sanh_tien_4_dep' : 0,
      'sanh_tien_5+_dep' : 0,
      'sanh_tien_sieu_dep' : 0,
      'sanh_lui_3_sl' : 0,
      'sanh_lui_4_sl' : 0,
      'sanh_lui_5_sl' : 0,
      'sanh_lui_6_sl' : 0,
      'sanh_lui_7_sl' : 0,
      'sanh_lui_8_sl' : 0,
      'sanh_lui_9_sl' : 0,
      'sanh_lui_3_dep' : 0,
      'sanh_lui_4_dep' : 0,
      'sanh_lui_5+_dep' : 0,
      'sanh_lui_sieu_dep' : 0,
      'sanh_o_duoi' : 0
  }

  for l in range(9, 2, -1):
    for p in range(10-l):
      v = is_ordered(sim[p:p+l])
      if v > 0:
        if p + l == len(sim): values['sanh_o_duoi'] = 1
        sim = sim[:p] + str('_' * l) + sim[p+l:]
        if l == 3:
          values['sanh_tien_3_sl'] += 1
          if sim[p:p+l][-1] in ['6', '8', '9', '0']: values['sanh_tien_3_dep'] = 1
        elif l == 4:
          values['sanh_tien_4_sl'] += 1
          if sim[p:p+l][-1] in ['6', '8', '9', '0']: values['sanh_tien_4_dep'] = 1
        else:
          if sim[p:p+l][-1] in ['6', '8', '9', '0']: values['sanh_tien_5+_dep'] = 1
          if l >= 6 or (l == 5 and values['sanh_tien_5+_dep'] == 1): values['sanh_tien_sieu_dep'] = 1 
          if l == 5: values['sanh_tien_5_sl'] = 1
          if l == 6: values['sanh_tien_6_sl'] = 1
          if l == 7: values['sanh_tien_7_sl'] = 1
          if l == 8: values['sanh_tien_8_sl'] = 1
          if l == 9: values['sanh_tien_9_sl'] = 1 
      elif v < 0:
        sim = sim[:p] + str('_' * l) + sim[p+l:]
        if l == 3:
          values['sanh_lui_3_sl'] += 1
          if sim[p:p+l][-1] in ['6', '8', '9', '0']: values['sanh_lui_3_dep'] = 1
        elif l == 4:
          values['sanh_lui_4_sl'] += 1
          if sim[p:p+l][-1] in ['6', '8', '9', '0']: values['sanh_lui_4_dep'] = 1
        else:
          if sim[p:p+l][-1] in ['6', '8', '9', '0']: values['sanh_lui_5+_dep'] = 1
          if l >= 6 or (l == 5 and values['sanh_lui_5+_dep'] == 1): values['sanh_lui_sieu_dep'] = 1 
          if l == 5: values['sanh_lui_5_sl'] = 1
          if l == 6: values['sanh_lui_6_sl'] = 1
          if l == 7: values['sanh_lui_7_sl'] = 1
          if l == 8: values['sanh_lui_8_sl'] = 1
          if l == 9: values['sanh_lui_9_sl'] = 1 

  return values


'''
Check đầu số và đầu số ưa thích
'''
# Đầu số cổ và đầu số mới
# Đầu số cổ return 1, đầu số mới return 0
def dau_so(sim_number: str or int):
  dau_so_moi = ['32','33','34','35','36','37','38','39','70','79','77','76','78','83','84','85','81','82','56','58','59']
  dau_so = []
  if isinstance(sim_number, int):
    sim_number = str(sim_number)
  if (len(sim_number) > 9):
    sim_number = sim_number[-9:]

  values = {
        'dau_so': 1,
        }

  two_first_number = sim_number[0:2]
  if two_first_number in dau_so_moi:
    values['dau_so'] = 0
  return values


# Đầu số ưa thích nhiều người lựa chọn
def dau_so_ua_thich(sim_number : str or int):
  two_number = ['56', '58', '59', '70', '76', '77', '78', '79', '81', '82', '83', '84', '85', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99']
  three_number = ['333', '345', '704', '707', '708', '777', '866', '868', '869', '886', '888', '889', '903', '909', '919', '929', '939', '949', '967', '968', '969', '978', '989', '999']

  if isinstance(sim_number, int):
    sim_number = str(sim_number)
  if (len(sim_number) > 9):
    sim_number = sim_number[-9:]
  
  values = {
        'dau_so_ua_thich': 0,
        }

  two_first_number = sim_number[0:2]
  three_first_number = sim_number[0:3]
  if two_first_number in two_number or three_first_number in three_number:
    values['dau_so_ua_thich'] = 1
  else: values['dau_so_ua_thich'] = 0
  
  return values


'''
Check nhà mạng
'''
# Viettel: 1
# Vinaphone: 2
# Mobifone: 3
# Vietnamobile: 4
# Gmobile: 5
# Itel: 6

def nha_mang(sim_number: str or int):
  # Danh sách đầu số các nhà mạng
  viettel = ['96','97','98','86','32','33','34','35','36','37','38','39']
  vinaphone = ['88','91','94','83','84','85','81','82']
  mobifone = ['89','90','93','70','79','77','76','78']
  vietnamobile = ['92','56','58','52']
  gmobile = ['99','59']
  itel = ['87']

  values = {
        'nha_mang' : 1
        }

  if isinstance(sim_number, int):
    sim_number = str(sim_number)
  if (len(sim_number) > 9):
    sim_number = sim_number[-9:]

  two_first_number = sim_number[0:2]

  if (two_first_number in viettel):
    values['nha_mang'] = 1
  elif (two_first_number in vinaphone):
    values['nha_mang'] = 2
  elif (two_first_number in mobifone):
    values['nha_mang'] = 3
  elif (two_first_number in vietnamobile):
    values['nha_mang'] = 4
  elif (two_first_number in gmobile):
    values['nha_mang'] = 5
  else: values['nha_mang'] = 6

  return values

'''
Check quẻ sim tốt xấu
'''
# Quẻ sim số 
# Quẻ cát: 1
# Quẻ đại cát: 2
# Quẻ thường : 3
# Quẻ hung: 4
# Quẻ đại hung: 5

def que_sim(sim_number:int or str):
  que_cat = ['1','6','7','8','11','13','15','17','21','24','25','27','32','36','42','43','51','56','62','64','67','72','76']
  que_dai_cat = ['3','5','16','18','23','28','30','31','38','40','46','47','66','78','80']
  que_hung = ['4','9','10','12','19','20','22','26','29','33','35','41','44','45','52','54','58','60','61','63','68','69','71','79']
  que_dai_hung = ['55', '75']
  binh_thuong = ['2','14','34','37','39','48','49','50','53','57','59','65','70','73','74','77']

  values = {
        'que_sim' : 3
        }

  if isinstance(sim_number, int):
    sim_number = str(sim_number)
  if (len(sim_number) > 9):
    sim_number = sim_number[-9:]

  last_four_number = sim_number[-4:]
  
  mod_que = str(int(last_four_number) % 80)


  if mod_que in que_cat:
    values['que_sim'] = 1
    return values
  elif mod_que in que_dai_cat:
    values['que_sim'] = 2
    return values
  elif mod_que in que_hung:
    values['que_sim'] = 4
    return values
  elif mod_que in que_dai_hung:
    values['que_sim'] = 5
    return values
  else: return values

'''
Check sim theo năm sinh
'''
def sim_nam_sinh(sim_number:int or str):
  if isinstance(sim_number, int):
    sim_number = str(sim_number)
  if (len(sim_number) > 9):
    sim_number = sim_number[-9:]

  values = {
        'nam_sinh_ddmmyyyy': 0,
        'nam_sinh_ddmyyyy' : 0,
        'nam_sinh_dmmyyyy' : 0,
        'nam_sinh_dmyyyy' : 0,
        'nam_sinh_yyyy' : 0,
        'nam_sinh_ddmmyy' : 0
        }
  

  # Sim đuôi yyyy
  long_year = int(sim_number[-4:])
  if long_year >= 1970 and long_year <= 2010:

    # Sim dạng ddmmyyyy
    long_month = sim_number[-6:-4]
    long_day = sim_number[-8:-6]
    short_year = sim_number[-2:]

    try:
      datetime.datetime(int(short_year),int(long_month),int(long_day))
      values['nam_sinh_ddmmyyyy'] = 1
      return values
    except:
      pass

    # Sim dạng ddmyyyyy
    long_day = sim_number[-7:-5]
    long_month = sim_number[-5:-4]
    short_year = sim_number[-2:]

    try:
      datetime.datetime(int(short_year),int(long_month),int(long_day))
      values['nam_sinh_ddmyyyy'] = 1
      return values
    except:
      pass

    # Sim dạng dmmyyyy
    long_day = sim_number[-7:-6]
    long_month = sim_number[-6:-4]
    short_year = sim_number[-2:]
    try:
      datetime.datetime(int(short_year),int(long_month),int(long_day))
      values['nam_sinh_dmmyyyy'] = 1
      return values
    except:
      pass


    # Sim dạng dmyyyy
    long_day = sim_number[-6:-5]
    long_month = sim_number[-5:-4]
    short_year = sim_number[-2:]
    try:
      datetime.datetime(int(short_year),int(long_month),int(long_day))
      values['nam_sinh_dmyyyy'] = 1
      return values
    except:
      pass

    values['nam_sinh_yyyy'] = 1
    return values

  # Sim dạng ddmmyy
  ngay_sinh = sim_number[-6:]
  year = int(ngay_sinh[-2:])
  day = int(ngay_sinh[0:2])
  month = int(ngay_sinh[2:4])
  validDate = True
  try:
    datetime.datetime(year, month, day)
  except:
    validDate = False
  
  if validDate:
    values['nam_sinh_ddmmyy'] = 1
    return values
  else: return values


'''
Số chữ số cấu thành 
'''
# chu_so_cau_thanh = []
def chu_so_cau_thanh(sim_number:int or str):
  if isinstance(sim_number, int):
    sim_number = str(sim_number)
  if (len(sim_number) > 9):
    sim_number = sim_number[-9:]
  
  values = {
        'chu_so_cau_thanh': len(list(set(sim_number))),
        }

  return values


# Hàm tách các group 
def split(sim_number, number):
    def Convert(a):
        it = iter(a)
        res_dct = dict(zip(it, it))
        return res_dct
    if isinstance(sim_number, int):
        sim_number = str(sim_number)
    if (len(sim_number) > 9):
        sim_number = sim_number[-9:]

    key_dict = []
    for i in range(0, len(sim_number) - number + 1):
        key_dict.append(sim_number[i:i+number])
        if i == len(sim_number) - number:
            key_dict.append(1)
        else:
            key_dict.append(0)
            
    return Convert(key_dict)

'''
Check sim gánh đảo
'''
# Sim gánh đảo
# Dạng 4 abba : 4_1
# Dạng 5 abxba : 5_1 5_2 
# Dạng 6 ab.aa.ab ab.cc.ba ab.ab.ba ab.ba.ab: 6_1 6_2 6_3 6_4

def ganh_dao(sim_number:int or str):

  if isinstance(sim_number, int):
    sim_number = str(sim_number)
  if (len(sim_number) > 9):
    sim_number = sim_number[-9:]

  values = {
        'ganh_dao_dang_4': 0,
        'ganh_dao_dang_5' : 0,
        'ganh_dao_dang_6_1' : 0,
        'ganh_dao_dang_6_2' : 0,
        'ganh_dao_dang_6_3' : 0,
        'ganh_dao_dang_6_4' : 0,
        }


  last_four = sim_number[-4:]
  last_five = sim_number[-5:]
  last_six = sim_number[-6:]

  # Dạng 6
  if len(list(set(last_six))) == 2 or len(list(set(last_six))) == 3:
    if (last_six[0:2] == (last_six[-2:])):
      if (last_six[2:4] == (last_six[2:4])[::-1]):
        values['ganh_dao_dang_6_1'] = 1
      elif (last_six[0:2] == (last_six[2:4])[::-1]):
        values['ganh_dao_dang_6_4'] = 1
    elif (last_six[0:2] == (last_six[-2:])[::-1]):
      if (last_six[2:4] == (last_six[2:4])[::-1]): 
        values['ganh_dao_dang_6_2'] = 1
      elif (last_six[0:2] == last_six[2:4]):
        values['ganh_dao_dang_6_3'] = 1

  # Dạng 5 
  if len(list(set(last_five))) == 2 or len(list(set(last_five))) == 3:
    if last_five[0:2] == (last_five[-2:])[::-1] or last_five[0:2] == last_five[-2:]:
      values['ganh_dao_dang_5'] = 1

  # Dạng 4
  if (last_four[0:2] == (last_four[-2:])[::-1]):
    if len(list(set(last_four))) == 2:
      values['ganh_dao_dang_4'] = 1
  
  # return last_four
  # print(last_four)
  # print(len(list(set(last_four))))
  return values

# Sim gánh đảo update
# Dạng 4 abba : 4_1
# Dạng 5 abxba : 5_1 5_2 
# Dạng 6 ab.aa.ab ab.cc.ba ab.ab.ba ab.ba.ab: 6_1 6_2 6_3 6_4

def ganh_dao_update(sim_number:int or str):

  if isinstance(sim_number, int):
    sim_number = str(sim_number)
  if (len(sim_number) > 9):
    sim_number = sim_number[-9:]

  values = {
        'ganh_dao_dang_4_sl': 0,
        'ganh_dao_dang_5_sl' : 0,
        'ganh_dao_dang_6_1_sl' : 0,
        'ganh_dao_dang_6_2_sl' : 0,
        'ganh_dao_dang_6_3_sl' : 0,
        'ganh_dao_dang_6_4_sl' : 0,
        'ganh_dao_duoi': 0
        }


  group_six = split(sim_number, 6)
  group_five = split(sim_number, 5)
  group_four = split(sim_number, 4)

  # Dạng 6
  if len(group_six) >= 1:
    for i in group_six:
      last_six = i

      if (last_six[0:2] == (last_six[-2:])):
        if (last_six[2:4] == (last_six[2:4])[::-1]):
          values['ganh_dao_dang_6_1_sl'] += 1
          if group_six[i] == 1:
            values['ganh_dao_duoi'] = 1
        elif (last_six[0:2] == (last_six[2:4])[::-1]):
          values['ganh_dao_dang_6_4_sl'] += 1
          if group_six[i] == 1:
            values['ganh_dao_duoi'] = 1

            
      elif (last_six[0:2] == (last_six[-2:])[::-1]):
        if (last_six[2:4] == (last_six[2:4])[::-1]): 
          values['ganh_dao_dang_6_2_sl'] += 1
          if group_six[i] == 1:
            values['ganh_dao_duoi'] = 1
        elif (last_six[0:2] == last_six[2:4]):
          values['ganh_dao_dang_6_3_sl'] += 1
          if group_six[i] == 1:
            values['ganh_dao_duoi'] = 1


  # Dạng 5 
  if len(group_five) >= 1:
    for i in group_five:
      last_five = i
      if last_five[0:2] == (last_five[-2:])[::-1] or last_five[0:2] == last_five[-2:]:
        values['ganh_dao_dang_5_sl'] += 1
        if group_five[i] == 1:
            values['ganh_dao_duoi'] = 1

  # Dạng 4
  if len(group_four) >= 1:
    for i in group_four:
      last_four = i
      if (last_four[0:2] == (last_four[-2:])[::-1]):
        values['ganh_dao_dang_4_sl'] += 1
        if group_four[i] == 1:
            values['ganh_dao_duoi'] = 1
    
  # return last_four

  # print(group_six)
  # print(group_five)
  # print(group_four)

  return values

'''
Check sim lặp theo bộ
'''

# sim lặp
# dạng 4 abab
# dạng 6 aa.ab.ab - ab.ab.ab - ab.ac.ac - ab.ba.ba - abc.abc - aa.bb.cc : 6_1 - 6_2 - 6_3 - 6_4 - 6_5 - 6_6
# dạng 8 ab.ab.ac.ac - ab.ab.cd.cd - ab.ab.ab.ab - abcd.abcd : 8_1 - 8_2 - 8_3 - 8_4

def sim_lap(sim_number: str or int):
  if isinstance(sim_number, int):
    sim_number = str(sim_number)
  if (len(sim_number) > 9):
    sim_number = sim_number[-9:]

  # Dạng 4
  def dang_4(sub_sim_number: str or int):
    if isinstance(sub_sim_number, int):
      sub_sim_number = str(sub_sim_number)
    if (len(sub_sim_number) > 4):
      sub_sim_number = sub_sim_number[-4:]
    if sub_sim_number[:-2] == sub_sim_number[-2:]:
      if len(list(set(sub_sim_number))) == 2:
        return 1
    return 0

  # Giá trị khởi tạo
  values = {
      'sim_lap_dang_4': 0,
      'sim_lap_dang_6_1' : 0,
      'sim_lap_dang_6_2' : 0,
      'sim_lap_dang_6_3' : 0,
      'sim_lap_dang_6_4' : 0,
      'sim_lap_dang_6_5' : 0,
      'sim_lap_dang_6_6' : 0,
      'sim_lap_dang_8_1' : 0,
      'sim_lap_dang_8_2' : 0,
      'sim_lap_dang_8_3' : 0,
      'sim_lap_dang_8_4' : 0 
    }

  if len(sim_number) >= 8: 
    last_eight = sim_number[-8:]
    # Dạng 8 ab.ab.ac.ac - ab.ab.cd.cd
    if dang_4(last_eight[-4:]):
      if dang_4(last_eight[:-4]):
        if len(list(set(last_eight))) == 3: 
          if last_eight[0] == last_eight[-4]: # Dạng ab.ab.ac.ac
            values['sim_lap_dang_8_1'] = 1
        elif len(list(set(last_eight))) == 4: # Dạng ab.ab.cd.cd
          values['sim_lap_dang_8_2'] = 1

        if dang_4(last_eight[-6:-2]): # Dạng ab.ab.ab.ab
          values['sim_lap_dang_8_3'] = 1
    # Dạng 8 abcd.abcd
    if len(list(set(last_eight))) == 4:
      if last_eight[0:4] == last_eight[-4:]:
        values['sim_lap_dang_8_4'] = 1

  if len(sim_number) >= 6:
    last_six = sim_number[-6:]
    # Dạng 6
    # Dạng 6 aa.ab.ab ab.ab.ab - ab.ac.ac - ab.ba.ba
    if dang_4(last_six[-4:]): # Lặp 4 chữ số cuối dạng ab.ab
      if last_six[0] == last_six[1]: # dạng aa.ab.ab
        values['sim_lap_dang_6_1'] = 1

      if dang_4(last_six[:-2]): # Kiểm tra 4 chữ số đầu dạng ab.ab
        values['sim_lap_dang_6_2'] = 1 # Dạng ab.ab.ab
      
      else:
        if len(list(set(last_six[:-2]))) == 3: # 4 chữ số đầu có 3 chữ số cấu thành ab.ac
          values['sim_lap_dang_6_3'] = 1
        elif len(list(set(last_six[:-2]))) == 2: 
          if last_six[:-2] == (last_six[:-2])[::-1]: # 4 chữ số đầu dạng gánh đảo ab.ba
            values['sim_lap_dang_6_4'] = 1

    # Dạng 6 abc.abc
    if last_six[:-3] == last_six[-3:]:
      values['sim_lap_dang_6_5'] = 1
    
    # Dạng 6 aa.bb.cc
    if (last_six[-1] == last_six[-2]) and (last_six[0] == last_six[1]) and (last_six[2] == last_six[3]):
      values['sim_lap_dang_6_6'] = 1 

  if len(sim_number) >= 4:
    last_four = sim_number[-4:]
    # Dạng 4
    if dang_4(last_four):
      values['sim_lap_dang_4'] = 1



  return values

# sim lặp
# dạng 4 abab
# dạng 6 aa.ab.ab - ab.ab.ab - ab.ac.ac - ab.ba.ba - abc.abc - aa.bb.cc : 6_1 - 6_2 - 6_3 - 6_4 - 6_5 - 6_6
# dạng 8 ab.ab.ac.ac - ab.ab.cd.cd - ab.ab.ab.ab - abcd.abcd : 8_1 - 8_2 - 8_3 - 8_4

def sim_lap_update(sim_number: str or int):
  if isinstance(sim_number, int):
    sim_number = str(sim_number)
  if (len(sim_number) > 9):
    sim_number = sim_number[-9:]

  # Dạng 4
  def dang_4(sub_sim_number: str or int):
    if isinstance(sub_sim_number, int):
      sub_sim_number = str(sub_sim_number)
    if (len(sub_sim_number) > 4):
      sub_sim_number = sub_sim_number[-4:]
    if sub_sim_number[:-2] == sub_sim_number[-2:] :
      return 1
    return 0

  # Giá trị khởi tạo
  values = {
      'sim_lap_dang_4_sl': 0,
      'sim_lap_dang_6_1_sl' : 0,
      'sim_lap_dang_6_2_sl' : 0,
      'sim_lap_dang_6_3_sl' : 0,
      'sim_lap_dang_6_4_sl' : 0,
      'sim_lap_dang_6_5_sl' : 0,
      'sim_lap_dang_6_6_sl' : 0,
      'sim_lap_dang_8_1_sl' : 0,
      'sim_lap_dang_8_2_sl' : 0,
      'sim_lap_dang_8_3_sl' : 0,
      'sim_lap_dang_8_4_sl' : 0,
      'sim_lap_duoi' : 0
    }
  group_eight = split(sim_number, 8)
  group_six = split(sim_number, 6)
  group_four = split(sim_number, 4)

  if len(group_eight) >= 1:
    for i in group_eight:
      last_eight = i
      # Dạng 8 ab.ab.ac.ac - ab.ab.cd.cd
      if dang_4(last_eight[-4:]):
        if dang_4(last_eight[:-4]):
          if len(list(set(last_eight))) == 3: 
            if last_eight[0] == last_eight[-4]: # Dạng ab.ab.ac.ac
              values['sim_lap_dang_8_1_sl'] += 1
              if group_eight[i] == 1:
                values['sim_lap_duoi'] = 1
          elif len(list(set(last_eight))) == 4: # Dạng ab.ab.cd.cd
            values['sim_lap_dang_8_2_sl'] += 1
            if group_eight[i] == 1:
                values['sim_lap_duoi'] = 1

          if dang_4(last_eight[-6:-2]): # Dạng ab.ab.ab.ab
            values['sim_lap_dang_8_3_sl'] += 1
            if group_eight[i] == 1:
                values['sim_lap_duoi'] = 1
      # Dạng 8 abcd.abcd
      if len(list(set(last_eight))) == 4:
        if last_eight[0:4] == last_eight[-4:]:
          values['sim_lap_dang_8_4_sl'] += 1
          if group_eight[i] == 1:
                values['sim_lap_duoi'] = 1

  if len(group_six) >= 1:
    for i in group_six:
      last_six = i
    # Dạng 6
    # Dạng 6 aa.ab.ab ab.ab.ab - ab.ac.ac - ab.ba.ba
      if dang_4(last_six[-4:]): # Lặp 4 chữ số cuối dạng ab.ab
        if last_six[0] == last_six[1]: # dạng aa.ab.ab
          values['sim_lap_dang_6_1_sl'] += 1
          if group_six[i] == 1:
                values['sim_lap_duoi'] = 1
        if dang_4(last_six[:-2]): # Kiểm tra 4 chữ số đầu dạng ab.ab
          values['sim_lap_dang_6_2_sl'] += 1 # Dạng ab.ab.ab
          if group_six[i] == 1:
                values['sim_lap_duoi'] = 1
        else:
          if len(list(set(last_six[:-2]))) == 3: # 4 chữ số đầu có 3 chữ số cấu thành ab.ac
            values['sim_lap_dang_6_3_sl'] += 1
            if group_six[i] == 1:
                values['sim_lap_duoi'] = 1
          elif len(list(set(last_six[:-2]))) == 2: 
            if last_six[:-2] == (last_six[:-2])[::-1]: # 4 chữ số đầu dạng gánh đảo ab.ba
              values['sim_lap_dang_6_4_sl'] += 1
              if group_six[i] == 1:
                values['sim_lap_duoi'] = 1

      # Dạng 6 abc.abc
      if last_six[:-3] == last_six[-3:]:
        values['sim_lap_dang_6_5_sl'] += 1
        if group_six[i] == 1:
          values['sim_lap_duoi'] = 1
      
      # Dạng 6 aa.bb.cc
      if (last_six[-1] == last_six[-2]) and (last_six[0] == last_six[1]) and (last_six[2] == last_six[3]):
        values['sim_lap_dang_6_6_sl'] += 1
        if group_six[i] == 1:
          values['sim_lap_duoi'] = 1

  if len(group_four) >= 1:
    for i in group_four:
      last_four = i
      # Dạng 4
      if dang_4(last_four):
        values['sim_lap_dang_4_sl'] += 1
        if group_four[i] == 1:
            values['sim_lap_duoi'] = 1



  return values

'''
Check sim thần tài lộc phát
'''
def than_tai_loc_phat(sim_number: str or int):
  if isinstance(sim_number, int):
    sim_number = str(sim_number)
  if (len(sim_number) > 9):
    sim_number = sim_number[-9:]

  # Thần tài : 0 - không có, 1 - thần tài nhỏ (39), 2 - thần tài lớn (79)
  # Lộc phát : 0 - không có, 1 - lộc phát (68), 2 - phát lộc (86)
  values = {
            'than_tai_nho': 0,
            'than_tai_lon': 0,
            'loc_phat': 0,
            'phat_loc': 0,
            'ttlp_gia_cao': 0,
            'ttlp_gia_tb': 0,
            'ttlp_gia_thap' : 0
           }

  last_two = sim_number[-2:]
  if last_two == '39':
    values['than_tai_nho'] = 1
  elif last_two == '79':
    values['than_tai_lon'] = 1
  elif last_two == '68':
    values['loc_phat'] = 1
  elif last_two == '86':
    values['phat_loc'] = 1

  # check_value = list(sim_lap(sim_number[0:-2]).values())
  # check_value += list(ganh_dao(sim_number[0:-2]).values())
  check_value = list(sim_lap_update(sim_number[0:-2]).values())
  check_value += list(ganh_dao_update(sim_number[0:-2]).values())
  check_value += list(lap_cung_gia_tri(sim_number[0:-2]).values())
  check_value += list(sanh_tien_lui(sim_number[0:-2]).values())[-4:]
  check_value += list(sanh_tien_lui(sim_number[0:-2]).values())[7:11]

  # print(check_value)
  count = 0
  for i in check_value:
    # if i == 1:
    #   count += 1
    if i != 0:
      count += i
  # print(count)

  if count >= 5:
    values['ttlp_gia_cao'] = 1
    return values
  elif count <= 4 and count >= 2:
    values['ttlp_gia_tb'] = 1
    return values

  values['ttlp_gia_thap'] = 1
  return values
        

'''
Tạo DataFrame
'''
def dataframe_creation(sim_number):
  sim_number_dict = {'sim_number': []} #0
  lap_cung_gia_tri_dict = [] #1
  sanh_tien_lui_dict = [] #2
  dau_so_dict = [] #3
  nha_mang_dict = [] #4
  dau_so_ua_thich_dict = [] #5
  que_sim_dict = [] #6
  sim_nam_sinh_dict = [] #7
  chu_so_cau_thanh_dict = [] #8
  ganh_dao_dict = [] #9
  sim_lap_dict = [] #10
  than_tai_loc_phat_dict = [] #11


  for i in sim_number:
    sim_number_dict['sim_number'].append(i)
    lap_cung_gia_tri_dict.append(lap_cung_gia_tri(i))
    sanh_tien_lui_dict.append(sanh_tien_lui(i))
    dau_so_dict.append(dau_so(i))
    nha_mang_dict.append(nha_mang(i))
    dau_so_ua_thich_dict.append(dau_so_ua_thich(i))
    que_sim_dict.append(que_sim(i))
    sim_nam_sinh_dict.append(sim_nam_sinh(i))
    chu_so_cau_thanh_dict.append(chu_so_cau_thanh(i))
    # ganh_dao_dict.append(ganh_dao(i))
    # sim_lap_dict.append(sim_lap(i))
    ganh_dao_dict.append(ganh_dao_update(i))
    sim_lap_dict.append(sim_lap_update(i))
    than_tai_loc_phat_dict.append(than_tai_loc_phat(i))
  
  df0 = pd.DataFrame.from_dict(sim_number_dict)
  df1 = pd.DataFrame.from_dict(lap_cung_gia_tri_dict)
  df2 = pd.DataFrame.from_dict(sanh_tien_lui_dict)
  df3 = pd.DataFrame.from_dict(dau_so_dict)
  df4 = pd.DataFrame.from_dict(nha_mang_dict)
  df5 = pd.DataFrame.from_dict(dau_so_ua_thich_dict)
  df6 = pd.DataFrame.from_dict(que_sim_dict)
  df7 = pd.DataFrame.from_dict(sim_nam_sinh_dict)
  df8 = pd.DataFrame.from_dict(chu_so_cau_thanh_dict)
  df9 = pd.DataFrame.from_dict(ganh_dao_dict)
  df10 = pd.DataFrame.from_dict(sim_lap_dict)
  df11 = pd.DataFrame.from_dict(than_tai_loc_phat_dict)

  result = pd.concat([df0, df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11], axis=1, join="inner")

  return result


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type = str, default = 'train_dataset.csv')
    parser.add_argument("--output", type = str, default = 'features_train.csv')
    parser.add_argument("--is-test-set", type = bool, default = False)
    parser.add_argument("--max-price", type = float, default = 1e10)
    args = parser.parse_args()

    df = pd.read_csv(args.input, index_col=False)
    # print(df.columns)
    if not args.is_test_set:
        print(f"Remove {df[df['price_vnd'] > args.max_price].shape[0]} samples")
        df = df[df['price_vnd'] <= args.max_price]
    sim_number = df['sim_number'].astype(str).values.tolist()
    new_df = dataframe_creation(sim_number)
    if not args.is_test_set:
        price = pd.DataFrame(df['price_vnd'].values, columns =['price_vnd'])
        new_df = pd.concat([new_df, price], axis=1)

    new_df.to_csv(args.output)
    print('Done!')

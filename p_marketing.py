import os
import pandas as pd
import jdatetime
import math

class Karmandan:
    def __init__(self, name_karmand ,fname_karmand, phone_karmand , kolle_mablaghe_furush=0 , filename="Karmandan_info.csv"):
        self.name_karmand = name_karmand
        self.fname_karmand = fname_karmand
        self.phone_karmand = phone_karmand
        self.kolle_mablaghe_furush=kolle_mablaghe_furush
        self.filename = filename
        #ملزومات ایجاد فایل برای کلاس کارمندان ____________________________________________

        self.sutuns=["code_karmand","name_karmand","fname_karmand","phone_karmand","kolle_mablaghe_furush"]

        if not os.path.exists(self.filename):
            df=pd.DataFrame(columns=self.sutuns)
            df.to_csv(self.filename, index=False)

        df = pd.read_csv(self.filename)
        # اختصاص کد به کارمندان ____________________________________________
        # اختصاص کد به کارمند
        if not df.empty:
            self.code_karmand = df["code_karmand"].max() + 1  # ماکسیمم مقدار ستون کد کارمند را بعلاوه یک میکنیم
        else:
            self.code_karmand = 1

        new_karmand = pd.DataFrame([{"code_karmand":self.code_karmand,
                                     "fname_karmand":self.fname_karmand,
                                    "name_karmand":self.name_karmand,
                                    "phone_karmand":self.phone_karmand,
                                    "kolle_mablaghe_furush": self.kolle_mablaghe_furush}])
        new_karmand.to_csv(self.filename , mode='a', header=False, index=False)

    #کل مبلغ فروشی که یک کارمند داشته ____________________________________________
    def update_kolle_mablaghe_furush (self):
        if os.path.exists('Sefareshat_info.csv'):
            df = pd.read_csv('Sefareshat_info.csv')
            if not df.empty and "mablagh_sefaresh" in df.columns and "code_karmand" in df.columns:
                # محاسبه کل مبلغ فروش مربوط به کارمند جاری
                self.kolle_mablaghe_furush = df[df["code_karmand"]== self.code_karmand]["mablagh_sefaresh"]. sum()
            if os.path.exists(self.filename):
                df_karmandan=pd.read_csv(self.filename)

                if "code_karmand" in df_karmandan.columns:
                    df_karmandan.loc[df_karmandan["code_karmand"]==self.code_karmand,"kolle_mablaghe_furush"]=self.kolle_mablaghe_furush
                    df_karmandan.to_csv(self.filename, index=False)

    #تغییرات اطلاعات یک کارمند ____________________________________________
    def update_info (self, new_name=None , new_fname=None, new_phone= None):
        if new_name :
            self.name_karmand = new_name
        if new_fname:
            self.fname_karmand = new_fname
        if new_phone:
            self.phone_karmand = new_phone
#  کلاس مشتریان ____________________________________________
class Moshtarian:
    def __init__(self, name_moshtary, fname_moshtary, kodemelly_moshtary,kolle_mablaghe_kharid=0, meghdare_takhfif=0, mablaghe_nahaii_bade_takhfif=0, bedehi=0 , filename="Moshtarian_info.csv" ):
        self.name_moshtary=name_moshtary
        self.fname_moshtary=fname_moshtary
        self.kodemelly_moshtary=kodemelly_moshtary
        self.kolle_mablaghe_kharid=kolle_mablaghe_kharid
        self.meghdare_takhfif=meghdare_takhfif
        self.mablaghe_nahaii_bade_takhfif=mablaghe_nahaii_bade_takhfif
        self.bedehi=bedehi
        self.filename = filename

        #ملزومات ایجاد فایل برای کلاس مشتریان ____________________________________________
        self.sutuns=["code_karbary", "name_moshtary", "fname_moshtary", "kodemelly_moshtary",
                     "kolle_mablaghe_kharid", "meghdare_takhfif" , "mablaghe_nahaii_bade_takhfif", "bedehi" ]

        # ایجاد فایل در صورت نبودن
        if not os.path.exists(self.filename):
            df=pd.DataFrame(columns=self.sutuns)
            df.to_csv(self.filename, index=False)

        df = pd.read_csv(self.filename)

        #اختصاص کد به مشتری ____________________________________________
         # اختصاص کد به مشتری
        if not df.empty:
            self.code_karbary=df["code_karbary"].max() + 1 #ماکسیمم مقدار ستون کد کاربری را بعلاوه یک میکنیم
        else:
            self.code_karbary=101

        #ایجاد دیتا برای فایل ____________________________________________
        new_data=pd.DataFrame([{"code_karbary": self.code_karbary,
                          "name_moshtary": self.name_moshtary,
                          "fname_moshtary": self.fname_moshtary,
                          "kodemelly_moshtary":self.kodemelly_moshtary,
                          "kolle_mablaghe_kharid":self.kolle_mablaghe_kharid,
                          "meghdare_takhfif": self.meghdare_takhfif,
                          "mablaghe_nahaii_bade_takhfif":self.mablaghe_nahaii_bade_takhfif,
                          "bedehi":self.bedehi}])

        new_data.to_csv(self.filename,mode="a",header=False, index=False) #ذخیره در فایل

    # محاسبه مبلغ نهایی بعد تخفیف ____________________________________________
    def update_mablaghe_nahaii_bade_takhfif(self):
        df_sefaresh = pd.read_csv("Sefareshat_info.csv")
        df_sefareshat_moshtary = df_sefaresh[df_sefaresh["code_karbary"] == self.code_karbary]

        # محاسبه جمع خریدهایی که به یک مشتری خاص داده شده
        mablaghe_nahaii_bade_takhfif = (df_sefareshat_moshtary["mablagh_sefaresh"] - df_sefareshat_moshtary["meghdare_takhfif"]).sum()

        # انتقال اطلاعات مبلغ نهایی بعد تخفیف از کلاس سفارش به داخل فایل مشتری اینفو
        df_moshtarian = pd.read_csv(self.filename)
        df_moshtarian.loc[df_moshtarian["code_karbary"] == self.code_karbary, "mablaghe_nahaii_bade_takhfif"] = mablaghe_nahaii_bade_takhfif
        df_moshtarian.to_csv(self.filename, index=False)

    #تغییر اطلاعات مشتری در صورت نیاز ____________________________________________
    def update_info(self, new_name=None, new_fname=None, new_kodemelly_moshtary=None):
        if new_name :
            self.name_moshtary = new_name
        if new_fname:
            self.fname_moshtary = new_fname
        if new_kodemelly_moshtary:
            self.kodemelly_moshtary = new_kodemelly_moshtary

    #  نمایش کل مشتریان ____________________________________________
    #نمایش کل مشتریان
    def show_kolle_moshtarian(self):
        if os.path.exists(self.filename):
            df=pd.read_csv(self.filename)
            print("👇🏻kolle moshtarian:")
            print()
            print(df)
            print("_" * 20)

        else:
            print("❎Moshtary mojod nist")
            print("_" * 20)

#کلاس محصولات ____________________________________________
class Mahsulat:
    def __init__(self, name_mahsul, gheimat, mande_dar_anbar=0 , filename="Mahsulat_info.csv"):
        self.name_mahsul=name_mahsul
        self.gheimat=gheimat
        self.mande_dar_anbar=mande_dar_anbar
        self.filename=filename
        self.tedad_mahsul_furush_rafteh= 0
        self.code_mahsul=101

    # ملزومات ایجاد فایل برای کلاس محصولات ____________________________________________
    def new_mahsul (self):
        # ایجاد ستون برای دیتا فریم
        self.sutun=["code_mahsul","name_mahsul","gheimat" , "tedade_avalie_mahsul", "mande_dar_anbar" , "tedad_mahsul_furush_rafteh"]

        # اگر فایل موجود نیست ایجادش کن با ستونهایی که در خط قبل گفته شده
        if not os.path.exists(self.filename):
            df = pd.DataFrame(columns=self.sutun)
            df.to_csv(self.filename , index=False)

        df = pd.read_csv(self.filename)


        #اختصاص کد به محصولات ____________________________________________
         # اختصاص کد به محصولات
        if not df.empty:
            self.code_mahsul=df["code_mahsul"].max() + 1 #ماکسیمم مقدار ستون کد محصول را بعلاوه یک میکنیم
        else:
            self.code_mahsul=101

        # ایجاد دیتا برای فایل کلاس محصولات ____________________________________________
        # ایجاد محصول جدید = پر کردن ستونهای دیتا فریم
        new_mahsul = pd.DataFrame([{"code_mahsul": self.code_mahsul,
                                    "name_mahsul": self.name_mahsul,
                                    "gheimat": self.gheimat,
                                    "tedade_avalie_mahsul": self.mande_dar_anbar,
                                    "mande_dar_anbar": self.mande_dar_anbar,
                                    "tedad_mahsul_furush_rafteh": self.tedad_mahsul_furush_rafteh}])
                                    #tedad_mahsul_furush_rafteh را حذف کنم؟
        #ذخیره اطلاعات در فایل محصولات اینفو ____________________________________________
        # ذخیره اطلاعات و پرینت
        new_mahsul.to_csv(self.filename,  mode='a', header=False , index=False)
        print(f"✅Mahsul '{self.name_mahsul}' be anbar add shod")
        print("_" * 20)

    def update_info(self, new_name=None, new_gheimat=None):
        if new_name:
            self.name_mahsul=new_name
        if new_gheimat:
            self.gheimat=new_gheimat

    #آپدیت مقدار مانده در انبار ____________________________________________
    # آپدیت مقدار مانده در انبار
    def update_mande_dar_anbar(self):

        if os.path.exists(self.filename):
            df = pd.read_csv(self.filename)

            if "code_mahsul" in df.columns and "mande_dar_anbar" in df.columns:
                # loc[A,B]در واقع محل دیتای ما در سطر A و ستون  B را میدهد
                df.loc[df["code_mahsul"]== self.code_mahsul, "mande_dar_anbar"]=self.mande_dar_anbar
                df.to_csv(self.filename, index=False)
                print(f"✅mande dar anbar baraye mahsul '{self.name_mahsul}' berooz shod.")
                print("_"*20)

        else:
            print("❎file 'mahsulat_info.csv' vojod nadarad!")
            print("_" * 20)

    #آپدیت مقدار فروش رفته هر محصول ____________________________________________
    # آپدیت مقدار فروش رفته هر محصول
    def update_tedad_mahsul_furush_rafteh(self):
        if os.path.exists(self.filename):
            df = pd.read_csv(self.filename)

            if "code_mahsul" in df.columns and "tedad_mahsul_furush_rafteh" in df.columns:
                df.loc[df["code_mahsul"]== self.code_mahsul, "tedad_mahsul_furush_rafteh"]=self.tedad_mahsul_furush_rafteh
                df.to_csv(self.filename, index=False)
                print(f"✅tedad mahsul furush rafteh berooz shod.")
                print("_"*20)

        else:
            print("❎file 'mahsulat_info.csv' vojod nadarad!")
            print("_" * 20)

    # نمایش کل محصولات ____________________________________________
    #نمایش کل محصولات
    def show_kolle_mahsulat(self):
        if os.path.exists(self.filename):
            df=pd.read_csv(self.filename)
            print("👇🏻kolle mahsulat:")
            print()
            print(df)
            print("_" * 20)

        else:
            print("❎anbar khali")
            print("_" * 20)

# class Sefareshat:
#     # ثبت زمان خرید
#     now = jdatetime.datetime.now()
#
#     def __init__(self,mahsul, code_mahsul ,moshtary, code_karbary, karmand, code_karmand,tedade_kharid ,mablaghe_nahaii_bade_takhfif=0,
#                  date_sefaresh=now,date_tahvil= now+ jdatetime.timedelta(days = 7) , filename= "Sefareshat_info.csv"):
#                 #نمونه محصول و مشتری را در init اوردم که بتوانم از اطلاعات خود نمونه ها استفاده کنم
#         self.mahsul = mahsul
#         self.code_mahsul=code_mahsul
#         self.moshtary=moshtary
#         self.code_karbary=code_karbary
#         self.tedade_kharid=tedade_kharid
#         self.mablaghe_nahaii_bade_takhfif=mablaghe_nahaii_bade_takhfif
#         self.date_sefaresh=date_sefaresh
#         self.date_tahvil=date_tahvil
#         self.filename=filename
#         self.karmand=karmand
#         self.code_karmand=code_karmand
#
#         # محاسبه مبلغ سفارش
#         self.mablagh_sefaresh = self.tedade_kharid * self.mahsul.gheimat
#
#         # محاسبه مبلغ نهایی سفارش بعد از تخفیف
#         self.mablaghe_nahaii_bade_takhfif = self.mablagh_sefaresh - self.meghdare_takhfif
#
#             #ملزومات ایجاد فایل برای کلاس سفارشات ____________________________________________
#
#     #ثبت سفارش در فایل
#     def sabte_sefaresh(self):
#
#         self.sutuns=["shmare_sefaresh", "code_karbary", "code_mahsul" ,"gheimat","tedade_kharid","mablagh_sefaresh","meghdare_takhfif","mablaghe_nahaii_bade_takhfif","date_sefaresh", "date_tahvil", "bedehi", "code_karmand"]
#
#         # اگر فایل موجود نباشه، فایل را با نام ستون بالا ایجاد میکنیم
#         if not os.path.exists( self.filename):
#             df=pd.DataFrame(columns=self.sutuns )
#             df.to_csv(self.filename, index=False)
#
#         df= pd.read_csv(self.filename)
#
#         # ____________________________________________
#
#          # اختصاص شماره به محصولات
#         if not df.empty:
#             self.shmare_sefaresh=df["shmare_sefaresh"].max() + 1 #ماکسیمم مقدار ستون شماره سفارش را بعلاوه یک میکنیم
#         else:
#             self.shmare_sefaresh=201
#
#
#         # مانده در انبار ____________________________________________
#
#         df_mahsulat=pd.read_csv("Mahsulat_info.csv")
#         mande_dar_anbar_file = df_mahsulat.loc[df_mahsulat["code_mahsul"]==self.code_mahsul , "mande_dar_anbar"].iloc[0]
#
#         # بررسی موجودی در انبار
#         if mande_dar_anbar_file < self.tedade_kharid:
#             print("❎Etmame mojudi!")
#             print("_" * 20)
#             return
#
#         else:
#             # کاهش موجودی انبار
#             self.mahsul.mande_dar_anbar =mande_dar_anbar_file - self.tedade_kharid
#             self.mahsul.update_mande_dar_anbar() #ذخیره مقدار جدید در فایل محصولات اینفو
#
#             # محاسبه امتیاز مشتری بر اساس خرید
#             self.emtiaz = self.mablagh_sefaresh // 1000
#
#             # اگر مشتری بدهی داشته باشد، تخفیف 0 میشه
#             if self.moshtary.bedehi > 0:
#                 self.meghdare_takhfif = 0
#             else:
#                 # هر دو امتیاز = 10% تخفیف
#                 # تبدیل امتیاز به تخفیف
#                 self.darsade_meghdare_takhfif = math.floor(self.emtiaz / 2) * 0.1
#                 self.meghdare_takhfif = self.darsade_meghdare_takhfif * self.mablagh_sefaresh
#
#             print(f"☑️Emtiaz moshtary ba code karbary '{self.code_karbary}': {self.emtiaz}")
#             print(f"☑️Meghdare takhfif baraye code karbary '{self.code_karbary}': {self.meghdare_takhfif}")
#             print("_" * 20)
#
#             # محاسبه مبلغ سفارش ____________________________________________
#
#             # #محاسبه مبلغ سفارش با توجه به تعداد کالا
#             self.moshtary.mablagh_sefaresh = self.mahsul.gheimat * self.tedade_kharid
#
#             # امتیاز و تخفیف  کاربر ️👇____________________________________________
#
#             #کل خریدهایی که کلا مشتری انجام داده
#             self.moshtary.kolle_mablaghe_kharid += self.mablagh_sefaresh
#             # self.moshtary.meghdare_takhfif += self.mablagh_sefaresh
#
#             # مقدار تخفیف جدید را به مقدار تخفیف قبلی اضافه میکنیم
#             self.moshtary.meghdare_takhfif += self.meghdare_takhfif
#
#             # #محاسبه مقادیر جدید برای مشتری
#             # مبلغ خرید جدید را به کال مبلغ خرید قبلی ضافه میکنیم
#             # self.mablaghe_nahaii_bade_takhfif += (self.mablagh_sefaresh - self.meghdare_takhfif)
#
#             # ____________________________________________
#
#             # ایجاد داده جدید سفارش
#             new_data = pd.DataFrame([{"shmare_sefaresh": self.shmare_sefaresh,
#                                       "code_karbary": self.code_karbary,
#                                       "code_mahsul": self.code_mahsul,
#                                       "gheimat": self.mahsul.gheimat,
#                                       "tedade_kharid": self.tedade_kharid,
#                                       "mablagh_sefaresh": self.mablagh_sefaresh,
#                                       "meghdare_takhfif": self.moshtary.meghdare_takhfif,
#                                       "mablaghe_nahaii_bade_takhfif":self.mablaghe_nahaii_bade_takhfif,
#                                       "date_sefaresh": self.date_sefaresh,
#                                       "date_tahvil": self.date_tahvil,
#                                       "bedehi": self.moshtary.bedehi,
#                                       "code_karmand":self.code_karmand}])
#
#             ##_____________________________________________________________
#
#             # اضافه کردن اطلاعات به فایل
#             new_data.to_csv(self.filename, mode='a', header=False, index=False)
#             print(f"✅Sefaresh {self.shmare_sefaresh} sabt shod!")
#             print("_" * 20)
#
#             ##_____________________________________________________________
#
#             self.karmand.update_kolle_mablaghe_furush()
#
#             ##_____________________________________________________________
#
#
#             #بروزرسانی فایل Moshtarian_info.csv
#             df_moshtarian=pd.read_csv("Moshtarian_info.csv")
#             df_moshtarian.loc[df_moshtarian["code_karbary"] == self.moshtary.code_karbary , "kolle_mablaghe_kharid"] = self.moshtary.kolle_mablaghe_kharid
#             df_moshtarian.loc[df_moshtarian["code_karbary"] == self.moshtary.code_karbary , "meghdare_takhfif"] = self.moshtary.meghdare_takhfif
#             df_moshtarian.to_csv("Moshtarian_info.csv", index=False)
#
#             self.moshtary.update_mablaghe_nahaii_bade_takhfif()
#
#     ##_____________________________________________________________
#
#     # نمایش کل سفارشات
#     def show_kolle_sefareshat(self):
#         if os.path.exists(self.filename):
#             df = pd.read_csv(self.filename)
#             print("👇🏻kolle sefareshat:")
#             print()
#             print(df)
#             print("_" * 20)
#
#         else:
#             print("❎Sefareshi mojod nist")
#             print("_" * 20)
#


#ایجاد کلاس سفارشات2 ____________________________________________
# کلاس سفارشات2 برخلاف کلاس سفارشات مستقل از کلاس محصولات است. برای دریافت سفارش مستقیم
#هدف: میخواهیم از لیست محصولاتی که قبلا ثبت شده خرید بزنیم اما در کلاس سفارشات همزمان محصولی در انبار ثبت میشد که مشکل ساز میشد
class Sefareshat2:
    # ثبت زمان خرید
    now = jdatetime.datetime.now()

    #مقادیر اولیه کلاس سفارشات2 ____________________________________________

    def __init__(self,name_mahsul, code_mahsul, gheimat, tedade_kharid, moshtary,karmand, mablaghe_nahaii_bade_takhfif=0,
                 date_sefaresh=now, date_tahvil=now+jdatetime.timedelta(days = 7), filename= "Sefareshat_info.csv"):
        self.name_mahsul=name_mahsul
        self.code_mahsul=code_mahsul
        self.gheimat=gheimat
        self.tedade_kharid=tedade_kharid
        # self.mande_dar_anbar=mande_dar_anbar
        self.moshtary=moshtary
        self.karmand=karmand
        self.mablaghe_nahaii_bade_takhfif=mablaghe_nahaii_bade_takhfif
        self.date_sefaresh=date_sefaresh
        self.date_tahvil=date_tahvil
        self.filename=filename

        #  # محاسبه مبلغ سفارش با توجه به تعداد کالا
        self.mablagh_sefaresh = self.tedade_kharid * self.gheimat

    # ملزومات ایجاد فایل برای کلاس سفارشات2 ____________________________________________

    # ثبت سفارش در فایل
    def sabte_sefaresh(self):

        self.sutuns = ["shmare_sefaresh", "code_karbary", "code_mahsul", "gheimat", "tedade_kharid",
                       "mablagh_sefaresh", "meghdare_takhfif", "mablaghe_nahaii_bade_takhfif", "date_sefaresh",
                       "date_tahvil", "bedehi", "code_karmand"]


        # اگر فایل موجود نباشه، فایل را با نام ستون بالا ایجاد میکنیم
        if not os.path.exists( self.filename):
            df=pd.DataFrame(columns=self.sutuns )
            df.to_csv(self.filename, index=False)

        df= pd.read_csv(self.filename)

        #اختصاص شماره به محصولات ____________________________________________

        # اختصاص شماره به محصولات
        if not df.empty:
            self.shmare_sefaresh=df["shmare_sefaresh"].max() + 1 #ماکسیمم مقدار ستون شماره سفارش را بعلاوه یک میکنیم
        else:
            self.shmare_sefaresh=201

        # مانده در انبار ____________________________________________

        if not os.path.exists("Mahsulat_info.csv"):
            print("❎Hich mahsuli dar anbar mojud nist!")
            print("_" * 20)
            # return

        elif "Mahsulat_info.csv":
            df_mahsulat=pd.read_csv("Mahsulat_info.csv")

            if self.code_mahsul not in df_mahsulat["code_mahsul"].values :
                print("❎In code az mahsulat mojud nist")
                print("_" * 20)

            else:
                mande_dar_anbar_file= df_mahsulat.loc[df_mahsulat["code_mahsul"] == self.code_mahsul, "mande_dar_anbar"].iloc[0]
                # عبارت iloc[0] برای این است که، اولین مقدار از سی انتخاب شده را برمیگردانیم. مطمئن شویم فقط یک مقدرا برگردانده میشود.


                # بررسی موجودی در انبار
                if mande_dar_anbar_file < self.tedade_kharid:
                    print("❎Etmame mojudi!")
                    print("_" * 20)
                    return

                else:
                    #کاهش موجودی انبار
                        df_mahsulat.loc[df_mahsulat["code_mahsul"]== self.code_mahsul, "mande_dar_anbar"] -= self.tedade_kharid
                        df_mahsulat.to_csv("Mahsulat_info.csv", index=False)


                        #امتیاز و تخفیف  کاربر ️👇____________________________________________

                        # محاسبه امتیاز مشتری بر اساس خرید
                        self.emtiaz = self.mablagh_sefaresh // 1000

                        # اگر مشتری بدهی داشته باشد، تخفیف 0 میشه
                        if self.moshtary.bedehi > 0:
                            self.meghdare_takhfif = 0
                        else:
                            # هر دو امتیاز = 10% تخفیف
                            # تبدیل امتیاز به تخفیف
                            self.darsade_meghdare_takhfif = math.floor(self.emtiaz / 2) * 0.1
                            self.meghdare_takhfif = self.darsade_meghdare_takhfif * self.mablagh_sefaresh

                        print(f"☑️Emtiaz moshtary ba code karbary '{self.moshtary.code_karbary}': {self.emtiaz}")
                        print(f"☑️Meghdare takhfif baraye code karbary '{self.moshtary.code_karbary}': {self.meghdare_takhfif}")
                        print("_" * 20)

                        # محاسبه مبلغ نهایی سفارش بعد از تخفیف
                        self.mablaghe_nahaii_bade_takhfif = self.mablagh_sefaresh - self.meghdare_takhfif


                        #کل خریدهایی که کلا مشتری انجام داده
                        self.moshtary.kolle_mablaghe_kharid += self.mablagh_sefaresh
                        # self.moshtary.meghdare_takhfif += self.mablagh_sefaresh

                        # مقدار تخفیف جدید را به مقدار تخفیف قبلی اضافه میکنیم
                        self.moshtary.meghdare_takhfif += self.meghdare_takhfif

                        #ایجاد دیتای جدید برای فایل از کلاس سفارشات2____________________________________________
                        # ایجاد دیتای جدید سفارش
                        new_data = pd.DataFrame([{"shmare_sefaresh": self.shmare_sefaresh,
                                                  "code_karbary": self.moshtary.code_karbary,
                                                  "code_mahsul": self.code_mahsul,
                                                  "gheimat": self.gheimat,
                                                  "tedade_kharid": self.tedade_kharid,
                                                  "mablagh_sefaresh": self.mablagh_sefaresh,
                                                  "meghdare_takhfif": self.moshtary.meghdare_takhfif,
                                                  "mablaghe_nahaii_bade_takhfif":self.mablaghe_nahaii_bade_takhfif,
                                                  "date_sefaresh": self.date_sefaresh,
                                                  "date_tahvil": self.date_tahvil,
                                                  "bedehi": self.moshtary.bedehi,
                                                  "code_karmand":self.karmand.code_karmand}])

                        ##اضافه کردن اطلاعات به فایل سفارشات2_____________________________________________________________

                        # اضافه کردن اطلاعات به فایل
                        new_data.to_csv(self.filename, mode='a', header=False, index=False)
                        print(f"✅️Sefaresh {self.shmare_sefaresh} sabt shod!")
                        print("_" * 20)

                        #کل مبلغ فروشی که یک کارمند داشته_____________________________________________________________

                        self.karmand.update_kolle_mablaghe_furush()

                        #بروزرسانی فایل Moshtarian_info.csv_____________________________________________________________

                        #بروزرسانی فایل Moshtarian_info.csv
                        df_moshtarian=pd.read_csv("Moshtarian_info.csv")
                        df_moshtarian.loc[df_moshtarian["code_karbary"] == self.moshtary.code_karbary , "kolle_mablaghe_kharid"] = self.moshtary.kolle_mablaghe_kharid
                        df_moshtarian.loc[df_moshtarian["code_karbary"] == self.moshtary.code_karbary , "meghdare_takhfif"] = self.moshtary.meghdare_takhfif
                        df_moshtarian.to_csv("Moshtarian_info.csv", index=False)


                        self.moshtary.update_mablaghe_nahaii_bade_takhfif()

        # تعداد محصول فروش رفته _____________________________________________________________
        df_mahsulat.loc[df_mahsulat["code_mahsul"] == self.code_mahsul, "tedad_mahsul_furush_rafteh"] += self.tedade_kharid
        df_mahsulat.to_csv("Mahsulat_info.csv", index=False)

        # محصولی که فروش ناکافی داشته -- حذف محصول با فروش 5 عدد در ماه _____________________________________________________________

        # پیدا کردن اندیس محصولی که مینیموم میزان فروش را داشته
        # idxmin() برای پیدا کردن اندیسی است که کمترین مقدار را در ستون tedad_mahsul_furush_rafteh داشته
        min_index_mahsul= df_mahsulat["tedad_mahsul_furush_rafteh"].idxmin()

        # محاسبه مدت زمان
        # زمان توسط پانداس در دیتا فریم به صورت استرینگ ثبت میشه.
        # برای تفریق کردن دو زمان باید از استرینگ خراج شوند. بنابراین از متد jdatetime.datetime.strptime استفاده  میکنیم.
        start_time=jdatetime.datetime.strptime(df["date_sefaresh"][0], "%Y-%m-%d %H:%M:%S.%f")
        end_time=jdatetime.datetime.strptime(df["date_sefaresh"][min_index_mahsul] , "%Y-%m-%d %H:%M:%S.%f")

        modat_zaman=  end_time - start_time
        print(modat_zaman)


        # اگر 10 ثاینه گذشته و محصول میزان فروشش کمتر از 5 عدد بوده دستور حذف از انبار داده شود
        if (modat_zaman > jdatetime.timedelta(seconds=50))  and  (min_index_mahsul < 5):
            name_mahsul_min_forush=df_mahsulat.loc[min_index_mahsul, "name_mahsul"]
            code_mahsul_min_forush=df_mahsulat.loc[min_index_mahsul, "code_mahsul"]

            print(f"🔴Mizane forush '{name_mahsul_min_forush}' ba code '{code_mahsul_min_forush}' = '{min_index_mahsul}' , kamtarin mizane forush ra dashte!!!")


            # # اگر مقدار فروش محصول کمتر از 5 بوده شود دستور حذف از انبار داده شود
            # if min_index_mahsul < 5 :
            print(f"🔴Mahsul ba code {code_mahsul_min_forush}' forushe kafi nadashte! => az anbar hazf shavad!!!")

            print("_" * 20)


    #نمایش کل سفارشات _____________________________________________________________

    # نمایش کل سفارشات
    def show_kolle_sefareshat(self):
        if os.path.exists(self.filename):
            df = pd.read_csv(self.filename)
            print("👇🏻 kolle sefareshat:")
            print()
            print(df)
            print("_" * 20)

        else:
            print("❎Sefareshi mojod nist")
            print("_" * 20)

#ایجاد نمونه و تغییر مشخصات کارمند_____________________________________________________________
#ایجاد نمونه برای: ثبت کارمند جدید
karmand = Karmandan("Mahammad", "Mohammady", 98912  )

# تغییر مشخصات کارمند
karmand.update_info(new_name="Reza")

###ایجاد نمونه و تغییر مشخصات کاربر_____________________________________________________________

# ایجاد نمونه برای:ثبت کاربر جدید
moshtary=Moshtarian("Ali", "Mahdian",736  )
# moshtary=Moshtarian("Ali", "Mahdian",736 , bedehi=2000 )
# moshtary1=Moshtarian("amir", "Mahdian",736 , 0,0 )

# تغییر مشخصات کاربر
# moshtary.update_info(new_kodemelly_moshtary=73677)

#ایجاد نمونه و تغییر مشخصات محصول_____________________________________________________________
# ایجاد نمونه برای:ثبت محصول در انبار
mahsul = Mahsulat("NoteBook", 1000, 100)
mahsul.new_mahsul()

# # تغییر مشخصات محصول
# mahsul.update_info(new_name = "Notebook")

#ایجاد نمونه برای کلاس سفارشات _____________________________________________________________
# ایجاد نمونه برای: کلاس Sefareshat
# sefaresh = Sefareshat(mahsul, mahsul.code_mahsul, moshtary,moshtary.code_karbary, karmand, karmand.code_karmand,2)
# sefaresh = Sefareshat(mahsul, 105, moshtary,101, 2)

# ثبت خرید از کلاس سفارشات
# sefaresh.sabte_sefaresh()

#ایجاد نمونه برای کلاس سفارشات2 _____________________________________________________________
# ایجاد نمونه برای: کلاس Sefareshat2
# ایجاد نمونه برای سفارشی که از لیست محصولات بتوان بدون ایجاد نمونه جدید سفارش دریافت کرد = که هدف کلاس Sefareshat2 بود
sefaresh2 = Sefareshat2 ("book", 117,1000,10, moshtary, karmand)

# ثبت خرید از کلاس Sefareshat2
sefaresh2.sabte_sefaresh()

#نمایش جدول "کل محصولات در انبار" و "کل مشتریان" و "کل سفارشات" در خروجی_____________________________________________________________
# نمایش جدول "کل محصولات در انبار" و "کل مشتریان" و "کل سفارشات" در خروجی
# mahsul.show_kolle_mahsulat()  #این خاصیت برای کلاس سفارشات کار میکنه و چون وجودش ضروری نبود برای کلاس سفارشات2 فعال نشده
moshtary.show_kolle_moshtarian()
sefaresh2.show_kolle_sefareshat()
import types
from telebot import types
import telebot
import db

bot = telebot.TeleBot("")
class Work:
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button1 = types.KeyboardButton(text="Надіслати лабу")
    button2 = types.KeyboardButton(text="Отримати лабу")

    keyboard2 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button3 = types.KeyboardButton(text="вийти")
    keyboard.add(button1)
    keyboard.add(button2)
    keyboard2.add(button3)
    _count_of_atributes = 0

    nokey = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    _step_of_writing = 0

    _curent_reading = False
    _cur_teacher = "none"
    _cur_disc = "none"
    _cur_number = "none"
    _cur_var = "none"
    _cur_specs = "none"
    def __init__(self):
      keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
      button1 = types.KeyboardButton(text="Надіслати лабу")
      button2 = types.KeyboardButton(text="Отримати лабу")

      nokey = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

      keyboard2 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
      button3 = types.KeyboardButton(text="вийти")
      keyboard.add(button1)
      keyboard.add(button2)
      keyboard2.add(button3)
      _count_of_atributes = 0

      _step_of_writing = 0

      _curent_reading = False
      _cur_teacher = "none"
      _cur_disc = "none"
      _cur_number = "none"
      _cur_var = "none"
      _cur_specs = "none"

    def get_cur_teacher(self):
        return self._cur_teacher
    def get_cur_number(self):
        return self._cur_number
    def get_cur_disc(self):
        return self._cur_disc
    def get_cur_specs(self):
        return self._cur_specs
    def get_cur_var(self):
        return self._cur_var

    def set_cur_teacher(self,i):
      self._cur_teacher=i

    def set_cur_number(self,i):
      self._cur_number= i

    def set_cur_disc(self,i):
      self._cur_disc=i

    def set_cur_specs(self,i):
     self._cur_specs= i

    def set_cur_var(self,i):
        self._cur_var=i

    def get_curent_reading(self):
        return self._curent_reading

    def set_curent_reading(self, i):
        self._curent_reading = i

    def get_count_of_atributes(self):
        return self._count_of_atributes

    def set_count_of_atributes(self, i):
        self._count_of_atributes = i

    def get_step_of_writing(self):
        return self._step_of_writing

    def set_step_of_writing(self,i):
        self._step_of_writing=i

    def get_count(self):
        return self._cur_number

    def reading(self,message: telebot.types.Message):
      keyboard_search = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

      self._curent_reading = True
      keyboard_search = self.keyboards(self._count_of_atributes, message)

    def makeboard(self,list=[]):
         but = []
         str = 'nothing'
         keyboard_search = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

         for x in range(0, len(list)):
             str = list[x]
             but1 = types.KeyboardButton(text=f"{str}")
             keyboard_search.add(but1)

         return keyboard_search

    def keyboards(self,i, message: telebot.types.Message):
      lab = db.Labs()
      self._count_of_atributes += 1

      keyboard_search = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
      if i == 0:
        bot.send_message(message.chat.id, "Оберіть викладача:", reply_markup=self.makeboard(lab.get_all_teacher()))
      elif i == 1:
        bot.send_message(message.chat.id, "Оберіть предмет:", reply_markup=self.makeboard(lab.get_all_disc(self._cur_teacher)))
      elif i == 2:
        bot.send_message(message.chat.id, "Оберіть спеціальність:",
                         reply_markup=self.makeboard(lab.get_all_specs(self._cur_teacher, self._cur_disc)))
      elif i == 3:
        bot.send_message(message.chat.id, "Оберіть номер лаби:",
                         reply_markup=self.makeboard(lab.get_all_number(self._cur_teacher, self._cur_disc, self._cur_specs)))
      elif i == 4:
        bot.send_message(message.chat.id, "Оберіть варіант:",
                         reply_markup=self.makeboard(lab.get_all_variant(self._cur_teacher, self._cur_disc, self._cur_specs,self._cur_number)))
      else:
        list=lab.get_url(self._cur_teacher, self._cur_specs, self._cur_disc, self._cur_number,self._cur_var)
        if  len(list)!=0:
          for x in lab.get_url(self._cur_teacher, self._cur_specs, self._cur_disc, self._cur_number,self._cur_var):
            bot.send_document(message.chat.id, open(x, 'rb'))

        else :bot.send_message(message.chat.id, "Немає такого файлу:", reply_markup=self.keyboard)
        count_of_atributes = 0
        bot.send_message(message.chat.id, "Оберіть дію:", reply_markup=self.keyboard)

      return keyboard_search



work = Work()
@bot.message_handler(content_types=['document'])
def only_file(message: telebot.types.Message):
    if work.get_step_of_writing() == 6:
        work.set_step_of_writing(0)
        file_name = message.document.file_name
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(f"urls/{file_name}", 'wb') as new_file:
            new_file.write(downloaded_file)
        db.Labs().set_data(work.get_cur_number(), work.get_cur_var(), work.get_cur_teacher(), work.get_cur_specs(), work.get_cur_disc(), f"urls/{file_name}")
        bot.send_message(message.chat.id, "Оберіть дію:", reply_markup=work.keyboard)
    else:
        bot.send_message(message.chat.id, "Оберіть дію:", reply_markup=work.keyboard)

@bot.message_handler(content_types=['text'])
def but_answer(message: telebot.types.Message):

    if message.text == "/start":
        work.set_curent_reading(False)
        work.set_step_of_writing(0)
        work.set_count_of_atributes(0)
        bot.send_message(message.chat.id, "Оберіть дію:", reply_markup=work.keyboard)
    elif message.text == "Надіслати лабу":
        work.set_curent_reading(False)
        work.set_step_of_writing(0)
        work.set_count_of_atributes(0)
        work.set_step_of_writing(work.get_step_of_writing()+1)
        bot.send_message(message.chat.id, "Дані заповнюйте українськими літерами, імена типу Іванов І.В, при виборі групи ініціали, виберіть варіант 0, якщо варіанту немає ")
        bot.send_message(message.chat.id, "Наприклад: Соломко Л.А., Бази даних, ПІ, 12, 0")
        bot.send_message(message.chat.id, "Введіть викладача",reply_markup=work.nokey)
    elif message.text == "Отримати лабу":
        work.set_curent_reading(False)
        work.set_step_of_writing(0)
        work.set_count_of_atributes(0)
        work.reading(message)
    elif work.get_step_of_writing() != 0:
        if work.get_step_of_writing() == 1:
            work.set_cur_teacher( message.text)
            bot.send_message(message.chat.id, "Введіть предмет")
            work.set_step_of_writing(work.get_step_of_writing() + 1)
        elif work.get_step_of_writing() == 2:
            work.set_cur_disc( message.text)
            bot.send_message(message.chat.id, "Введіть спеціальність")
            work.set_step_of_writing(work.get_step_of_writing()+1)
        elif work.get_step_of_writing() == 3:
            work.set_cur_specs(message.text)
            bot.send_message(message.chat.id, "Введіть номер лаби")
            work.set_step_of_writing(work.get_step_of_writing() + 1)
        elif work.get_step_of_writing() == 4:
            work.set_cur_number( message.text)
            bot.send_message(message.chat.id, "Введіть варіант")
            work.set_step_of_writing(work.get_step_of_writing() + 1)
        elif work.get_step_of_writing() == 5:
            work.set_cur_var(message.text)
            bot.send_message(message.chat.id, "Надішліть файл лаби")
            work.set_step_of_writing(work.get_step_of_writing() + 1)
        else:  bot.send_message(message.chat.id, "Надішліть файл лаби")
    elif work.get_curent_reading() and work.get_count_of_atributes() != 0:
        if work.get_count_of_atributes() == 1:
            work.set_cur_teacher(message.text)
        elif work.get_count_of_atributes() == 2:
            work.set_cur_disc( message.text)
        elif work.get_count_of_atributes() == 3:
            work.set_cur_specs(message.text)
        elif work.get_count_of_atributes() == 4:
            work.set_cur_number(message.text)
        elif work.get_count_of_atributes() == 5:
            work.set_cur_var (message.text)
        work.reading(message)
    elif work.get_curent_reading() and work.get_count_of_atributes() == 0:
        work.set_curent_reading (False)
        work.set_cur_var (message.text)
        work.search()
    else:
        work.set_curent_reading(False)
        work.set_step_of_writing(0)
        work.set_count_of_atributes(0)
        bot.send_message(message.chat.id, "Оберіть дію:", reply_markup=work.keyboard)


bot.polling()

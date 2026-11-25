ХӨДӨӨ АЖ АХУЙН ВЭБ САЙТ (Flask)
================================

1) Хавтсыг VS Code дээр нээнэ:  File -> Open Folder -> khuduu_ajakhui
2) Terminal нээнэ:              Terminal -> New Terminal
3) (Заавал биш) виртуал орчин:
       python -m venv venv
       venv\Scripts\activate
4) Сан суулгана:
       pip install -r requirements.txt
5) Ажиллуулна:
       python app.py
6) Хөтөч дээр нээнэ:  http://127.0.0.1:5000

Бүтэц:
  app.py            - Flask-ийн үндсэн код (маршрут, нэвтрэлт, мэдээллийн сан)
  templates/        - HTML хуудсууд (base.html нь цэс, хөл хэсэгтэй)
  static/*.css       - загварууд (base, menu, home, content, login, dashboard)
  static/script.js  - гар утасны цэс
  database.db       - анх ажиллуулахад автоматаар үүснэ

Нэвтрэх хэсэг: /register дээр бүртгүүлээд, /login дээр нэвтэрнэ.

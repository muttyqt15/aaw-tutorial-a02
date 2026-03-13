"""Generate Tutorial A02 PDF report."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Preformatted,
    HRFlowable, Image, PageBreak, Table, TableStyle
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import os

OUTPUT = "/Users/qin/Projects/acad/aaw/tutorial-a02/Tutorial_WorkloadDesign_2306207101_MuttaqinMuzakkir.pdf"
SCREENSHOTS = "/Users/qin/Projects/acad/aaw/tutorial-a02/screenshots"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=2*cm,
    leftMargin=2*cm,
    topMargin=2*cm,
    bottomMargin=2*cm,
)

styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    'CustomTitle', parent=styles['Title'],
    fontSize=18, spaceAfter=6, textColor=colors.HexColor('#1a1a2e')
)
h1_style = ParagraphStyle(
    'H1', parent=styles['Heading1'],
    fontSize=14, textColor=colors.HexColor('#16213e'),
    spaceAfter=4, spaceBefore=12,
    borderPad=4,
)
h2_style = ParagraphStyle(
    'H2', parent=styles['Heading2'],
    fontSize=12, textColor=colors.HexColor('#0f3460'),
    spaceAfter=4, spaceBefore=8,
)
h3_style = ParagraphStyle(
    'H3', parent=styles['Heading3'],
    fontSize=10, textColor=colors.HexColor('#533483'),
    spaceAfter=2, spaceBefore=6,
)
body_style = ParagraphStyle(
    'Body', parent=styles['Normal'],
    fontSize=10, leading=14, spaceAfter=4, alignment=TA_JUSTIFY
)
code_style = ParagraphStyle(
    'Code', parent=styles['Code'],
    fontSize=8, leading=11, fontName='Courier',
    backColor=colors.HexColor('#f0f0f0'),
    textColor=colors.HexColor('#1a1a1a'),
    leftIndent=8, rightIndent=8, spaceBefore=4, spaceAfter=4,
    borderPad=6,
    borderWidth=1,
    borderColor=colors.HexColor('#b0b0b0'),
    borderRadius=2,
)
label_style = ParagraphStyle(
    'Label', parent=styles['Normal'],
    fontSize=8, textColor=colors.HexColor('#888888'),
    spaceAfter=2, fontName='Helvetica-Oblique'
)
answer_style = ParagraphStyle(
    'Answer', parent=styles['Normal'],
    fontSize=10, leading=14, spaceAfter=4, leftIndent=12,
    borderLeftWidth=3, borderLeftColor=colors.HexColor('#0f3460'),
    borderLeftPadding=8, alignment=TA_JUSTIFY
)
info_style = ParagraphStyle(
    'Info', parent=styles['Normal'],
    fontSize=9, leading=13, backColor=colors.HexColor('#e8f4f8'),
    leftIndent=8, rightIndent=8, spaceBefore=2, spaceAfter=4,
    borderPad=5,
)


def section_divider(color='#16213e'):
    return HRFlowable(width='100%', thickness=2, color=colors.HexColor(color), spaceAfter=6, spaceBefore=4)


def thin_divider():
    return HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#cccccc'), spaceAfter=4, spaceBefore=4)


def code_block(text):
    return Preformatted(text, code_style)


def img(filename, width=14*cm, caption=None):
    path = os.path.join(SCREENSHOTS, filename)
    if not os.path.exists(path):
        return [Paragraph(f"[Screenshot: {filename} - not found]", label_style)]
    elems = []
    try:
        from PIL import Image as PILImage
        with PILImage.open(path) as pil_img:
            orig_w, orig_h = pil_img.size
        aspect = orig_h / orig_w
        height = width * aspect
        max_h = 10 * cm
        if height > max_h:
            height = max_h
            width = height / aspect
        im = Image(path, width=width, height=height)
        im.hAlign = 'CENTER'
        elems.append(im)
    except Exception:
        try:
            im = Image(path, width=width)
            im.hAlign = 'CENTER'
            elems.append(im)
        except Exception as e:
            elems.append(Paragraph(f"[Image error: {e}]", label_style))
    if caption:
        elems.append(Paragraph(caption, label_style))
    return elems


def answer(text):
    return Paragraph(text, answer_style)


story = []

# --- COVER ---
story.append(Spacer(1, 3*cm))
story.append(Paragraph("Tutorial A02", title_style))
story.append(Paragraph("Workload Design", ParagraphStyle('SubTitle', parent=styles['Normal'],
    fontSize=22, textColor=colors.HexColor('#0f3460'), spaceAfter=8, alignment=TA_CENTER)))
story.append(section_divider())
story.append(Spacer(1, 0.5*cm))

info_table = Table([
    ['Nama', ':', 'Muttaqin Muzakkir'],
    ['NPM',  ':', '2306207101'],
    ['Mata Kuliah', ':', 'Arsitektur Aplikasi Web (AAW)'],
    ['Topik', ':', 'Stream Processing (Kafka, RabbitMQ) & Advanced Database (MySQL Master-Slave)'],
    ['Tanggal', ':', '9 Maret 2026'],
], colWidths=[3.5*cm, 0.5*cm, 12*cm])
info_table.setStyle(TableStyle([
    ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
    ('FONTNAME', (2,0), (2,-1), 'Helvetica'),
    ('FONTSIZE', (0,0), (-1,-1), 10),
    ('LEADING', (0,0), (-1,-1), 16),
    ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor('#16213e')),
]))
story.append(info_table)
story.append(PageBreak())

# --- SECTION A: KAFKA ---
story.append(Paragraph("Section A: Apache Kafka", h1_style))
story.append(section_divider())

# A1
story.append(Paragraph("A1: Memulai Kafka dan Membuat Topic (Q1)", h2_style))
story.append(Paragraph(
    "Kafka berjalan otomatis melalui Docker Compose (container <b>kafka</b> dengan port 9092). "
    "Berikut output pembuatan dan verifikasi topic <i>quickstart-events</i>:",
    body_style
))

story.append(code_block(
"""$ docker compose up -d
 Container kafka  Started
 Container rabbitmq  Started
 Container mysql-master  Started
 Container mysql-slave  Started

$ docker ps --filter "name=kafka" --format "table {{.Names}}\\t{{.Status}}\\t{{.Ports}}"
NAMES    STATUS          PORTS
kafka    Up 17 seconds   0.0.0.0:9092->9092/tcp, [::]:9092->9092/tcp

$ docker exec kafka /opt/kafka/bin/kafka-topics.sh \\
    --create --topic quickstart-events --bootstrap-server localhost:9092
Created topic quickstart-events.

$ docker exec kafka /opt/kafka/bin/kafka-topics.sh \\
    --list --bootstrap-server localhost:9092
quickstart-events

$ docker exec kafka /opt/kafka/bin/kafka-topics.sh \\
    --describe --topic quickstart-events --bootstrap-server localhost:9092
Topic: quickstart-events  TopicId: kMt-7ZqETISWmsDejI2zgg
  PartitionCount: 1  ReplicationFactor: 1  Configs: min.insync.replicas=1
  Topic: quickstart-events  Partition: 0  Leader: 1  Replicas: 1  Isr: 1"""
))

story.append(Paragraph("<b>Jawaban Q1:</b>", h3_style))
story.append(answer(
    "Topic <i>quickstart-events</i> berhasil dibuat dan diverifikasi menggunakan perintah "
    "<code>--list</code> (menampilkan nama topic) dan <code>--describe</code> (menampilkan detail: "
    "PartitionCount=1, ReplicationFactor=1, Leader=1). Kafka berjalan dalam mode KRaft (tanpa "
    "ZooKeeper) di dalam container Docker pada port 9092."
))

story.append(thin_divider())

# A2
story.append(Paragraph("A2: Producer Mengirim Events, Consumer Membaca (Q2 & Q3)", h2_style))
story.append(Paragraph(
    "Producer mengirim 5 pesan ke topic, kemudian consumer membaca semua pesan dari awal "
    "(<code>--from-beginning</code>):",
    body_style
))

story.append(code_block(
"""# Terminal Producer:
$ echo -e "Hello Kafka!\\nEvent number 1\\nEvent number 2\\n
Event number 3\\nStream processing test" | \\
  docker exec -i kafka /opt/kafka/bin/kafka-console-producer.sh \\
  --topic quickstart-events --bootstrap-server localhost:9092

# Terminal Consumer:
$ docker exec kafka /opt/kafka/bin/kafka-console-consumer.sh \\
  --topic quickstart-events --from-beginning --max-messages 10 \\
  --bootstrap-server localhost:9092

Hello Kafka!
Event number 1
Event number 2
Event number 3
Stream processing test
Hello Kafka!
Event number 1
Event number 2
Event number 3
Stream processing test
Processed a total of 10 messages"""
))

story.append(Paragraph("<b>Jawaban Q2:</b>", h3_style))
story.append(answer(
    "Consumer menerima semua pesan yang dikirim producer secara real-time. Dengan flag "
    "<code>--from-beginning</code>, consumer juga membaca pesan lama yang sudah tersimpan di log "
    "Kafka. Hal ini menunjukkan bahwa Kafka bersifat persistent - pesan disimpan di disk dan dapat "
    "dibaca ulang kapan saja."
))
story.append(Paragraph("<b>Jawaban Q3 (Jika Producer Membanjiri Data):</b>", h3_style))
story.append(answer(
    "Jika producer mengirim data dalam jumlah sangat besar (flood), consumer akan mengalami "
    "<i>consumer lag</i> - yaitu perbedaan offset antara pesan terakhir yang diproduksi dan pesan "
    "terakhir yang dikonsumsi. Namun Kafka tidak kehilangan data karena pesan dibu&ffer di disk "
    "(log retention). Consumer dapat catch-up ketika producer melambat. Inilah keunggulan Kafka "
    "sebagai message broker dengan durability tinggi."
))

story.append(thin_divider())

# A3
story.append(Paragraph("A3: Dua Consumer Secara Bersamaan (Q4)", h2_style))
story.append(Paragraph(
    "Dua consumer group berbeda (<i>consumer-group-a</i> dan <i>consumer-group-b</i>) membaca "
    "dari topic yang sama secara bersamaan:",
    body_style
))

story.append(code_block(
"""# Consumer 1 (group-a):
$ docker exec kafka /opt/kafka/bin/kafka-console-consumer.sh \\
  --topic quickstart-events --from-beginning --max-messages 5 \\
  --group consumer-group-a --bootstrap-server localhost:9092

Hello Kafka!
Event number 1
Event number 2
Event number 3
Stream processing test

# Consumer 2 (group-b) - berjalan bersamaan:
$ docker exec kafka /opt/kafka/bin/kafka-console-consumer.sh \\
  --topic quickstart-events --from-beginning --max-messages 5 \\
  --group consumer-group-b --bootstrap-server localhost:9092

Hello Kafka!
Event number 1
Event number 2
Event number 3
Stream processing test"""
))

story.append(Paragraph("<b>Jawaban Q4:</b>", h3_style))
story.append(answer(
    "Tanpa consumer group (atau dengan group berbeda): kedua consumer menerima SEMUA pesan -"
    "setiap consumer mendapat salinan penuh dari topic. Ini cocok untuk use case broadcasting "
    "(misalnya logging + analytics membaca data yang sama). "
    "Dengan consumer group yang SAMA: pesan dibagi (partitioned) antar consumer dalam group -"
    "setiap pesan hanya diterima oleh satu consumer. Ini cocok untuk scaling horizontal "
    "pemrosesan pesan."
))

story.append(thin_divider())

# A4
story.append(Paragraph("A4: Force-Stop Kafka, Observasi Behavior (Q5)", h2_style))
story.append(Paragraph(
    "Kafka dihentikan paksa saat producer sedang berjalan, lalu di-restart untuk verifikasi durability:",
    body_style
))

story.append(code_block(
"""# Stop kafka container:
$ docker stop kafka
kafka
Kafka stopped at: Mon Mar  9 16:50:46 WIB 2026

# Coba consumer saat kafka mati:
$ docker exec kafka /opt/kafka/bin/kafka-console-consumer.sh ...
Error response from daemon: container 7a0f21ec... is not running

# Restart kafka:
$ docker start kafka
kafka

# Consumer membaca ulang - data tetap ada:
$ docker exec kafka /opt/kafka/bin/kafka-console-consumer.sh \\
  --topic quickstart-events --from-beginning --max-messages 10 \\
  --bootstrap-server localhost:9092

Hello Kafka!
Event number 1
Event number 2
Event number 3
Stream processing test
Hello Kafka!
Event number 1
Event number 2
Event number 3
Stream processing test
Processed a total of 10 messages"""
))

story.append(Paragraph("<b>Jawaban Q5:</b>", h3_style))
story.append(answer(
    "Ketika Kafka dihentikan paksa: (1) Producer mendapat error koneksi - pesan yang belum "
    "ter-commit ke broker hilang dari buffer producer. (2) Consumer tidak dapat terhubung dan "
    "berhenti menerima pesan. (3) Namun semua pesan yang sudah TERSIMPAN di Kafka log (disk) "
    "tetap aman - terbukti saat Kafka direstart, consumer dapat membaca ulang semua pesan "
    "dari awal. Kafka menggunakan write-ahead log yang durable, sehingga data tidak hilang "
    "ketika broker restart normal maupun paksa."
))

story.append(PageBreak())

# --- SECTION B: RABBITMQ ---
story.append(Paragraph("Section B: RabbitMQ", h1_style))
story.append(section_divider('#533483'))

# B1
story.append(Paragraph("B1: RabbitMQ Management Dashboard (Q1)", h2_style))
story.append(Paragraph(
    "Dashboard diakses melalui browser di <code>http://localhost:15672</code> dengan kredensial "
    "<b>admin/admin</b>:",
    body_style
))
for elem in img('b1-rabbitmq-dashboard.png', caption="Gambar B1: RabbitMQ Management Dashboard - Overview tab"):
    story.append(elem)
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("<b>Jawaban Q1:</b>", h3_style))
story.append(answer(
    "Dashboard RabbitMQ Management menampilkan: (1) <b>Totals</b> - jumlah pesan dalam antrian, "
    "message rates (publish/deliver/ack per detik), dan global counts (Connections, Channels, "
    "Exchanges, Queues, Consumers). (2) <b>Nodes</b> - health node termasuk file descriptors, "
    "memory usage (135 MiB), disk space, dan uptime. (3) <b>Tabs navigasi</b> untuk monitoring "
    "Connections, Channels, Exchanges, Queues secara detail. Dashboard ini memudahkan observasi "
    "real-time terhadap aliran pesan di sistem."
))

story.append(thin_divider())

# B2
story.append(Paragraph("B2: publish.py dan consume.py", h2_style))

story.append(Paragraph("<b>publish.py:</b>", h3_style))
story.append(code_block(
"""import pika

credentials = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=credentials)
)
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body='Hello RabbitMQ!')
print("[x] Sent 'Hello RabbitMQ!'")

connection.close()"""
))

story.append(Paragraph("<b>consume.py:</b>", h3_style))
story.append(code_block(
"""import pika

credentials = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=credentials)
)
channel = connection.channel()

channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(f"[x] Received {body.decode()}")

channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
print('[*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()"""
))

story.append(thin_divider())

# B3
story.append(Paragraph("B3: Jalankan publish.py Beberapa Kali, Pantau Dashboard (Q2)", h2_style))
story.append(Paragraph(
    "Publisher dijalankan 3 kali, lalu queue <i>hello</i> dipantau di dashboard:",
    body_style
))

story.append(code_block(
"""$ python publish.py
[x] Sent 'Hello RabbitMQ!'

$ python publish.py
[x] Sent 'Hello RabbitMQ!'

$ python publish.py
[x] Sent 'Hello RabbitMQ!'"""))

for elem in img('b3-queue-messages.png', caption="Gambar B3: Queue 'hello' menampilkan 3 pesan Ready"):
    story.append(elem)
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("<b>Jawaban Q2:</b>", h3_style))
story.append(answer(
    "Setiap kali publish.py dijalankan, counter <b>Ready</b> pada queue bertambah 1. "
    "Saat consumer aktif, pesan langsung dikonsumsi dan counter turun. Tanpa consumer aktif, "
    "pesan terakumulasi di queue (terlihat di kolom Ready). Dashboard juga menampilkan "
    "message rate (publish/s dan deliver/s) yang berubah secara real-time."
))

story.append(thin_divider())

# B4
story.append(Paragraph("B4: Dua Consumer Bersamaan (Q3)", h2_style))
story.append(Paragraph(
    "Dua consumer dijalankan secara bersamaan; publisher mengirim 6 pesan - setiap consumer "
    "menerima tepat 3 pesan (round-robin):",
    body_style
))

story.append(code_block(
"""# Consumer 1 (Terminal 1):
[*] Waiting for up to 3 messages...
[x] Received Hello RabbitMQ!
[x] Received Hello RabbitMQ!
[x] Received Hello RabbitMQ!

# Consumer 2 (Terminal 2):
[*] Waiting for up to 3 messages...
[x] Received Hello RabbitMQ!
[x] Received Hello RabbitMQ!
[x] Received Hello RabbitMQ!

# Publisher (6x):
[x] Sent 'Hello RabbitMQ!'  (x6)"""
))

story.append(Paragraph("<b>Jawaban Q3:</b>", h3_style))
story.append(answer(
    "RabbitMQ mendistribusikan pesan menggunakan algoritma <b>round-robin</b> antar consumer "
    "yang terhubung ke queue yang sama. Dari 6 pesan yang dikirim, Consumer 1 mendapat 3 pesan "
    "dan Consumer 2 mendapat 3 pesan - distribusi merata. Setiap pesan hanya diterima oleh SATU "
    "consumer (berbeda dengan Kafka tanpa consumer group). Ini ideal untuk scaling horizontal "
    "worker processes."
))

story.append(thin_divider())

# B5
story.append(Paragraph("B5: Stop Consumer di Tengah Antrian (Q4)", h2_style))
story.append(Paragraph(
    "Queue diisi 5 pesan tanpa consumer aktif, kemudian consumer dihentikan setelah dijalankan. "
    "Dashboard menampilkan pesan yang tersisa:",
    body_style
))

story.append(code_block(
"""# Publish 5 pesan tanpa consumer:
$ python publish.py  # x5
[x] Sent 'Hello RabbitMQ!'  (x5)

# Dashboard menampilkan antrian:
Queue: hello | Ready: 7 | Unacked: 0 | Total: 7 | Consumers: 0"""
))

for elem in img('b5-queue-after-stop.png', caption="Gambar B5: Queue dengan 7 pesan Ready, 0 consumer aktif"):
    story.append(elem)
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("<b>Jawaban Q4:</b>", h3_style))
story.append(answer(
    "Perilaku bergantung pada setting acknowledgment: "
    "(1) Dengan <b>auto_ack=True</b> (konfigurasi saat ini): RabbitMQ menganggap pesan sudah "
    "diproses begitu dikirim ke consumer. Jika consumer mati setelah menerima pesan tetapi "
    "sebelum selesai memprosesnya, pesan HILANG. "
    "(2) Dengan <b>auto_ack=False</b>: RabbitMQ menunggu ACK eksplisit. Jika consumer mati "
    "tanpa mengirim ACK, pesan di-requeue otomatis dan dapat diambil consumer lain. "
    "Dashboard menunjukkan pesan tersisa di queue (Ready=7) saat tidak ada consumer aktif -"
    "RabbitMQ menyimpan pesan di memory/disk hingga ada consumer yang mengambilnya."
))

story.append(PageBreak())

# --- SECTION C: MYSQL MASTER-SLAVE ---
story.append(Paragraph("Section C: MySQL Master-Slave Replication", h1_style))
story.append(section_divider('#1a6b3c'))

# C1
story.append(Paragraph("C1: Master dan Slave Berjalan di Port Berbeda (Q1)", h2_style))

story.append(code_block(
"""$ docker ps --filter "name=mysql" \\
    --format "table {{.Names}}\\t{{.Status}}\\t{{.Ports}}"

NAMES          STATUS          PORTS
mysql-slave    Up 20 minutes   0.0.0.0:3307->3306/tcp
mysql-master   Up 20 minutes   0.0.0.0:3306->3306/tcp

$ docker exec mysql-master mysql -uroot -prootpass -e "SELECT 'master ready';"
master ready

$ docker exec mysql-slave mysql -uroot -prootpass -e "SELECT 'slave ready';"
slave ready"""
))

story.append(Paragraph("<b>Jawaban Q1:</b>", h3_style))
story.append(answer(
    "Dua instance MySQL berjalan di container terpisah: <b>mysql-master</b> pada port host "
    "<b>3306</b> dan <b>mysql-slave</b> pada port host <b>3307</b>. Keduanya dikonfigurasi "
    "dengan server-id berbeda (master: server-id=1 dengan binary logging aktif; slave: "
    "server-id=2 dengan relay-log). Perbedaan port memungkinkan aplikasi terhubung ke "
    "instance yang berbeda dari host yang sama."
))

story.append(thin_divider())

# C2
story.append(Paragraph("C2: Setup Replication", h2_style))

story.append(code_block(
"""# Master IP:
$ docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mysql-master
192.168.240.4

# Pada master - buat user replikasi:
mysql> CREATE USER 'replica'@'%' IDENTIFIED WITH mysql_native_password BY 'password';
mysql> GRANT REPLICATION SLAVE ON *.* TO 'replica'@'%';
mysql> FLUSH PRIVILEGES;
mysql> SHOW MASTER STATUS;
+------------------+----------+
| File             | Position |
+------------------+----------+
| mysql-bin.000004 |      847 |
+------------------+----------+

# Pada slave - konfigurasi replikasi:
mysql> CHANGE MASTER TO
    MASTER_HOST='192.168.240.4', MASTER_USER='replica',
    MASTER_PASSWORD='password', MASTER_PORT=3306,
    MASTER_LOG_FILE='mysql-bin.000004', MASTER_LOG_POS=847;
mysql> START SLAVE;
mysql> SHOW SLAVE STATUS\\G
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
        Seconds_Behind_Master: 0
                   Last_Error: (none)"""
))

story.append(thin_divider())

# C3
story.append(Paragraph("C3: INSERT di Master, Verifikasi di Slave (Q2)", h2_style))

story.append(code_block(
"""# Pada master:
mysql> CREATE DATABASE testdb;
mysql> USE testdb;
mysql> CREATE TABLE users(id INT, name VARCHAR(50));
mysql> INSERT INTO users VALUES(1,'Test');
mysql> INSERT INTO users VALUES(2,'Alice');
mysql> INSERT INTO users VALUES(3,'Bob');
mysql> SELECT * FROM users;
+----+-------+
| id | name  |
+----+-------+
|  1 | Test  |
|  2 | Alice |
|  3 | Bob   |
+----+-------+

# Pada slave (setelah insert di master):
mysql> USE testdb;
mysql> SELECT * FROM users;
+----+-------+
| id | name  |
+----+-------+
|  1 | Test  |
|  2 | Alice |
|  3 | Bob   |
+----+-------+"""
))

story.append(Paragraph("<b>Jawaban Q2:</b>", h3_style))
story.append(answer(
    "Data yang di-INSERT di master secara otomatis direplikasi ke slave melalui binary log. "
    "Proses: (1) Master mencatat setiap perubahan data ke binary log (mysql-bin.000004). "
    "(2) Slave IO thread membaca binary log dari master dan menyimpannya sebagai relay log. "
    "(3) Slave SQL thread menjalankan event dari relay log ke database slave. "
    "Hasilnya identik - ketiga row (Test, Alice, Bob) tersedia di slave tanpa perlu operasi "
    "manual apapun."
))

story.append(thin_divider())

# C4
story.append(Paragraph("C4: Force-Stop Master, Cek Slave (Q3)", h2_style))

story.append(code_block(
"""$ docker stop mysql-master
mysql-master

# Slave masih bisa melayani query:
mysql-slave> USE testdb;
mysql-slave> SELECT * FROM users;
+----+-------+
| id | name  |
+----+-------+
|  1 | Test  |
|  2 | Alice |
|  3 | Bob   |
+----+-------+

# Status slave setelah master mati:
mysql-slave> SHOW SLAVE STATUS\\G
             Slave_IO_Running: Connecting   ← tidak bisa reach master
            Slave_SQL_Running: Yes          ← data lokal tetap available
        Seconds_Behind_Master: NULL
                Last_IO_Error: Can't connect to MySQL server on '192.168.240.4:3306' (111)
      Slave_SQL_Running_State: Replica has read all relay log; waiting for more updates"""
))

story.append(Paragraph("<b>Jawaban Q3:</b>", h3_style))
story.append(answer(
    "Ketika master dihentikan: (1) Data yang sudah direplikasi ke slave tetap TERSEDIA -"
    "slave dapat melayani query read dengan data yang sudah ada (Test, Alice, Bob). "
    "(2) IO thread pada slave berstatus <i>Connecting</i> - slave terus mencoba terhubung "
    "ke master setiap 60 detik. (3) SQL thread tetap aktif (Yes) karena tidak perlu "
    "koneksi aktif ke master untuk menjalankan relay log yang sudah ada. "
    "Ini menunjukkan slave dapat berfungsi sebagai <b>read replica</b> darurat saat master down."
))

story.append(thin_divider())

# C5
story.append(Paragraph("C5: Menulis Langsung ke Slave (Q4)", h2_style))

story.append(code_block(
"""# Master direstart dulu:
$ docker start mysql-master

# Tulis langsung ke slave:
mysql-slave> USE testdb;
mysql-slave> INSERT INTO users VALUES(99,'DirectOnSlave');
mysql-slave> SELECT * FROM users;
+----+---------------+
| id | name          |
+----+---------------+
|  1 | Test          |
|  2 | Alice         |
|  3 | Bob           |
| 99 | DirectOnSlave |  ← ada di slave
+----+---------------+

# Cek di master - row 99 TIDAK ada:
mysql-master> USE testdb;
mysql-master> SELECT * FROM users;
+----+-------+
| id | name  |
+----+-------+
|  1 | Test  |
|  2 | Alice |
|  3 | Bob   |
+----+-------+"""
))

story.append(Paragraph("<b>Jawaban Q4:</b>", h3_style))
story.append(answer(
    "Write langsung ke slave TIDAK direplikasi ke master karena replikasi MySQL bersifat "
    "<b>satu arah (master → slave)</b>. Row dengan id=99 hanya ada di slave. "
    "Risiko: (1) <b>Data inconsistency</b> - slave memiliki data yang tidak ada di master, "
    "sehingga jika slave dipromosikan menjadi master baru (failover), data ini bisa "
    "bertentangan dengan replikasi berikutnya. "
    "(2) <b>Replication break</b> - jika master kemudian memasukkan row dengan id=99, "
    "slave akan error karena duplicate key. "
    "Best practice: slave seharusnya bersifat <b>read-only</b> (konfigurasi: "
    "<code>read_only=1</code>) untuk mencegah penulisan langsung."
))

story.append(Spacer(1, 1*cm))
story.append(section_divider())
story.append(Paragraph(
    "[ Akhir Tutorial A02 ] Muttaqin Muzakkir (2306207101)",
    ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9,
                   textColor=colors.HexColor('#888888'), alignment=TA_CENTER)
))

# Build PDF
doc.build(story)
print(f"PDF generated: {OUTPUT}")

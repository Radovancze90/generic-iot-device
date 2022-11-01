import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mysql.connector as mysql

mailer = smtplib.SMTP('smtp')

mysql_connection = None
query_fetch_devices_with_outage = ("""
SELECT
    t.id,
    t.name,
    (SELECT GROUP_CONCAT(r.name SEPARATOR ', ') FROM main_region_devices rd INNER JOIN main_region r ON r.id = rd.region_id WHERE rd.device_id = t.id) region_names,
    (SELECT GROUP_CONCAT(ud.name SEPARATOR ', ') FROM main_userdevice ud WHERE ud.device_id = t.id) user_names,
    t.last_ping_at
FROM (
    SELECT
        d.id,
        d.outage_report_for,
        d.name,
        MAX(dl.created_at) last_ping_at
    FROM main_devicelog dl
    INNER JOIN main_device d ON d.id = dl.device_id
    GROUP BY d.id
    HAVING MAX(dl.created_at) < DATE_SUB(NOW(), INTERVAL 1 MINUTE)
) t
WHERE t.outage_report_for IS NULL OR t.last_ping_at > t.outage_report_for
""")
query_update_device_outage_report_for = ("""
    UPDATE main_device SET outage_report_for = %s WHERE id = %s
""")
# query_fetch_device_crontab = ("""
#     SELECT GROUP_CONCAT(CONCAT(dc.hour, ':', dc.minute, ' - ', IF(dc.action = 'relay_on', 'Zapnout', 'Vypnout')) SEPARATOR ', ')
#     FROM main_devicecron dc
#     WHERE dc.device_id = %s
#     ORDER BY dc.hour ASC, dc.minute ASC
# """)
query_fetch_device_crontab = ("""
    SELECT TRIM(',' FROM GROUP_CONCAT(CONCAT(LPAD(dc.hour, 2, 0), ':', LPAD(dc.minute, 2, 0), IF(dc.action = 'relay_on', '', ',')) SEPARATOR ' - '))
    FROM main_devicecron dc
    WHERE dc.device_id = %s
    ORDER BY dc.hour ASC, dc.minute ASC;
""")
query_fetch_user_device_email_for_device = ("""
    SELECT u.email
    FROM main_userdevice ud
    INNER JOIN main_client c ON c.user_id = ud.user_id
    INNER JOIN auth_user u ON u.id = ud.user_id
    WHERE ud.device_id = %s AND c.outage_notification = 1
""")

def init_mysql_connection():
    global mysql_connection

    mysql_connection = mysql.connect(host="db", user="root", password="DB PASS", database="web")

def get_mysql_cursor():
    global mysql_connection

    try:
        mysql_connection.ping(reconnect=True, attempts=3, delay=5)
    except mysql.connector.Error as err:
        init_mysql_connection()

    return mysql_connection.cursor()

def send_client_notification(row):
    global mailer
    global query_fetch_device_crontab

    cursor = get_mysql_cursor()
    cursor.execute(query_fetch_device_crontab, (row[0], ))

    crontab = ""

    for crontab_row in cursor:
        crontab = crontab_row[0]

    html_content = """\
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>Text ..........</title>
        <style>a:hover {text-decoration:none;}</style>
    </head>
    <body style="padding:0; margin:0; font-family:Verdana,Tahoma,Arial,Helvetica,sans-serif; font-size:13px;">
    <div style="width:600px; margin:0 auto; padding:5px 0;">
        <div>
            <p>
                Dobrý den,<br>
                <br>
                automatickou kontrolou jsme zjistili, že zařízení
    """

    html_content += row[3]

    html_content += """\
                <br>
                která má nastavenou provozní dobu
    """

    html_content += crontab

    html_content += """\
                <br>
                Zpráva ....................

            </p>
        </div>
    </div>
    </body>
    </html>
    """

    cursor = get_mysql_cursor()
    cursor.execute(query_fetch_user_device_email_for_device, (row[0], ))

    for email_row in cursor:
        print(email_row[0])
	# tady to uprav
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Zařízení" + row[3] + " není dostupné"
        msg['From'] = "info@domena"
        msg['To'] = email_row[0]

        msg.attach(MIMEText(html_content, 'html'))

        mailer.sendmail("info@domena", email_row[0], msg.as_string())
	# až sem

def send_admin_notification(rows):
    global mailer

    html_content = """\
    <html>
        <head>
        </head>
        <body>
            <table width="100%" style="width:100%;">
                <thead>
                    <tr>
                        <th align="left" style="text-align:left;">Název zařízení</th>
                        <th align="left" style="text-align:left;">Regiony</th>
                        <th align="left" style="text-align:left;">Vlastníci</th>
                        <th align="left" style="text-align:left;">Poslední aktivita</th>
                    </tr>
                </thead>
                <tbody>
    """

    for row in rows:
        print(row)
        html_content += \
            "<tr>" + \
            "<td>" + row[1] + "</td>" + \
            "<td>" + row[2] + "</td>" + \
            "<td>" + row[3] + "</td>" + \
            "<td>" + row[4].strftime("%d.%m.%Y %H:%M") + "</td>" + \
            "</tr>\n"


    html_content += """
                </tbody>
            </table>
        </body>
    </html>
    """
    # tady to uprav
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Nová nedostupná zařízení"
    msg['From'] = "admin@donena"
    msg['To'] = "info@domena"

    msg.attach(MIMEText(html_content, 'html'))

    mailer.sendmail("admin@domena", "info@domena", msg.as_string())
    # až sem
init_mysql_connection()

cursor = get_mysql_cursor()
cursor.execute(query_fetch_devices_with_outage)

rows = []

for row in cursor:
    rows.append(row)

for row in rows:
    cursor.execute(query_update_device_outage_report_for, (row[4], row[0]))

mysql_connection.commit()

if len(rows) > 0:
    send_admin_notification(rows)

    for row in rows:
        send_client_notification(row)

mailer.quit()

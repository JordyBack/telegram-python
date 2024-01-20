import pymysql
import config
from datetime import datetime
import logging
from colorlog import ColoredFormatter

# Configuration du log avec une fonction pour la coloration
def configure_logging():
    log_format = "[%(levelname)s] %(message)s"
    logging.basicConfig(format=log_format, datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger()
    console_handler = logging.StreamHandler()
    logging.basicConfig(format=log_format)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logging.addLevelName(logging.INFO, "\033[94m%s\033[0m" % logging.getLevelName(logging.INFO))
    logging.addLevelName(logging.WARNING, "\033[93m%s\033[0m" % logging.getLevelName(logging.WARNING))
    logging.addLevelName(logging.ERROR, "\033[91m%s\033[0m" % logging.getLevelName(logging.ERROR))
    logging.addLevelName(logging.CRITICAL, "\033[91m%s\033[0m" % logging.getLevelName(logging.CRITICAL))
configure_logging()

# Connection à la bdd
def getConnection():
    connection = pymysql.connect(host=config.mysql_host,
                                 user=config.mysql_user,
                                 password=config.mysql_pw,
                                 db=config.mysql_db,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor,
                                 autocommit=True)
    return connection   

def checkDatabaseConnection():
    try:
        connection = getConnection()
        connection.ping()
        print("=====================================================================")
        logging.info("La base de données est connectée avec succès.")
    except pymysql.MySQLError as e:
        logging.error(f"Erreur lors de la connexion à la base de données : {e}")

def createTables():
    connection = getConnection()
    with connection.cursor() as cursor:
        tablename = "users"
        try:
            cursor.execute(
                "	CREATE TABLE `" + tablename + "` (  `userid` int(11) DEFAULT NULL,  `open_ticket` int(4) DEFAULT 0,  `banned` int(4) DEFAULT 0,  \
                `open_ticket_spam` int(4) DEFAULT 1,  `open_ticket_link` varchar(50) DEFAULT NULL,  `open_ticket_time` datetime NOT NULL DEFAULT '1000-01-01 00:00:00')")
            return createTables
        except pymysql.MySQLError as e:
            print("\033[91m[Erreur] La table `users`est déjà existante.\033[0m")
            print("=====================================================================")

def spam(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = "SELECT banned, open_ticket, open_ticket_spam FROM users WHERE userid = %s"
        cursor.execute(sql, user_id)
        data = cursor.fetchone()
        ticket_spam = data['open_ticket_spam']

        sql = "UPDATE users SET open_ticket_spam = %s WHERE userid = %s"
        spam = ticket_spam + 1
        cursor.execute(sql, (spam, user_id))
        return spam


def user_tables(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = "SELECT open_ticket, banned, open_ticket_time, open_ticket_spam, open_ticket_link FROM users WHERE userid = %s"
        cursor.execute(sql, user_id)
        data = cursor.fetchone()
        return data


def getOpenTickets():
    connection = getConnection()
    with connection.cursor() as cursor:
        tmp = []
        cursor.execute("SELECT userid FROM users WHERE open_ticket = 1")
        for i in cursor.fetchall():
            tmp.append(i['userid'])
        return tmp


def getBanned():
    connection = getConnection()
    with connection.cursor() as cursor:
        tmp = []
        cursor.execute("SELECT userid FROM users WHERE banned = 1")
        for i in cursor.fetchall():
            tmp.append(i['userid'])
        return tmp


def start_bot(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = "SELECT EXISTS(SELECT userid FROM users WHERE userid = %s)"
        cursor.execute(sql, user_id)
        result = cursor.fetchone()
        if not list(result.values())[0]:
            sql = "INSERT INTO users(userid) VALUES (%s)"
            cursor.execute(sql, user_id)
            logging.info(f"\033[94mUtilisateur {user_id} ajouté à la base de données.\033[0m")
        else:
            logging.info(f"\033[94mL'utilisateur {user_id} est déjà présent dans la base de données.\033[0m")

def open_ticket(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = "UPDATE users SET open_ticket = 1, open_ticket_time = %s WHERE userid = %s"
        now = datetime.now()
        cursor.execute(sql, (now, user_id))
        open_tickets.append(user_id)
        return open_ticket


def post_open_ticket(link, msg_id):
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = "UPDATE users SET open_ticket_link = %s WHERE userid = %s"
        cursor.execute(sql, (link, msg_id))
        return post_open_ticket


def reset_open_ticket(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = "UPDATE users SET open_ticket = 0,  open_ticket_spam = 1 WHERE userid = %s"
        cursor.execute(sql, user_id)
        open_tickets.pop(open_tickets.index(user_id))
        return reset_open_ticket


def ban_user(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = "UPDATE users SET banned = 1 WHERE userid = %s"
        cursor.execute(sql, user_id)
        banned.append(user_id)
        return ban_user


def unban_user(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = "UPDATE users SET banned = 0 WHERE userid = %s"
        cursor.execute(sql, user_id)
        banned.pop(banned.index(user_id))
        return unban_user

checkDatabaseConnection()
createTables = createTables()
open_tickets = getOpenTickets()
banned = getBanned()

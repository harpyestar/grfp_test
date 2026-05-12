"""
MySQL 数据库连接工具
提供 RFP 项目相关的酒店数据查询功能（grfp 库）

使用方法:
    # 方式一：上下文管理器
    with MySQLDB() as db:
        hotels = db.query_normal_hotels(project_id)

    # 方式二：便捷函数（自动连接/关闭）
    hotels = get_normal_hotels(project_id)
"""

import pymysql
from typing import List, Dict
from utils.logger import get_logger

logger = get_logger(__name__)

# MySQL 数据库连接配置
MYSQL_CONFIG = {
    "host": "172.16.88.71",
    "port": 3306,
    "user": "root",
    "password": "ABcd@1234",
    "database": "grfp",
    "charset": "utf8mb4",
}


class MySQLDB:
    """MySQL 数据库操作类"""

    def __init__(self):
        self.connection = None

    def connect(self) -> None:
        """建立 MySQL 数据库连接"""
        logger.info(
            f"正在连接 MySQL 数据库 {MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}/{MYSQL_CONFIG['database']} ..."
        )
        try:
            self.connection = pymysql.connect(
                host=MYSQL_CONFIG["host"],
                port=MYSQL_CONFIG["port"],
                user=MYSQL_CONFIG["user"],
                password=MYSQL_CONFIG["password"],
                database=MYSQL_CONFIG["database"],
                charset=MYSQL_CONFIG["charset"],
                cursorclass=pymysql.cursors.DictCursor,
            )
            logger.info("MySQL 数据库连接成功")
        except pymysql.Error as e:
            error_msg = f"MySQL 数据库连接失败: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e

    def close(self) -> None:
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            logger.info("MySQL 数据库连接已关闭")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def query_normal_hotels(self, project_id: str) -> List[Dict]:
        """
        查询普通酒店名单（t_project_intent_hotel）
        根据 project_id 和 invite_status=1 过滤，关联 t_hotel 获取酒店名

        Args:
            project_id: 项目 ID

        Returns:
            List[Dict]: [{hotel_id, hotel_name}, ...]
        """
        sql = """
        SELECT t.hotel_id, h.name_en_us AS hotel_name
        FROM t_project_intent_hotel t
        JOIN t_hotel h ON t.hotel_id = h.hotel_id
        WHERE t.project_id = %(project_id)s AND t.invite_status = 1
        ORDER BY t.hotel_id
        """
        cursor = self.connection.cursor()
        cursor.execute(sql, {"project_id": project_id})
        rows = cursor.fetchall()
        cursor.close()
        logger.info(f"查询到 {len(rows)} 条普通酒店记录")
        return [{"hotel_id": str(row["hotel_id"]), "hotel_name": row["hotel_name"]} for row in rows]

    def query_group_hotels(self, project_id: str) -> List[Dict]:
        """
        查询集团意向单店酒店名单（t_project_invite_hotel）
        根据 project_id 过滤，关联 t_hotel 获取酒店名

        Args:
            project_id: 项目 ID

        Returns:
            List[Dict]: [{hotel_id, hotel_name}, ...]
        """
        sql = """
        SELECT t.hotel_id, h.name_en_us AS hotel_name
        FROM t_project_invite_hotel t
        JOIN t_hotel h ON t.hotel_id = h.hotel_id
        WHERE t.project_id = %(project_id)s
        ORDER BY t.hotel_id
        """
        cursor = self.connection.cursor()
        cursor.execute(sql, {"project_id": project_id})
        rows = cursor.fetchall()
        cursor.close()
        logger.info(f"查询到 {len(rows)} 条集团酒店记录")
        return [{"hotel_id": str(row["hotel_id"]), "hotel_name": row["hotel_name"]} for row in rows]


# ======================== 便捷查询函数（自动连接/关闭）=======================

def get_normal_hotels(project_id: str) -> List[Dict]:
    """查询普通酒店名单，自动连接和关闭数据库"""
    with MySQLDB() as db:
        return db.query_normal_hotels(project_id)


def get_group_hotels(project_id: str) -> List[Dict]:
    """查询集团酒店名单，自动连接和关闭数据库"""
    with MySQLDB() as db:
        return db.query_group_hotels(project_id)


# ======================== 数据库连接测试 ========================

def test_connection() -> bool:
    """
    测试 MySQL 数据库连接是否正常（独立运行，不需外部依赖）

    Returns:
        True  连接成功
        False 连接失败

    使用方式:
        python -m utils.mysql_db
    """
    print("=" * 60)
    print("MySQL 数据库连接测试")
    print("=" * 60)
    print(f"目标: {MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}/{MYSQL_CONFIG['database']}")
    print(f"用户: {MYSQL_CONFIG['user']}")
    print()

    try:
        with MySQLDB() as db:
            cursor = db.connection.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            cursor.close()

            if result and result["1"] == 1:
                print("[OK] 数据库连接正常")
                print(f"[OK] 基础查询验证通过: SELECT 1 = {result['1']}")

            tables_to_check = [
                ("t_project_intent_hotel", "普通酒店意向表"),
                ("t_project_invite_hotel", "集团邀请酒店表"),
                ("t_hotel", "酒店信息表"),
            ]
            for table_name, desc in tables_to_check:
                cursor = db.connection.cursor()
                cursor.execute(
                    "SELECT COUNT(*) AS cnt FROM information_schema.tables "
                    "WHERE table_schema = %(db)s AND table_name = %(table)s",
                    {"db": MYSQL_CONFIG["database"], "table": table_name},
                )
                row = cursor.fetchone()
                cursor.close()
                if row and row["cnt"] > 0:
                    print(f"[OK] 表 {table_name}（{desc}）可访问")
                else:
                    print(f"[WARN] 表 {table_name}（{desc}）不可访问")

            sql_checks = [
                "SELECT COUNT(*) AS cnt FROM t_project_intent_hotel",
                "SELECT COUNT(*) AS cnt FROM t_project_invite_hotel",
                "SELECT COUNT(*) AS cnt FROM t_hotel",
            ]
            print()
            print("--- 验证实际 SQL ---")
            for sql in sql_checks:
                cursor = db.connection.cursor()
                try:
                    cursor.execute(sql)
                    row = cursor.fetchone()
                    print(f"[OK] {sql} -> {row['cnt']} 行")
                except pymysql.Error as e:
                    print(f"[FAIL] {sql} -> {e}")
                finally:
                    cursor.close()

        print()
        print("[OK] 数据库连接测试通过")
        print("=" * 60)
        return True

    except Exception as e:
        print()
        print(f"[FAIL] 数据库连接失败: {e}")
        print("=" * 60)
        return False


if __name__ == "__main__":
    test_connection()
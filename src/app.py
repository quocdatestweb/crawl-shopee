from crontab import CronTab


class Crawler:
    def __init__(self):
        cron = CronTab(user="root")
        cron.remove_all()

        # collect shop flow a
        self.execute(
            lambda: cron.new(
                command="/usr/local/bin/python /crawler/src/job/shopee/collect_shop_flow_a.py"
            ).setall(0, "0,12", None, None, None),
            quantity=1,
        )

        # collect shop flow b
        self.execute(
            lambda: cron.new(
                command="/usr/local/bin/python /crawler/src/job/shopee/collect_shop_flow_b.py"
            ).setall(0, "0,12", None, None, None),
            quantity=1,
        )

        # get shop detail
        self.execute(
            lambda: cron.new(
                command="/usr/local/bin/python /crawler/src/job/shopee/get_shop_detail.py"
            ).setall(0, "0,12", None, None, None),
            quantity=1,
        )

        # save product statistics
        self.execute(
            lambda: cron.new(
                command="/usr/local/bin/python /crawler/src/job/database/save_product_statistics.py"
            ).setall(0, None, None, None, None),
            quantity=1,
        )

        # save shop statistics
        self.execute(
            lambda: cron.new(
                command="/usr/local/bin/python /crawler/src/job/database/save_shop_statistics.py"
            ).setall(0, None, None, None, None),
            quantity=1,
        )

        # Sync filter table
        self.execute(
            lambda: cron.new(
                command="/usr/local/bin/python /crawler/src/job/database/sync_filter_table.py"
            ).setall(0, "0,8,16", None, None, None),
            quantity=1,
        )

        # get product in shop
        self.execute(
            lambda: cron.new(
                command="/usr/local/bin/python /crawler/src/job/shopee/collect_product_in_shop.py 84600"
            ).setall(0, "0,12", None, None, None),
            quantity=1,
        )

        # test
        self.execute(
            lambda: cron.new(
                command="/usr/local/bin/python /crawler/src/job/shopee/test.py"
            ).minute.every(1),
            quantity=1,
        )

        # Write cron job
        cron.write()

    def execute(self, command, quantity):
        for _ in range(quantity):
            command()


if __name__ == "__main__":
    Crawler()

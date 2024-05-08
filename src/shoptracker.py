from crontab import CronTab


class Crawler:
    def __init__(self):
        cron = CronTab(user="root")
        cron.remove_all()

        # get shop detail
        self.execute(
            lambda: cron.new(
                command="/usr/local/bin/python /crawler/src/job/shopee/shoptracker/get_shop_detail.py"
            ).setall(0, None, None, None, None),
            quantity=1,
        )

        # save product statistics
        self.execute(
            lambda: cron.new(
                command="/usr/local/bin/python /crawler/src/job/shopee/shoptracker/save_product_statistics.py"
            ).setall(0, None, None, None, None),
            quantity=1,
        )

        # save shop statistics
        self.execute(
            lambda: cron.new(
                command="/usr/local/bin/python /crawler/src/job/shopee/shoptracker/save_shop_statistics.py"
            ).setall(0, None, None, None, None),
            quantity=1,
        )

        # Sync filter table
        self.execute(
            lambda: cron.new(
                command="/usr/local/bin/python /crawler/src/job/shopee/shoptracker/sync_filter_table.py"
            ).setall(0, None, None, None, None),
            quantity=1,
        )

        # get product in shop
        self.execute(
            lambda: cron.new(
                command="/usr/local/bin/python /crawler/src/job/shopee/shoptracker/collect_product_in_shop.py"
            ).setall(0, None, None, None, None),
            quantity=1,
        )

        # test
        self.execute(
            lambda: cron.new(
                command="/usr/local/bin/python /crawler/src/job/shopee/shoptracker/test.py"
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

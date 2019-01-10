import asyncio
from pyppeteer import launch
import sqlite3

conn = sqlite3.connect('accounts.db')
c = conn.cursor()
c.execute('SELECT username FROM accounts')
column = c.fetchall()


async def main():
    total = len(column)
    count = 0
    for user in column:
        browser = await launch()
        page = await browser.newPage()
        await page.setViewport({'width': 960, 'height': 1200})
        await page.goto('https://instagram.com/%s' % user)
        await page.screenshot({'path': 'static/screenshots/%s.jpeg' % user})
        await browser.close()
        count += 1
        print("{0}/{1} - screenshot".format(count, total))


def run():
    asyncio.get_event_loop().run_until_complete(main())

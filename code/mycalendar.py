import calendar
from datetime import datetime


class MyCalendar(calendar.LocaleHTMLCalendar):
    """
    元々のカレンダークラスを継承してカスタマイズ

    Args:
        username (str): ユーザ名
        linked_date (dict): 予定
    """

    def __init__(self, username, linked_date: dict):
        calendar.LocaleHTMLCalendar.__init__(self, firstweekday=6, locale='ja-jp')

        # 何か予定がある場合はリンクする
        self.username = username
        # dict{'datetime': done}
        self.linked_date = linked_date

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        親クラスだと「年テーブルの中に月テーブル」になっているので月ごとのテーブルに枠をつけるよう上書き
        """

        v = []
        a = v.append

        a('<table class="table is-bordered">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, theyear, themonth))
            a('\n')
        a('</table><br>')
        a('\n')
        return ''.join(v)

    def formatweek(self, theweek, theyear, themonth):
        """
        週メソッドも上書き
        """

        s = ''.join(self.formatday(d, wd, theyear, themonth) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s

    def formatday(self, day, weekday, theyear, themonth):
        """
        オーバーライド
        引数で year と month を渡すようにした
        """

        if day == 0:
            return '<td style="background-color: #eee"> </td>'
        else:
            html = '<td class="text-center {highlight}"><a href="{url}" class="{text}">{day}</a></td>'
            text = 'blue'
            highlight = ''
            # 予定がある場合は強調させる
            date = datetime(year=theyear, month=themonth, day=day)
            date_str = date.strftime('%Y%m%d')
            if date_str in self.linked_date:
                # 終了した予定
                if self.linked_date[date_str]:
                    highlight = 'has-background-success'
                    text = 'has-text-white'
                # 過去の予定
                elif date < datetime.now():
                    highlight = 'has-background-grey'
                    text = 'has-text-white'
                # これからの予定
                else:
                    highlight = 'has-background-warning'

            # 今日の日付を強調
            if date_str == datetime.today().strftime("%Y%m%d"):
                highlight = 'is-capitalized has-background-primary'
                text = 'has-text-white has-text-weight-bold'

            # 変数展開
            return html.format(
                url='/todo/{}/{}/{}/{}'.format(self.username, theyear, themonth, day),
                text=text,
                day=day,
                highlight=highlight
            )

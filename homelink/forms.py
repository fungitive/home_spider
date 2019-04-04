from django import forms


DISTRICT_CHOICES = (
                    ('yuexiu', '越秀'),
                    ('tianhe', '天河'),
                    ('haizhu', '海珠'),
                    ('liwan', '荔湾'),
                    ('baiyun', '白云'),
                    ('panyu', '番禺'),
                    ('huangpu', '黄埔'),
                    ('nansha', '南沙'),
                    ('huadong', '花都'),
                    ('conghua', '从化'),
                    ('zengcheng', '增城')
            )
PRICE_CHOICES = (
                ('p1','100万以下'),
                ('p2', '100-200万'),
                ('p3', '200-250万'),
                ('p4', '250-300万'),
                ('p5', '300-400万'),
                ('p6', '400-500万'),
                ('p7', '500-800万'),
                ('p8', '800万以上'))
BEDROOM_CHOICES = (('l1', '一室'),('l2', '二室'), ('l3', '三室'))


class HouseChoiceForm(forms.Form):
    district = forms.CharField(label="区域", widget=forms.RadioSelect(choices=DISTRICT_CHOICES,attrs={'class': "list-inline"}))
    price = forms.CharField(label="价格",widget=forms.RadioSelect(choices=PRICE_CHOICES,attrs={'class': "list-inline"}))
    bedroom = forms.CharField(label="房型",widget=forms.RadioSelect(choices=BEDROOM_CHOICES,attrs={'class':"list-inline"}))

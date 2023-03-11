import pandas as pd
from game.models import Category


def load_categories(file):
    df = pd.read_excel(file, sheet_name='Sheet1')
    data = df.iloc[:, 0].tolist()
    for i in range(len(data)):
        cat = Category.objects.create(
            name=df.iloc[i, 2],
            code=df.iloc[i, 0]
        )
        cat.save()

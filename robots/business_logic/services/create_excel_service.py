from datetime import datetime, timedelta

import pandas as pd
from django.db.models import Count

from robots.models import Robot, RobotModel


def create_excel() -> None:
    """
    This function retrieves information about created robots
    from the database and writes it to an Excel file in the project's root folder.
    """
    end_of_week = datetime.now()
    start_of_week = end_of_week - timedelta(days=7)

    data = (
        Robot.objects.filter(created__gte=start_of_week, created__lte=end_of_week)
        .select_related('model')
        .values('model__name', 'version')
        .annotate(count=Count('id'))
    )

    models = RobotModel.objects.all()
    writer = pd.ExcelWriter('robot_week.xlsx', engine='xlsxwriter')

    for model in models:
        model_data = list(data.filter(model=model))

        if model_data:
            df = pd.DataFrame.from_records(model_data)
            df.columns = ['Model', 'Version', 'Quantity per week']
            df.to_excel(writer, sheet_name=model.name, index=False)
            worksheet = writer.sheets[model.name]
            worksheet.set_column('C:C', 20)

        else:
            df = pd.DataFrame.from_records([{model.name: 'This model was not created'}])
            df.to_excel(writer, sheet_name=model.name, index=False)
            worksheet = writer.sheets[model.name]
            worksheet.set_column('A:A', 25)

    writer.close()

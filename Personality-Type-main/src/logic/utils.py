import pandas as pd

def write_to_xlsx(dataframe, columns_names, rows_names, xlsx_name):
    writer = pd.ExcelWriter(xlsx_name, engine='xlsxwriter')
    dataframe.to_excel(writer, sheet_name='Sheet1')
    writer.save()

def write_report(report, estimator, cv, train_sizes, train_scores_mean, validation_scores_mean, model_score, delay):
    report.write('estimator: {0} \n'.format(str(estimator)))
    report.write('train_size: \n {0} \n\n'.format(train_sizes))
    report.write('Mean training scores\n\n {0} \n\n'.format(train_scores_mean))
    report.write('Mean validation scores\n\n {0} \n\n'.format(validation_scores_mean))

    report.write('Model score: {0} \n'.format(model_score))
    report.write('delay = {0}'.format(delay))
    report.close()
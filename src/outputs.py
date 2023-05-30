import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import BASE_DIR, DATETIME_FORMAT


def control_output(pre_results, cli_args):
    titles = {
        'p': ('Cтатус', 'Количество'),
        'l': ('Ссылка на документацию', 'Версия', 'Статус'),
        'w': ('Ссылка на статью', 'Заголовок', 'Редактор, Автор')
    }
    results = [titles[str(cli_args).split(',')[0][16]]]
    results = results + pre_results
    output = cli_args.output
    if output == 'pretty':
        pretty_output(results)
    elif output == 'file':
        print(str(cli_args).split(',')[0][16])
        file_output(results, cli_args)
    else:
        default_output(results)


def default_output(results):
    for row in results:
        print(*row)


def pretty_output(results):
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args):
    # тесты требуют наличие вычисления пути от базового католога :(
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='unix')
        writer.writerows(results)
    logging.info(f'Файл с результатами был сохранён: {file_path}')

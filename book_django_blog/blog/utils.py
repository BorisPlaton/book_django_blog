from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def get_paginator(query_set, page_num, objects_per_page=10):
    paginator_obj = Paginator(query_set, objects_per_page)
    try:
        paginator = paginator_obj.page(page_num)
    except PageNotAnInteger:
        # Если страница не является целым числом, возвращаем первую страницу.
        paginator = paginator_obj.page(1)
    except EmptyPage:
        # Если номер страницы больше, чем общее количество страниц, возвращаем последнюю.
        paginator = paginator_obj.page(paginator_obj.num_pages)

    return paginator

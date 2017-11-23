import logging

log = logging.getLogger(__name__)


def print_stats(stats, asc=False):
    log.info("Found the following jobs: ")
    num_classifications = sum(stats.values())
    stats_sorted = sort_stats(stats, asc)
    pattern = "{:<30} {:<4}"
    print(pattern.format('Job Name', 'Count'))
    print('------------------------------------')
    for job_name, count in stats_sorted:
        print(pattern.format(job_name, count))
    print('------------------------------------')
    print(pattern.format('Total', num_classifications))
    print(pattern.format('Jobs per vacancy', num_classifications/(len(stats_sorted) or 1)))
    print('====================================')


def sort_stats(stats, asc=True):
    return sorted(stats.items(), key=lambda k: k[1], reverse=not asc)
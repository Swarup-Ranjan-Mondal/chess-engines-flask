import multiprocessing

def calculate_workers():
    return multiprocessing.cpu_count()

workers = calculate_workers()
print(f"Number of Gunicorn workers: {workers}")
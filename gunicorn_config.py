import multiprocessing

def calculate_workers():
    return (multiprocessing.cpu_count() * 2) + 1

workers = calculate_workers()
print(f"Number of Gunicorn workers: {workers}")
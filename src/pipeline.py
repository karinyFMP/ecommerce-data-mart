from extract import extract
from transform import transform
from load import load

def run_pipeline():
    data = extract()
    transformed = transform(data)
    load(transformed)
    print("ETL executado com sucesso!")

if __name__ == "__main__":
    run_pipeline()
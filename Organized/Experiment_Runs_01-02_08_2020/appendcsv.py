import pandas as pd
import os

def main():
    cwd = os.getcwd().replace('\\', '/')

    directories = [
        "ada",
        "logreg",
        "mlp",
        "rf",
        "svm"
    ]

    for dir in directories:
        df = pd.DataFrame()
        os.chdir("{}/experimentresults/{}/".format(cwd, dir))
        csv_files = os.listdir()

        for csv in csv_files:
            data = pd.read_csv("{}/experimentresults/{}/{}".format(cwd, dir, csv))
            data["augmentation"] = csv
            df = df.append(data)
        
        df.to_csv("{}/experimentresults/{}/all_experiments.csv".format(cwd, dir), index = False)
        df.to_excel("{}/experimentresults/{}/all_experiments.xlsx".format(cwd, dir), index = False)
            

if __name__ == "__main__":
    main()
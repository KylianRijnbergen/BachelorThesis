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
        os.chdir("{}/{}/".format(cwd, dir))
        
        
        
        csv_files = os.listdir()

        print(csv_files)
        AUGMENTATION = ["1.01", "1.015", "1.02", "1.025", "1.03", "1.035", "1.04", "1.045", "1.05"]
        
        data = pd.DataFrame()
        for augmentation in AUGMENTATION:
            intermediate_data = pd.DataFrame()
            for seed in range(0, 10):
                if "seed{}_augmentation{}.csv".format(seed, augmentation) in csv_files:
                    df = pd.read_csv("{}/{}/seed{}_augmentation{}.csv".format(cwd, dir, seed, augmentation))
                    df["seed"] = seed
                    df["augmentation"] = augmentation
                    intermediate_data = pd.concat([intermediate_data, df], axis = 1)
            data = pd.concat([data, intermediate_data], axis = 0)    
        data.to_excel("{}/{}/all_experiments.xlsx".format(cwd, dir), index = False)
if __name__ == "__main__":
    main()
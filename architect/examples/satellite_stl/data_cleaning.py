import pandas as pd


def clean_counterexample_guided():
    # Create a dataframe to aggregate the results
    results_df = pd.DataFrame()
    for seed in range(50):
        save_dir = "logs/satellite_stl/safety_and_goal_only/comparison"
        filename = f"{save_dir}/counterexample_guided_{seed}.csv"
        df = pd.read_csv(filename)

        # Add one to rounds to account for zero-indexing
        rounds_mask = df.measurement == "Optimization rounds"
        df.loc[rounds_mask, "value"] = df[rounds_mask].value + 1

        results_df = results_df.append(df, ignore_index=True)

    # Save the new dataframe
    save_dir = "logs/satellite_stl/safety_and_goal_only/comparison"
    filename = f"{save_dir}/combined_counterexample_guided.csv"
    results_df.to_csv(filename, index=False)


def clean_single_example():
    # Create a dataframe to aggregate the results
    results_df = pd.DataFrame()
    for seed in range(50):
        save_dir = "logs/satellite_stl/safety_and_goal_only/comparison"
        filename = f"{save_dir}/single_example_{seed}.csv"
        df = pd.read_csv(filename)

        # Add missing rows (this optimization ran for 1 round with 1 exogenous sample)
        df = df.append(
            {"seed": seed, "measurement": "Optimization rounds", "value": 1},
            ignore_index=True,
        )
        df = df.append(
            {"seed": seed, "measurement": "Final population size", "value": 1},
            ignore_index=True,
        )
        results_df = results_df.append(df, ignore_index=True)

    # Save the new dataframe
    save_dir = "logs/satellite_stl/safety_and_goal_only/comparison"
    filename = f"{save_dir}/combined_single_example.csv"
    results_df.to_csv(filename, index=False)


def clean_random_batch_1():
    # Create a dataframe to aggregate the results
    results_df = pd.DataFrame()
    for seed in range(50):
        save_dir = "logs/satellite_stl/safety_and_goal_only/comparison"
        filename = f"{save_dir}/random_batch_1_{seed}.csv"
        df = pd.read_csv(filename)

        results_df = results_df.append(df, ignore_index=True)

    # Save the new dataframe
    save_dir = "logs/satellite_stl/safety_and_goal_only/comparison"
    filename = f"{save_dir}/combined_random_batch_1.csv"
    results_df.to_csv(filename, index=False)


def clean_random_batch_32():
    # Create a dataframe to aggregate the results
    results_df = pd.DataFrame()
    for seed in range(50):
        save_dir = "logs/satellite_stl/safety_and_goal_only/comparison"
        filename = f"{save_dir}/random_batch_32_{seed}.csv"
        df = pd.read_csv(filename)

        # Add missing rows (this optimization ran for 1 round with 32 exogenous samples)
        df = df.append(
            {"seed": seed, "measurement": "Optimization rounds", "value": 1},
            ignore_index=True,
        )
        df = df.append(
            {"seed": seed, "measurement": "Final population size", "value": 32},
            ignore_index=True,
        )
        results_df = results_df.append(df, ignore_index=True)

    # Save the new dataframe
    save_dir = "logs/satellite_stl/safety_and_goal_only/comparison"
    filename = f"{save_dir}/combined_random_batch_32.csv"
    results_df.to_csv(filename, index=False)


def clean_random_batch_64():
    # Create a dataframe to aggregate the results
    results_df = pd.DataFrame()
    for seed in range(50):
        save_dir = "logs/satellite_stl/safety_and_goal_only/comparison"
        filename = f"{save_dir}/random_batch_64_{seed}.csv"
        df = pd.read_csv(filename)

        # Add missing rows (this optimization ran for 1 round with 64 exogenous samples)
        # Add one to rounds to account for zero-indexing
        rounds_mask = df.measurement == "Optimization rounds"
        df.loc[rounds_mask, "value"] = df[rounds_mask].value + 1

        results_df = results_df.append(df, ignore_index=True)

    # Save the new dataframe
    save_dir = "logs/satellite_stl/safety_and_goal_only/comparison"
    filename = f"{save_dir}/combined_random_batch_64.csv"
    results_df.to_csv(filename, index=False)


if __name__ == "__main__":
    clean_counterexample_guided()
    clean_single_example()
    clean_random_batch_1()
    clean_random_batch_32()
    clean_random_batch_64()
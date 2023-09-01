import pandas as pd
import re
import os

# 读取addresses.csv文件
def load_addresses_from_csv(csv_path):
    addresses_df = pd.read_csv(csv_path)
    return set(addresses_df['Address'])

# 定义一个函数来从txt文件中提取地址
def extract_addresses_from_txt(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        return set(re.findall(r'0x[a-fA-F0-9]{40}', content))

def main():
    # Load addresses from CSV
    csv_addresses = load_addresses_from_csv("C:/Users/ylhk/Desktop/PYTHON/huawei/all_addresses_500.csv")

    # List all txt file paths
    txt_files = [
        r"D:\sybil\text\arbitrum_txlist_connected_groups.txt",
        r"D:\sybil\text\avax_txlist_connected_groups.txt",
        r"D:\sybil\text\bsc_txlist_connected_groups.txt",
        r"D:\sybil\text\gnosis_tokentx_connected_groups.txt",
        r"D:\sybil\text\gnosis_txlist_connected_groups.txt",
        r"D:\sybil\text\moonbeam_tokentx_connected_groups.txt",
        r"D:\sybil\text\moonbeam_txlist_connected_groups.txt",
        r"D:\sybil\text\moonriver_txlist_connected_groups.txt",
        r"D:\sybil\text\optimism_txlist_connected_groups.txt",
    ]

    # Iterate through txt files and find addresses not in CSV
    non_matching_results = {}
    all_txt_addresses = set()
    for file_path in txt_files:
        txt_addresses = extract_addresses_from_txt(file_path)
        all_txt_addresses.update(txt_addresses)
        non_matching_addresses = txt_addresses.difference(csv_addresses)
        non_matching_results[os.path.basename(file_path)] = len(non_matching_addresses)

    # Print the results for each txt file
    for file_name, count in non_matching_results.items():
        print(f"{file_name}: {count} addresses not found in the CSV")

    # Check for addresses in all txt files combined that are not in the CSV
    combined_non_matching_addresses = all_txt_addresses.difference(csv_addresses)
    print(f"Total addresses in all txt files not found in the CSV: {len(combined_non_matching_addresses)}")


# Run the main function
if __name__ == "__main__":
    main()
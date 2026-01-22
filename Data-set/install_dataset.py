import kagglehub

# Download latest version
path = kagglehub.dataset_download("pysharma/delivery-address-dataset")

print("Path to dataset files:", path)

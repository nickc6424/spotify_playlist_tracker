import archive, extract, load


def main():
    """Main orchestration method for ETL process."""
    s3_bucket_name = "playlist-extracts"
    data_extract = extract.get_songs()
    archive.main(s3_bucket_name, data_extract)
    load.main(data_extract)


if __name__ == "__main__":
    main()

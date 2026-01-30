from tasks import execute_crawler

if __name__ == "__main__":
    test_url = "https://example.com"

    result = execute_crawler.delay(test_url)

    print("Task submitted successfully!")
    print("Task ID:", result.id)

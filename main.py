from scraper.scraper import scrape_website
from db.db_connection import save_dynamic_user_inputs


def main():
    url = input("Enter the URL to scrape and mimic: ")
    template_folder = scrape_website(url)
    print(f"Website template saved in {template_folder}")

    # Example dynamic inputs for demonstration (these would normally come from a form on the template)
    inputs = {
        "username": "example_user",
        "password": "example_password"
    }

    # Save dynamic inputs to the database
    save_dynamic_user_inputs(url, inputs)
    print(f"User inputs for {url} have been saved to the database.")


if __name__ == "__main__":
    main()

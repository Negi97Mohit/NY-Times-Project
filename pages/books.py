from pynytimes import NYTAPI
import streamlit as st


def main():

    api_key = "Frvpakmi7RzBNtGrwxKbcGNxwqBNvVEI"
    nyt = NYTAPI(api_key, parse_dates=True)

# Get fiction best sellers list
    books = nyt.best_sellers_list()
    st.write(books)


if __name__ == "__main__":
    main()

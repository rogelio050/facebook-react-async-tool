# Facebook React Async Tool

This tool allows you to send reactions to a Facebook post using multiple access tokens concurrently.

## Usage

1. Install requirements:
    ```
    pip install -r requirements.txt
    ```
2. Prepare `tokens.txt` with one Facebook access token per line.
3. Run:
    ```
    python facebook_react_async.py <post_id> <reaction_type> <tokens.txt>
    ```

#!/usr/bin/env python3
"""Upload a local folder to Mail.ru Cloud."""
import argparse
import os

import cloud_mail_api


def upload_directory(local_dir: str, cloud_dir: str, cm: cloud_mail_api.CloudMail) -> None:
    """Recursively upload *local_dir* to *cloud_dir* in user's storage."""
    for root, dirs, files in os.walk(local_dir):
        rel_path = os.path.relpath(root, local_dir)
        target_cloud_dir = cloud_dir
        if rel_path != ".":
            target_cloud_dir = os.path.join(cloud_dir, rel_path).replace("\\", "/")
        cm.api.folder.add(target_cloud_dir)
        for name in files:
            local_file = os.path.join(root, name)
            cloud_file = os.path.join(target_cloud_dir, name).replace("\\", "/")
            cm.api.file.add(local_file, cloud_file)


def main() -> None:
    parser = argparse.ArgumentParser(description="Upload folder to Mail.ru Cloud")
    parser.add_argument("login", help="Account login (email)")
    parser.add_argument("password", help="Account password")
    parser.add_argument("local_folder", help="Local folder to upload")
    parser.add_argument("cloud_folder", help="Destination folder in cloud")
    parser.add_argument(
        "--cookies", help="Optional path to cookies file to reuse session")

    args = parser.parse_args()

    cm = cloud_mail_api.CloudMail(args.login, args.password)

    if args.cookies and os.path.exists(args.cookies):
        cm.load_cookies_from_file(args.cookies)
        if not cm.is_cookies_valid():
            cm.auth()
    else:
        cm.auth()

    upload_directory(args.local_folder, args.cloud_folder, cm)

    if args.cookies:
        cm.save_cookies_to_file(args.cookies)


if __name__ == "__main__":
    main()

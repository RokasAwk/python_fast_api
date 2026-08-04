"""手動簽發一組測試用 JWT access token，貼到 Swagger UI 的 Authorize 或 Authorization header 使用。

用法：python generate_token.py [--sub service] [--minutes 60]
"""
import argparse
from datetime import timedelta

from auth import create_access_token


def main():
    parser = argparse.ArgumentParser(description="簽發測試用 JWT access token")
    parser.add_argument("--sub", default="service", help="token 的主體識別，預設 service")
    parser.add_argument("--minutes", type=int, default=None, help="有效時間（分鐘），預設使用 .env 的 JWT_EXPIRE_MINUTES")
    args = parser.parse_args()

    expires_delta = timedelta(minutes=args.minutes) if args.minutes else None
    token = create_access_token({"sub": args.sub}, expires_delta=expires_delta)
    print(token)


if __name__ == "__main__":
    main()

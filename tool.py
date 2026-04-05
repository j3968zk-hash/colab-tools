import requests
import os
import time

BASE_URL = "https://cloudily.org"

# 👉 ĐỔI PATH Ở ĐÂY (folder chứng khoán)
FOLDER_PATH = "/EBook/Ebook 3/Chứng khoán"

SAVE_PATH = "/content/drive/MyDrive/ebooks_chung_khoan"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://cloudily.org/"
}

def get_file_list(path):
    url = BASE_URL + "/api/fs/list"
    res = requests.post(url, json={"path": path}, headers=headers)
    return res.json()["data"]["content"]

def get_download_link(path):
    url = BASE_URL + "/api/fs/get"
    res = requests.post(url, json={"path": path}, headers=headers)
    return res.json()["data"]["raw_url"]

def download_file(url, filename):
    r = requests.get(url, headers=headers)
    with open(filename, "wb") as f:
        f.write(r.content)

def main():
    os.makedirs(SAVE_PATH, exist_ok=True)

    files = get_file_list(FOLDER_PATH)

    total = 0
    success = 0
    fail = 0
    skipped = 0

    for f in files:
        if not f["is_dir"]:
            total += 1

            full_path = FOLDER_PATH + "/" + f["name"]
            save_file = os.path.join(SAVE_PATH, f["name"])

            # 👉 Nếu file đã tồn tại thì bỏ qua
            if os.path.exists(save_file):
                print("⏩ Bỏ qua:", f["name"])
                skipped += 1
                continue

            print("Đang tải:", f["name"])

            try:
                link = get_download_link(full_path)
                download_file(link, save_file)
                print("✔ Done:", f["name"])
                success += 1
                time.sleep(1)
            except Exception as e:
                print("❌ Fail:", f["name"], e)
                fail += 1

    print("\n==== KẾT QUẢ ====")
    print("Tổng file:", total)
    print("Tải mới:", success)
    print("Bỏ qua:", skipped)
    print("Fail:", fail)

    # 👉 CHECK 100%
    if fail == 0 and (success + skipped) == total:
        print("✅ DONE 100%")
    else:
        print("❌ CHƯA ĐỦ FILE")

if __name__ == "__main__":
    main()

import requests
import json
import base64
from config import REVE_API_KEY


class ReveAPI:

    def __init__(self, api_key):
        # URL dasar dan header otorisasi yang diperlukan oleh Reve API
        self.URL = "https://api.reve.com/v1/"
        self.HEADERS = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def generate_image(
        self,
        prompt,
        aspect_ratio="16:9",
        version="latest",
        save_json="reve_output.json",
        save_image="reve_image.png"
    ):
        # Data permintaan yang berisi parameter pembuatan gambar
        payload = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "version": version
        }

        # Mengirim permintaan ke Reve API
        response = requests.post(
            self.URL + "image/create",
            headers=self.HEADERS,
            json=payload
        )

        # Memicu error jika status HTTP tidak OK
        response.raise_for_status()

        # Respons JSON yang sudah diparsing dari API
        result = response.json()

        # Simpan respons JSON jika diperlukan
        if save_json:
            with open(save_json, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=4, ensure_ascii=False)

        print(f"ID Permintaan: {result.get('request_id')}")
        print(f"Kredit digunakan: {result.get('credits_used')}")
        print(f"Kredit tersisa: {result.get('credits_remaining')}")

        # Jika API mengembalikan gambar — dekode dan simpan
        if result.get("image") and save_image:
            self.save_image(result["image"], save_image)

        # API menandai pelanggaran kebijakan konten dengan flag ini
        if result.get("content_violation"):
            print("Peringatan: Terjadi pelanggaran kebijakan konten")
        else:
            print("Gambar berhasil dibuat")

        return result

    def save_image(self, base64_string, file_path):
        # Mendekode string base64 dan menyimpannya sebagai file
        decoded_data = base64.b64decode(base64_string)
        with open(file_path, "wb") as img_file:
            img_file.write(decoded_data)
        print(f"Gambar disimpan ke {file_path}")


# Instance utama untuk klien API (akan digunakan oleh bot nanti)
reve_api = ReveAPI(REVE_API_KEY)


if __name__ == "__main__":
    # Contoh pengujian (prompt dalam Bahasa Inggris atau bisa diganti)
    result = reve_api.generate_image(
        "Seekor kucing berbulu lembut memakai kacamata",
        save_json="reve_output.json",
        save_image="generated_image.png"
    )
    print(result)
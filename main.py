import requests
import json
import base64

REVE_API_KEY = "papi.9f8abb78-6ef7-4d03-9022-9edac64aca74.YrfwCuZJnbyH0BMFCDMJHGII-Zx4wu3p"

headers = {
    "Authorization": f"Bearer {REVE_API_KEY}", 
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def generate_reve_image(
    prompt,
    aspect_ratio="16:9",
    version="latest",
    save_json="reve_output.json",
    save_image="reve_image.png"
):
    payload = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "version": version
    }

    try:
        response = requests.post(
            "https://api.reve.com/v1/image/create",
            headers=headers,
            json=payload
        )
        response.raise_for_status()

        result = response.json()

        # Simpan respons JSON
        if save_json:
            with open(save_json, "w") as f:
                json.dump(result, f, indent=4)

        print(f"ID Permintaan: {result.get('request_id')}")
        print(f"Credit terpakai: {result.get('credits_used')}")
        print(f"Credit tersisa: {result.get('credits_remaining')}")

        # Konversi gambar base64 menjadi PNG
        if result.get("image"):
            try:
                image_data = base64.b64decode(result["image"])

                if save_image:
                    with open(save_image, "wb") as img_file:
                        img_file.write(image_data)

                print(f"Gambar disimpan ke {save_image}")
            except Exception as e:
                print(f"Gagal mendekode gambar base64: {e}")

        if result.get("content_violation"):
            print("Peringatan: Terdeteksi pelanggaran kebijakan konten")
        else:
            print("Gambar berhasil dihasilkan")

        return result

    except requests.exceptions.RequestException as e:
        print(f"Permintaan gagal: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Gagal membaca respon: {e}")
        return None


# Contoh pemanggilan fungsi
# result = generate_reve_image("Gunung yang tenang dengan seekor beruang")
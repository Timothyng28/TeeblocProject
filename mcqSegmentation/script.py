import requests
import os

urls = [
"https://www.testpapersfree.com/pdfs/P5_Science_2023_WA1_Raffles.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_WA1_Nanyang.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_WA1_Redswastika.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_WA1_ACS.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_WA1_Marisstella.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_WA1_Mahabodhi.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_WA1_henrypark.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_WA1_Nanhua.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_WA1_CHIJ.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_WA2_Nanyang.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_WA2_Rosyth.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_WA2_Taonan.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_WA2_Redswastika.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_WA2_ACS.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_WA2_Aitong.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_WA2_MarisStella.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_WA2_Mahabodhi.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_WA2_Raffles.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_WA2_Henrypark.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_WA2_nanhua.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_SA2_Raffles.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_SA2_Nanyang.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_SA2_Rosyth.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_SA2_Taonan.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_SA2_Redswastika.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_SA2_Aitong.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_SA2_ACS.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_SA2_Marisstella.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_SA2_Mahabothi.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_SA2_Henrypark.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_SA2_Nanhua.pdf",
"https://www.testpapersfree.com/pdfs/P5_Science_2023_SA2_CHIJ.pdf",
"https://www.testpapersfree.com/pdfs/P6_Maths_2023_WA1_CHIJ.pdf",
"https://www.testpapersfree.com/pdfs/P6_Maths_2023_WA1_Nanhua.pdf",
"https://www.testpapersfree.com/pdfs/P6_Maths_2023_WA1_Nanyang.pdf",
"https://www.testpapersfree.com/pdfs/P6_Maths_2023_WA1_Raffles.pdf",
"https://www.testpapersfree.com/pdfs/P6_Maths_2023_WA1_Rosyth.pdf",
"https://www.testpapersfree.com/pdfs/P6_Maths_2023_WA1_Singaporechinesegirls.pdf",
"https://www.testpapersfree.com/pdfs/P6_Maths_2023_WA2_ACS_Junior.pdf",
"https://www.testpapersfree.com/pdfs/P6_Maths_2023_WA2_CHIJ.pdf",
"https://www.testpapersfree.com/pdfs/P6_Maths_2023_WA2_Nanhua.pdf",
"https://www.testpapersfree.com/pdfs/P6_Maths_2023_WA2_Nanyang.pdf",
"https://www.testpapersfree.com/pdfs/P6_Maths_2023_WA2_RafflesGirls.pdf",
"https://www.testpapersfree.com/pdfs/P6_Maths_2023_WA2_Rosyth.pdf ",
"https://www.testpapersfree.com/pdfs/P6_Maths_2023_WA2_Taonan.pdf",
"https://www.testpapersfree.com/pdfs/P6_Maths_2023_SA2_ACS_Junior.pdf",
"https://www.testpapersfree.com/pdfs/P6_Maths_2023_SA2_ACS_Primary.pdf",
"https://www.testpapersfree.com/pdfs/P6_Maths_2023_SA2_AiTong.pdf",
"https://www.testpapersfree.com/pdfs/P6_Maths_2023_SA2_Catholichigh.pdf",
"https://www.testpapersfree.com/pdfs/P6_Maths_2023_SA2_CHIJ.pdf",
"https://www.testpapersfree.com/pdfs/P6_Maths_2023_SA2_Marisstella.pdf",
"https://www.testpapersfree.com/pdfs/P6_Maths_2023_SA2_MGS.pdf",
"https://www.testpapersfree.com/pdfs/P6_Maths_2023_SA2_Nanhua.pdf",
"https://www.testpapersfree.com/pdfs/P6_Maths_2023_SA2_Nanyang.pdf",
"https://www.testpapersfree.com/pdfs/P6_Maths_2023_SA2_Peichun.pdf",
"https://www.testpapersfree.com/pdfs/P6_Maths_2023_SA2_Peihwa.pdf",
"https://www.testpapersfree.com/pdfs/P6_Maths_2023_SA2_Rafflesgirls.pdf",
"https://www.testpapersfree.com/pdfs/P6_Maths_2023_SA2_Redswastika.pdf",
"https://www.testpapersfree.com/pdfs/P6_Maths_2023_SA2_Rosyth.pdf",
"https://www.testpapersfree.com/pdfs/P6_Maths_2023_SA2_SCGS.pdf",
"https://www.testpapersfree.com/pdfs/P6_Maths_2023_SA2_Temasek.pdf",
"https://www.testpapersfree.com/pdfs/P6_Maths_2023_SA2_Taonan.pdf",

]

save_directory = "/Users/timothy/projects/Teebloc/whitespace/pdf"

# Ensure the save directory exists
os.makedirs(save_directory, exist_ok=True)

for url in urls:
    url = url.strip()  # Remove trailing spaces
    filename = url.split("/")[-1]
    file_path = os.path.join(save_directory, filename)

    try:
        response = requests.get(url, timeout=10)  # Timeout to prevent long waits
        if response.status_code == 200:
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download {filename}: HTTP {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {filename}: {e}")

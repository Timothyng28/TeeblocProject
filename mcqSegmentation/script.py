import requests
import os

urls = [
    "https://www.testpapersfree.com/pdfs/P3_Science_2023_WA1_Raffles.pdf",
"https://www.testpapersfree.com/pdfs/P3_Science_2023_WA1_Nanhua.pdf",
"https://www.testpapersfree.com/pdfs/P3_Science_2023_WA1_Taonan.pdf",
"https://www.testpapersfree.com/pdfs/P3_Science_2023_WA1_Henrypark.pdf",
"https://www.testpapersfree.com/pdfs/P3_Science_2023_WA1_MGS.pdf",
"https://www.testpapersfree.com/pdfs/P3_Science_2023_WA1_Mahabodhi.pdf",
"https://www.testpapersfree.com/pdfs/P3_Science_2023_WA1_Nanyang.pdf",
"https://www.testpapersfree.com/pdfs/P3_Science_2023_WA1_Rosyth.pdf",
"https://www.testpapersfree.com/pdfs/P3_Science_2023_WA1_Catholichigh.pdf",
"https://www.testpapersfree.com/pdfs/P3_Science_2023_WA1_Redswastika.pdf",
"https://www.testpapersfree.com/pdfs/P3_Science_2023_WA1_Peichun.pdf",
"https://www.testpapersfree.com/pdfs/P3_Science_2023_SA2_Raffles.pdf",
"https://www.testpapersfree.com/pdfs/P3_Science_2023_SA2_Nanhua.pdf",
"https://www.testpapersfree.com/pdfs/P3_Science_2023_SA2_Taonan.pdf",
"https://www.testpapersfree.com/pdfs/P3_Science_2023_SA2_SCGS.pdf",
"https://www.testpapersfree.com/pdfs/P3_Science_2023_SA2_Henrypark.pdf",
"https://www.testpapersfree.com/pdfs/P3_Science_2023_SA2_MGS.pdf",
"https://www.testpapersfree.com/pdfs/P3_Science_2023_SA2_ACS.pdf",
"https://www.testpapersfree.com/pdfs/P3_Science_2023_SA2_Mahabodhi.pdf",
"https://www.testpapersfree.com/pdfs/P3_Science_2023_SA2_CHIJ.pdf",
"https://www.testpapersfree.com/pdfs/P3_Science_2023_SA2_Rosyth.pdf",
"https://www.testpapersfree.com/pdfs/P3_Science_2023_SA2_Peihwa.pdf",
"https://www.testpapersfree.com/pdfs/P3_Science_2023_SA2_Redswastika.pdf",
"https://www.testpapersfree.com/pdfs/P3_Science_2023_SA2_Catholichigh.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_WA1_Nanhua.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_WA1_Taonan.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_WA1_Henrypark.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_WA1_ACSj.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_WA1_Redswastika.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_WA1_Catholichigh.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_WA1_MGSpl.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_WA1_Methodistgirls.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_WA1_Sthildas.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_WA1_PeihwaGirls.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_WA2_Raffles Girls.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_WA2_Nanyang.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_WA2_Nanhua.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_WA2_Rosyth.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_WA3_Nanhua.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_WA2_Redswastika.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_WA2_Mahabodhi.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_WA2_Henrypark.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_SA2_Nanyang_.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_SA2_Nanhua.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_SA2_Rosyth.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_SA2_Taonan.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_SA2_CHIJ.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_SA2_Henrypark.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_SA2_ACS.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_SA2_Redswastika.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_SA2_Mahabodhi.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_SA2_Catholichigh.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_SA2_MGSpl.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_SA2_MGS.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_SA2_Sthildas.pdf",
"https://www.testpapersfree.com/pdfs/P4_Science_2023_SA2_Peihwa.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_SA1_Raffles.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_WA1_Nanyang.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_WA1_Taonan.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_WA1_Henrypark.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_WA1_ACSJunior.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_WA1_Redswastika.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_WA1_Mahabodhi.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_WA1_Catholichigh.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_WA1_Methodistpl.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_WA1_Peihwa.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_WA1_Sthildas.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_WA1_Nanhua.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_WA2_Rosyth.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_WA2_Henrypark.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_WA2_ACSjunior.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_WA2_Redswastika.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_WA2_Mahabodhi.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_WA2_Catholichigh.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_WA2_Methodistpl.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_WA2_Methodistprimary.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_WA2_Pweihwa.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_WA2_Peihwa.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_SA2_Nanyang.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_SA2_Nanhua.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_SA2_Rosyth.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_SA2_Taonan.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_SA2_CHIJ.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_SA2_Henrypark.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_SA2_ACS.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_SA2_Redswastika.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_SA2_Mahabodhi.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_SA2_Catholichigh.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_SA2_MGSpl.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_SA2_MGS.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_SA2_SCGS.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_SA2_Peichun.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_SA2_Peihwa.pdf",
"https://www.testpapersfree.com/pdfs/P4_Maths_2023_SA2_Sthildas.pdf",

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

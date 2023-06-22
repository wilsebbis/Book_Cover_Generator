import openai
import confidential
import requests
from PIL import Image

openai.api_key = confidential.openai_api_key

def func(num, desc):
    description = desc
    
    blank_large = Image.new('RGBA', (1024, 1024), (255, 0, 0, 0))

    blank_large.save(confidential.Blank_Large, 'PNG')

    while True:
        try:
            response = openai.Image.create_edit(
                image=open(confidential.Blank_Large, "rb"),
                mask=open(confidential.Blank_Large, "rb"),
                prompt=description,
                n=1,
                size="1024x1024"
            )
        except openai.error.RateLimitError:
            print("Rate Limit Error")
            continue
        except openai.error.APIError:
            print("API Error: probably bad gateway")
            continue
        except openai.error.ServiceUnavailableError:
                print("openai.error.ServiceUnavailableError")
                continue
        break

    image_url = response['data'][0]['url']

    img_data = requests.get(image_url).content

    with open(confidential.Original_Image, 'bw') as handler:
            handler.write(img_data)

    original = Image.open(confidential.Original_Image)

    original_cropped_top = original.crop((0, 324, 1024, 1024))

    blank_large.paste(original_cropped_top, (0, 0))

    blank_large.save(confidential.Blank_Bottom, 'PNG')

    while True:
        try:
            response = openai.Image.create_edit(
                image=open(confidential.Blank_Bottom, "rb"),
                mask=open(confidential.Blank_Bottom, "rb"),
                prompt=description,
                n=1,
                size="1024x1024"
            )
        except openai.error.RateLimitError:
            print("Rate Limit Error")
            continue
        except openai.error.APIError:
            print("API Error: probably bad gateway")
            continue
        except openai.error.ServiceUnavailableError:
                print("openai.error.ServiceUnavailableError")
                continue
        break

    image_url = response['data'][0]['url']

    img_data = requests.get(image_url).content

    with open(confidential.Complete_Bottom, 'bw') as handler:
        handler.write(img_data)

    original_with_top = original.crop((0, 0, 1024, 724))

    new_blank_large = Image.new('RGBA', (1024, 1024), (255, 0, 0, 0))

    new_blank_large.paste(original_with_top, (0, 324))

    new_blank_large.save(confidential.Blank_Top, 'PNG')

    while True:
        try:
            response = openai.Image.create_edit(
                image=open(confidential.Blank_Top, "rb"),
                mask=open(confidential.Blank_Top, "rb"),
                prompt=description,
                n=1,
                size="1024x1024"
            )
        except openai.error.RateLimitError:
            print("Rate Limit Error")
            continue
        except openai.error.APIError:
            print("API Error: probably bad gateway")
            continue
        except openai.error.ServiceUnavailableError:
                print("openai.error.ServiceUnavailableError")
                continue
        break

    image_url = response['data'][0]['url']

    img_data = requests.get(image_url).content

    with open(confidential.Complete_Top, 'bw') as handler:
            handler.write(img_data)

    toptop = Image.open(confidential.Complete_Top)

    top3 = toptop.crop((0, 0, 1024, 324))

    top3.save(confidential.Cropped_Top, 'PNG')

    bottombottom = Image.open(confidential.Complete_Bottom)

    bottom2 = bottombottom.crop((0, 724, 1024, 1024))

    bottom2.save(confidential.Cropped_Bottom, 'PNG')

    blank_even_larger = Image.new('RGBA', (1024, 1624), (255, 0, 0, 0))

    blank_even_larger.paste(top3, (0, 0))

    blank_even_larger.paste(original, (0, 324))

    blank_even_larger.paste(bottom2, (0, 1348))

    blank_even_larger = blank_even_larger.crop((0, 0, 1000, 1600))

    blank_even_larger.save(confidential.Final_Image + str(num) + ".png", 'PNG')

def main():
    description = "An epic fantasy painting montage of a vase with roses on it, a laminated wooden baseball bat, an old rusty treasure chest, and a grand pirate ship with tattered sails."
    for i in range(10):
        func(i, description)
        
main()
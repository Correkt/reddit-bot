import praw
import requests
import time
import os

bot = praw.Reddit(
    user_agent="fgfljfldkhgaehgawuieguh",
    client_id="zoJdF7wQ0JlEYvN4Xym0cw",
    client_secret=os.environ["REDDIT_BOT_CLIENT_SECRET"],
    username="CorrektBot",
    password=os.environ["REDDIT_BOT_PASSWORD"]
)

IMAGE_ENDPOINT = "https://correkt.ai/image"
API_KEY = os.environ["CORREKT_API_KEY"]
# subreddit = bot.subreddit('all')
# comments = subreddit.stream.comments()

# while True:
#     for comment in comments:
#         text = comment.body
#         if 'u/CorrektOfficial' in text.lower():
#             comment.reply('hello')


def getImages(submission):

    print(submission)

    imageUrl = submission.url
    print(imageUrl)

    if "gallery" in imageUrl:
        ids = [i['media_id'] for i in submission.gallery_data['items']]
        gallery = []
        for id in ids:
            link = submission.media_metadata[id]['p'][0]['u']
            link = link.split("?")[0].replace("preview", "i")
            gallery.append(link)
        return gallery
    else:
        if (imageUrl[-1] == "/"):
            imageUrl = imageUrl[:-1]
        suffix = imageUrl.split('.')[-1].split('?')[0]; 
        types = ["png", "jpg", "jpeg"]
        if suffix in types:
            return [imageUrl]
    
    # isImgur = imageUrl.includes('imgur.com');
    # if "imgur.com" in imageUrl:
        # // cases:
        # // http://i.imgur.com/f7VXJQF - single image
        # // http://imgur.com/mLkJuXP/ - single image, different url formatting
        # // https://imgur.com/a/9RKPOtA - album, single image
        # // http://imgur.com/a/liD3a - album, multiple images
        # // http://imgur.com/gallery/HFoOCeg gallery, single image
        # // https://imgur.com/gallery/5l71D gallery, multiple images (album)

    #     // An alternative method for imgur gifs/videos is to use "_d.jpg?maxwidth=520&shape=thumb&fidelity=high", however to keep them consistent with
    #     // giphy etc, magic eye will use the reddit thumbnail

    #     let imgurHash = imageUrl.split('/')[imageUrl.split('/').length - 1]; // http://imgur.com/S1dZBPm.weird?horrible=true
    #     imgurHash = imgurHash.split('.')[0];
    #     imgurHash = imgurHash.split('?')[0];
    #     const imgurClientId = '1317612995a5ccf';
    #     const options = {
    #         headers: {
    #             Authorization: `Client-ID ${imgurClientId}`,
    #         },
    #     };

    #     const isAlbum = imageUrl.includes('imgur.com/a/');
    #     const isGallery = imageUrl.includes('imgur.com/gallery/');
    #     if (isGallery || isAlbum) {
    #         const albumFetchUrl = isGallery ? `https://api.imgur.com/3/gallery/album/${imgurHash}/images` : `https://api.imgur.com/3/album/${imgurHash}/images`;
    #         const albumResult = await fetch(albumFetchUrl, options); // gallery album
    #         const albumData = await albumResult.json();
    #         if (albumData.success && albumData.data && albumData.data[0]) {
    #             // gallery with multiple images
    #             if (albumData.data[0].animated) {
    #                 return animatedMediaUrl(thumbnail);
    #             }
    #             return { imageUrl: albumData.data[0].link, submissionType: 'image' };
    #         } else if (albumData.success && albumData.data && albumData.data.images && albumData.data.images[0]) {
    #             // Not sure if case is valid - log for testing
    #             log.warn('Abnormal gallery url for processing: ', imageUrl);
    #             return null;
    #         } else {
    #             // gallery but only one image
    #             const albumImageFetchUrl = `https://api.imgur.com/3/gallery/image/${imgurHash}`;
    #             const imageResult = await fetch(albumImageFetchUrl, options);
    #             const albumImage = await imageResult.json();
    #             if (albumImage.success && albumImage.data) {
    #                 if (albumImage.data.animated) {
    #                     return animatedMediaUrl(thumbnail);
    #                 }

    #                 return { imageUrl: albumImage.data.link, submissionType: 'image' };
    #             } else {
    #                 log.warn('Tried to parse this imgur album/gallery url but failed: ', imageUrl);
    #                 return null;
    #             }
    #         }
    #     } else {
    #         // single image
    #         const result = await fetch(`https://api.imgur.com/3/image/${imgurHash}`, options);
    #         const singleImage = await result.json();
    #         if (singleImage.success && singleImage.data) {
    #             if (singleImage.data.animated) {
    #                 return animatedMediaUrl(thumbnail);
    #             }

    #             return { imageUrl: singleImage.data.link, submissionType: 'image' };
    #         } else {
    #             log.warn('Tried to parse this imgur url but failed: ', imageUrl);
    #             return null;
    #         }
    #     }
    # }


def main():
    while True:
        unreads = list(bot.inbox.unread(limit=None))

        for item in unreads:
            print("1")
            if "u/correktbot" in item.body.lower():
                #print(item.submission.title)
                #print(item.submission.url)
                print("hi")

                submission = item.submission
                gallery = getImages(submission)

                print(gallery)

                data = {"srcs": gallery, "api_key": API_KEY}
                r = requests.post(url=IMAGE_ENDPOINT, json=data)
                if r.status_code == 200:
                    paste = r.json()
                    comment = ""
                    for i, src in enumerate(gallery):
                        data = paste[src]
                        if data["ai_probability"] >= 50:
                            comment += str(i+1) + ") There's a " + str(data["ai_probability"]) + "% chance this is AI generated." +  "\n"
                        elif data["ai_probability"] < 50:
                            comment += str(i+1) + ") There is a low chance this is AI generated." + "\n"
                        else:
                            comment += str(i+1) + data["error"] + "\n"
                    comment += "We are currently in alpha testing. Join our Discord server to learn more! [https://discord.gg/Hj9ffKm9ny]"
                    item.reply(comment)
                elif r.status_code == 400:
                    time.sleep(20)
                    paste = r.json()
                    comment = ""
                    for i, src in enumerate(gallery):
                        data = paste[src]
                        if data["ai_probability"] >= 50:
                            comment += str(i+1) + ") There's a " + str(data["ai_probability"]) + "% chance this is AI generated." +  "\n"
                        elif data["ai_probability"] < 50:
                            comment += str(i+1) + ") There is a low chance this is AI generated." + "\n"
                        else:
                            comment += str(i+1) + data["error"] + "\n"
                    comment += "We are currently in alpha testing. Join our Discord server to learn more! [https://discord.gg/Hj9ffKm9ny]"
                    item.reply(comment)
                else:
                    print(r.status_code)
                time.sleep(1)
                    
        bot.inbox.mark_read(unreads)

        time.sleep(10)

main()
